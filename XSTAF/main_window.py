
import os
from PyQt4 import QtCore, QtGui

from ui.ui_mainWindow import Ui_XSTAFMainWindow
import logger
import dialogs
from DUT_window import DUTWindow

class MainWindow(QtGui.QMainWindow, Ui_XSTAFMainWindow):

    def __init__(self, server_instance):
        QtGui.QMainWindow.__init__(self)

        #view
        self.setupUi(self)

        #model
        self.server = server_instance
        self.DUTsModel = QtGui.QStandardItemModel(self.DUTView)
        self.DUTView.setModel(self.DUTsModel)

        #config logger with default configuration
        logger.LOGGER.config()

        ##########################################
        #signals and slots

        #connect logger signal to mainWindow slot
        self.connect(logger.LOGGER, logger.LOGGER.updateLog, self.update_log)

        #signals and slots for actions
        self.connect(self.actionNewWorkSpace, QtCore.SIGNAL("triggered(bool)"), self.new_workspace)
        self.connect(self.actionOpenWorkSpace, QtCore.SIGNAL("triggered(bool)"), self.open_workspace)
        self.connect(self.actionSaveWorkSpace, QtCore.SIGNAL("triggered(bool)"), self.save_workspace)

        self.connect(self.actionSettings, QtCore.SIGNAL("triggered(bool)"), self.settings)
        self.connect(self.actionStartSTAF, QtCore.SIGNAL("triggered(bool)"), self.start_STAF)
        self.connect(self.actionRefresh, QtCore.SIGNAL("triggered(bool)"), self.refresh)
        self.connect(self.actionAddDUT, QtCore.SIGNAL("triggered(bool)"), self.add_DUT)
        self.connect(self.actionRemoveDUT, QtCore.SIGNAL("triggered(bool)"), self.remove_DUT)
        self.connect(self.actionOpenDUTView, QtCore.SIGNAL("triggered(bool)"), self.open_DUT_view)

        #signals and slots for DUT view
        self.connect(self.DUTView, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.DUT_view_right_clicked)
        self.connect(self.DUTView, QtCore.SIGNAL("doubleClicked(QModelIndex)"), self.DUT_view_double_clicked)

        #when staf status changes, we should handle it
        self.connect(self.server, self.server.staf_status_change, self.handle_staf_status_change)
        ##########################################

        #staf
        self.staf_status = 0b10000000 #StatusUnKnown
        self.server.config_staf()

        #DUTWindow list for managing DUT window
        self.DUTWindows = {}

        #refresh ui
        self.refresh_ui()

    def settings(self):
        settings_dialog = dialogs.SettingsDialog(self)
        settings_dialog.exec_()

    def handle_staf_status_change(self, staf_status):
        '''
        handle staf status change signal
        '''
        logger.LOGGER.debug("Handle STAF status change")
        if not staf_status:
            #left start STAF button enabled, in case STAF stops unexpected
            self.actionStartSTAF.setEnabled(True)
        elif staf_status & 0b01000000:
            #enable start STAF button, user can start local STAF process manually
            self.actionStartSTAF.setEnabled(True)
        elif staf_status & 0b10000000:
            #disable start STAF button, user cannot start STAF process since STAF is not configured right
            self.actionStartSTAF.setDisabled(True)

        if not staf_status:
            #add monitors for all DUTs in workspace, runner should be added when DUT status is OK
            if self.server.has_workspace():
                workspace = self.server.get_workspace()
                for dut_instance in workspace.duts():
                    dut_instance.add_monitor()
        elif staf_status & 0b11000000:
            #remove monitors and runners for all DUTs in workspace
            if self.server.has_workspace():
                workspace = self.server.get_workspace()
                for dut_instance in workspace.duts():
                    dut_instance.remove_runner()
                    dut_instance.remove_monitor()

        self.staf_status = staf_status
        self.refresh_ui()

    def start_STAF(self):
        self.server.start_staf()

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

    def check_unsaved_workspace(self):
        if self.server.is_default_workspace_exist():
            #ask user if load exist workspace or create a new one
            load_default = dialogs.ConfirmDialog.confirm(self, "Detect unsaved workspace, load it or not?")
            if load_default:
                self.server.add_workspace()
                workspace = self.server.get_workspace()
                workspace.load(workspace.DefaultWorkspacePath)
                self.refresh_ui()

    def new_workspace(self):
        #ask user if save workspace before open new workspace
        if self.server.has_workspace():
            save_current = dialogs.ConfirmDialog.confirm(self, "Save current workspace before create new one?")
            if save_current:
                self.save_workspace()

        self.server.add_workspace()
        self.refresh_ui()

    def open_workspace(self):
        #ask user if save workspace before open new workspace
        if self.server.has_workspace():
            save_current = dialogs.ConfirmDialog.confirm(self, "Save current workspace before opening new one?")
            if save_current:
                self.save_workspace()

        workspace_path = str(QtGui.QFileDialog.getExistingDirectory(self, "Open WorkSpace"))
        if os.path.isdir(workspace_path):
            self.server.add_workspace()
            workspace = self.server.get_workspace()
            workspace.load(workspace_path)
            self.refresh_ui()

    def save_workspace(self):
        if not self.server.has_workspace():
            return

        workspace = self.server.get_workspace()
        if workspace.is_current_default():
            workspace_path = str(QtGui.QFileDialog.getExistingDirectory(self, "Save WorkSpace"))
            workspace.save(workspace_path)
        else:
            workspace.save(workspace.workspace_path)

    def refresh(self):
        refresh_dialog = dialogs.RefreshAllDialog(self)
        refresh_dialog.exec_()

    def refresh_ui(self):
        if self.server.has_workspace():
            self.actionSaveWorkSpace.setEnabled(True)
            self.actionAddDUT.setEnabled(True)
            self.actionRemoveDUT.setEnabled(True)
            if self.staf_status & 0b10000000:
                self.actionRefresh.setDisabled(True)
            else:
                self.actionRefresh.setEnabled(True)

            self.DUTsModel.clear()
            self.DUTsModel.setHorizontalHeaderItem(0, QtGui.QStandardItem(QtCore.QString("Name")))
            self.DUTsModel.setHorizontalHeaderItem(1, QtGui.QStandardItem(QtCore.QString("IP")))
            self.DUTsModel.setHorizontalHeaderItem(2, QtGui.QStandardItem(QtCore.QString("Status")))
            for DUT_instance in self.server.get_workspace().duts():
                IP = QtGui.QStandardItem(QtCore.QString("%0").arg(DUT_instance.ip))
                name = QtGui.QStandardItem(QtCore.QString("%0").arg(DUT_instance.name))
                status = QtGui.QStandardItem(QtCore.QString("%0").arg(DUT_instance.pretty_status))
                self.DUTsModel.appendRow([name, IP, status])
        else:
            self.actionSaveWorkSpace.setDisabled(True)
            self.actionAddDUT.setDisabled(True)
            self.actionRemoveDUT.setDisabled(True)
            self.actionRefresh.setDisabled(True)
            self.DUTsModel.clear()

    def add_DUT(self):
        if not self.server.has_workspace():
            return

        addDUTDialog = dialogs.AddDUTDialog(self)
        addDUTDialog.exec_()
        self.refresh_ui()

    def remove_DUT(self):
        if not self.server.has_workspace():
            return

        workspace = self.server.get_workspace()
        for selectedIndex in self.DUTView.selectedIndexes():
            dut_ip = str(self.DUTsModel.itemFromIndex(self.DUTsModel.index(selectedIndex.row(), 1)).text())
            if workspace.has_dut(dut_ip):
                workspace.remove_dut(dut_ip)
        self.refresh_ui()

    def open_DUT_view(self):
        for selected_index in self.DUTView.selectedIndexes():
            dut_ip = str(self.DUTsModel.itemFromIndex(self.DUTsModel.index(selected_index.row(), 1)).text())
            if dut_ip not in self.DUTWindows:
                dut_window = DUTWindow(self, dut_ip)
                self.DUTWindows[dut_ip] = dut_window
                dut_window.show()
            else:
                dut_window = self.DUTWindows[dut_ip]
                dut_window.setFocus()

    def DUT_view_right_clicked(self, point):
        context_menu = QtGui.QMenu()
        index = self.DUTView.indexAt(point)
        item = self.DUTsModel.itemFromIndex(index)
        if item is None:
            return
        else:
            context_menu.addAction(self.actionOpenDUTView)
            context_menu.addAction(self.actionRemoveDUT)
            context_menu.exec_(self.DUTView.mapToGlobal(point))

    def DUT_view_double_clicked(self, index):
        logger.LOGGER.debug("Double Click: column: %s, raw: %s", index.column(), index.row())
        self.open_DUT_view()

    def closeEvent(self, event):
        if self.server.has_workspace():
            workspace = self.server.get_workspace()
            #stop DUT threads
            for dut_instance in workspace.duts():
                dut_instance.remove_runner()

            #check if need save workspace
            save_current = dialogs.ConfirmDialog.confirm(self, "Save current workspace before close?")
            if save_current:
                self.save_workspace()

            #delete tmp workspace
            workspace.clean_default()
