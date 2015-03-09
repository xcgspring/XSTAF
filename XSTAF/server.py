
import os
import zipfile
import xml.etree.ElementTree as ET

import logger
from DUT import DUT
from staf import STAF

class Server(object):
    '''
    server is the enter point of control layer
    server is response for check and start STAF, and manage workspace
    '''
    def __init__(self):
        #staf instance
        self.staf_instance = None
        #settings
        self.settings = {
            "STAF_dir" : r"c:\staf",
        }

    def update_settings(self, **kwargs):
        for arg in kwargs.items():
            if arg[0] in self.settings:
                self.settings[arg[0]] = arg[1]
        
    def get_settings(self, index):
        if index in self.settings:
            return self.settings[index]
        else:
            return None
        
    def check_and_start_staf(self):
        self.staf_instance = STAF(self.settings["STAF_dir"])
        assert(self.staf_instance.check_and_start_staf())
        
    def new_workspace():
        #new and load workspace will change workspace object in server
        #ui need prompt user to save original workspace before new or load new workspace
        workspace = _WorkSpace(self.staf_instance)
        assert(workspace.new())
        self.workspace = workspace
        #this flag used to indicate ui if need to ask user to provide workspace_path when save workspace
        #ui should only ask user to provide workspace_path when new is True
        self.new = True
        
    def load_workspace(workspace_path):
        #new and load workspace will change workspace object in server
        #ui need prompt user to save original workspace before new or load new workspace
        workspace = _WorkSpace(self.staf_instance)
        assert(workspace.load(workspace_path))
        self.workspace = workspace
        self.new = False
        
    def save_workspace(workspace_path):
        #save current workspace to workspace_path
        self.workspace.save(workspace_path)
        self.new = False
        
class _WorkSpace(object):
    '''
    a workspace could be a structured folder or zipped folder
    structure like:
    workspace_name |--configs.xml (contains workspace informations, like settings, DUTs info, test suites info)
                   |
                   |--test results (contains all test suites with test results)
                   |
                   |--test logs (contains all logs)
    '''
    ConfigFile = "configs.xml"
    TestResultFolder = "test_results"
    TestLogFolder = "test_logs"
        
    def __init__(self, staf_instance):
        self.staf_instance = staf_instance
        #some settings
        self.settings = {}
        
    def update_settings(self, **kwargs):
        for arg in kwargs.items():
            if arg[0] in self.settings:
                self.settings[arg[0]] = arg[1]
        
    def get_settings(self, index):
        if index in self.settings:
            return self.settings[index]
        else:
            return None
        
    def new(self):
        self.workspace_path = ""
        #DUT instance list for DUT management
        self.DUTs = {}
        return True
        
    def load(self, workspace_path):
        if os.path.isdir(workspace_path):
            #workspace is a folder
            pass
        elif zipfile.is_zipfile(workspace_path):
            #workspace is a zip file
            #unzip it
            zipfile.ZipFile(workspace_path).extractall()
        else:
            logger.LOGGER.error("Invalid workspace: %s" % workspace_path)
            return False
            
        self.workspace_path = workspace_path
        
        configure_file = os.path.join(workspace_path, self.ConfigFile)
        assert(os.path.isfile(configure_file))
        #read configures
        xml_tree = ET.parse(self.test_suite_file)
        root_element = xml_tree.getroot()
        
        #load settings
        settings_element = root_element.find("settings")
        setting_elements = settings_element.findall("setting")
        for setting_element in setting_elements:
            setting_name = setting_element.attrib["name"]
            setting_value = setting_element.text
            if setting_name in self.settings:
                self.settings[setting_name] = setting_value
            
        #load DUTs and test suites
        DUTs_element = root_element.find("DUTs")
        DUT_elements = DUTs_element.findall("DUT")
        for DUT_element in DUT_elements:
            DUT_IP = DUT_element.attrib["ip"]
            DUT_name = DUT_element.attrib["name"]
            DUT_instance = DUT(self.staf_instance, ip, name)
            self.DUTs[DUT_IP] = DUT_instance
            testsuites_element = DUT_element.find("testsuites")
            testsuite_elements = testsuites_element.findall("testsuite")
            for testsuite_element in testsuite_elements:
                testsuite_name = testsuite_element.attrib["name"]
                testsuite_path = os.path.join(self.workspace_path, self.TestResultFolder, DUT_IP, testsuite_name)
                if not os.path.isfile(testsuite_path):
                    logger.LOGGER.warn("testsuite not exist: %s" % testsuite_path)
                    continue
                DUT_instance.add_testsuite(testsuite_path)
        
    def save(self, workspace_path):
        #save all configs and results
        #and copy to new location if needed
        
        #save configs
        root_element = ET.Element("XSTAF")
        settings_element = ET.SubElement(root_element, "settings")
        DUTs_element = ET.SubElement(root_element, "DUTs")
        
        #dump settings
        for setting in self.settings.items():
            setting_name = setting[0]
            setting_value = setting[1]
            setting_element = ET.SubElement(settings_element, "setting", attrib={"name":setting_name})
            setting_element.text = setting_value
            
        #dump DUTs and test suites
        for DUT in self.DUTs.items():
            DUT_IP = DUT[0]
            DUT_instance = DUT[1]
            DUT_name = DUT_instance.name
            DUT_element = ET.SubElement(DUTs_element, "DUT", attrib={"ip":DUT_IP, "name":DUT_name})
            testsuites_element = ET.SubElement(DUT_element, "testsuites")
            for testsuite in DUT_instance.testsuites.items():
                testsuite_name = testsuite[0]
                testsuite_element = ET.SubElement(testsuites_element, "testsuite", attrib={"name":testsuite_name})
                
        #write configure file
        configure_file = os.path.join(workspace_path, self.ConfigFile)
        ET.ElementTree(root_element).write(configure_file)
        
        #save testsuites and test results
        for DUT in self.DUTs.items():
            for testsuite in DUT_instance.testsuites.items():
                testsuite_name = testsuite[0]
                testsuite_instance = testsuite[1]
                
        
        
        
        
        
        
        
        
        
        #check if need copy
        if not os.path.samefile(self.workspace_path, workspace_path):
            #need copy
        
        
    def export(self, package_path):
    
        
        
    def has_DUT(self, ip):
        return (ip in self.DUTs)
        
    def add_DUT(self, ip, name):
        #add DUT
        logger.LOGGER.debug("Add DUT: %s" % ip)
        self.DUTs[ip] = DUT(self.staf_instance, ip, name)
        
    def remove_DUT(self, ip):
        logger.LOGGER.debug("Remove DUT: %s" % ip)
        DUT_instance = self.DUTs[ip]
        #stop DUT task runner thread
        DUT_instance.pause_task_runner()
        #remove it from server DUT list
        del self.DUTs[ip]

        