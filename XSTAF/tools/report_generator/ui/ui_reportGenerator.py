# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'reportGenerator.ui'
#
# Created: Fri May 15 16:15:54 2015
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
        TestReportDialog.resize(531, 463)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/report_generate.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        TestReportDialog.setWindowIcon(icon)
        self.gridLayout = QtGui.QGridLayout(TestReportDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.passFailSettingsGroupBox2 = QtGui.QGroupBox(TestReportDialog)
        self.passFailSettingsGroupBox2.setObjectName(_fromUtf8("passFailSettingsGroupBox2"))
        self.gridLayout_3 = QtGui.QGridLayout(self.passFailSettingsGroupBox2)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.failFirstRadioButton2 = QtGui.QRadioButton(self.passFailSettingsGroupBox2)
        self.failFirstRadioButton2.setObjectName(_fromUtf8("failFirstRadioButton2"))
        self.gridLayout_3.addWidget(self.failFirstRadioButton2, 1, 0, 1, 1)
        self.passFirstRadioButton2 = QtGui.QRadioButton(self.passFailSettingsGroupBox2)
        self.passFirstRadioButton2.setObjectName(_fromUtf8("passFirstRadioButton2"))
        self.gridLayout_3.addWidget(self.passFirstRadioButton2, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.passFailSettingsGroupBox2, 0, 1, 1, 1)
        self.reportInfoGroupBox = QtGui.QGroupBox(TestReportDialog)
        self.reportInfoGroupBox.setObjectName(_fromUtf8("reportInfoGroupBox"))
        self.gridLayout_5 = QtGui.QGridLayout(self.reportInfoGroupBox)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.label_6 = QtGui.QLabel(self.reportInfoGroupBox)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_5.addWidget(self.label_6, 0, 0, 1, 1)
        self.titleEdit = QtGui.QLineEdit(self.reportInfoGroupBox)
        self.titleEdit.setObjectName(_fromUtf8("titleEdit"))
        self.gridLayout_5.addWidget(self.titleEdit, 0, 1, 1, 1)
        self.label_7 = QtGui.QLabel(self.reportInfoGroupBox)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_5.addWidget(self.label_7, 1, 0, 1, 2)
        self.summaryTextEdit = QtGui.QTextEdit(self.reportInfoGroupBox)
        self.summaryTextEdit.setObjectName(_fromUtf8("summaryTextEdit"))
        self.gridLayout_5.addWidget(self.summaryTextEdit, 2, 0, 1, 2)
        self.gridLayout.addWidget(self.reportInfoGroupBox, 6, 0, 1, 2)
        self.ReportLocationGroupBox = QtGui.QGroupBox(TestReportDialog)
        self.ReportLocationGroupBox.setObjectName(_fromUtf8("ReportLocationGroupBox"))
        self.gridLayout_6 = QtGui.QGridLayout(self.ReportLocationGroupBox)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.reportLineEdit = QtGui.QLineEdit(self.ReportLocationGroupBox)
        self.reportLineEdit.setObjectName(_fromUtf8("reportLineEdit"))
        self.gridLayout_6.addWidget(self.reportLineEdit, 0, 0, 1, 1)
        self.searchToolButton = QtGui.QToolButton(self.ReportLocationGroupBox)
        self.searchToolButton.setObjectName(_fromUtf8("searchToolButton"))
        self.gridLayout_6.addWidget(self.searchToolButton, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.ReportLocationGroupBox, 7, 0, 1, 2)
        self.passFailSettingsGroupBox1 = QtGui.QGroupBox(TestReportDialog)
        self.passFailSettingsGroupBox1.setObjectName(_fromUtf8("passFailSettingsGroupBox1"))
        self.gridLayout_8 = QtGui.QGridLayout(self.passFailSettingsGroupBox1)
        self.gridLayout_8.setObjectName(_fromUtf8("gridLayout_8"))
        self.passFirstRadioButton1 = QtGui.QRadioButton(self.passFailSettingsGroupBox1)
        self.passFirstRadioButton1.setObjectName(_fromUtf8("passFirstRadioButton1"))
        self.gridLayout_8.addWidget(self.passFirstRadioButton1, 0, 0, 1, 1)
        self.failFirstRadioButton1 = QtGui.QRadioButton(self.passFailSettingsGroupBox1)
        self.failFirstRadioButton1.setObjectName(_fromUtf8("failFirstRadioButton1"))
        self.gridLayout_8.addWidget(self.failFirstRadioButton1, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.passFailSettingsGroupBox1, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(TestReportDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 8, 0, 1, 2)
        self.formatSettingsGroupBox = QtGui.QGroupBox(TestReportDialog)
        self.formatSettingsGroupBox.setObjectName(_fromUtf8("formatSettingsGroupBox"))
        self.gridLayout_4 = QtGui.QGridLayout(self.formatSettingsGroupBox)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.excelCheckBox = QtGui.QCheckBox(self.formatSettingsGroupBox)
        self.excelCheckBox.setObjectName(_fromUtf8("excelCheckBox"))
        self.gridLayout_4.addWidget(self.excelCheckBox, 2, 1, 1, 1)
        self.htmlCheckBox = QtGui.QCheckBox(self.formatSettingsGroupBox)
        self.htmlCheckBox.setObjectName(_fromUtf8("htmlCheckBox"))
        self.gridLayout_4.addWidget(self.htmlCheckBox, 0, 1, 1, 1)
        self.csvCheckBox = QtGui.QCheckBox(self.formatSettingsGroupBox)
        self.csvCheckBox.setObjectName(_fromUtf8("csvCheckBox"))
        self.gridLayout_4.addWidget(self.csvCheckBox, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.formatSettingsGroupBox, 2, 0, 1, 2)

        self.retranslateUi(TestReportDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), TestReportDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), TestReportDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(TestReportDialog)

    def retranslateUi(self, TestReportDialog):
        TestReportDialog.setWindowTitle(_translate("TestReportDialog", "Test Report Generator", None))
        self.passFailSettingsGroupBox2.setTitle(_translate("TestReportDialog", "Pass/Fail setting for multiple runs on different DUT:", None))
        self.failFirstRadioButton2.setText(_translate("TestReportDialog", "Fail first", None))
        self.passFirstRadioButton2.setText(_translate("TestReportDialog", "Pass first", None))
        self.reportInfoGroupBox.setTitle(_translate("TestReportDialog", "Report infomations:", None))
        self.label_6.setText(_translate("TestReportDialog", "Title:", None))
        self.label_7.setText(_translate("TestReportDialog", "Summary:", None))
        self.ReportLocationGroupBox.setTitle(_translate("TestReportDialog", "Report location:", None))
        self.searchToolButton.setText(_translate("TestReportDialog", "...", None))
        self.passFailSettingsGroupBox1.setTitle(_translate("TestReportDialog", "Pass/Fail setting for multiple runs on same DUT:", None))
        self.passFirstRadioButton1.setText(_translate("TestReportDialog", "Pass first", None))
        self.failFirstRadioButton1.setText(_translate("TestReportDialog", "Fail first", None))
        self.formatSettingsGroupBox.setTitle(_translate("TestReportDialog", "Format setting:", None))
        self.excelCheckBox.setText(_translate("TestReportDialog", "Excel (Not support yet)", None))
        self.htmlCheckBox.setText(_translate("TestReportDialog", "HTML (use jinja2 template library)", None))
        self.csvCheckBox.setText(_translate("TestReportDialog", "CSV (Not support yet)", None))

import resources_rc
