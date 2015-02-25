
from PyQt4 import QtCore, QtGui
from ui.ui_mainWindow import Ui_XSTAFMainWindow
from ui.ui_settingsDialog import Ui_Settings

class SettingsDialog(QtGui.QDialog, Ui_Settings):
    def __init__(self, server):
        QtGui.QDialog.__init__(self)
        
        self.setupUi(self)
        self.server = server
        
    def accept(self):
        self.server.staf_dir = self.STAFDir.text()
        print("Setting staf_dir to %s" % self.server.staf_dir)
        QtGui.QDialog.accept(self)

class MainWindow(QtGui.QMainWindow, Ui_XSTAFMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        
        #view
        self.setupUi(self)
        
        #model
        from server import Server
        self.server = Server()
        
        #Slots
        self.connect(self.actionSettings, QtCore.SIGNAL("triggered(bool)"), self.settings)
        
    def settings(self):
        settingsDialog = SettingsDialog(self.server)
        settingsDialog.exec_()
        

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())