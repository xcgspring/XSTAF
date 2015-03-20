
import time
from PyQt4 import QtCore, QtGui

from XSTAF.core.logger import LOGGER
from XSTAF.ui.ui_settingsDialog import Ui_Settings
from XSTAF.ui.ui_addDUT import Ui_addDUT
from XSTAF.ui.ui_refresh import Ui_refreshDialog
from XSTAF.ui.ui_confirmDialog import Ui_confirmDialog
from XSTAF.ui.ui_toolManager import Ui_toolManagerDialog
from XSTAF.ui.ui_changeDUT import Ui_changeDUT

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
        self.loggingFileEdit.setText(QtCore.QString("%0").arg(self.server.get_settings("LogLocation")))
        self.WorkspaceLocation.setText(QtCore.QString("%0").arg(self.server.get_settings("WorkspaceLocation")))
        self.toolLocationEdit.setText(QtCore.QString("%0").arg(self.server.get_settings("ToolsLocation")))
        self.toolConfigureFileEdit.setText(QtCore.QString("%0").arg(self.server.get_settings("ToolsConfigureFile")))
        self.dutLogLocationEdit.setText(QtCore.QString("%0").arg(self.server.get_settings("remote_log_location")))
        self.dutTmpFilesLocationEdit.setText(QtCore.QString("%0").arg(self.server.get_settings("remote_tmp_files_location")))
        
        logging_level_file = self.server.get_settings("LoggerLevelFile")
        logging_level_stream = self.server.get_settings("LoggerLevelStream")

        for level in ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]:
            self.loggingFileLevel.addItem(level)
            self.loggingStreamLevel.addItem(level)

        indexs = {"CRITICAL" : 0, "ERROR": 1, "WARNING": 2, "INFO": 3, "DEBUG": 4}
        self.loggingFileLevel.setCurrentIndex(indexs[logging_level_file])
        self.loggingStreamLevel.setCurrentIndex(indexs[logging_level_stream])

    def accept(self):
        logging_file = str(self.loggingFileEdit.text())
        logging_level_file=str(self.loggingFileLevel.currentText())
        logging_level_stream=str(self.loggingStreamLevel.currentText())
        staf_dir = str(self.STAFDirEdit.text())
        workspace_location = str(self.WorkspaceLocation.text())
        tool_location = str(self.toolLocationEdit.text())
        tool_config_file = str(self.toolConfigureFileEdit.text())
        dut_log_location = str(self.dutLogLocationEdit.text())
        dut_tmp_files_location = str(self.dutTmpFilesLocationEdit.text())
        
        self.server.apply_settings(STAFDir=staf_dir, \
                                    LogLocation=logging_file, \
                                    LoggerLevelFile=logging_level_file, \
                                    LoggerLevelStream=logging_level_stream, \
                                    WorkspaceLocation=workspace_location, \
                                    ToolsLocation=tool_location, \
                                    ToolsConfigureFile=tool_config_file, \
                                    remote_log_location=dut_log_location, \
                                    remote_tmp_files_location=dut_tmp_files_location)
        self.server.config()

        LOGGER.debug("Config logging_file: %s", logging_file)
        LOGGER.debug("Config logging_level_file: %s", logging_level_file)
        LOGGER.debug("Config logging_level_stream: %s", logging_level_stream)
        LOGGER.debug("Config staf dir: %s", staf_dir)
        LOGGER.debug("Config workspace dir: %s", workspace_location)
        LOGGER.debug("Config tool location: %s", tool_location)
        LOGGER.debug("Config tool config file: %s", tool_config_file)
        LOGGER.debug("Config dut log location: %s", remote_log_location)
        LOGGER.debug("Config dut tmp files location: %s", remote_tmp_files_location)
        
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
            LOGGER.debug("Add DUT ip: %s name: %s", ip, name)
            workspace = self.server.get_workspace()
            workspace.add_dut(ip, name)
        else:
            LOGGER.debug("No workspace, cannot add DUT")
        QtGui.QDialog.accept(self)
        
class ChangeDUTInfoDialog(QtGui.QDialog, Ui_changeDUT):
    def __init__(self, main_window, orginal_ip):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.DUTIP.setInputMask("000.000.000.000")
        self.server = main_window.server
        self.orginal_ip = orginal_ip
        self.orginalDUTInfo.setText(QtCore.QString("Change DUT info for DUT %0").arg(self.orginal_ip))

    def accept(self):
        changed_ip = str(self.DUTIP.text())
        changed_name = str(self.DUTName.text())

        LOGGER.debug("Change DUT info")
        workspace = self.server.get_workspace()
        workspace.change_dut_info(self.orginal_ip, changed_ip, changed_name)

        QtGui.QDialog.accept(self)

class RefreshAllThread(QtCore.QThread):
    def __init__(self, server):
        QtCore.QThread.__init__(self)
        self.server = server

    def run(self):
        self.server.check_staf()
        
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

class ToolManagerDialog(QtGui.QDialog, Ui_toolManagerDialog):
    def __init__(self, main_window):
        QtGui.QDialog.__init__(self, main_window)
        self.setupUi(self)
        self.parent = main_window
        self.server = main_window.server
        
        #signal and slot
        self.connect(self.downButton, QtCore.SIGNAL("clicked(bool)"), self.remove_tool)
        self.connect(self.upButton, QtCore.SIGNAL("clicked(bool)"), self.add_tool)
        #tool list view
        self.loaded_tools_model = QtGui.QStandardItemModel(self.loadedToolsListView)
        self.loadedToolsListView.setModel(self.loaded_tools_model)
        
        self.avaliable_tools_model = QtGui.QStandardItemModel(self.avaliableToolsListView)
        self.avaliableToolsListView.setModel(self.avaliable_tools_model)
        
        #self.downButton.setDisabled(True)
        #self.upButton.setDisabled(True)
        
        self._refresh_tool_view()
        
    def _refresh_tool_view(self):
        self.loaded_tools_model.clear()
        for tool_name, tool in self.server.loaded_tools():
            tool_item = QtGui.QStandardItem(tool.icon(), QtCore.QString("%s" % tool_name))
            self.loaded_tools_model.appendRow(tool_item)
            
        self.avaliable_tools_model.clear()
        for tool_name, tool in self.server.available_tools():
            tool_item = QtGui.QStandardItem(tool.icon(), QtCore.QString("%s" % tool_name))
            self.avaliable_tools_model.appendRow(tool_item)
        
    def add_tool(self):
        for selected_index in self.avaliableToolsListView.selectedIndexes():
            tool_item = self.avaliable_tools_model.itemFromIndex(selected_index)
            tool_name = str(tool_item.text())
            self.server.add_tool(tool_name)
        self._refresh_tool_view()
        
    def remove_tool(self):
        for selected_index in self.loadedToolsListView.selectedIndexes():
            tool_item = self.loaded_tools_model.itemFromIndex(selected_index)
            tool_name = str(tool_item.text())
            self.server.remove_tool(tool_name)
        self._refresh_tool_view()