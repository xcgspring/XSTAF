# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'reportGenerator.ui'
#
# Created: Thu Mar 19 16:55:50 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_TestReportDialog(object):
    def setupUi(self, TestReportDialog):
        TestReportDialog.setObjectName(_fromUtf8("TestReportDialog"))
        TestReportDialog.resize(582, 463)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/report_generate.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        TestReportDialog.setWindowIcon(icon)
        self.gridLayout = QtGui.QGridLayout(TestReportDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.radioButton_4 = QtGui.QRadioButton(TestReportDialog)
        self.radioButton_4.setObjectName(_fromUtf8("radioButton_4"))
        self.gridLayout.addWidget(self.radioButton_4, 5, 1, 1, 1)
        self.line = QtGui.QFrame(TestReportDialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 0, 0, 1, 3)
        self.radioButton = QtGui.QRadioButton(TestReportDialog)
        self.radioButton.setObjectName(_fromUtf8("radioButton"))
        self.gridLayout.addWidget(self.radioButton, 1, 1, 1, 1)
        self.radioButton_2 = QtGui.QRadioButton(TestReportDialog)
        self.radioButton_2.setObjectName(_fromUtf8("radioButton_2"))
        self.gridLayout.addWidget(self.radioButton_2, 2, 1, 1, 1)
        self.line_2 = QtGui.QFrame(TestReportDialog)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout.addWidget(self.line_2, 8, 0, 1, 3)
        self.checkBox = QtGui.QCheckBox(TestReportDialog)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.gridLayout.addWidget(self.checkBox, 9, 1, 1, 1)
        self.checkBox_2 = QtGui.QCheckBox(TestReportDialog)
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
        self.gridLayout.addWidget(self.checkBox_2, 10, 1, 1, 1)
        self.label_3 = QtGui.QLabel(TestReportDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 21, 0, 1, 1)
        self.line_3 = QtGui.QFrame(TestReportDialog)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.gridLayout.addWidget(self.line_3, 11, 0, 1, 3)
        self.buttonBox = QtGui.QDialogButtonBox(TestReportDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 22, 0, 1, 3)
        self.lineEdit = QtGui.QLineEdit(TestReportDialog)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.gridLayout.addWidget(self.lineEdit, 21, 1, 1, 1)
        self.line_4 = QtGui.QFrame(TestReportDialog)
        self.line_4.setFrameShape(QtGui.QFrame.HLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_4.setObjectName(_fromUtf8("line_4"))
        self.gridLayout.addWidget(self.line_4, 3, 0, 1, 3)
        self.radioButton_3 = QtGui.QRadioButton(TestReportDialog)
        self.radioButton_3.setObjectName(_fromUtf8("radioButton_3"))
        self.gridLayout.addWidget(self.radioButton_3, 4, 1, 1, 1)
        self.label_5 = QtGui.QLabel(TestReportDialog)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 12, 0, 1, 1)
        self.label_6 = QtGui.QLabel(TestReportDialog)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 12, 1, 1, 1)
        self.lineEdit_2 = QtGui.QLineEdit(TestReportDialog)
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.gridLayout.addWidget(self.lineEdit_2, 12, 2, 1, 1)
        self.label_7 = QtGui.QLabel(TestReportDialog)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 13, 1, 1, 1)
        self.textBrowser = QtGui.QTextBrowser(TestReportDialog)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.gridLayout.addWidget(self.textBrowser, 14, 1, 1, 2)
        self.label = QtGui.QLabel(TestReportDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.toolButton = QtGui.QToolButton(TestReportDialog)
        self.toolButton.setObjectName(_fromUtf8("toolButton"))
        self.gridLayout.addWidget(self.toolButton, 21, 2, 1, 1)
        self.label_2 = QtGui.QLabel(TestReportDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 9, 0, 1, 1)
        self.label_4 = QtGui.QLabel(TestReportDialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)
        self.line_5 = QtGui.QFrame(TestReportDialog)
        self.line_5.setFrameShape(QtGui.QFrame.HLine)
        self.line_5.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_5.setObjectName(_fromUtf8("line_5"))
        self.gridLayout.addWidget(self.line_5, 20, 0, 1, 3)

        self.retranslateUi(TestReportDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), TestReportDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), TestReportDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(TestReportDialog)

    def retranslateUi(self, TestReportDialog):
        TestReportDialog.setWindowTitle(_translate("TestReportDialog", "Test Report Generator", None))
        self.radioButton_4.setText(_translate("TestReportDialog", "Fail first", None))
        self.radioButton.setText(_translate("TestReportDialog", "Generate one report for all DUTs", None))
        self.radioButton_2.setText(_translate("TestReportDialog", "Generate one report for each DUT", None))
        self.checkBox.setText(_translate("TestReportDialog", "HTML (Require jinja2 installed)", None))
        self.checkBox_2.setText(_translate("TestReportDialog", "Excel (Require MS Excel installed)", None))
        self.label_3.setText(_translate("TestReportDialog", "Report location:", None))
        self.radioButton_3.setText(_translate("TestReportDialog", "Pass first", None))
        self.label_5.setText(_translate("TestReportDialog", "Report infomations:", None))
        self.label_6.setText(_translate("TestReportDialog", "Title:", None))
        self.label_7.setText(_translate("TestReportDialog", "Summary:", None))
        self.label.setText(_translate("TestReportDialog", "Merge setting:", None))
        self.toolButton.setText(_translate("TestReportDialog", "...", None))
        self.label_2.setText(_translate("TestReportDialog", "Format setting:", None))
        self.label_4.setText(_translate("TestReportDialog", "Test Case Pass/Fail setting:", None))

import resources_rc
