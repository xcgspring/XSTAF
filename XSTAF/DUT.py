
import Queue
import threading

class DUT(threading.Thread):
    #DUT status
    #Invalid status, we cannot assign task to DUT under these status
    DUTStatusUnknown = 0b10000001
    STAFHandleRegisterFail = 0b10000010
    DUTNotDetected = 0b10000011
    DUTLockedbyOthers = 0b10000100

    #Normal status, we can assign task to DUT
    DUTIdle = 0b00000001
    DUTBusy = 0b00000010
    
    #pretty status list
    PrettyStatus = {
        DUTStatusUnknown : "Unknown",
        STAFHandleRegisterFail : "STAF handle register fail",
        DUTNotDetected : "DUT not detected",
        DUTLockedbyOthers : "DUT Locked by others",
        DUTIdle : "DUT idle",
        DUTBusy : "DUT Busy",
    }
    
    def __init__(self, staf_handle, queue, ip, name):
        threading.Thread.__init__(self)

        self.staf_handle = staf_handle
        self.queue = queue
        self.ip = ip
        self.name = name
        
        self.testsuites = {}
        self.status = self.DUTStatusUnknown
        
        self._init_and_set_status()
        
    def _init_and_set_status(self):
        #create and register staf handle
        if not self.staf_handle.register():
            self.status = self.STAFHandleRegisterFail
            return
        
        #configure the staf handle
        assert(self.staf_handle.configure())
        
        #check DUTstatus
        self.DUT_status()
        
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
            
        self.status = self.DUTIdle
        return self.status
        
    def DUT_pretty_status(self):
        '''
        return DUT pretty status
        '''
        return self.PrettyStatus[self.DUT_status()]
        
    def run(self):
        print("DUT thread for IP %s start" % self.ip)
        while True:
            work = self.queue.get(block=True)
            if work == "stop":
                break
            self.do_work(work)
        print("DUT thread for IP %s exit" % self.ip)
            
    def stop(self):
        print("DUT thread for IP %s stopping" % self.ip)
        self.queue.put("stop")
            
    def do_work(self, work):
        print(work)
        pass
        
    def add_testsuite(self, testsuite):
        pass
        
    def remove_testsuite(self, testsuite):
        pass
        
    def info(self):
        pass
        
    def run_testsuite(self, testsuite):
        pass
        
    def run_testcase(self, testcase):
        pass
        
    def stop_running(self):
        pass
        
def createDUT(staf_instance, ip, name):
    queue = Queue.Queue()
    staf_handle = staf_instance.get_handle(ip)
    return DUT(staf_handle, queue, ip, name)
