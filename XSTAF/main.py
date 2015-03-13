
import sys
from PyQt4 import QtGui

import logger
from server import Server
from main_window import MainWindow

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    server = Server()
    mainWin = MainWindow(server)
    mainWin.show()
    mainWin.check_unsaved_workspace()
    sys.exit(app.exec_())
