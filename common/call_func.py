import subprocess
import time

import Word
from common.log import Log
from common.normal_func import Normal_func


class Call_func(object):
    def __init__(self):
        self.log = Log(__name__).getlog()

    @classmethod
    def testReady(cls):
        call_config = Normal_func.getConfig()['config_call']
        Word.call_process.clear()
        return call_config

    def dial(self, number):
        nf = Normal_func()
        nf.exec_cmd('ATD{};'.format(number))
        starttime = time.time()
        self.log.debug("拨号开始时间: {}".format(starttime))
        time.sleep(3)
        return nf, starttime

    def cp_calling_to_answer(self) -> int:
        """
        Pass Condition:
            - 总体时间未超时
            - 通话时长>= 保持时间
            - ["拨号", "对端响铃", "对端接听", "通话结束"]

        pass:
​	        拨号成功后对端振铃，对端接听，通话时长>=保持时长，终端主动挂断  return 0
        fail:
            拨号失败 return 1
​	        拨号成功后对端振铃，未接听，直至超时  return 2
​	        拨号成功后对端振铃，对端拒接 return 3
​	        拨号成功后对端振铃，对端接听，通话时长低于保持时长,电话挂断 return 4

        :return:
        """
        call_config = Call_func.testReady()
        timeout = int(call_config['call_timeout'])
        hold_time = int(call_config['call_hold'])

        nf, starttime = self.dial(call_config['call_number'])

        while time.time() - starttime < timeout:
            time.sleep(1)
            self.log.debug("process:{}".format(Word.call_process))
            if Word.call_process != ["Error"] or Word.call_process == ['拨号', '通话结束']:

                if Word.call_process == ["拨号", "对端振铃", "通话结束"]:
                    # 对端拒接
                    return 3
                elif Word.call_process == ["拨号", "对端振铃", "对端接听"]:
                    print("==========对端接听")
                    real_holdtime = time.time()
                    while True:
                        if time.time() - real_holdtime < hold_time and Word.call_process[-1] == "通话结束":
                            # 对端接听，通话时长少于保持时长且已挂断
                            return 4
                        elif time.time() - real_holdtime >= hold_time:
                            # pass
                            nf.exec_cmd('AT+CHUP')
                            time.sleep(3)
                            return 0
            else:
                # 拨号失败
                return 1
        # 超时
        return 2

    def cp_caller_hangs_up(self) -> int:
        """
        Pass Condition：
            - 总体时间未超时
            - 通话时长>=保持时长，对端挂断电话
            - ["拨号", "对端响铃", "对端接听", 通话结束"]

        pass：
​	        拨号成功后对端响铃，对端接听，通话时长>=保持时长，对端挂断电话  return 0
        fail：
​	        拨号失败 return 1
​	        拨号成功后对端响铃，未接听，直至超时 return 2
​	        拨号后对端响铃，对端拒接 return 3
​	        拨号成功后对端响铃，对端接听，通话时长低于保持时长，挂断电话 return 4

        :return:
        """
        call_config = Call_func.testReady()
        timeout = int(call_config['call_timeout'])
        hold_time = int(call_config['call_hold'])

        nf, starttime = self.dial(call_config['call_number'])

        while time.time() - starttime < timeout:
            time.sleep(1)
            self.log.debug("process:{}".format(Word.call_process))

            if Word.call_process != ["Error"]:

                if Word.call_process == ["拨号", "对端振铃", "通话结束"]:
                    # 对端拒接
                    return 3
                elif Word.call_process == ["拨号", "对端振铃", "对端接听"]:
                    real_holdtime = time.time()
                    while True:
                        if real_holdtime < hold_time and Word.call_process[-1] == "通话结束":
                            # 对端接听，通话时长少于保持时长且已挂断
                            return 4
                        elif real_holdtime >= hold_time:
                            # pass
                            subprocess.call('adb shell input keyevent KEYCODE_ENDCALL')
                            time.sleep(3)
                            return 0

                else:
                    self.log.debug("pass process: {}".format(Word.call_process))
            else:
                # 拨号失败
                return 1
        # 超时
        return 2

    def cp_call_reject(self) -> int:
        """
        Pass Condition:
        - 总体时间未超时
        - 预设值时长 <= 响铃时长 < 超时时长
        - ["拨号", "对端响铃", 通话结束"]

        pass:
​		    拨号后对端响铃，对端拒接 return 0
        fail:
​	        拨号失败 return 1
​	        拨号成功后对端响铃，未接听，直至超时 return 2
​	        拨号成功后对端响铃，对端接听 return 3
​	        拨号成功后对端响铃，响铃时长 < 响铃预设值，通话结束 return 4
        :return:
        """

        call_config = Call_func.testReady()
        timeout = int(call_config['call_timeout'])
        ring_time = int(call_config['call_ring'])

        nf, starttime = self.dial(call_config['call_number'])

        while time.time() - starttime < timeout:
            process = Word.call_process
            self.log.debug("process:{}".format(process))
            if process != ["Error"]:

                if process == ["拨号", "对端振铃"]:
                    real_ringtime = time.time()
                    self.log.debug("开始振铃时间；{}".format(real_ringtime))
                    while True:

                        if time.time() - real_ringtime < ring_time and process[-1] == "通话结束":
                            # 对端振铃，振铃时长小于预设值
                            return 4
                        elif time.time() - real_ringtime >= ring_time:
                            # pass
                            subprocess.call('adb shell input keyevent KEYCODE_ENDCALL')
                            time.sleep(3)
                            return 0
                        elif process[-1] == "对端接听":
                            # 对端接听
                            return 3
                else:
                    self.log.debug("pass process: {}".format(process))

            else:
                # 拨号失败
                return 1
        # 超时
        return 2

    def cp_call_no_answer(self) -> list:
        """
        Pass Condition:
            - 总体时间未超时
            - 预设值时长 <= 响铃时长 < 超时时长
            - ["拨号", "对端响铃", 通话结束"]

        pass：
​	        拨号成功后对端响铃，未接听，直至超时 return 0
        fail:
​	        拨号失败 return 1
​	        拨号后对端响铃，对端拒接 return 2
​	        拨号成功后对端响铃，对端接听 return 3
​	        拨号成功后对端响铃，响铃时长 < 响铃超时时间,通话结束 return 4
        :return:
        """
        call_config = Call_func.testReady()
        timeout = int(call_config['call_timeout'])
        ring_timeout = int(call_config['call_ringtimeout'])

        nf, starttime = self.dial(call_config['call_number'])

        while time.time() - starttime < timeout:
            process = Word.call_process
            self.log.debug("process:{}".format(process))
            if process != ["Error"]:
                if process == ["拨号", "对端振铃", "对端接听"]:
                    # 对端接听
                    return 3

                elif process == ["拨号", "对端振铃"]:
                    real_ringtime = time.time()
                    self.log.debug("开始振铃时间；{}".format(real_ringtime))
                    while True:

                        if time.time() - real_ringtime < ring_timeout and process[-1] == "通话结束":
                            # 对端振铃，振铃时长小于预设值
                            return 4
                        elif time.time() - real_ringtime >= ring_timeout:
                            # pass
                            if process == ["拨号", "对端振铃", "通话结束"]:
                                return 0
                            else:
                                self.log.debug("主叫未接，已振铃{}".format(time.time() - real_ringtime))
                else:
                    self.log.debug("pass process: {}".format(process))
            else:
                # 拨号失败
                return 1
        # 超时
        return 2
