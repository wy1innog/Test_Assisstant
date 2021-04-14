import re
import subprocess
import sys
import serial
import yaml
from PyQt5.QtCore import QTimer

from serial import SerialException

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


    def port_open(self):
        self.ser.setPort(self.ComboBox_port_select.currentText())

        try:
            self.ser.open()
            self.timerstart()
            self.Btn_port_open.setEnabled(False)
            self.Btn_port_close.setEnabled(True)
            self.GroupBox_CP_test.setTitle("串口状态(%s)" % self.ser.port)
            self.log.info(self.ser)
        except:
            # QMessageBox.critical( "Port Error", "此串口不能被打开！")
            print("此串口不能被打开")

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


    def timerstart(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.data_recv)
        # 每隔0.003s执行一次接收
        self.timer.start(3)


    def data_recv(self):
        """
        串口接收数据
        :return:
        """
        ser = self.ser

        try:
            if ser.inWaiting():

                data = ser.read(ser.inWaiting())
                self.log.debug("Receive data:%s" % data.decode('utf-8', "ignore"))

                # 检查是否有关键log
                Normal_func.call_check(str(data))
                if self.RECV_FLAG == True:
                    self.TextBrowser_CP_recv.insertPlainText(data.decode('utf-8', "ignore"))
                # recv_to_bottom(self)
            else:
                pass
        except SerialException as e:
            if ser.is_open:
                self.log.error(e)
                self.port_close()


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
    def call_check(self, line):
        """
        通话测试关键词
        :param line: 接收的数据
        """
        with open('config/config.yml', 'r', encoding='utf-8') as f:
            content = yaml.load(f.read(), yaml.FullLoader)
            number = content['config_call']['call_number']
        network_registered = '+CREG: 0,1'

        dial = '^DSCI: 1,0,2,0,0,"{}"'.format(number)

        ring = '^DSCI: 1,0,3,0,0,"{}"'.format(number)

        hang_up = '^DSCI: 1,0,6,0,0,"{}"'.format(number)

        # 表明主叫电话终止成功，原因正常呼叫清除
        hang_up_active = '^DSCI: 1,0,6,0,0,"{}",129,,16,3'.format(number)
        # 对端挂断
        reject_hang_up = '^DSCI: 1,0,6,0,0,"{}",129,,16,6'.format(number)
        reject_hang_up = '^DSCI: 1,0,6,0,0,"{}",129,,16,130'.format(number)
        # NO CARRIER表明异常挂断,原因协议错误，未指定，ap侧显示呼出界面直接清除
        dial_error = '^DSCI: 1,0,6,0,0,"{}",129,,111'.format(number)
        # NO CARRIER表示电话状态为电话终止，未接通原因目的地障碍， APP侧语音提示所拨打电话已关机。
        unreachable = '^DSCI: 1,0,6,0,0,"{}",129,,27'.format(number)
        # NO CARRIER表示电话状态为电话终止，原因无效的数字格式，部分机器会提示所拨打号码为空号。
        error_number = '^DSCI: 1,0,6,0,0,"{}",129,,28'.format(number)
        # flight mode
        flight_mode = '^DSCI: 1,0,6,0,0,"{}",129,,31'.format(number)
        # BUSY表示电话状态为电话终止，未接通原因用户忙， APP侧语音提示所拨打电话正在通话中，请稍后再拨。
        busy = '^DSCI: 1,0,6,0,0,"{}",129,,17'.format(number)
        # NO CARRIER表示电话状态为电话终止，原因空号， APP侧语音提示所拨打是空号，请查证再拨
        empty_number = '^DSCI: 1,0,6,0,0,"{}",129,,1,'.format(number)
        answer = '^DSCI: 1,0,0,0,0,"{}"'.format(number)

        if network_registered in line:
            self.NETWORK_REGISTERED = True
            self.log.info("NETWORK_REGISTERED  +CREG: 0,1")

        if dial in line:
            self.TextBrowser_CP_recv.append("正在拨号>> %s" % number)
            self.process.append("拨号")
            self.log.info("正在拨号>> %s" % number)
        if ring in line:
            self.TextBrowser_CP_recv.append("对端振铃")
            self.process.append("对端振铃")
            self.log.info("对端振铃")
        if answer in line:
            self.TextBrowser_CP_recv.append("对端已接听")
            self.process.append("对端接听")
            self.log.info("对端已接听")
        if 'NO ANSWER' in line:
            self.TextBrowser_CP_recv.append("对端无应答")
            self.process.append("对端无应答, 通话结束")
            self.log.info("对端无应答")

        if hang_up_active in line:
            self.TextBrowser_CP_recv.append("主动挂断，通话结束")
            self.process.append("通话结束")
            self.log.info("主动挂断，通话结束\n")
        elif busy in line:
            self.TextBrowser_CP_recv.append("所拨打的号码正在通话中，通话结束")
            self.process.append("busy, 通话结束")
            self.log.info("所拨打的号码正在通话中，通话结束\n")
        elif flight_mode in line:
            self.TextBrowser_CP_recv.append("所拨打的号码正在通话中，通话结束")
            self.process.append("busy, 通话结束")
            self.log.info("所拨打的号码正在通话中，通话结束\n")
        elif dial_error in line:
            self.TextBrowser_CP_recv.append("异常挂断，通话结束")
            self.process.append("通话结束")
            self.log.info("通话结束\n")
        elif unreachable in line:
            self.TextBrowser_CP_recv.append("所拨打的号码已关机，通话结束")
            self.process.append("通话结束")
            self.log.info("通话结束\n")
        elif error_number in line:
            self.TextBrowser_CP_recv.append("无效的数字格式，通话结束")
            self.process.append("通话结束")
            self.log.info("通话结束\n")
        elif empty_number in line:
            self.TextBrowser_CP_recv.append("所拨打的号码是空号，通话结束")
            self.process.append("通话结束")
            self.log.info("通话结束\n")
        elif hang_up in line:
            self.TextBrowser_CP_recv.append("通话结束")
            self.process.append("通话结束")
            self.log.info("通话结束\n")

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

