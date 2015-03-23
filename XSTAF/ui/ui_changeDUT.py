# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'changeDUT.ui'
#
# Created: Mon Mar 23 13:42:56 2015
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

class Ui_changeDUT(object):
    def setupUi(self, changeDUT):
        changeDUT.setObjectName(_fromUtf8("changeDUT"))
        changeDUT.resize(400, 119)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/DUT.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        changeDUT.setWindowIcon(icon)
        self.gridLayout = QtGui.QGridLayout(changeDUT)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.DUTIP = QtGui.QLineEdit(changeDUT)
        self.DUTIP.setObjectName(_fromUtf8("DUTIP"))
        self.gridLayout.addWidget(self.DUTIP, 1, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(changeDUT)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 3)
        self.label = QtGui.QLabel(changeDUT)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(158, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 1, 1, 1)
        self.label_2 = QtGui.QLabel(changeDUT)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.DUTName = QtGui.QLineEdit(changeDUT)
        self.DUTName.setObjectName(_fromUtf8("DUTName"))
        self.gridLayout.addWidget(self.DUTName, 2, 2, 1, 1)
        self.orginalDUTInfo = QtGui.QLabel(changeDUT)
        self.orginalDUTInfo.setObjectName(_fromUtf8("orginalDUTInfo"))
        self.gridLayout.addWidget(self.orginalDUTInfo, 0, 0, 1, 3)

        self.retranslateUi(changeDUT)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), changeDUT.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), changeDUT.reject)
        QtCore.QMetaObject.connectSlotsByName(changeDUT)

    def retranslateUi(self, changeDUT):
        changeDUT.setWindowTitle(_translate("changeDUT", "change DUT info", None))
        self.label.setText(_translate("changeDUT", "DUT ip", None))
        self.label_2.setText(_translate("changeDUT", "DUT name", None))
        self.orginalDUTInfo.setText(_translate("changeDUT", "TextLabel", None))

import resources_rc
