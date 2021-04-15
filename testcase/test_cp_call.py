import sys

import Word

sys.path.append("..")
from common.log import Log
from common.call_func import Call_func

class Test_Call:

    def __init__(self):
        self.log = Log(__name__).getlog()
        # todo:测试前的执行步骤，入网检测

    def test_calling_to_answer(self):
        """
        主叫主挂，终端主叫，对端接听后，终端主动挂断
        :param times: 测试次数
        :param number: 对端号码
        :return: None
        """
        self.log.info("主叫主挂测试++++")
        call_func = Call_func()
        resultcode = call_func.cp_calling_to_answer()
        self.log.info("test process: %s" % resultcode)

        if resultcode == 1:
            self.log.info("主叫主挂fail——拨号失败")
        elif resultcode == 2:
            self.log.info("主叫主挂fail——对端未接听")
        elif resultcode == 3:
            self.log.info("主叫主挂fail——对端拒接")
        elif resultcode == 4:
            self.log.info("主叫主挂fail——通话时长低于保持时长")

        if resultcode == 0:
            Word.pass_case += 1
            self.log.info("主叫主挂pass")
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
        self.log.info("test process: %s" % resultcode)

        if resultcode == 1:
            self.log.info("主叫被挂fail——拨号失败")
        elif resultcode == 2:
            self.log.info("主叫被挂fail——对端未接听")
        elif resultcode == 3:
            self.log.info("主叫被挂fail——对端拒接")
        elif resultcode == 4:
            self.log.info("主叫被挂fail——通话时长低于保持时长")

        if resultcode == 0:
            Word.pass_case += 1
            self.log.info("主叫被挂pass")
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
            self.log.info("主叫拒接fail——拨号失败")
        elif resultcode == 2:
            self.log.info("主叫拒接fail——对端未接听")
        elif resultcode == 3:
            self.log.info("主叫拒接fail——对端接听")
        elif resultcode == 4:
            self.log.info("主叫拒接fail——响铃时长低于设置时长")

        if resultcode == 0:
            Word.pass_case += 1
            self.log.info("主叫拒接pass")
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
            self.log.info("主叫未接fail——拨号失败")
        elif resultcode == 2:
            self.log.info("主叫未接fail——对端拒接")
        elif resultcode == 3:
            self.log.info("主叫未接fail——对端接听")
        elif resultcode == 4:
            self.log.info("主叫未接fail——响铃时长低于设置时长")

        if resultcode == 0:
            Word.pass_case += 1
            self.log.info("主叫未接pass")
            return "pass"
        else:
            Word.fail_case += 1
            return "failed"
