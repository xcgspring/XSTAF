
import logger
from workspace import WorkSpace
from staf import STAFInstance

class Server(object):
    '''
    server is the enter point of control layer
    server is response for check and start STAF, and manage workspace
    '''
    def __init__(self):
        #settings
        self.settings = {
            "STAFDir" : r"c:\staf",
        }

        self.workspace = None

    def config_staf(self):
        STAFInstance.config(STAFDir=self.settings["STAFDir"])
        STAFInstance.check()
        return STAFInstance.status

    @staticmethod
    def start_staf():
        STAFInstance.start()
        return STAFInstance.status

    def apply_settings(self, **kwargs):
        for arg in kwargs.items():
            if arg[0] in self.settings:
                self.settings[arg[0]] = arg[1]

    def get_settings(self, index):
        if index in self.settings:
            return self.settings[index]
        else:
            return None

    @staticmethod
    def is_default_workspace_exist():
        #to handle existing default workspace
        return WorkSpace.check_default_exist()

    def is_current_workspace_default(self):
        #check if current workspace is in default location
        if self.workspace is None:
            return False
        else:
            return self.workspace.check_current_default()

    @staticmethod
    def clean_default_workspace():
        WorkSpace.clean_default()

    def new_workspace(self):
        #new and load workspace will change workspace object in server
        #ui need prompt user to save original workspace before new or load new workspace
        workspace = WorkSpace()
        workspace.new()
        self.workspace = workspace

    def load_workspace(self, workspace_path=""):
        #new and load workspace will change workspace object in server
        #ui need prompt user to save original workspace before new or load new workspace
        if not workspace_path:
            workspace_path = WorkSpace.DefaultWorkspacePath

        workspace = WorkSpace()
        workspace.load(workspace_path)
        self.workspace = workspace

    def save_workspace(self, workspace_path=""):
        #save current workspace to workspace_path
        self.workspace.save(workspace_path)

    def DUTs(self):
        if not self.workspace is None:
            for DUT in self.workspace.DUTs.items():
                yield DUT[1]

    def get_DUT(self, ip):
        if not self.workspace is None:
            return self.workspace.DUTs[ip]

    def has_DUT(self, ip):
        if not self.workspace is None:
            return self.workspace.has_DUT(ip)

    def add_DUT(self, ip, name):
        if not self.workspace is None:
            self.workspace.add_DUT(ip, name)

    def remove_DUT(self, ip):
        if not self.workspace is None:
            self.workspace.remove_DUT(ip)