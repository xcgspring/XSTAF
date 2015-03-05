
import time
import threading
from PyQt4 import QtCore, QtGui
from ui.ui_mainWindow import Ui_XSTAFMainWindow, _translate
from ui.ui_settingsDialog import Ui_Settings
from ui.ui_addDUT import Ui_addDUT
from ui.ui_DUT import Ui_DUTWindow
from ui.ui_refresh import Ui_refreshDialog

import logger
from server import Server

STAFServer = Server()

class DUTWindow(QtGui.QMainWindow, Ui_DUTWindow):
    def __init__(self, parent, ip):
        self.parent = parent
        self.ip = ip
        self.DUT_instance = STAFServer.DUTs[ip]
        self.name = self.DUT_instance.name
        QtGui.QMainWindow.__init__(self, self.parent)

        #view
        self.setupUi(self)
        #set DUT window title
        self.setWindowTitle("DUTWindow", "DUT IP: %s Name: %s Status: %s" % (self.ip, self.name, self.pretty_status), None)
        
        #model
        self.testsModel = QtGui.QStandardItemModel()
        self.TestsTreeView.setModel(self.testsModel)
        
        self.taskQueueModel = QtGui.QStandardItemModel()
        self.taskQueueListView.setModel(self.taskQueueModel)
        
        #set DUTWindow UI status
        self.actionRemoveTestSuite.setDisabled(True)
        self.actionStartRunner.setDisabled(True)
        self.actionPauseRunner.setDisabled(True)
        
        #signals and slots
        self.connect(self.actionAddTestSuite, QtCore.SIGNAL("triggered(bool)"), self.add_test_suite)
        self.connect(self.actionRemoveTestSuite, QtCore.SIGNAL("triggered(bool)"), self.remove_test_suite)
        self.connect(self.actionRefresh, QtCore.SIGNAL("triggered(bool)"), self.refresh)
        
        self.connect(self.actionAddtoTaskQueue, QtCore.SIGNAL("triggered(bool)"), self.add_test_to_task_queue)
        self.connect(self.actionRemoveFromTaskQueue, QtCore.SIGNAL("triggered(bool)"), self.remove_test_from_task_queue)
        
        self.connect(self.actionStartRunner, QtCore.SIGNAL("triggered(bool)"), self.start_task_runner)
        self.connect(self.actionPauseRunner, QtCore.SIGNAL("triggered(bool)"), self.pause_task_runner)
        
        self.connect(self.TestsTreeView, QtCore.SIGNAL("clicked(QModelIndex)"), self.test_view_clicked)
        self.connect(self.TestsTreeView, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.test_view_right_clicked)
        self.connect(self.taskQueueListView, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.task_queue_view_right_clicked)
        
        #some states
        self.task_runner_running = False
        
    def _refresh_test_view(self):
        self.testsModel.clear()
        for testsuite in self.DUT_instance.testsuites.items():
            testsuite_name = testsuite[0]
            
            testsuite_item = QtGui.QStandardItem(QtCore.QString("%0").arg(testsuite_name))
            for testcase in testsuite[1].testcases.items():
                testcase_item = QtGui.QStandardItem(QtCore.QString("%0").arg(testcase[0]))
                testsuite_item.appendRow(testcase_item)
                
            self.testsModel.appendRow(testsuite_item)
        
    def add_test_suite(self):
        test_suite_file = QtGui.QFileDialog.getOpenFileName(self, "Add TestSuite")
        import os
        if os.path.isfile(test_suite_file):
            testsuite = self.DUT_instance.add_testsuite(str(test_suite_file))
            self._refresh_test_view()
            logger.LOGGER().debug("Add testsuite: %s" % test_suite_file)
        
    def remove_test_suite(self):
        for selected_index in self.TestsTreeView.selectedIndexes():
            item = self.testsModel.itemFromIndex(selected_index)
            if item.parent() is None:
                self.DUT_instance.remove_testsuite(str(item.text()))
                self._refresh_test_view()
                logger.LOGGER().debug("Remove testsuite: %s" % item.text())
        
    def test_view_clicked(self, index):
        logger.LOGGER().debug("Click: column: %s, raw: %s" % (index.column(), index.row()))
        item = self.testsModel.itemFromIndex(index)

        if item.parent() is None:
            #click on testsuite
            self.actionRemoveTestSuite.setEnabled(True)
            
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
                logger.LOGGER().debug("Add testsuite to task queue: %s" % testsuite_name)
                self.DUT_instance.add_testsuite_to_task_queue(testsuite_name)
            else:
                #add test case
                testsuite_name = str(item.parent().text())
                testcase_name = str(item.text())
                logger.LOGGER().debug("Add testcase to task queue: %s, %s" % (testsuite_name, testcase_name))
                self.DUT_instance.add_testcase_to_task_queue(testsuite_name, testcase_name)
    
        self._refresh_task_queue_view()
    
    def remove_test_from_task_queue(self):
        for selected_index in self.taskQueueListView.selectedIndexes():
            task_item = self.taskQueueModel.itemFromIndex(selected_index)
            task_index = str(task_item.data().toString())
            
            self.DUT_instance.remove_testcase_from_task_queue(task_index)
            logger.LOGGER().debug("Remove task: %s, Index: %s" % (task_item.text(), repr(task_index)))
        
        self._refresh_task_queue_view()
        
    def start_task_runner(self):
        self.DUT_instance.start_task_runner()
        
        self.actionStartRunner.setDisabled(True)
        self.actionPauseRunner.setEnabled(True)
        
        self.task_runner_running = True
        logger.LOGGER().debug("Start task runner")
        
    def pause_task_runner(self):
        self.DUT_instance.pause_task_runner()
        
        self.actionStartRunner.setEnabled(True)
        self.actionPauseRunner.setDisabled(True)
        
        self.task_runner_running = False
        logger.LOGGER().debug("Pause task runner")
        
    def refresh(self):
        #get DUT status
        self.DUT_instance.refresh()
        self.pretty_status = self.DUT_instance.pretty_status
        self.status = self.DUT_instance.status
        
        #set window title
        self.setWindowTitle("DUTWindow", "DUT IP: %s Name: %s Status: %s" % (self.ip, self.name, self.pretty_status), None)
        #set action status
        if self.status & 0b10000000:
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
            
    def closeEvent(self, event):
        #need update parent's DUTWindow list when one DUTWindow close
        del self.parent.DUTWindows[self.ip]
    
