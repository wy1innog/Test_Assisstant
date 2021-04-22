from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow

import Word
import common.pysql_connect as pysql
from common.DialogUtil import showEmptyMessageBox
from caseConfig_Page import CaseConfig_Page
from ensureCaseTable_Page import EnsureCaseTable_Page
from cpSettings_page import CP_settings
from ui.caseTableUI import Ui_Testcase_table


class CaseTable_Page(QMainWindow, Ui_Testcase_table):

    def __init__(self, Tab):
        super().__init__()
        self.setupUi(self)
        self.log = Word.log[0]
        self.TAB = Tab
        self.case_Qtree_dict = {}
        self.case_module_Qtree_dict = {}
        self.init()

    def init(self):

        self.caseConfig_window = CaseConfig_Page()
        self.ensureTable_window = EnsureCaseTable_Page()
        self.cpSettings = CP_settings()
        self.Btn_cancel_case.clicked.connect(self.close)
        self.Btn_save_case.clicked.connect(self.saveBeTestcase)
        self.Btn_config_case.clicked.connect(self.show_cpSettings_window)
        self.ensureTable_window.Btn_ensure_ok.clicked.connect(self.close)

    def show_cpSettings_window(self):
        self.cpSettings.show()

    def recover_check(self):
        """
        清空所有勾选
        """
        item = self.get_QTreeItemIterator(self.TreeWidget_case)
        while item.value():
            item.value().setCheckState(0, QtCore.Qt.Unchecked)
            item.__iadd__(1)

    def saveBeTestcase(self):
        """
        将勾选的测试项保存格式
            [{'title':'xx', 'module': 'xx', 'execStatus':0, 'passCount': 10, 'failCount': 10}, {...},...]
        :return:
        """
        QTreeWidgetItemIterator = self.get_QTreeItemIterator(self.TreeWidget_case)

        module = self.getModlue()
        while QTreeWidgetItemIterator.value():
            value = QTreeWidgetItemIterator.value()

            if value.checkState(0) == QtCore.Qt.Checked and value.text(0) not in module:
                Word.be_testcase.append({'title': value.text(0), 'execStatus': 0, 'passCount': 0, 'failCount': 0})

            QTreeWidgetItemIterator.__iadd__(1)

        self.ensureTable_window.ListWidget_ensureTable.clear()

        # 用例名称添加到待测表
        if len(Word.be_testcase) != 0:
            for i in Word.be_testcase:
                self.ensureTable_window.show_case(i['title'])

            self.ensureTable_window.show()

        else:
            showEmptyMessageBox("未选择测试用例！")
            Word.log.warning("No matching data")

    def get_QTreeItemIterator(self, TreeWidget):
        return QtWidgets.QTreeWidgetItemIterator(TreeWidget)

    def get_useTable(self):
        if self.TAB.upper() == 'AP':
            return 'ap_testcases'
        else:
            return 'cp_testcases'

    def getModlue(self):
        module_list = []
        use_table = self.get_useTable()
        sql = "select DISTINCT belong from %s" % use_table
        result = pysql.exec_sql(sql)
        for i in range(len(result)):
            module_list.append(result[i]['belong'])

        return module_list

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
        item_1.setCheckState(0, QtCore.Qt.Unchecked)
        item_1.setFlags(
            QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsTristate)

        btn = QtWidgets.QPushButton()
        btn.setText(title)
        btn.setFixedSize(93, 28)
        Word.tree_btn_Dict[title] = btn
        self.TreeWidget_case.setItemWidget(item_1, 1, btn)
        title_name = item_1.text(0)
        assert title_name == title, "用例名字不匹配"
        assert QtCore.Qt.Unchecked == item_1.checkState(0)
        self.case_Qtree_dict[title_name] = item_1

    # 测试用例添加到用例表中
    def loadCase(self):
        cursor, conn = pysql.conn_db()
        self.TreeWidget_case.clear()
        useTable = self.get_useTable()
        # pysql.exec_sql("select belong, count(*) as count from %s GROUP BY belong"% useTable)
        all_case = pysql.exec_sql("select title, belong from %s" % useTable)
        # [{'title': '主叫主挂', 'belong': '通话测试'}, {'title': '主叫被挂', 'belong': '通话测试'}, {'title': '主叫拒接', 'belong':
        # '通话测试'}, {'title': '主叫未接', 'belong': '通话测试'}]

        all_module = pysql.exec_sql("select DISTINCT belong from %s order by belong" % useTable)
        cursor.close()
        conn.close()
        if all_case is None:
            self.log.info("表中无内容!")

        else:
            # 添加模块级
            for belong in all_module:
                # 返回模块title, 模块对象
                module_title, module_title_obj = self.add_top_item(belong['belong'])
                self.case_module_Qtree_dict[module_title] = module_title_obj

            # 添加测试子项
            for case in all_case:
                for case_module in self.case_module_Qtree_dict.items():
                    if case['belong'] == case_module[0]:

                        case_module_obj = self.case_module_Qtree_dict[case_module[0]]
                        self.add_item(case['title'], case_module_obj)
            self.addCaseBtn()

    def addCaseBtn(self):
        for title in Word.tree_btn_Dict:
            btn = Word.tree_btn_Dict[title]
            if title == "主叫主挂":
                btn.clicked.connect(CaseConfig_Page.caseConfig_calling_to_answer)
            elif title == "主叫被挂":
                btn.clicked.connect(CaseConfig_Page.caseConfig_caller_hangs_up)
            elif title == "主叫拒接":
                btn.clicked.connect(CaseConfig_Page.caseConfig_call_reject)
            elif title == "主叫未接":
                btn.clicked.connect(CaseConfig_Page.caseConfig_call_no_answer)
