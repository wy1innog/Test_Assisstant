
class test_ap_case:






def test_BT_connect(open_BT, BT_name=123):
    assert BT_name == "hello"

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
        if dev() != 0 and dev() != 2 and self.TEST_FLAG == True:
            pass_count = 0
            timeout = 120
            self.ap_printf("Case——test_reboot: 第%d次测试，共%s次" % (int(current_test_times) + 1, times))
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
                                       (int(current_test_times) + 1, end - start))
                        break

                else:
                    time.sleep(5)
                    end = time.time()
            else:
                self.ap_printf("reboot重启 ?? 重启时间超过120s，重启超时！")

        else:
            self.TextBrowser_AP_recv.append("无设备连接，测试终止")

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
