import sys

import Word

sys.path.append("..")
from common.call_func import Call_func

class Test_Call:

    def __init__(self):
        self.log = Word.log[0]
        # todo:测试前的执行步骤，入网检测

    def test_call_to_answer(self):
        """
        主叫主挂，终端主叫，对端接听后，终端主动挂断
        :param times: 测试次数
        :param number: 对端号码
        :return: None
        """
        self.log.info("主叫主挂测试++++")
        call_func = Call_func()
        resultcode = call_func.cp_call_to_answer()

        if resultcode == 1:
            self.log.info("主叫主挂fail——拨号失败\n")
        elif resultcode == 2:
            self.log.info("主叫主挂fail——对端未接听\n")
        elif resultcode == 3:
            self.log.info("主叫主挂fail——对端拒接\n")
        elif resultcode == 4:
            self.log.info("主叫主挂fail——通话时长低于保持时长\n")

        if resultcode == 0:
            Word.pass_case += 1
            self.log.info("主叫主挂pass\n")
            return "pass"
        else:
            Word.fail_case += 1
            return "failed"

    def test_caller_hangs_up(self):
        """
        主叫被挂，终端主叫，对端接听接听后，对端主动挂断
        :param times: 测试次数
        :param number: 对端号码
        :return: None
        """
        self.log.info("主叫被挂测试++++")
        call_func = Call_func()
        resultcode = call_func.cp_caller_hangs_up()

        if resultcode == 1:
            self.log.info("主叫被挂fail——拨号失败\n")
        elif resultcode == 2:
            self.log.info("主叫被挂fail——超时\n")
        elif resultcode == 3:
            self.log.info("主叫被挂fail——对端拒接\n")
        elif resultcode == 4:
            self.log.info("主叫被挂fail——通话时长低于保持时长\n")
        elif resultcode == 5:
            self.log.info("主叫被挂fail——未USB连接对端设备\n")
        elif resultcode == 6:
            self.log.info("主叫被挂fail——对端接听\n")

        if resultcode == 0:
            Word.pass_case += 1
            self.log.info("主叫被挂pass\n")
            return "pass"
        else:
            Word.fail_case += 1
            return "failed"

    def test_call_reject(self):
        """
        测试项——主叫拒接，终端主叫，对端挂断
        :param times: 测试次数
        :param number: 对端号码
        :return: None
        """
        self.log.info("主叫拒接测试++++")
        call_func = Call_func()

        resultcode = call_func.cp_call_reject()

        if resultcode == 1:
            self.log.info("主叫拒接fail——拨号失败\n")
        elif resultcode == 2:
            self.log.info("主叫拒接fail——通话超时\n")
        elif resultcode == 3:
            self.log.info("主叫拒接fail——对端接听\n")
        elif resultcode == 4:
            self.log.info("主叫拒接fail——响铃时长低于设置时长\n")
        elif resultcode == 5:
            self.log.info("主叫被挂fail——未USB连接对端设备\n")

        if resultcode == 0:
            Word.pass_case += 1
            self.log.info("主叫拒接pass\n")
            return "pass"
        else:
            Word.fail_case += 1
            return "failed"

    def test_call_no_answer(self):
        """
        测试项——主叫未接，终端主叫，对端不予接听
        :param times: 测试次数
        :param number: 对端号码
        :return: None
        """
        self.log.info("主叫未接测试++++")
        call_func = Call_func()
        resultcode = call_func.cp_call_no_answer()

        if resultcode == 1:
            self.log.info("主叫未接fail——拨号失败\n")
        elif resultcode == 2:
            self.log.info("主叫未接fail——对端拒接\n")
        elif resultcode == 3:
            self.log.info("主叫未接fail——对端接听\n")
        elif resultcode == 4:
            self.log.info("主叫未接fail——响铃时长低于设置时长\n")

        if resultcode == 0:
            Word.pass_case += 1
            self.log.info("主叫未接pass\n")
            return "pass"
        else:
            Word.fail_case += 1
            return "failed"
