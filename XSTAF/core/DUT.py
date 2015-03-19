
import os
import Queue
import uuid
import time
import socket
from PyQt4 import QtCore

from XSTAF.core.logger import LOGGER
from XSTAF.core.test_manage import TestSuite, Run
from XSTAF.core.staf import STAFInstance

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
        LOGGER.debug("Add task, Index: %s, task: %s" % (index, repr(item)) )

    def _get(self):
        #find oldest index and pop the item
        indexs = self.queue.keys()
        indexs.sort()
        LOGGER.debug("Get task: %s" % indexs[0] )
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
    test_result_change = QtCore.SIGNAL("testResultChange")
    #task queue change
    task_queue_change = QtCore.SIGNAL("taskQueueChange")
    
    def __init__(self, DUT_instance):
        QtCore.QThread.__init__(self)
        self.DUT_instance = DUT_instance
        #task queue used to store task to process 
        self.task_queue = None
        
        #staf handle used to push task to DUT
        self.staf_handle = STAFInstance.get_handle("%s_task_runner"%self.DUT_instance.ip)
        #create and register staf handle
        assert(self.staf_handle.register())
        #configure the staf handle
        assert(self.staf_handle.configure())
        
        #remote log location
        self.remote_log_location = r"c:\XSTAF"
        self.remote_log_tmp_location = r"c:\XSTAF\tmplogs"
        
    def start(self):
        LOGGER.info("DUT task runner thread for IP %s start" % self.DUT_instance.ip)
        self.prepare_DUT()
        QtCore.QThread.start(self)
        
    def terminate(self):
        LOGGER.info("DUT task runner thread for IP %s terminate" % self.DUT_instance.ip)
        QtCore.QThread.terminate(self)
        
    def prepare_DUT(self):
        #make some dirs
        self.staf_handle.create_directory(self.DUT_instance.ip, self.remote_log_tmp_location)
        
    def run_task(self, work):
        LOGGER.debug("Start task, Name: %s" % work.name)
        
        run = Run()
        #start time
        run.start = "%.3f" % time.time()
        #init result
        run.result = run.Pass
        #lock DUT
        LOGGER.debug("    Step1: Lock DUT, DUT: %s" % self.DUT_instance.ip)
        if not self.staf_handle.lock_DUT(self.DUT_instance.ip):
            run.result = run.Fail
            run.status = "Lock DUT Fail\n"
        else:
            #run case
            LOGGER.debug("    Step2: Run command, command: %s" % work.command)
            remote_log_file = os.path.join(self.remote_log_location, str(work.ID), "%s_%s.log"%(work.name, run.start) )
            if not self.staf_handle.start_process(self.DUT_instance.ip, work.command, remote_log_file):
                run.result = run.Fail
                run.status = "Test Run Fail\n"
                
            #copy log
            local_log_location = os.path.join(self.DUT_instance.workspace_log_path, str(work.ID))
            if not os.path.isdir(local_log_location):
                os.makedirs(local_log_location)
            LOGGER.debug("    Step3: Copy logs")
            
            #copy stdout/stderr log
            LOGGER.debug("    Step3.1: Copy stdout/stderr logs")
            if not self.staf_handle.copy_log_file(self.DUT_instance.ip, remote_log_file, local_log_location):
                run.result = run.Fail
                run.status = run.status+"Copy stdout/stderr logs Fail\n"
                
            #copy tmp logs in remote global log location, and delete them after copy done
            LOGGER.debug("    Step3.2: Copy tmp logs")
            if not self.staf_handle.copy_tmp_log_directory(self.DUT_instance.ip, self.remote_log_tmp_location, local_log_location):
                run.result = run.Fail
                run.status = run.status+"Copy tmp logs Fail\n"

            run.log_location = local_log_location
                
        #release DUT
        LOGGER.debug("    Step4: Release DUT, DUT: %s" % self.DUT_instance.ip )
        if not self.staf_handle.release_DUT(self.DUT_instance.ip):
            run.result = run.Fail
            run.status = run.status+"Release DUT Fail\n"

        run.end = "%.3f" % time.time()
        
        #add this run to work, index using start time
        work.add_run(run)
        
        #emit update ui signal
        self.emit(self.test_result_change)
        
    def run(self):
        while True:
            #run task
            work = self.task_queue.get(block=True)
            self.emit(self.task_queue_change)
            self.run_task(work)
    
