from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow

from ui.ensureCaseTable import Ui_EnsureCase_table

class EnsureCaseTable_Page(QMainWindow, Ui_EnsureCase_table):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init()
        self.testcase_ready_list = []

    def init(self):
        self.Btn_ensureTable_cancel.clicked.connect(self.close)
        self.Btn_ensure_ok.clicked.connect(self.close)
        # self.Btn_ensure_up.clicked.connect(self.up_selected)

    def show_case(self, case_title):
        item = QtWidgets.QListWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        item.setFont(font)
        item.setText(case_title)
        self.ListWidget_ensureTable.addItem(item)
