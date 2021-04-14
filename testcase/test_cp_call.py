import sys

# from mainpage import Test_func

sys.path.append("..")
from common.log import Log
from common.call_func import Call_func

class Test_Call:

    def __init__(self):
        self.log = Log(__name__).getlog()
        print("入网准备")
        #todo:测试前的执行步骤，入网
        pass

    # pytest --count 3 test_cp_call.py
    # @pytest.mark.repeat(3)

    def test_calling_to_answer(self, times=1):
        """
        主叫主挂，终端主叫，对端接听后，终端主动挂断
        :param times: 测试次数
        :param number: 对端号码
        :return: None
        """
        call_func = Call_func()
        for i in range(int(times)):
            current_process = ['拨号', '对端振铃', '对端接听', '通话结束']
            process = call_func.cp_calling_to_answer()

            self.log.info("test process: %s"% process)
            assert process == current_process
            self.log.info("主叫主挂测试pass")



    def test_caller_hangs_up(self, times=1):
        """
        主叫被挂，终端主叫，对端接听接听后，对端主动挂断
        :param times: 测试次数
        :param number: 对端号码
        :return: None
        """
        call_func = Call_func()
        for i in range(int(times)):
            current_process = ['拨号', '对端振铃', '对端接听', '通话结束']
            process = call_func.cp_caller_hangs_up()
            print("test process: %s"% process)
            # self.log.info("test process: %s"% process)
            assert process == current_process
            # self.log.info("主叫被挂pass")

    def test_call_reject(self, times=1):
        """
        测试项——主叫拒接，终端主叫，对端挂断
    #   :param times: 测试次数
    #   :param number: 对端号码
    #   :return: None
        """
        call_func = Call_func()
        for i in range(int(times)):
            current_process = ['拨号', '对端振铃', '通话结束']
            process = call_func.cp_call_reject()

            self.log.info("test process: %s" % process)
            try:
                assert process == current_process
                self.log.info("主叫拒接pass")
            except AssertionError:
                self.log.warning("主叫拒接failed")


    def test_call_no_answer(self, times=1):
        """
        测试项——主叫未接，终端主叫，对端不予接听
        :param times: 测试次数
        :param number: 对端号码
        :return: None
        """
        call_func = Call_func()
        for i in range(int(times)):
            current_process = ['拨号', '对端振铃', '通话结束']
            process = call_func.cp_call_no_answer()

            self.log.info("test process: %s" % process)
            assert process == current_process
            self.log.info("主叫未接pass")


    # def _caller_hangs_up(self, times, number, interval):
    #
    #     global starttime
    #     pass_hangs_up = 0
    #     fail_hangs_up = 0
    #     self.TextBrowser_CP_recv.append("测试项：主叫被挂 测试次数:%s" % times)
    #     self.RECV_FLAG = False
    #
    #
    #     self.log.debug("Test times:%s" % times)
    #     for i in range(int(times)):
    #         recv_to_bottom(self)
    #         if self.TEST_FLAG and self.NETWORK_REGISTERED == True:
    #             self.process.clear()
    #             time.sleep(interval)
    #             self.TextBrowser_CP_recv.append("主叫被挂 >> 第%s次, 共%s次," % (i + 1, times))
    #             self.__exec_cmd('ATD%s;' % number)
    #             self.log.info("主叫被挂 >> 第%s次, 共%s次," % (i + 1, times))
    #
    #             while True:
    #                 try:
    #                     time.sleep(3)
    #                     self.log.debug("dial process: %s" % self.process)
    #                     if self.process[-1] == "对端接听":
    #                         starttime = time.time()
    #                     elif self.process[-1] == "通话结束":
    #                         endtime = time.time()
    #                         if self.process == current_process:
    #                             # 如果挂断时间小于70s，属对端挂断
    #                             if endtime - starttime < 200:
    #                                 pass_hangs_up += 1
    #                                 self.log.info("通话流程为正确流程：{}".format(self.process))
    #                             else:
    #                                 fail_hangs_up += 1
    #                                 self.log.warning("主叫拒接：通话")
    #                         else:
    #                             fail_hangs_up += 1
    #                             self.log.warning("通话流程有误：{}".format(self.process))
    #                         break
    #                 except IndexError:
    #                     self.log.error("拨打失败，请检查是被是否入网")
    #                     self.TextBrowser_CP_recv.append("测试停止，请检查设备入网状态")
    #                     fail_hangs_up += 1
    #                     self.TEST_FLAG = False
    #                     break
    #         else:
    #             i -= 1
    #             self.TextBrowser_CP_recv.append("网络未注册")
    #             break
    #     self.TEST_FLAG = False
    #     self.TextBrowser_CP_recv.append("测试项：主叫被挂 测试次数:%d, pass:%d, fail:%d\r\n" %
    #                                     (i + 1, pass_hangs_up, fail_hangs_up))
    #     recv_to_bottom(self)
    #     self.log.info("测试项：主叫被挂 测试次数:%d, pass:%d, fail:%d\r\n" %
    #                   (i + 1, pass_hangs_up, fail_hangs_up))
    #
    # def _calling_reject(self, times, number, interval):
    #     """
    #     测试项——主叫拒接，终端主叫，对端挂断
    #     :param times: 测试次数
    #     :param number: 对端号码
    #     :return: None
    #     """
    #     global i
    #     pass_calling_reject = 0
    #     fail_calling_reject = 0
    #     self.TextBrowser_CP_recv.append("测试项：主叫拒接 测试次数:%s" % times)
    #     self.RECV_FLAG = False
    #     current_process = ['拨号', '对端振铃', '通话结束']
    #
    #     self.log.debug("Test times:%s" % times)
    #     for i in range(int(times)):
    #         recv_to_bottom(self)
    #         if self.TEST_FLAG and self.NETWORK_REGISTERED == True:
    #             time.sleep(interval)
    #             self.process.clear()
    #             self.TextBrowser_CP_recv.append("主叫拒接 >> 第%s次, 共%s次," % (i + 1, times))
    #             self.__exec_cmd('ATD%s;' % number)
    #             self.log.info("主叫拒接 >> 第%s次, 共%s次," % (i + 1, times))
    #
    #             while True:
    #                 try:
    #                     time.sleep(3)
    #                     self.log.debug("dial process: %s" % self.process)
    #                     if "通话结束" in self.process[-1]:
    #                         if self.process == current_process:
    #                             pass_calling_reject += 1
    #                             self.log.info("通话流程为正确流程：{}".format(self.process))
    #                         else:
    #                             fail_calling_reject += 1
    #                             self.log.warning("通话流程有误：{}".format(self.process))
    #                         break
    #                 except IndexError:
    #                     self.log.error("拨打失败，请检查是被是否入网")
    #                     self.TextBrowser_CP_recv.append("测试停止，请检查设备入网状态")
    #                     fail_calling_reject += 1
    #                     self.TEST_FLAG = False
    #                     break
    #         else:
    #             i -= 1
    #             self.TextBrowser_CP_recv.append("网络未注册")
    #             break
    #     self.TEST_FLAG = False
    #     self.TextBrowser_CP_recv.append("测试项：主叫拒接 测试次数:%s, pass:%d, fail:%d\r\n" %
    #                                     (i + 1, pass_calling_reject, fail_calling_reject))
    #     recv_to_bottom(self)
    #     self.log.info("测试项：主叫拒接 测试次数:%d, pass:%d, fail:%d\r\n" %
    #                   (i + 1, pass_calling_reject, fail_calling_reject))
    #
    # def _no_caller_answer(self, times, number, interval):
    #     """
    #     测试项——主叫未接，终端主叫，对端不予接听
    #     :param times: 测试次数
    #     :param number: 对端号码
    #     :return: None
    #     """
    #     global i
    #     pass_no_caller_answer = 0
    #     fail_no_caller_answer = 0
    #     self.TextBrowser_CP_recv.append("测试项：主叫未接 测试次数:%s" % times)
    #     self.RECV_FLAG = False
    #     # current_process = ['拨号', '对端振铃', '对端无应答, 通话结束']
    #     current_process = ['拨号', '对端振铃', '通话结束']
    #
    #     self.log.debug("Test times: %s" % times)
    #     for i in range(int(times)):
    #         recv_to_bottom(self)
    #         if self.TEST_FLAG and self.NETWORK_REGISTERED == True:
    #             self.process.clear()
    #             time.sleep(interval)
    #             self.TextBrowser_CP_recv.append("主叫未接 >> 第%s次, 共%s次," % (i + 1, times))
    #             self.__exec_cmd('ATD%s;' % number)
    #             self.log.info("主叫未接 >> 第%s次, 共%s次," % (i + 1, times))
    #
    #             while True:
    #                 time.sleep(3)
    #                 self.log.debug("dial process: %s" % self.process)
    #                 try:
    #                     if self.process[-1] == "通话结束":
    #                         if self.process == current_process:
    #                             pass_no_caller_answer += 1
    #                             self.log.info("通话流程为正确流程：{}".format(self.process))
    #                         else:
    #                             fail_no_caller_answer += 1
    #                             self.log.warning("通话流程有误：{}".format(self.process))
    #                         break
    #
    #                     # timeout
    #                 except IndexError:
    #                     self.log.error("拨打失败，请检查是被是否入网")
    #                     self.TextBrowser_CP_recv.append("测试停止，请检查设备入网状态")
    #                     fail_no_caller_answer += 1
    #                     self.TEST_FLAG = False
    #                     break
    #         else:
    #             i -= 1
    #             self.TextBrowser_CP_recv.append("网络未注册")
    #             break
    #     self.TEST_FLAG = False
    #     self.TextBrowser_CP_recv.append("测试项：主叫未接 测试次数:%s, pass:%d, fail:%d\r\n" %
    #                                     (i + 1, pass_no_caller_answer, fail_no_caller_answer))
    #     recv_to_bottom(self)
    #     self.log.info("测试项：主叫未接 测试次数:%s, pass:%d, fail:%d\r\n" %
    #                   (i + 1, pass_no_caller_answer, fail_no_caller_answer))