from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QDialog, QPushButton

from ui.caseTableUI import Ui_Testcase_table
from caseConfig_Page import CaseConfig_Page
from ensureCaseTable_Page import EnsureCaseTable_Page
import common.pysql_connect as pysql
from common.log import Log

class CaseTable_Page(QMainWindow, Ui_Testcase_table):
    readyCase = []

    def __init__(self, Tab):
        super().__init__()
        self.setupUi(self)
        self.log = Log(__name__).getlog()
        self.Tab = Tab
        self.case_Qtree_dict = {}
        self.case_module_Qtree_dict = {}
        self.ensureCaseList = []
        self.titleSet = set()
        self.init()

    def init(self):

        self.caseConfig_window = CaseConfig_Page()
        self.ensureTable_window = EnsureCaseTable_Page()
        self.Btn_cancel_case.clicked.connect(self.close)
        self.Btn_save_case.clicked.connect(self.save_case_state)
        self.ensureTable_window.Btn_ensure_ok.clicked.connect(self.close)
        self.ensureTable_window.Btn_ensureTable_cancel.clicked.connect(self.clearList)
        self.Btn_config_case.clicked.connect(self.show_caseConfig_window)


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
        useTable = self.get_useTable()
        result = pysql.exec_sql("select * from %s"% useTable)
        if len(result)==0:
            self.showEmptyMessageBox()
            self.log.info("Table no case!")
        else:
            self.show_ensureTable_window()
            self.load_ensure_case()


    def get_QTreeItemIterator(self, TreeWidget):
        return QtWidgets.QTreeWidgetItemIterator(TreeWidget)

    def get_useTable(self):
        if self.Tab.upper()=='AP':
            return 'ap_testcases'
        else:
            return 'cp_testcases'

    def load_ensure_case(self):
        # 在待测表加载勾选的测试用例
        print(self.ensureCaseList)
        self.ensureTable_window.ListWidget_ensureTable.clear()
        if len(self.ensureCaseList) != 0:
            for i in self.ensureCaseList:
                self.ensureTable_window.show_case(i)
                CaseTable_Page.readyCase.append(i)

        else:
            self.log.warning("No matching data")




    def update_checked_state(self):
        """
        修改数据库对应title的checked状态
        使用QTreeWidgetItemInterator遍历item，__iadd__(1), __isub__(1)分别用来到下/上一个节点
        """
        item = self.get_QTreeItemIterator(self.TreeWidget_case)
        useTable = self.get_useTable()
        title_dict = pysql.exec_sql("select DISTINCT belong from %s"%useTable)
        for i in title_dict:
            self.titleSet.add(i['belong'])
        # 用例是否被勾选，并且不是标题，添加进ensureCaseList
        self.ensureCaseList.clear()
        while item.value():
            for title in self.titleSet:
                if item.value().checkState(0) == QtCore.Qt.Checked and item.value().text(0)!=title:
                    self.ensureCaseList.append(item.value().text(0))

                elif item.value().checkState(0) == QtCore.Qt.Unchecked:
                    pass

                #     # 到下一个节点
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
        configBtn = QtWidgets.QPushButton(self.TreeWidget_case)
        self.TreeWidget_case
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

    # 加载数据库到用例表中
    def load_case(self):
        cursor, conn = pysql.conn_db()
        self.TreeWidget_case.clear()
        useTable = self.get_useTable()
        module_caseCount = pysql.exec_sql("select belong, count(*) as count from %s GROUP BY belong"% useTable)
        test_case = pysql.exec_sql("select title, belong from %s"% useTable)

        if test_case is None:
            self.log.info("表中无内容!")
        else:
            result = pysql.exec_sql("select DISTINCT belong from %s order by belong"% useTable)



            # 添加模块级
            for belong in result:
                # 返回模块title, 模块对象
                module_title, module_title_obj = self.add_top_item(belong['belong'])
                self.case_module_Qtree_dict[module_title] = module_title_obj



            # 添加测试子项
            for case in test_case:
                for case_module in self.case_module_Qtree_dict.items():
                    if case['belong'] == case_module[0]:

                        case_module_obj = self.case_module_Qtree_dict[case_module[0]]
                        self.add_item(case['title'], case_module_obj)
                    else:
                        pass
            cursor.close()
            conn.close()

    def clearList(self):
        self.ensureCaseList.clear()
