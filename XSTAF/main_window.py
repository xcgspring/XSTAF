
import os
from PyQt4 import QtCore, QtGui

from ui.ui_mainWindow import Ui_XSTAFMainWindow
import logger
import dialogs
from DUT_window import DUTWindow

class MainWindow(QtGui.QMainWindow, Ui_XSTAFMainWindow):
    #STAF ready signal
    STAFReady = QtCore.SIGNAL("STAFReady")

    def __init__(self, server_instance):
        QtGui.QMainWindow.__init__(self)

        #view
        self.setupUi(self)

        #model
        self.server = server_instance
        self.DUTsModel = QtGui.QStandardItemModel(self.DUTView)
        self.DUTView.setModel(self.DUTsModel)

        #signals and slots
        self.connect(self.actionNewWorkSpace, QtCore.SIGNAL("triggered(bool)"), self.new_work_space)
        self.connect(self.actionOpenWorkSpace, QtCore.SIGNAL("triggered(bool)"), self.open_work_space)
        self.connect(self.actionSaveWorkSpace, QtCore.SIGNAL("triggered(bool)"), self.save_work_space)

        self.connect(self.actionSettings, QtCore.SIGNAL("triggered(bool)"), self.settings)
        self.connect(self.actionStartSTAF, QtCore.SIGNAL("triggered(bool)"), self.start_STAF)
        self.connect(self.actionRefresh, QtCore.SIGNAL("triggered(bool)"), self.refresh)
        self.connect(self.actionAddDUT, QtCore.SIGNAL("triggered(bool)"), self.add_DUT)
        self.connect(self.actionRemoveDUT, QtCore.SIGNAL("triggered(bool)"), self.remove_DUT)

        #self.connect(self.DUTView, QtCore.SIGNAL("clicked(QModelIndex)"), self.DUT_clicked)
        self.connect(self.DUTView, QtCore.SIGNAL("doubleClicked(QModelIndex)"), self.DUT_double_clicked)

        #flags
        self.staf_ready = False
        self.has_workspace = False

        #connect logger signal to mainWindow slot
        self.connect(logger.LOGGER, logger.LOGGER.updateLog, self.update_log)
        #config logger with default configuration
        logger.LOGGER.config()

        #init staf
        staf_status = self.server.config_staf()
        if staf_status & 0b10000000:
            self.actionStartSTAF.setDisabled(True)
            self.actionRefresh.setDisabled(True)
            self.staf_ready = False
        elif staf_status & 0b01000000:
            self.staf_ready = False
            self.actionStartSTAF.setEnabled(True)
            self.actionRefresh.setDisabled(True)
        elif not staf_status:
            self.staf_ready = True
            self.actionStartSTAF.setEnabled(True)
            self.actionRefresh.setEnabled(True)

        #init some status
        self.actionSaveWorkSpace.setDisabled(True)
        self.actionAddDUT.setDisabled(True)
        self.actionRemoveDUT.setDisabled(True)

        #DUTWindow list
        self.DUTWindows = {}

    def settings(self):
        settings_dialog = dialogs.SettingsDialog(self)
        settings_dialog.exec_()

    def start_STAF(self):
        staf_status = self.server.start_staf()
        if not staf_status:
            self.staf_ready = True
            #emit staf ready signal to update DUT ui
            self.emit(self.STAFReady)
            self.actionStartSTAF.setEnabled(True)
            self.actionRefresh.setEnabled(True)
        elif staf_status & 0b01000000:
            #not start
            self.staf_ready = False
            self.actionStartSTAF.setEnabled(True)
            self.actionRefresh.setDisabled(True)
        elif staf_status & 0b10000000:
            self.staf_ready = False
            self.actionStartSTAF.setDisabled(True)
            self.actionRefresh.setDisabled(True)

    def update_log(self, record):
        levelno = record.levelno
        if levelno >= logger.level_name("CRITICAL"):
            color_str = '<div style="color:red">%s</div>' # red
        elif levelno >= logger.level_name("ERROR"):
            color_str = '<div style="color:red">%s</div>' # red
        elif levelno >= logger.level_name("WARN"):
            color_str = '<div style="color:orange">%s</div>' # orange
        elif levelno >= logger.level_name("INFO"):
            color_str = '<div style="color:black">%s</div>' # black
        elif levelno >= logger.level_name("DEBUG"):
            color_str = '<div style="color:gray">%s</div>' # gray
        else:
            color_str = '<div style="color:black">%s</div>' # black
        msg = color_str % ("[ %s ][ %s:%s ] %s" % (logger.level_name(levelno), record.filename, record.lineno, record.getMessage()))
        self.XSTAFLogEdit.append(msg)

    def check_unsaved_work_space(self):
        if self.server.is_default_workspace_exist():
            #ask user if load exist workspace or create a new one
            load_default = dialogs.ConfirmDialog.confirm(self, "Detect existing project, load it or not?")
            if load_default:
                self.server.load_workspace()
                self.refresh_without_checking_status()

    def new_work_space(self):
        #ask user if save workspace before open new workspace
        if not self.server.workspace is None:
            save_current = dialogs.ConfirmDialog.confirm(self, "Save current workspace before opening new one?")
            if save_current:
                self.save_work_space()

        self.server.new_workspace()
        self.has_workspace = True
        self.refresh_without_checking_status()

    def open_work_space(self):
        #ask user if save workspace before open new workspace
        if not self.server.workspace is None:
            save_current = dialogs.ConfirmDialog.confirm(self, "Save current workspace before opening new one?")
            if save_current:
                self.save_work_space()

        workspace_path = str(QtGui.QFileDialog.getExistingDirectory(self, "Open WorkSpace"))
        if os.path.isdir(workspace_path):
            self.server.load_workspace(workspace_path)
            self.has_workspace = True
            self.refresh_without_checking_status()

    def save_work_space(self):
        if self.server.is_current_workspace_default():
            workspace_path = str(QtGui.QFileDialog.getExistingDirectory(self, "Save WorkSpace"))
            self.server.save_workspace(workspace_path)
        else:
            self.server.save_workspace()

    def refresh(self):
        refresh_dialog = dialogs.RefreshAllDialog(self)
        refresh_dialog.exec_()

    def refresh_without_checking_status(self):
        self.DUTsModel.clear()
        self.DUTsModel.setHorizontalHeaderItem(0, QtGui.QStandardItem(QtCore.QString("Name")))
        self.DUTsModel.setHorizontalHeaderItem(1, QtGui.QStandardItem(QtCore.QString("IP")))
        self.DUTsModel.setHorizontalHeaderItem(2, QtGui.QStandardItem(QtCore.QString("Status")))
        for DUT_instance in self.server.DUTs():
            IP = QtGui.QStandardItem(QtCore.QString("%0").arg(DUT_instance.ip))
            name = QtGui.QStandardItem(QtCore.QString("%0").arg(DUT_instance.name))
            status = QtGui.QStandardItem(QtCore.QString("%0").arg(DUT_instance.pretty_status))
            self.DUTsModel.appendRow([name, IP, status])

        if self.has_workspace:
            #if we have workspace, we can enable follow action
            self.actionSaveWorkSpace.setEnabled(True)
            self.actionAddDUT.setEnabled(True)
            self.actionRemoveDUT.setEnabled(True)
        else:
            self.actionSaveWorkSpace.setDisabled(True)
            self.actionAddDUT.setDisabled(True)
            self.actionRemoveDUT.setDisabled(True)

        if self.staf_ready:
            #if staf start, we can enable follow action
            self.actionRefresh.setEnabled(True)
        else:
            self.actionRefresh.setDisabled(True)

    def add_DUT(self):
        addDUTDialog = dialogs.AddDUTDialog(self)
        addDUTDialog.exec_()
        self.refresh_without_checking_status()

    def remove_DUT(self):
        for selectedIndex in self.DUTView.selectedIndexes():
            DUT_IP = str(self.DUTsModel.itemFromIndex(self.DUTsModel.index(selectedIndex.row(), 1)).text())
            if self.server.has_DUT(DUT_IP):
                self.server.remove_DUT(DUT_IP)
        self.refresh_without_checking_status()

#    '''
#    def DUT_clicked(self, index):
#        logger.LOGGER.debug("Click: column: %s, raw: %s" % (index.column(), index.row()))
#        DUT_IP = self.DUTsModel.itemFromIndex(self.DUTsModel.index(index.row(), 1)).text()
#        DUT_name = self.DUTsModel.itemFromIndex(self.DUTsModel.index(index.row(), 0)).text()
#        self.infoEdit.clear()
#        self.infoEdit.append(QtCore.QString("DUT IP: %0 name: %1").arg(DUT_IP).arg(DUT_name))
#    '''

    def DUT_double_clicked(self, index):
        logger.LOGGER.debug("Double Click: column: %s, raw: %s", index.column(), index.row())
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
        for DUT_instance in self.server.DUTs():
            DUT_instance.pause_task_runner()

        #check if need save workspace
        if not self.server.workspace is None:
            save_current = dialogs.ConfirmDialog.confirm(self, "Save current workspace before close?")
            if save_current:
                self.save_work_space()

        #delete tmp workspace
        self.server.clean_default_workspace()
