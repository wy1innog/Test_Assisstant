import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication

from mainpage import Ass

if __name__ == '__main__':
    attribute = QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    ass = Ass()
    ass.show()

    sys.exit(app.exec_())
