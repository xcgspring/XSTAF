import os
import traceback
from XSTAF.core.logger import LOGGER
from XSTAF.core.workspace import WorkSpace
from PyQt4 import QtCore, QtGui
from ui.ui_workspace_merger import Ui_workspaceMergerDialog
import ui.resources_rc

class Tool(object):
    _description = "workspace merger"
    main_window = None
    
    @classmethod
    def set_main_window(cls, main_window):
        cls.main_window = main_window
    
    @staticmethod
    def icon():
        tool_icon = QtGui.QIcon()
        tool_icon.addPixmap(QtGui.QPixmap(":icons/icons/merger.png"))
        return tool_icon
    
    @classmethod
    def launch(cls):
        try:
            LOGGER.info("Launch workspace merger")
            tool_dialog = WorkspaceMerger(cls.main_window)
            tool_dialog.exec_()
        except:
            LOGGER.error(traceback.format_exc())
        
    @classmethod
    def description(cls):
        return cls._description
    
class WorkspaceMerger(QtGui.QDialog, Ui_workspaceMergerDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        
        #input workspace list view model
        self.input_workspace_model = QtGui.QStandardItemModel(self.inputListView)
        self.inputListView.setModel(self.input_workspace_model)
        
        self.connect(self.addButton, QtCore.SIGNAL("clicked(bool)"), self.add_input_workspace)
        self.connect(self.removeButton, QtCore.SIGNAL("clicked(bool)"), self.remove_input_workspace)
        self.connect(self.inputToolButton, QtCore.SIGNAL("clicked(bool)"), self.get_input_workspace)
        self.connect(self.outputToolButton, QtCore.SIGNAL("clicked(bool)"), self.get_output_workspace)
        
        #workspace path to be merged
        self.workspace_paths = []
        
    def _refresh_workspace_list_view(self):
        self.input_workspace_model.clear()
        for workspace_path in self.workspace_paths:
            workspace_item = QtGui.QStandardItem(QtCore.QString("%0").arg(workspace_path))
            self.input_workspace_model.appendRow(workspace_item)
        
    def add_input_workspace(self):
        #just have a check if workspace exist
        workspace_path = str(self.inputLineEdit.text())
        if not os.path.isdir(workspace_path):
            LOGGER.info("Workspace path provided not exist: %s" % workspace_path)
            return
            
        self.workspace_paths.append(workspace_path)
        self._refresh_workspace_list_view()
        
    def remove_input_workspace(self):
        for selected_index in self.inputListView.selectedIndexes():
            workspace_item = self.input_workspace_model.itemFromIndex(selected_index)
            workspace_path = str(workspace_item.text())
            self.workspace_paths.remove(workspace_path)
        self._refresh_workspace_list_view()
        
    def get_input_workspace(self):
        workspace_path = QtGui.QFileDialog.getExistingDirectory(self, "Get input workspace")
        self.inputLineEdit.setText(workspace_path)
        
    def get_output_workspace(self):
        workspace_path = QtGui.QFileDialog.getExistingDirectory(self, "Get output workspace")
        self.outputLineEdit.setText(workspace_path)
        
    def accept(self):
        output_workspace_path = str(self.outputLineEdit.text())
        output_workspace = WorkSpace()
        output_workspace.new(output_workspace_path)
        for workspace_path in self.workspace_paths:
            workspace = WorkSpace()
            workspace.load(workspace_path)
            output_workspace.merge(workspace)
        output_workspace.save(output_workspace_path)

        QtGui.QDialog.accept(self)