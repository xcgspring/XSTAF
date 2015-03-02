# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DUT.ui'
#
# Created: Mon Mar 02 16:51:04 2015
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
        self.TestsTreeView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.TestsTreeView.setObjectName(_fromUtf8("TestsTreeView"))
        self.TestsTreeView.header().setVisible(False)
        self.gridLayout.addWidget(self.TestsTreeView, 0, 0, 1, 1)
        DUTWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(DUTWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 716, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuTestSuite = QtGui.QMenu(self.menubar)
        self.menuTestSuite.setObjectName(_fromUtf8("menuTestSuite"))
        self.menuRun = QtGui.QMenu(self.menubar)
        self.menuRun.setObjectName(_fromUtf8("menuRun"))
        DUTWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(DUTWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        DUTWindow.setStatusBar(self.statusbar)
        self.TaskQueueDock = QtGui.QDockWidget(DUTWindow)
        self.TaskQueueDock.setObjectName(_fromUtf8("TaskQueueDock"))
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.gridLayout_2 = QtGui.QGridLayout(self.dockWidgetContents)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.textEdit = QtGui.QTextEdit(self.dockWidgetContents)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.gridLayout_2.addWidget(self.textEdit, 0, 0, 1, 1)
        self.TaskQueueDock.setWidget(self.dockWidgetContents)
        DUTWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.TaskQueueDock)
        self.toolBar = QtGui.QToolBar(DUTWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        DUTWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
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
        self.actionRunTest = QtGui.QAction(DUTWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/run.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRunTest.setIcon(icon4)
        self.actionRunTest.setObjectName(_fromUtf8("actionRunTest"))
        self.actionPauseStopTest = QtGui.QAction(DUTWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/pause.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPauseStopTest.setIcon(icon5)
        self.actionPauseStopTest.setObjectName(_fromUtf8("actionPauseStopTest"))
        self.actionRefresh = QtGui.QAction(DUTWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/refresh.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRefresh.setIcon(icon6)
        self.actionRefresh.setObjectName(_fromUtf8("actionRefresh"))
        self.menuTestSuite.addAction(self.actionAddTestSuite)
        self.menuTestSuite.addAction(self.actionRemoveTestSuite)
        self.menuRun.addAction(self.actionRunTest)
        self.menuRun.addAction(self.actionPauseStopTest)
        self.menubar.addAction(self.menuTestSuite.menuAction())
        self.menubar.addAction(self.menuRun.menuAction())
        self.toolBar.addAction(self.actionAddTestSuite)
        self.toolBar.addAction(self.actionRemoveTestSuite)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionRefresh)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionRunTest)
        self.toolBar.addAction(self.actionPauseStopTest)
        self.toolBar.addSeparator()

        self.retranslateUi(DUTWindow)
        QtCore.QMetaObject.connectSlotsByName(DUTWindow)

    def retranslateUi(self, DUTWindow):
        DUTWindow.setWindowTitle(_translate("DUTWindow", "MainWindow", None))
        self.menuTestSuite.setTitle(_translate("DUTWindow", "TestSuite", None))
        self.menuRun.setTitle(_translate("DUTWindow", "Run", None))
        self.toolBar.setWindowTitle(_translate("DUTWindow", "toolBar", None))
        self.actionAddTestSuite.setText(_translate("DUTWindow", "addTestSuite", None))
        self.actionRemoveTestSuite.setText(_translate("DUTWindow", "removeTestSuite", None))
        self.actionLockDUT.setText(_translate("DUTWindow", "lockDUT", None))
        self.actionReleaseDUT.setText(_translate("DUTWindow", "releaseDUT", None))
        self.actionRunTest.setText(_translate("DUTWindow", "RunTest", None))
        self.actionRunTest.setToolTip(_translate("DUTWindow", "RunTest", None))
        self.actionPauseStopTest.setText(_translate("DUTWindow", "PauseStopTest", None))
        self.actionPauseStopTest.setToolTip(_translate("DUTWindow", "PauseStopTest", None))
        self.actionRefresh.setText(_translate("DUTWindow", "Refresh", None))
        self.actionRefresh.setToolTip(_translate("DUTWindow", "Refresh", None))

import resources_rc
