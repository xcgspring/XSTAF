# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'toolManager.ui'
#
# Created: Thu Mar 19 14:08:38 2015
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

class Ui_toolManagerDialog(object):
    def setupUi(self, toolManagerDialog):
        toolManagerDialog.setObjectName(_fromUtf8("toolManagerDialog"))
        toolManagerDialog.resize(408, 371)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/toolManage.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        toolManagerDialog.setWindowIcon(icon)
        self.gridLayout = QtGui.QGridLayout(toolManagerDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.loadedToolsListView = QtGui.QListView(toolManagerDialog)
        self.loadedToolsListView.setObjectName(_fromUtf8("loadedToolsListView"))
        self.gridLayout.addWidget(self.loadedToolsListView, 1, 0, 3, 1)
        self.upButton = QtGui.QToolButton(toolManagerDialog)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/up.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.upButton.setIcon(icon1)
        self.upButton.setObjectName(_fromUtf8("upButton"))
        self.gridLayout.addWidget(self.upButton, 6, 1, 1, 1)
        self.avaliableToolsListView = QtGui.QListView(toolManagerDialog)
        self.avaliableToolsListView.setObjectName(_fromUtf8("avaliableToolsListView"))
        self.gridLayout.addWidget(self.avaliableToolsListView, 6, 0, 1, 1)
        self.label = QtGui.QLabel(toolManagerDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtGui.QLabel(toolManagerDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 5, 0, 1, 1)
        self.line = QtGui.QFrame(toolManagerDialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 4, 0, 1, 1)
        self.downButton = QtGui.QToolButton(toolManagerDialog)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/down.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.downButton.setIcon(icon2)
        self.downButton.setObjectName(_fromUtf8("downButton"))
        self.gridLayout.addWidget(self.downButton, 2, 1, 1, 1)

        self.retranslateUi(toolManagerDialog)
        QtCore.QMetaObject.connectSlotsByName(toolManagerDialog)

    def retranslateUi(self, toolManagerDialog):
        toolManagerDialog.setWindowTitle(_translate("toolManagerDialog", "Tool manager", None))
        self.upButton.setText(_translate("toolManagerDialog", "up", None))
        self.label.setText(_translate("toolManagerDialog", "Loaded Tools:", None))
        self.label_2.setText(_translate("toolManagerDialog", "Available Tools:", None))
        self.downButton.setText(_translate("toolManagerDialog", "down", None))

import resources_rc
