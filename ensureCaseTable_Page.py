from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow

from ui.ensureCaseTable import Ui_EnsureCase_table

class EnsureCaseTable_Page(QMainWindow, Ui_EnsureCase_table):
    # 让多窗口之间传递信号 刷新主窗口信息
    my_Signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init()
        self.testcase_ready_list = []


    def init(self):
        self.Btn_ensureTable_cancel.clicked.connect(self.close)
        self.Btn_ensure_ok.clicked.connect(self.close)


    def sendEditContent(self):
        content = '1'
        self.my_Signal.emit(content)

    def closeEvent(self, event):
        self.sendEditContent()

    def show_case(self, case_title):
        item = QtWidgets.QListWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        item.setFont(font)
        item.setText(case_title)
        self.ListWidget_ensureTable.addItem(item)

    def clear_case(self):
        """
        清空待测表的用例
        """
        self.ListWidget_ensureTable.clear()