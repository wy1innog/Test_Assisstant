import re
import subprocess
import sys
import serial
import yaml
from PyQt5.QtCore import QTimer

from serial import SerialException

import Word
from ui.mainUI import Ui_MainWindow

sys.path.append("..")
from common.log import Log

# from ui.main import Ui_MainWindow

# WIN32 API
IS_WIN32 = 'win32' in str(sys.platform).lower()


class Normal_func(Ui_MainWindow):
    log = Log(__name__).getlog()

    def __init__(self):
        self.log = Log(__name__).getlog()
        self.ser = self.getSer()
        self.process = []
        self.RECV_FLAG = True

    def getSer(self):
        self.ser = serial.Serial()
        self.ser.baudrate = 115200
        return self.ser

    def exec_cmd(self, cmd):
        """
        执行AT指令
        :param cmd: AT指令
        """
        cmd = (cmd + '\r\n').encode('utf-8')
        try:
            print("exec_cmd:", self.ser)
            self.ser.write(cmd)
            return 1
        except SerialException:
            return 0

    @classmethod
    def getBeTestCaseTitle(cls):
        casetitle = []
        for case in Word.be_testcase:
            casetitle.append(case['title'])
        return casetitle

    def port_open(self):
        self.ser.setPort(self.ComboBox_port_select.currentText())

        try:
            self.ser.open()
            self.Btn_port_open.setEnabled(False)
            self.Btn_port_close.setEnabled(True)
            self.GroupBox_CP_test.setTitle("串口状态(%s)" % self.ser.port)
            self.log.info(self.ser)
        except:
            # QMessageBox.critical( "Port Error", "此串口不能被打开！")
            self.log.warning("此串口不能被打开")

    def port_close(self):
        """
        CP 关闭串口
        :return:
        """
        try:
            self.log.info(self.ser)

            self.ser.close()
            self.log.info("串口已关闭")
        except:
            pass
        self.Btn_port_open.setEnabled(True)
        self.Btn_port_close.setEnabled(False)
        self.GroupBox_CP_test.setTitle("串口状态（已关闭）")







    @classmethod
    def network_check(self):
        # todo:入网
        pass

    @classmethod
    def subprocess_getoutput(cls, cmd):
        # also works for Popen. It creates a new *hidden* window, so it will work in frozen apps (.exe).
        if IS_WIN32:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags = subprocess.CREATE_NEW_CONSOLE | subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            # kwargs['startupinfo'] = startupinfo
        retcode = subprocess.getoutput(cmd)
        return retcode

    @classmethod
    def subprocess_call(cls, *args, **kwargs):
        # also works for Popen. It creates a new *hidden* window, so it will work in frozen apps (.exe).
        if IS_WIN32:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags = subprocess.CREATE_NEW_CONSOLE | subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            kwargs['startupinfo'] = startupinfo
        retcode = subprocess.call(*args, **kwargs)
        return retcode

    def getDev(self):
        """
        检测设备，有设备，返回设备名；无设备，返回0
        :return: 设备名
        :return: 0
        """
        pattern = re.compile('[a-zA-Z0-9]+\sdevice$')
        devices_list = self.subprocess_getoutput('adb devices').strip().split('\n')
        devName = devices_list[-1].split('\t')[0]
        devices_count = 0
        for d in devices_list:
            r = pattern.match(d)
            if r:
                devices_count += 1
        if devices_count == 0:
            return 0
        elif devices_count == 1:
            return devName
        else:
            return 2

    # def recv_to_bottom(self):
    #     # 获取到text光标
    #     textCursor = CP_recv_textBrowser.textCursor()
    #     # 滚动到底部
    #     textCursor.movePosition(textCursor.End)
    #     # 设置光标到text中
    #     self.CP_recv_textBrowser.setTextCursor(textCursor)
    @classmethod
    def getConfig(cls) -> dict:
        # 获取配置
        with open('config/config.yml', 'r', encoding='utf-8') as f:
            content = yaml.load(f.read(), yaml.FullLoader)
            return content

    @classmethod
    def number_check(self, words):
        if words.isdigit() == True:
            tmp = int(words)
            if tmp > 0:
                return True
            else:
                pass
        else:
            return False

