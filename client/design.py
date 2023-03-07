# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'client/untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(797, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.connection_frame = QtWidgets.QFrame(self.centralwidget)
        self.connection_frame.setGeometry(QtCore.QRect(170, 310, 271, 191))
        self.connection_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.connection_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.connection_frame.setObjectName("connection_frame")
        self.groupBox = QtWidgets.QGroupBox(self.connection_frame)
        self.groupBox.setGeometry(QtCore.QRect(10, 20, 251, 151))
        self.groupBox.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox.setObjectName("groupBox")
        self.gridLayoutWidget = QtWidgets.QWidget(self.groupBox)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 251, 141))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.hostEntry = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.hostEntry.setObjectName("hostEntry")
        self.gridLayout.addWidget(self.hostEntry, 3, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 1, 1, 1)
        self.portEntry = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.portEntry.setObjectName("portEntry")
        self.gridLayout.addWidget(self.portEntry, 3, 1, 1, 1)
        self.connectButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.connectButton.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.connectButton.setObjectName("connectButton")
        self.gridLayout.addWidget(self.connectButton, 4, 0, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 2)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.idle_frame = QtWidgets.QFrame(self.centralwidget)
        self.idle_frame.setGeometry(QtCore.QRect(140, 70, 331, 221))
        self.idle_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.idle_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.idle_frame.setObjectName("idle_frame")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.idle_frame)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(10, 10, 311, 201))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.create_button_2 = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.create_button_2.setObjectName("create_button_2")
        self.gridLayout_2.addWidget(self.create_button_2, 3, 0, 1, 2)
        self.play_button = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.play_button.setObjectName("play_button")
        self.gridLayout_2.addWidget(self.play_button, 1, 1, 1, 1)
        self.world_selection = QtWidgets.QComboBox(self.gridLayoutWidget_2)
        self.world_selection.setObjectName("world_selection")
        self.world_selection.addItem("")
        self.gridLayout_2.addWidget(self.world_selection, 1, 0, 1, 1)
        self.world_frame = QtWidgets.QFrame(self.centralwidget)
        self.world_frame.setGeometry(QtCore.QRect(480, 140, 201, 211))
        self.world_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.world_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.world_frame.setObjectName("world_frame")
        self.gridLayoutWidget_3 = QtWidgets.QWidget(self.world_frame)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(10, 10, 185, 191))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.world_private = QtWidgets.QCheckBox(self.gridLayoutWidget_3)
        self.world_private.setObjectName("world_private")
        self.gridLayout_3.addWidget(self.world_private, 7, 1, 1, 1)
        self.create_button2 = QtWidgets.QPushButton(self.gridLayoutWidget_3)
        self.create_button2.setObjectName("create_button2")
        self.gridLayout_3.addWidget(self.create_button2, 9, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 3, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 0, 0, 1, 1)
        self.world_name = QtWidgets.QLineEdit(self.gridLayoutWidget_3)
        self.world_name.setObjectName("world_name")
        self.gridLayout_3.addWidget(self.world_name, 0, 1, 1, 1)
        self.world_type = QtWidgets.QLineEdit(self.gridLayoutWidget_3)
        self.world_type.setObjectName("world_type")
        self.gridLayout_3.addWidget(self.world_type, 3, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 797, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "Подключение к серверу"))
        self.hostEntry.setText(_translate("MainWindow", "127.0.0.1"))
        self.label_2.setText(_translate("MainWindow", "Порт:"))
        self.portEntry.setText(_translate("MainWindow", "4000"))
        self.connectButton.setText(_translate("MainWindow", "Подключиться"))
        self.label.setText(_translate("MainWindow", "Хост:"))
        self.create_button_2.setText(_translate("MainWindow", "Создать мир"))
        self.play_button.setText(_translate("MainWindow", "Играть"))
        self.world_selection.setItemText(0, _translate("MainWindow", "Новый мир"))
        self.world_private.setText(_translate("MainWindow", "Приватный"))
        self.create_button2.setText(_translate("MainWindow", "Создать"))
        self.label_3.setText(_translate("MainWindow", "Тип"))
        self.label_5.setText(_translate("MainWindow", "Имя"))
