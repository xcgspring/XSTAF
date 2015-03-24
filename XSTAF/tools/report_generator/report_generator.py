import os

from XSTAF.core.logger import LOGGER
from PyQt4 import QtCore, QtGui
from ui.ui_reportGenerator import Ui_TestReportDialog
import ui.resources_rc

class Tool(object):
    _description = "Report Generator"
    main_window = None
    
    @classmethod
    def set_main_window(cls, main_window):
        cls.main_window = main_window
    
    @staticmethod
    def icon():
        tool_icon = QtGui.QIcon()
        tool_icon.addPixmap(QtGui.QPixmap(":icons/icons/report_generate.png"))
        return tool_icon
    
    @classmethod
    def launch(cls):
        LOGGER.info("Launch report generator tool")
        tool_dialog = ReportGenerator(cls.main_window)
        tool_dialog.exec_()
        
    @classmethod
    def description(cls):
        return cls._description
    
    
class _DataRun(object):
    '''
    data object for run
    '''
    def __init__(self, run, dut_info):
        self.run = run
        self._dut_info = dut_info
        
    @property
    def result(self):
        if self.run.result & 0b00000001:
            return False
        if not self.run.result:
            return True
        
    @property
    def pretty_result(self):
        if self.result:
            return "Pass"
        if not self.result:
            return "Fail"
        
    @property
    def dut_info(self):
        return self._dut_info
        
class _DataTestCase(object):
    '''
    data object for testcase
    '''
    #pass/fail policy, will affect all _DataTestCase instance
    #set this flag to True, one pass run will set testcase to pass
    #set this flag to False, one fail run will set testcase to fail
    PassFirst = True
    
    def __init__(self, testcase, dut_info):
        self.name = testcase.name
        self.data = testcase.data
        self.data_runs = {}
        for run in testcase.runs():
            data_run = _DataRun(run, dut_info)
            self.data_runs[run.start+dut_info["ip"]] = data_run
            
        #one testsuite could run multiple duts
        self.duts_info = []
        self.duts_info.append(dut_info)
        
    @classmethod
    def set_pass_fail_policy(cls, pass_first):
        cls.PassFirst = pass_first
        
    @property
    def runs(self):
        for data_id, data_run in self.data_runs.items():
            yield data_run
    
    @property
    def result(self):
        if not len(self.data_runs):
            result = "Not run"
            return result
            
        if self.PassFirst:
            result = "Fail"
            for run in self.runs:
                if run.result:
                    result = "Pass"
        else:
            result = "Pass"
            for run in self.runs:
                if not run.result:
                    result = "Fail"
        return result
    
    def merge(self, testcase, dut_info):
        self.duts_info.append(dut_info)
        for run in testcase.runs():
            data_run = _DataRun(run, dut_info)
            self.data_runs[run.start+dut_info[ip]] = data_run

class _DataTestSuite(object):
    '''
    data object for testsuite
    '''
    def __init__(self, testsuite, dut_info):
        self.name = testsuite.name
        self.data_testcases = {}
        for testcase in testsuite.testcases():
            data_testcase = _DataTestCase(testcase, dut_info)
            self.data_testcases[testcase.name] = data_testcase
        
        #one testsuite could run multiple duts
        self.duts_info = []
        self.duts_info.append(dut_info)
    
    @property
    def testcases(self):
        for name, data_testcase in self.data_testcases.items():
            yield data_testcase
            
    @property
    def len(self):
        return len(self.data_testcases)
        
    @property
    def passed(self):
        passed = 0
        for testcase in self.testcases:
            if testcase.result == "Pass":
                passed += 1
        return passed
        
    @property
    def failed(self):
        failed = 0
        for testcase in self.testcases:
            if testcase.result == "Fail":
                failed += 1
        return failed
        
    @property
    def NotRun(self):
        NotRun = 0
        for testcase in self.testcases:
            if testcase.result == "Not run":
                NotRun += 1
        return NotRun
        
    def merge(self, testsuite, dut_info):
        self.duts_info.append(dut_info)
        for testcase in testsuite.testcases():
            if testcase.name in self.data_testcases:
                self.data_testcases[testcase.name].merge(testcase, dut_info)
            else:
                self.data_testcases[testcase.name] = _DataTestCase(testcase, dut_info)

