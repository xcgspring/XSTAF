
import os
import time
import uuid
import threading
import xml.etree.ElementTree as ET

class TestCase(object):
    #test case result
    NotRun = 0b10000000
    Fail = 0b00000001
    Pass = 0b00000000
    
    #pretty results
    PrettyResults = { NotRun : "not run",
                    Fail: "fail",
                    Pass: "pass", }
    
    #to make ID generation thread safe
    mutex = threading.Lock()
    
    def __init__(self):
        #make a unique ID for each test case instance
        self.mutex.acquire()
        self.ID = uuid.uuid1()
        time.sleep(0.01)
        self.mutex.release()
        
        self.name = ""
        self.command = ""
        self.auto = False
        self.timeout = 600
        self.description = ""
        self.status = ""
        self.log_location = ""
        self.result = self.NotRun
        self.pretty_result = self.get_pretty_result()
        
    def get_pretty_result(self):
        self.pretty_result = self.PrettyResults[self.result]
        return self.pretty_result

class TestSuite(object):
    def __init__(self):
        pass
        
class PyAnvilTestSuite(object):
    def __init__(self, test_suite_file):
        self.test_suite_file = test_suite_file
        
        self.testcases = {}
        self._parse_and_build()
        
    def _parse_and_build(self):
        self.name = os.path.basename(self.test_suite_file)
        
        xml_tree = ET.parse(self.test_suite_file)
        root = xml_tree.getroot()
        testcase_elements = root.findall("TestList/ToolCase")
        for testcase_element in testcase_elements:
            testcase = TestCase()
            testcase.name = testcase_element.attrib["name"]
            #testcase.ID = testcase.name
            executable = testcase_element.find("Executable").text
            parameters = testcase_element.find("Parameters").text
            testcase.command = executable+" "+parameters
            testcase.auto = True
            
            if not testcase_element.find("Timeout") is None:
                testcase.timeout = int(testcase_element.find("Timeout").text)
            if not testcase_element.find("Description") is None:
                testcase.description = testcase_element.find("Description").text
            
            self.testcases[testcase.ID] = testcase
            
    def passed_count(self):
        count = 0
        for testcase in self.testcases.items():
            if testcase[1].result == testcase[1].Pass:
                count +=1
        return count
        
    def failed_count(self):
        count = 0
        for testcase in self.testcases.items():
            if testcase[1].result == testcase[1].Fail:
                count +=1
        return count
        
    def not_run_count(self):
        count = 0
        for testcase in self.testcases.items():
            if testcase[1].result == testcase[1].NotRun:
                count +=1
        return count