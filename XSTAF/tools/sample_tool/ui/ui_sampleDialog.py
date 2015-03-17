# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sampleDialog.ui'
#
# Created: Tue Mar 17 12:55:23 2015
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

class Ui_SampleDialog(object):
    def setupUi(self, SampleDialog):
        SampleDialog.setObjectName(_fromUtf8("SampleDialog"))
        SampleDialog.resize(400, 60)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/sample.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        SampleDialog.setWindowIcon(icon)
        self.gridLayout = QtGui.QGridLayout(SampleDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(SampleDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(SampleDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(SampleDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), SampleDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), SampleDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SampleDialog)

    def retranslateUi(self, SampleDialog):
        SampleDialog.setWindowTitle(_translate("SampleDialog", "Sample", None))
        self.label.setText(_translate("SampleDialog", "This a sample!", None))

import resources_rc
