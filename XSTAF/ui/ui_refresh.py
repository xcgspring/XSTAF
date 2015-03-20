# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'refresh.ui'
#
# Created: Fri Mar 20 13:40:16 2015
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

class Ui_refreshDialog(object):
    def setupUi(self, refreshDialog):
        refreshDialog.setObjectName(_fromUtf8("refreshDialog"))
        refreshDialog.resize(377, 58)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/refresh.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        refreshDialog.setWindowIcon(icon)
        self.gridLayout = QtGui.QGridLayout(refreshDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.progressBar = QtGui.QProgressBar(refreshDialog)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout.addWidget(self.progressBar, 1, 0, 1, 1)
        self.statusLabel = QtGui.QLabel(refreshDialog)
        self.statusLabel.setObjectName(_fromUtf8("statusLabel"))
        self.gridLayout.addWidget(self.statusLabel, 0, 0, 1, 1)

        self.retranslateUi(refreshDialog)
        QtCore.QMetaObject.connectSlotsByName(refreshDialog)

    def retranslateUi(self, refreshDialog):
        refreshDialog.setWindowTitle(_translate("refreshDialog", "Refreshing", None))
        self.statusLabel.setText(_translate("refreshDialog", "TextLabel", None))

import resources_rc
