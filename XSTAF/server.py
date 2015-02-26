
from DUT import createDUT
from staf import STAF
from message_processer import Processer

class Server(object):

    def __init__(self):
        #
        self.DUTs = {}
        #staf instance, used to communicate with staf service
        self.staf_instance = None
        self.staf_dir = r"c:\staf"
        
    def init_STAF(self):
        self.staf_instance = STAF(self.staf_dir)
        assert(self.staf_instance.check_staf())
        assert(self.staf_instance.connect_staf())
        assert(self.staf_instance.configure_staf())
        print("STAF handle register to STAF service")
        
    def start_message_processer(self):
        pass
        
    def add_DUT(self, ip, name):
        #add DUT will create a new thread for DUT
        queue, DUT_thread = createDUT(self.staf_instance, ip, name)
        #start thread
        DUT_thread.start()
        #add queue to server dict, for controlling DUT later
        self.DUTs[ip] = (queue, DUT_thread)
        
    def remove_DUT(self, ip):
        pass
        