# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DUT.ui'
#
# Created: Fri Mar 20 13:40:15 2015
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
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/DUT.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        DUTWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(DUTWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.TestsTreeView = QtGui.QTreeView(self.centralwidget)
        self.TestsTreeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.TestsTreeView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.TestsTreeView.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
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
        self.taskQueueListView = QtGui.QListView(self.dockWidgetContents)
        self.taskQueueListView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.taskQueueListView.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.taskQueueListView.setObjectName(_fromUtf8("taskQueueListView"))
        self.gridLayout_2.addWidget(self.taskQueueListView, 0, 1, 1, 1)
        self.TaskQueueDock.setWidget(self.dockWidgetContents)
        DUTWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.TaskQueueDock)
        self.toolBar = QtGui.QToolBar(DUTWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        DUTWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.TestInfoDock = QtGui.QDockWidget(DUTWindow)
        self.TestInfoDock.setObjectName(_fromUtf8("TestInfoDock"))
        self.dockWidgetContents_4 = QtGui.QWidget()
        self.dockWidgetContents_4.setObjectName(_fromUtf8("dockWidgetContents_4"))
        self.gridLayout_5 = QtGui.QGridLayout(self.dockWidgetContents_4)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.testInfoTableView = QtGui.QTableView(self.dockWidgetContents_4)
        self.testInfoTableView.setObjectName(_fromUtf8("testInfoTableView"))
        self.testInfoTableView.horizontalHeader().setVisible(False)
        self.testInfoTableView.verticalHeader().setVisible(False)
        self.gridLayout_5.addWidget(self.testInfoTableView, 0, 0, 1, 1)
        self.TestInfoDock.setWidget(self.dockWidgetContents_4)
        DUTWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.TestInfoDock)
        self.actionAddTestSuite = QtGui.QAction(DUTWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/addTestSuite.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAddTestSuite.setIcon(icon1)
        self.actionAddTestSuite.setObjectName(_fromUtf8("actionAddTestSuite"))
        self.actionRemoveTestSuite = QtGui.QAction(DUTWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/removeTestSuite.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRemoveTestSuite.setIcon(icon2)
        self.actionRemoveTestSuite.setObjectName(_fromUtf8("actionRemoveTestSuite"))
        self.actionLockDUT = QtGui.QAction(DUTWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/lock.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionLockDUT.setIcon(icon3)
        self.actionLockDUT.setObjectName(_fromUtf8("actionLockDUT"))
        self.actionReleaseDUT = QtGui.QAction(DUTWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/releaseLock.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionReleaseDUT.setIcon(icon4)
        self.actionReleaseDUT.setObjectName(_fromUtf8("actionReleaseDUT"))
        self.actionStartRunner = QtGui.QAction(DUTWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/run.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionStartRunner.setIcon(icon5)
        self.actionStartRunner.setObjectName(_fromUtf8("actionStartRunner"))
        self.actionRefresh = QtGui.QAction(DUTWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/refresh.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRefresh.setIcon(icon6)
        self.actionRefresh.setObjectName(_fromUtf8("actionRefresh"))
        self.actionPauseRunner = QtGui.QAction(DUTWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/pause.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPauseRunner.setIcon(icon7)
        self.actionPauseRunner.setObjectName(_fromUtf8("actionPauseRunner"))
        self.actionAddtoTaskQueue = QtGui.QAction(DUTWindow)
        self.actionAddtoTaskQueue.setObjectName(_fromUtf8("actionAddtoTaskQueue"))
        self.actionRemoveFromTaskQueue = QtGui.QAction(DUTWindow)
        self.actionRemoveFromTaskQueue.setObjectName(_fromUtf8("actionRemoveFromTaskQueue"))
        self.actionClearTaskQueue = QtGui.QAction(DUTWindow)
        self.actionClearTaskQueue.setObjectName(_fromUtf8("actionClearTaskQueue"))
        self.actionRemoveResult = QtGui.QAction(DUTWindow)
        self.actionRemoveResult.setObjectName(_fromUtf8("actionRemoveResult"))
        self.menuTestSuite.addAction(self.actionAddTestSuite)
        self.menuTestSuite.addAction(self.actionRemoveTestSuite)
        self.menuRun.addAction(self.actionStartRunner)
        self.menuRun.addAction(self.actionPauseRunner)
        self.menubar.addAction(self.menuTestSuite.menuAction())
        self.menubar.addAction(self.menuRun.menuAction())
        self.toolBar.addAction(self.actionAddTestSuite)
        self.toolBar.addAction(self.actionRemoveTestSuite)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionRefresh)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionStartRunner)
        self.toolBar.addAction(self.actionPauseRunner)
        self.toolBar.addSeparator()

        self.retranslateUi(DUTWindow)
        QtCore.QMetaObject.connectSlotsByName(DUTWindow)

    def retranslateUi(self, DUTWindow):
        DUTWindow.setWindowTitle(_translate("DUTWindow", "MainWindow", None))
        self.menuTestSuite.setTitle(_translate("DUTWindow", "TestSuite", None))
        self.menuRun.setTitle(_translate("DUTWindow", "Run", None))
        self.TaskQueueDock.setWindowTitle(_translate("DUTWindow", "Task Queue", None))
        self.toolBar.setWindowTitle(_translate("DUTWindow", "toolBar", None))
        self.TestInfoDock.setWindowTitle(_translate("DUTWindow", "Test Info", None))
        self.actionAddTestSuite.setText(_translate("DUTWindow", "addTestSuite", None))
        self.actionRemoveTestSuite.setText(_translate("DUTWindow", "removeTestSuite", None))
        self.actionLockDUT.setText(_translate("DUTWindow", "lockDUT", None))
        self.actionReleaseDUT.setText(_translate("DUTWindow", "releaseDUT", None))
        self.actionStartRunner.setText(_translate("DUTWindow", "StartRunner", None))
        self.actionStartRunner.setToolTip(_translate("DUTWindow", "StartRunner", None))
        self.actionRefresh.setText(_translate("DUTWindow", "Refresh", None))
        self.actionRefresh.setToolTip(_translate("DUTWindow", "Refresh", None))
        self.actionPauseRunner.setText(_translate("DUTWindow", "PauseRunner", None))
        self.actionPauseRunner.setToolTip(_translate("DUTWindow", "PauseRunner", None))
        self.actionAddtoTaskQueue.setText(_translate("DUTWindow", "addtoTaskQueue", None))
        self.actionAddtoTaskQueue.setToolTip(_translate("DUTWindow", "addtoTaskQueue", None))
        self.actionRemoveFromTaskQueue.setText(_translate("DUTWindow", "removeFromTaskQueue", None))
        self.actionRemoveFromTaskQueue.setToolTip(_translate("DUTWindow", "removeFromTaskQueue", None))
        self.actionClearTaskQueue.setText(_translate("DUTWindow", "clearTaskQueue", None))
        self.actionClearTaskQueue.setToolTip(_translate("DUTWindow", "clearTaskQueue", None))
        self.actionRemoveResult.setText(_translate("DUTWindow", "removeResult", None))
        self.actionRemoveResult.setToolTip(_translate("DUTWindow", "removeResult", None))

import resources_rc
