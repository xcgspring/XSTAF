
from DUT import createDUT
from staf import STAF

class Server(object):

    def __init__(self):
        #DUT list
        self.DUTs = {}
        #settings
        self.settings = {
            "STAF_dir" : r"c:\staf",
        }
        #staf instance
        self.staf_instance = None
        
    def update_settings(self, **kwargs):
        for arg in kwargs.items():
            if arg[0] in self.settings:
                self.settings[arg[0]] = arg[1]
        
    def check_and_start_staf(self):
        self.staf_instance = STAF(self.settings["STAF_dir"])
        assert(self.staf_instance.check_and_start_staf())
        
    def has_DUT(self, ip):
        return (ip in self.DUTs)
        
    def add_DUT(self, ip, name):
        #add DUT will create a new thread for DUT
        DUT_thread = createDUT(self.staf_instance, ip, name)
        #start thread
        DUT_thread.start()
        #add queue to server dict, for controlling DUT later
        self.DUTs[ip] = DUT_thread
        
    def remove_DUT(self, ip):
        print("Remove DUT: %s" % ip)
        DUT_thread = self.DUTs[ip]
        #remove it from server DUT list
        del self.DUTs[ip]
        #stop thread
        DUT_thread.stop()
        