
from PyQt4 import QtCore, QtGui
from ui.client_ui import Ui_XSTAFClient, _fromUtf8
from ui.settings_dialog_ui import Ui_settingsDialog


class SettingsDialog(QtGui.QDialog):
    def __init__(self, parent):
        super(SettingsDialog, self).__init__(parent)
        
        self.ui = Ui_settingsDialog()
        self.ui.setupUi(self)

class ClientWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(ClientWindow, self).__init__(parent)
        
        #add client window ui
        self.ui = Ui_XSTAFClient()
        self.ui.setupUi(self)
        
        #add settings dialog ui
        self.setting_dialog = SettingsDialog(self)
        
        #add more signals and slots
        self.connect(self.ui.actionSettings, QtCore.SIGNAL(_fromUtf8("triggered()")), self.set_settings)
        
        #settings
        self.staf_dir = r"c:\staf"
        self.staf_queue_depth = r"1000"
        
        #check staf exist
        
        
        #register self with staf lifecycle service
        
    def set_settings(self):
        '''
        '''
        self.setting_dialog.ui.STAFDir.setText(self.staf_dir)
        self.setting_dialog.ui.stafQueueDepth.setText(self.staf_queue_depth)
        self.setting_dialog.exec_()
        self.staf_dir = self.setting_dialog.ui.STAFDir.text()
        self.staf_queue_depth = self.setting_dialog.ui.stafQueueDepth.text()
        
    def check_staf(self):
        '''
        check if staf exist
        if exist
            return
        if not exist
            prompt a dialog warn user
            return
        '''
        
    def connect_staf(self):
        '''
        check if local staf process start
        if not
            start staf process
            
        create a staf handle to connect to staf process
        '''
    
    def register_self(self):
        '''
        register self to staf's life cycle service
        so every time staf process start, client is started
        '''
        
    def configure_staf(self):
        '''
        need to configure staf before run test
        '''
        
if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    mainWin = ClientWindow()
    mainWin.show()
    sys.exit(app.exec_())