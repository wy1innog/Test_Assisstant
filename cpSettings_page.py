import os
import re
import sys

import psutil
import serial
import serial.tools.list_ports
import yaml
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog
sys.coinit_flags = 2
from pywinauto import MatchError, application, keyboard

import Word
from ui.cpSettingsUI import Ui_Dialog
from common.DialogUtil import showEmptyMessageBox


class CP_settings(Ui_Dialog, QDialog):
    # 让多窗口之间传递信号，刷新主窗口信息
    my_Signal = QtCore.pyqtSignal(str)
    config_path = Word.config_path

    def __init__(self):
        super(Ui_Dialog, self).__init__()
        self.setupUi(self)
        self.log = Word.log[0]
        icon = 'D:\\ihblu\\wyrepo\\Test_Assistant\\img\\icon.ico'
        self.setWindowIcon(QIcon(icon))
        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        # self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.init()

    def init(self):
        self.Btn_settings_save.clicked.connect(self.__write_config)
        self.Btn_settings_save.clicked.connect(self.close)
        self.Btn_settings_cancel.clicked.connect(self.close)
        self.Btn_TT_browse.clicked.connect(self.TT_browse)
        self.Btn_Trace_browse.clicked.connect(self.Trace_browse)
        self.Btn_refresh_port.clicked.connect(self.port_check)


    def sendEditContent(self):
        content = '1'
        self.my_Signal.emit(content)

    def closeEvent(self, event):
        self.sendEditContent()

    def TT_browse(self):
        config_cptest = self.getCpTestConfig()
        if config_cptest:
            m = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件", config_cptest['TT_path'], "*.exe")
        else:
            m = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件", "C:/", "*.exe")
        self.Ledit_TT_path.setText(m[0])

    def Trace_browse(self):
        config_cptest = self.getCpTestConfig()
        if config_cptest:
            m = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件", config_cptest['Trace_path'], "*.exe")
        else:
            m = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件", "C:/", "*.exe")
        self.Ledit_Trace_path.setText(m[0])




    def __write_config(self):
        with open(self.config_path, 'r', encoding='utf-8') as f:
            content = yaml.load(f.read(), yaml.FullLoader)
            if self.RadioBtn_TT_on.isChecked() or self.RadioBtn_Trace_on.isChecked():
                try:
                    content['CP_test']['TT_path'] = self.Ledit_TT_path.text()
                    content['CP_test']['Trace_path'] = self.Ledit_Trace_path.text()
                    useCOM = re.search(r'COM\d+', self.ComboBox_serial_port.currentText()).group(0)
                    content['CP_test']['useCOM'] = useCOM
                except (AttributeError, UnboundLocalError):
                    showEmptyMessageBox("COM未选择")
                    self.RadioBtn_TT_off.setChecked()
                    self.RadioBtn_Trace_off.setChecked()
            else:
                try:
                    content['CP_test']['TT_path'] = self.Ledit_TT_path.text()
                    content['CP_test']['Trace_path'] = self.Ledit_Trace_path.text()
                    useCOM = re.search(r'COM\d+', self.ComboBox_serial_port.currentText()).group(0)
                    content['CP_test']['useCOM'] = useCOM
                except Exception:
                    pass

            if self.RadioBtn_TT_on.isChecked():
                content['CP_test']['TTlog'] = True
            else:
                content['CP_test']['TTlog'] = False

            if self.RadioBtn_Trace_on.isChecked():
                content['CP_test']['Tracelog'] = True
            else:
                content['CP_test']['Tracelog'] = False
            if self.RadioBtn_failAutoStop_on.isChecked():
                content['CP_test']['FailAutoStop'] = True
            else:
                content['CP_test']['FailAutoStop'] = False

        with open(self.config_path, 'w', encoding='utf-8') as wf:
            yaml.dump(content, wf, Dumper=yaml.SafeDumper)
        self.log.debug("write CP config, TT path: %s\nTrace path: %s\nCOM: %s" %
                      (self.Ledit_TT_path.text(), self.Ledit_Trace_path.text(),
                       self.ComboBox_serial_port.currentText()))

        # 连接TT
        if self.RadioBtn_TT_on.isChecked() and self.Ledit_TT_path.text() != '':
            self.log.debug("connect TT")
            self.connectTT()
        elif self.RadioBtn_TT_on.isChecked() and self.Ledit_TT_path.text() == '':
            showEmptyMessageBox("未填写TT.exe路径")
        if self.RadioBtn_Trace_on.isChecked() and self.Ledit_Trace_path.text() != '':
            self.log.debug("connect Trace")
            self.connectTrace()
        elif self.RadioBtn_Trace_on.isChecked() and self.Ledit_Trace_path.text() == '':
            showEmptyMessageBox("未填写Trace.exe路径")

        elif self.RadioBtn_TT_off.isChecked():
            pass
        elif self.RadioBtn_Trace_off.isChecked():
            pass
        else:
            showEmptyMessageBox("something wrong")

    def port_check(self):
        """
        CP 检测连接log的端口
        :return: None
        """
        self.Com_Dict = {}
        port_list = list(serial.tools.list_ports.comports())
        self.ComboBox_serial_port.clear()
        for port in port_list:
            res = ' '.join(port.description.split(' ')[1:])
            self.ComboBox_serial_port.addItem(res)

        self.log.debug("Port list:%s" % self.Com_Dict)
        if len(self.Com_Dict) == 0:
            self.ComboBox_serial_port.setCurrentText("无串口")

    def getCpTestConfig(self):

        with open(self.config_path, 'r', encoding='utf-8') as f:
            content = yaml.load(f.read(), yaml.FullLoader)
            return content['CP_test']

    def connectTT(self):
        cp_test_config = self.getCpTestConfig()
        TTpath = cp_test_config['TT_path']
        ProcessName = TTpath.split('/')[-1]
        self.log.debug("Process name: {}".format(ProcessName))
        self.checkProcess(ProcessName)
        os.environ.update({"__COMPAT_LAYER": "RUnAsInvoker"})
        try:
            app = application.Application(backend='uia').start(TTpath, timeout=5)
            wind_1 = app['Leadcore TT']
            wind_1.wait("active", timeout=5)
            keyboard.send_keys('^n')
            keyboard.send_keys('{ENTER}')

            wind_2 = wind_1['连接配置']
            wind_2.child_window(class_name="Edit", found_index=1).set_text(cp_test_config['useCOM'])
            wind_2.child_window(title='确定').click()
        except MatchError:
            showEmptyMessageBox("请勿进行手动操作")

    def connectTrace(self):
        cp_test_config = self.getCpTestConfig()
        TracePath = cp_test_config['Trace_path']
        ProcessName = TracePath.split('/')[-1]
        self.log.debug("Process name: {}".format(ProcessName))
        self.checkProcess(ProcessName)
        os.environ.update({"__COMPAT_LAYER": "RUnAsInvoker"})
        try:
            app = application.Application(backend='uia').start(TracePath, timeout=5)
            wind_1 = app['Trace - [Exception]']
            wind_1.wait("active", timeout=5)
            keyboard.send_keys('{ENTER}')

            xtpBarTop = wind_1.child_window(title="xtpBarTop")
            xtpBarTop.child_window(title="Config", control_type="Button").click()
        except MatchError:
            showEmptyMessageBox("请勿进行手动操作")

    def checkProcess(self, ProcessName):
        pids = psutil.process_iter()
        for pid in pids:
            if (pid.name() == ProcessName):
                self.log.debug("{} exists, pid: {}".format(ProcessName, pid.pid))
                pid.terminate()
                self.log.debug("{} is terminal".format(pid.name()))
