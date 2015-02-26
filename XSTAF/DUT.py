
import Queue
import threading

class DUT(threading.Thread):
    
    def __init__(self, staf_instance, queue, ip, name):
        threading.Thread.__init__(self)

        self.staf_instance = staf_instance
        self.queue = queue
        
        self.testsuites = []
        
        self.ip = ip
        self.name = name
        
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
    dut = DUT(staf_instance, queue, ip, name)
    
    return queue, dut