class SettingsDialog(QtGui.QDialog, Ui_Settings):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        
        self.setupUi(self)
        
        #init the settings
        self.STAFDirEdit.setText(QtCore.QString("%0").arg(STAFServer.get_settings("STAF_dir")))
        self.loggingFileEdit.setText(QtCore.QString("%0").arg(logger.CONFIGS["logging_file"]))
        
        indexs = {"CRITICAL": 0,
                "ERROR": 1, 
                "WARNING": 2,
                "INFO": 3,
                "DEBUG": 4, }
        
        for key in indexs.keys():
            self.loggingFileLevel.insertItem(indexs[key], QtCore.QString(key))
            self.loggingStreamLevel.insertItem(indexs[key], QtCore.QString(key))
        
        logging_level_file = logger.level_name(logger.CONFIGS["logging_level_file"])
        logging_level_stream = logger.level_name(logger.CONFIGS["logging_level_stream"])
        
        self.loggingFileLevel.setCurrentIndex(indexs[logging_level_file])
        self.loggingStreamLevel.setCurrentIndex(indexs[logging_level_stream])

    def accept(self):
        STAFDir = str(self.STAFDirEdit.text())
        STAFServer.update_settings(STAF_dir=STAFDir)
        logger.CONFIGS["logging_file"] = str(self.loggingFileEdit.text())
        logger.CONFIGS["logging_level_file"] = logger.level_name(str(self.loggingFileLevel.currentText()))
        logger.CONFIGS["logging_level_stream"] = logger.level_name(str(self.loggingStreamLevel.currentText()))
        logger.config()
        logger.LOGGER().debug("Config staf dir: %s" % STAFDir)
        logger.LOGGER().debug("Config logging_file: %s" % str(self.loggingFileEdit.text()) )
        logger.LOGGER().debug("Config logging_level_file: %s" % str(self.loggingFileLevel.currentText()) )
        logger.LOGGER().debug("Config logging_level_stream: %s" % str(self.loggingStreamLevel.currentText()) )
        
        QtGui.QDialog.accept(self)

class AddDUTDialog(QtGui.QDialog, Ui_addDUT):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.DUTIP.setInputMask("000.000.000.000")
    
    def accept(self):
        ip = str(self.DUTIP.text())
        name = str(self.DUTName.text())
        logger.LOGGER().debug("Add DUT ip: %s name: %s" % (ip, name))
        STAFServer.add_DUT(ip, name)
        QtGui.QDialog.accept(self)
        
class RefreshThread(QtCore.QThread):
    
    def __init__(self):
        QtCore.QThread.__init__(self)
    
    def run(self):
        for DUT in STAFServer.DUTs.items():
            DUT_instance = DUT[1]
            self.emit(QtCore.SIGNAL("notify_status"), "Refreshing DUT: %s..." % DUT_instance.ip)
            #refresh DUT, will check DUT status, time cost
            DUT_instance.refresh()
            #this signal will update DUT view
            self.emit(QtCore.SIGNAL("notify_DUTsView"))
            
        time.sleep(0.1)
        self.emit(QtCore.SIGNAL("notify_stop"))
            
