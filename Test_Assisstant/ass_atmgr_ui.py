# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_at_mgr_ih002.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(346, 345)
        self.listWidget = QtWidgets.QListWidget(Dialog)
        self.listWidget.setGeometry(QtCore.QRect(30, 50, 256, 261))
        self.listWidget.setObjectName("listWidget")

        # 按钮： +
        self.btn_add = QtWidgets.QPushButton(Dialog)
        self.btn_add.setGeometry(QtCore.QRect(300, 80, 31, 31))
        self.btn_add.setObjectName("pushButton")

        # 按钮： -
        self.btn_sub = QtWidgets.QPushButton(Dialog)
        self.btn_sub.setGeometry(QtCore.QRect(300, 150, 31, 31))
        self.btn_sub.setObjectName("pushButton_2")

        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(120, 10, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "AT指令管理"))
        self.btn_add.setText(_translate("Dialog", "+"))
        self.btn_sub.setText(_translate("Dialog", "-"))
        self.label.setText(_translate("Dialog", "AT指令管理"))
