# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DUT.ui'
#
# Created: Fri Feb 27 10:55:34 2015
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

class Ui_DUTWindow(object):
    def setupUi(self, DUTWindow):
        DUTWindow.setObjectName(_fromUtf8("DUTWindow"))
        DUTWindow.resize(716, 578)
        self.centralwidget = QtGui.QWidget(DUTWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.TestsTreeView = QtGui.QTreeView(self.centralwidget)
        self.TestsTreeView.setObjectName(_fromUtf8("TestsTreeView"))
        self.gridLayout.addWidget(self.TestsTreeView, 0, 0, 1, 1)
        DUTWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(DUTWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 716, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuDUT = QtGui.QMenu(self.menubar)
        self.menuDUT.setObjectName(_fromUtf8("menuDUT"))
        self.menuTestSuite = QtGui.QMenu(self.menubar)
        self.menuTestSuite.setObjectName(_fromUtf8("menuTestSuite"))
        DUTWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(DUTWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        DUTWindow.setStatusBar(self.statusbar)
        self.dockWidget = QtGui.QDockWidget(DUTWindow)
        self.dockWidget.setObjectName(_fromUtf8("dockWidget"))
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.gridLayout_2 = QtGui.QGridLayout(self.dockWidgetContents)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.textEdit = QtGui.QTextEdit(self.dockWidgetContents)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.gridLayout_2.addWidget(self.textEdit, 0, 0, 1, 1)
        self.dockWidget.setWidget(self.dockWidgetContents)
        DUTWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.dockWidget)
        self.toolBar = QtGui.QToolBar(DUTWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        DUTWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.dockWidget_2 = QtGui.QDockWidget(DUTWindow)
        self.dockWidget_2.setObjectName(_fromUtf8("dockWidget_2"))
        self.dockWidgetContents_2 = QtGui.QWidget()
        self.dockWidgetContents_2.setObjectName(_fromUtf8("dockWidgetContents_2"))
        self.gridLayout_4 = QtGui.QGridLayout(self.dockWidgetContents_2)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.textEdit_2 = QtGui.QTextEdit(self.dockWidgetContents_2)
        self.textEdit_2.setObjectName(_fromUtf8("textEdit_2"))
        self.gridLayout_4.addWidget(self.textEdit_2, 0, 0, 1, 1)
        self.dockWidget_2.setWidget(self.dockWidgetContents_2)
        DUTWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.dockWidget_2)
        self.dockWidget_3 = QtGui.QDockWidget(DUTWindow)
        self.dockWidget_3.setObjectName(_fromUtf8("dockWidget_3"))
        self.dockWidgetContents_3 = QtGui.QWidget()
        self.dockWidgetContents_3.setObjectName(_fromUtf8("dockWidgetContents_3"))
        self.gridLayout_3 = QtGui.QGridLayout(self.dockWidgetContents_3)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.textEdit_3 = QtGui.QTextEdit(self.dockWidgetContents_3)
        self.textEdit_3.setObjectName(_fromUtf8("textEdit_3"))
        self.gridLayout_3.addWidget(self.textEdit_3, 0, 0, 1, 1)
        self.dockWidget_3.setWidget(self.dockWidgetContents_3)
        DUTWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.dockWidget_3)
        self.actionAddTestSuite = QtGui.QAction(DUTWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/addTestSuite.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAddTestSuite.setIcon(icon)
        self.actionAddTestSuite.setObjectName(_fromUtf8("actionAddTestSuite"))
        self.actionRemoveTestSuite = QtGui.QAction(DUTWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/removeTestSuite.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRemoveTestSuite.setIcon(icon1)
        self.actionRemoveTestSuite.setObjectName(_fromUtf8("actionRemoveTestSuite"))
        self.actionLockDUT = QtGui.QAction(DUTWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/lock.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionLockDUT.setIcon(icon2)
        self.actionLockDUT.setObjectName(_fromUtf8("actionLockDUT"))
        self.actionReleaseDUT = QtGui.QAction(DUTWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/releaseLock.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionReleaseDUT.setIcon(icon3)
        self.actionReleaseDUT.setObjectName(_fromUtf8("actionReleaseDUT"))
        self.menuDUT.addAction(self.actionLockDUT)
        self.menuDUT.addAction(self.actionReleaseDUT)
        self.menuTestSuite.addAction(self.actionAddTestSuite)
        self.menuTestSuite.addAction(self.actionRemoveTestSuite)
        self.menubar.addAction(self.menuDUT.menuAction())
        self.menubar.addAction(self.menuTestSuite.menuAction())
        self.toolBar.addAction(self.actionAddTestSuite)
        self.toolBar.addAction(self.actionRemoveTestSuite)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionLockDUT)
        self.toolBar.addAction(self.actionReleaseDUT)

        self.retranslateUi(DUTWindow)
        QtCore.QMetaObject.connectSlotsByName(DUTWindow)

    def retranslateUi(self, DUTWindow):
        DUTWindow.setWindowTitle(_translate("DUTWindow", "MainWindow", None))
        self.menuDUT.setTitle(_translate("DUTWindow", "DUT", None))
        self.menuTestSuite.setTitle(_translate("DUTWindow", "TestSuite", None))
        self.toolBar.setWindowTitle(_translate("DUTWindow", "toolBar", None))
        self.actionAddTestSuite.setText(_translate("DUTWindow", "addTestSuite", None))
        self.actionRemoveTestSuite.setText(_translate("DUTWindow", "removeTestSuite", None))
        self.actionLockDUT.setText(_translate("DUTWindow", "lockDUT", None))
        self.actionReleaseDUT.setText(_translate("DUTWindow", "releaseDUT", None))

import resources_rc
