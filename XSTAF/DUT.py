
import Queue
import threading

from test_manage import TestSuite, PyAnvilTestSuite

class DUTTaskRunner(threading.Thread):
    def __init__(self, staf_instance, ip):
        threading.Thread.__init__(self)
        self.ip = ip
        #task queue used to store task to process 
        self.task_queue = Queue.Queue()
        #result queue used to store task process results
        self.result_queue = Queue.Queue()
        
        #staf handle used to push task to DUT
        self.staf_handle = staf_instance.get_handle("%s_task_runner"%self.ip)
        #create and register staf handle
        assert(self.staf_handle.register())
        #configure the staf handle
        assert(self.staf_handle.configure())
        
    def run_task(self, work):
        print(work)
        pass
        
    def run(self):
        print("DUT task runner thread for IP %s start" % self.ip)
        while True:
            work = self.task_queue.get(block=True)
            if work == "stop":
                break
            self.run_task(work)
        print("DUT task runner thread for IP %s exit" % self.ip)
        
    def stop(self):
        print("DUT task runner thread for IP %s stopping" % self.ip)
        self.task_queue.put("stop")
    
class DUTMonitor(object):
    #DUT status
    #Unknown Failure
    UnknownFailure = 0b10000000
    #Invalid status, we cannot assign task to DUT under these status
    DUTStatusUnknown = 0b10000001
    DUTNotDetected = 0b10000010
    #locked by others, we only can do limited operations
    DUTLockedbyOthers = 0b10000011

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

    def __init__(self, staf_instance, ip):
    
        self.ip = ip
        self.status = self.DUTStatusUnknown
        
        #this staf handle is for checking DUT status, all use of this handle should be no blocking, not to freeze UI 
        self.staf_handle = staf_instance.get_handle("%s_monitor"%self.ip)
        #create and register staf handle
        assert(self.staf_handle.register())
        #configure the staf handle
        assert(self.staf_handle.configure())
        
    def DUT_status(self):
        '''
        return DUT status
        '''
        if not self.staf_handle.ping(self.ip):
            self.status = self.DUTNotDetected
            return self.status
            
        if self.staf_handle.check_if_DUT_locked(self.ip):
            self.status = self.DUTLockedbyOthers
            return self.status
            
        self.status = self.DUTNormal
        return self.status
        
    def DUT_pretty_status(self, status):
        '''
        return DUT pretty status
        '''
        return self.PrettyStatus[status]
        
class DUT(object):
    def __init__(self, staf_instance, ip, name):
        self.ip = ip
        self.name = name

        #start monitor
        self.monitor = DUTMonitor(staf_instance, self.ip)
        #start task runner
        self.task_runner = DUTTaskRunner(staf_instance, self.ip)
        
        #test suite list for manage test suite
        self.testsuites = {}
        
        #do some pre-loads
        self.task_runner.start()
        
    def refresh(self):
        #check DUT status
        self.status = self.monitor.DUT_status()
        self.pretty_status = self.monitor.DUT_pretty_status(self.status)
        
    def stop_task_runner(self):
        self.task_runner.stop()
        
    def add_testsuite(self, testsuite_file):
        testsuite = PyAnvilTestSuite(testsuite_file)
        self.testsuites[testsuite.name] = testsuite
        
        return testsuite
        
    def remove_testsuite(self, testsuite_name):
        del self.testsuites[testsuite_name]
        
    def info(self):
        pass
        
    def run_testsuite(self, testsuite):
        pass
        
    def run_testcase(self, testcase):
        pass
        
    def stop_running(self):
        pass
        
