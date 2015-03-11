
import os
import Queue
import uuid
import time
import socket
import logger
from PyQt4 import QtCore

from test_manage import TestSuite, Run
from staf import get_staf_instance

class CustomQueue(Queue.Queue):
    #custom queue basing on dict

    def _init(self, maxsize):
        self.queue = {}

    def _qsize(self, len=len):
        return len(self.queue)

    def _put(self, item):
        #use time stamp as index when putting item to queue
        index = "%.3f" % time.time()
        #sleep a little time to make index unique
        time.sleep(0.01)
        self.queue[index] = item
        logger.LOGGER.debug("Add task, Index: %s, task: %s" % (index, repr(item)) )

    def _get(self):
        #find oldest index and pop the item
        indexs = self.queue.keys()
        indexs.sort()
        logger.LOGGER.debug("Get task: %s" % indexs[0] )
        return self.queue.pop(indexs[0])
        
    def clear(self):
        self.not_empty.acquire()
        try:
            self.queue.clear()
            self.not_full.notify()
        finally:
            self.not_empty.release()
    
    def list(self):
        self.mutex.acquire()
        tasks = self.queue
        self.mutex.release()
        return tasks
        
    def remove(self, index):
        self.mutex.acquire()
        if index in self.queue:
            del self.queue[index]
            self.not_full.notify()
        self.mutex.release()
        
class DUTTaskRunner(QtCore.QThread):
    #signal to update DUT ui
    updateDUTUI = QtCore.SIGNAL("updateDUTUI")
    #signal thread exit
    #taskRunnerExit = QtCore.SIGNAL("taskRunnerExit")
    
    def __init__(self, DUT_instance):
        QtCore.QThread.__init__(self)
        self.DUT_instance = DUT_instance
        #task queue used to store task to process 
        self.task_queue = None
        
        #staf handle used to push task to DUT
        self.staf_handle = get_staf_instance().get_handle("%s_task_runner"%self.DUT_instance.ip)
        #create and register staf handle
        assert(self.staf_handle.register())
        #configure the staf handle
        assert(self.staf_handle.configure())
        
        #stop flag, runner thread will check this flag to determine if need stop
        self._stop_flag = False
        
        #remote log location
        self.remote_log_location = r"c:\XSTAF"
        self.remote_log_tmp_location = r"c:\XSTAF\tmplogs"
        
    def start(self):
        self._stop_flag = False
        self.prepare_DUT()
        QtCore.QThread.start(self)
        
    def prepare_DUT(self):
        #make some dirs
        self.staf_handle.create_directory(self.DUT_instance.ip, self.remote_log_tmp_location)
        
    def run_task(self, work):
        logger.LOGGER.debug("Start task, Name: %s" % work.name)
        
        run = Run()
        #start time
        run.start = "%.3f" % time.time()
        #init result
        run.result = run.Pass
        #lock DUT
        logger.LOGGER.debug("    Step1: Lock DUT, DUT: %s" % self.DUT_instance.ip)
        if not self.staf_handle.lock_DUT(self.DUT_instance.ip):
            run.result = run.Fail
            run.status = "Lock DUT Fail\n"
        else:
            #run case
            logger.LOGGER.debug("    Step2: Run command, command: %s" % work.command)
            remote_log_file = os.path.join(self.remote_log_location, str(work.ID), "%s_%s.log"%(work.name, run.start) )
            if not self.staf_handle.start_process(self.DUT_instance.ip, work.command, remote_log_file):
                run.result = run.Fail
                run.status = "Test Run Fail\n"
                
            #copy log
            local_log_location = os.path.join(self.DUT_instance.workspace_log_path, str(work.ID))
            if not os.path.isdir(local_log_location):
                os.makedirs(local_log_location)
            logger.LOGGER.debug("    Step3: Copy logs")
            
            #copy stdout/stderr log
            logger.LOGGER.debug("    Step3.1: Copy stdout/stderr logs")
            if not self.staf_handle.copy_log_file(self.DUT_instance.ip, remote_log_file, local_log_location):
                run.result = run.Fail
                run.status = run.status+"Copy stdout/stderr logs Fail\n"
                
            #copy tmp logs in remote global log location, and delete them after copy done
            logger.LOGGER.debug("    Step3.2: Copy tmp logs")
            if not self.staf_handle.copy_tmp_log_directory(self.DUT_instance.ip, self.remote_log_tmp_location, local_log_location):
                run.result = run.Fail
                run.status = run.status+"Copy tmp logs Fail\n"

            run.log_location = local_log_location
                
        #release DUT
        logger.LOGGER.debug("    Step4: Release DUT, DUT: %s" % self.DUT_instance.ip )
        if not self.staf_handle.release_DUT(self.DUT_instance.ip):
            run.result = run.Fail
            run.status = run.status+"Release DUT Fail\n"

        run.end = "%.3f" % time.time()
        
        #add this run to work, index using start time
        work.runs[run.start] = run
        
        #emit update ui signal
        self.emit(self.updateDUTUI)
        
    def run(self):
        logger.LOGGER.debug("DUT task runner thread for IP %s start" % self.DUT_instance.ip)
        while True:
            #check stop flag
            if self._stop_flag:
                break
            
            #run task
            work = self.task_queue.get(block=True)
            self.run_task(work)
        
        #emit thread edit signal
        #self.emit(self.taskRunnerExit)
        
        logger.LOGGER.debug("DUT task runner thread for IP %s exit" % self.DUT_instance.ip)
        
    def pause(self):
        logger.LOGGER.debug("DUT task runner thread for IP %s stopping" % self.DUT_instance.ip)
        self._stop_flag = True
    
