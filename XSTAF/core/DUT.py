
import os
import Queue
import uuid
import time
import socket
import traceback
from PyQt4 import QtCore

from XSTAF.core.logger import LOGGER
from XSTAF.core.test_manage import TestSuite, Run
from XSTAF.core.staf import STAFInstance

class CustomQueue(Queue.Queue):
    #custom queue basing on dict

    def _init(self, maxsize):
        self.queue = {}
        self._last_task = None

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
        self._last_task = self.queue.pop(indexs[0])
        return self._last_task
        
    def last_task(self):
        #last task is under process, other task are waiting
        return self._last_task
        
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
        
    def __contains__(self, task):
        self.mutex.acquire()
        for index, in_task in self.queue.items():
            if task is in_task:
                self.mutex.release()
                return True
        self.mutex.release()
        return False

        
class DUTTaskRunner(QtCore.QThread):
    #signal to update DUT ui
    test_result_change = QtCore.SIGNAL("testResultChange")
    #task queue change
    runner_busy = QtCore.SIGNAL("runnerBusy")
    #task queue idle
    runner_idle = QtCore.SIGNAL("runnerIdle")
    
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
        
        #task cancel flag
        self._cancel_task = False
        
    def start(self):
        LOGGER.info("DUT task runner thread for IP %s start" % self.DUT_instance.ip)
        QtCore.QThread.start(self)
        
    def terminate(self):
        LOGGER.info("DUT task runner thread for IP %s terminate" % self.DUT_instance.ip)
        QtCore.QThread.terminate(self)
        
    def cancel_task(self):
        self._cancel_task = True
        
    def run_task(self, work, run):
        #lock DUT
        LOGGER.debug("    Step1: Lock DUT, DUT: %s" % self.DUT_instance.ip)
        self.staf_handle.lock_DUT(self.DUT_instance.ip)
        #clean previous process info
        LOGGER.debug("    Step2: free process info")
        self.staf_handle.free_process_status(self.DUT_instance.ip)
        #create some directories
        LOGGER.debug("    Step3: create log directory and tmp files location")
        self.staf_handle.create_directory(self.DUT_instance.ip, self.DUT_instance.get_settings("remote_log_location"))
        self.staf_handle.create_directory(self.DUT_instance.ip, self.DUT_instance.get_settings("remote_tmp_files_location"))
        self.staf_handle.clean_directory(self.DUT_instance.ip, self.DUT_instance.get_settings("remote_tmp_files_location"))
        #run case
        LOGGER.debug("    Step4: Run command, command: %s" % work.command)
        remote_log_file = os.path.join(self.DUT_instance.get_settings("remote_log_location"), str(work.ID), "%s_%s.log"%(work.name, run.start))
        self.staf_handle.start_process(self.DUT_instance.ip, work.command, remote_log_file)
        
        while True:
            #wait until process end or time out
            #check time out
            current_time = time.time()
            if current_time - float(run.start) > work.timeout:
                #stop the process
                self.staf_handle.stop_process(self.DUT_instance.ip)
                LOGGER.info("Time out encounter")
                run.result = run.Fail
                break
            
            #check if user manually cancel the test
            if self._cancel_task:
                #stop the process
                self.staf_handle.stop_process(self.DUT_instance.ip)
                LOGGER.info("User manually cancel task")
                run.result = run.NotRun
                break
                
            #check process status
            result = self.staf_handle.query_process_status(self.DUT_instance.ip)
            if not result is None:
                LOGGER.info("Process end, result: %s, end time: %s" % result)
                if int(result[0]) == 0:
                    run.result = run.Pass
                else:
                    run.result = run.Fail
                break
                
            #check the status every 1s
            time.sleep(1)
        
        #copy log
        local_log_location = os.path.join(self.DUT_instance.workspace_log_path, self.DUT_instance.ip, str(work.ID), run.start)
        if not os.path.isdir(local_log_location):
            os.makedirs(local_log_location)
        #copy stdout/stderr log
        LOGGER.debug("    Step5: Copy stdout/stderr logs")
        self.staf_handle.copy_log_file(self.DUT_instance.ip, remote_log_file, local_log_location)
        #copy tmp logs in remote global log location, and delete them after copy done
        LOGGER.debug("    Step6: Copy tmp logs")
        self.staf_handle.copy_tmp_log_directory(self.DUT_instance.ip, self.DUT_instance.get_settings("remote_tmp_files_location"), local_log_location)
        #run.log_location = local_log_location
        #release DUT
        LOGGER.debug("    Step7: Release DUT, DUT: %s" % self.DUT_instance.ip )
        self.staf_handle.release_DUT(self.DUT_instance.ip)
        
    def run(self):
        while True:
            self.emit(self.runner_idle)
            #get task from task queue
            work = self.task_queue.get(block=True)
            
            LOGGER.debug("Start task, Name: %s" % work.name)
            self.emit(self.runner_busy)
            run = Run()
            run.start = "%.3f" % time.time()
            work.add_run(run)
            #set cancel task to false
            self._cancel_task = False
            
            try:
                self.run_task(work, run)
            except:
                LOGGER.info(traceback.format_exc())
                run.result = run.Fail
                
            run.end = "%.3f" % time.time()
            #emit test result change signal, if manual case, ui should prompt user to change test result manually
            LOGGER.debug("emit test result change signal")
            self.emit(self.test_result_change, work.auto, run)
            
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
    #settings
    settings = {"remote_log_location" : r"c:\XSTAF",
                     "remote_tmp_files_location" : r"c:\XSTAF\tmpfiles",
                    }

    def __init__(self, workspace, ip, name=""):
        QtCore.QObject.__init__(self)
        self.workspace = workspace
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
        
    @classmethod
    def config(cls, **kwargs):
        for arg in kwargs.items():
            key = arg[0]
            value = arg[1]
            if key in cls.settings:
                cls.settings[key] = value
        
    def get_settings(self, key):
        return self.settings[key]
        
    @property
    def workspace_log_path(self):
        return os.path.join(self.workspace.workspace_path, self.workspace.TestLogFolder)
        
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
            
    def cancel_task(self):
        if not self.task_runner is None:
            self.task_runner.cancel_task()
            
    def clear_all_results(self):
        for testsuite in self.testsuites():
            for testcase in testsuite.testcases():
                testcase.remove_all_runs()

    ############################################
    #task suite management methods
    ############################################
    def has_testsuite(self, testsuite_name):
        return testsuite_name in self._testsuites
    
    def add_testsuite(self, testsuite_file):
        testsuite = TestSuite(testsuite_file)
        self._testsuites[testsuite.name] = testsuite

    def add_testsuite_object(self, testsuite):
        #used to move testsuite object from one dut to another
        self._testsuites[testsuite.name] = testsuite
        
    def remove_testsuite(self, testsuite_name):
        del self._testsuites[testsuite_name]
        
    def get_testsuite(self, testsuite_name):
        return self._testsuites[testsuite_name]
        
    def testsuites(self):
        testsuite_names = self._testsuites.keys()
        testsuite_names.sort()
        for testsuite_name in testsuite_names:
            yield self._testsuites[testsuite_name]
            
    def remove_testresult(self, testsuite_name, testcase_id, run_id):
        testsuite = self.get_testsuite(testsuite_name)
        testcase = testsuite.get_testcase(testcase_id)
        testcase.remove_run(run_id)
        
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
        
    def is_in_queue(self, testcase):
        return testcase in self.task_queue
        
    def last_task_in_queue(self):
        return self.task_queue.last_task()
        