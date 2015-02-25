
from DUT import DUT
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
        
    def start_message_processer(self):
        pass
        
    def add_DUT(self, ip):
        pass
        
    def remove_DUT(self, ip):
        pass
        