import time
from common.log import Log
from common.normal_func import Normal_func


class Call_func(object):
    def __init__(self):
        self.log = Log(__name__).getlog()

    @classmethod
    def getCall_config(self) -> tuple:
        call_config = Normal_func.getConfig()['config_call']
        return call_config



    def cp_calling_to_answer(self):
        #todo:主叫主挂流程
        global endtime
        nf = Normal_func()
        call_config = Call_func.getCall_config()
        nf.process.clear()
        nf.exec_cmd('ATD%s;' % call_config['call_number'])

        while True:
            starttime = time.time()
            time.sleep(1)
            # if nf.process == []:
            #     self.log.info("空流程")
            #     return nf.process

            if nf.process[-1] == "拨号":
                endtime = time.time()
                self.log.info("dial process: %s" % nf.process)

            elif nf.process[-1] == "通话结束" and nf.process[-2] == "对端接听":
                self.log.warning("pnf: 拨号 -> 对端振铃 -> 对端接听 -> 通话结束")
                endtime = time.time()
                return nf.process

            elif nf.process[-1] == "通话结束" and nf.process[-2] == "对端振铃":
                self.log.warning("拨号 -> 对端振铃 -> 通话结束")
                return nf.process

            elif nf.process[-1] == "通话结束" and nf.process[-2] == "拨号":
                self.log.warning("拨号 -> 通话结束")
                return nf.process

            elif endtime-starttime == call_config['call_timeout']:
                self.log.debug("通话超时，主动挂断")
                nf.exec_cmd('AT+CHUP')
                return nf.process
            else:
                endtime = time.time()
                self.log.error("error:%s" %(__name__))



    def cp_caller_hangs_up(self) -> list:
        # todo:主叫被挂流程
        global endtime
        nf = Normal_func()
        nf.process.clear()
        call_config = Call_func.getCall_config()
        nf.exec_cmd('ATD%s;' % call_config['call_number'])

        while True:
            starttime = time.time()
            time.sleep(1)
            if nf.process == []:
                self.log.info("空流程")
                return nf.process
            if nf.process[-1] == "拨号":
                endtime = time.time()
                self.log.debug("dial process: %s" % nf.process)

            elif nf.process[-1] == "通话结束" and nf.process[-2] == "对端接听":
                self.log.warning("pnf: 拨号 -> 对端振铃 -> 对端接听 -> 通话结束")
                endtime = time.time()
                return nf.process

            elif nf.process[-1] == "通话结束" and nf.process[-2] == "对端振铃":
                self.log.warning("拨号 -> 对端振铃 -> 通话结束")
                return nf.process

            elif nf.process[-1] == "通话结束" and nf.process[-2] == "拨号":
                self.log.warning("拨号 -> 通话结束")
                return nf.process

            elif endtime-starttime == call_config['call_timeout']:
                self.log.debug("通话超时，主动挂断")
                nf.exec_cmd('AT+CHUP')
                return nf.process
            else:
                endtime = time.time()
                self.log.error("error:%s" %(__name__))


    def cp_call_reject(self) -> list:
        # todo:主叫拒接流程
        global endtime
        nf = Normal_func()
        nf.process.clear()
        call_config = Call_func.getCall_config()
        nf.exec_cmd('ATD%s;' % call_config['call_number'])

        while True:
            starttime = time.time()
            time.sleep(1)
            if nf.process == []:
                self.log.info("空流程")
                return nf.process

            if nf.process[-1] == "拨号":
                endtime = time.time()
                self.log.debug("dial process: %s" % nf.process)

            elif nf.process[-1] == "通话结束" and nf.process[-2] == "对端振铃":
                self.log.warning("pnf: 拨号 -> 对端振铃 -> 通话结束")
                return nf.process

            elif nf.process[-1] == "通话结束" and nf.process[-2] == "对端接听":
                self.log.warning("拨号 -> 对端振铃 -> 对端接听 -> 通话结束")
                return nf.process

            elif nf.process[-1] == "通话结束" and nf.process[-2] == "拨号":
                self.log.warning("拨号 -> 通话结束")
                return nf.process

            elif endtime - starttime == call_config['call_timeout']:
                self.log.debug("通话超时，主动挂断")
                nf.exec_cmd('AT+CHUP')
                return nf.process

            else:
                endtime = time.time()
                self.log.error("error:%s" %(__name__))

    def cp_call_no_answer(self) -> list:
        # todo:主叫未接流程
        global endtime
        nf = Normal_func()
        nf.process.clear()
        call_config= Call_func.getCall_config()
        nf.exec_cmd('ATD%s;' % call_config['call_number'])

        while True:
            starttime = time.time()
            time.sleep(1)
            if nf.process == []:
                self.log.info("空流程")
                return nf.process

            if nf.process[-1] == "拨号":
                endtime = time.time()
                self.log.debug("dial process: %s" % nf.process)

            elif nf.process[-1] == "通话结束" and nf.process[-2] == "对端振铃":
                self.log.warning("pnf: 拨号 -> 对端振铃 -> 通话结束")
                return nf.process

            elif nf.process[-1] == "通话结束" and nf.process[-2] == "对端接听":
                self.log.warning("拨号 -> 对端振铃 -> 对端接听 -> 通话结束")
                return nf.process

            elif nf.process[-1] == "通话结束" and nf.process[-2] == "拨号":
                self.log.warning("拨号 -> 通话结束")
                return nf.process

            elif nf.process[-1] != "通话结束" and endtime-starttime == call_config['call_timeout']:
                self.log.debug("振铃超时，未挂断，已超过设定值")

            elif nf.process[-1] != "通话结束" and endtime-starttime > call_config['call_timeout']:
                self.log.debug("对端未接，已挂断")
                return nf.process

            else:
                endtime = time.time()
                self.log.error("error:%s" % (__name__))
