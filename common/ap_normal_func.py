import subprocess
import re


class ApNormalFunc:

    @classmethod
    def case_to_func(cls, case):
        ap_case_func_dict = {
            'SD卡检测': 'test_call_to_answer',
            'SIM卡检测': 'test_caller_hangs_up',
            'WIFI开关检测': 'test_call_reject',
            'WIFI连接': 'test_call_no_answer',
            '蓝牙连接': 'test_call_no_answer',
            '蓝牙开关': 'test_call_no_answer',
            '主叫主挂': 'test_call_no_answer',
            '主叫被挂': 'test_call_no_answer',
            '主叫拒接': 'test_call_no_answer',
            '主叫未接': 'test_call_no_answer',
        }
        return ap_case_func_dict.get(case)

    @classmethod
    def getDev(cls):
        """
        检测设备，有设备，返回设备名；无设备，返回0
        :return: 设备名
        :return: 0
        """
        pattern = re.compile('[a-zA-Z0-9]+\sdevice$')
        devices_list = subprocess.getoutput('adb devices').strip().split('\n')
        devName = devices_list[-1].split('\t')[0]
        devices_count = 0
        for d in devices_list:
            r = pattern.match(d)
            if r:
                devices_count += 1
        if devices_count == 0:
            return 0
        elif devices_count == 1:
            return devName
        else:
            return 2

    def open_BT(self):
        # todo:打开蓝牙
        pass

    def close_BT(self):
        # todo: 关闭蓝牙
        pass

    def reboot(self):
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


