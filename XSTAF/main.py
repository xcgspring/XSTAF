
import os
import time
import threading
from PyQt4 import QtCore, QtGui
from ui.ui_mainWindow import Ui_XSTAFMainWindow, _translate, _fromUtf8
from ui.ui_settingsDialog import Ui_Settings
from ui.ui_addDUT import Ui_addDUT
from ui.ui_DUT import Ui_DUTWindow
from ui.ui_refresh import Ui_refreshDialog
from ui.ui_confirmDialog import Ui_confirmDialog
import ui.resources_rc

import logger
from server import Server

STAFServer = Server()

class ConfirmDialog(QtGui.QDialog, Ui_confirmDialog):
    Confirmed = False
    
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        
        self.connect(self.yesButton, QtCore.SIGNAL("clicked(bool)"), self.accept)
        self.connect(self.noButton, QtCore.SIGNAL("clicked(bool)"), self.reject)
        
    @classmethod
    def confirm(cls, parent=None, message=""):
        instance = ConfirmDialog(parent)
        instance.messageLabel.setText(message)
        instance.exec_()
        return instance.Confirmed
    
    def accept(self):
        self.Confirmed = True
        QtGui.QDialog.accept(self)
        
    def reject(self):
        self.Confirmed = False
        QtGui.QDialog.reject(self)

class RefreshDUTThread(QtCore.QThread):
    def __init__(self, ip):
        QtCore.QThread.__init__(self)
        self.ip = ip
    
    def run(self):
        DUT_instance = STAFServer.get_DUT(self.ip)
        self.emit(QtCore.SIGNAL("notify_status"), "Refreshing DUT: %s..." % DUT_instance.ip)
        #refresh DUT, will check DUT status, time cost
        DUT_instance.refresh()
            
        time.sleep(0.1)
        self.emit(QtCore.SIGNAL("notify_stop"))
            
