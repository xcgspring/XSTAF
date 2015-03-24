# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'workspace_merger.ui'
#
# Created: Tue Mar 24 13:44:50 2015
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

class Ui_workspaceMergerDialog(object):
    def setupUi(self, workspaceMergerDialog):
        workspaceMergerDialog.setObjectName(_fromUtf8("workspaceMergerDialog"))
        workspaceMergerDialog.resize(400, 344)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/merger.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        workspaceMergerDialog.setWindowIcon(icon)
        self.gridLayout_3 = QtGui.QGridLayout(workspaceMergerDialog)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.groupBox = QtGui.QGroupBox(workspaceMergerDialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.inputLineEdit = QtGui.QLineEdit(self.groupBox)
        self.inputLineEdit.setObjectName(_fromUtf8("inputLineEdit"))
        self.gridLayout_2.addWidget(self.inputLineEdit, 1, 0, 1, 3)
        self.addButton = QtGui.QPushButton(self.groupBox)
        self.addButton.setObjectName(_fromUtf8("addButton"))
        self.gridLayout_2.addWidget(self.addButton, 2, 0, 1, 1)
        self.inputToolButton = QtGui.QToolButton(self.groupBox)
        self.inputToolButton.setObjectName(_fromUtf8("inputToolButton"))
        self.gridLayout_2.addWidget(self.inputToolButton, 1, 3, 1, 1)
        self.removeButton = QtGui.QPushButton(self.groupBox)
        self.removeButton.setObjectName(_fromUtf8("removeButton"))
        self.gridLayout_2.addWidget(self.removeButton, 2, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 2, 2, 1, 1)
        self.inputListView = QtGui.QListView(self.groupBox)
        self.inputListView.setObjectName(_fromUtf8("inputListView"))
        self.gridLayout_2.addWidget(self.inputListView, 0, 0, 1, 4)
        self.gridLayout_3.addWidget(self.groupBox, 0, 0, 2, 2)
        self.groupBox_2 = QtGui.QGroupBox(workspaceMergerDialog)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.outputToolButton = QtGui.QToolButton(self.groupBox_2)
        self.outputToolButton.setObjectName(_fromUtf8("outputToolButton"))
        self.gridLayout.addWidget(self.outputToolButton, 0, 1, 1, 1)
        self.outputLineEdit = QtGui.QLineEdit(self.groupBox_2)
        self.outputLineEdit.setObjectName(_fromUtf8("outputLineEdit"))
        self.gridLayout.addWidget(self.outputLineEdit, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_2, 2, 0, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(workspaceMergerDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_3.addWidget(self.buttonBox, 3, 0, 1, 1)

        self.retranslateUi(workspaceMergerDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), workspaceMergerDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), workspaceMergerDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(workspaceMergerDialog)

    def retranslateUi(self, workspaceMergerDialog):
        workspaceMergerDialog.setWindowTitle(_translate("workspaceMergerDialog", "Workspace Merger", None))
        self.groupBox.setTitle(_translate("workspaceMergerDialog", "Input workspaces", None))
        self.addButton.setText(_translate("workspaceMergerDialog", "Add", None))
        self.inputToolButton.setText(_translate("workspaceMergerDialog", "...", None))
        self.removeButton.setText(_translate("workspaceMergerDialog", "Remove", None))
        self.groupBox_2.setTitle(_translate("workspaceMergerDialog", "Output workspace", None))
        self.outputToolButton.setText(_translate("workspaceMergerDialog", "...", None))

import resources_rc
