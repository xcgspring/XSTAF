
from XSTAF.core.logger import LOGGER
from PyQt4 import QtCore, QtGui
from ui.ui_sampleDialog import Ui_SampleDialog, _fromUtf8
import ui.resources_rc

class Tool(object):
    _description = "Sample Tool"
    
    def __init__(self, main_window):
        self.main_window = main_window
    
    @staticmethod
    def icon():
        tool_icon = QtGui.QIcon()
        tool_icon.addPixmap(QtGui.QPixmap(_fromUtf8(":icons/icons/sample.png")))
        return tool_icon
        
    def launch(self):
        LOGGER.debug("Launch sample tool")
        tool_dialog = SampleTool(self.main_window)
        tool_dialog.exec_()
        
    @classmethod
    def description(cls):
        return cls._description
    
class SampleTool(QtGui.QDialog, Ui_SampleDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)