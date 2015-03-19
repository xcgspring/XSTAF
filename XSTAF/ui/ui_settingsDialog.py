# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settingsDialog.ui'
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

class Ui_Settings(object):
    def setupUi(self, Settings):
        Settings.setObjectName(_fromUtf8("Settings"))
        Settings.resize(400, 189)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/settings.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Settings.setWindowIcon(icon)
        self.gridLayout = QtGui.QGridLayout(Settings)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_2 = QtGui.QLabel(Settings)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.loggingFileEdit = QtGui.QLineEdit(Settings)
        self.loggingFileEdit.setObjectName(_fromUtf8("loggingFileEdit"))
        self.gridLayout.addWidget(self.loggingFileEdit, 0, 2, 1, 1)
        self.label_3 = QtGui.QLabel(Settings)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 1, 1, 1)
        self.loggingFileLevel = QtGui.QComboBox(Settings)
        self.loggingFileLevel.setObjectName(_fromUtf8("loggingFileLevel"))
        self.gridLayout.addWidget(self.loggingFileLevel, 1, 2, 1, 1)
        self.label_4 = QtGui.QLabel(Settings)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 2, 1, 1, 1)
        self.loggingStreamLevel = QtGui.QComboBox(Settings)
        self.loggingStreamLevel.setObjectName(_fromUtf8("loggingStreamLevel"))
        self.gridLayout.addWidget(self.loggingStreamLevel, 2, 2, 1, 1)
        self.line_3 = QtGui.QFrame(Settings)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.gridLayout.addWidget(self.line_3, 3, 0, 1, 3)
        self.label = QtGui.QLabel(Settings)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 4, 0, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(132, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 4, 1, 1, 1)
        self.STAFDirEdit = QtGui.QLineEdit(Settings)
        self.STAFDirEdit.setText(_fromUtf8(""))
        self.STAFDirEdit.setObjectName(_fromUtf8("STAFDirEdit"))
        self.gridLayout.addWidget(self.STAFDirEdit, 4, 2, 1, 1)
        self.line_2 = QtGui.QFrame(Settings)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout.addWidget(self.line_2, 5, 0, 1, 3)
        self.label_5 = QtGui.QLabel(Settings)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 6, 0, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 6, 1, 1, 1)
        self.WorkspaceLocation = QtGui.QLineEdit(Settings)
        self.WorkspaceLocation.setObjectName(_fromUtf8("WorkspaceLocation"))
        self.gridLayout.addWidget(self.WorkspaceLocation, 6, 2, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Settings)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 7, 0, 1, 2)

        self.retranslateUi(Settings)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Settings.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Settings.reject)
        QtCore.QMetaObject.connectSlotsByName(Settings)

    def retranslateUi(self, Settings):
        Settings.setWindowTitle(_translate("Settings", "Settings", None))
        self.label_2.setText(_translate("Settings", "logging file", None))
        self.label_3.setText(_translate("Settings", "logging file level", None))
        self.label_4.setText(_translate("Settings", "logging stream level", None))
        self.label.setText(_translate("Settings", "STAF dir", None))
        self.label_5.setText(_translate("Settings", "Workspace location", None))

import resources_rc