class DUTMonitor(object):
    #DUT status
    #Invalid status, we cannot assign task to DUT under these status
    DUTStatusUnknown = 0b10000000
    #Unknown Failure
    UnknownFailure = 0b10000001
    DUTNotDetected = 0b10000010
    #locked by others, we only can do limited operations
    DUTLockedbyOthers = 0b01000001

    #Normal status, we have full DUT control
    DUTNormal = 0b00000000
    
    #pretty status list
    PrettyStatus = {
        UnknownFailure : "Unknown failure",
        DUTStatusUnknown : "Status unknown",
        DUTNotDetected : "DUT not detected",
        DUTLockedbyOthers : "DUT Locked by others",
        DUTNormal : "DUT normal",
    }

    def __init__(self, dut):
        self.dut = dut
        self._status = self.DUTStatusUnknown
        
        #this staf handle is for checking DUT status, all use of this handle should be no blocking, not to freeze UI 
        self.staf_handle = STAFInstance.get_handle("%s_monitor"%self.dut.ip)
        #create and register staf handle
        self.staf_handle.register()
        #configure the staf handle
        self.staf_handle.configure()
        
    def check_status(self):
        if not self.staf_handle.ping(self.dut.ip):
            self._status = self.DUTNotDetected
            return self._status
        if self.staf_handle.check_if_DUT_locked(self.dut.ip):
            self._status = self.DUTLockedbyOthers
            return self._status
        self._status = self.DUTNormal
        return self._status
        
    @classmethod
    def pretty_status(cls, status):
        return cls.PrettyStatus[status]

class DUT(QtCore.QObject):

    #DUT status change should update ui
    status_change = QtCore.SIGNAL("DUTStatusChange")

    def __init__(self, workspace_log_path, ip, name=""):
        QtCore.QObject.__init__(self)
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
        self._testsuites = {}
        
        self.status = DUTMonitor.DUTStatusUnknown
        self.pretty_status = DUTMonitor.pretty_status(self.status)
        
    ############################################
    #monitor and task runner related methods
    ############################################
    def add_monitor(self):
        if STAFInstance.status & 0b10000000:
            LOGGER.error("Can not add DUT monitor, local STAF not ready")
            return
            
        #add monitor if needed
        if self.monitor is None:
            self.monitor = DUTMonitor(self)
    
    def remove_monitor(self):
        self.monitor = None
        
    def get_monitor_status(self):
        if not self.monitor is None:
            self.status = self.monitor.check_status()
            self.pretty_status = DUTMonitor.pretty_status(self.status)
        else:
            self.status = DUTMonitor.DUTStatusUnknown
            self.pretty_status = DUTMonitor.pretty_status(self.status)
        
        LOGGER.debug("DUT IP: %s Name %s Status %s", self.ip, self.name, self.pretty_status)
        self.emit(self.status_change)
        
    def add_runner(self):
        if STAFInstance.status & 0b10000000:
            LOGGER.error("Can not add DUT task runner, local STAF not ready")
            return

        if self.status & 0b11000000:
            LOGGER.error("Can not add DUT task runner, DUT not ready")
            return
            
        if self.task_runner is None:
            self.task_runner = DUTTaskRunner(self)
            self.task_runner.task_queue = self.task_queue

    def get_runner(self):
        return self.task_runner
            
    def start_runner(self):
        '''
        start task runner
        '''
        if not self.task_runner is None:
            self.task_runner.start()
        
    def stop_runner(self):
        '''
        check DUT status
        '''
        if not self.task_runner is None:
            self.task_runner.terminate()
            
    def remove_runner(self):
        self.stop_runner()
        self.runner = None
        
    def is_runner_running(self):
        if self.task_runner is None:
            return False
        else:
            return self.task_runner.isRunning()

    ############################################
    #task suite management methods
    ############################################
    def has_testsuite(self, testsuite_name):
        return testsuite_name in self._testsuites
    
    def add_testsuite(self, testsuite_file):
        testsuite = TestSuite(testsuite_file)
        self._testsuites[testsuite.name] = testsuite
        
    def remove_testsuite(self, testsuite_name):
        del self._testsuites[testsuite_name]
        
    def get_testsuite(self, testsuite_name):
        return self._testsuites[testsuite_name]
        
    def testsuites(self):
        for testsuite_item in self._testsuites.items():
            yield testsuite_item[1]
        
    ############################################
    #task queue methods
    ############################################
    def clean_task_queue(self):
        self.task_queue.clear()
        
    def list_all_tasks_in_task_queue(self):
        return self.task_queue.list()
        
    def add_testcase_to_task_queue(self, testsuite_name, testcase_id):
        testcase = self.get_testsuite(testsuite_name).get_testcase(testcase_id)
        self.task_queue.put(testcase)
        
    def add_testsuite_to_task_queue(self, testsuite_name):
        for testcase in self.get_testsuite(testsuite_name).testcases():
            self.task_queue.put(testcase)
        
    def remove_testcase_from_task_queue(self, id):
        self.task_queue.remove(id)
        