class RefreshDUTDialog(QtGui.QDialog, Ui_refreshDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        
        self.parent = parent
        self.progressBar.setRange(0, 0)
        self.refresh_thread = RefreshDUTThread(parent.ip)
        
        #signal and slot
        self.connect(self.refresh_thread, QtCore.SIGNAL("notify_status"), self.update_status)
        self.connect(self.refresh_thread, QtCore.SIGNAL("notify_stop"), self.accept)

        self.refresh_thread.start()

    def update_status(self, status):
        self.statusLabel.setText(status)
        
    def accept(self):
        self.parent.refresh_without_checking_status()
        QtGui.QDialog.accept(self)

class DUTWindow(QtGui.QMainWindow, Ui_DUTWindow):
    def __init__(self, parent, ip):
        self.parent = parent
        self.ip = ip
        self.DUT_instance = STAFServer.get_DUT(ip)
        self.name = self.DUT_instance.name
        QtGui.QMainWindow.__init__(self, self.parent)

        #view
        self.setupUi(self)
        #set DUT window title
        self.setWindowTitle(_translate("DUTWindow", "DUT IP: %s Name: %s Status: %s" % (self.ip, self.name, self.DUT_instance.pretty_status), None))
        
        #model
        self.testsModel = QtGui.QStandardItemModel(self.TestsTreeView)
        self.TestsTreeView.setModel(self.testsModel)
        
        self.taskQueueModel = QtGui.QStandardItemModel(self.taskQueueListView)
        self.taskQueueListView.setModel(self.taskQueueModel)
        
        #set DUTWindow UI status
        self.actionRefresh.setDisabled(True)
        self.actionRemoveTestSuite.setDisabled(True)
        self.actionStartRunner.setDisabled(True)
        self.actionPauseRunner.setDisabled(True)
        
        #signals and slots
        self.connect(self.actionAddTestSuite, QtCore.SIGNAL("triggered(bool)"), self.add_test_suite)
        self.connect(self.actionRemoveTestSuite, QtCore.SIGNAL("triggered(bool)"), self.remove_test_suite)
        self.connect(self.actionRefresh, QtCore.SIGNAL("triggered(bool)"), self.refresh)
        
        self.connect(self.actionAddtoTaskQueue, QtCore.SIGNAL("triggered(bool)"), self.add_test_to_task_queue)
        self.connect(self.actionRemoveFromTaskQueue, QtCore.SIGNAL("triggered(bool)"), self.remove_test_from_task_queue)
        self.connect(self.actionClearTaskQueue, QtCore.SIGNAL("triggered(bool)"), self.clear_task_queue)
        
        self.connect(self.actionStartRunner, QtCore.SIGNAL("triggered(bool)"), self.start_task_runner)
        self.connect(self.actionPauseRunner, QtCore.SIGNAL("triggered(bool)"), self.pause_task_runner)
        
        self.connect(self.TestsTreeView, QtCore.SIGNAL("clicked(QModelIndex)"), self.test_view_clicked)
        self.connect(self.TestsTreeView, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.test_view_right_clicked)
        self.connect(self.taskQueueListView, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.task_queue_view_right_clicked)
        

        #self.connect(self.DUT_instance.task_runner, self.DUT_instance.task_runner.taskRunnerExit, self.taskRunnerExit)
        self.connect(self.parent, self.parent.STAFReady, self.add_runner_and_monitor)
        
        #some states
        self.task_runner_running = False
        
        #load existing test suites
        self._refresh_test_view()
        
    def _refresh_test_view(self):
        notRunIcon = QtGui.QIcon()
        notRunIcon.addPixmap(QtGui.QPixmap(_fromUtf8(":icons/icons/not-run.png")))
        failIcon = QtGui.QIcon()
        failIcon.addPixmap(QtGui.QPixmap(_fromUtf8(":icons/icons/fail.png")))
        passIcon = QtGui.QIcon()
        passIcon.addPixmap(QtGui.QPixmap(_fromUtf8(":icons/icons/pass.png")))

        self.testsModel.clear()
        for testsuite in self.DUT_instance.testsuites.items():
            testsuite_name = testsuite[0]
            testsuite_item = QtGui.QStandardItem(QtCore.QString("%0").arg(testsuite_name))
            for testcase in testsuite[1].testcases.items():
                testcase_item = QtGui.QStandardItem(QtCore.QString(testcase[1].name))
                for run in testcase[1].runs.items():
                
                    if run[1].result & 0b10000000:
                        icon = notRunIcon
                    elif run[1].result & 0b00000001:
                        icon = failIcon
                    elif not run[1].result:
                        icon = passIcon
                    else:
                        logger.LOGGER.warn("Encounter unexpected test result: %s" % run[1].result)
                        icon = QtGui.QIcon()
                        
                    format_time = time.strftime("%d %b %H:%M:%S", time.localtime(float(run[1].start)))
                    run_item = QtGui.QStandardItem(icon, QtCore.QString("Run begin at: %s" % format_time))
                    testcase_item.appendRow(run_item)
                #store test id in test case item
                testcase_id = testcase[0]
                testcase_item.setData(QtCore.QVariant(testcase_id))
                testsuite_item.appendRow(testcase_item)
                
            self.testsModel.appendRow(testsuite_item)
        
    def add_test_suite(self):
        test_suite_file = QtGui.QFileDialog.getOpenFileName(self, "Add TestSuite")
        if os.path.isfile(test_suite_file):
            testsuite = self.DUT_instance.add_testsuite(str(test_suite_file))
            self._refresh_test_view()
            logger.LOGGER.debug("Add testsuite: %s" % test_suite_file)
        
    def remove_test_suite(self):
        for selected_index in self.TestsTreeView.selectedIndexes():
            item = self.testsModel.itemFromIndex(selected_index)
            if item.parent() is None:
                logger.LOGGER.debug("Remove testsuite: %s" % item.text())
                self.DUT_instance.remove_testsuite(str(item.text()))
                self._refresh_test_view()
        
    def test_view_clicked(self, index):
        #logger.LOGGER.debug("Click: column: %s, raw: %s" % (index.column(), index.row()))
        item = self.testsModel.itemFromIndex(index)
        if not item is None:
            if item.parent() is None:
                #click on testsuite
                self.actionRemoveTestSuite.setEnabled(True)
                #print testsuite info in test view
                testsuite = self.DUT_instance.testsuites[str(item.text())]
                info = "TestSuite: %s\n" % testsuite.test_suite_file
                info += "  Total test case: %d\n" % len(testsuite.testcases)
                #info += "  Passed: %d\n" % testsuite.passed_count()
                #info += "  Failed: %d\n" % testsuite.failed_count()
                #info += "  NotRun: %d\n" % testsuite.not_run_count()
            else:
                self.actionRemoveTestSuite.setDisabled(True)
                #print testcase info in test view
                testsuite_name = str(item.parent().text())
                testcase_id = item.data().toPyObject()
                testsuite = self.DUT_instance.testsuites[testsuite_name]
                testcase = testsuite.testcases[testcase_id]
                info = "TestCase: %s\n" % testcase.name
                info += "  ID: %s\n" % testcase.ID
                info += "  Command: %s\n" % testcase.command
                info += "  Auto: %s\n" % testcase.auto
                info += "  TimeOut: %s\n" % testcase.timeout
                info += "  Description: %s\n" % testcase.description
                #info += "  Status: %s\n" % testcase.status
                #info += "  Log location: %s\n" % testcase.log_location
                #info += "  Result: %s\n" % testcase.get_pretty_result()
            
            self.TestInfoEdit.clear()
            self.TestInfoEdit.append(info)
                
    def test_view_right_clicked(self, point):
        context_menu = QtGui.QMenu()
        index = self.TestsTreeView.indexAt(point)
        item = self.testsModel.itemFromIndex(index)
        if item.parent() is None:
            context_menu.addAction(self.actionRemoveTestSuite)
            context_menu.addAction(self.actionAddtoTaskQueue)
            context_menu.exec_(self.TestsTreeView.mapToGlobal(point))
        else:
            context_menu.addAction(self.actionAddtoTaskQueue)
            context_menu.exec_(self.TestsTreeView.mapToGlobal(point))
        
    def task_queue_view_right_clicked(self, point):
        context_menu = QtGui.QMenu()
        index = self.taskQueueListView.indexAt(point)
        item = self.taskQueueModel.itemFromIndex(index)

        context_menu.addAction(self.actionClearTaskQueue)
        if not item is None:
            context_menu.addAction(self.actionRemoveFromTaskQueue)
        context_menu.exec_(self.taskQueueListView.mapToGlobal(point))
        
    def _refresh_task_queue_view(self):
        task_queue = self.DUT_instance.list_all_tasks_in_task_queue()
        task_indexs = task_queue.keys()
        task_indexs.sort()
        task_indexs.reverse()
        self.taskQueueModel.clear()
        for task_index in task_indexs:
            task = task_queue[task_index]
            format_time = time.strftime("%d %b %H:%M:%S", time.localtime(float(task_index)))
            task_item = QtGui.QStandardItem(QtCore.QString("ID: %0 Name: %1 Time: %2").arg(task_index).arg(task.name).arg(format_time))
            #store the task_index in item data
            task_item.setData(QtCore.QVariant(task_index))
            
            self.taskQueueModel.appendRow(task_item)

    def add_test_to_task_queue(self):
        for selected_index in self.TestsTreeView.selectedIndexes():
            item = self.testsModel.itemFromIndex(selected_index)
            if item.parent() is None:
                #add test suite
                testsuite_name = str(item.text())
                logger.LOGGER.debug("Add testsuite to task queue: %s" % testsuite_name)
                self.DUT_instance.add_testsuite_to_task_queue(testsuite_name)
            else:
                #add test case
                testsuite_name = str(item.parent().text())
                testcase_name = str(item.text())
                testcase_id = item.data().toPyObject()
                logger.LOGGER.debug("Add testcase to task queue: %s, %s" % (testsuite_name, testcase_name))
                self.DUT_instance.add_testcase_to_task_queue(testsuite_name, testcase_id)
    
        self._refresh_task_queue_view()
    
    def remove_test_from_task_queue(self):
        for selected_index in self.taskQueueListView.selectedIndexes():
            task_item = self.taskQueueModel.itemFromIndex(selected_index)
            task_index = str(task_item.data().toString())
            
            self.DUT_instance.remove_testcase_from_task_queue(task_index)
            logger.LOGGER.debug("Remove task: %s, Index: %s" % (task_item.text(), repr(task_index)))
        
        self._refresh_task_queue_view()
        
    def clear_task_queue(self):
        self.DUT_instance.clean_task_queue()
        self._refresh_task_queue_view()
        
    def add_runner_and_monitor(self):
        self.DUT_instance.add_monitor()
        self.DUT_instance.add_runner()
        self.connect(self.DUT_instance.task_runner, self.DUT_instance.task_runner.updateDUTUI, self.refresh_without_checking_status)
        
        self.refresh_without_checking_status()
        
    def start_task_runner(self):
        self.DUT_instance.start_task_runner()
        
        self.actionStartRunner.setDisabled(True)
        self.actionPauseRunner.setEnabled(True)
        
        self.task_runner_running = True
        logger.LOGGER.debug("Start task runner")
        
    def pause_task_runner(self):
        self.DUT_instance.pause_task_runner()
        
        self.actionStartRunner.setEnabled(True)
        self.actionPauseRunner.setDisabled(True)
        
        self.task_runner_running = False
        logger.LOGGER.debug("Pause task runner")
        
    def refresh(self):
        refresh_dialog = RefreshDUTDialog(self)
        refresh_dialog.exec_()
        
    def refresh_without_checking_status(self):
        #set window title
        self.setWindowTitle(_translate("DUTWindow", "DUT IP: %s Name: %s Status: %s" % (self.ip, self.name, self.DUT_instance.pretty_status), None))
        #set action status
        if self.parent.staf_ready:
            self.actionRefresh.setEnabled(True)
        
            if self.DUT_instance.status & 0b11000000:
                #Cannot control DUT
                self.actionStartRunner.setDisabled(True)
                self.actionPauseRunner.setDisabled(True)
            else:
                if self.task_runner_running:
                    self.actionPauseRunner.setEnabled(True)
                else:
                    self.actionStartRunner.setEnabled(True)
            
        #refresh test view
        self._refresh_test_view()
        #refresh task queue
        self._refresh_task_queue_view()
        #refresh Server DUTView
        self.parent.refresh_without_checking_status()
    '''
    def taskRunnerExit(self):
        self.task_runner_running = False
        self.refresh_without_checking_status()
    '''
    def closeEvent(self, event):
        #need update parent's DUTWindow list when one DUTWindow close
        del self.parent.DUTWindows[self.ip]
    
class SettingsDialog(QtGui.QDialog, Ui_Settings):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        
        self.setupUi(self)
        
        #init the settings
        self.STAFDirEdit.setText(QtCore.QString("%0").arg(STAFServer.get_settings("STAF_dir")))
        self.loggingFileEdit.setText(QtCore.QString("%0").arg(logger.LOGGER.configs["logging_file"]))
        
        indexs = {"CRITICAL": 0,
                "ERROR": 1, 
                "WARNING": 2,
                "INFO": 3,
                "DEBUG": 4, }
        
        for key in indexs.keys():
            self.loggingFileLevel.insertItem(indexs[key], QtCore.QString(key))
            self.loggingStreamLevel.insertItem(indexs[key], QtCore.QString(key))
        
        logging_level_file = logger.level_name(logger.LOGGER.configs["logging_level_file"])
        logging_level_stream = logger.level_name(logger.LOGGER.configs["logging_level_stream"])
        
        self.loggingFileLevel.setCurrentIndex(indexs[logging_level_file])
        self.loggingStreamLevel.setCurrentIndex(indexs[logging_level_stream])

    def accept(self):
        STAFDir = str(self.STAFDirEdit.text())
        STAFServer.update_settings(STAF_dir=STAFDir)
        logger.LOGGER.config(  logging_file = str(self.loggingFileEdit.text()), 
                        logging_level_file = logger.level_name(str(self.loggingFileLevel.currentText())),
                        logging_level_stream = logger.level_name(str(self.loggingStreamLevel.currentText())) )
        logger.LOGGER.debug("Config staf dir: %s" % STAFDir)
        logger.LOGGER.debug("Config logging_file: %s" % str(self.loggingFileEdit.text()) )
        logger.LOGGER.debug("Config logging_level_file: %s" % str(self.loggingFileLevel.currentText()) )
        logger.LOGGER.debug("Config logging_level_stream: %s" % str(self.loggingStreamLevel.currentText()) )
        
        QtGui.QDialog.accept(self)

class AddDUTDialog(QtGui.QDialog, Ui_addDUT):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.DUTIP.setInputMask("000.000.000.000")
    
    def accept(self):
        ip = str(self.DUTIP.text())
        name = str(self.DUTName.text())
        logger.LOGGER.debug("Add DUT ip: %s name: %s" % (ip, name))
        STAFServer.add_DUT(ip, name)
        QtGui.QDialog.accept(self)
        
class RefreshAllThread(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)
    
    def run(self):
        for DUT_instance in STAFServer.DUTs():
            self.emit(QtCore.SIGNAL("notify_status"), "Refreshing DUT: %s..." % DUT_instance.ip)
            #refresh DUT, will check DUT status, time cost
            DUT_instance.refresh()
            #this signal will update DUT view
            self.emit(QtCore.SIGNAL("notify_DUTsView"))
            
        time.sleep(0.1)
        self.emit(QtCore.SIGNAL("notify_stop"))
            
class RefreshAllDialog(QtGui.QDialog, Ui_refreshDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        
        self.parent = parent
        self.progressBar.setRange(0, 0)
        self.refresh_thread = RefreshAllThread()
        
        #signal and slot
        self.connect(self.refresh_thread, QtCore.SIGNAL("notify_status"), self.update_status)
        self.connect(self.refresh_thread, QtCore.SIGNAL("notify_DUTsView"), self.update_DUTsView)
        self.connect(self.refresh_thread, QtCore.SIGNAL("notify_stop"), self.accept)

        self.refresh_thread.start()

    def update_status(self, status):
        self.statusLabel.setText(status)
        
    def update_DUTsView(self):
        self.parent.refresh_without_checking_status()
        
class MainWindow(QtGui.QMainWindow, Ui_XSTAFMainWindow):
    #STAF ready signal
    STAFReady = QtCore.SIGNAL("STAFReady")
    
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        
        #view
        self.setupUi(self)
        
        #model
        self.DUTsModel = QtGui.QStandardItemModel(self.DUTView)
        self.DUTView.setModel(self.DUTsModel)
        
        #signals and slots
        self.connect(self.actionNewWorkSpace, QtCore.SIGNAL("triggered(bool)"), self.new_work_space)
        self.connect(self.actionOpenWorkSpace, QtCore.SIGNAL("triggered(bool)"), self.open_work_space)
        self.connect(self.actionSaveWorkSpace, QtCore.SIGNAL("triggered(bool)"), self.save_work_space)
        
        self.connect(self.actionSettings, QtCore.SIGNAL("triggered(bool)"), self.settings)
        self.connect(self.actionCheckAndStartSTAF, QtCore.SIGNAL("triggered(bool)"), self.check_and_start_STAF)
        self.connect(self.actionRefresh, QtCore.SIGNAL("triggered(bool)"), self.refresh)
        self.connect(self.actionAddDUT, QtCore.SIGNAL("triggered(bool)"), self.add_DUT)
        self.connect(self.actionRemoveDUT, QtCore.SIGNAL("triggered(bool)"), self.remove_DUT)
        
        #self.connect(self.DUTView, QtCore.SIGNAL("clicked(QModelIndex)"), self.DUT_clicked)
        self.connect(self.DUTView, QtCore.SIGNAL("doubleClicked(QModelIndex)"), self.DUT_double_clicked)
        
        #connect logger signal to mainWindow slot
        self.connect(logger.LOGGER, logger.LOGGER.updateLog, self.update_log)
        #config logger with default configuration
        logger.LOGGER.config()
        
        #init some status
        self.actionSaveWorkSpace.setDisabled(True)
        self.actionRefresh.setDisabled(True)
        self.actionAddDUT.setDisabled(True)
        self.actionRemoveDUT.setDisabled(True)

        #DUTWindow list
        self.DUTWindows = {}
        
        #flags
        self.staf_ready = False
        self.has_workspace = False
        
    def settings(self):
        settingsDialog = SettingsDialog()
        settingsDialog.exec_()
        
    def update_log(self, record):
        levelno = record.levelno
        if(levelno>=logger.level_name("CRITICAL")):
            color_str = '<div style="color:red">%s</div>' # red
        elif(levelno>=logger.level_name("ERROR")):
            color_str = '<div style="color:red">%s</div>' # red
        elif(levelno>=logger.level_name("WARN")):
            color_str = '<div style="color:yellow">%s</div>' # yellow
        elif(levelno>=logger.level_name("INFO")):
            color_str = '<div style="color:black">%s</div>' # black
        elif(levelno>=logger.level_name("DEBUG")):
            color_str = '<div style="color:gray">%s</div>' # gray
        else:
            color_str = '<div style="color:black">%s</div>' # black
        msg = color_str % record.msg
        self.XSTAFLogEdit.append(msg)
        
    def new_work_space(self):
        if STAFServer.check_if_default_workspace_exist():
            #ask user if load exist workspace or create a new one
            load_default = ConfirmDialog.confirm(self, "Detect existing project, load it or not?")
            if load_default:
                STAFServer.load_workspace()
            else:
                STAFServer.new_workspace()
        else:
            STAFServer.new_workspace()
        
        self.has_workspace = True
        self.refresh_without_checking_status()
    
    def open_work_space(self):
        #ask user if save workspace before open new workspace
        save_current = ConfirmDialog.confirm(self, "Save current workspace before opening new one?")
        if save_current:
            self.save_work_space()
    
        workspace_path = str(QtGui.QFileDialog.getExistingDirectory (self, "Open WorkSpace"))
        if os.path.isdir(workspace_path):
            STAFServer.load_workspace(workspace_path)
            self.has_workspace = True
            self.refresh_without_checking_status()
    
    def save_work_space(self):
        if STAFServer.new:
            workspace_path = str(QtGui.QFileDialog.getExistingDirectory (self, "Save WorkSpace"))
            STAFServer.save_workspace(workspace_path)
        else:
            STAFServer.save_workspace()
            
    def check_and_start_STAF(self):
        STAFServer.check_and_start_staf()
        self.staf_ready = True
        #emit staf ready signal to update DUT ui
        self.emit(self.STAFReady)
        
    def refresh(self):
        refresh_dialog = RefreshAllDialog(self)
        refresh_dialog.exec_()
        
    def refresh_without_checking_status(self):
        self.DUTsModel.clear()
        self.DUTsModel.setHorizontalHeaderItem(0, QtGui.QStandardItem(QtCore.QString("Name")))
        self.DUTsModel.setHorizontalHeaderItem(1, QtGui.QStandardItem(QtCore.QString("IP")))
        self.DUTsModel.setHorizontalHeaderItem(2, QtGui.QStandardItem(QtCore.QString("Status")))
        for DUT_instance in STAFServer.DUTs():
            IP = QtGui.QStandardItem(QtCore.QString("%0").arg(DUT_instance.ip))
            name = QtGui.QStandardItem(QtCore.QString("%0").arg(DUT_instance.name))
            status = QtGui.QStandardItem(QtCore.QString("%0").arg(DUT_instance.pretty_status))
            self.DUTsModel.appendRow([name, IP, status])
            
        if self.has_workspace:
            #if we have workspace, we can enable follow action
            self.actionSaveWorkSpace.setEnabled(True)
            self.actionAddDUT.setEnabled(True)
            self.actionRemoveDUT.setEnabled(True)
        
        if self.staf_ready:
            #if staf start, we can enable follow action
            self.actionRefresh.setEnabled(True)

    def add_DUT(self):
        addDUTDialog = AddDUTDialog()
        addDUTDialog.exec_()
        self.refresh_without_checking_status()
        
    def remove_DUT(self):
        for selectedIndex in self.DUTView.selectedIndexes():
            DUT_IP = str(self.DUTsModel.itemFromIndex(self.DUTsModel.index(selectedIndex.row(), 1)).text())
            if STAFServer.has_DUT(DUT_IP):
                STAFServer.remove_DUT(DUT_IP)
        self.refresh_without_checking_status()
    
    '''
    def DUT_clicked(self, index):
        logger.LOGGER.debug("Click: column: %s, raw: %s" % (index.column(), index.row()))
        DUT_IP = self.DUTsModel.itemFromIndex(self.DUTsModel.index(index.row(), 1)).text()
        DUT_name = self.DUTsModel.itemFromIndex(self.DUTsModel.index(index.row(), 0)).text()
        self.infoEdit.clear()
        self.infoEdit.append(QtCore.QString("DUT IP: %0 name: %1").arg(DUT_IP).arg(DUT_name))
    '''
    
    def DUT_double_clicked(self, index):
        logger.LOGGER.debug("Double Click: column: %s, raw: %s" % (index.column(), index.row()))
        DUT_IP = str(self.DUTsModel.itemFromIndex(self.DUTsModel.index(index.row(), 1)).text())
        if DUT_IP not in self.DUTWindows:
            DUT_window = DUTWindow(self, DUT_IP)
            self.DUTWindows[DUT_IP] = DUT_window
            DUT_window.show()
        else:
            DUT_window = self.DUTWindows[DUT_IP]
            DUT_window.setFocus()
        
    def closeEvent(self, event):
        #we need terminate all threads before close
        #stop DUT threads
        for DUT_instance in STAFServer.DUTs():
            DUT_instance.pause_task_runner()
        
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())