class DUTMonitor(object):
    #DUT status
    #Unknown Failure
    UnknownFailure = 0b10000000
    #Invalid status, we cannot assign task to DUT under these status
    DUTStatusUnknown = 0b10000001
    DUTNotDetected = 0b10000010
    #locked by others, we only can do limited operations
    DUTLockedbyOthers = 0b01000001

    #Normal status, we have full DUT control
    DUTNormal = 0b00000001
    
    #pretty status list
    PrettyStatus = {
        UnknownFailure : "Unknown failure",
        DUTStatusUnknown : "Status unknown",
        DUTNotDetected : "DUT not detected",
        DUTLockedbyOthers : "DUT Locked by others",
        DUTNormal : "DUT normal",
    }

    def __init__(self, DUT_instance):
    
        self.DUT_instance = DUT_instance
        self.status = self.DUTStatusUnknown
        
        #this staf handle is for checking DUT status, all use of this handle should be no blocking, not to freeze UI 
        self.staf_handle = get_staf_instance().get_handle("%s_monitor"%self.DUT_instance.ip)
        #create and register staf handle
        assert(self.staf_handle.register())
        #configure the staf handle
        assert(self.staf_handle.configure())
        
    def DUT_status(self):
        '''
        return DUT status
        '''
        if not self.staf_handle.ping(self.DUT_instance.ip):
            self.status = self.DUTNotDetected
            return self.status
            
        if self.staf_handle.check_if_DUT_locked(self.DUT_instance.ip):
            self.status = self.DUTLockedbyOthers
            return self.status
            
        self.status = self.DUTNormal
        return self.status
        
    @classmethod
    def DUT_pretty_status(cls, status):
        '''
        return DUT pretty status
        '''
        return cls.PrettyStatus[status]
        
class DUT(object):
    def __init__(self, workspace_log_path, ip, name=""):
        self.workspace_log_path = workspace_log_path
        self.ip = ip
        self.name = name
        
        #monitor
        self.monitor = None
        #task runner
        self.task_runner = None
        #task queue
        self.task_queue = CustomQueue()
        
        #test suite list for manage test suite
        self.testsuites = {}
        
        #init status
        self.status = DUTMonitor.DUTStatusUnknown
        self.pretty_status = DUTMonitor.DUT_pretty_status(self.status)
        
    def add_monitor(self):
        #add monitor if needed
        if self.monitor is None:
            self.monitor = DUTMonitor(self)
            
    def add_runner(self):
        if self.task_runner is None:
            self.task_runner = DUTTaskRunner(self)
            self.task_runner.task_queue = self.task_queue
        
    def refresh(self):
        #check DUT status
        self.status = self.monitor.DUT_status()
        self.pretty_status = self.monitor.DUT_pretty_status(self.status)
        
        #auto name DUT
        if not self.name and not(self.status & 0b10000000) :
            self.name = socket.gethostbyaddr(self.ip)[0]
        
    def start_task_runner(self):
        if not self.task_runner is None:
            self.task_runner.start()
        
    def pause_task_runner(self):
        if not self.task_runner is None:
            self.task_runner.pause()
        
    def add_testsuite(self, testsuite_file):
        testsuite = TestSuite(testsuite_file)
        self.testsuites[testsuite.name] = testsuite
        return testsuite
        
    def remove_testsuite(self, testsuite_name):
        del self.testsuites[testsuite_name]
        
    def clean_task_queue(self):
        self.task_queue.clear()
        
    def list_all_tasks_in_task_queue(self):
        return self.task_queue.list()
        
    def add_testcase_to_task_queue(self, testsuite_name, testcase_id):
        testcase = self.testsuites[testsuite_name].testcases[testcase_id]
        self.task_queue.put(testcase)
        
    def add_testsuite_to_task_queue(self, testsuite_name):
        for testcase in self.testsuites[testsuite_name].testcases.items():
            self.task_queue.put(testcase[1])
        
    def remove_testcase_from_task_queue(self, id):
        self.task_queue.remove(id)
        
        
        
        
