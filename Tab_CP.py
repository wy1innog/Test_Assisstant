import json
import threading
import time
from json import JSONDecodeError

import serial
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QComboBox
from serial import SerialTimeoutException, SerialException

from common.Ass_util import recv_to_bottom
from common.log import Log
from ui.main_ui import Ui_MainWindow


class CP(Ui_MainWindow, QMainWindow):
    config_path = 'config/config.cfg'

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.log = Log(__name__).getlog()

        self.ser = serial.Serial()
        self.port_check()
        self._prepare_AT()
        self.process = []
        self.RECV_FLAG = True
        self.TEST_FLAG = False
        self.NETWORK_REGISTERED = False

        # Tab CP

        # 定时器接收数据
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.data_receive)


# 停止正在进行的cp测试项
    def stop_test_cp(self):
        if self.TEST_FLAG == True:
            self.TEST_FLAG = False
            self.CP_recv_textBrowser.append("测试被强制停止！！！本次测试结束后终止测试")
            self.log.warning("force stop test !!!")
        else:
            pass

    # 导入config.json中所有指令
    def _prepare_AT(self):
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                AT_list = config['AT_list']
                self.Edit_test_count_AP.setPlaceholderText(config['Test_times'])
                self.Edit_test_count.setPlaceholderText(config['Test_times'])
                for line in AT_list:
                    self.combox_at_choice.addItem(line.strip())

        except FileNotFoundError:
            info = {
                "number": "18701997306",
                "content": "AT",
                "Test_times": "1",
                "interval": "5",
                "AT_list": ["AT", "AT+CFUN?", "AT+CREG?", "AT^DMSN", "AT+CGMR"]
            }
            with open(self.config_path, 'w', encoding='utf-8') as fp:
                json.dump(info, fp=fp, indent=4, ensure_ascii=False)
                self._prepare_AT()
        except (JSONDecodeError, TypeError) as e:
            self.log.error("配置文件出现问题，请删除配置文件重新打开程序（会自动生成新配置文件）")



    def port_check(self):
        # 检测所有存在的串口
        self.log.info("######>>> Check port")
        self.Com_Dict = {}
        port_list = list(serial.tools.list_ports.comports())
        self.combox_sp_choice.clear()
        for port in port_list:
            self.Com_Dict["%s" % port[0]] = "%s" % port[1]
            self.combox_sp_choice.addItem(port[0])

        self.log.debug("Port list:%s" % self.Com_Dict)
        if len(self.Com_Dict) == 0:
            self.combox_sp_choice.setCurrentText("无串口")

    def port_open(self):
        # 打开串口
        self.log.info("######>>> Open port")
        self.ser.port = self.combox_sp_choice.currentText()
        self.ser.baudrate = int(self.combox_baudrate.currentText())
        self.log.info("Port:%s  baudrate:%s  bytesize:8  parity:N  stopbits:1" % (self.ser.port, self.ser.baudrate))
        try:
            self.ser.open()

        except:
            # QMessageBox.critical(self, "Port Error", "此串口不能被打开！")
            QMessageBox.critical(self, "Port Error", "此串口不能被打开！")
            return None

        # 每隔0.003s执行一次接收
        self.timer.start(3)
        if self.ser.is_open:
            self.btn_sp_open.setEnabled(False)
            self.btn_sp_close.setEnabled(True)
            self.CP_func_left_GroupBox.setTitle("串口状态（已开启） %s" % self.ser.name)

    def port_close(self):
        self.log.info("######>>> Close port")
        try:
            self.ser.close()
        except:
            pass
        self.btn_sp_open.setEnabled(True)
        self.btn_sp_close.setEnabled(True)
        self.CP_func_left_GroupBox.setTitle("串口状态（已关闭）")

    # def refresh_at_list(self):
    #     ds.listWidget.clear()
    #     with open(self.config_path, 'r', encoding='utf-8') as f:
    #         AT_list = json.load(f)['AT_list']
    #         for line in AT_list:
    #             ds.listWidget.addItem(line.strip())
    #     self.log.info("######>>> Refresh at list")

    def refresh_at_combobox(self):
        self.combox_at_choice.clear()
        self.combox_at_choice.addItem("刷新")
        with open(self.config_path, 'r', encoding='utf-8') as f:
            AT_list = json.load(f)['AT_list']
            for line in AT_list:
                self.combox_at_choice.addItem(line.strip())

        self.log.debug("######>>> Refresh at combobox")

    def exec_choose_at(self):
        at_cmd1 = self.combox_at_choice.currentText()
        if at_cmd1 != "刷新":
            if self.ser.is_open:
                try:
                    self.RECV_FLAG = True
                    at_cmd = (at_cmd1 + '\r\n').encode('utf-8')
                    self.ser.write(at_cmd)
                    self.log.info("Send Combobox Cmd: %s" % at_cmd1)
                except SerialTimeoutException:
                    pass
        else:
            self.refresh_at_combobox()



    # 发送数据
    def data_send(self):
        if self.ser.is_open:
            at_cmd = self.CP_send_textEdit.toPlainText().strip()
            self.RECV_FLAG = True
            if at_cmd != "":
                # 非空字符串
                input_s = (at_cmd + '\r\n').encode('utf-8')
                self.ser.write(input_s)
                self.log.info("Send At Cmd: %s" % at_cmd)
        else:
            self.CP_recv_textBrowser.append("终端状态异常")
            self.log.warning("终端连接状态异常")

    # 接收数据
    def data_receive(self):
        try:
            if self.ser.inWaiting():

                data = self.ser.read(self.ser.inWaiting())
                self.log.debug("Receive data:%s" % data.decode('utf-8', "ignore"))

                # 检查是否有关键log
                self.call_check(str(data))
                if self.RECV_FLAG == True:
                    self.CP_recv_textBrowser.insertPlainText(data.decode('utf-8', "ignore"))
                recv_to_bottom(self)
            else:
                pass
        except SerialException:
            if self.ser.is_open:
                self.port_close()

    # 清除显示
    def cp_clear_send(self):
        self.CP_send_textEdit.setText("")

    def cp_clear_recv(self):
        self.CP_recv_textBrowser.setText("")

    # 根据选框执行相应测试项
    def run_test_choice_cp(self):
        self._exec_cmd("AT^DSCI=1")
        self._exec_cmd("AT+CREG?")
        if self.TEST_FLAG == False:
            self.TEST_FLAG = True

            if self.ser.is_open:

                if self.Radio_calling_to_answer.isChecked():
                    self.call_test('calling_to_answer')

                elif self.Radio_caller_hangs_up.isChecked():
                    self.call_test('caller_hangs_up')

                elif self.Radio_calling_reject.isChecked():
                    self.call_test('calling_reject')

                elif self.Radio_no_caller_answer.isChecked():
                    self.call_test('no_caller_answer')

                else:
                    self.CP_recv_textBrowser.append("未选择测试项")

            else:
                self.log.warning("终端状态异常")


    def _exec_cmd(self, cmd):
        cmd1 = (cmd + '\r\n').encode('utf-8')
        try:
            self.ser.write(cmd1)
            self.log.info("exec >> " + cmd)
        except SerialException:
            self.log.warning("Attempting to use a port that is not open")
            self.CP_recv_textBrowser.append("终端状态异常")

    def call_check(self, line):
        with open(self.config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        number = config['number']
        network_registered = '+CREG: 0,1'

        dial = '^DSCI: 1,0,2,0,0,"{}"'.format(number)

        ring = '^DSCI: 1,0,3,0,0,"{}"'.format(number)

        hang_up = '^DSCI: 1,0,6,0,0,"{}"'.format(number)

        # 表明主叫电话终止成功，原因正常呼叫清除
        hang_up_active = '^DSCI: 1,0,6,0,0,"{}",129,,16,3'.format(number)
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
            self.CP_recv_textBrowser.append("正在拨号>> %s" % number)
            self.process.append("拨号")
            self.log.info("正在拨号>> %s" % number)
        if ring in line:
            self.CP_recv_textBrowser.append("对端振铃")
            self.process.append("对端振铃")
            self.log.info("对端振铃")
        if answer in line:
            self.CP_recv_textBrowser.append("对端已接听")
            self.process.append("对端接听")
            self.log.info("对端已接听")
        if 'NO ANSWER' in line:
            self.CP_recv_textBrowser.append("对端无应答")
            self.process.append("对端无应答, 通话结束")
            self.log.info("对端无应答")

        if hang_up_active in line:
            self.CP_recv_textBrowser.append("主动挂断，通话结束")
            self.process.append("通话结束")
            self.log.info("主动挂断，通话结束\n")
        elif busy in line:
            self.CP_recv_textBrowser.append("所拨打的号码正在通话中，通话结束")
            self.process.append("busy, 通话结束")
            self.log.info("所拨打的号码正在通话中，通话结束\n")
        elif flight_mode in line:
            self.CP_recv_textBrowser.append("所拨打的号码正在通话中，通话结束")
            self.process.append("busy, 通话结束")
            self.log.info("所拨打的号码正在通话中，通话结束\n")
        elif dial_error in line:
            self.CP_recv_textBrowser.append("异常挂断，通话结束")
            self.process.append("通话结束")
            self.log.info("通话结束\n")
        elif unreachable in line:
            self.CP_recv_textBrowser.append("所拨打的号码已关机，通话结束")
            self.process.append("通话结束")
            self.log.info("通话结束\n")
        elif error_number in line:
            self.CP_recv_textBrowser.append("无效的数字格式，通话结束")
            self.process.append("通话结束")
            self.log.info("通话结束\n")
        elif empty_number in line:
            self.CP_recv_textBrowser.append("所拨打的号码是空号，通话结束")
            self.process.append("通话结束")
            self.log.info("通话结束\n")
        elif hang_up in line:
            self.CP_recv_textBrowser.append("通话结束")
            self.process.append("通话结束")
            self.log.info("通话结束\n")

    def call_test(self, test_item):
        with open(self.config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            number = config['number']
            interval = int(config['interval'])
            times_text = self.Edit_test_count.text()

        if times_text.isdigit():
            times = times_text

            config['Test_times'] = times_text
            if test_item == 'calling_to_answer':
                self.log.debug("calling_to_answer")
                thread_calling = threading.Thread(target=self._calling_to_answer, args=(times, number, interval))
                thread_calling.start()
            elif test_item == 'caller_hangs_up':
                self.log.debug("caller_hangs_up")
                thread_calling = threading.Thread(target=self._caller_hangs_up, args=(times, number, interval))
                thread_calling.start()
            elif test_item == 'calling_reject':
                self.log.debug("calling_reject")
                thread_calling = threading.Thread(target=self._calling_reject, args=(times_text, number, interval))
                thread_calling.start()
            elif test_item == 'no_caller_answer':
                self.log.debug("no_caller_answer")
                thread_calling = threading.Thread(target=self._no_caller_answer, args=(times_text, number, interval))
                thread_calling.start()
        elif times_text == '':
            times = config['Test_times']
            if test_item == 'calling_to_answer':
                self.log.debug("calling_to_answer")
                thread_calling = threading.Thread(target=self._calling_to_answer, args=(times, number, interval))
                thread_calling.start()
            elif test_item == 'caller_hangs_up':
                self.log.debug("caller_hangs_up")
                thread_calling = threading.Thread(target=self._caller_hangs_up, args=(times, number, interval))
                thread_calling.start()
            elif test_item == 'calling_reject':
                self.log.debug("calling_reject")
                thread_calling = threading.Thread(target=self._calling_reject, args=(times, number, interval))
                thread_calling.start()
            elif test_item == 'no_caller_answer':
                self.log.debug("no_caller_answer")
                thread_calling = threading.Thread(target=self._no_caller_answer, args=(times, number, interval))
                thread_calling.start()
        else:
            self.CP_recv_textBrowser.append("次数格式错误，请重新输入")

    def _calling_to_answer(self, times, number, interval):
        """
        测试项——主叫主挂，终端主叫，对端接听后，终端主动挂断
        :param times: 测试次数
        :param number: 对端号码
        :return: None
        """
        global i
        pass_calling_to_answer = 0
        fail_calling_to_answer = 0
        self.CP_recv_textBrowser.append("测试项：主叫主挂 测试次数:%s" % times)
        self.RECV_FLAG = False
        current_process = ['拨号', '对端振铃', '对端接听', '通话结束']

        self.log.debug("Test times: %s" % times)
        for i in range(int(times)):
            recv_to_bottom(self)
            if self.TEST_FLAG and self.NETWORK_REGISTERED == True:
                self.process.clear()
                time.sleep(interval)
                self.CP_recv_textBrowser.append("主叫主挂 >> 第%s次, 共 %s次" % (i+1, times))
                self._exec_cmd('ATD%s;' % number)

                self.log.info("主叫主挂 >> 第%s次, 共%s次," % (i+1, times))

                while True:
                    try:
                        time.sleep(3)
                        self.log.debug("dial process: %s" % self.process)
                        if self.process[-1] == "对端接听":
                            # 等待5s超时，自动挂断
                            time.sleep(5)
                            self._exec_cmd('AT+CHUP')

                        elif self.process[-1] == "通话结束":
                            if self.process == current_process:
                                pass_calling_to_answer += 1
                                self.log.info("通话流程为正确流程：{}".format(self.process))
                            else:
                                fail_calling_to_answer += 1
                                self.log.warning("通话流程有误：{}".format(self.process))
                            break
                    except IndexError:
                        self.log.warning("拨打失败，请检查设备是否入网")
                        self.CP_recv_textBrowser.append("测试停止，请检查设备入网状态")
                        fail_calling_to_answer += 1
                        break

            else:
                i -= 1
                self.CP_recv_textBrowser.append("网络未注册")
                break
        self.TEST_FLAG = False
        self.CP_recv_textBrowser.append("测试项：主叫主挂 测试次数: %d, pass: %d, fail: %d\r\n" %
                                        (i+1, pass_calling_to_answer, fail_calling_to_answer))
        recv_to_bottom(self)

        self.log.info("测试项：主叫主挂 测试次数: %d, pass: %d, fail: %d\r\n" %
                    (i+1, pass_calling_to_answer, fail_calling_to_answer))


    def _caller_hangs_up(self, times, number, interval):
        """
        测试项——主叫被挂，终端主叫，对端接听接听后，对端主动挂断
        :param times: 测试次数
        :param number: 对端号码
        :return: None
        """
        global i
        pass_hangs_up = 0
        fail_hangs_up = 0
        self.CP_recv_textBrowser.append("测试项：主叫被挂 测试次数:%s" % times)
        self.RECV_FLAG = False
        current_process = ['拨号', '对端振铃', '对端接听', '通话结束']

        self.log.debug("Test times:%s" % times)
        for i in range(int(times)):
            recv_to_bottom(self)
            if self.TEST_FLAG and self.NETWORK_REGISTERED == True:
                self.process.clear()
                time.sleep(interval)
                self.CP_recv_textBrowser.append("主叫被挂 >> 第%s次, 共%s次," % (i+1, times))
                self._exec_cmd('ATD%s;' % number)
                self.log.info("主叫被挂 >> 第%s次, 共%s次," % (i+1, times))

                while True:
                    try:
                        time.sleep(3)
                        self.log.debug("dial process: %s" % self.process)
                        if self.process[-1] == "对端接听":
                            time.sleep(5)
                            self._exec_cmd('AT+CHUP')
                        elif self.process[-1] == "通话结束":
                            if self.process == current_process:
                                pass_hangs_up += 1
                                self.log.info("通话流程为正确流程：{}".format(self.process))

                            else:
                                fail_hangs_up += 1
                                self.log.warning("通话流程有误：{}".format(self.process))
                            break
                    except IndexError:
                        self.log.error("拨打失败，请检查是被是否入网")
                        self.CP_recv_textBrowser.append("测试停止，请检查设备入网状态")
                        fail_hangs_up += 1
                        self.TEST_FLAG = False
                        break
            else:
                i -= 1
                break
        self.TEST_FLAG = False
        self.CP_recv_textBrowser.append("测试项：主叫被挂 测试次数:%d, pass:%d, fail:%d\r\n" %
                                        (i+1, pass_hangs_up, fail_hangs_up))
        recv_to_bottom(self)
        self.log.info("测试项：主叫被挂 测试次数:%d, pass:%d, fail:%d\r\n" %
                    (i+1, pass_hangs_up, fail_hangs_up))


    def _calling_reject(self, times, number, interval):
        """
        测试项——主叫拒接，终端主叫，对端挂断
        :param times: 测试次数
        :param number: 对端号码
        :return: None
        """
        global i
        pass_calling_reject = 0
        fail_calling_reject = 0
        self.CP_recv_textBrowser.append("测试项：主叫拒接 测试次数:%s" % times)
        self.RECV_FLAG = False
        current_process = ['拨号', '对端振铃', '通话结束']

        self.log.debug("Test times:%s" % times)
        for i in range(int(times)):
            recv_to_bottom(self)
            if self.TEST_FLAG and self.NETWORK_REGISTERED == True:
                time.sleep(interval)
                self.process.clear()
                self.CP_recv_textBrowser.append("主叫拒接 >> 第%s次, 共%s次," % (i+1, times))
                self._exec_cmd('ATD%s;' % number)
                self.log.info("主叫拒接 >> 第%s次, 共%s次," % (i+1, times))

                while True:
                    try:
                        time.sleep(3)
                        self.log.debug("dial process: %s" % self.process)
                        if "通话结束" in self.process[-1]:
                            if self.process == current_process:
                                pass_calling_reject += 1
                                self.log.info("通话流程为正确流程：{}".format(self.process))
                            else:
                                fail_calling_reject += 1
                                self.log.warning("通话流程有误：{}".format(self.process))
                            break
                    except IndexError:
                        self.log.error("拨打失败，请检查是被是否入网")
                        self.CP_recv_textBrowser.append("测试停止，请检查设备入网状态")
                        fail_calling_reject += 1
                        self.TEST_FLAG = False
                        break
            else:
                i -= 1
                break
        self.TEST_FLAG = False
        self.CP_recv_textBrowser.append("测试项：主叫拒接 测试次数:%s, pass:%d, fail:%d\r\n" %
                                        (i+1, pass_calling_reject, fail_calling_reject))
        recv_to_bottom(self)
        self.log.info("测试项：主叫拒接 测试次数:%d, pass:%d, fail:%d\r\n" %
                    (i+1, pass_calling_reject, fail_calling_reject))


    def _no_caller_answer(self, times, number, interval):
        """
        测试项——主叫未接，终端主叫，对端不予接听
        :param times: 测试次数
        :param number: 对端号码
        :return: None
        """
        global i
        pass_no_caller_answer = 0
        fail_no_caller_answer = 0
        self.CP_recv_textBrowser.append("测试项：主叫未接 测试次数:%s" % times)
        self.RECV_FLAG = False
        # current_process = ['拨号', '对端振铃', '对端无应答, 通话结束']
        current_process = ['拨号', '对端振铃', '通话结束']

        self.log.debug("Test times: %s" % times)
        for i in range(int(times)):
            recv_to_bottom(self)
            if self.TEST_FLAG and self.NETWORK_REGISTERED == True:
                self.process.clear()
                time.sleep(interval)
                self.CP_recv_textBrowser.append("主叫未接 >> 第%s次, 共%s次," % (i+1, times))
                self._exec_cmd('ATD%s;' % number)
                self.log.info("主叫未接 >> 第%s次, 共%s次," % (i+1, times))

                while True:
                    time.sleep(3)
                    self.log.debug("dial process: %s" % self.process)
                    try:
                        if self.process[-1] == "通话结束":
                            if self.process == current_process:
                                pass_no_caller_answer += 1
                                self.log.info("通话流程为正确流程：{}".format(self.process))
                            else:
                                fail_no_caller_answer += 1
                                self.log.warning("通话流程有误：{}".format(self.process))
                            break

                        # timeout
                    except IndexError:
                        self.log.error("拨打失败，请检查是被是否入网")
                        self.CP_recv_textBrowser.append("测试停止，请检查设备入网状态")
                        fail_no_caller_answer += 1
                        self.TEST_FLAG = False
                        break
            else:
                i -= 1
                break
        self.TEST_FLAG = False
        self.CP_recv_textBrowser.append("测试项：主叫未接 测试次数:%s, pass:%d, fail:%d\r\n" %
                                        (i+1, pass_no_caller_answer, fail_no_caller_answer))
        recv_to_bottom(self)
        self.log.info("测试项：主叫未接 测试次数:%s, pass:%d, fail:%d\r\n" %
                    (i+1, pass_no_caller_answer, fail_no_caller_answer))