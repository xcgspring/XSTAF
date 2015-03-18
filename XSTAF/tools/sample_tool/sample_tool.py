
from XSTAF.core.logger import LOGGER
from PyQt4 import QtCore, QtGui
from ui.ui_sampleDialog import Ui_SampleDialog
import ui.resources_rc

class Tool(object):
    _description = "Sample Tool"
    main_window = None
    
    @classmethod
    def set_main_window(cls, main_window):
        cls.main_window = main_window
    
    @staticmethod
    def icon():
        tool_icon = QtGui.QIcon()
        tool_icon.addPixmap(QtGui.QPixmap(":icons/icons/sample.png"))
        return tool_icon
    
    @classmethod
    def launch(cls):
        LOGGER.info("Launch sample tool")
        tool_dialog = SampleTool(cls.main_window)
        tool_dialog.exec_()
        
    @classmethod
    def description(cls):
        return cls._description
    
class SampleTool(QtGui.QDialog, Ui_SampleDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)