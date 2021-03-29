
import yaml
from PyQt5.QtWidgets import QMainWindow
from ui.caseConfig import Ui_Case_config as cf

from common.log import Log

class CaseConfig_Page(QMainWindow, cf):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.log = Log(__name__).getlog()
        self.init()

    def init(self):
        self.__load_config()
        self.Btn_config_ok.clicked.connect(self.write_config)
        self.Btn_config_ok.clicked.connect(self.close)
        self.Btn_config_cancel.clicked.connect(self.close)

    def __load_config(self):
        with open('config/config.yml', 'r', encoding='utf-8') as f:
            content = yaml.load(f.read(), yaml.FullLoader)

            self.Ledit_call_number.setText(content['config_call']['call_number'])
            self.Ledit_call_interval.setText(content['config_call']['call_interval'])
            self.Ledit_call_hold.setText(content['config_call']['call_hold'])
            self.Ledit_WIFI_SSID.setText(content['config_WIFI']['WIFI_SSID'])
            self.Ledit_WIFI_PWD.setText(content['config_WIFI']['WIFI_PWD'])
            self.Ledit_WIFI_interval.setText(content['config_WIFI']['WIFI_interval'])
            self.Ledit_BT_name.setText(content['config_BT']['BT_name'])

    def write_config(self):
        with open('config/config.yml', 'r', encoding='utf-8') as f:
            content = yaml.load(f.read(), yaml.FullLoader)
            content['config_call']['call_number'] = self.Ledit_call_number.text()
            content['config_call']['call_interval'] = self.Ledit_call_interval.text()
            content['config_call']['call_hold'] = self.Ledit_call_hold.text()
            content['config_WIFI']['WIFI_SSID'] = self.Ledit_WIFI_SSID.text()
            content['config_WIFI']['WIFI_PWD'] = self.Ledit_WIFI_PWD.text()
            content['config_WIFI']['WIFI_interval'] = self.Ledit_WIFI_interval.text()
            content['config_BT']['BT_name'] = self.Ledit_BT_name.text()
            # obj = self.__dict__
            # for key, value in obj.items():
            #     if isinstance(value, PyQt5.QtWidgets.QLineEdit) and value.textChanged:
            #         print(key, value)

        with open('config/config.yml', 'w', encoding='utf-8') as wf:
            yaml.dump(content, wf, Dumper=yaml.SafeDumper)
        self.log.info("数据写入完成")
