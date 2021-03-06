
import os
import time
import uuid
import threading
import xml.etree.ElementTree as ET

from XSTAF.core.logger import LOGGER

class Run(object):
    #test case result
    NotRun = 0b10000000
    Fail = 0b00000001
    Pass = 0b00000000
    
    #pretty results
    Results = { NotRun : "not run",
                Fail : "fail",
                Pass : "pass", 
                "not run" : NotRun,
                "fail" : Fail, 
                "pass" : Pass, }

    def __init__(self):
        self.start = ""
        self.end = ""
        self.status = ""

        self._result = self.NotRun
        
    @property
    def result(self):
        return self._result
        
    @result.setter
    def result(self, value):
        if value in self.Results:
            if isinstance(value, str):
                value = self.Results[value]
            self._result = value
        else:
            LOGGER.warning("unacceptable result: %s" % repr(value))

    @property
    def pretty_result(self):
        return self.Results[self.result]
        
class TestCase(object):
    #to make ID generation thread safe
    mutex = threading.Lock()
    
    def __init__(self):
        #make a unique ID for each test case instance
        self.mutex.acquire()
        self._ID = uuid.uuid1()
        time.sleep(0.01)
        self.mutex.release()
        
        self.name = ""
        self.command = ""
        self.auto = False
        self.timeout = 600
        self.description = ""
        self.data = ""
        
        self._runs = {}
        
    def runs(self):
        run_ids = self._runs.keys()
        run_ids.sort()
        for run_id in run_ids:
            yield self._runs[run_id]
    
    def add_run(self, run):
        #we use task start time as id
        self._runs[run.start] = run
        
    def get_run(self, id):
        return self._runs[id]
        
    def remove_run(self, id):
        del self._runs[id]
        
    def remove_all_runs(self):
        self._runs = {}
        
    @property
    def ID(self):
        return self._ID
        
    @ID.setter
    def ID(self, id):
        self._ID = id
            
class TestSuite(object):
    def __init__(self, test_suite_file):
        self.test_suite_file = test_suite_file
        
        self._testcases = {}
        self._parse_and_build()
        
    def _parse_and_build(self):
        self.name = os.path.basename(self.test_suite_file)
        
        xml_tree = ET.parse(self.test_suite_file)
        root_element = xml_tree.getroot()
        
        if root_element.tag == "XMLTestCollection":
            #pyanvil test scenarios
            self._parse_pyanvil_test_suite(root_element)
        elif root_element.tag == "TestSuite":
            self._parse_test_suite(root_element)
            
    def _parse_pyanvil_test_suite(self, root_element):
        testcase_elements = root_element.findall("TestList/ToolCase")
        for testcase_element in testcase_elements:
            testcase = TestCase()
            testcase.data = testcase_element.attrib["name"]
            #pyanvil case do not have a global id, use system gen id
            #testcase.ID = testcase.name
            executable = testcase_element.find("Executable").text
            parameters = testcase_element.find("Parameters").text
            testcase.command = executable+" "+parameters
            testcase.auto = True
            
            if not testcase_element.find("Timeout") is None:
                testcase.timeout = int(testcase_element.find("Timeout").text)
            if not testcase_element.find("Description") is None:
                testcase.name = testcase_element.find("Description").text
            
            self._testcases[testcase.ID] = testcase
            
    def _parse_test_suite(self, root_element):
        testcases_element = root_element.find("TestCases")
        testcase_elements = testcases_element.findall("TestCase")
        for testcase_element in testcase_elements:
            testcase = TestCase()
            testcase.ID = uuid.UUID(testcase_element.find("ID").text)
            testcase.name = testcase_element.find("Name").text
            testcase.command = testcase_element.find("Command").text
            
            #optional
            if not testcase_element.find("Auto") is None:
                auto = testcase_element.find("Auto").text
                if auto.upper() == "TRUE":
                    testcase.auto = True
                else:
                    testcase.auto = False
            if not testcase_element.find("Timeout") is None:
                testcase.timeout = int(testcase_element.find("Timeout").text)
            if not testcase_element.find("Description") is None:
                testcase.description = testcase_element.find("Description").text
            if not testcase_element.find("Data") is None:
                testcase.description = testcase_element.find("Data").text
                
            #test run results
            runs_element = testcase_element.find("Runs")
            run_elements = runs_element.findall("Run")
            for run_element in run_elements:
                run = Run()
                run.start = run_element.find("Start").text
                run.end = run_element.find("End").text
                run.result = run_element.find("Result").text
                run.status = run_element.find("Status").text
                if run.status is None:
                    run.status = ""
                testcase.add_run(run)
                
            self._testcases[testcase.ID] = testcase

    def testcases(self):
        testcase_ids = self._testcases.keys()
        testcase_ids.sort()
        for testcase_id in testcase_ids:
            yield self._testcases[testcase_id]
            
    def testcase_number(self):
        return len(self._testcases)
        
    def get_testcase(self, testcase_id):
        return self._testcases[testcase_id]