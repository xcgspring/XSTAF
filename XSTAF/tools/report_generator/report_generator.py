import os
import traceback
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
        try:
            LOGGER.info("Launch report generator tool")
            tool_dialog = ReportGenerator(cls.main_window)
            tool_dialog.exec_()
        except:
            LOGGER.error(traceback.format_exc())
        
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
        return self.run.result
        
    @property
    def pretty_result(self):
        return self.run.Results[self.result]
        
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
    passFirstSameDUT = True
    passFirstDifferentDUT = True
    
    def __init__(self, testcase, dut_info, workspace_data):
        self.name = testcase.name
        self.data = testcase.data
        self.data_runs = {}
        self.data_runs[dut_info["ip"]] = {}
        for run in testcase.runs():
            data_run = _DataRun(run, dut_info)
            self.data_runs[dut_info["ip"]][run.start] = data_run
            
        #one testsuite could run on multiple duts
        self.duts_info = []
        self.duts_info.append(dut_info)
        
        self.workspace_data = workspace_data
        
        #hold test results for each dut in workspace
        self._results_for_all_duts = {}
        
    @classmethod
    def set_pass_fail_policy(cls, passFirstSameDUT, passFirstDifferentDUT):
        cls.passFirstSameDUT = passFirstSameDUT
        cls.passFirstDifferentDUT = passFirstDifferentDUT
        
    @property
    def runs(self):
        for data_id, data_runs in self.data_runs.items():
            for run_start, run in data_runs.items():
                yield run
    
    @property
    def results_for_all_duts(self):
        #check the result for each dut testsuite runs with
        for dut_ip, runs in self.data_runs.items():
            results = []
            for run_start, run in runs.items():
                results.append(run.result)
            
            if len(results) == 0:
                self._results_for_all_duts[dut_ip] = "NotRun"
            elif not 0x00000001 in results:
                if 0x00000000 in results:
                    self._results_for_all_duts[dut_ip] = "Pass"
                else:
                    self._results_for_all_duts[dut_ip] = "NotRun"
            elif not 0x00000000 in results:
                if 0x00000000 in results:
                    self._results_for_all_duts[dut_ip] = "Fail"
                else:
                    self._results_for_all_duts[dut_ip] = "NotRun"
            else:
                self._results_for_all_duts[dut_ip] = "Mixed"
                
        #for other dut in workspace
        for dut in self.workspace_data.duts:
            if dut["ip"] not in self._results_for_all_duts:
                self._results_for_all_duts[dut["ip"]] = "NotRun"
                
        #generate the result data in same order with workspace duts
        for dut in self.workspace_data.duts:
            yield self._results_for_all_duts[dut["ip"]]
            
    @property
    def result(self):
        #check result for each dut
        #the result will be affected by passFirstSameDUT
        results_for_all_duts = []
        for dut_ip, runs in self.data_runs.items():
            results = []
            for run_start, run in runs.items():
                results.append(run.result)
        
            if len(results) == 0:
                results_for_all_duts.append("NotRun")
                break
                
            if self.passFirstSameDUT:
                if 0x00000000 in results:
                    results_for_all_duts.append("Pass")
                elif 0x00000001 in results:
                    results_for_all_duts.append("Fail")
                else:
                    results_for_all_duts.append("NotRun")
            else:
                if 0x00000001 in results:
                    results_for_all_duts.append("Fail")
                elif 0x00000000 in results:
                    results_for_all_duts.append("Pass")
                else:
                    results_for_all_duts.append("NotRun")
        
        #check final result
        #the result will be affected by passFirstDifferentDUT
        if self.passFirstDifferentDUT:
            if "Pass" in results_for_all_duts:
                return "Pass"
            elif "Fail" in results_for_all_duts:
                return "Fail"
            else:
                return "NotRun"
        else:
            if "Fail" in results_for_all_duts:
                return "Fail"
            elif "Pass" in results_for_all_duts:
                return "Pass"
            else:
                return "NotRun"
        
    def merge(self, testcase, dut_info):
        self.duts_info.append(dut_info)
        self.data_runs[dut_info["ip"]] = {}
        for run in testcase.runs():
            data_run = _DataRun(run, dut_info)
            self.data_runs[dut_info["ip"]][run.start] = data_run

class _DataTestSuite(object):
    '''
    data object for testsuite
    '''
    def __init__(self, testsuite, dut_info, workspace_data):
        self.name = testsuite.name
        self.data_testcases = {}
        for testcase in testsuite.testcases():
            data_testcase = _DataTestCase(testcase, dut_info, workspace_data)
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
            if testcase.result == "NotRun":
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
                    self.data_testsuites[testsuite.name] = _DataTestSuite(testsuite, dut_info, self)
        
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
        
        self.passFirstRadioButton1.toggle()
        self.passFirstRadioButton2.toggle()
        self.htmlCheckBox.toggle()
        self.csvCheckBox.toggle()
        
        #current not support excel report generate
        #self.csvCheckBox.setDisabled(True)
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

            if self.passFirstRadioButton1.isChecked():
                passFirstSameDUT = True
            else:
                passFirstSameDUT = False
            if self.passFirstRadioButton2.isChecked():
                passFirstDifferentDUT = True
            else:
                passFirstDifferentDUT = False
            _DataTestCase.set_pass_fail_policy(passFirstSameDUT, passFirstDifferentDUT)
            
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