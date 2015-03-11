
import os
import shutil
import zipfile
import xml.etree.ElementTree as ET

import logger
from DUT import DUT
from staf import get_staf_instance, config_staf

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
        
        self.workspace = None
        #new workspace flag
        self.new = False

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
        config_staf(self.settings["STAF_dir"])
        staf_instance = get_staf_instance()
        assert(staf_instance.check_and_start_staf())
        
    def check_if_default_workspace_exist(self):
        #to handle existing default workspace
        return _WorkSpace.check_default()
        
    def clean_default_workspace(self):
        _WorkSpace.clean_default()
        
    def new_workspace(self):
        #new and load workspace will change workspace object in server
        #ui need prompt user to save original workspace before new or load new workspace
        workspace = _WorkSpace()
        workspace.new()
        self.workspace = workspace
        #this flag used to indicate ui if need to ask user to provide workspace_path when save workspace
        #ui should only ask user to provide workspace_path when new is True
        self.new = True
        
    def load_workspace(self, workspace_path=""):
        #new and load workspace will change workspace object in server
        #ui need prompt user to save original workspace before new or load new workspace
        if not workspace_path:
            workspace_path = _WorkSpace.DefaultWorkspacePath
        
        workspace = _WorkSpace()
        workspace.load(workspace_path)
        self.workspace = workspace
        self.new = False
        
    def save_workspace(self, workspace_path=""):
        #save current workspace to workspace_path
        self.workspace.save(workspace_path)
        self.new = False
        
    def DUTs(self):
        if not self.workspace is None:
            for DUT in self.workspace.DUTs.items():
                yield DUT[1]
            
    def get_DUT(self, ip):
        if not self.workspace is None:
            return self.workspace.DUTs[ip]
        
    def has_DUT(self, ip):
        if not self.workspace is None:
            return self.workspace.has_DUT()
        
    def add_DUT(self, ip, name):
        if not self.workspace is None:
            self.workspace.add_DUT(ip, name)
        
    def remove_DUT(self, ip):
        if not self.workspace is None:
            self.workspace.remove_DUT(ip)
        
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
        
    #default workspace location
    DefaultWorkspacePath = r"c:\XSTAF\workspaces\.default"
        
    def __init__(self):
        #some settings
        self.settings = {}
        #DUT instance list for DUT management
        self.DUTs = {}

    def update_settings(self, **kwargs):
        for arg in kwargs.items():
            if arg[0] in self.settings:
                self.settings[arg[0]] = arg[1]
        
    def get_settings(self, index):
        if index in self.settings:
            return self.settings[index]
        else:
            return None
        
    @classmethod
    def check_default(cls):
        #check if default workspace already existing
        if os.path.isdir(cls.DefaultWorkspacePath):
            return True
        else:
            return False
    
    @classmethod
    def clean_default(cls):
        #clean default workspace
        if os.path.isdir(cls.DefaultWorkspacePath):
            shutil.rmtree(cls.DefaultWorkspacePath)
        
    def new(self):
        self.clean_default()
        if not os.path.isdir(self.DefaultWorkspacePath):
            os.makedirs(self.DefaultWorkspacePath)
            
        self.workspace_path = self.DefaultWorkspacePath
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
        xml_tree = ET.parse(configure_file)
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
            DUT_instance = DUT(DUT_IP, DUT_name)
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
        
        return True
        
    def save(self, workspace_path=""):
        '''
        save all configs and results
        and copy to new location if needed
        '''
        #function to format XML
        def indent(elem, level=0):
            i = "\n" + level*"  "
            if len(elem):
                if not elem.text or not elem.text.strip():
                    elem.text = i + "  "
                if not elem.tail or not elem.tail.strip():
                    elem.tail = i
                for elem in elem:
                    indent(elem, level+1)
                if not elem.tail or not elem.tail.strip():
                    elem.tail = i
            else:
                if level and (not elem.tail or not elem.tail.strip()):
                    elem.tail = i
        
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
        configure_file = os.path.join(self.workspace_path, self.ConfigFile)
        indent(root_element)
        ET.ElementTree(root_element).write(configure_file)
        
        #save testsuites and test results
        for DUT in self.DUTs.items():
            DUT_IP = DUT[0]
            DUT_instance = DUT[1]
            for testsuite in DUT_instance.testsuites.items():
                testsuite_name = testsuite[0]
                testsuite_instance = testsuite[1]
                
                root_element = ET.Element("TestSuite")
                testcases_element = ET.SubElement(root_element, "TestCases")
                for testcase in testsuite_instance.testcases.items():
                    testcase_element = ET.SubElement(testcases_element, "TestCase")
                    name_element = ET.SubElement(testcase_element, "Name")
                    name_element.text = testcase[1].name
                    command_element = ET.SubElement(testcase_element, "Command")
                    command_element.text = testcase[1].command
                    auto_element = ET.SubElement(testcase_element, "Auto")
                    auto_element.text = str(testcase[1].auto)
                    timeout_element = ET.SubElement(testcase_element, "Timeout")
                    timeout_element.text = str(testcase[1].timeout)
                    description_element = ET.SubElement(testcase_element, "Description")
                    description_element.text = testcase[1].description
                    
                    runs_element = ET.SubElement(testcase_element, "Runs")
                    for run in testcase[1].runs.items():
                        run_element = ET.SubElement(runs_element, "Run")
                        start_element = ET.SubElement(run_element, "Start")
                        start_element.text = run[1].start
                        end_element = ET.SubElement(run_element, "End")
                        end_element.text = run[1].end
                        result_element = ET.SubElement(run_element, "Result")
                        result_element.text = run[1].get_pretty_result()
                        status_element = ET.SubElement(run_element, "Status")
                        status_element.text = run[1].status
                        log_element = ET.SubElement(run_element, "Log")
                        log_element.text = run[1].log_location
                
                testsuite_path = os.path.join(self.workspace_path, self.TestResultFolder, DUT_IP, testsuite_name)
                testsuite_dir = os.path.dirname(testsuite_path)
                if not os.path.isdir(testsuite_dir):
                    os.makedirs(testsuite_dir)
                indent(root_element)
                ET.ElementTree(root_element).write(testsuite_path)
                
        #check if need copy
        if os.path.isdir(workspace_path) and (os.path.abspath(self.workspace_path).lower() != os.path.abspath(workspace_path).lower() ):
            #need copy
            #clean target directory
            shutil.rmtree(workspace_path)
            #copy
            shutil.copytree(self.workspace_path, workspace_path)
            #update workspace path
            self.workspace_path = workspace_path
            
    def export(self, package_path):
        pass
        
        
    def report(self):
        pass
        
        
    def has_DUT(self, ip):
        return (ip in self.DUTs)
        
    def add_DUT(self, ip, name):
        #add DUT
        logger.LOGGER.debug("Add DUT: %s" % ip)
        self.DUTs[ip] = DUT(ip, name)
        
    def remove_DUT(self, ip):
        logger.LOGGER.debug("Remove DUT: %s" % ip)
        DUT_instance = self.DUTs[ip]
        #stop DUT task runner thread
        DUT_instance.pause_task_runner()
        #remove it from server DUT list
        del self.DUTs[ip]

        