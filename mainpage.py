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

from serial import SerialTimeoutException, SerialException

from common.Ass_util import subprocess_getoutput, subprocess_call, dev, recv_to_bottom

parent_path = os.path.dirname(sys.path[0])
if parent_path not in sys.path:
    sys.path.append(parent_path)

from ui.ui_mainpage import Ui_MainWindow
from atpage import At_settings
from settingspage import Default_settings
from common.log import Log


class Ass(QMainWindow, QComboBox, Ui_MainWindow):
    config_path = 'config/config.cfg'

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



    def initUI(self):
        self.setWindowTitle("Test Assistant")
        icon = 'img\icon.ico'
        self.setWindowIcon(QIcon(icon))
        self.actionAT_manager.triggered.connect(self.refresh_at_combobox)

        self.btn_dev_check.clicked.connect(self.dev_check)
        self.btn_btStatus.clicked.connect(self.bt_status)
        self.btn_wifiStatus.clicked.connect(self.wifi_status)
        self.btn_wifiInfo.clicked.connect(self.wifi_info)
        self.btn_simStatus.clicked.connect(self.sim_status)
        self.btn_sdStatus.clicked.connect(self.sdcard_status)
        self.btn_listPkg.clicked.connect(self.list_package)
        self.btn_catchLog.clicked.connect(self.get_locallog)
        self.btn_run_test_ap.clicked.connect(self.run_test_choice_ap)
        self.btn_stop_test_ap.clicked.connect(self.stop_test_ap)
        self.AP_btn_clear_recv.clicked.connect(self.ap_clear_recv)
        self.AP_btn_start.clicked.connect(self.dial)
        self.AP_btn_clear_send.clicked.connect(self.ap_clear_send)

        self.btn_sp_check.clicked.connect(self.port_check)
        self.btn_sp_open.clicked.connect(self.port_open)
        self.btn_sp_close.clicked.connect(self.port_close)
        self.btn_at_exec.clicked.connect(self.exec_choose_at)

        self.btn_run_test.clicked.connect(self.run_test_choice_cp)
        self.btn_stop_test.clicked.connect(self.stop_test_cp)
        self.CP_btn_start.clicked.connect(self.data_send)
        self.CP_btn_clear_recv.clicked.connect(self.cp_clear_recv)
        self.CP_btn_clear_send.clicked.connect(self.cp_clear_send)

    def stop_test_ap(self):
        if self.TEST_FLAG == True:
            self.TEST_FLAG = False
            self.AP_recv_textBrowser.append("测试被强制停止！！！本次测试结束后终止测试")
            self.log.warning("force stop test !!!")
        else:
            pass

        # 打印当前连接的设备

    def check_device(self):
        pattern = re.compile('[a-zA-Z0-9]+\sdevice$')
        devices_list = subprocess_getoutput('adb devices').strip().split('\n')
        self.log.debug('######>>> Devices: %s' % devices_list[1:])
        devices_count = 0
        for d in devices_list:
            r = pattern.match(d)
            if r:
                devices_count += 1
        if devices_count == 0:
            self.AP_recv_textBrowser.append("No devices/emulators found")
            return 0
        elif devices_count == 1:
            return 1
        else:
            return 2

    def dev_check(self):
        # 检测所有存在的安卓设备
        self.log.info("######>>> Check device")
        self.combox_dev_choice.clear()
        dev_list = []
        result = subprocess_getoutput("adb devices").strip().split("\n")
        for dev in result:
            if "List of devices attached" in dev:
                continue
            if "device" in dev:
                dev_list.append(dev[:-7])

        if len(dev_list) == 0:
            self.combox_dev_choice.addItem("   无设备")
        for dev in dev_list:
            self.combox_dev_choice.addItem(dev)

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
            self.AP_recv_textBrowser.append("Bluetooth status error")
            self.log.warning("Bluetooth status error, flag=%s" % flag)

    def bt_status(self):
        # 打印蓝牙开关状态
        self.log.info("######>>> Bluetooth status")
        if self.check_device() != 0:
            if self._bt_status():
                self.AP_recv_textBrowser.append("蓝牙状态: 开启\n")
            else:
                self.AP_recv_textBrowser.append("蓝牙状态: 关闭\n")

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
        # 打印wifi开关状态
        self.log.info("######>>> wifi status")
        if self.check_device() != 0:
            wifi_code = self._wifi_status()
            if wifi_code == 1:
                self.AP_recv_textBrowser.append("WiFi状态: 开启\n")
                self.AP_recv_textBrowser.append(self._wifi_info('SSID'))
            elif wifi_code == 0:
                self.AP_recv_textBrowser.append("WiFi状态: 关闭\n")
                self.log.info("######>>> check wifi status: closed")
            else:
                self.AP_recv_textBrowser.append("WiFi状态异常\n")

    def _wifi_info(self, key):
        mWifiInfo = \
            subprocess_getoutput('adb -s %s shell dumpsys wifi | findstr mWifiInfo' % dev()).strip().split('\n')[0]
        self.log.debug("wifi info:%s" % mWifiInfo)
        if 'null' in mWifiInfo:
            self.AP_recv_textBrowser.append("WiFi未连接")
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
                self.AP_recv_textBrowser.append(SSID)
            elif key == 'IP_addr':
                self.AP_recv_textBrowser.append(IP_addr)
            elif key == 'WLAN_MAC':
                self.AP_recv_textBrowser.append(WLAN_MAC)

    def wifi_info(self):
        # 打印wifi详细状态
        self.log.info("######>>> wifi info")
        if self.check_device() != 0:
            wifi_code = self._wifi_status()
            if wifi_code == 1:
                mWifiInfo = subprocess_getoutput('adb -s %s shell dumpsys wifi | findstr mWifiInfo' %
                                                 dev()).strip().split('\n')[0]
                if 'null' in mWifiInfo:
                    self.AP_recv_textBrowser.append("WiFi未连接\n")
                else:
                    self.AP_recv_textBrowser.append("\n")
                    IP_info = subprocess_getoutput('adb -s %s shell dumpsys wifi | findstr ip_address' %
                                                   dev()).strip().split('\n')[-1]
                    IP_addr = ' ' + IP_info[:10] + ':' + IP_info[11:]
                    wifiInfo_list = mWifiInfo.split(',')
                    wifiInfo_list.insert(1, IP_addr)
                    for item in wifiInfo_list:
                        self.AP_recv_textBrowser.append(item)
                    self.AP_recv_textBrowser.append("\n")
            elif wifi_code == 0:
                self.AP_recv_textBrowser.append("WiFi状态: 关闭\n")
                self.log.info("######>>> check wifi status: closed")
            elif wifi_code == 2:
                self.AP_recv_textBrowser.append("WiFi状态异常\n")

    def sim_status(self):
        # 打印SIM卡状态
        self.log.info("######>>> SIM status")
        if self.check_device() != 0:
            sim_result = subprocess_getoutput('adb -s %s shell getprop | findstr gsm.sim.state' % dev())
            self.log.debug("SIM status:%s" % sim_result)
            if sim_result == '[gsm.sim.state]: [NOT_READY]\n':
                self.AP_recv_textBrowser.append("Sim卡状态：异常\n")
            elif sim_result == '[gsm.sim.state]: [ABSENT]\n':
                self.AP_recv_textBrowser.append("Sim卡状态：异常\n")
            elif sim_result == '[gsm.sim.state]: [READY]\n':
                self.AP_recv_textBrowser.append("Sim卡状态：正常\n")
            elif sim_result == '[gsm.sim.state]: [LOADED]\n':
                self.AP_recv_textBrowser.append("Sim卡状态：正常\n")
            elif sim_result == '[gsm.sim.state]: [UNKNOWN]\n':
                self.AP_recv_textBrowser.append("Sim卡状态：异常\n")
            elif sim_result == '[gsm.sim.state]: [PIN_REQUIRED]\n':
                self.AP_recv_textBrowser.append("Sim卡状态：锁定状态，需要用户的PIN码解锁\n")
            elif sim_result == '[gsm.sim.state]: [PUK_REQUIRED]\n':
                self.AP_recv_textBrowser.append("Sim卡状态：锁定状态，需要用户的PUK码解锁\n")
            elif sim_result == '[gsm.sim.state]: [NETWORK_LOCKED]\n':
                self.AP_recv_textBrowser.append("Sim卡状态：锁定状态，需要网络的PIN码解锁\n")
            elif sim_result == '[gsm.sim.state]: [LOADED,LOADED]\n':
                self.AP_recv_textBrowser.append("双卡，有钱有钱\n")
            else:
                self.AP_recv_textBrowser.append("check SIM card error!\n")

    def sdcard_status(self):
        # 打印SDcard状态
        self.log.info("######>>> Sdcard status")
        if self.check_device() != 0:
            # 判断/storage/sdcard1下文件夹大小是否为0
            used_storage = subprocess_getoutput('adb -s %s shell du -sH storage/sdcard1' % dev()).split('\t')[0]
            self.log.debug("used_storage:%s" % used_storage)
            # 判断状态栏是否有无SD卡标识
            notif_icon = subprocess_getoutput('adb -s %s shell dumpsys notification | findstr sdcard' % dev())
            self.log.debug("SD card notification: %s" % notif_icon)
            if (used_storage == '0') and ('stat_notify_sdcard_usb' in notif_icon):
                self.AP_recv_textBrowser.append("未插入SD卡\n")
            elif (used_storage != '0') and ('stat_notify_sdcard_usb' not in notif_icon):
                self.AP_recv_textBrowser.append("已识别SD卡\n")
            else:
                self.AP_recv_textBrowser.append("check SD card error!\n")

        # list package

    def list_package(self):
        if self.check_device() != 0:
            listpkg = subprocess_getoutput('adb -s %s shell pm list packages' % dev())
            self.AP_recv_textBrowser.append("已安装应用包名：\n" + listpkg + "\n")

    def get_locallog(self):
        thread_getlog = threading.Thread(target=self._get_locallog)
        thread_getlog.start()

        # 抓取data/local/log目录下文件

    def _get_locallog(self):
        self.log.info("######>>> get local log")
        if self.check_device() != 0:
            self.AP_recv_textBrowser.append("log抓取中……")
            # savelog_path = os.path.dirname(__file__) + '\logs'
            savelog_path = '\logs'
            print("savelog_path: {}".format(savelog_path))
            if not os.path.exists(savelog_path):
                os.makedirs(savelog_path)
            save_dir = os.path.join(savelog_path, '{0:%Y%m%d%H%M%S}'.format(datetime.datetime.now()))

            status = subprocess_call("adb -s %s pull data/local/log %s" % (dev(), save_dir))

            self.log.debug("Pull local log status:%s" % status)

            if status == 0:
                self.AP_recv_textBrowser.append("log抓取完成，已保存至" + save_dir + "\n")
            else:
                self.AP_recv_textBrowser.append("log保存失败，请检查设备状态\n")

    def run_test_choice_ap(self):
        if self.TEST_FLAG == False:
            self.TEST_FLAG = True
            if self.check_device() != 0:
                if self.reboot_test.isChecked():
                    times_text = self.Edit_test_count_AP.text()
                    if times_text == '':
                        with open(self.config_path, 'r', encoding='utf-8') as f:
                            config = json.load(f)
                            times_text = config['Test_times']
                    elif times_text.isdigit():
                        pass
                    t1 = threading.Thread(target=self.run, args=(times_text,))
                    t1.start()
                else:
                    self.log.info("未选择测试项")
        else:
            pass

        # reboot,timeout=120

    def run(self, times):
        global i
        pass_count = 0
        with open(self.config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            config['Test_times'] = times
        self.AP_recv_textBrowser.append("测试项：reboot重启 次数：%s" % times)
        self.log.info("测试项：reboot重启 次数：%s" % times)
        for i in range(int(times)):
            if self.TEST_FLAG == True:
                self.AP_recv_textBrowser.append("reboot重启 >> 第%d次测试 共%s次,正在测试..." % (i + 1, times))
                subprocess_call('adb reboot')

                start = time.time()
                time.sleep(5)
                if dev() == False:
                    while True:
                        timef = time.time()
                        ensure_boot = subprocess_getoutput('adb shell dumpsys power | findstr mBootCompleted')
                        if 'true' in ensure_boot:
                            end = time.time()
                            pass_count += 1
                            self.AP_recv_textBrowser.append("reboot重启 >> 第%d次测试完成，剩余%s次,用时%d seconds" %
                                                            (i + 1, int(times) - (i + 1), end - start))
                            break
                        if timef - start >= 120:
                            self.AP_recv_textBrowser.append("reboot重启 ?? 重启时间超过120s，重启超时！")
                            break
                        recv_to_bottom()
            else:
                pass
        self.AP_recv_textBrowser.append("reboot重启测试完成，测试%d次, pass:%d次\n" % (i + 1, pass_count))
        self.log.info("reboot重启测试结束，测试%d次" % (i + 1))

    def ap_clear_recv(self):
        self.AP_recv_textBrowser.clear()

    def ap_clear_send(self):
        self.textEdit_number.clear()

    def dial(self):
        if self.check_device() != 0:

            number = self.textEdit_number.text().strip()
            self.log.debug("deviceName: {}  dial number:{}".format(dev(), number))
            if len(number) == 0:
                self.AP_recv_textBrowser.append("电话号码不能为空")
            elif number.isdigit():
                subprocess_call(
                    "adb -s %s shell am start -a android.intent.action.CALL -d tel:%s" % (dev(), number))

                self.AP_recv_textBrowser.append("正在拨号：{}\r\n".format(number))
            else:
                self.AP_recv_textBrowser.append("电话号码必须为数字")


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
