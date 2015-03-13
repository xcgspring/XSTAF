
import time
from PyQt4 import QtCore, QtGui

import logger
from ui.ui_settingsDialog import Ui_Settings
from ui.ui_addDUT import Ui_addDUT
from ui.ui_refresh import Ui_refreshDialog
from ui.ui_confirmDialog import Ui_confirmDialog

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
    def __init__(self, dut_instance):
        QtCore.QThread.__init__(self)
        self.dut_instance = dut_instance

    def run(self):
        #check DUT status, time cost
        self.dut_instance.get_monitor_status()
        #emit stop signal to exit refresh dialog
        self.emit(QtCore.SIGNAL("notify_stop"))

class RefreshDUTDialog(QtGui.QDialog, Ui_refreshDialog):
    def __init__(self, dut_window):
        QtGui.QDialog.__init__(self, dut_window)
        self.setupUi(self)

        self.progressBar.setRange(0, 0)
        self.statusLabel.setText("Refreshing DUT: %s..." % dut_window.ip)
        self.refresh_thread = RefreshDUTThread(dut_window.dut)
        #signal and slot
        self.connect(self.refresh_thread, QtCore.SIGNAL("notify_stop"), self.accept)
        self.refresh_thread.start()

    def accept(self):
        QtGui.QDialog.accept(self)

class SettingsDialog(QtGui.QDialog, Ui_Settings):
    def __init__(self, main_window):
        QtGui.QDialog.__init__(self, main_window)

        self.setupUi(self)
        self.parent = main_window
        self.server = main_window.server

        #init the settings
        self.STAFDirEdit.setText(QtCore.QString("%0").arg(self.server.get_settings("STAFDir")))
        self.loggingFileEdit.setText(QtCore.QString("%0").arg(logger.LOGGER.configs["logging_file"]))

        indexs = {"CRITICAL": 0, \
                "ERROR": 1, \
                "WARNING": 2, \
                "INFO": 3, \
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
        self.server.apply_settings(STAFDir=STAFDir)
        self.server.config_staf()

        logger.LOGGER.config(logging_file=str(self.loggingFileEdit.text()),\
                        logging_level_file=logger.level_name(str(self.loggingFileLevel.currentText())),\
                        logging_level_stream=logger.level_name(str(self.loggingStreamLevel.currentText())))

        logger.LOGGER.debug("Config staf dir: %s", STAFDir)
        logger.LOGGER.debug("Config logging_file: %s", str(self.loggingFileEdit.text()))
        logger.LOGGER.debug("Config logging_level_file: %s", str(self.loggingFileLevel.currentText()))
        logger.LOGGER.debug("Config logging_level_stream: %s", str(self.loggingStreamLevel.currentText()))

        QtGui.QDialog.accept(self)

class AddDUTDialog(QtGui.QDialog, Ui_addDUT):
    def __init__(self, main_window):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.DUTIP.setInputMask("000.000.000.000")
        self.server = main_window.server

    def accept(self):
        ip = str(self.DUTIP.text())
        name = str(self.DUTName.text())

        if self.server.has_workspace():
            logger.LOGGER.debug("Add DUT ip: %s name: %s", ip, name)
            workspace = self.server.get_workspace()
            workspace.add_dut(ip, name)
        else:
            logger.LOGGER.debug("No workspace, cannot add DUT")
        QtGui.QDialog.accept(self)

class RefreshAllThread(QtCore.QThread):
    def __init__(self, server):
        QtCore.QThread.__init__(self)
        self.server = server

    def run(self):
        self.server.config_staf()
        
        if self.server.has_workspace():
            workspace = self.server.get_workspace()
            for dut in workspace.duts():
                self.emit(QtCore.SIGNAL("notify_status"), "Refreshing DUT: %s..." % dut.ip)
                #refresh DUT, will check DUT status, time cost
                dut.get_monitor_status()
                #this signal will update DUT view
                self.emit(QtCore.SIGNAL("notify_DUTsView"))

        time.sleep(0.1)
        self.emit(QtCore.SIGNAL("notify_stop"))

class RefreshAllDialog(QtGui.QDialog, Ui_refreshDialog):
    def __init__(self, main_window):
        QtGui.QDialog.__init__(self, main_window)
        self.setupUi(self)

        self.parent = main_window
        self.progressBar.setRange(0, 0)
        self.refresh_thread = RefreshAllThread(main_window.server)

        #signal and slot
        self.connect(self.refresh_thread, QtCore.SIGNAL("notify_status"), self.update_status)
        self.connect(self.refresh_thread, QtCore.SIGNAL("notify_DUTsView"), self.update_DUTsView)
        self.connect(self.refresh_thread, QtCore.SIGNAL("notify_stop"), self.accept)

        self.refresh_thread.start()

    def update_status(self, status):
        self.statusLabel.setText(status)

    def update_DUTsView(self):
        self.parent.refresh_ui()
