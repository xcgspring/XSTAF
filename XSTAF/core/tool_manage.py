
import os
import sys
import pickle

from XSTAF.core.logger import LOGGER

class ToolManager(object):

    def __init__(self):
        self.settings = {"ToolsLocation" : r"tools",
                        "ToolsConfigureFile" : "config.pickle"}
                        
        self.tool_name_list = []
        self.abs_tools_location = ""
        self.pickle_config_file = ""

    def apply_settings(self, **kwargs):
        for arg in kwargs.items():
            if arg[0] in self.settings:
                self.settings[arg[0]] = arg[1]

    def config(self):
        tools_location = self.settings["ToolsLocation"]
        if not os.path.isabs(tools_location):
            #check if tools location exist in XSTAF path
            XSTAF_path = os.path.dirname(os.path.abspath(__file__))
            abs_tools_location = os.path.join(XSTAF_path, "..", tools_location)
        else:
            abs_tools_location = tools_location
                
        if not os.path.isdir(abs_tools_location):
            LOGGER.warning("Can not find tools location: %s", abs_tools_location)
            return
            
        #append abs tools path to python lib path
        #so we can dynamic import them
        self.abs_tools_location = abs_tools_location
        sys.path.append(abs_tools_location)
        
        #try get tools name list from pickle file
        pickle_config_file = os.path.join(abs_tools_location, self.settings["ToolsConfigureFile"])
        if not os.path.isfile(pickle_config_file):
            LOGGER.warning("Can not find config file: %s", pickle_config_file)
        
        self.pickle_config_file = pickle_config_file
        self.load_config()

    def get_tool(self, tool_name):
        try:
            tool = __import__(tool_name).Tool
        except (ImportError, AttributeError):
            LOGGER.warning("Can not import tool: %s" % tool_name)
            return None
        else:
            return tool
            
    def load_config(self):
        #we load tool names from pickle file
        if os.path.isfile(self.pickle_config_file):
            with open(self.pickle_config_file, 'r') as f:
                self.tool_name_list = pickle.load(f)
        
    def save_config(self):
        #we save current tool names to pickle file
        with open(self.pickle_config_file, 'w') as f:
            pickle.dump(self.tool_name_list, f)
        
    @property
    def available_tool_name_list(self):
        #check all packages under abs_tools_location
        for name in os.listdir(self.abs_tools_location):
            #only check dirs
            abs_name = os.path.join(self.abs_tools_location, name)
            if os.path.isdir(abs_name):
                if not(name in self.tool_name_list) and not(self.get_tool(name) is None):
                    yield name