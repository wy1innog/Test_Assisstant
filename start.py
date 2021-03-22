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
    set_page = Default_settings()
    at_page = At_settings()
    ass.Menu_Settings.triggered.connect(set_page.show)
    ass.Menu_Atmgr_action.triggered.connect(at_page.show)
    ass.show()

    sys.exit(app.exec_())