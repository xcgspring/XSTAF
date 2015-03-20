
import os
import sys
import pickle
import traceback

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
            self.abs_tools_location  = os.path.join(XSTAF_path, "..", tools_location)
        else:
            self.abs_tools_location  = tools_location

        #try get tools name list from pickle file
        self.pickle_config_file = os.path.join(self.abs_tools_location, self.settings["ToolsConfigureFile"])
        self.load_config()

    def get_tool(self, tool_module_name):
        if not os.path.isdir(self.abs_tools_location):
            LOGGER.warning("Can not find tools location: %s", self.abs_tools_location)
            return None
        #append abs tools path to python lib path
        #so we can dynamic import them
        sys.path.append(self.abs_tools_location)
        try:
            tool_module = __import__(tool_module_name)
            #want to reload the tool if tool is updated
            tool_module = reload(tool_module)
            tool = tool_module.Tool
        except (ImportError, AttributeError) as e:
            LOGGER.info("Can not import tool: %s" % tool_name)
            LOGGER.debug(traceback.format_exc())
            return None
        else:
            return tool
            
    def load_config(self):
        if not os.path.isfile(self.pickle_config_file):
            LOGGER.warning("Can not find config file: %s", self.pickle_config_file)
            return
        #we load tool names from pickle file
        if os.path.isfile(self.pickle_config_file):
            with open(self.pickle_config_file, 'r') as f:
                self.tool_name_list = pickle.load(f)
        
    def save_config(self):
        if not os.path.isdir(self.abs_tools_location):
            LOGGER.warning("Can not find tools location: %s", self.abs_tools_location)
            return None
        #we save current tool names to pickle file
        with open(self.pickle_config_file, 'w') as f:
            pickle.dump(self.tool_name_list, f)
        
    @property
    def available_tool_name_list(self):
        if not os.path.isdir(self.abs_tools_location):
            LOGGER.warning("Can not find tools location: %s", self.abs_tools_location)
            while False:
                yield None
        else:
            #check all packages under abs_tools_location
            for name in os.listdir(self.abs_tools_location):
                #only check dirs
                abs_name = os.path.join(self.abs_tools_location, name)
                if os.path.isdir(abs_name):
                    if not(name in self.tool_name_list) and not(self.get_tool(name) is None):
                        yield name