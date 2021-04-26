import yaml
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QPushButton

import Word
from cpSettings_page import CP_settings
from common.DialogUtil import showEmptyMessageBox

class CaseConfig_Page:
    config_path = Word.config_path
    List_call_answer = []
    List_caller_hangs_up = []
    List_call_reject = []
    List_call_no_answer = []


    @classmethod
    def getCaseConfigDialog(cls, title, item_list):
        cls.List_call_answer.clear()
        cls.List_caller_hangs_up.clear()
        cls.List_call_reject.clear()
        cls.List_call_no_answer.clear()
        dialog = QDialog()
        dialog.setMinimumSize(440, 330)
        icon = 'D:\\ihblu\\wyrepo\\Test_Assistant\\img\\icon.ico'
        dialog.setWindowIcon(QIcon(icon))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        font.setWeight(50)

        cls.btn = QPushButton("ok", dialog)
        cls.btn.setGeometry(QtCore.QRect(260, 280, 110, 32))

        cls.btn.setFont(font)

        for i in range(len(item_list)):
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
            elif title == "主叫被挂":
                cls.List_caller_hangs_up.append(LeditName)
            elif title == "主叫拒接":
                cls.List_call_reject.append(LeditName)
            elif title == "主叫未接":
                cls.List_call_no_answer.append(LeditName)

        if title == "主叫主挂":
            cls.btn.clicked.connect(CaseConfig_Page.saveConfig_calling_to_answer)
        elif title == "主叫被挂":
            cls.btn.clicked.connect(CaseConfig_Page.saveConfig_caller_hangs_up)
        elif title == "主叫拒接":
            cls.btn.clicked.connect(CaseConfig_Page.saveConfig_call_reject)
        elif title == "主叫未接":
            cls.btn.clicked.connect(CaseConfig_Page.saveConfig_call_no_answer)

        cls.btn.clicked.connect(dialog.close)


        dialog.setWindowTitle(title)
        dialog.exec_()

    # 判断列表中内容是否为整数数字
    @classmethod
    def checkDigit(cls, list1):
        for item in list1:
            if not item.text().isdigit():
                return False
        return True

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
        result = CaseConfig_Page.checkDigit(cls.List_call_answer)
        if result:
            with open(cls.config_path, 'r', encoding='utf-8') as f:
                config = yaml.load(f.read(), yaml.FullLoader)
                content = config['call_to_answer']
                content['number'] = cls.List_call_answer[0].text()
                content['hold'] = cls.List_call_answer[1].text()
                content['interval'] = cls.List_call_answer[2].text()
                content['timeout'] = cls.List_call_answer[3].text()
                with open(cls.config_path, 'w', encoding='utf-8') as wf:
                    yaml.dump(config, wf, Dumper=yaml.SafeDumper)
        else:
            showEmptyMessageBox("格式输入错误")

    @classmethod
    def saveConfig_caller_hangs_up(cls):
        result = CaseConfig_Page.checkDigit(cls.List_caller_hangs_up)
        if result:
            with open(cls.config_path, 'r', encoding='utf-8') as f:
                config = yaml.load(f.read(), yaml.FullLoader)
                content = config['caller_hangs_up']
                content['number'] = cls.List_caller_hangs_up[0].text()
                content['hold'] = cls.List_caller_hangs_up[1].text()
                content['interval'] = cls.List_caller_hangs_up[2].text()
                content['timeout'] = cls.List_caller_hangs_up[3].text()
            with open(cls.config_path, 'w', encoding='utf-8') as wf:
                yaml.dump(config, wf, Dumper=yaml.SafeDumper)
        else:
            showEmptyMessageBox("格式输入错误")

    @classmethod
    def saveConfig_call_reject(cls):
        result = CaseConfig_Page.checkDigit(cls.List_call_reject)
        if result:
            with open(cls.config_path, 'r', encoding='utf-8') as f:
                config = yaml.load(f.read(), yaml.FullLoader)
                content = config['call_reject']
                content['number'] = cls.List_call_reject[0].text()
                content['ring_time'] = cls.List_call_reject[1].text()
                content['interval'] = cls.List_call_reject[2].text()
                content['timeout'] = cls.List_call_reject[3].text()
            with open(cls.config_path, 'w', encoding='utf-8') as wf:
                yaml.dump(config, wf, Dumper=yaml.SafeDumper)
        else:
            showEmptyMessageBox("格式输入错误")

    @classmethod
    def saveConfig_call_no_answer(cls):
        result = CaseConfig_Page.checkDigit(cls.List_call_no_answer)
        if result:
            with open(cls.config_path, 'r', encoding='utf-8') as f:
                config = yaml.load(f.read(), yaml.FullLoader)
                content = config['call_no_answer']
                content['number'] = cls.List_call_no_answer[0].text()
                content['ring_time'] = cls.List_call_no_answer[1].text()
                content['interval'] = cls.List_call_no_answer[2].text()
                content['timeout'] = cls.List_call_no_answer[3].text()
            with open(cls.config_path, 'w', encoding='utf-8') as wf:
                yaml.dump(config, wf, Dumper=yaml.SafeDumper)
        else:
            showEmptyMessageBox("格式输入错误")
