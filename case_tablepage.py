from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow

from common.pysql_connect import *
from ui.testcase_table import Ui_Testcase_table


class TestCaseTable(QMainWindow, Ui_Testcase_table):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init()

    def init(self):
        self.load_case()

    # 加载数据库到用例表中
    def load_case(self):
        cursor, conn = conn_db()
        test_case = select_case("all")
        if test_case is None:
            print("数据库无数据")
        # assert test_case != '', "数据库无数据"
        else:
            for case in test_case:
                print(case)
                Case_title = case['Case_title']
                print(Case_title)
                self.insert_case(Case_title)
            cursor.close()
            conn.close()

    def insert_item(self, title):
        item = QtWidgets.QTreeWidgetItem(self.TreeWidget_case)
        font = QtGui.QFont()
        font.setPointSize(11)
        item.setFont(0, font)
        item.setText(0, title)
        item.setCheckState(0, QtCore.Qt.Unchecked)


if __name__ == '__main__':
    tct = TestCaseTable()
    tct.load_case()
