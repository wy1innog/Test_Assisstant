import pickle

import yaml
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QPushButton

class CaseConfig_Page:
    List_call_answer = []
    List_caller_hangs_up = []
    List_call_reject = []
    List_call_no_answer = []


    # def __init__(self):
    #     super().__init__()
    #     self.setupUi(self)
    #     self.log = Log(__name__).getlog()
    #
    #     self.init()

    # def init(self):
        # self.__load_config()
        # self.Btn_config_ok.clicked.connect(self.write_config)
        # self.Btn_config_ok.clicked.connect(self.close)
        # self.Btn_config_cancel.clicked.connect(self.close)


    # def write_config(self):
    #     with open('config/config.yml', 'r', encoding='utf-8') as f:
    #         content = yaml.load(f.read(), yaml.FullLoader)
    #         content['config_call']['call_number'] = self.Ledit_call_number.text()
    #         content['config_call']['call_interval'] = self.Ledit_call_interval.text()
    #         content['config_call']['call_hold'] = self.Ledit_call_hold.text()
    #         content['config_WIFI']['WIFI_SSID'] = self.Ledit_WIFI_SSID.text()
    #         content['config_WIFI']['WIFI_PWD'] = self.Ledit_WIFI_PWD.text()
    #         content['config_WIFI']['WIFI_interval'] = self.Ledit_WIFI_interval.text()
    #         content['config_BT']['BT_name'] = self.Ledit_BT_name.text()
    #         # obj = self.__dict__
    #         # for key, value in obj.items():
    #         #     if isinstance(value, PyQt5.QtWidgets.QLineEdit) and value.textChanged:
    #         #         print(key, value)
    #
    #     with open('config/config.yml', 'w', encoding='utf-8') as wf:
    #         yaml.dump(content, wf, Dumper=yaml.SafeDumper)
    #     self.log.info("数据写入完成")

    @classmethod
    def getCaseConfigDialog(cls, title, item_list):
        dialog = QDialog()
        dialog.setMinimumSize(440, 330)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        font.setWeight(50)

        cls.btn = QPushButton("ok", dialog)
        cls.btn.setGeometry(QtCore.QRect(260, 280, 110, 32))

        cls.btn.setFont(font)

        for i in range(len(item_list)):
            LabelName = "label" + str(i)
            LeditName = "Ledit" + str(i)
            Label_height = 40 + i * 60
            Ledit_height = 35 + i * 60
            LabelName = QtWidgets.QLabel(dialog)
            LabelName.setGeometry(QtCore.QRect(40, Label_height, 109, 21))
            LabelName.setFont(font)
            LabelName.setText(item_list[i])
            LeditName = QtWidgets.QLineEdit(dialog)
            LeditName.setGeometry(160, Ledit_height, 210, 32)
            LeditName.setFont(font)

            if title == "主叫主挂":
                cls.List_call_answer.append(LeditName)
                cls.btn.clicked.connect(CaseConfig_Page.saveConfig_calling_to_answer)
            elif title == "主叫被挂":
                cls.List_caller_hangs_up.append(LeditName)
                cls.btn.clicked.connect(CaseConfig_Page.saveConfig_caller_hangs_up)
            elif title == "主叫拒接":
                cls.List_call_reject.append(LeditName)
                cls.btn.clicked.connect(CaseConfig_Page.saveConfig_call_reject)
            elif title == "主叫未接":
                cls.List_call_no_answer.append(LeditName)
                cls.btn.clicked.connect(CaseConfig_Page.saveConfig_call_no_answer)

        cls.btn.clicked.connect(dialog.close)


        dialog.setWindowTitle(title)
        dialog.exec_()

    @classmethod
    def caseConfig_calling_to_answer(cls):
        item_list = ["对端电话", "保持时间(秒)", "测试间隔(秒)", "超时时间(秒)"]
        CaseConfig_Page.getCaseConfigDialog("主叫主挂", item_list)

    @classmethod
    def caseConfig_caller_hangs_up(cls):
        item_list = ["对端电话", "保持时间(秒)", "测试间隔(秒)", "超时时间(秒)"]
        CaseConfig_Page.getCaseConfigDialog("主叫被挂", item_list)

    @classmethod
    def caseConfig_call_reject(cls):
        item_list = ["对端电话", "响铃时长(秒)", "测试间隔(秒)", "超时时间(秒)"]
        CaseConfig_Page.getCaseConfigDialog("主叫拒接", item_list)

    @classmethod
    def caseConfig_call_no_answer(cls):
        item_list = ["对端电话", "响铃时长(秒)", "测试间隔(秒)", "超时时间(秒)"]
        CaseConfig_Page.getCaseConfigDialog("主叫未接", item_list)

    @classmethod
    def saveConfig_calling_to_answer(cls):
        with open('config/config.yml', 'r', encoding='utf-8') as f:
            config = yaml.load(f.read(), yaml.FullLoader)
            content = config['call_to_answer']
            content['number'] = cls.List_call_answer[0].text()
            content['hold'] = cls.List_call_answer[1].text()
            content['interval'] = cls.List_call_answer[2].text()
            content['timeout'] = cls.List_call_answer[3].text()
            with open('config/config.yml', 'w', encoding='utf-8') as wf:
                yaml.dump(config, wf, Dumper=yaml.SafeDumper)

    @classmethod
    def saveConfig_caller_hangs_up(cls):
        with open('config/config.yml', 'r', encoding='utf-8') as f:
            config = yaml.load(f.read(), yaml.FullLoader)
            content = config['caller_hangs_up']
            content['number'] = cls.List_caller_hangs_up[0].text()
            content['hold'] = cls.List_caller_hangs_up[1].text()
            content['interval'] = cls.List_caller_hangs_up[2].text()
            content['timeout'] = cls.List_caller_hangs_up[3].text()
        with open('config/config.yml', 'w', encoding='utf-8') as wf:
            yaml.dump(config, wf, Dumper=yaml.SafeDumper)

    @classmethod
    def saveConfig_call_reject(cls):
        with open('config/config.yml', 'r', encoding='utf-8') as f:
            config = yaml.load(f.read(), yaml.FullLoader)
            content = config['call_reject']
            content['number'] = cls.List_call_reject[0].text()
            content['ring_time'] = cls.List_call_reject[1].text()
            content['interval'] = cls.List_call_reject[2].text()
            content['timeout'] = cls.List_call_reject[3].text()
        with open('config/config.yml', 'w', encoding='utf-8') as wf:
            yaml.dump(config, wf, Dumper=yaml.SafeDumper)

    @classmethod
    def saveConfig_call_no_answer(cls):
        with open('config/config.yml', 'r', encoding='utf-8') as f:
            config = yaml.load(f.read(), yaml.FullLoader)
            content = config['call_no_answer']
            content['number'] = cls.List_call_no_answer[0].text()
            content['ring_time'] = cls.List_call_no_answer[1].text()
            content['interval'] = cls.List_call_no_answer[2].text()
            content['timeout'] = cls.List_call_no_answer[3].text()
        with open('config/config.yml', 'w', encoding='utf-8') as wf:
            yaml.dump(config, wf, Dumper=yaml.SafeDumper)
