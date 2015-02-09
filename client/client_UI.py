
from PyQt4 import QtCore, QtGui
from ui.client_ui import Ui_XSTAFClient

class ClientWindow(QtGui.QMainWindow):
    def __init__(self):
        super(ClientWindow, self).__init__()
        
        self.ui = Ui_XSTAFClient()
        self.ui.setupUi(self)
        
if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    mainWin = ClientWindow()
    mainWin.show()
    sys.exit(app.exec_())