from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QDialog, QPushButton

from ui.caseTableUI import Ui_Testcase_table
from caseConfig_Page import CaseConfig_Page
from ensureCaseTable_Page import EnsureCaseTable_Page
import common.pysql_connect as pysql
from common.log import Log
import Word


class CaseTable_Page(QMainWindow, Ui_Testcase_table):

    def __init__(self, Tab):
        super().__init__()
        self.setupUi(self)
        self.log = Log(__name__).getlog()
        self.TAB = Tab
        self.case_Qtree_dict = {}
        self.case_module_Qtree_dict = {}
        self.init()

    def init(self):

        self.caseConfig_window = CaseConfig_Page()
        self.ensureTable_window = EnsureCaseTable_Page()
        self.Btn_cancel_case.clicked.connect(self.close)
        self.Btn_save_case.clicked.connect(self.saveBeTestcase)
        self.ensureTable_window.Btn_ensure_ok.clicked.connect(self.close)
        # self.ensureTable_window.Btn_ensureTable_cancel.clicked.connect(self.clearList)
        self.Btn_config_case.clicked.connect(self.show_caseConfig_window)



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
        dialog.exec_()

    def saveBeTestcase(self):
        """
        将勾选的测试项保存格式
            [{'title':'xx', 'module': 'xx', 'execStatus':0, 'passCount': 10, 'failCount': 10}, {...},...]
        :return:
        """
        # self.load_ensure_case()
        QTreeWidgetItemIterator = self.get_QTreeItemIterator(self.TreeWidget_case)

        module = self.getModlue()
        self.log.debug("module : %s" % module)
        while QTreeWidgetItemIterator.value():
            value = QTreeWidgetItemIterator.value()

            if value.checkState(0) == QtCore.Qt.Checked and value.text(0) not in module:
                Word.be_testcase.append({'title': value.text(0), 'execStatus': 0, 'passCount': 0, 'failCount': 0})
            else:
                pass

            QTreeWidgetItemIterator.__iadd__(1)

        self.ensureTable_window.ListWidget_ensureTable.clear()

        # 用例名称添加到待测表
        if len(Word.be_testcase) != 0:
            for i in Word.be_testcase:
                self.ensureTable_window.show_case(i['title'])

            self.ensureTable_window.show()

        else:
            self.showEmptyMessageBox()
            self.log.warning("No matching data")


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
        item_1.setText(0, title)
        item_1.setCheckState(0, QtCore.Qt.Unchecked)
        item_1.setFlags(
            QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsTristate)

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
        # [{'title': '主叫主挂', 'belong': '通话测试'}, {'title': '主叫被挂', 'belong': '通话测试'}, {'title': '主叫拒接', 'belong': '通话测试'}, {'title': '主叫未接', 'belong': '通话测试'}]

        all_module = pysql.exec_sql("select DISTINCT belong from %s order by belong" % useTable)
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
                    else:
                        pass
            cursor.close()
            conn.close()
