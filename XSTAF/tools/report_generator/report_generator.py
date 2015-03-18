from XSTAF.core.logger import LOGGER
from PyQt4 import QtCore, QtGui
from ui.ui_reportGenerator import Ui_TestReportDialog
import ui.resources_rc

class Tool(object):
    _description = "Report Generator"
    main_window = None
    
    @classmethod
    def set_main_window(cls, main_window):
        cls.main_window = main_window
    
    @staticmethod
    def icon():
        tool_icon = QtGui.QIcon()
        tool_icon.addPixmap(QtGui.QPixmap(":icons/icons/report_generate.png"))
        return tool_icon
    
    @classmethod
    def launch(cls):
        LOGGER.info("Launch report generator tool")
        tool_dialog = ReportGenerator(cls.main_window)
        tool_dialog.exec_()
        
    @classmethod
    def description(cls):
        return cls._description
    
class _Data(object):
    '''
    extract information from workspace
    '''
    def __init__(self, workspace):
        pass
    
    def config(self, **kwargs):
        pass
    
    def duts(self):
        pass
        
    def testsuites(self):
        pass
    
    
class ReportGenerator(QtGui.QDialog, Ui_TestReportDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        
        self.server = parent.server
        
        self.generateEachRadioButton.toggle()
        self.passFirstRadioButton.toggle()
        self.htmlCheckBox.toggle()
        self.excelCheckBox.setDisabled(True)
        
        self.connect(self.searchToolButton, QtCore.SIGNAL("clicked(bool)"), self.get_report_location)
        
        self.workspace = self.server.get_workspace()
        if self.workspace is None:
            LOGGER.warning("Current no workspace loaded, could not generate report")
    
    def get_report_location(self):
        if not self.workspace is None:
            report_path = QtGui.QFileDialog.getExistingDirectory(self, "Get report location", self.workspace.workspace_path)
            self.reportLineEdit.setText(report_path)
    
    def accept(self):
        if not self.workspace is None:
            pass
        QtGui.QDialog.accept(self)