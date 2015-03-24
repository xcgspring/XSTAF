
import os
import shutil
import zipfile
import xml.etree.ElementTree as ET

from XSTAF.core.logger import LOGGER
from XSTAF.core.DUT import DUT

class WorkSpace(object):
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

    #settings
    settings = {"WorkspaceLocation" : r"c:\XSTAF\workspaces",
                "DefaultWorkspace" : r".default",}

    def __init__(self):
        #DUT instance list for DUT management
        self._duts = {}

        self.workspace_path = ""
        
    @classmethod
    def config(cls, **kwargs):
        for arg in kwargs.items():
            key = arg[0]
            value = arg[1]
            if key in cls.settings:
                cls.settings[key] = value

    ############################################
    #workspace related methods
    ############################################
    @classmethod
    def is_default_exist(cls):
        #check if default workspace already existing
        default_workspace_path = os.path.join(cls.settings["WorkspaceLocation"], cls.settings["DefaultWorkspace"])
        if os.path.isdir(default_workspace_path):
            return True
        else:
            return False

    @classmethod
    def clean_default(cls):
        #clean default workspace
        default_workspace_path = os.path.join(cls.settings["WorkspaceLocation"], cls.settings["DefaultWorkspace"])
        if os.path.isdir(default_workspace_path):
            shutil.rmtree(default_workspace_path)

    def new(self, workspace_path=""):
        if not workspace_path:
            self.clean_default()
            default_workspace_path = os.path.join(self.settings["WorkspaceLocation"], self.settings["DefaultWorkspace"])
            if not os.path.isdir(default_workspace_path):
                os.makedirs(default_workspace_path)
            self.workspace_path = os.path.join(default_workspace_path)
        else:
            if not os.path.isdir(workspace_path):
                os.makedirs(workspace_path)
            self.load(workspace_path)

    def load(self, workspace_path):
        if os.path.isdir(workspace_path):
            #workspace is a folder
            pass
        elif zipfile.is_zipfile(workspace_path):
            #workspace is a zip file
            #unzip it
            zipfile.ZipFile(workspace_path).extractall()
        else:
            LOGGER.error("Invalid workspace: %s", workspace_path)
            raise ValueError("Invalid workspace: %s" % workspace_path)

        self.workspace_path = workspace_path

        configure_file = os.path.join(workspace_path, self.ConfigFile)
        if not os.path.isfile(configure_file):
            #no configure file, just return
            LOGGER.warning("No configure file in workspace: %s", self.workspace_path)
            return

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
        duts_element = root_element.find("DUTs")
        dut_elements = duts_element.findall("DUT")
        for dut_element in dut_elements:
            dut_ip = dut_element.attrib["ip"]
            dut_name = dut_element.attrib["name"]
            self.add_dut(dut_ip, dut_name)
            testsuites_element = dut_element.find("testsuites")
            testsuite_elements = testsuites_element.findall("testsuite")
            for testsuite_element in testsuite_elements:
                testsuite_name = testsuite_element.attrib["name"]
                testsuite_path = os.path.join(self.workspace_path, self.TestResultFolder, dut_ip, testsuite_name)
                if not os.path.isfile(testsuite_path):
                    LOGGER.warn("testsuite not exist: %s", testsuite_path)
                    continue
                self._duts[dut_ip].add_testsuite(testsuite_path)

    def save(self, workspace_path):
        '''
        save all configs and results
        and copy to new location if needed
        '''
        if os.path.isdir(workspace_path):
            #update workspace path
            self.workspace_path = workspace_path
        else:
            LOGGER.error("Target workspace path not exist, please create it first: %s", workspace_path)
            raise ValueError("Target workspace path not exist, please create it first: %s" % workspace_path)
        
        #clean workspace dir
        try:
            shutil.rmtree(self.workspace_path)
            os.makedirs(self.workspace_path)
        except Exception:
            LOGGER.warning("Clean workspace fail: %s", self.workspace_path)
        
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
        for dut in self.duts():
            dut_element = ET.SubElement(DUTs_element, "DUT", attrib={"ip":dut.ip, "name":dut.name})
            testsuites_element = ET.SubElement(dut_element, "testsuites")
            for testsuite in dut.testsuites():
                ET.SubElement(testsuites_element, "testsuite", attrib={"name":testsuite.name})

        #write configure file
        configure_file = os.path.join(self.workspace_path, self.ConfigFile)
        indent(root_element)
        ET.ElementTree(root_element).write(configure_file)

        #save testsuites and test results
        for dut in self.duts():
            for testsuite in dut.testsuites():
                root_element = ET.Element("TestSuite")
                testcases_element = ET.SubElement(root_element, "TestCases")
                for testcase in testsuite.testcases():
                    testcase_element = ET.SubElement(testcases_element, "TestCase")
                    id_element = ET.SubElement(testcase_element, "ID")
                    id_element.text = str(testcase.ID)
                    name_element = ET.SubElement(testcase_element, "Name")
                    name_element.text = testcase.name
                    command_element = ET.SubElement(testcase_element, "Command")
                    command_element.text = testcase.command
                    auto_element = ET.SubElement(testcase_element, "Auto")
                    auto_element.text = str(testcase.auto)
                    timeout_element = ET.SubElement(testcase_element, "Timeout")
                    timeout_element.text = str(testcase.timeout)
                    description_element = ET.SubElement(testcase_element, "Description")
                    description_element.text = testcase.description

                    runs_element = ET.SubElement(testcase_element, "Runs")
                    for run in testcase.runs():
                        run_element = ET.SubElement(runs_element, "Run")
                        start_element = ET.SubElement(run_element, "Start")
                        start_element.text = run.start
                        end_element = ET.SubElement(run_element, "End")
                        end_element.text = run.end
                        result_element = ET.SubElement(run_element, "Result")
                        result_element.text = run.pretty_result
                        status_element = ET.SubElement(run_element, "Status")
                        status_element.text = run.status
                        log_element = ET.SubElement(run_element, "Log")
                        log_element.text = run.log_location

                testsuite_path = os.path.join(self.workspace_path, self.TestResultFolder, dut.ip, testsuite.name)
                testsuite_dir = os.path.dirname(testsuite_path)
                if not os.path.isdir(testsuite_dir):
                    os.makedirs(testsuite_dir)
                indent(root_element)
                ET.ElementTree(root_element).write(testsuite_path)

    def is_current_default(self):
        default_workspace_path = os.path.join(self.settings["WorkspaceLocation"], self.settings["DefaultWorkspace"])
        return self.workspace_path == default_workspace_path

    def export(self, package_path):
        pass

    def merge(self, *to_be_merged_workspaces):
        #if all duts in two workspaces are not same, merge is simple
        #just add duts and copy all logs from merged workspace
        for to_be_merged_workspace in to_be_merged_workspaces:
            #add duts
            self._duts.update(to_be_merged_workspace._duts)
            #copy all logs
            source_log_path = os.path.join(to_be_merged_workspace.workspace_path, self.TestLogFolder)
            if os.path.isdir(source_log_path):
                for item in os.listdir(source_log_path):
                    target = os.path.join(self.workspace_path, self.TestLogFolder, item)
                    source = os.path.join(source_log_path, item)
                    shutil.copytree(source, target)

    def split(self, output_path):
        #split will create a standalone workspace for each dut in current workspace
        for dut in duts:
            new_workspace = WorkSpace()
            new_workspace.new(os.path.join(output_path, dut.ip))
            new_workspace._duts[dut.ip] = dut
            #copy logs
            log_path = os.path.join(self.workspace_path, self.TestLogFolder, dut.ip)
            if os.path.isdir(log_path):
                target = os.path.join(new_workspace.workspace_path, self.TestLogFolder, dut.ip)
                shutil.copytree(log_path, target)
                
            new_workspace.save(new_workspace.workspace_path)

    ############################################
    #DUT management methods
    ############################################
    def has_dut(self, ip):
        return (ip in self._duts)

    def add_dut(self, ip, name):
        dut = DUT(os.path.join(self.workspace_path, self.TestLogFolder), ip, name)
        self._duts[ip] = dut
        return dut

    def remove_dut(self, ip):
        dut = self._duts[ip]
        #remove task runner
        dut.remove_runner()
        #remove dut from server DUT list
        del self._duts[ip]

    def get_dut(self, ip):
        return self._duts[ip]
        
    def duts(self):
        for dut_item in self._duts.items():
            yield dut_item[1]

    def change_dut_info(self, original_ip, changed_ip, changed_name):
        #change dut info process like below
        #1. create a new dut object
        new_dut = self.add_dut(changed_ip, changed_name)
        
        #2. load testsuites from old dut object
        original_dut = self._duts[original_ip]
        for testsuite in original_dut.testsuites():
            new_dut.add_testsuite_object(testsuite)
            
        #3. delete old dut
        self.remove_dut(original_ip)
        
        