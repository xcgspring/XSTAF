
from PyQt4 import QtCore, QtGui
from ui.ui_mainWindow import Ui_XSTAFMainWindow
from ui.ui_settingsDialog import Ui_Settings
from ui.ui_addDUT import Ui_addDUT
from ui.ui_DUT import Ui_DUTWindow, _translate

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
        
        #model
        self.testsModel = QtGui.QStandardItemModel()
        self.TestsTreeView.setModel(self.testsModel)
        
        #set DUTWindow UI status
        self.actionRemoveTestSuite.setDisabled(True)
        self.actionRunTest.setDisabled(True)
        self.actionPauseStopTest.setDisabled(True)
        
        #signals and slots
        self.connect(self.actionAddTestSuite, QtCore.SIGNAL("triggered(bool)"), self.add_test_suite)
        self.connect(self.actionRemoveTestSuite, QtCore.SIGNAL("triggered(bool)"), self.remove_test_suite)
        self.connect(self.actionRefresh, QtCore.SIGNAL("triggered(bool)"), self.set_UI_status)
        
        self.connect(self.TestsTreeView, QtCore.SIGNAL("clicked(QModelIndex)"), self.test_clicked)
        
    def add_test_suite(self):
        test_suite_file = QtGui.QFileDialog.getOpenFileName(self, "Add TestSuite")
        import os
        if os.path.isfile(test_suite_file):
            testsuite = self.DUT_instance.add_testsuite(str(test_suite_file))
            
            testsuite_item = QtGui.QStandardItem(QtCore.QString("%0").arg(testsuite.name))
            for testcase in testsuite.testcases.items():
                testcase_item = QtGui.QStandardItem(QtCore.QString("%0").arg(testcase[0]))
                testsuite_item.appendRow(testcase_item)
                
            self.testsModel.appendRow(testsuite_item)
        
    def remove_test_suite(self):
        for selected_index in self.TestsTreeView.selectedIndexes():
            item = self.testsModel.itemFromIndex(selected_index)
            if item.parent() is None:
                self.DUT_instance.remove_testsuite(str(item.text()))
                self.testsModel.removeRow(selected_index.row())
        
    def test_clicked(self, index):
        print("Click: column: %s, raw: %s" % (index.column(), index.row()))
        item = self.testsModel.itemFromIndex(index)

        if item.parent() is None:
            #click on testsuite
            self.actionRemoveTestSuite.setEnabled(True)
        
    def set_UI_status(self):
        #get DUT status
        self.DUT_instance.refresh()
        self.pretty_status = self.DUT_instance.pretty_status
        self.status = self.DUT_instance.status
        
        #set window title
        self.setWindowTitle(_translate("DUTWindow", "DUT IP: %s Name: %s Status: %s" % (self.ip, self.name, self.pretty_status), None))
        #set action status
        if self.status & 0b10000000:
            #Cannot control DUT
            self.actionRunTest.setDisabled(True)
            self.actionPauseStopTest.setDisabled(True)
        else:
            self.actionRunTest.setEnabled(True)
            self.actionPauseStopTest.setEnabled(True)
            
    def closeEvent(self, event):
        #need update parent's DUTWindow list when one DUTWindow close
        del self.parent.DUTWindows[self.ip]
    
class SettingsDialog(QtGui.QDialog, Ui_Settings):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        
        self.setupUi(self)
        
    def accept(self):
        STAFDir = str(self.STAFDir.text())
        STAFServer.update_settings(STAF_dir=STAFDir)
        print("Setting staf_dir to %s" % STAFDir)
        QtGui.QDialog.accept(self)

class AddDUTDialog(QtGui.QDialog, Ui_addDUT):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        
        self.setupUi(self)
    
    def accept(self):
        ip = str(self.DUTIP.text())
        name = str(self.DUTName.text())
        print("Add DUT ip: %s name: %s" % (ip, name))
        STAFServer.add_DUT(ip, name)
        QtGui.QDialog.accept(self)
        
