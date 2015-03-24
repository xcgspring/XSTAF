# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'testsuite_generator.ui'
#
# Created: Tue Mar 24 09:44:01 2015
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

class Ui_TestSuiteDialog(object):
    def setupUi(self, TestSuiteDialog):
        TestSuiteDialog.setObjectName(_fromUtf8("TestSuiteDialog"))
        TestSuiteDialog.resize(438, 211)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/generator.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        TestSuiteDialog.setWindowIcon(icon)
        self.gridLayout = QtGui.QGridLayout(TestSuiteDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.groupBox_2 = QtGui.QGroupBox(TestSuiteDialog)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label_2 = QtGui.QLabel(self.groupBox_2)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_3.addWidget(self.label_2, 1, 0, 1, 1)
        self.outputLineEdit = QtGui.QLineEdit(self.groupBox_2)
        self.outputLineEdit.setObjectName(_fromUtf8("outputLineEdit"))
        self.gridLayout_3.addWidget(self.outputLineEdit, 1, 1, 1, 1)
        self.outputToolButton = QtGui.QToolButton(self.groupBox_2)
        self.outputToolButton.setObjectName(_fromUtf8("outputToolButton"))
        self.gridLayout_3.addWidget(self.outputToolButton, 1, 2, 1, 1)
        self.gridLayout.addWidget(self.groupBox_2, 1, 0, 1, 4)
        self.buttonBox = QtGui.QDialogButtonBox(TestSuiteDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 2, 1, 1, 1)
        self.groupBox = QtGui.QGroupBox(TestSuiteDialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.csvRadioButton = QtGui.QRadioButton(self.groupBox)
        self.csvRadioButton.setObjectName(_fromUtf8("csvRadioButton"))
        self.gridLayout_2.addWidget(self.csvRadioButton, 2, 0, 1, 1)
        self.inputLineEdit = QtGui.QLineEdit(self.groupBox)
        self.inputLineEdit.setObjectName(_fromUtf8("inputLineEdit"))
        self.gridLayout_2.addWidget(self.inputLineEdit, 3, 1, 1, 1)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 3, 0, 1, 1)
        self.pyanvilRadioButton = QtGui.QRadioButton(self.groupBox)
        self.pyanvilRadioButton.setObjectName(_fromUtf8("pyanvilRadioButton"))
        self.gridLayout_2.addWidget(self.pyanvilRadioButton, 1, 0, 1, 1)
        self.inputToolButton = QtGui.QToolButton(self.groupBox)
        self.inputToolButton.setObjectName(_fromUtf8("inputToolButton"))
        self.gridLayout_2.addWidget(self.inputToolButton, 3, 2, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 1, 1, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem3, 2, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 4)

        self.retranslateUi(TestSuiteDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), TestSuiteDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), TestSuiteDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(TestSuiteDialog)

    def retranslateUi(self, TestSuiteDialog):
        TestSuiteDialog.setWindowTitle(_translate("TestSuiteDialog", "TestSuite generator", None))
        self.groupBox_2.setTitle(_translate("TestSuiteDialog", "Output", None))
        self.label_2.setText(_translate("TestSuiteDialog", "Output location", None))
        self.outputToolButton.setText(_translate("TestSuiteDialog", "...", None))
        self.groupBox.setTitle(_translate("TestSuiteDialog", "Input", None))
        self.csvRadioButton.setText(_translate("TestSuiteDialog", "From CSV", None))
        self.label.setText(_translate("TestSuiteDialog", "Input file", None))
        self.pyanvilRadioButton.setText(_translate("TestSuiteDialog", "From pyanvil senario", None))
        self.inputToolButton.setText(_translate("TestSuiteDialog", "...", None))

import resources_rc
