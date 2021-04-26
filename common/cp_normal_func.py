import os
import subprocess
import sys
import serial
# from pywinauto import application
# from pywinauto.keyboard import send_keys

import Word
from common.log import Log
from ui.mainUI import Ui_MainWindow

sys.path.append("..")

# WIN32 API
IS_WIN32 = 'win32' in str(sys.platform).lower()


class CpNormalFunc(Ui_MainWindow):
    log = Log(__name__).getlog()
    config_path = Word.config_path

    def __init__(self):
        # self.log = Word.log[0]
        pass

    def getSer(self):
        self.ser = serial.Serial()
        self.ser.baudrate = 115200
        return self.ser

    @classmethod
    def case_to_func(cls, case):
        cp_case_func_dict = {
            '主叫主挂': 'test_call_to_answer',
            '主叫被挂': 'test_caller_hangs_up',
            '主叫拒接': 'test_call_reject',
            '主叫未接': 'test_call_no_answer',
        }
        return cp_case_func_dict.get(case)

    @classmethod
    def getSerialno(cls):
        cmd = "adb get-serialno"
        serialno = subprocess.getoutput(cmd)
        if serialno != "unknown":
            return serialno
        else:
            return "unknown"

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
        try:
            Word.ser.setPort(self.ComboBox_port_select.currentText())
        except serial.SerialException:
            self.log.error("找不到端口")
        try:
            if Word.ser.is_open:
                pass
            else:
                Word.ser.open()
            self.exec_cmd("AT^DSCI=1")
            self.Btn_port_open.setEnabled(False)
            self.Btn_port_close.setEnabled(True)
            self.GroupBox_CP_test.setTitle("串口状态(%s)" % Word.ser.port)
            self.log.debug("ser is open: %s" % Word.ser)
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
    def chup_up(cls):
        cls.exec_cmd(cls, "AT+CHUP")

    @classmethod
    def network_check(cls):
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





