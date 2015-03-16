
import sys
from PyQt4 import QtGui

import XSTAF.core.logger
from XSTAF.core.server import Server
from XSTAF.core.main_window import MainWindow

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    server = Server()
    server.config()
    mainWin = MainWindow(server)
    mainWin.show()
    mainWin.check_unsaved_workspace()
    sys.exit(app.exec_())
