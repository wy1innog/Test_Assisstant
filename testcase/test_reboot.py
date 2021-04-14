import time


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
