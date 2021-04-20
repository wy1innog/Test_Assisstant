import re
import subprocess
import sys
import time

import psutil
import serial
import yaml

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
        # self.RECV_FLAG = True

    def getSer(self):
        self.ser = serial.Serial()
        self.ser.baudrate = 115200
        return self.ser

    @classmethod
    def getBeTestCaseTitle(cls):
        casetitle = []
        for case in Word.be_testcase:
            casetitle.append(case['title'])
        return casetitle

    @classmethod
    def clearTestStatus(self):
        Word.testcase_sum = 0
        Word.waittest_testcase = 0
        Word.already_testcase = 0
        Word.pass_case = 0
        Word.fail_case = 0

    def port_open(self):
        Word.ser.setPort(self.ComboBox_port_select.currentText())

        try:
            if Word.ser.is_open:
                pass
            else:
                Word.ser.open()
            self.exec_cmd("AT^DSCI=1")
            self.Btn_port_open.setEnabled(False)
            self.Btn_port_close.setEnabled(True)
            self.GroupBox_CP_test.setTitle("串口状态(%s)" % Word.ser.port)
            self.log.info("ser is open: %s" % Word.ser)

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

    def exec_cmd(self, cmd):
        """
        执行AT指令
        :param cmd: AT指令
        """
        cmd = (cmd + '\r\n').encode('utf-8')
        try:
            Word.ser.write(cmd)
            self.log.debug("exec cmd: {}".format(cmd))
            return 1
        except serial.SerialException:
            return 0

    @classmethod
    def network_check(self):
        # todo:入网检测
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

    @classmethod
    def case_to_func(cls, case):
        cp_case_func_dict = {
            '主叫主挂': 'test_calling_to_answer',
            '主叫被挂': 'test_caller_hangs_up',
            '主叫拒接': 'test_call_reject',
            '主叫未接': 'test_call_no_answer',
        }
        return cp_case_func_dict.get(case)

    @classmethod
    def start(cls, pid):
        p = psutil.Process(pid)
        print("(start)pid: {}".format(pid))
        print("(start)p: {}".format(p))
        time.sleep(1)

    @classmethod
    def pause(cls, pid):
        p = psutil.Process(pid)
        print("(pause)pid: {}".format(pid))
        print("(pause)p: {}".format(p))
        time.sleep(10000)
