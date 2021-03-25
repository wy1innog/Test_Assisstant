# coding=utf-8
import datetime
import json
import os
import re
import sys
import threading
import time
from operator import methodcaller

import serial
import serial.tools.list_ports
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QComboBox
from serial import SerialException

from caseTable_Page import TestCaseTable_Page
from common.Ass_util import subprocess_getoutput, subprocess_call, dev, recv_to_bottom
from common.log import Log
from ui.main import Ui_MainWindow
import common.pysql_connect as pysql

parent_path = os.path.dirname(sys.path[0])
if parent_path not in sys.path:
    sys.path.append(parent_path)


class Ass(QMainWindow, QComboBox, Ui_MainWindow):
    config_path = 'config.cfg'

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.log = Log(__name__).getlog()
        self.dev_check()
        self.initUI()
        self.ser = serial.Serial()
        self.port_check()
        self._prepare_AT()
        self.process = []
        self.RECV_FLAG = True
        self.TEST_FLAG = False
        self.NETWORK_REGISTERED = False
        pysql.recover_checked_state()

    def initUI(self):
        self.setWindowTitle("Test Assistant")
        icon = 'D:\\ihblu\\wyrepo\\Test_Assistant\\img\\icon.ico'
        self.setWindowIcon(QIcon(icon))
        self.caseTable_window = TestCaseTable_Page()
        self.Btn_dev_check.clicked.connect(self.dev_check)
        self.Btn_select_case.clicked.connect(self.show_caseTable)

        self.Btn_AP_runTest.clicked.connect(self.run_AP_selected_test)
        self.Btn_AP_stopTest.clicked.connect(self.stop_test_ap)
        self.Btn_AP_clearBrowser.clicked.connect(self.ap_clear_recv)

        self.Btn_port_check.clicked.connect(self.port_check)
        self.Btn_port_open.clicked.connect(self.port_open)
        self.Btn_port_close.clicked.connect(self.port_close)
        self.Btn_at_exec.clicked.connect(self.exec_choose_at)

        self.Btn_CP_runTest.clicked.connect(self.run_test_choice_cp)
        self.Btn_CP_stopTest.clicked.connect(self.stop_test_cp)
        self.Btn_CP_send.clicked.connect(self.data_send)
        self.Btn_CP_clear_recvBrowser.clicked.connect(self.cp_clear_recv)
        self.Btn_CP_clear_sendEdit.clicked.connect(self.cp_clear_send)

        # 定时器接收数据
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.data_receive)

    def show_caseTable(self):
        self.caseTable_window.show()

    def run_AP_selected_test(self):
        self.TEST_FLAG = True
        if dev() != 0 and dev() != 2:
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

    def test_SIM(self, current_test_times, times):
        """
        检测SIM卡是否安装，getprop | grep gsm.sim.state
        :return: None
        """
        if dev()!=0 and dev() < 2 and self.TEST_FLAG == True:
            self.log.info("Case——test_SIM: 第%d次测试, 共%s次" % (int(current_test_times)+1, times))
            self.ap_printf("Case——test_SIM: 第%d次测试, 共%s次" % (int(current_test_times)+1, times))
            UE_sim = subprocess_getoutput('adb -s %s shell getprop | findstr gsm.sim.state' % dev()).split(':')[-1]
            self.log.debug("SIM status:%s" % UE_sim)
            sim_state_list = {
                "READY": "1",
                "LOADED": "1",
                "NOT_READY": "0",
                "ABSENT": "0",
                "UNKNOWN": "0"
            }

            if ',' in UE_sim:
                # 双卡
                UE_sim_list = UE_sim.split(',')
                self.ap_printf("检测为双卡，状态分别为：")
                for UE_sim_N in UE_sim_list:
                    for state in sim_state_list:
                        if state in UE_sim_N and sim_state_list[state] == "1":
                            self.ap_printf("SIM卡状态：正常")
                        elif state in UE_sim_N and sim_state_list[state] == "0":
                            self.ap_printf("SIM卡状态：异常")

            else:
                # 单卡
                for state in sim_state_list:
                    if state in UE_sim and sim_state_list[state] == "1":
                        self.TextBrowser_AP_recv.append("SIM卡状态：正常")
                    elif state in UE_sim and sim_state_list[state] == "0":
                        self.TextBrowser_AP_recv.append("SIM卡状态：异常")
                    else:
                        self.TextBrowser_AP_recv.append("SIM卡状态：未知")
        else:
            self.TextBrowser_AP_recv.append("无设备连接")
        self.TextBrowser_AP_recv.append("\n")

    def test_SDcard(self, current_test_times, times):
        """
        AP SD卡检测是否存在，storage/sdcard1 and SD card icon
        :return:
        """

        if dev()!=0 and dev() < 2 and self.TEST_FLAG == True:
            # 打印SDcard状态
            self.log.info("Case——test_SDcard: 第%d次测试, 共%s次" % (int(current_test_times)+1, times))
            self.ap_printf("Case——test_SDcard: 第%d次测试, 共%s次" % (int(current_test_times)+1, times))
            # 判断/storage/sdcard1下文件夹大小是否为0
            used_storage = subprocess_getoutput('adb -s %s shell du -sH storage/sdcard1' % dev()).split('\t')[0]
            self.log.debug("used_storage:%s" % used_storage)
            # 判断状态栏是否有无SD卡标识
            notif_icon = subprocess_getoutput('adb -s %s shell dumpsys notification | findstr sdcard' % dev())
            self.log.debug("SD card notification: %s" % notif_icon)
            if (used_storage == '0') and ('stat_notify_sdcard_usb' in notif_icon):
                self.ap_printf("未插入SD卡\n")
            elif (used_storage != '0') and ('stat_notify_sdcard_usb' not in notif_icon):
                self.ap_printf("已识别SD卡\n")
            else:
                self.ap_printf("check SD card error!\n")
            # assert (used_storage != '0') and ('stat_notify_sdcard_usb' not in notif_icon)
        else:
            self.ap_printf("无设备连接")

    def test_reboot(self, current_test_times, times):
        """
        AP reboot, timeout=120s
        :param times: 重启次数
        :return: None
        """
        if dev()!=0 and dev() != 2 and self.TEST_FLAG == True:
            pass_count = 0
            timeout = 120
            self.ap_printf("Case——test_reboot: 第%d次测试，共%s次" % (int(current_test_times)+1, times))
            self.log.info("测试项：reboot重启 次数：%s" % times)
            subprocess_call('adb reboot')
            start = time.time()
            self.log.debug("reboot test start time: {}".format(start))
            time.sleep(5)
            end = time.time()
            while end - start <= timeout:
                if dev() != 0:
                    ensure_boot = subprocess_getoutput('adb shell dumpsys power | findstr mBootCompleted')
                    if 'true' in ensure_boot:
                        end = time.time()
                        self.log.debug("reboot test end time: {}".format(end))
                        pass_count += 1
                        self.ap_printf("reboot重启 >> 第%d次测试完成，用时%d秒" %
                                                        (int(current_test_times)+1, end-start))
                        break

                else:
                    time.sleep(5)
                    end = time.time()
            else:
                self.ap_printf("reboot重启 ?? 重启时间超过120s，重启超时！")

        else:
            self.TextBrowser_AP_recv.append("无设备连接，测试终止")


    def test_BT(self):
        pass


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
        result = subprocess_getoutput("adb devices").strip().split("\n")
        for dev in result:
            if "List of devices attached" in dev:
                continue
            if "device" in dev:
                dev_list.append(dev[:-7])

        if len(dev_list) == 0:
            self.ComboBox_dev_select.addItem("  无设备")
        for dev in dev_list:
            self.ComboBox_dev_select.addItem(dev)

        self.log.debug("Device list:%s" % dev_list)

    def _bt_status(self):
        # 1:open  0:close

        flag = subprocess_getoutput('adb -s %s shell settings get global bluetooth_on' % dev()).strip()
        self.log.debug("Bluetooth status: %s" % flag)
        if '1' in flag:
            return True
        elif '0' in flag:
            return False
        else:
            self.TextBrowser_AP_recv.append("Bluetooth status error")
            self.log.warning("Bluetooth status error, flag=%s" % flag)

    def bt_status(self):
        """
        AP 打印蓝牙开关状态
        :return: None
        """
        self.log.info("######>>> Bluetooth status")
        if dev() != 0:
            if self._bt_status():
                self.TextBrowser_AP_recv.append("蓝牙状态: 开启\n")
            else:
                self.TextBrowser_AP_recv.append("蓝牙状态: 关闭\n")
        else:
            self.TextBrowser_AP_recv.append("无设备连接")

    def _wifi_status(self):
        wifi_status = subprocess_getoutput('adb -s %s shell dumpsys wifi | findstr Wi-Fi' % dev())
        if 'enabled' in wifi_status:
            self.log.debug("wifi status: %s" % wifi_status)
            return 1
        elif 'disabled' in wifi_status:
            self.log.debug("wifi status: %s" % wifi_status)
            return 0
        else:
            self.log.error("######??? someting error about wifi status:{}".format(wifi_status))
            return 2

    def wifi_status(self):
        """
        AP 打印wifi开启状态
        :return: None
        """
        self.log.info("######>>> wifi status")
        if dev() != 0:
            wifi_code = self._wifi_status()
            if wifi_code == 1:
                self.TextBrowser_AP_recv.append("WiFi状态: 开启\n")
                self.TextBrowser_AP_recv.append(self._wifi_info('SSID'))
            elif wifi_code == 0:
                self.TextBrowser_AP_recv.append("WiFi状态: 关闭\n")
                self.log.info("######>>> check wifi status: closed")
            else:
                self.TextBrowser_AP_recv.append("WiFi状态异常\n")
        self.TextBrowser_AP_recv.append("无设备连接")

    def _wifi_info(self, key):
        mWifiInfo = \
            subprocess_getoutput('adb -s %s shell dumpsys wifi | findstr mWifiInfo' % dev()).strip().split('\n')[0]
        self.log.debug("wifi info:%s" % mWifiInfo)
        if 'null' in mWifiInfo:
            self.TextBrowser_AP_recv.append("WiFi未连接")
            self.log.info("######>>> wifi未连接")
        else:
            SSID = re.search('SSID:\s\w+', mWifiInfo).group()
            IP_addr = \
                subprocess_getoutput('adb -s %s shell dumpsys wifi | findstr ip_address' % dev()).strip().split(
                    '\n')[-1]
            WLAN_MAC = subprocess_getoutput(
                'adb -s %s shell dumpsys wifi | findstr p2p_device_address' % dev()).strip().split('\n')[-1]
            self.log.debug("SSID:%s IP_addr:%s WLAN_MAC:%s" % (SSID, IP_addr, WLAN_MAC))
            if key == 'SSID':
                self.TextBrowser_AP_recv.append(SSID)
            elif key == 'IP_addr':
                self.TextBrowser_AP_recv.append(IP_addr)
            elif key == 'WLAN_MAC':
                self.TextBrowser_AP_recv.append(WLAN_MAC)

    def wifi_info(self):
        """
        AP 打印已连接wifi详细状态
        :return: None
        """
        self.log.info("######>>> wifi info")
        if dev() != 0:
            wifi_code = self._wifi_status()
            if wifi_code == 1:
                mWifiInfo = subprocess_getoutput('adb -s %s shell dumpsys wifi | findstr mWifiInfo' %
                                                 dev()).strip().split('\n')[0]
                if 'null' in mWifiInfo:
                    self.TextBrowser_AP_recv.append("WiFi未连接\n")
                else:
                    self.TextBrowser_AP_recv.append("\n")
                    IP_info = subprocess_getoutput('adb -s %s shell dumpsys wifi | findstr ip_address' %
                                                   dev()).strip().split('\n')[-1]
                    IP_addr = ' ' + IP_info[:10] + ':' + IP_info[11:]
                    wifiInfo_list = mWifiInfo.split(',')
                    wifiInfo_list.insert(1, IP_addr)
                    for item in wifiInfo_list:
                        self.TextBrowser_AP_recv.append(item)
                    self.TextBrowser_AP_recv.append("\n")
            elif wifi_code == 0:
                self.TextBrowser_AP_recv.append("WiFi状态: 关闭\n")
                self.log.info("######>>> check wifi status: closed")
            elif wifi_code == 2:
                self.TextBrowser_AP_recv.append("WiFi状态异常\n")
        else:
            self.TextBrowser_AP_recv.append("无设备连接")






    def get_locallog(self):
        thread_getlog = threading.Thread(target=self._get_locallog)
        thread_getlog.start()

    def _get_locallog(self):
        """
        AP 获取设备data/local/log目录下log到本地/logs/
        :return: None
        """
        self.log.info("######>>> get local log")
        if dev() != 0:
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

    # def AP_select_runTest(self):
    #     """
    #     AP测试项选择
    #     :return: None
    #     """
    #     if self.TEST_FLAG == False:
    #         self.TEST_FLAG = True
    #
    #     select_test = self.ap_test_combobox.currentText()
    #     if dev() != 0:
    #         times_text = self.Edit_test_count_AP.text()
    #         if times_text == '':
    #             with open(self.config_path, 'r', encoding='utf-8') as f:
    #                 config = json.load(f)
    #                 times_text = config['Test_times']
    #         elif times_text.isdigit():
    #             pass
    #         if select_test == "reboot重启":
    #             t1 = threading.Thread(target=self.reboot, args=(times_text,))
    #             t1.start()
    #         elif "ZBK" in select_test:
    #             t1 = threading.Thread(target=self.zbk_reboot, args=(times_text,))
    #             t1.start()
    #     else:
    #         self.TextBrowser_AP_recv.append("无设备连接或未选择测试项")
    #         self.log.info("无设备连接或未选择测试项")

    def ap_clear_recv(self):
        # 清楚AP接收区内容
        self.TextBrowser_AP_recv.clear()

    def ap_clear_send(self):
        # 清除AP发送区内容
        self.textEdit_number.clear()

    def dial(self):
        """
        AP Tab 拨号
        :return: None
        """
        if dev() != 0:

            number = self.textEdit_number.text().strip()
            self.log.debug("deviceName: {}  dial number:{}".format(dev(), number))
            if len(number) == 0:
                self.TextBrowser_AP_recv.append("电话号码不能为空")
            elif number.isdigit():
                subprocess_call(
                    "adb -s %s shell am start -a android.intent.action.CALL -d tel:%s" % (dev(), number))

                self.TextBrowser_AP_recv.append("正在拨号：{}\r\n".format(number))
            else:
                self.TextBrowser_AP_recv.append("电话号码必须为数字")
        else:
            self.TextBrowser_CP_recv.append("无设备连接")

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

    def _prepare_AT(self):
        """
        导入/config/config.cfg中AT指令
        :return: None
        """
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f, strict=False)
                AT_list = config['AT_list']
                interval = config['interval']
                number = config['number']
                assert interval, number

                for line in AT_list:
                    self.ComboBox_at_select.addItem(line.strip())

        except Exception:
            info = {
                "number": "18701997306",
                "content": "AT",
                "Test_times": "3",
                "interval": "5",
                "AT_list": ["AT", "AT+CFUN?", "AT+CREG?", "AT^DMSN", "AT+CGMR"]
            }

            with open(self.config_path, 'w', encoding='utf-8') as fp:
                json.dump(info, fp=fp, indent=4, ensure_ascii=False)
                # self._prepare_AT()
        # except (JSONDecodeError, TypeError) as e:
        #     self.log.error("配置文件出现问题，请删除配置文件重新打开程序（会自动生成新配置文件）")

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

        self.log.debug("Port list:%s" % self.Com_Dict)
        if len(self.Com_Dict) == 0:
            self.ComboBox_port_select.setCurrentText("无串口")

    def port_open(self):
        """
        打开串口
        :return: None
        """
        self.log.info("######>>> Open port")
        self.ser.port = self.ComboBox_port_select.currentText()
        self.ser.baudrate = int(self.ComboBox_baudrate.currentText())
        self.log.info("Port:%s  baudrate:%s  bytesize:8  parity:N  stopbits:1" % (self.ser.port, self.ser.baudrate))
        try:
            self.ser.open()
            self.__exec_cmd('AT^DSCI=1')
        except:
            QMessageBox.critical(self, "Port Error", "此串口不能被打开！")
            return None

        # 每隔0.003s执行一次接收
        self.timer.start(3)
        if self.ser.is_open:
            self.Btn_port_open.setEnabled(False)
            self.Btn_port_close.setEnabled(True)
            self.GroupBox_CP_test.setTitle("串口状态（已开启） %s" % self.ser.name)

    def port_close(self):
        """
        CP 关闭串口
        :return:
        """
        self.log.info("######>>> Close port")
        try:
            self.ser.close()
        except:
            pass
        self.Btn_port_open.setEnabled(True)
        self.Btn_port_close.setEnabled(True)
        self.GroupBox_CP_test.setTitle("串口状态（已关闭）")

    def refresh_at_combobox(self):
        """
        CP 刷新AT下拉框
        :return:
        """
        self.ComboBox_at_select.clear()
        self.ComboBox_at_select.addItem("刷新")
        with open(self.config_path, 'r', encoding='utf-8') as f:
            AT_list = json.load(f)['AT_list']
            for line in AT_list:
                self.ComboBox_at_select.addItem(line.strip())

        self.log.debug("######>>> Refresh at combobox")

    def exec_choose_at(self):
        """
        执行选择的
        :return:
        """
        at_cmd = self.ComboBox_at_select.currentText()
        if at_cmd != "刷新":
            if self.ser.is_open:
                self.RECV_FLAG = True
                self.__exec_cmd(at_cmd)
                self.log.info("exec AT combobox：{}".format(at_cmd))
        else:
            self.refresh_at_combobox()

    def data_send(self):
        """
        串口发送数据
        :return:
        """
        if self.ser.is_open:
            at_cmd = self.CP_send_textEdit.toPlainText().strip()
            self.RECV_FLAG = True
            if at_cmd != "":
                # 非空字符串
                input_s = (at_cmd + '\r\n').encode('utf-8')
                self.ser.write(input_s)
                self.log.info("Send At Cmd: %s" % at_cmd)
        else:
            self.log.warning("终端连接状态异常")

    def data_receive(self):
        """
        串口接收数据
        :return:
        """
        try:
            if self.ser.inWaiting():

                data = self.ser.read(self.ser.inWaiting())
                self.log.debug("Receive data:%s" % data.decode('utf-8', "ignore"))

                # 检查是否有关键log
                self.call_check(str(data))
                if self.RECV_FLAG == True:
                    self.TextBrowser_CP_recv.insertPlainText(data.decode('utf-8', "ignore"))
                recv_to_bottom(self)
            else:
                pass
        except SerialException:
            if self.ser.is_open:
                self.port_close()

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

    def run_test_choice_cp(self):
        """
        CP 执行测试选项
        """
        self.RECV_FLAG = False
        self.__exec_cmd("AT+CREG?")
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
                self.TextBrowser_CP_recv.append("未选择测试项")

        else:
            self.log.warning("串口未打开")

    def __exec_cmd(self, cmd):
        """
        执行AT指令
        :param cmd: AT指令
        """
        cmd1 = (cmd + '\r\n').encode('utf-8')
        try:
            self.ser.write(cmd1)
            self.log.info("exec >> " + cmd)
        except SerialException:
            self.log.warning("Attempting to use a port that is not open")
            self.TextBrowser_CP_recv.append("终端状态异常")

    def call_check(self, line):
        """
        通话测试关键词
        :param line: 接收的数据
        """
        with open(self.config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        number = config['number']
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
        self.TextBrowser_CP_recv.append("测试项：主叫主挂 测试次数:%s" % times)
        self.RECV_FLAG = False
        current_process = ['拨号', '对端振铃', '对端接听', '通话结束']

        self.log.debug("Test times: %s" % times)
        for i in range(int(times)):
            recv_to_bottom(self)
            if self.TEST_FLAG and self.NETWORK_REGISTERED == True:
                self.process.clear()
                time.sleep(interval)
                self.TextBrowser_CP_recv.append("主叫主挂 >> 第%s次, 共 %s次" % (i + 1, times))
                self.__exec_cmd('ATD%s;' % number)

                self.log.info("主叫主挂 >> 第%s次, 共%s次," % (i + 1, times))

                while True:
                    try:
                        time.sleep(3)
                        self.log.debug("dial process: %s" % self.process)
                        if self.process[-1] == "对端接听":
                            # 等待5s超时，自动挂断
                            time.sleep(5)
                            self.__exec_cmd('AT+CHUP')

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
                        self.TextBrowser_CP_recv.append("测试停止，请检查设备入网状态")
                        fail_calling_to_answer += 1
                        break

            else:
                i -= 1
                self.TextBrowser_CP_recv.append("网络未注册")
                break
        self.TEST_FLAG = False
        self.TextBrowser_CP_recv.append("测试项：主叫主挂 测试次数: %d, pass: %d, fail: %d\r\n" %
                                        (i + 1, pass_calling_to_answer, fail_calling_to_answer))
        recv_to_bottom(self)

        self.log.info("测试项：主叫主挂 测试次数: %d, pass: %d, fail: %d\r\n" %
                      (i + 1, pass_calling_to_answer, fail_calling_to_answer))

    def _caller_hangs_up(self, times, number, interval):
        """
        测试项——主叫被挂，终端主叫，对端接听接听后，对端主动挂断
        :param times: 测试次数
        :param number: 对端号码
        :return: None
        """
        global starttime
        pass_hangs_up = 0
        fail_hangs_up = 0
        self.TextBrowser_CP_recv.append("测试项：主叫被挂 测试次数:%s" % times)
        self.RECV_FLAG = False
        current_process = ['拨号', '对端振铃', '对端接听', '通话结束']

        self.log.debug("Test times:%s" % times)
        for i in range(int(times)):
            recv_to_bottom(self)
            if self.TEST_FLAG and self.NETWORK_REGISTERED == True:
                self.process.clear()
                time.sleep(interval)
                self.TextBrowser_CP_recv.append("主叫被挂 >> 第%s次, 共%s次," % (i + 1, times))
                self.__exec_cmd('ATD%s;' % number)
                self.log.info("主叫被挂 >> 第%s次, 共%s次," % (i + 1, times))

                while True:
                    try:
                        time.sleep(3)
                        self.log.debug("dial process: %s" % self.process)
                        if self.process[-1] == "对端接听":
                            starttime = time.time()
                        elif self.process[-1] == "通话结束":
                            endtime = time.time()
                            if self.process == current_process:
                                # 如果挂断时间小于70s，属对端挂断
                                if endtime - starttime < 200:
                                    pass_hangs_up += 1
                                    self.log.info("通话流程为正确流程：{}".format(self.process))
                                else:
                                    fail_hangs_up += 1
                                    self.log.warning("主叫拒接：通话")
                            else:
                                fail_hangs_up += 1
                                self.log.warning("通话流程有误：{}".format(self.process))
                            break
                    except IndexError:
                        self.log.error("拨打失败，请检查是被是否入网")
                        self.TextBrowser_CP_recv.append("测试停止，请检查设备入网状态")
                        fail_hangs_up += 1
                        self.TEST_FLAG = False
                        break
            else:
                i -= 1
                self.TextBrowser_CP_recv.append("网络未注册")
                break
        self.TEST_FLAG = False
        self.TextBrowser_CP_recv.append("测试项：主叫被挂 测试次数:%d, pass:%d, fail:%d\r\n" %
                                        (i + 1, pass_hangs_up, fail_hangs_up))
        recv_to_bottom(self)
        self.log.info("测试项：主叫被挂 测试次数:%d, pass:%d, fail:%d\r\n" %
                      (i + 1, pass_hangs_up, fail_hangs_up))

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
        self.TextBrowser_CP_recv.append("测试项：主叫拒接 测试次数:%s" % times)
        self.RECV_FLAG = False
        current_process = ['拨号', '对端振铃', '通话结束']

        self.log.debug("Test times:%s" % times)
        for i in range(int(times)):
            recv_to_bottom(self)
            if self.TEST_FLAG and self.NETWORK_REGISTERED == True:
                time.sleep(interval)
                self.process.clear()
                self.TextBrowser_CP_recv.append("主叫拒接 >> 第%s次, 共%s次," % (i + 1, times))
                self.__exec_cmd('ATD%s;' % number)
                self.log.info("主叫拒接 >> 第%s次, 共%s次," % (i + 1, times))

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
                        self.TextBrowser_CP_recv.append("测试停止，请检查设备入网状态")
                        fail_calling_reject += 1
                        self.TEST_FLAG = False
                        break
            else:
                i -= 1
                self.TextBrowser_CP_recv.append("网络未注册")
                break
        self.TEST_FLAG = False
        self.TextBrowser_CP_recv.append("测试项：主叫拒接 测试次数:%s, pass:%d, fail:%d\r\n" %
                                        (i + 1, pass_calling_reject, fail_calling_reject))
        recv_to_bottom(self)
        self.log.info("测试项：主叫拒接 测试次数:%d, pass:%d, fail:%d\r\n" %
                      (i + 1, pass_calling_reject, fail_calling_reject))

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
        self.TextBrowser_CP_recv.append("测试项：主叫未接 测试次数:%s" % times)
        self.RECV_FLAG = False
        # current_process = ['拨号', '对端振铃', '对端无应答, 通话结束']
        current_process = ['拨号', '对端振铃', '通话结束']

        self.log.debug("Test times: %s" % times)
        for i in range(int(times)):
            recv_to_bottom(self)
            if self.TEST_FLAG and self.NETWORK_REGISTERED == True:
                self.process.clear()
                time.sleep(interval)
                self.TextBrowser_CP_recv.append("主叫未接 >> 第%s次, 共%s次," % (i + 1, times))
                self.__exec_cmd('ATD%s;' % number)
                self.log.info("主叫未接 >> 第%s次, 共%s次," % (i + 1, times))

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
                        self.TextBrowser_CP_recv.append("测试停止，请检查设备入网状态")
                        fail_no_caller_answer += 1
                        self.TEST_FLAG = False
                        break
            else:
                i -= 1
                self.TextBrowser_CP_recv.append("网络未注册")
                break
        self.TEST_FLAG = False
        self.TextBrowser_CP_recv.append("测试项：主叫未接 测试次数:%s, pass:%d, fail:%d\r\n" %
                                        (i + 1, pass_no_caller_answer, fail_no_caller_answer))
        recv_to_bottom(self)
        self.log.info("测试项：主叫未接 测试次数:%s, pass:%d, fail:%d\r\n" %
                      (i + 1, pass_no_caller_answer, fail_no_caller_answer))
