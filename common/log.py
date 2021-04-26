import datetime
import time
import logging
import os

class Log(object):
    def __init__(self, logger=None, log_cate='search'):
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)

        self.log_time = time.strftime("%Y_%m_%d")
        file_dir = os.getcwd() + '/syslog'


        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        self.log_path = file_dir

        # self.log_name = self.log_path + "/" + log_cate + "." + self.log_time + '.log'
        # print（self.log_name）

        self.log_name = os.path.join(self.log_path, 'runlog_{0:%Y%m%d%H%M%S}.log'.format(datetime.datetime.now()))

        fh = logging.FileHandler(self.log_name, 'a', encoding="utf-8")
        fh.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
        fmt="%(asctime)s %(filename)s->%(funcName)s [line:%(lineno)d] %(levelname)s %(message)s",
        datefmt="%Y/%m/%d %X")

        # 为handler指定输出格式
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # 为logger添加的日志处理器
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def getlog(self):
        return self.logger