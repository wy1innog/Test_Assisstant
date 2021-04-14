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
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QComboBox


from caseTable_Page import CaseTable_Page
from common.log import Log
from common.normal_func import Normal_func
import common.pysql_connect as pysql
from cpSettings_page import CP_settings
from testcase.test_cp_call import Test_Call

parent_path = os.path.dirname(sys.path[0])
if parent_path not in sys.path:
    sys.path.append(parent_path)


class Ass(QMainWindow, QComboBox, Normal_func):


    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.log = Log(__name__).getlog()
        self.dev_check()
        self.ser = self.getSer()
        self.port_check()
        self.initUI()
        self.RECV_FLAG = True
        self.TEST_FLAG = False
        self.NETWORK_REGISTERED = False
        pysql.recover_checked_state()
        self.fresh_test_show()


    def initUI(self):
        self.setWindowTitle("Test Assistant")
        icon = 'D:\\ihblu\\wyrepo\\Test_Assistant\\img\\icon.ico'
        self.setWindowIcon(QIcon(icon))
        # 实例化用例表，从tab AP，CP打开取出对应的用例
        self.caseTable_apwindow = CaseTable_Page('ap')
        self.caseTable_cpwindow = CaseTable_Page('cp')

        self.cp_settings = CP_settings()


        self.Btn_dev_check.clicked.connect(self.dev_check)
        self.Btn_select_ap_case.clicked.connect(self.action_select_by_ap)

        self.Btn_AP_runTest.clicked.connect(self.run_AP_selected_test)
        self.Btn_AP_stopTest.clicked.connect(self.stop_test_ap)
        self.Btn_AP_clearBrowser.clicked.connect(self.ap_clear_recv)

        self.Btn_port_check.clicked.connect(self.port_check)
        self.Btn_port_open.clicked.connect(self.port_open)
        self.Btn_port_close.clicked.connect(self.port_close)

        self.Btn_select_cp_case.clicked.connect(self.show_cpcaseTable)
        self.Btn_CP_runTest.clicked.connect(self.run_cp_selectedCase)
        self.Btn_CP_stopTest.clicked.connect(self.stop_test_cp)
        self.Btn_CP_send.clicked.connect(self.data_send)
        self.Btn_CP_clear_recvBrowser.clicked.connect(self.cp_clear_recv)
        self.Btn_CP_clear_sendEdit.clicked.connect(self.cp_clear_send)


    def action_select_by_ap(self):
        self.caseTable_apwindow.show()
        pysql.recover_checked_state()
        self.caseTable_apwindow.recover_check()
        self.caseTable_apwindow.load_case()

    def show_cpcaseTable(self):
        # 在Tab cp点击测试项按钮，返回待用cp用例的用例表界面
        self.caseTable_cpwindow.show()
        self.caseTable_cpwindow.load_case()

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
            if self.TEST_FLAG == False:
                self.TEST_FLAG = True

            caseTuple = tuple(CaseTable_Page.readyCase)
            # caseTuple = CaseTable_Page.readyCase
            self.log.debug(caseTuple)

            if len(caseTuple) > 0:
                # self.log.info("准备执行的测试用例：%s"% caseTuple)

                if len(caseTuple) == 1:
                    sql = "select title, func from %s where title in %s" % (useTable, caseTuple[0])
                else:
                    sql = "select title, func from %s where title in %s" % (useTable, caseTuple)
                self.log.debug(sql)
                result = pysql.exec_sql(sql)
                # result = [{'title': '主叫主挂', 'func': 'test_calling_to_answer'}, {'title': '主叫被挂', 'func': 'test_caller_hangs_up'}, {'title': '主叫拒接', 'func': 'test_call_reject'}, {'title': '主叫未接', 'func': 'test_call_no_answer'}]
                for i in range(len(result)):
                    print(result[i]['func'])
                    methodcaller(result[i]['func'])(test_call)
                    time.sleep(5)

            else:
                self.log.error("待测用例异常，请重新选择")
                self.TextBrowser_CP_recv.append("待测用例异常，请重新选择")

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





    def fresh_test_show(self):
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
