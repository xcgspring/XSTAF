# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resultEditor.ui'
#
# Created: Fri May 22 14:35:04 2015
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

class Ui_ResultEditorDialog(object):
    def setupUi(self, ResultEditorDialog):
        ResultEditorDialog.setObjectName(_fromUtf8("ResultEditorDialog"))
        ResultEditorDialog.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(ResultEditorDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.commentsGroupBox = QtGui.QGroupBox(ResultEditorDialog)
        self.commentsGroupBox.setObjectName(_fromUtf8("commentsGroupBox"))
        self.gridLayout_3 = QtGui.QGridLayout(self.commentsGroupBox)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.commentsTextEdit = QtGui.QTextEdit(self.commentsGroupBox)
        self.commentsTextEdit.setObjectName(_fromUtf8("commentsTextEdit"))
        self.gridLayout_3.addWidget(self.commentsTextEdit, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.commentsGroupBox, 1, 0, 1, 4)
        self.resultGroupBox = QtGui.QGroupBox(ResultEditorDialog)
        self.resultGroupBox.setObjectName(_fromUtf8("resultGroupBox"))
        self.gridLayout_2 = QtGui.QGridLayout(self.resultGroupBox)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.passRadioButton = QtGui.QRadioButton(self.resultGroupBox)
        self.passRadioButton.setObjectName(_fromUtf8("passRadioButton"))
        self.gridLayout_2.addWidget(self.passRadioButton, 0, 0, 1, 1)
        self.failRadioButton = QtGui.QRadioButton(self.resultGroupBox)
        self.failRadioButton.setObjectName(_fromUtf8("failRadioButton"))
        self.gridLayout_2.addWidget(self.failRadioButton, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.resultGroupBox, 0, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ResultEditorDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 2, 1, 2)
        spacerItem2 = QtGui.QSpacerItem(101, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 2, 1, 1, 1)

        self.retranslateUi(ResultEditorDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ResultEditorDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ResultEditorDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ResultEditorDialog)

    def retranslateUi(self, ResultEditorDialog):
        ResultEditorDialog.setWindowTitle(_translate("ResultEditorDialog", "Result Editor", None))
        self.commentsGroupBox.setTitle(_translate("ResultEditorDialog", "Comments", None))
        self.resultGroupBox.setTitle(_translate("ResultEditorDialog", "Pass/Fail", None))
        self.passRadioButton.setText(_translate("ResultEditorDialog", "Pass", None))
        self.failRadioButton.setText(_translate("ResultEditorDialog", "Fail", None))

