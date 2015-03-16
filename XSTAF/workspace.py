
import os
import shutil
import zipfile
import xml.etree.ElementTree as ET

import logger
from DUT import DUT

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

    #default workspace location
    DefaultWorkspacePath = r"c:\XSTAF\workspaces\.default"

    def __init__(self):
        #some settings
        self.settings = {}
        #DUT instance list for DUT management
        self._duts = {}

        self.workspace_path = ""

    def update_settings(self, **kwargs):
        for arg in kwargs.items():
            if arg[0] in self.settings:
                self.settings[arg[0]] = arg[1]

    def get_settings(self, index):
        if index in self.settings:
            return self.settings[index]
        else:
            return None

    ############################################
    #workspace related methods
    ############################################
    @classmethod
    def is_default_exist(cls):
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

    def load(self, workspace_path):
        if os.path.isdir(workspace_path):
            #workspace is a folder
            pass
        elif zipfile.is_zipfile(workspace_path):
            #workspace is a zip file
            #unzip it
            zipfile.ZipFile(workspace_path).extractall()
        else:
            logger.LOGGER.error("Invalid workspace: %s", workspace_path)
            raise ValueError("Invalid workspace: %s" % workspace_path)

        self.workspace_path = workspace_path

        configure_file = os.path.join(workspace_path, self.ConfigFile)
        if not os.path.isfile(configure_file):
            #no configure file, just return
            logger.LOGGER.warning("No configure file in workspace: %s", self.workspace_path)
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
                    logger.LOGGER.warn("testsuite not exist: %s", testsuite_path)
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
            logger.LOGGER.error("Target workspace path not exist, please create it first: %s", workspace_path)
            raise ValueError("Target workspace path not exist, please create it first: %s" % workspace_path)
        
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
                for testcase in testsuite.testcases.items():
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
                        result_element.text = run[1].pretty_result
                        status_element = ET.SubElement(run_element, "Status")
                        status_element.text = run[1].status
                        log_element = ET.SubElement(run_element, "Log")
                        log_element.text = run[1].log_location

                testsuite_path = os.path.join(self.workspace_path, self.TestResultFolder, dut.ip, testsuite.name)
                testsuite_dir = os.path.dirname(testsuite_path)
                if not os.path.isdir(testsuite_dir):
                    os.makedirs(testsuite_dir)
                indent(root_element)
                ET.ElementTree(root_element).write(testsuite_path)

    def is_current_default(self):
        return self.workspace_path == self.DefaultWorkspacePath

    def export(self, package_path):
        pass

    def report(self):
        pass

    ############################################
    #DUT management methods
    ############################################
    def has_dut(self, ip):
        return (ip in self._duts)

    def add_dut(self, ip, name):
        dut = DUT(os.path.join(self.workspace_path, self.TestLogFolder), ip, name)
        dut.add_monitor()
        self._duts[ip] = dut

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
