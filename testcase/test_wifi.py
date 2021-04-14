from common.Ass_util import subprocess_getoutput


class Test_WIFI:
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
