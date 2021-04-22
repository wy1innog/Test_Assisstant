from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QDialog, QPushButton


def showEmptyMessageBox(msg):
    dialog = QDialog()
    dialog.setMinimumSize(311, 140)

    font1 = QtGui.QFont()
    font1.setPointSize(10)
    btn = QPushButton("ok", dialog)
    btn.setGeometry(QtCore.QRect(110, 100, 91, 40))
    btn.setFont(font1)
    btn.clicked.connect(dialog.close)

    label_mes = QtWidgets.QLabel(dialog)
    label_mes.setGeometry(QtCore.QRect(80, 40, 151, 41))
    font = QtGui.QFont()
    font.setFamily("微软雅黑")
    font.setPointSize(12)
    label_mes.setFont(font)
    label_mes.setText(msg)

    dialog.setWindowTitle("提示")
    dialog.exec_()
