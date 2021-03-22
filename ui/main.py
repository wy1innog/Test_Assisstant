# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QAction


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(976, 724)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QtCore.QSize(200, 0))
        self.tabWidget.setObjectName("tabWidget")
        self.AP_2 = QtWidgets.QWidget()
        self.AP_2.setObjectName("AP_2")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.AP_2)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.GroupBox_AP_test = QtWidgets.QGroupBox(self.AP_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.GroupBox_AP_test.sizePolicy().hasHeightForWidth())
        self.GroupBox_AP_test.setSizePolicy(sizePolicy)
        self.GroupBox_AP_test.setMinimumSize(QtCore.QSize(280, 0))
        self.GroupBox_AP_test.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.GroupBox_AP_test.setTitle("")
        self.GroupBox_AP_test.setObjectName("GroupBox_AP_test")
        self.Label_dev_check = QtWidgets.QLabel(self.GroupBox_AP_test)
        self.Label_dev_check.setGeometry(QtCore.QRect(20, 10, 61, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Label_dev_check.sizePolicy().hasHeightForWidth())
        self.Label_dev_check.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(9)
        self.Label_dev_check.setFont(font)
        self.Label_dev_check.setObjectName("Label_dev_check")
        self.Btn_dev_check = QtWidgets.QPushButton(self.GroupBox_AP_test)
        self.Btn_dev_check.setGeometry(QtCore.QRect(110, 20, 110, 25))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Btn_dev_check.sizePolicy().hasHeightForWidth())
        self.Btn_dev_check.setSizePolicy(sizePolicy)
        self.Btn_dev_check.setObjectName("Btn_dev_check")
        self.ComboBox_dev_select = QtWidgets.QComboBox(self.GroupBox_AP_test)
        self.ComboBox_dev_select.setGeometry(QtCore.QRect(110, 60, 110, 22))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ComboBox_dev_select.sizePolicy().hasHeightForWidth())
        self.ComboBox_dev_select.setSizePolicy(sizePolicy)
        self.ComboBox_dev_select.setObjectName("ComboBox_dev_select")
        self.CheckBox_SIM_test = QtWidgets.QCheckBox(self.GroupBox_AP_test)
        self.CheckBox_SIM_test.setGeometry(QtCore.QRect(20, 150, 91, 19))
        self.CheckBox_SIM_test.setObjectName("CheckBox_SIM_test")
        self.CheckBox_reboot_test = QtWidgets.QCheckBox(self.GroupBox_AP_test)
        self.CheckBox_reboot_test.setGeometry(QtCore.QRect(20, 190, 101, 19))
        self.CheckBox_reboot_test.setObjectName("CheckBox_reboot_test")
        self.Label_dev_select = QtWidgets.QLabel(self.GroupBox_AP_test)
        self.Label_dev_select.setGeometry(QtCore.QRect(20, 50, 61, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Label_dev_select.sizePolicy().hasHeightForWidth())
        self.Label_dev_select.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(9)
        self.Label_dev_select.setFont(font)
        self.Label_dev_select.setObjectName("Label_dev_select")
        self.CheckBox_SDcard_test = QtWidgets.QCheckBox(self.GroupBox_AP_test)
        self.CheckBox_SDcard_test.setGeometry(QtCore.QRect(140, 150, 91, 19))
        self.CheckBox_SDcard_test.setObjectName("CheckBox_SDcard_test")
        self.CheckBox_BT_test = QtWidgets.QCheckBox(self.GroupBox_AP_test)
        self.CheckBox_BT_test.setGeometry(QtCore.QRect(140, 190, 121, 19))
        self.CheckBox_BT_test.setObjectName("CheckBox_BT_test")
        self.CheckBox_GPS_test = QtWidgets.QCheckBox(self.GroupBox_AP_test)
        self.CheckBox_GPS_test.setGeometry(QtCore.QRect(20, 230, 111, 19))
        self.CheckBox_GPS_test.setObjectName("CheckBox_GPS_test")
        self.CheckBox_AP_caller_hang_up_test = QtWidgets.QCheckBox(self.GroupBox_AP_test)
        self.CheckBox_AP_caller_hang_up_test.setGeometry(QtCore.QRect(20, 440, 91, 19))
        self.CheckBox_AP_caller_hang_up_test.setObjectName("CheckBox_AP_caller_hang_up_test")
        self.CheckBox_AP_caller_was_hang_up_test = QtWidgets.QCheckBox(self.GroupBox_AP_test)
        self.CheckBox_AP_caller_was_hang_up_test.setGeometry(QtCore.QRect(140, 440, 91, 19))
        self.CheckBox_AP_caller_was_hang_up_test.setObjectName("CheckBox_AP_caller_was_hang_up_test")
        self.CheckBox_AP_caller_was_refused_test = QtWidgets.QCheckBox(self.GroupBox_AP_test)
        self.CheckBox_AP_caller_was_refused_test.setGeometry(QtCore.QRect(20, 480, 91, 19))
        self.CheckBox_AP_caller_was_refused_test.setObjectName("CheckBox_AP_caller_was_refused_test")
        self.CheckBox_AP_no_answer_test = QtWidgets.QCheckBox(self.GroupBox_AP_test)
        self.CheckBox_AP_no_answer_test.setGeometry(QtCore.QRect(140, 480, 91, 19))
        self.CheckBox_AP_no_answer_test.setObjectName("CheckBox_AP_no_answer_test")
        self.Btn_AP_runTest = QtWidgets.QPushButton(self.GroupBox_AP_test)
        self.Btn_AP_runTest.setEnabled(True)
        self.Btn_AP_runTest.setGeometry(QtCore.QRect(10, 560, 120, 28))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Btn_AP_runTest.sizePolicy().hasHeightForWidth())
        self.Btn_AP_runTest.setSizePolicy(sizePolicy)
        self.Btn_AP_runTest.setMinimumSize(QtCore.QSize(0, 0))
        self.Btn_AP_runTest.setMaximumSize(QtCore.QSize(150, 16777215))
        self.Btn_AP_runTest.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Btn_AP_runTest.setObjectName("Btn_AP_runTest")
        self.Btn_AP_stopTest = QtWidgets.QPushButton(self.GroupBox_AP_test)
        self.Btn_AP_stopTest.setGeometry(QtCore.QRect(150, 560, 120, 28))
        self.Btn_AP_stopTest.setObjectName("Btn_AP_stopTest")
        self.Label_call_test_title = QtWidgets.QLabel(self.GroupBox_AP_test)
        self.Label_call_test_title.setGeometry(QtCore.QRect(10, 400, 81, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.Label_call_test_title.setFont(font)
        self.Label_call_test_title.setObjectName("Label_call_test_title")
        self.Label_AP_test_times = QtWidgets.QLabel(self.GroupBox_AP_test)
        self.Label_AP_test_times.setGeometry(QtCore.QRect(20, 520, 72, 25))
        self.Label_AP_test_times.setObjectName("Label_AP_test_times")
        self.LineEdit_AP_test_times = QtWidgets.QLineEdit(self.GroupBox_AP_test)
        self.LineEdit_AP_test_times.setGeometry(QtCore.QRect(110, 520, 90, 25))
        self.LineEdit_AP_test_times.setObjectName("LineEdit_AP_test_times")
        self.Label_func_test_title = QtWidgets.QLabel(self.GroupBox_AP_test)
        self.Label_func_test_title.setGeometry(QtCore.QRect(10, 110, 101, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.Label_func_test_title.setFont(font)
        self.Label_func_test_title.setObjectName("Label_func_test_title")
        self.CheckBox_WIFI_test = QtWidgets.QCheckBox(self.GroupBox_AP_test)
        self.CheckBox_WIFI_test.setGeometry(QtCore.QRect(140, 230, 121, 19))
        self.CheckBox_WIFI_test.setObjectName("CheckBox_WIFI_test")
        self.CheckBox_APP_startexit_test = QtWidgets.QCheckBox(self.GroupBox_AP_test)
        self.CheckBox_APP_startexit_test.setGeometry(QtCore.QRect(20, 270, 111, 19))
        self.CheckBox_APP_startexit_test.setObjectName("CheckBox_APP_startexit_test")
        self.CheckBox_Camera_test = QtWidgets.QCheckBox(self.GroupBox_AP_test)
        self.CheckBox_Camera_test.setGeometry(QtCore.QRect(140, 270, 111, 19))
        self.CheckBox_Camera_test.setObjectName("CheckBox_Camera_test")
        self.CheckBox_Contact_test = QtWidgets.QCheckBox(self.GroupBox_AP_test)
        self.CheckBox_Contact_test.setGeometry(QtCore.QRect(20, 310, 111, 19))
        self.CheckBox_Contact_test.setObjectName("CheckBox_Contact_test")
        self.CheckBox_OTA_test = QtWidgets.QCheckBox(self.GroupBox_AP_test)
        self.CheckBox_OTA_test.setGeometry(QtCore.QRect(140, 310, 111, 19))
        self.CheckBox_OTA_test.setObjectName("CheckBox_OTA_test")
        self.CheckBox_APKoper_test = QtWidgets.QCheckBox(self.GroupBox_AP_test)
        self.CheckBox_APKoper_test.setGeometry(QtCore.QRect(20, 350, 111, 19))
        self.CheckBox_APKoper_test.setObjectName("CheckBox_APKoper_test")
        self.CheckBox_APK_install_test = QtWidgets.QCheckBox(self.GroupBox_AP_test)
        self.CheckBox_APK_install_test.setGeometry(QtCore.QRect(140, 350, 141, 19))
        self.CheckBox_APK_install_test.setObjectName("CheckBox_APK_install_test")
        self.horizontalLayout_5.addWidget(self.GroupBox_AP_test)
        self.AP_verLayout_recv = QtWidgets.QVBoxLayout()
        self.AP_verLayout_recv.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.AP_verLayout_recv.setContentsMargins(10, 5, 10, 5)
        self.AP_verLayout_recv.setObjectName("AP_verLayout_recv")
        self.GroupBox_AP_recv = QtWidgets.QGroupBox(self.AP_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.GroupBox_AP_recv.sizePolicy().hasHeightForWidth())
        self.GroupBox_AP_recv.setSizePolicy(sizePolicy)
        self.GroupBox_AP_recv.setMinimumSize(QtCore.QSize(300, 0))
        self.GroupBox_AP_recv.setObjectName("GroupBox_AP_recv")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.GroupBox_AP_recv)
        self.verticalLayout_5.setContentsMargins(10, 5, 10, 5)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.TextBrowser_AP_recv = QtWidgets.QTextBrowser(self.GroupBox_AP_recv)
        self.TextBrowser_AP_recv.setMinimumSize(QtCore.QSize(300, 0))
        self.TextBrowser_AP_recv.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.TextBrowser_AP_recv.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.TextBrowser_AP_recv.setObjectName("TextBrowser_AP_recv")
        self.verticalLayout_5.addWidget(self.TextBrowser_AP_recv)
        self.AP_verLayout_recv.addWidget(self.GroupBox_AP_recv)
        self.horizontalLayout_5.addLayout(self.AP_verLayout_recv)
        self.AP_verLayout_right_2 = QtWidgets.QVBoxLayout()
        self.AP_verLayout_right_2.setObjectName("AP_verLayout_right_2")
        spacerItem = QtWidgets.QSpacerItem(0, 800, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.AP_verLayout_right_2.addItem(spacerItem)
        self.Btn_AP_clearBrowser = QtWidgets.QPushButton(self.AP_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(5)
        sizePolicy.setHeightForWidth(self.Btn_AP_clearBrowser.sizePolicy().hasHeightForWidth())
        self.Btn_AP_clearBrowser.setSizePolicy(sizePolicy)
        self.Btn_AP_clearBrowser.setObjectName("Btn_AP_clearBrowser")
        self.AP_verLayout_right_2.addWidget(self.Btn_AP_clearBrowser)
        self.horizontalLayout_5.addLayout(self.AP_verLayout_right_2)
        self.tabWidget.addTab(self.AP_2, "")
        self.CP_2 = QtWidgets.QWidget()
        self.CP_2.setObjectName("CP_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.CP_2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.GroupBox_CP_test = QtWidgets.QGroupBox(self.CP_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.GroupBox_CP_test.sizePolicy().hasHeightForWidth())
        self.GroupBox_CP_test.setSizePolicy(sizePolicy)
        self.GroupBox_CP_test.setMinimumSize(QtCore.QSize(240, 0))
        self.GroupBox_CP_test.setMaximumSize(QtCore.QSize(180, 16777215))
        self.GroupBox_CP_test.setObjectName("GroupBox_CP_test")
        self.Btn_at_exec = QtWidgets.QPushButton(self.GroupBox_CP_test)
        self.Btn_at_exec.setGeometry(QtCore.QRect(40, 220, 140, 25))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Btn_at_exec.sizePolicy().hasHeightForWidth())
        self.Btn_at_exec.setSizePolicy(sizePolicy)
        self.Btn_at_exec.setObjectName("Btn_at_exec")
        self.Label_port_check = QtWidgets.QLabel(self.GroupBox_CP_test)
        self.Label_port_check.setGeometry(QtCore.QRect(20, 10, 61, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Label_port_check.sizePolicy().hasHeightForWidth())
        self.Label_port_check.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(9)
        self.Label_port_check.setFont(font)
        self.Label_port_check.setObjectName("Label_port_check")
        self.Btn_port_close = QtWidgets.QPushButton(self.GroupBox_CP_test)
        self.Btn_port_close.setGeometry(QtCore.QRect(120, 140, 90, 25))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Btn_port_close.sizePolicy().hasHeightForWidth())
        self.Btn_port_close.setSizePolicy(sizePolicy)
        self.Btn_port_close.setObjectName("Btn_port_close")
        self.Label_port_select = QtWidgets.QLabel(self.GroupBox_CP_test)
        self.Label_port_select.setGeometry(QtCore.QRect(20, 50, 61, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Label_port_select.sizePolicy().hasHeightForWidth())
        self.Label_port_select.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(9)
        self.Label_port_select.setFont(font)
        self.Label_port_select.setObjectName("Label_port_select")
        self.Btn_port_open = QtWidgets.QPushButton(self.GroupBox_CP_test)
        self.Btn_port_open.setGeometry(QtCore.QRect(20, 140, 90, 25))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Btn_port_open.sizePolicy().hasHeightForWidth())
        self.Btn_port_open.setSizePolicy(sizePolicy)
        self.Btn_port_open.setObjectName("Btn_port_open")
        self.ComboBox_port_select = QtWidgets.QComboBox(self.GroupBox_CP_test)
        self.ComboBox_port_select.setGeometry(QtCore.QRect(110, 60, 90, 25))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ComboBox_port_select.sizePolicy().hasHeightForWidth())
        self.ComboBox_port_select.setSizePolicy(sizePolicy)
        self.ComboBox_port_select.setObjectName("ComboBox_port_select")
        self.Btn_port_check = QtWidgets.QPushButton(self.GroupBox_CP_test)
        self.Btn_port_check.setGeometry(QtCore.QRect(110, 20, 90, 25))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Btn_port_check.sizePolicy().hasHeightForWidth())
        self.Btn_port_check.setSizePolicy(sizePolicy)
        self.Btn_port_check.setObjectName("Btn_port_check")
        self.Label_baudrate = QtWidgets.QLabel(self.GroupBox_CP_test)
        self.Label_baudrate.setGeometry(QtCore.QRect(20, 90, 61, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Label_baudrate.sizePolicy().hasHeightForWidth())
        self.Label_baudrate.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(9)
        self.Label_baudrate.setFont(font)
        self.Label_baudrate.setObjectName("Label_baudrate")
        self.ComboBox_baudrate = QtWidgets.QComboBox(self.GroupBox_CP_test)
        self.ComboBox_baudrate.setGeometry(QtCore.QRect(110, 100, 90, 25))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ComboBox_baudrate.sizePolicy().hasHeightForWidth())
        self.ComboBox_baudrate.setSizePolicy(sizePolicy)
        self.ComboBox_baudrate.setObjectName("ComboBox_baudrate")
        self.ComboBox_baudrate.addItem("")
        self.ComboBox_baudrate.addItem("")
        self.ComboBox_baudrate.addItem("")
        self.ComboBox_baudrate.addItem("")
        self.ComboBox_baudrate.addItem("")
        self.ComboBox_baudrate.addItem("")
        self.ComboBox_baudrate.addItem("")
        self.ComboBox_baudrate.addItem("")
        self.ComboBox_baudrate.addItem("")
        self.ComboBox_baudrate.addItem("")
        self.ComboBox_baudrate.addItem("")
        self.ComboBox_baudrate.addItem("")
        self.Label_at_select = QtWidgets.QLabel(self.GroupBox_CP_test)
        self.Label_at_select.setGeometry(QtCore.QRect(20, 180, 54, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Label_at_select.sizePolicy().hasHeightForWidth())
        self.Label_at_select.setSizePolicy(sizePolicy)
        self.Label_at_select.setObjectName("Label_at_select")
        self.ComboBox_at_select = QtWidgets.QComboBox(self.GroupBox_CP_test)
        self.ComboBox_at_select.setGeometry(QtCore.QRect(80, 180, 120, 25))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ComboBox_at_select.sizePolicy().hasHeightForWidth())
        self.ComboBox_at_select.setSizePolicy(sizePolicy)
        self.ComboBox_at_select.setObjectName("ComboBox_at_select")
        self.Btn_CP_runTest = QtWidgets.QPushButton(self.GroupBox_CP_test)
        self.Btn_CP_runTest.setGeometry(QtCore.QRect(10, 530, 100, 25))
        self.Btn_CP_runTest.setObjectName("Btn_CP_runTest")
        self.Btn_CP_stopTest = QtWidgets.QPushButton(self.GroupBox_CP_test)
        self.Btn_CP_stopTest.setGeometry(QtCore.QRect(130, 530, 100, 25))
        self.Btn_CP_stopTest.setObjectName("Btn_CP_stopTest")
        self.CheckBox_CP_caller_hang_up_test = QtWidgets.QRadioButton(self.GroupBox_CP_test)
        self.CheckBox_CP_caller_hang_up_test.setGeometry(QtCore.QRect(20, 320, 219, 19))
        self.CheckBox_CP_caller_hang_up_test.setObjectName("CheckBox_CP_caller_hang_up_test")
        self.CheckBox_CP_caller_was_hang_up_test = QtWidgets.QRadioButton(self.GroupBox_CP_test)
        self.CheckBox_CP_caller_was_hang_up_test.setGeometry(QtCore.QRect(20, 360, 219, 19))
        self.CheckBox_CP_caller_was_hang_up_test.setObjectName("CheckBox_CP_caller_was_hang_up_test")
        self.CheckBox_CP_no_answer_test = QtWidgets.QRadioButton(self.GroupBox_CP_test)
        self.CheckBox_CP_no_answer_test.setGeometry(QtCore.QRect(20, 440, 219, 19))
        self.CheckBox_CP_no_answer_test.setObjectName("CheckBox_CP_no_answer_test")
        self.CheckBox_CP_caller_was_refused_test = QtWidgets.QRadioButton(self.GroupBox_CP_test)
        self.CheckBox_CP_caller_was_refused_test.setGeometry(QtCore.QRect(20, 400, 219, 19))
        self.CheckBox_CP_caller_was_refused_test.setObjectName("CheckBox_CP_caller_was_refused_test")
        self.Label_CP_test_times = QtWidgets.QLabel(self.GroupBox_CP_test)
        self.Label_CP_test_times.setGeometry(QtCore.QRect(20, 480, 60, 25))
        self.Label_CP_test_times.setObjectName("Label_CP_test_times")
        self.LineEdit_CP_test_times = QtWidgets.QLineEdit(self.GroupBox_CP_test)
        self.LineEdit_CP_test_times.setGeometry(QtCore.QRect(100, 480, 90, 25))
        self.LineEdit_CP_test_times.setObjectName("LineEdit_CP_test_times")
        self.Label_CP_calling_test_title = QtWidgets.QLabel(self.GroupBox_CP_test)
        self.Label_CP_calling_test_title.setGeometry(QtCore.QRect(10, 280, 72, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.Label_CP_calling_test_title.setFont(font)
        self.Label_CP_calling_test_title.setObjectName("Label_CP_calling_test_title")
        self.horizontalLayout_3.addWidget(self.GroupBox_CP_test)
        self.verticalLayout_CP_recv = QtWidgets.QVBoxLayout()
        self.verticalLayout_CP_recv.setObjectName("verticalLayout_CP_recv")
        self.GroupBox_CP_recv = QtWidgets.QGroupBox(self.CP_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(9)
        sizePolicy.setVerticalStretch(6)
        sizePolicy.setHeightForWidth(self.GroupBox_CP_recv.sizePolicy().hasHeightForWidth())
        self.GroupBox_CP_recv.setSizePolicy(sizePolicy)
        self.GroupBox_CP_recv.setObjectName("GroupBox_CP_recv")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.GroupBox_CP_recv)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.TextBrowser_CP_recv = QtWidgets.QTextBrowser(self.GroupBox_CP_recv)
        self.TextBrowser_CP_recv.setObjectName("TextBrowser_CP_recv")
        self.verticalLayout_8.addWidget(self.TextBrowser_CP_recv)
        self.verticalLayout_CP_recv.addWidget(self.GroupBox_CP_recv)
        self.GroupBox_CP_send = QtWidgets.QGroupBox(self.CP_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.GroupBox_CP_send.sizePolicy().hasHeightForWidth())
        self.GroupBox_CP_send.setSizePolicy(sizePolicy)
        self.GroupBox_CP_send.setObjectName("GroupBox_CP_send")
        self.gridLayout = QtWidgets.QGridLayout(self.GroupBox_CP_send)
        self.gridLayout.setObjectName("gridLayout")
        self.TextBrowser_CP_send = QtWidgets.QTextEdit(self.GroupBox_CP_send)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TextBrowser_CP_send.sizePolicy().hasHeightForWidth())
        self.TextBrowser_CP_send.setSizePolicy(sizePolicy)
        self.TextBrowser_CP_send.setObjectName("TextBrowser_CP_send")
        self.gridLayout.addWidget(self.TextBrowser_CP_send, 0, 0, 1, 1)
        self.verticalLayout_CP_recv.addWidget(self.GroupBox_CP_send)
        self.horizontalLayout_3.addLayout(self.verticalLayout_CP_recv)
        self.CP_verLayout_right_2 = QtWidgets.QVBoxLayout()
        self.CP_verLayout_right_2.setObjectName("CP_verLayout_right_2")
        spacerItem1 = QtWidgets.QSpacerItem(0, 400, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.CP_verLayout_right_2.addItem(spacerItem1)
        self.Btn_CP_clear_recvBrowser = QtWidgets.QPushButton(self.CP_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(5)
        sizePolicy.setHeightForWidth(self.Btn_CP_clear_recvBrowser.sizePolicy().hasHeightForWidth())
        self.Btn_CP_clear_recvBrowser.setSizePolicy(sizePolicy)
        self.Btn_CP_clear_recvBrowser.setObjectName("Btn_CP_clear_recvBrowser")
        self.CP_verLayout_right_2.addWidget(self.Btn_CP_clear_recvBrowser)
        spacerItem2 = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.CP_verLayout_right_2.addItem(spacerItem2)
        self.Btn_CP_send = QtWidgets.QPushButton(self.CP_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(5)
        sizePolicy.setHeightForWidth(self.Btn_CP_send.sizePolicy().hasHeightForWidth())
        self.Btn_CP_send.setSizePolicy(sizePolicy)
        self.Btn_CP_send.setObjectName("Btn_CP_send")
        self.CP_verLayout_right_2.addWidget(self.Btn_CP_send)
        self.Btn_CP_clear_sendEdit = QtWidgets.QPushButton(self.CP_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(5)
        sizePolicy.setHeightForWidth(self.Btn_CP_clear_sendEdit.sizePolicy().hasHeightForWidth())
        self.Btn_CP_clear_sendEdit.setSizePolicy(sizePolicy)
        self.Btn_CP_clear_sendEdit.setObjectName("Btn_CP_clear_sendEdit")
        self.CP_verLayout_right_2.addWidget(self.Btn_CP_clear_sendEdit)
        self.horizontalLayout_3.addLayout(self.CP_verLayout_right_2)
        self.tabWidget.addTab(self.CP_2, "")
        self.horizontalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 976, 26))
        self.menubar.setObjectName("menubar")
        self.Menu_ATmgr = QtWidgets.QMenu(self.menubar)
        self.Menu_ATmgr.setObjectName("Menu_ATmgr")

        self.Menu_Settings = QtWidgets.QMenu(self.menubar)
        self.Menu_Settings.setObjectName("Menu_Settings")

        self.Menu_Atmgr_action = QtWidgets.QAction(MainWindow)
        self.Menu_Atmgr_action.setObjectName("AtmgrAction")

        self.settings_action = QtWidgets.QAction(MainWindow)
        self.settings_action.setObjectName("settingsAction")

        self.Menu_ATmgr.addAction(self.Menu_Atmgr_action)
        self.Menu_Settings.addAction(self.settings_action)

        self.menubar.addAction(self.Menu_Settings.menuAction())
        self.menubar.addAction(self.Menu_Settings.menuAction())
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Label_dev_check.setText(_translate("MainWindow", "设备检测"))
        self.Btn_dev_check.setText(_translate("MainWindow", "设备检测"))
        self.CheckBox_SIM_test.setStatusTip(_translate("MainWindow", "检测SIM卡状态"))
        self.CheckBox_SIM_test.setText(_translate("MainWindow", "SIM卡检测"))
        self.CheckBox_reboot_test.setStatusTip(_translate("MainWindow", "开关机重启"))
        self.CheckBox_reboot_test.setText(_translate("MainWindow", "开关机测试"))
        self.Label_dev_select.setText(_translate("MainWindow", "设备选择"))
        self.CheckBox_SDcard_test.setStatusTip(_translate("MainWindow", "检测SD卡状态"))
        self.CheckBox_SDcard_test.setText(_translate("MainWindow", "SD卡检测"))
        self.CheckBox_BT_test.setText(_translate("MainWindow", "蓝牙开关测试"))
        self.CheckBox_GPS_test.setText(_translate("MainWindow", "GPS开关测试"))
        self.CheckBox_AP_caller_hang_up_test.setStatusTip(_translate("MainWindow", "主叫对端，接通后，主动挂断"))
        self.CheckBox_AP_caller_hang_up_test.setText(_translate("MainWindow", "主叫主挂"))
        self.CheckBox_AP_caller_was_hang_up_test.setStatusTip(_translate("MainWindow", "主叫对端，接通后，对端挂断"))
        self.CheckBox_AP_caller_was_hang_up_test.setText(_translate("MainWindow", "主叫被挂"))
        self.CheckBox_AP_caller_was_refused_test.setStatusTip(_translate("MainWindow", "主叫对端，对端拒接"))
        self.CheckBox_AP_caller_was_refused_test.setText(_translate("MainWindow", "主叫拒接"))
        self.CheckBox_AP_no_answer_test.setStatusTip(_translate("MainWindow", "主叫对端，对端未接听，直至超时挂断"))
        self.CheckBox_AP_no_answer_test.setText(_translate("MainWindow", "主叫未接"))
        self.Btn_AP_runTest.setStatusTip(_translate("MainWindow", "测试项：{}   测试次数：{}"))
        self.Btn_AP_runTest.setText(_translate("MainWindow", "开始测试"))
        self.Btn_AP_runTest.setProperty("setAlignment", _translate("MainWindow", "Qt.AlignCenter"))
        self.Btn_AP_stopTest.setStatusTip(_translate("MainWindow", "当前测试完成后结束测试"))
        self.Btn_AP_stopTest.setText(_translate("MainWindow", "停止测试"))
        self.Label_call_test_title.setText(_translate("MainWindow", "通话测试"))
        self.Label_AP_test_times.setText(_translate("MainWindow", "测试次数:"))
        self.Label_func_test_title.setText(_translate("MainWindow", "功能项测试"))
        self.CheckBox_WIFI_test.setText(_translate("MainWindow", "WIFI开关测试"))
        self.CheckBox_APP_startexit_test.setText(_translate("MainWindow", "APP启动退出"))
        self.CheckBox_Camera_test.setText(_translate("MainWindow", "Camera测试"))
        self.CheckBox_Contact_test.setText(_translate("MainWindow", "联系人测试"))
        self.CheckBox_OTA_test.setText(_translate("MainWindow", "OTA压测"))
        self.CheckBox_APKoper_test.setText(_translate("MainWindow", "APK测试"))
        self.CheckBox_APK_install_test.setText(_translate("MainWindow", "APK安装卸载测试"))
        self.GroupBox_AP_recv.setTitle(_translate("MainWindow", "接收区"))
        self.TextBrowser_AP_recv.setProperty("align", _translate("MainWindow", "center"))
        self.Btn_AP_clearBrowser.setStatusTip(_translate("MainWindow", "清除接收区内容"))
        self.Btn_AP_clearBrowser.setText(_translate("MainWindow", "清除"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.AP_2), _translate("MainWindow", "AP"))
        self.GroupBox_CP_test.setTitle(_translate("MainWindow", "串口状态"))
        self.Btn_at_exec.setText(_translate("MainWindow", "执行"))
        self.Label_port_check.setText(_translate("MainWindow", "串口检测"))
        self.Btn_port_close.setText(_translate("MainWindow", "关闭串口"))
        self.Label_port_select.setText(_translate("MainWindow", "串口选择"))
        self.Btn_port_open.setText(_translate("MainWindow", "打开串口"))
        self.ComboBox_port_select.setStatusTip(_translate("MainWindow", "显示当前选择的串口"))
        self.Btn_port_check.setStatusTip(_translate("MainWindow", "检测当前连接PC的串口"))
        self.Btn_port_check.setText(_translate("MainWindow", "检测串口"))
        self.Label_baudrate.setText(_translate("MainWindow", "波特率"))
        self.ComboBox_baudrate.setStatusTip(_translate("MainWindow", "显示当前选择的波特率"))
        self.ComboBox_baudrate.setItemText(0, _translate("MainWindow", "115200"))
        self.ComboBox_baudrate.setItemText(1, _translate("MainWindow", "1200"))
        self.ComboBox_baudrate.setItemText(2, _translate("MainWindow", "2400"))
        self.ComboBox_baudrate.setItemText(3, _translate("MainWindow", "4800"))
        self.ComboBox_baudrate.setItemText(4, _translate("MainWindow", "9600"))
        self.ComboBox_baudrate.setItemText(5, _translate("MainWindow", "14400"))
        self.ComboBox_baudrate.setItemText(6, _translate("MainWindow", "19200"))
        self.ComboBox_baudrate.setItemText(7, _translate("MainWindow", "38400"))
        self.ComboBox_baudrate.setItemText(8, _translate("MainWindow", "56000"))
        self.ComboBox_baudrate.setItemText(9, _translate("MainWindow", "57600"))
        self.ComboBox_baudrate.setItemText(10, _translate("MainWindow", "128000"))
        self.ComboBox_baudrate.setItemText(11, _translate("MainWindow", "256000"))
        self.Label_at_select.setText(_translate("MainWindow", "AT指令"))
        self.ComboBox_at_select.setStatusTip(_translate("MainWindow", "显示当前准备发送的AT指令"))
        self.Btn_CP_runTest.setStatusTip(_translate("MainWindow", "测试项：{}   测试次数：{}"))
        self.Btn_CP_runTest.setText(_translate("MainWindow", "开始"))
        self.Btn_CP_stopTest.setStatusTip(_translate("MainWindow", "当前测试完成后结束测试"))
        self.Btn_CP_stopTest.setText(_translate("MainWindow", "停止"))
        self.CheckBox_CP_caller_hang_up_test.setStatusTip(_translate("MainWindow", "主叫对端，接通后，主动挂断"))
        self.CheckBox_CP_caller_hang_up_test.setText(_translate("MainWindow", "主叫主挂"))
        self.CheckBox_CP_caller_was_hang_up_test.setStatusTip(_translate("MainWindow", "主叫对端，接通后，对端挂断"))
        self.CheckBox_CP_caller_was_hang_up_test.setText(_translate("MainWindow", "主叫被挂"))
        self.CheckBox_CP_no_answer_test.setStatusTip(_translate("MainWindow", "主叫对端，对端未接听，直至超时挂断"))
        self.CheckBox_CP_no_answer_test.setText(_translate("MainWindow", "主叫未接"))
        self.CheckBox_CP_caller_was_refused_test.setStatusTip(_translate("MainWindow", "主叫对端，对端拒接"))
        self.CheckBox_CP_caller_was_refused_test.setText(_translate("MainWindow", "主叫拒接"))
        self.Label_CP_test_times.setText(_translate("MainWindow", "测试次数"))
        self.Label_CP_calling_test_title.setText(_translate("MainWindow", "通话测试"))
        self.GroupBox_CP_recv.setTitle(_translate("MainWindow", "接收区"))
        self.GroupBox_CP_send.setTitle(_translate("MainWindow", "发送区"))
        self.Btn_CP_clear_recvBrowser.setStatusTip(_translate("MainWindow", "清除接收区内容"))
        self.Btn_CP_clear_recvBrowser.setText(_translate("MainWindow", "清除"))
        self.Btn_CP_send.setStatusTip(_translate("MainWindow", "发送AT指令"))
        self.Btn_CP_send.setText(_translate("MainWindow", "发送"))
        self.Btn_CP_send.setShortcut(_translate("MainWindow", "Return"))
        self.Btn_CP_clear_sendEdit.setStatusTip(_translate("MainWindow", "清除发送区内容"))
        self.Btn_CP_clear_sendEdit.setText(_translate("MainWindow", "清除"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.CP_2), _translate("MainWindow", "CP"))
        self.Menu_ATmgr.setTitle(_translate("MainWindow", "设置"))
        self.Menu_Settings.setTitle(_translate("MainWindow", "AT指令"))
