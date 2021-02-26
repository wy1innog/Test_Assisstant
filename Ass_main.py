# coding=utf-8
import os
import re
import sys
import time
import json
from json import JSONDecodeError
import threading
import serial
import datetime
import serial.tools.list_ports
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog, QComboBox
from PyQt5.QtCore import QTimer
import logging.config

from Tab_AP import AP
from Tab_CP import CP
from common.Ass_util import subprocess_getoutput

parent_path = os.path.dirname(sys.path[0])
if parent_path not in sys.path:
    sys.path.append(parent_path)

from ui.main_ui import Ui_MainWindow
from at_settings import At_settings
from default_settings import Default_settings
from common.log import Log



class Ass(QMainWindow, QComboBox, Ui_MainWindow):
    config_path = 'config/config.cfg'

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.log = Log(__name__).getlog()
        self.ap = AP()
        self.cp = CP()
        self.initUI()
        # self.port_check()
        # self.process = []
        # self.RECV_FLAG = True
        # self.TEST_FLAG = False
        # self.NETWORK_REGISTERED = False


    def initUI(self):
        self.setWindowTitle("Test Assistant")
        icon = 'img\icon.ico'
        self.setWindowIcon(QIcon(icon))
        self.actionAT_manager.triggered.connect(CP.refresh_at_combobox)

        # self.btn_dev_check.clicked.connect(self.ap.dev_check)
        self.btn_dev_check.clicked.connect(AP.dev_check)
        self.btn_btStatus.clicked.connect(self.ap.bt_status)
        self.btn_wifiStatus.clicked.connect(self.ap.wifi_status)
        self.btn_wifiInfo.clicked.connect(self.ap.wifi_info)
        self.btn_simStatus.clicked.connect(self.ap.sim_status)
        self.btn_sdStatus.clicked.connect(self.ap.sdcard_status)
        self.btn_listPkg.clicked.connect(self.ap.list_package)
        self.btn_catchLog.clicked.connect(self.ap.get_locallog)
        self.btn_run_test_ap.clicked.connect(self.ap.run_test_choice_ap)
        self.btn_stop_test_ap.clicked.connect(self.ap.stop_test_ap)
        self.AP_btn_clear_recv.clicked.connect(self.ap.ap_clear_recv)
        self.AP_btn_start.clicked.connect(self.ap.dial)
        self.AP_btn_clear_send.clicked.connect(self.ap.ap_clear_send)

        self.btn_sp_check.clicked.connect(self.cp.port_check)
        self.btn_sp_open.clicked.connect(self.cp.port_open)
        self.btn_sp_close.clicked.connect(self.cp.port_close)
        self.btn_at_exec.clicked.connect(self.cp.exec_choose_at)

        self.btn_run_test.clicked.connect(self.cp.run_test_choice_cp)
        self.btn_stop_test.clicked.connect(self.cp.stop_test_cp)
        self.CP_btn_start.clicked.connect(self.cp.data_send)
        self.CP_btn_clear_recv.clicked.connect(self.cp.cp_clear_recv)
        self.CP_btn_clear_send.clicked.connect(self.cp.cp_clear_send)

    def widgetAppend(self, widget, message):
        var = self.widget
        var.append("message")

if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)

    et = Ass()

    dsa = At_settings()
    ds = Default_settings()
    btn = et.actionAT_manager.triggered.connect(dsa.show)
    btn1 = et.actionDefSet.triggered.connect(ds.show)
    et.show()

    sys.exit(app.exec_())
