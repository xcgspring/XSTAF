# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addDUT.ui'
#
# Created: Thu Mar 19 16:55:48 2015
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

class Ui_addDUT(object):
    def setupUi(self, addDUT):
        addDUT.setObjectName(_fromUtf8("addDUT"))
        addDUT.resize(400, 96)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/add.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        addDUT.setWindowIcon(icon)
        self.gridLayout = QtGui.QGridLayout(addDUT)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.DUTIP = QtGui.QLineEdit(addDUT)
        self.DUTIP.setObjectName(_fromUtf8("DUTIP"))
        self.gridLayout.addWidget(self.DUTIP, 0, 2, 1, 1)
        self.label = QtGui.QLabel(addDUT)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(addDUT)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 3)
        spacerItem = QtGui.QSpacerItem(158, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(addDUT)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 1, 1, 1)
        self.DUTName = QtGui.QLineEdit(addDUT)
        self.DUTName.setObjectName(_fromUtf8("DUTName"))
        self.gridLayout.addWidget(self.DUTName, 1, 2, 1, 1)

        self.retranslateUi(addDUT)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), addDUT.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), addDUT.reject)
        QtCore.QMetaObject.connectSlotsByName(addDUT)

    def retranslateUi(self, addDUT):
        addDUT.setWindowTitle(_translate("addDUT", "add DUT", None))
        self.label.setText(_translate("addDUT", "DUT ip", None))
        self.label_2.setText(_translate("addDUT", "DUT name", None))

import resources_rc
