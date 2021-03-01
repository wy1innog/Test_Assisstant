import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication

from atpage import At_settings
from mainpage import Ass
from settingspage import Default_settings

if __name__ == '__main__':
    attribute = QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)

    ass = Ass()
    atpage = At_settings()
    setpage = Default_settings()
    at_btn = ass.actionAT_manager.triggered.connect(atpage.show)
    set_btn = ass.actionDefSet.triggered.connect(setpage.show)

    ass.show()
    sys.exit(app.exec_())