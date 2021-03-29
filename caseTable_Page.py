from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QDialog, QPushButton

from common.pysql_connect import *
from ui.caseTable import Ui_Testcase_table
from caseConfig_Page import CaseConfig_Page
from ensureCaseTable_Page import EnsureCaseTable_Page
import common.pysql_connect as pysql
from common.log import Log

class TestCaseTable_Page(QMainWindow, Ui_Testcase_table):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.log = Log(__name__).getlog()
        self.case_Qtree_dict = {}
        self.case_module_Qtree_dict = {}
        self.init()

    def init(self):
        self.load_case()
        self.caseConfig_window = CaseConfig_Page()
        self.ensureTable_window = EnsureCaseTable_Page()
        self.Btn_cancel_case.clicked.connect(self.close)
        self.Btn_save_case.clicked.connect(self.save_case_state)
        self.ensureTable_window.my_Signal.connect(self.ensureTable_window.clear_case)
        self.ensureTable_window.Btn_ensure_ok.clicked.connect(self.close)
        self.Btn_config_case.clicked.connect(self.show_caseConfig_window)
        # 点击保存后整体查看case_Qtree_dict chekced情况，写入到数据库并生成待测表
        # self.Btn_save_case.clicked.connect(self.update_table)

    def show_ensureTable_window(self):
        self.ensureTable_window.show()

    def show_caseConfig_window(self):
        self.caseConfig_window.show()

    def recover_check(self):
        """
        清空所有勾选
        """
        item = self.get_QTreeItemIterator(self.TreeWidget_case)
        while item.value():
            item.value().setCheckState(0, QtCore.Qt.Unchecked)
            item.__iadd__(1)

    def showEmptyMessageBox(self):
        dialog = QDialog()
        dialog.setObjectName("Emptycase_dialog")
        dialog.setMinimumSize(311, 140)

        btn = QPushButton("ok", dialog)
        btn.setGeometry(QtCore.QRect(110, 100, 91, 40))
        font1 = QtGui.QFont()
        font1.setPointSize(10)
        btn.setFont(font1)
        btn.clicked.connect(dialog.close)

        label_mes = QtWidgets.QLabel(dialog)
        label_mes.setGeometry(QtCore.QRect(80, 40, 151, 41))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        label_mes.setFont(font)
        label_mes.setText("未选择测试用例！")

        dialog.setWindowTitle("提示")
        # dialog.setWindowModality(Qt.ApplicationModal)
        dialog.exec_()


    def save_case_state(self):
        self.update_checked_state()
        sql = "select * from android_testcases where checked=1"
        rows = pysql.exec_sql(sql)
        print(rows[0])
        if rows[0] == 0:
            self.showEmptyMessageBox()
        else:
            self.show_ensureTable_window()
            self.load_ensure_case()

    def get_QTreeItemIterator(self, TreeWidget):
        return QtWidgets.QTreeWidgetItemIterator(TreeWidget)

    def load_ensure_case(self):
        rows, test_case_dict = pysql.exec_sql("select Case_title from android_testcases where checked=1")
        if rows:
            for i in test_case_dict:
                self.ensureTable_window.show_case(i['Case_title'])
                self.ensureTable_window.testcase_ready_list.append(i['Case_title'])
        else:
            self.log.warning("No matching data")


    def update_checked_state(self):
        """
        修改数据库对应case_title的checked状态
        使用QTreeWidgetItemInterator遍历item，__iadd__(1), __isub__(1)分别用来到下/上一个节点
        """
        item = self.get_QTreeItemIterator(self.TreeWidget_case)
        while item.value():
            if item.value().checkState(0) == QtCore.Qt.Checked:
                pysql.update_checked(item.value().text(0), '1')
            elif item.value().checkState(0) == QtCore.Qt.Unchecked:
                pysql.update_checked(item.value().text(0), '0')
                # 到下一个节点
            item.__iadd__(1)


    # 添加模块标题
    def add_top_item(self, title):
        item_0 = QtWidgets.QTreeWidgetItem(self.TreeWidget_case)

        item_0.setText(0, title)
        font = QtGui.QFont()
        font.setPointSize(11)
        item_0.setFont(0, font)
        item_0.setText(0, title)
        item_0.setCheckState(0, QtCore.Qt.Unchecked)
        item_0.setFlags(
            QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsTristate)

        return item_0.text(0), item_0

    # 添加测试子项
    def add_item(self, title, belong_QtreeWidget):
        item_1 = QtWidgets.QTreeWidgetItem(belong_QtreeWidget)
        item_1.checkState(0)
        item_1.setText(0, title)
        font = QtGui.QFont()
        font.setPointSize(9)
        item_1.setFont(0, font)
        item_1.setText(0, title)
        item_1.setCheckState(0, QtCore.Qt.Unchecked)
        item_1.setFlags(
            QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsTristate)

        title_name = item_1.text(0)
        assert title_name == title, "用例名字不匹配"
        assert QtCore.Qt.Unchecked == item_1.checkState(0)
        self.case_Qtree_dict[title_name] = item_1


    # def update_table(self):
    #     cursor, conn = conn_db()
    #     for item in self.case_Qtree_dict.items():
    #         if item[1].setCheckState(0, QtCore.Qt.checked)
    #
    #
    #     update_sql = 'update %s set checked=1 where Case_title=%s'
    #     cursor.execute(update_sql, (use_table, title))

    # 加载数据库到用例表中
    def load_case(self):
        cursor, conn = conn_db()
        test_case = select_case("all")
        if test_case is None:
            print("数据库无数据")
        # assert test_case != '', "数据库无数据"
        else:
            rows, Case_belong = exec_sql("select DISTINCT Case_belong from android_testcases order by Case_belong ")
            # 添加模块级
            for belong in Case_belong:
                module_title, module_title_obj = self.add_top_item(belong['Case_belong'])
                self.case_module_Qtree_dict[module_title] = module_title_obj

            # 添加测试子项
            for case in test_case:
                for case_module in self.case_module_Qtree_dict.items():

                    if case['Case_belong'] == case_module[0]:
                        case_module_obj = self.case_module_Qtree_dict[case_module[0]]
                        self.add_item(case['Case_title'], case_module_obj)
                    else:
                        pass
            cursor.close()
            conn.close()


