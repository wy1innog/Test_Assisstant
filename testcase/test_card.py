class Test_Card:
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