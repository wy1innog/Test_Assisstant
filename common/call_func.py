import subprocess
import time

import Word
from common.cp_normal_func import CpNormalFunc


class Call_func(object):
    def __init__(self):
        self.log = Word.log[0]

    @classmethod
    def testReady(cls, title):
        call_config = CpNormalFunc.getConfig()[title]
        for item in call_config:
            if call_config[item] == "":
                return 1
            else:
                Word.call_process.clear()
                return call_config

    @classmethod
    def checkConfig(cls, casetitle):
        for case in casetitle:
            configName = CpNormalFunc.case_to_func(case)[5:]

            title_config = Call_func.testReady(configName)
            if title_config != 1:
                return 0
            else:
                return 1


    def dial(self, number):
        nf = CpNormalFunc()
        nf.exec_cmd('ATD{};'.format(number))
        start_time = time.time()
        time.sleep(3)
        return start_time

    def cp_call_to_answer(self) -> int:
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
        call_config = Call_func.testReady("call_to_answer")
        timeout = int(call_config['timeout'])
        pre_hold_time = int(call_config['hold']) - 2

        start_time = self.dial(call_config['number'])
        self.log.debug("wait pre hold time: {}".format(pre_hold_time))

        while time.time() - start_time < timeout:
            self.log.debug("call time: {}".format(time.time() - start_time))

            if Word.call_process == ["拨号", "对端振铃", "对端接听"]:
                answer_time = time.time()
                self.log.debug("answer_time: {}".format(answer_time))
                time.sleep(pre_hold_time)
                hold_time = time.time() - answer_time
                self.log.debug("real hold time: {}".format(hold_time))

                if hold_time >= pre_hold_time and Word.call_process[-1] != "通话结束":
                    # pass
                    CpNormalFunc.chup_up()
                    return 0
                else:
                    # 未达到pre hold time
                    CpNormalFunc.chup_up()
                    return 4
            elif not Word.call_process or Word.call_process[0] == "Error":
                # 拨打失败
                return 1
            elif Word.call_process[-1] == "通话结束":
                # 对端拒接
                return 3
            else:
                time.sleep(2)
        # 超时
        CpNormalFunc.chup_up()
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
        call_config = Call_func.testReady("caller_hangs_up")
        timeout = int(call_config['timeout'])
        pre_hold_time = int(call_config['hold']) - 2
        self.log.debug("pre_hold_time: {}".format(pre_hold_time))

        start_time = self.dial(call_config['number'])
        while time.time() - start_time < timeout:
            self.log.debug("call time: {}".format(time.time() - start_time))

            if Word.call_process == ["拨号", "对端振铃", "对端接听"]:
                answer_time = time.time()
                self.log.debug("answer_time: {}".format(answer_time))
                if Word.call_process[-1] != "通话结束":
                    time.sleep(pre_hold_time + 2)
                    real_hold_time = time.time() - answer_time
                    if real_hold_time >= pre_hold_time and Word.call_process[-1] != "通话结束":
                        serialno = CpNormalFunc.getSerialno()
                        self.log.debug("serialno: {}".format(serialno))
                        if serialno == "unknown":
                            CpNormalFunc.chup_up()
                            return 5
                        else:
                            subprocess.call("adb shell input keyevent KEYCODE_ENDCALL")
                            time.sleep(3)
                            if Word.call_process[-1] == "通话结束":
                                return 0
                    else:
                        # 未达到pre hold time
                        CpNormalFunc.chup_up()
                        return 4
            elif not Word.call_process or Word.call_process[0] == "Error":
                # 拨打失败
                return 1
            elif Word.call_process[-1] == "通话结束":
                # 对端拒接
                return 3
            else:
                time.sleep(2)
        # 超时
        CpNormalFunc.chup_up()
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

        call_config = Call_func.testReady("call_reject")
        timeout = int(call_config['timeout'])
        pre_ring_time = int(call_config['ring_time']) - 2

        start_time = self.dial(call_config['number'])
        while time.time() - start_time < timeout:
            self.log.debug("call time: {}".format(time.time() - start_time))

            if Word.call_process == ["拨号", "对端振铃"]:
                ring_time = time.time()
                self.log.debug("ring_time: {}".format(ring_time))
                time.sleep(pre_ring_time + 2)
                real_ring_time = time.time() - ring_time
                self.log.debug("real ring time: {}".format(real_ring_time))

                if real_ring_time >= pre_ring_time and Word.call_process[-1] != "通话结束":
                    self.log.debug("enter here")
                    # pass
                    serialno = CpNormalFunc.getSerialno()
                    if serialno == "unknown":
                        CpNormalFunc.chup_up()
                        return 5
                    else:
                        subprocess.call("adb shell input keyevent KEYCODE_ENDCALL")
                        self.log.debug("对端挂断")
                        # 手机挂断后，对端语音提示10s，关掉提示
                        time.sleep(10)
                        CpNormalFunc.chup_up()
                        time.sleep(2)
                        if Word.call_process[-1] == "通话结束":
                            return 0
                        else:
                            print("wtf???")
                elif Word.call_process[:3] == ["拨号", "对端振铃", "对端接听"]:
                    CpNormalFunc.chup_up()
                    return 6
                else:
                    CpNormalFunc.chup_up()
                    return 4
            elif not Word.call_process or Word.call_process[0] == "Error" or Word.call_process == ["拨号", "通话结束"]:
                # 拨打失败
                return 1
            else:
                time.sleep(2)
        # 超时
        CpNormalFunc.chup_up()
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
        call_config = Call_func.testReady("call_no_answer")
        if call_config == 0:
            return 6
        else:
            timeout = int(call_config['timeout'])
            pre_ring_timeout = int(call_config['ring_time'])

            start_time = self.dial(call_config['number'])

            while time.time() - start_time < timeout:
                self.log.debug("call time: {}".format(time.time() - start_time))

                if Word.call_process == ["拨号", "对端振铃"]:
                    ring_time = time.time()
                    self.log.debug("ring_time: {}".format(ring_time))
                    time.sleep(pre_ring_timeout)
                    real_ring_time = time.time() - ring_time
                    self.log.debug("real ring time: {}".format(real_ring_time))

                    if real_ring_time >= pre_ring_timeout and Word.call_process[-1] != "通话结束":
                        # pass
                        CpNormalFunc.chup_up()
                        return 0
                    else:
                        return 4
                elif not Word.call_process or Word.call_process[0] == "Error" or Word.call_process == ["拨号", "通话结束"]:
                    # 拨打失败
                    return 1
                else:
                    time.sleep(2)
            # 超时
            CpNormalFunc.chup_up()
            return 2