class _Data(object):
    '''
    extract information from workspace
    testsuites with same name in different dut will be merged
    '''
    def __init__(self, workspace):
        self.workspace = workspace
        self.settings = {"title" : "Test Report",
                        "summary" : "",}
        self.data_testsuites = {}
        for dut in self.workspace.duts():
            dut_info = {}
            dut_info["ip"] = dut.ip
            dut_info["name"] = dut.name
            for testsuite in dut.testsuites():
                if testsuite.name in self.data_testsuites:
                    self.data_testsuites[testsuite.name].merge(testsuite, dut_info)
                else:
                    self.data_testsuites[testsuite.name] = _DataTestSuite(testsuite, dut_info)
        
    def config(self, **kwargs):
        for key in kwargs:
            if key in self.settings:
                self.settings[key] = kwargs[key]
    @property
    def title(self):
        return self.settings["title"]

    @property
    def summary(self):
        return self.settings["summary"]
        
    @property
    def duts(self):
        for dut in self.workspace.duts():
            dut_info = {}
            dut_info["ip"] = dut.ip
            dut_info["name"] = dut.name
            yield dut_info
    
    @property
    def testsuites(self): 
        for data_testsuite_name, data_testsuite in self.data_testsuites.items():
            yield data_testsuite
            
    @property
    def total(self):
        total = 0
        for testsuite in self.testsuites:
            total += testsuite.len
        return total
        
    @property
    def passed(self):
        passed = 0
        for testsuite in self.testsuites:
            passed += testsuite.passed
        return passed
        
    @property
    def failed(self):
        failed = 0
        for testsuite in self.testsuites:
            failed += testsuite.failed
        return failed
    
    @property
    def NotRun(self):
        NotRun = 0
        for testsuite in self.testsuites:
            NotRun += testsuite.NotRun
        return NotRun
    
class ReportGenerator(QtGui.QDialog, Ui_TestReportDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        
        self.server = parent.server
        
        self.passFirstRadioButton.toggle()
        self.htmlCheckBox.toggle()
        self.csvCheckBox.toggle()
        #current not support excel report generate
        self.excelCheckBox.setDisabled(True)
        
        self.connect(self.searchToolButton, QtCore.SIGNAL("clicked(bool)"), self.get_report_location)
        
        self.workspace = self.server.get_workspace()
        if self.workspace is None:
            LOGGER.warning("Current no workspace loaded, could not generate report")
        else:
            self.reportLineEdit.setText(self.workspace.workspace_path)
    
    def get_report_location(self):
        if not self.workspace is None:
            report_path = QtGui.QFileDialog.getExistingDirectory(self, "Get report location", self.workspace.workspace_path)
            self.reportLineEdit.setText(report_path)
    
    def accept(self):
        if not self.workspace is None:
            data = _Data(self.workspace)

            if self.passFirstRadioButton.isChecked():
                passFirst = True
            else:
                passFirst = False
            _DataTestCase.set_pass_fail_policy(passFirst)
            
            title = str(self.titleEdit.text())
            summary = str(self.summaryTextEdit.toPlainText())
            data.config(summary=summary)
            if title:
                data.config(title=title)
            
            report_location = str(self.reportLineEdit.text())
            if not os.path.isdir(report_location):
                LOGGER.warning("report location not exist, please check!")
                return
            
            if self.htmlCheckBox.isChecked():
                #generate html report
                LOGGER.info("generate html report: %s in %s" % (title+".html", report_location))
                from html.html_generator import HtmlGenerator
                HtmlGenerator(data).generate(report_location, title+".html")

            if self.csvCheckBox.isChecked():
                #generate excel report
                LOGGER.info("generate csv report in: %s" % (os.path.join(report_location, title)))
                from csv.csv_generator import CSVGenerator
                CSVGenerator(data).generate(os.path.join(report_location, title))
            
        QtGui.QDialog.accept(self)