class RefreshDialog(QtGui.QDialog, Ui_refreshDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        
        self.parent = parent
        self.progressBar.setRange(0, 0)
        self.refresh_thread = RefreshThread()
        
        #signal and slot
        self.connect(self.refresh_thread, QtCore.SIGNAL("notify_status"), self.update_status)
        self.connect(self.refresh_thread, QtCore.SIGNAL("notify_DUTsView"), self.update_DUTsView)
        self.connect(self.refresh_thread, QtCore.SIGNAL("notify_stop"), self.accept)

        self.refresh_thread.start()

        
    def update_status(self, status):
        self.statusLabel.setText(status)
        
    def update_DUTsView(self):
        self.parent.refresh_without_checking_status()
        
class EditStream(object):
    def __init__(self, edit):
        self.edit = edit
        
    def write(self, string):
        self.edit.append(QtCore.QString(string))
        
class MainWindow(QtGui.QMainWindow, Ui_XSTAFMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        
        #view
        self.setupUi(self)
        
        #model
        self.DUTsModel = QtGui.QStandardItemModel()
        self.DUTView.setModel(self.DUTsModel)
        
        self.DUTsModel.setHorizontalHeaderItem(0, QtGui.QStandardItem(QtCore.QString("Name")))
        self.DUTsModel.setHorizontalHeaderItem(1, QtGui.QStandardItem(QtCore.QString("IP")))
        self.DUTsModel.setHorizontalHeaderItem(2, QtGui.QStandardItem(QtCore.QString("Status")))
        
        #signals and slots
        self.connect(self.actionSettings, QtCore.SIGNAL("triggered(bool)"), self.settings)
        self.connect(self.actionCheckAndStartSTAF, QtCore.SIGNAL("triggered(bool)"), self.check_and_start_STAF)
        self.connect(self.actionRefresh, QtCore.SIGNAL("triggered(bool)"), self.refresh)
        self.connect(self.actionAddDUT, QtCore.SIGNAL("triggered(bool)"), self.add_DUT)
        self.connect(self.actionRemoveDUT, QtCore.SIGNAL("triggered(bool)"), self.remove_DUT)
        
        #self.connect(self.DUTView, QtCore.SIGNAL("clicked(QModelIndex)"), self.DUT_clicked)
        self.connect(self.DUTView, QtCore.SIGNAL("doubleClicked(QModelIndex)"), self.DUT_double_clicked)
        
        #init some status
        self.actionRefresh.setDisabled(True)
        self.actionAddDUT.setDisabled(True)
        self.actionRemoveDUT.setDisabled(True)
        
        #DUTWindow list
        self.DUTWindows = {}
        
        #init logger
        self.init_logger()
        
    def settings(self):
        settingsDialog = SettingsDialog()
        settingsDialog.exec_()
        
    def init_logger(self):
        #set logger stream handle to XSTAFLogEdit
        #other settings use default
        logger.CONFIGS["logging_stream"] = EditStream(self.XSTAFLogEdit)
        logger.config()
        
    def check_and_start_STAF(self):
        STAFServer.check_and_start_staf()

        self.actionRefresh.setEnabled(True)
        self.actionAddDUT.setEnabled(True)
        self.actionRemoveDUT.setEnabled(True)
            
    def refresh(self):
        refresh_dialog = RefreshDialog(self)
        refresh_dialog.exec_()
        
    def refresh_without_checking_status(self):
        self.DUTsModel.clear()
        self.DUTsModel.setHorizontalHeaderItem(0, QtGui.QStandardItem(QtCore.QString("Name")))
        self.DUTsModel.setHorizontalHeaderItem(1, QtGui.QStandardItem(QtCore.QString("IP")))
        self.DUTsModel.setHorizontalHeaderItem(2, QtGui.QStandardItem(QtCore.QString("Status")))
        for DUT in STAFServer.DUTs.items():
            DUT_instance = DUT[1]
            IP = QtGui.QStandardItem(QtCore.QString("%0").arg(DUT_instance.ip))
            name = QtGui.QStandardItem(QtCore.QString("%0").arg(DUT_instance.name))
            status = QtGui.QStandardItem(QtCore.QString("%0").arg(DUT_instance.pretty_status))
            self.DUTsModel.appendRow([name, IP, status])
        
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
        logger.LOGGER().debug("Click: column: %s, raw: %s" % (index.column(), index.row()))
        DUT_IP = self.DUTsModel.itemFromIndex(self.DUTsModel.index(index.row(), 1)).text()
        DUT_name = self.DUTsModel.itemFromIndex(self.DUTsModel.index(index.row(), 0)).text()
        self.infoEdit.clear()
        self.infoEdit.append(QtCore.QString("DUT IP: %0 name: %1").arg(DUT_IP).arg(DUT_name))
    '''
    
    def DUT_double_clicked(self, index):
        logger.LOGGER().debug("Double Click: column: %s, raw: %s" % (index.column(), index.row()))
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
        for DUT in STAFServer.DUTs.items():
            DUT_instance = DUT[1]
            DUT_instance.pause_task_runner()
        
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())