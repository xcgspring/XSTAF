# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'confirmDialog.ui'
#
# Created: Thu Mar 12 13:17:23 2015
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

class Ui_confirmDialog(object):
    def setupUi(self, confirmDialog):
        confirmDialog.setObjectName(_fromUtf8("confirmDialog"))
        confirmDialog.resize(398, 60)
        self.gridLayout = QtGui.QGridLayout(confirmDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.noButton = QtGui.QPushButton(confirmDialog)
        self.noButton.setObjectName(_fromUtf8("noButton"))
        self.gridLayout.addWidget(self.noButton, 1, 2, 1, 1)
        self.yesButton = QtGui.QPushButton(confirmDialog)
        self.yesButton.setObjectName(_fromUtf8("yesButton"))
        self.gridLayout.addWidget(self.yesButton, 1, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.messageLabel = QtGui.QLabel(confirmDialog)
        self.messageLabel.setObjectName(_fromUtf8("messageLabel"))
        self.gridLayout.addWidget(self.messageLabel, 0, 0, 1, 3)

        self.retranslateUi(confirmDialog)
        QtCore.QMetaObject.connectSlotsByName(confirmDialog)

    def retranslateUi(self, confirmDialog):
        confirmDialog.setWindowTitle(_translate("confirmDialog", "Dialog", None))
        self.noButton.setText(_translate("confirmDialog", "No", None))
        self.yesButton.setText(_translate("confirmDialog", "Yes", None))
        self.messageLabel.setText(_translate("confirmDialog", "TextLabel", None))