class MainWindow(QtGui.QMainWindow, Ui_XSTAFMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        
        #view
        self.setupUi(self)
        
        #model
        self.DUTsModel = QtGui.QStandardItemModel()
        self.DUTView.setModel(self.DUTsModel)
        
        #signals and slots
        self.connect(self.actionSettings, QtCore.SIGNAL("triggered(bool)"), self.settings)
        self.connect(self.actionCheckAndStartSTAF, QtCore.SIGNAL("triggered(bool)"), self.check_and_start_STAF)
        self.connect(self.actionRefresh, QtCore.SIGNAL("triggered(bool)"), self.refresh)
        self.connect(self.actionAddDUT, QtCore.SIGNAL("triggered(bool)"), self.add_DUT)
        self.connect(self.actionRemoveDUT, QtCore.SIGNAL("triggered(bool)"), self.remove_DUT)
        
        self.connect(self.DUTView, QtCore.SIGNAL("clicked(QModelIndex)"), self.DUT_clicked)
        self.connect(self.DUTView, QtCore.SIGNAL("doubleClicked(QModelIndex)"), self.DUT_double_clicked)
        
        #init some status
        self.actionRefresh.setDisabled(True)
        self.actionAddDUT.setDisabled(True)
        self.actionRemoveDUT.setDisabled(True)
        
        #DUTWindow list
        self.DUTWindows = {}
        
        
    def settings(self):
        settingsDialog = SettingsDialog()
        settingsDialog.exec_()
        
    def check_and_start_STAF(self):
        STAFServer.check_and_start_staf()

        self.actionRefresh.setEnabled(True)
        self.actionAddDUT.setEnabled(True)
        self.actionRemoveDUT.setEnabled(True)
        
    def refresh(self):
        #
        self.DUTsModel.clear()
        self.DUTsModel.setHorizontalHeaderItem(0, QtGui.QStandardItem(QtCore.QString("Name")))
        self.DUTsModel.setHorizontalHeaderItem(1, QtGui.QStandardItem(QtCore.QString("IP")))
        self.DUTsModel.setHorizontalHeaderItem(2, QtGui.QStandardItem(QtCore.QString("Status")))
        for DUT in STAFServer.DUTs.items():
            DUT_instance = DUT[1]
            DUT_instance.refresh()
            IP = QtGui.QStandardItem(QtCore.QString("%0").arg(DUT_instance.ip))
            name = QtGui.QStandardItem(QtCore.QString("%0").arg(DUT_instance.name))
            status = QtGui.QStandardItem(QtCore.QString("%0").arg(DUT_instance.pretty_status))
            self.DUTsModel.appendRow([name, IP, status])
        
    def add_DUT(self):
        addDUTDialog = AddDUTDialog()
        addDUTDialog.exec_()
        self.refresh()
        
    def remove_DUT(self):
        for selectedIndex in self.DUTView.selectedIndexes():
            DUT_IP = str(self.DUTsModel.itemFromIndex(self.DUTsModel.index(selectedIndex.row(), 1)).text())
            if STAFServer.has_DUT(DUT_IP):
                STAFServer.remove_DUT(DUT_IP)
        self.refresh()
        
    def DUT_clicked(self, index):
        print("Click: column: %s, raw: %s" % (index.column(), index.row()))
        DUT_IP = self.DUTsModel.itemFromIndex(self.DUTsModel.index(index.row(), 1)).text()
        DUT_name = self.DUTsModel.itemFromIndex(self.DUTsModel.index(index.row(), 0)).text()
        self.infoEdit.clear()
        self.infoEdit.append((QtCore.QString("DUT IP: %0 name: %1").arg(DUT_IP).arg(DUT_name)))
        
    def DUT_double_clicked(self, index):
        print("Double Click: column: %s, raw: %s" % (index.column(), index.row()))
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
            DUT_instance.stop_task_runner()
        
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())