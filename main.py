import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication

from mainpage import MainPage

if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    mainpage = MainPage()
    mainpage.show()

    sys.exit(app.exec_())
