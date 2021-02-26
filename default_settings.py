import json
from json import JSONDecodeError

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog

from ui.default_settings_ui import Default_settings_Dialog
from ui.main_ui import Ui_MainWindow
from common.log import Log

class Default_settings(Default_settings_Dialog, QDialog, Ui_MainWindow):
    config_path = 'config/config.cfg'

    def __init__(self):
        super(Default_settings_Dialog, self).__init__()
        self.setupUi(self)
        self.log = Log(__name__).getlog()
        # icon = '..\\img\\icon.ico'
        icon = 'img\icon.ico'
        self.setWindowIcon(QIcon(icon))
        self.init()

    def init(self):
        self.log.info("######>>> Init Default settings Dialog")

        self.button_ok.clicked.connect(self.modify_config)
        self.button_ok.clicked.connect(self.close)
        self.button_cancel.clicked.connect(self.close)
        try:

            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                number = config['number']
                times = config['Test_times']
                interval = config['interval']
                self.edit_called_number.setPlaceholderText(number)
                self.edit_times.setPlaceholderText(times)
                self.edit_test_interval.setPlaceholderText(interval)
        except JSONDecodeError:
            self.log.error("配置文件出现问题，请删除配置文件重新打开程序（会自动生成新config）")

    def modify_config(self):
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                if self.edit_called_number.isModified():
                    config['number'] = self.edit_called_number.text()
                    self.log.info("config.cfg modified number: %s" % self.edit_called_number.text())
                if self.edit_times.isModified():
                    config['Test_times'] = self.edit_times.text()
                    self.log.info("config.cfg modified Test times: %s" % self.edit_times.text())
                if self.edit_test_interval.isModified():
                    config['interval'] = self.edit_test_interval.text()
                    self.log.info("config.cfg modified interval: %s" % self.edit_test_interval.text())

            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)

        except JSONDecodeError:
            self.log.error("配置文件出现问题，请删除配置文件重新打开程序（会自动生成新config）")
