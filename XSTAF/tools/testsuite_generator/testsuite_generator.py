
import os
import uuid
import time
import traceback
import xml.etree.ElementTree as ET
from PyQt4 import QtCore, QtGui

from XSTAF.core.logger import LOGGER
from ui.ui_testsuite_generator import Ui_TestSuiteDialog
import ui.resources_rc

class Tool(object):
    _description = "testsuite generator"
    main_window = None
    
    @classmethod
    def set_main_window(cls, main_window):
        cls.main_window = main_window
    
    @staticmethod
    def icon():
        tool_icon = QtGui.QIcon()
        tool_icon.addPixmap(QtGui.QPixmap(":icons/icons/generator.png"))
        return tool_icon
    
    @classmethod
    def launch(cls):
        try:
            LOGGER.info("Launch testsuite generator tool")
            tool_dialog = TestsuiteGenerator(cls.main_window)
            tool_dialog.exec_()
        except:
            LOGGER.error(traceback.format_exc())
        
    @classmethod
    def description(cls):
        return cls._description
    
class TestsuiteGenerator(QtGui.QDialog, Ui_TestSuiteDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        
        self.pyanvilRadioButton.toggle()
        self.connect(self.inputToolButton, QtCore.SIGNAL("clicked(bool)"), self.get_input_file)
        self.connect(self.outputToolButton, QtCore.SIGNAL("clicked(bool)"), self.get_output_location)
        
    def get_input_file(self):
        input_file = QtGui.QFileDialog.getOpenFileName(self, "Input file")
        self.inputLineEdit.setText(input_file)
        
    def get_output_location(self):
        output_path = QtGui.QFileDialog.getExistingDirectory(self, "Output location")
        self.outputLineEdit.setText(output_path)
    
    def accept(self):
        input_file = str(self.inputLineEdit.text())
        output_path = str(self.outputLineEdit.text())
        
        if self.pyanvilRadioButton.isChecked():
            parser = PyAnvilParser(input_file)
            parser.generate(output_path)
        else:
            parser = CSVParser(input_file)
            parser.generate(output_path)
        
        QtGui.QDialog.accept(self)
        
#function to format XML
def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
        
class CSVParser(object):
    '''
    csv format requried:
    "name,command,auto,timeout,description,data"
    '''
    def __init__(self, input_file):
        self.input_file = input_file
        
    def generate(self, output_path):
        input_file_basename = os.path.basename(self.input_file).split(".")[0]
        output_file = os.path.join(output_path, input_file_basename+"_generated.xml")
        
        root_element = ET.Element("TestSuite")
        testcases_element = ET.SubElement(root_element, "TestCases")
        with open(self.input_file, 'r') as in_f:
            for line in in_f:
                values = line.split(",")
                if len(values) < 6:
                    values += ("", )*(6-len(values))
                elif len(values) > 6:
                    values = values[0:6]
                name, command, auto, timeout, description, data = values
                
                testcase_element = ET.SubElement(testcases_element, "TestCase")
                id_element = ET.SubElement(testcase_element, "ID")
                id_element.text = str(uuid.uuid1())
                time.sleep(0.01)
                name_element = ET.SubElement(testcase_element, "Name")
                name_element.text = name
                command_element = ET.SubElement(testcase_element, "Command")
                command_element.text = command
                auto_element = ET.SubElement(testcase_element, "Auto")
                auto_element.text = auto
                timeout_element = ET.SubElement(testcase_element, "Timeout")
                timeout_element.text = timeout
                description_element = ET.SubElement(testcase_element, "Description")
                description_element.text = description
                data_element = ET.SubElement(testcase_element, "Data")
                data_element.text = data
        indent(root_element)
        ET.ElementTree(root_element).write(output_file)
    
class PyAnvilParser(object):
    def __init__(self, input_file):
        self.input_file = input_file
        
    def generate(self, output_path):
        input_file_basename = os.path.basename(self.input_file).split(".")[0]
        output_file = os.path.join(output_path, input_file_basename+"_generated.xml")
        
        root_element = ET.Element("TestSuite")
        testcases_element = ET.SubElement(root_element, "TestCases")
        
        input_xml_tree = ET.parse(self.input_file)
        input_root_element = input_xml_tree.getroot()
        input_testcase_elements = input_root_element.findall("TestList/ToolCase")
        for input_testcase_element in input_testcase_elements:
            data = input_testcase_element.attrib["name"]
            executable = input_testcase_element.find("Executable").text
            parameters = input_testcase_element.find("Parameters").text
            command = executable+" "+parameters
            auto = "True"
            description = ""
            if not input_testcase_element.find("Timeout") is None:
                timeout = input_testcase_element.find("Timeout").text
            if not input_testcase_element.find("Description") is None:
                name = input_testcase_element.find("Description").text

            testcase_element = ET.SubElement(testcases_element, "TestCase")
            id_element = ET.SubElement(testcase_element, "ID")
            id_element.text = str(uuid.uuid1())
            time.sleep(0.01)
            name_element = ET.SubElement(testcase_element, "Name")
            name_element.text = name
            command_element = ET.SubElement(testcase_element, "Command")
            command_element.text = command
            auto_element = ET.SubElement(testcase_element, "Auto")
            auto_element.text = auto
            timeout_element = ET.SubElement(testcase_element, "Timeout")
            timeout_element.text = timeout
            description_element = ET.SubElement(testcase_element, "Description")
            description_element.text = description
            data_element = ET.SubElement(testcase_element, "Data")
            data_element.text = data
            
        indent(root_element)
        ET.ElementTree(root_element).write(output_file)