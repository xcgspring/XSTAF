
from PyQt4 import QtCore

import logger
from workspace import WorkSpace
from staf import STAFInstance

class Server(QtCore.QObject):
    '''
    server is the enter point of control layer
    server is response for check and start STAF, and manage workspace
    '''
    #STAF status change should change main window ui and DUT ui
    #STAF status signal contains STAF status
    staf_status_change = QtCore.SIGNAL("STAFStatusChange")
    
    def __init__(self):
        QtCore.QObject.__init__(self)
        #settings
        self.settings = {
            "STAFDir" : r"c:\staf",
        }

        self._workspace = None

    def apply_settings(self, **kwargs):
        for arg in kwargs.items():
            if arg[0] in self.settings:
                self.settings[arg[0]] = arg[1]

    def get_settings(self, index):
        if index in self.settings:
            return self.settings[index]
        else:
            return None
        
    ############################################
    #STAF related methods
    ############################################
    def config_staf(self):
        STAFInstance.config(STAFDir=self.settings["STAFDir"])
        STAFInstance.check()
        self.emit(self.staf_status_change, STAFInstance.status)
        return STAFInstance.status

    def start_staf(self):
        STAFInstance.start()
        self.emit(self.staf_status_change, STAFInstance.status)
        return STAFInstance.status

    ############################################
    #workspace management methods
    #current only support one workspace, load another workspace will replace current workspace
    ############################################
    @staticmethod
    def is_default_workspace_exist():
        return WorkSpace.is_default_exist()
    
    def has_workspace(self):
        return not (self._workspace is None)
    
    def add_workspace(self):
        #new and load workspace will change workspace object in server
        #ui need prompt user to save original workspace before new or load new workspace
        workspace = WorkSpace()
        workspace.new()
        self._workspace = workspace

    def remove_workspace(self):
        self._workspace = None
        
    def get_workspace(self):
        return self._workspace
    
