
from DUT import DUT
from staf import STAF

class Server(object):

    def __init__(self):
        #DUT instance list for DUT management
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
        #add DUT
        print("Add DUT: %s" % ip)
        self.DUTs[ip] = DUT(self.staf_instance, ip, name)
        
    def remove_DUT(self, ip):
        print("Remove DUT: %s" % ip)
        DUT_instance = self.DUTs[ip]
        #stop DUT task runner thread
        DUT_instance.stop_task_runner()
        #remove it from server DUT list
        del self.DUTs[ip]

        