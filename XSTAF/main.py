
from PyQt4 import QtCore, QtGui
from ui.ui_mainWindow import Ui_XSTAFMainWindow
from ui.ui_settingsDialog import Ui_Settings
from ui.ui_addDUT import Ui_addDUT

class SettingsDialog(QtGui.QDialog, Ui_Settings):
    def __init__(self, server):
        QtGui.QDialog.__init__(self)
        
        self.setupUi(self)
        self.server = server
        
    def accept(self):
        self.server.staf_dir = str(self.STAFDir.text())
        print("Setting staf_dir to %s" % self.server.staf_dir)
        QtGui.QDialog.accept(self)

class AddDUTDialog(QtGui.QDialog, Ui_addDUT):
    def __init__(self, server):
        QtGui.QDialog.__init__(self)
        
        self.setupUi(self)
        self.server = server
    
    def accept(self):
        ip = str(self.DUTIP.text())
        name = str(self.DUTName.text())
        print("Add DUT ip: %s name: %s" % (ip, name))
        self.server.add_DUT(ip, name)
        QtGui.QDialog.accept(self)
        
class MainWindow(QtGui.QMainWindow, Ui_XSTAFMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        
        #view
        self.setupUi(self)
        
        #model
        from server import Server
        self.server = Server()
        self.DUTsModel = QtGui.QStandardItemModel()
        self.DUTView.setModel(self.DUTsModel)
        
        #signals and slots
        self.connect(self.actionSettings, QtCore.SIGNAL("triggered(bool)"), self.settings)
        self.connect(self.actionRegisterHandle, QtCore.SIGNAL("triggered(bool)"), self.init_STAF)
        self.connect(self.actionRefresh, QtCore.SIGNAL("triggered(bool)"), self.refresh)
        self.connect(self.actionAddDUT, QtCore.SIGNAL("triggered(bool)"), self.add_DUT)
        self.connect(self.actionRemoveDUT, QtCore.SIGNAL("triggered(bool)"), self.remove_DUT)
        
        self.connect(self.DUTView, QtCore.SIGNAL("clicked(QModelIndex)"), self.DUT_clicked)
        self.connect(self.DUTView, QtCore.SIGNAL("doubleClicked(QModelIndex)"), self.DUT_double_clicked)
        
        #init some status
        self.actionRefresh.setDisabled(True)
        self.actionAddDUT.setDisabled(True)
        self.actionRemoveDUT.setDisabled(True)
        
    def settings(self):
        settingsDialog = SettingsDialog(self.server)
        settingsDialog.exec_()
        
    def init_STAF(self):
        self.server.init_STAF()
        self.actionRegisterHandle.setDisabled(True)
        self.actionRefresh.setEnabled(True)
        self.actionAddDUT.setEnabled(True)
        self.actionRemoveDUT.setEnabled(True)
        
    def refresh(self):
        #
        self.DUTsModel.clear()
        self.DUTsModel.setHorizontalHeaderItem(0, QtGui.QStandardItem(QtCore.QString("Name")))
        self.DUTsModel.setHorizontalHeaderItem(1, QtGui.QStandardItem(QtCore.QString("IP")))
        self.DUTsModel.setHorizontalHeaderItem(2, QtGui.QStandardItem(QtCore.QString("Status")))
        for DUT in self.server.DUTs.items():
            IP = QtGui.QStandardItem(QtCore.QString("%0").arg(DUT[0]))
            name = QtGui.QStandardItem(QtCore.QString("%0").arg(DUT[1][1].name))
            status = QtGui.QStandardItem(QtCore.QString("%0").arg("unknown"))
            self.DUTsModel.appendRow([name, IP, status])
        
    def add_DUT(self):
        addDUTDialog = AddDUTDialog(self.server)
        addDUTDialog.exec_()
        self.refresh()
        
    def remove_DUT(self):
        for selectedIndex in self.DUTView.selectedIndexes():
            DUT_IP = str(self.DUTsModel.itemFromIndex(self.DUTsModel.index(selectedIndex.row(), 1)).text())
            if self.server.has_DUT(DUT_IP):
                self.server.remove_DUT(DUT_IP)
        self.refresh()
        
    def DUT_clicked(self, index):
        print("Click: column: %s, raw: %s" % (index.column(), index.row()))
        DUT_IP = self.DUTsModel.itemFromIndex(self.DUTsModel.index(index.row(), 1)).text()
        DUT_name = self.DUTsModel.itemFromIndex(self.DUTsModel.index(index.row(), 0)).text()
        self.infoEdit.clear()
        self.infoEdit.append((QtCore.QString("DUT IP: %0 name: %1").arg(DUT_IP).arg(DUT_name)))
        
    def DUT_double_clicked(self, index):
        print("Double Click: column: %s, raw: %s" % (index.column(), index.row()))
        DUT_IP = self.DUTsModel.itemFromIndex(self.DUTsModel.index(index.row(), 1)).text()
        DUT_name = self.DUTsModel.itemFromIndex(self.DUTsModel.index(index.row(), 0)).text()
        print(DUT_IP)

    def closeEvent(self, event):
        #we need terminate all threads before close
        #stop DUT threads
        for DUT in self.server.DUTs.items():
            DUT_thread = DUT[1][1]
            DUT_thread.stop()
            DUT_thread.join()
        
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())