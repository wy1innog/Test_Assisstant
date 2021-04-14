# coding=utf-8
import datetime
import json
import os
import subprocess
import sys
import threading
import time
from operator import methodcaller

import serial
import serial.tools.list_ports
import yaml
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QComboBox

import Word
from caseTable_Page import CaseTable_Page
from common.log import Log
from common.normal_func import Normal_func
import common.pysql_connect as pysql
from cpSettings_page import CP_settings
from testcase.test_cp_call import Test_Call

parent_path = os.path.dirname(sys.path[0])
if parent_path not in sys.path:
    sys.path.append(parent_path)


class MainPage(QMainWindow, QComboBox, Normal_func):


    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.log = Log(__name__).getlog()
        self.dev_check()
        self.port_check()
        self.ser = self.getSer()
        pysql.recover_checked_state()
        self.testStatusShow()
        self.RECV_FLAG = True
        self.TEST_FLAG = False
        self.NETWORK_REGISTERED = False


    def initUI(self):
        self.setWindowTitle("Test Assistant")
        icon = 'D:\\ihblu\\wyrepo\\Test_Assistant\\img\\icon.ico'
        self.setWindowIcon(QIcon(icon))
        # 实例化用例表，从tab AP，CP打开取出对应的用例
        self.caseTable_apwindow = CaseTable_Page('ap')
        self.caseTable_cpwindow = CaseTable_Page('cp')

        self.cp_settings = CP_settings()


        self.Btn_dev_check.clicked.connect(self.dev_check)
        self.Btn_select_ap_case.clicked.connect(self.showAPCaseTable)

        self.Btn_AP_runTest.clicked.connect(self.run_AP_selected_test)
        self.Btn_AP_stopTest.clicked.connect(self.stop_test_ap)
        self.Btn_AP_clearBrowser.clicked.connect(self.ap_clear_recv)

        self.Btn_port_check.clicked.connect(self.port_check)
        self.Btn_port_open.clicked.connect(self.port_open)
        self.Btn_port_open.clicked.connect(self.timerstart)
        self.Btn_port_close.clicked.connect(self.port_close)

        self.Btn_select_cp_case.clicked.connect(self.showCPCaseTable)
        self.Btn_CP_runTest.clicked.connect(self.run_cp_selectedCase)
        self.Btn_CP_stopTest.clicked.connect(self.stop_test_cp)
        self.Btn_CP_send.clicked.connect(self.data_send)
        self.Btn_CP_clear_recvBrowser.clicked.connect(self.cp_clear_recv)
        self.Btn_CP_clear_sendEdit.clicked.connect(self.cp_clear_send)


    def showAPCaseTable(self):
        Word.be_testcase.clear()
        self.caseTable_apwindow.show()
        pysql.recover_checked_state()
        self.caseTable_apwindow.recover_check()
        self.caseTable_apwindow.loadCase()

    def showCPCaseTable(self):
        # 在Tab cp点击测试项按钮，返回待用cp用例的用例表界面
        Word.be_testcase.clear()
        self.caseTable_cpwindow.show()
        self.caseTable_cpwindow.loadCase()

    def show_cpSettings(self):
        self.cp_settings.show()

    def run_AP_selected_test(self):
        self.TEST_FLAG = True
        if self.nf.getDev() != 0 and self.nf.getDev() != 2:
            # {多选框：[状态<1：勾选，0，未勾选>，对应方法]}
            test_item = {"CheckBox_SIM_test": [0, "test_SIM"],
                         "CheckBox_SDcard_test": [0, "test_SDcard"],
                         "CheckBox_reboot_test": [0, "test_reboot"],
                         "CheckBox_BT_test": [0, "test_BT"],
                         "CheckBox_GPS_test": [0, "test_GPS"],
                         "CheckBox_WIFI_test": [0, "test_WIFI"],
                         "CheckBox_APP_startexit_test": [0, "test_APP_startexit"],
                         "CheckBox_Camera_test": [0, "test_Camera"],
                         "CheckBox_Contact_test": [0, "test_Contact"],
                         "CheckBox_OTA_test": [0, "test_OTA"],
                         "CheckBox_APKoper_test": [0, "test_APKoper"],
                         "CheckBox_APK_install_test": [0, "test_APK_install"]
                         }
            times = self.LineEdit_AP_test_times.text()
            func_list = []
            for item in test_item:
                checkbox_obj = getattr(self, item)
                if checkbox_obj.isChecked():
                    test_item[item][0] = 1

            for item in test_item:
                if test_item[item][0] == 1:
                    func_list.append(test_item[item][1])
                else:
                    pass
            self.log.debug("Test func: %s\tTest times: %s" % (func_list, times))

            if func_list and times.isdigit():
                for func in func_list:
                    for current_test_times in range(int(times)):
                        myfunc = methodcaller(func, current_test_times, times)(self)
                        thread = threading.Thread(target=myfunc)
                        thread.start()
            else:
                self.ap_printf("未选择测试项或测试次数")

    def stop_test_ap(self):
        """
        强制停止AP侧测试项
        :return: None
        """
        if self.TEST_FLAG == True:
            self.TEST_FLAG = False
            self.TextBrowser_AP_recv.append("测试被强制停止！！！本次测试结束后终止测试")
            self.log.warning("force stop test !!!")
        else:
            pass

    def dev_check(self):
        """
        AP 设备下拉框选项添加
        :return: None
        """
        self.log.info("######>>> Check device")
        self.ComboBox_dev_select.clear()
        dev_list = []
        result = subprocess.getoutput("adb devices").strip().split("\n")
        for dev in result:
            if "List of devices attached" in dev:
                continue
            if "device" in dev:
                dev_list.append(dev[:-7])

        if len(dev_list) == 0:
            self.ComboBox_dev_select.addItem(" 无设备")
        for dev in dev_list:
            self.ComboBox_dev_select.addItem(dev)

        self.log.debug("Device list:%s" % dev_list)


    def get_locallog(self):
        thread_getlog = threading.Thread(target=self._get_locallog)
        thread_getlog.start()

    def _get_locallog(self):
        """
        AP 获取设备data/local/log目录下log到本地/logs/
        :return: None
        """
        self.log.info("######>>> get local log")
        if getDev() != 0:
            self.TextBrowser_AP_recv.append("log抓取中……")
            # savelog_path = os.path.dirname(__file__) + '\logs'
            savelog_path = '\logs'
            print("savelog_path: {}".format(savelog_path))
            if not os.path.exists(savelog_path):
                os.makedirs(savelog_path)
            save_dir = os.path.join(savelog_path, '{0:%Y%m%d%H%M%S}'.format(datetime.datetime.now()))

            status = subprocess_call("adb -s %s pull data/local/log %s" % (dev(), save_dir))

            self.log.debug("Pull local log status:%s" % status)

            if status == 0:
                self.TextBrowser_AP_recv.append("log抓取完成，已保存至" + save_dir + "\n")
            else:
                self.TextBrowser_AP_recv.append("log保存失败，请检查设备状态\n")
        else:
            self.TextBrowser_AP_recv.append("无设备连接")


    def ap_clear_recv(self):
        # 清楚AP接收区内容
        self.TextBrowser_AP_recv.clear()

    def ap_clear_send(self):
        # 清除AP发送区内容
        self.textEdit_number.clear()

    # CP ================================================================================================

    def port_check(self):
        """
        CP 检测连接PC的端口
        :return: None
        """
        self.log.info("######>>> Check port")
        self.Com_Dict = {}
        port_list = list(serial.tools.list_ports.comports())
        self.ComboBox_port_select.clear()
        for port in port_list:
            self.Com_Dict["%s" % port[0]] = "%s" % port[1]
            self.ComboBox_port_select.addItem(port[0])

        self.log.debug("Port list:%s\n" % self.Com_Dict)
        if len(self.Com_Dict) == 0:
            self.ComboBox_port_select.setCurrentText("无串口")


    def run_cp_selectedCase(self):
        """
        CP 执行测试选项
        """
        test_call = Test_Call()
        self.RECV_FLAG = False

        useTable = 'cp_testcases'
        test_times = self.Ledit_CP_test_times.text()
        if Normal_func.number_check(test_times) == True:
            self.TEST_FLAG = True

            self.log.debug(Word.be_testcase)
            casetitle = Normal_func.getBeTestCaseTitle()

            for index in Word.cp_case_func_dict:
                for case in casetitle:
                    if index == case:
                        methodcaller(Word.cp_case_func_dict[index])(test_call)


        else:
            self.log.warning("测试次数输入格式错误")
            self.TextBrowser_CP_recv.append("测试次数输入格式错误")

    def stop_test_cp(self):
        """
        CP 停止测试项
        :return:
        """
        if self.TEST_FLAG == True:
            self.TEST_FLAG = False
            self.TextBrowser_CP_recv.append("测试被强制停止！！！本次测试结束后终止测试")
            self.log.warning("force stop test !!!")
        else:
            pass





    def testStatusShow(self):
        self.textBrowser.setText("正在执行：xx\n\n共xx条用例，已测试xx条，\n未测试xx条\nPASS:XX\nFAILED:XX")

    def data_send(self):
        """
        串口发送数据
        :return:
        """
        if self.ser.is_open:
            at_cmd = self.TextEdit_CP_send.toPlainText().strip()
            self.RECV_FLAG = True
            if at_cmd != "":
                # 非空字符串
                self.exec_cmd(at_cmd)
                # input_s = (at_cmd + '\r\n').encode('utf-8')
                # self.ser.write(input_s)
                self.log.info("Send At Cmd: %s" % at_cmd)
        else:
            self.log.warning("终端连接状态异常")

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
                self.call_check(str(data))
                if self.RECV_FLAG == True:
                    self.TextBrowser_CP_recv.insertPlainText(data.decode('utf-8', "ignore"))
                # recv_to_bottom(self)
            else:
                pass
        except serial.SerialException as e:
            if ser.is_open:
                self.log.error(e)
                self.port_close()

    def timerstart(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.data_recv)
        # 每隔0.003s执行一次接收
        self.timer.start(3)

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


    def cp_clear_send(self):
        """
        清除CP发送框内容
        """
        self.TextBrowser_CP_send.setText("")

    def cp_clear_recv(self):
        """
        清除CP接收框内容
        """
        self.TextBrowser_CP_recv.setText("")



    def cp_test_times_load(self):
        """
        刷新CP 测试次数
        :return:
        """
        with open(self.config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            times = int(config['Test_times'])
        self.Edit_test_count.setText(times)
        self.log.info("close settings page, modify test times")

    def call_test(self, test_item):
        """
        通话测试选择
        :param test_item: 测试项
        """
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
            self.TextBrowser_CP_recv.append("次数格式错误，请重新输入")

    def aptextPrint(self, text):
        self.TextBrowser_AP_recv.append(text)

    def cptextPrint(self, text):
        self.TextBrowser_CP_recv.append(text)
