import json
from json import JSONDecodeError

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QInputDialog

from ui.ass_atmgr_ui import Ui_Dialog
from ui.main_ui import Ui_MainWindow
from common.log import Log

class At_settings(Ui_Dialog, QDialog, Ui_MainWindow):

    def __init__(self):
        super(Ui_Dialog, self).__init__()
        self.setupUi(self)
        icon = 'img\icon.ico'
        self.config_path = 'config/config.cfg'
        self.log = Log(__name__).getlog()
        self.setWindowIcon(QIcon(icon))
        self.init()

    def init(self):
        self.log.info("######>>> Init settings AT Dialog")

        self.btn_add.clicked.connect(self.add_at_cmd)
        self.btn_sub.clicked.connect(self.remove_at_cmd)
        try:

            with open(self.config_path, 'r', encoding='utf-8') as f:
                AT_list = json.load(f)['AT_list']
                for cmd in AT_list:
                    self.listWidget.insertItem(0, cmd.strip())
        except JSONDecodeError:
            self.log.error("配置文件出现问题，请删除配置文件重新打开程序（会自动生成新config）")

    def add_at_cmd(self):
        at_text, status = QInputDialog.getText(self, "添加新指令", "请输入新指令:")

        at_text = str(at_text).upper()
        self.log.info("######>>> Add new AT cmd: text=%s, status=%s" % (at_text, status))
        if at_text.startswith("AT"):
            if at_text and status:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config_file = json.load(f)
                    config_file['AT_list'].append(at_text)

                with open(self.config_path, 'w', encoding='utf-8') as f:
                    json.dump(config_file, fp=f, indent=4, ensure_ascii=False)
                    self.listWidget.addItem(at_text.strip())
        else:
            self.log.info("######??? Add new AT cmd failed! format illegal")

    def remove_at_cmd(self):
        try:
            item = self.listWidget.currentItem()
            self.log.info("######>>> Remove AT Command: %s" % item.text())
            self.listWidget.takeItem(self.listWidget.row(item))

            with open(self.config_path, 'r', encoding='utf-8') as f:
                config_file = json.load(f)
                sub_text = item.text()
                AT_list = config_file['AT_list']
                for i in AT_list:
                    if sub_text == i.strip():
                        AT_list.remove(i)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config_file, f, indent=4, ensure_ascii=False)
                self.log.info("######!!! Remove AT Command: %s success" % item.text())

        except Exception as e:
            self.log.error("No select item")
