from PyQt5 import uic
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
import sys
import pandas as pd


class MainScreen(QMainWindow):
    def __init__(self):
        super(MainScreen, self).__init__()
        uic.loadUi(r'ui_files\main.ui', self)

        ## Initialize functions
        self.show()


app = QApplication(sys.argv) 
window = MainScreen() 
app.exec_() 
