# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settingsDialog.ui'
#
# Created: Fri Jun 05 09:54:09 2015
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
        Settings.resize(546, 502)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/settings.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Settings.setWindowIcon(icon)
        self.gridLayout = QtGui.QGridLayout(Settings)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.groupBox_5 = QtGui.QGroupBox(Settings)
        self.groupBox_5.setObjectName(_fromUtf8("groupBox_5"))
        self.gridLayout_6 = QtGui.QGridLayout(self.groupBox_5)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.label_8 = QtGui.QLabel(self.groupBox_5)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout_6.addWidget(self.label_8, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(194, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem, 0, 1, 2, 1)
        self.dutTmpFilesLocationEdit = QtGui.QLineEdit(self.groupBox_5)
        self.dutTmpFilesLocationEdit.setObjectName(_fromUtf8("dutTmpFilesLocationEdit"))
        self.gridLayout_6.addWidget(self.dutTmpFilesLocationEdit, 1, 2, 2, 1)
        self.label_9 = QtGui.QLabel(self.groupBox_5)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout_6.addWidget(self.label_9, 2, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(194, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem1, 2, 1, 1, 1)
        self.dutLogLocationEdit = QtGui.QLineEdit(self.groupBox_5)
        self.dutLogLocationEdit.setObjectName(_fromUtf8("dutLogLocationEdit"))
        self.gridLayout_6.addWidget(self.dutLogLocationEdit, 0, 2, 1, 1)
        self.gridLayout.addWidget(self.groupBox_5, 5, 0, 1, 3)
        self.groupBox = QtGui.QGroupBox(Settings)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)
        self.loggingFileLevel = QtGui.QComboBox(self.groupBox)
        self.loggingFileLevel.setObjectName(_fromUtf8("loggingFileLevel"))
        self.gridLayout_2.addWidget(self.loggingFileLevel, 1, 3, 1, 1)
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_2.addWidget(self.label_4, 2, 0, 1, 1)
        self.loggingStreamLevel = QtGui.QComboBox(self.groupBox)
        self.loggingStreamLevel.setObjectName(_fromUtf8("loggingStreamLevel"))
        self.gridLayout_2.addWidget(self.loggingStreamLevel, 2, 3, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 2, 1, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem3, 1, 1, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem4, 1, 2, 1, 1)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem5, 2, 2, 1, 1)
        self.loggingFileEdit = QtGui.QLineEdit(self.groupBox)
        self.loggingFileEdit.setObjectName(_fromUtf8("loggingFileEdit"))
        self.gridLayout_2.addWidget(self.loggingFileEdit, 0, 2, 1, 2)
        spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem6, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 3)
        self.groupBox_3 = QtGui.QGroupBox(Settings)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.gridLayout_4 = QtGui.QGridLayout(self.groupBox_3)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        spacerItem7 = QtGui.QSpacerItem(199, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem7, 0, 1, 1, 1)
        self.WorkspaceLocation = QtGui.QLineEdit(self.groupBox_3)
        self.WorkspaceLocation.setObjectName(_fromUtf8("WorkspaceLocation"))
        self.gridLayout_4.addWidget(self.WorkspaceLocation, 0, 2, 1, 1)
        self.label_5 = QtGui.QLabel(self.groupBox_3)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_4.addWidget(self.label_5, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_3, 3, 0, 1, 3)
        self.groupBox_2 = QtGui.QGroupBox(Settings)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label = QtGui.QLabel(self.groupBox_2)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        spacerItem8 = QtGui.QSpacerItem(226, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem8, 0, 1, 1, 1)
        self.STAFDirEdit = QtGui.QLineEdit(self.groupBox_2)
        self.STAFDirEdit.setText(_fromUtf8(""))
        self.STAFDirEdit.setObjectName(_fromUtf8("STAFDirEdit"))
        self.gridLayout_3.addWidget(self.STAFDirEdit, 0, 2, 1, 1)
        self.gridLayout.addWidget(self.groupBox_2, 2, 0, 1, 3)
        self.groupBox_4 = QtGui.QGroupBox(Settings)
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.gridLayout_5 = QtGui.QGridLayout(self.groupBox_4)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.toolLocationEdit = QtGui.QLineEdit(self.groupBox_4)
        self.toolLocationEdit.setObjectName(_fromUtf8("toolLocationEdit"))
        self.gridLayout_5.addWidget(self.toolLocationEdit, 0, 2, 1, 1)
        self.label_6 = QtGui.QLabel(self.groupBox_4)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_5.addWidget(self.label_6, 0, 0, 1, 1)
        self.toolConfigureFileEdit = QtGui.QLineEdit(self.groupBox_4)
        self.toolConfigureFileEdit.setObjectName(_fromUtf8("toolConfigureFileEdit"))
        self.gridLayout_5.addWidget(self.toolConfigureFileEdit, 1, 2, 3, 1)
        spacerItem9 = QtGui.QSpacerItem(150, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem9, 0, 1, 1, 1)
        spacerItem10 = QtGui.QSpacerItem(150, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem10, 2, 1, 1, 1)
        self.label_7 = QtGui.QLabel(self.groupBox_4)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_5.addWidget(self.label_7, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_4, 4, 0, 1, 3)
        self.buttonBox = QtGui.QDialogButtonBox(Settings)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 7, 0, 1, 2)
        self.restoreButton = QtGui.QPushButton(Settings)
        self.restoreButton.setObjectName(_fromUtf8("restoreButton"))
        self.gridLayout.addWidget(self.restoreButton, 6, 2, 1, 1)

        self.retranslateUi(Settings)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Settings.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Settings.reject)
        QtCore.QMetaObject.connectSlotsByName(Settings)

    def retranslateUi(self, Settings):
        Settings.setWindowTitle(_translate("Settings", "Settings", None))
        self.groupBox_5.setTitle(_translate("Settings", "DUT settings", None))
        self.label_8.setText(_translate("Settings", "DUT log location", None))
        self.label_9.setText(_translate("Settings", "DUT tmp files location", None))
        self.groupBox.setTitle(_translate("Settings", "logging settings", None))
        self.label_2.setText(_translate("Settings", "logging file", None))
        self.label_3.setText(_translate("Settings", "logging file level", None))
        self.label_4.setText(_translate("Settings", "logging stream level", None))
        self.groupBox_3.setTitle(_translate("Settings", "Workspace settings", None))
        self.label_5.setText(_translate("Settings", "Workspace location", None))
        self.groupBox_2.setTitle(_translate("Settings", "STAF settings", None))
        self.label.setText(_translate("Settings", "STAF dir", None))
        self.groupBox_4.setTitle(_translate("Settings", "Tool settings", None))
        self.label_6.setText(_translate("Settings", "Tool location", None))
        self.label_7.setText(_translate("Settings", "Tool configure file", None))
        self.restoreButton.setText(_translate("Settings", "Restore default settings", None))

import resources_rc
