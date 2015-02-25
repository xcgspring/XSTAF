
import threading

class Processer(threading.Thread):
    def __init__(self, staf_instance):
        threading.Thread.__init__(self)
        
        self.staf_instance = staf_instance
        
    def run(self):
        while True:
            message = self.staf_instance.get_message()
            self.process_message(message)
            
    def process_message(self, message):
        pass
        #self.staf_instance.start_process(DUT, command)
    
    