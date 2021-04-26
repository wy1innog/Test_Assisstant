import subprocess
import re
import time


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
        reboot_timeout = 60
        subprocess.run('adb reboot')
        start_time = time.time()
        print("start time: {}".format(start_time))

        if self.getDev() == 1:
            while time.time()-start_time <= reboot_timeout:
                ensure_boot = subprocess.getoutput('adb shell dumpsys power | findstr mBootCompleted')
                if 'true' in ensure_boot:
                    end = time.time()
                    print("end time: {}".format(end))
                    print("reboot take time: {}".format(end-start_time))
                    break

                else:
                    time.sleep(5)
            else:
                print("reboot超时")
        else:
            print("未连接设备或连接多个设备")

