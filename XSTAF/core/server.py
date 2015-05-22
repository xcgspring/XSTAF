
import os
import pickle
from PyQt4 import QtCore

from XSTAF.core.logger import LOGGER
from XSTAF.core.workspace import WorkSpace
from XSTAF.core.staf import STAFInstance
from XSTAF.core.tool_manage import ToolManager
from XSTAF.core.DUT import DUT

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
        self.default_settings = {
            #logger
            "LogLocation" : r"c:\XSTAF\XSTAF.log",
            "LoggerLevelFile" : "DEBUG",
            "LoggerLevelStream" : "INFO",
            #STAF
            "STAFDir" : r"c:\staf",
            #workspace
            "WorkspaceLocation" : r"c:\XSTAF\workspaces",
            #tools dir
            "ToolsLocation" : r"tools",
            "ToolsConfigureFile" : "config.pickle",
            #DUT
            "remote_log_location" : r"c:\XSTAF",
            "remote_tmp_files_location" : r"c:\XSTAF\tmpfiles",
        }
        
        #settings save file
        self._settings_save_file = r"c:\XSTAF\XSTAF_settings.pickle"
        #try load saved setting
        self.load_saved_settings()

        self._workspace = None
        self.tool_manager = ToolManager()

    def apply_settings(self, **kwargs):
        for arg in kwargs.items():
            if arg[0] in self.settings:
                self.settings[arg[0]] = arg[1]

    def get_settings(self, index):
        if index in self.settings:
            return self.settings[index]
        else:
            return None
    
    def load_saved_settings(self):
        if not os.path.isfile(self._settings_save_file):
            self.settings = self.default_settings
        else:
            with open(self._settings_save_file, 'r') as f:
                self.settings = pickle.load(f)
        
    def save_settings(self):
        path = os.path.dirname(self._settings_save_file)
        if not os.path.isdir(path):
            os.makedirs(path)
            
        with open(self._settings_save_file, 'w') as f:
            pickle.dump(self.settings, f)
            
    def load_default_settings(self):
        self.settings = self.default_settings
    
    def config(self):
        self.config_logger()
        self.config_staf()
        self.config_workspace()
        self.config_tool()
        self.config_dut()
        self.save_settings()
        
    ############################################
    #logger related methods
    ############################################
    def config_logger(self):
        LOGGER.config(logging_level_file = self.settings["LoggerLevelFile"],
                            logging_level_stream = self.settings["LoggerLevelStream"],
                            logging_file = self.settings["LogLocation"])
    
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

    def check_staf(self):
        STAFInstance.check()
        self.emit(self.staf_status_change, STAFInstance.status)
        return STAFInstance.status
    ############################################
    #workspace management methods
    #current only support one workspace, load another workspace will replace current workspace
    ############################################
    def config_workspace(self):
        WorkSpace.config(WorkspaceLocation = self.settings["WorkspaceLocation"])

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
    
    ############################################
    #tool management methods
    ############################################
    def config_tool(self):
        self.tool_manager.apply_settings(ToolsLocation=self.settings["ToolsLocation"], 
                                            ToolsConfigureFile=self.settings["ToolsConfigureFile"])
        self.tool_manager.config()
    
    def loaded_tools(self):
        #yield tools server current has
        for tool_name in self.tool_manager.tool_name_list:
            tool = self.tool_manager.get_tool(tool_name)
            if not tool is None:
                yield tool_name, tool

    def available_tools(self):
        #yield all available tools
        for tool_name in self.tool_manager.available_tool_name_list:
            tool = self.tool_manager.get_tool(tool_name)
            if not tool is None:
                yield tool_name, tool
                
    def add_tool(self, tool_name):
        #add tool to server
        if not tool_name in self.tool_manager.tool_name_list:
            self.tool_manager.tool_name_list.append(tool_name)
            self.tool_manager.save_config()
    
    def remove_tool(self, tool_name):
        #remove tool from server
        if tool_name in self.tool_manager.tool_name_list:
            self.tool_manager.tool_name_list = [name for name in self.tool_manager.tool_name_list if name != tool_name]
            self.tool_manager.save_config()
    
    def remove_all_tools(self):
        self.tool_manager.tool_name_list = []
        self.tool_manager.save_config()
    
    ############################################
    #DUT management methods
    ############################################
    def config_dut(self):
        DUT.config(remote_log_location=self.settings["remote_log_location"], remote_tmp_files_location=self.settings["remote_tmp_files_location"])
        
    ############################################
    #Setting save file
    ############################################