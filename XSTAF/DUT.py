
import threading

class DUT(threading.Thread):
    
    def __init__(self, staf_instance, queue, ip, name=None):
        threading.Thread.__init__(self)

        self.staf_instance = staf_instance
        self.queue = queue
        
        self.testsuites = []
        
        self.ip = ip
        self.name = name
        
    def run(self):
        while True:
            work = self.queue.get(block=True)
            self.do_work(work)
            
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