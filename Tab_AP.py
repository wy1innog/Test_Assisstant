import datetime
import json
import os
import re
import threading
import time

from PyQt5.QtWidgets import QMainWindow

from common.Ass_util import subprocess_getoutput, dev, subprocess_call, recv_to_bottom
from common.log import Log
from ui.main_ui import Ui_MainWindow


class AP(Ui_MainWindow, QMainWindow):
    config_path = 'config/config.cfg'

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.log = Log(__name__).getlog()
        self.dev_check()

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
