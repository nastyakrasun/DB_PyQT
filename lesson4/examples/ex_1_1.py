"""
Подключаем файл с разметкой интерфейса, созданного через qtdesigner
(вариант без создания класса MyWindow)
"""

import sys
from PyQt5.QtWidgets import QWidget, QApplication, qApp
from PyQt5 import uic


APP = QApplication(sys.argv)
WINDOW_OBJ = QWidget()
UI = uic.loadUi('test.ui', WINDOW_OBJ)
UI.btnQuit.clicked.connect(qApp.quit)
WINDOW_OBJ.show()

sys.exit(APP.exec_())
