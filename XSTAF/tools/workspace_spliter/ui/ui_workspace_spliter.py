# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'workspace_spliter.ui'
#
# Created: Tue Mar 24 13:44:48 2015
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

class Ui_workspaceSpliterDialog(object):
    def setupUi(self, workspaceSpliterDialog):
        workspaceSpliterDialog.setObjectName(_fromUtf8("workspaceSpliterDialog"))
        workspaceSpliterDialog.resize(400, 159)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/spliter.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        workspaceSpliterDialog.setWindowIcon(icon)
        self.gridLayout = QtGui.QGridLayout(workspaceSpliterDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.groupBox = QtGui.QGroupBox(workspaceSpliterDialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.inputLineEdit = QtGui.QLineEdit(self.groupBox)
        self.inputLineEdit.setObjectName(_fromUtf8("inputLineEdit"))
        self.gridLayout_2.addWidget(self.inputLineEdit, 0, 0, 1, 1)
        self.inputToolButton = QtGui.QToolButton(self.groupBox)
        self.inputToolButton.setObjectName(_fromUtf8("inputToolButton"))
        self.gridLayout_2.addWidget(self.inputToolButton, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        self.groupBox_2 = QtGui.QGroupBox(workspaceSpliterDialog)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.outputLineEdit = QtGui.QLineEdit(self.groupBox_2)
        self.outputLineEdit.setObjectName(_fromUtf8("outputLineEdit"))
        self.gridLayout_3.addWidget(self.outputLineEdit, 0, 0, 1, 1)
        self.outputToolButton = QtGui.QToolButton(self.groupBox_2)
        self.outputToolButton.setObjectName(_fromUtf8("outputToolButton"))
        self.gridLayout_3.addWidget(self.outputToolButton, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBox_2, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(workspaceSpliterDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)

        self.retranslateUi(workspaceSpliterDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), workspaceSpliterDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), workspaceSpliterDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(workspaceSpliterDialog)

    def retranslateUi(self, workspaceSpliterDialog):
        workspaceSpliterDialog.setWindowTitle(_translate("workspaceSpliterDialog", "Workspace Spliter", None))
        self.groupBox.setTitle(_translate("workspaceSpliterDialog", "Input workspace", None))
        self.inputToolButton.setText(_translate("workspaceSpliterDialog", "...", None))
        self.groupBox_2.setTitle(_translate("workspaceSpliterDialog", "Output workspaces path", None))
        self.outputToolButton.setText(_translate("workspaceSpliterDialog", "...", None))

import resources_rc
