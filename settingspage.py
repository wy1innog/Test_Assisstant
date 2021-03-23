import json
from json import JSONDecodeError

from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QMessageBox

from common.log import Log
from ui.settings import Ui_Dialog


class Default_settings(Ui_Dialog, QDialog):
    config_path = 'config.cfg'
    # 让多窗口之间传递信号，刷新主窗口信息
    my_Signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super(Ui_Dialog, self).__init__()
        self.setupUi(self)
        self.log = Log(__name__).getlog()
        icon = 'D:\\ihblu\\wyrepo\\Test_Assistant\\img\\icon.ico'
        self.setWindowIcon(QIcon(icon))
        self.init()

    def init(self):
        self.log.info("######>>> Init Default settings Dialog")

        self.Btn_settings_save.clicked.connect(self.modify_config)
        self.Btn_settings_save.clicked.connect(self.close)
        self.Btn_settings_cancel.clicked.connect(self.close)

        try:

            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f, strict=False)
                number = config['number']
                interval = config['interval']
                self.LineEdit_calledNumber.setPlaceholderText(number)
                self.LineEdit_callInterval.setPlaceholderText(interval)
        except (FileNotFoundError, JSONDecodeError) as e:
            self.log.error("配置文件出现问题，请删除配置文件重新打开程序（会自动生成新config）")

    def sendEditContent(self):
        content = '1'
        self.my_Signal.emit(content)

    def closeEvent(self, event):
        self.sendEditContent()

    def msg_box(self, title, msg):
        return QMessageBox(QMessageBox.Warning, title, msg)
    def modify_config(self):
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                if self.LineEdit_calledNumber.isModified() and self.LineEdit_calledNumber.text().isdigit():
                    config['number'] = self.LineEdit_calledNumber.text()
                    self.log.info("config.cfg modified number: %s" % self.LineEdit_calledNumber.text())
                else:
                    self.msg_box('警告', '号码格式错误')

                if self.LineEdit_callInterval.isModified() and self.LineEdit_callInterval.text().isdigit():
                    config['interval'] = self.LineEdit_callInterval.text()
                    self.log.info("config.cfg modified interval: %s" % self.LineEdit_callInterval.text())
                else:
                    self.msg_box('警告', '通话间隔格式错误(请输入数字，单位秒)')
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)

        except JSONDecodeError:
            self.log.error("配置文件出现问题，请删除配置文件重新打开程序（会自动生成新config）")
