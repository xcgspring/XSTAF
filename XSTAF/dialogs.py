
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
    def __init__(self, ip, server):
        QtCore.QThread.__init__(self)
        self.ip = ip
        self.server = server

    def run(self):
        DUT_instance = self.server.get_DUT(self.ip)
        self.emit(QtCore.SIGNAL("notify_status"), "Refreshing DUT: %s..." % DUT_instance.ip)
        #refresh DUT, will check DUT status, time cost
        DUT_instance.refresh()

        time.sleep(0.1)
        self.emit(QtCore.SIGNAL("notify_stop"))

class RefreshDUTDialog(QtGui.QDialog, Ui_refreshDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)

        self.parent = parent
        self.progressBar.setRange(0, 0)
        self.refresh_thread = RefreshDUTThread(parent.ip, parent.server)

        #signal and slot
        self.connect(self.refresh_thread, QtCore.SIGNAL("notify_status"), self.update_status)
        self.connect(self.refresh_thread, QtCore.SIGNAL("notify_stop"), self.accept)

        self.refresh_thread.start()

    def update_status(self, status):
        self.statusLabel.setText(status)

    def accept(self):
        self.parent.refresh_without_checking_status()
        QtGui.QDialog.accept(self)

class SettingsDialog(QtGui.QDialog, Ui_Settings):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)

        self.setupUi(self)
        self.parent = parent
        self.server = parent.server

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
        staf_status = self.server.config_staf()
        if not staf_status:
            self.parent.staf_ready = True
            #emit staf ready signal to update DUT ui
            self.parent.emit(self.parent.STAFReady)
            self.parent.actionStartSTAF.setEnabled(True)
            self.parent.actionRefresh.setEnabled(True)
        elif staf_status & 0b01000000:
            #not start
            self.parent.staf_ready = False
            self.parent.actionStartSTAF.setEnabled(True)
            self.parent.actionRefresh.setDisabled(True)
        elif staf_status & 0b10000000:
            self.parent.staf_ready = False
            self.parent.actionStartSTAF.setDisabled(True)
            self.parent.actionRefresh.setDisabled(True)

        logger.LOGGER.config(logging_file=str(self.loggingFileEdit.text()),\
                        logging_level_file=logger.level_name(str(self.loggingFileLevel.currentText())),\
                        logging_level_stream=logger.level_name(str(self.loggingStreamLevel.currentText())))

        logger.LOGGER.debug("Config staf dir: %s", STAFDir)
        logger.LOGGER.debug("Config logging_file: %s", str(self.loggingFileEdit.text()))
        logger.LOGGER.debug("Config logging_level_file: %s", str(self.loggingFileLevel.currentText()))
        logger.LOGGER.debug("Config logging_level_stream: %s", str(self.loggingStreamLevel.currentText()))

        QtGui.QDialog.accept(self)

class AddDUTDialog(QtGui.QDialog, Ui_addDUT):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.DUTIP.setInputMask("000.000.000.000")
        self.server = parent.server

    def accept(self):
        ip = str(self.DUTIP.text())
        name = str(self.DUTName.text())
        logger.LOGGER.debug("Add DUT ip: %s name: %s", ip, name)
        self.server.add_DUT(ip, name)
        QtGui.QDialog.accept(self)

class RefreshAllThread(QtCore.QThread):
    def __init__(self, server):
        QtCore.QThread.__init__(self)
        self.server = server

    def run(self):
        for DUT_instance in self.server.DUTs():
            self.emit(QtCore.SIGNAL("notify_status"), "Refreshing DUT: %s..." % DUT_instance.ip)
            #refresh DUT, will check DUT status, time cost
            DUT_instance.refresh()
            #this signal will update DUT view
            self.emit(QtCore.SIGNAL("notify_DUTsView"))

        time.sleep(0.1)
        self.emit(QtCore.SIGNAL("notify_stop"))

class RefreshAllDialog(QtGui.QDialog, Ui_refreshDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)

        self.parent = parent
        self.progressBar.setRange(0, 0)
        self.refresh_thread = RefreshAllThread(parent.server)

        #signal and slot
        self.connect(self.refresh_thread, QtCore.SIGNAL("notify_status"), self.update_status)
        self.connect(self.refresh_thread, QtCore.SIGNAL("notify_DUTsView"), self.update_DUTsView)
        self.connect(self.refresh_thread, QtCore.SIGNAL("notify_stop"), self.accept)

        self.refresh_thread.start()

    def update_status(self, status):
        self.statusLabel.setText(status)

    def update_DUTsView(self):
        self.parent.refresh_without_checking_status()
