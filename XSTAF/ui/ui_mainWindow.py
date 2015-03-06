# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created: Fri Mar 06 12:47:40 2015
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

class Ui_XSTAFMainWindow(object):
    def setupUi(self, XSTAFMainWindow):
        XSTAFMainWindow.setObjectName(_fromUtf8("XSTAFMainWindow"))
        XSTAFMainWindow.resize(718, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/server.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        XSTAFMainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(XSTAFMainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_3 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.DUTView = QtGui.QTableView(self.centralwidget)
        self.DUTView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.DUTView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.DUTView.setObjectName(_fromUtf8("DUTView"))
        self.DUTView.verticalHeader().setVisible(False)
        self.gridLayout_3.addWidget(self.DUTView, 0, 0, 1, 1)
        XSTAFMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(XSTAFMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 718, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuDUTs = QtGui.QMenu(self.menubar)
        self.menuDUTs.setObjectName(_fromUtf8("menuDUTs"))
        XSTAFMainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(XSTAFMainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        XSTAFMainWindow.setStatusBar(self.statusbar)
        self.XSTAFLogDock = QtGui.QDockWidget(XSTAFMainWindow)
        self.XSTAFLogDock.setObjectName(_fromUtf8("XSTAFLogDock"))
        self.dockWidgetContents_2 = QtGui.QWidget()
        self.dockWidgetContents_2.setObjectName(_fromUtf8("dockWidgetContents_2"))
        self.gridLayout = QtGui.QGridLayout(self.dockWidgetContents_2)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.XSTAFLogEdit = QtGui.QTextEdit(self.dockWidgetContents_2)
        self.XSTAFLogEdit.setObjectName(_fromUtf8("XSTAFLogEdit"))
        self.gridLayout.addWidget(self.XSTAFLogEdit, 0, 0, 1, 1)
        self.XSTAFLogDock.setWidget(self.dockWidgetContents_2)
        XSTAFMainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.XSTAFLogDock)
        self.toolBar = QtGui.QToolBar(XSTAFMainWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        XSTAFMainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionSettings = QtGui.QAction(XSTAFMainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/settings.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSettings.setIcon(icon1)
        self.actionSettings.setObjectName(_fromUtf8("actionSettings"))
        self.actionAddDUT = QtGui.QAction(XSTAFMainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/add.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAddDUT.setIcon(icon2)
        self.actionAddDUT.setObjectName(_fromUtf8("actionAddDUT"))
        self.actionRemoveDUT = QtGui.QAction(XSTAFMainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/minus.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRemoveDUT.setIcon(icon3)
        self.actionRemoveDUT.setObjectName(_fromUtf8("actionRemoveDUT"))
        self.actionRefresh = QtGui.QAction(XSTAFMainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/refresh.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRefresh.setIcon(icon4)
        self.actionRefresh.setObjectName(_fromUtf8("actionRefresh"))
        self.actionCheckAndStartSTAF = QtGui.QAction(XSTAFMainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/connect.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCheckAndStartSTAF.setIcon(icon5)
        self.actionCheckAndStartSTAF.setObjectName(_fromUtf8("actionCheckAndStartSTAF"))
        self.menuFile.addAction(self.actionSettings)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionCheckAndStartSTAF)
        self.menuDUTs.addAction(self.actionRefresh)
        self.menuDUTs.addAction(self.actionAddDUT)
        self.menuDUTs.addAction(self.actionRemoveDUT)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuDUTs.menuAction())
        self.toolBar.addAction(self.actionSettings)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionCheckAndStartSTAF)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionRefresh)
        self.toolBar.addAction(self.actionAddDUT)
        self.toolBar.addAction(self.actionRemoveDUT)

        self.retranslateUi(XSTAFMainWindow)
        QtCore.QMetaObject.connectSlotsByName(XSTAFMainWindow)

    def retranslateUi(self, XSTAFMainWindow):
        XSTAFMainWindow.setWindowTitle(_translate("XSTAFMainWindow", "XSTAF", None))
        self.menuFile.setTitle(_translate("XSTAFMainWindow", "STAF", None))
        self.menuDUTs.setTitle(_translate("XSTAFMainWindow", "DUTs", None))
        self.XSTAFLogDock.setWindowTitle(_translate("XSTAFMainWindow", "XSTAF Log", None))
        self.toolBar.setWindowTitle(_translate("XSTAFMainWindow", "toolBar", None))
        self.actionSettings.setText(_translate("XSTAFMainWindow", "settings", None))
        self.actionAddDUT.setText(_translate("XSTAFMainWindow", "addDUT", None))
        self.actionRemoveDUT.setText(_translate("XSTAFMainWindow", "removeDUT", None))
        self.actionRefresh.setText(_translate("XSTAFMainWindow", "refresh", None))
        self.actionCheckAndStartSTAF.setText(_translate("XSTAFMainWindow", "checkAndStartSTAF", None))
        self.actionCheckAndStartSTAF.setToolTip(_translate("XSTAFMainWindow", "checkAndStartSTAF", None))

import resources_rc
