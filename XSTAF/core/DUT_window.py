
import os
import time
from PyQt4 import QtCore, QtGui

from XSTAF.core.logger import LOGGER
from XSTAF.core.dialogs import RefreshDUTDialog
from XSTAF.ui.ui_DUT import Ui_DUTWindow, _translate, _fromUtf8

class DUTWindow(QtGui.QMainWindow, Ui_DUTWindow):
    def __init__(self, main_window, ip):
        self.parent = main_window
        self.server = main_window.server
        self.ip = ip
        self.workspace = self.server.get_workspace()
        self.dut = self.workspace.get_dut(ip)
        QtGui.QMainWindow.__init__(self, main_window)
        #view
        self.setupUi(self)
        #model
        self.testsModel = QtGui.QStandardItemModel(self.TestsTreeView)
        self.TestsTreeView.setModel(self.testsModel)
        self.taskQueueModel = QtGui.QStandardItemModel(self.taskQueueListView)
        self.taskQueueListView.setModel(self.taskQueueModel)

        ##########################################
        #signals and slots
        
        #for actions
        self.connect(self.actionAddTestSuite, QtCore.SIGNAL("triggered(bool)"), self.add_test_suite)
        self.connect(self.actionRemoveTestSuite, QtCore.SIGNAL("triggered(bool)"), self.remove_test_suite)
        self.connect(self.actionRefresh, QtCore.SIGNAL("triggered(bool)"), self.refresh)
        self.connect(self.actionAddtoTaskQueue, QtCore.SIGNAL("triggered(bool)"), self.add_test_to_task_queue)
        self.connect(self.actionRemoveFromTaskQueue, QtCore.SIGNAL("triggered(bool)"), self.remove_test_from_task_queue)
        self.connect(self.actionClearTaskQueue, QtCore.SIGNAL("triggered(bool)"), self.clear_task_queue)
        self.connect(self.actionStartRunner, QtCore.SIGNAL("triggered(bool)"), self.start_task_runner)
        self.connect(self.actionPauseRunner, QtCore.SIGNAL("triggered(bool)"), self.pause_task_runner)

        #for test tree view and task queue view
        self.connect(self.TestsTreeView, QtCore.SIGNAL("clicked(QModelIndex)"), self.test_view_clicked)
        self.connect(self.TestsTreeView, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.test_view_right_clicked)
        self.connect(self.taskQueueListView, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.task_queue_view_right_clicked)
        
        #for local STAF process status change
        self.connect(self.server, self.server.staf_status_change, self.refresh_ui)
        #
        self.connect(self.dut, self.dut.status_change, self.handle_dut_status_change)
        ##########################################
        
        #runner status
        self.task_runner_running = False

        #refresh ui
        self.handle_dut_status_change()
        
    def handle_dut_status_change(self):
        if not self.dut.status:
            self.dut.add_runner()
            task_runner = self.dut.get_runner()
            #check if runner running
            self.task_runner_running = self.dut.is_runner_running()
            #connect runner signals to DUT view slots
            self.connect(task_runner, task_runner.test_result_change, self._refresh_test_view)
            self.connect(task_runner, task_runner.task_queue_change, self._refresh_task_queue_view)
        else:
            self.dut.remove_runner()
            self.task_runner_running = False
        self.refresh_ui()

    def add_test_suite(self):
        test_suite_file = QtGui.QFileDialog.getOpenFileName(self, "Add TestSuite")
        if os.path.isfile(test_suite_file):
            self.dut.add_testsuite(str(test_suite_file))
            self._refresh_test_view()
            LOGGER.debug("Add testsuite: %s", test_suite_file)

    def remove_test_suite(self):
        for selected_index in self.TestsTreeView.selectedIndexes():
            item = self.testsModel.itemFromIndex(selected_index)
            if item.parent() is None:
                LOGGER.debug("Remove testsuite: %s", item.text())
                self.dut.remove_testsuite(str(item.text()))
                self._refresh_test_view()

    def test_view_clicked(self, index):
        #LOGGER.debug("Click: column: %s, raw: %s", (index.column(), index.row()))
        item = self.testsModel.itemFromIndex(index)
        if not item is None:
            if item.parent() is None:
                #click on testsuite
                self.actionRemoveTestSuite.setEnabled(True)
                #print testsuite info in test view
                testsuite = self.dut.get_testsuite(str(item.text()))
                info = "TestSuite: %s\n" % testsuite.test_suite_file
                info += "  Total test case: %d\n" % testsuite.testcase_number()

            elif item.parent().parent() is None:
                self.actionRemoveTestSuite.setDisabled(True)
                #print testcase info in test view
                testsuite_name = str(item.parent().text())
                testcase_id = item.data().toPyObject()
                testsuite = self.dut.get_testsuite(testsuite_name)
                testcase = testsuite.get_testcase(testcase_id)
                info = "TestCase: %s\n" % testcase.name
                info += "  ID: %s\n" % testcase.ID
                info += "  Command: %s\n" % testcase.command
                info += "  Auto: %s\n" % testcase.auto
                info += "  TimeOut: %s\n" % testcase.timeout
                info += "  Description: %s\n" % testcase.description

            else:
                self.actionRemoveTestSuite.setDisabled(True)
                testsuite_name = str(item.parent().parent().text())
                testcase_id = item.parent().data().toPyObject()
                run_id = str(item.data().toPyObject())
                testsuite = self.dut.get_testsuite(testsuite_name)
                testcase = testsuite.get_testcase(testcase_id)
                run = testcase.get_run(run_id)
                info = "TestRun: \n"
                info += "Start: %s\n" % run.start
                info += "End: %s\n" % run.end
                info += "  Status: %s\n" % run.status
                info += "  Log location: %s\n" % run.log_location
                info += "  Result: %s\n" % run.pretty_result

            self.TestInfoEdit.clear()
            self.TestInfoEdit.append(info)

    def test_view_right_clicked(self, point):
        context_menu = QtGui.QMenu()
        index = self.TestsTreeView.indexAt(point)
        item = self.testsModel.itemFromIndex(index)
        if item is None:
            return

        if item.parent() is None:
            #test suite level
            context_menu.addAction(self.actionRemoveTestSuite)
            context_menu.addAction(self.actionAddtoTaskQueue)
            context_menu.exec_(self.TestsTreeView.mapToGlobal(point))
        elif item.parent().parent() is None:
            #test case level
            context_menu.addAction(self.actionAddtoTaskQueue)
            context_menu.exec_(self.TestsTreeView.mapToGlobal(point))
        else:
            #run level
            return

    def task_queue_view_right_clicked(self, point):
        context_menu = QtGui.QMenu()
        index = self.taskQueueListView.indexAt(point)
        item = self.taskQueueModel.itemFromIndex(index)

        context_menu.addAction(self.actionClearTaskQueue)
        if not item is None:
            context_menu.addAction(self.actionRemoveFromTaskQueue)
        context_menu.exec_(self.taskQueueListView.mapToGlobal(point))

    def add_test_to_task_queue(self):
        for selected_index in self.TestsTreeView.selectedIndexes():
            item = self.testsModel.itemFromIndex(selected_index)
            if item.parent() is None:
                #add test suite
                testsuite_name = str(item.text())
                LOGGER.debug("Add testsuite to task queue: %s", testsuite_name)
                self.dut.add_testsuite_to_task_queue(testsuite_name)
            else:
                #add test case
                testsuite_name = str(item.parent().text())
                testcase_name = str(item.text())
                testcase_id = item.data().toPyObject()
                LOGGER.debug("Add testcase to task queue: %s, %s", testsuite_name, testcase_name)
                self.dut.add_testcase_to_task_queue(testsuite_name, testcase_id)

        self._refresh_task_queue_view()

    def remove_test_from_task_queue(self):
        for selected_index in self.taskQueueListView.selectedIndexes():
            task_item = self.taskQueueModel.itemFromIndex(selected_index)
            task_index = str(task_item.data().toString())

            self.dut.remove_testcase_from_task_queue(task_index)
            LOGGER.debug("Remove task: %s, Index: %s", task_item.text(), repr(task_index))

        self._refresh_task_queue_view()

    def clear_task_queue(self):
        self.dut.clean_task_queue()
        self._refresh_task_queue_view()

    def start_task_runner(self):
        self.dut.start_runner()

        self.actionStartRunner.setDisabled(True)
        self.actionPauseRunner.setEnabled(True)

        self.task_runner_running = True
        LOGGER.debug("Start task runner")

    def pause_task_runner(self):
        self.dut.stop_runner()

        self.actionStartRunner.setEnabled(True)
        self.actionPauseRunner.setDisabled(True)

        self.task_runner_running = False
        LOGGER.debug("Stop task runner")

    def refresh(self):
        refresh_dialog = RefreshDUTDialog(self)
        refresh_dialog.exec_()

    def _refresh_test_view(self):
        notRunIcon = QtGui.QIcon()
        notRunIcon.addPixmap(QtGui.QPixmap(_fromUtf8(":icons/icons/not-run.png")))
        failIcon = QtGui.QIcon()
        failIcon.addPixmap(QtGui.QPixmap(_fromUtf8(":icons/icons/fail.png")))
        passIcon = QtGui.QIcon()
        passIcon.addPixmap(QtGui.QPixmap(_fromUtf8(":icons/icons/pass.png")))
        
        #keep node expanded info
        #after refresh, should restore the expanded node
        expanded_testsuites = []
        expanded_testcases = []
        for i in range(self.testsModel.rowCount()):
            testsuite_item = self.testsModel.item(i)
            testsuite_index = self.testsModel.indexFromItem(testsuite_item)
            if self.TestsTreeView.isExpanded(testsuite_index):
                testsuite_name = testsuite_item.text()
                expanded_testsuites.append(testsuite_name)
            for i in range(testsuite_item.rowCount()):
                testcase_item = testsuite_item.child(i)
                testcase_index = self.testsModel.indexFromItem(testcase_item)
                if self.TestsTreeView.isExpanded(testcase_index):
                    testcase_id = testcase_item.data().toPyObject()
                    expanded_testcases.append(testcase_id)
                
        #LOGGER.debug("expanded test suite: %s" % repr(expanded_testsuites))
        #LOGGER.debug("expanded test case: %s" % repr(expanded_testcases))
        
        self.testsModel.clear()
        for testsuite in self.dut.testsuites():
            testsuite_item = QtGui.QStandardItem(QtCore.QString("%0").arg(testsuite.name))
            self.testsModel.appendRow(testsuite_item)
            if testsuite.name in expanded_testsuites:
                testsuite_index = self.testsModel.indexFromItem(testsuite_item)
                self.TestsTreeView.expand(testsuite_index)
            
            for testcase in testsuite.testcases():
                testcase_item = QtGui.QStandardItem(QtCore.QString(testcase.name))
                for run in testcase.runs():
                    if run.result & 0b10000000:
                        icon = notRunIcon
                    elif run.result & 0b00000001:
                        icon = failIcon
                    elif not run.result:
                        icon = passIcon
                    else:
                        LOGGER.warn("Encounter unexpected test result: %s", run.result)
                        icon = QtGui.QIcon()
                    format_time = time.strftime("%d %b %H:%M:%S", time.localtime(float(run.start)))
                    run_item = QtGui.QStandardItem(icon, QtCore.QString("Run begin at: %s" % format_time))
                    run_id = run.start
                    run_item.setData(QtCore.QVariant(run_id))
                    testcase_item.appendRow(run_item)
                #store test id in test case item
                testcase_id = testcase.ID
                testcase_item.setData(QtCore.QVariant(testcase_id))
                testsuite_item.appendRow(testcase_item)
                if testcase_id in expanded_testcases:
                    testcase_index = self.testsModel.indexFromItem(testcase_item)
                    self.TestsTreeView.expand(testcase_index)

    def _refresh_task_queue_view(self):
        task_queue = self.dut.list_all_tasks_in_task_queue()
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
        
    def refresh_ui(self):
        #set window title
        self.setWindowTitle(_translate("DUTWindow", "DUT IP: %s Name: %s Status: %s" % (self.ip, self.dut.name, self.dut.pretty_status), None))
        #set action status
        if not self.parent.staf_status:
            self.actionRefresh.setEnabled(True)
            
            if not self.dut.status:
                if self.task_runner_running:
                    self.actionStartRunner.setDisabled(True)
                    self.actionPauseRunner.setEnabled(True)
                else:
                    self.actionStartRunner.setEnabled(True)
                    self.actionPauseRunner.setDisabled(True)
            elif self.dut.status & 0b11000000:
                #Cannot control DUT
                self.actionStartRunner.setDisabled(True)
                self.actionPauseRunner.setDisabled(True)

        #refresh test view
        self._refresh_test_view()
        #refresh task queue
        self._refresh_task_queue_view()
        #refresh Server DUTView
        self.parent.refresh_ui()
        
    def closeEvent(self, event):
        #need update parent's DUTWindow list when one DUTWindow close
        del self.parent.DUTWindows[self.ip]
