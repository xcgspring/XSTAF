import os
import traceback
from XSTAF.core.logger import LOGGER
from XSTAF.core.workspace import WorkSpace
from PyQt4 import QtCore, QtGui
from ui.ui_workspace_spliter import Ui_workspaceSpliterDialog
import ui.resources_rc

class Tool(object):
    _description = "workspace spliter"
    main_window = None
    
    @classmethod
    def set_main_window(cls, main_window):
        cls.main_window = main_window
    
    @staticmethod
    def icon():
        tool_icon = QtGui.QIcon()
        tool_icon.addPixmap(QtGui.QPixmap(":icons/icons/spliter.png"))
        return tool_icon
    
    @classmethod
    def launch(cls):
        try:
            LOGGER.info("Launch workspace spliter")
            tool_dialog = WorkspaceSpliter(cls.main_window)
            tool_dialog.exec_()
        except:
            LOGGER.error(traceback.format_exc())
        
    @classmethod
    def description(cls):
        return cls._description
    
class WorkspaceSpliter(QtGui.QDialog, Ui_workspaceSpliterDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        
        self.connect(self.inputToolButton, QtCore.SIGNAL("clicked(bool)"), self.get_input_workspace)
        self.connect(self.outputToolButton, QtCore.SIGNAL("clicked(bool)"), self.get_output_workspace)
        
    def get_input_workspace(self):
        workspace_path = QtGui.QFileDialog.getExistingDirectory(self, "Get input workspace")
        self.inputLineEdit.setText(workspace_path)
        
    def get_output_workspace(self):
        workspace_path = QtGui.QFileDialog.getExistingDirectory(self, "Get output workspace")
        self.outputLineEdit.setText(workspace_path)
        
    def accept(self):
        input_workspace_path = str(self.inputLineEdit.text())
        output_workspace_path = str(self.outputLineEdit.text())
        input_workspace = WorkSpace()
        input_workspace.load(input_workspace_path)
        input_workspace.split(output_workspace_path)
        
        QtGui.QDialog.accept(self)