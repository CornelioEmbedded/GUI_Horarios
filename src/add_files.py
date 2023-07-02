from PyQt5 import uic
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
import sys
import pandas as pd
import convertion
import random
import configparser


class AddFilesScreen(QWidget):
    csv_file = None
    def __init__(self):
        super(AddFilesScreen, self).__init__()
        uic.loadUi(r'ui_files\add_files.ui', self)

        ## Buttons
        self.ordinary_class_button = self.findChild(QPushButton, 'add_ordinary_class')
        self.labs_button = self.findChild(QPushButton, 'add_labs')
        self.saturdays_button = self.findChild(QPushButton, 'add_saturdays_class')

        self.ordinary_class_button.clicked.connect(self.ordinary_class_click)
        # self.labs_button.clicked.connect()
        # self.saturdays_button.clicked.connect()
    
    def ordinary_class_click(self):
        """Open excel file, and return a new items list from excel"""
        file, _ = QFileDialog.getOpenFileName(self, 'Open File', 'c:\\', 'Excel Files (*.xlsx)')
        print(convertion.from_excel_to_csv(file))

