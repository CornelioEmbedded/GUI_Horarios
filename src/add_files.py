from PyQt5 import uic
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
import sys
import pandas as pd
import convertion
import random
import configparser
from functools import partial


class AddFilesScreen(QWidget):
    csv_file = None
    def __init__(self):
        super(AddFilesScreen, self).__init__()
        uic.loadUi(r'ui_files\add_files.ui', self)

        ## Buttons
        self.ordinary_class_button = self.findChild(QPushButton, 'add_ordinary_class')
        self.labs_button = self.findChild(QPushButton, 'add_labs')
        self.saturdays_button = self.findChild(QPushButton, 'add_saturday_class')

        self.ordinary_class_button.clicked.connect(lambda _, param="ordinario": self.generate_csv_from_excel(param))
        self.labs_button.clicked.connect(lambda _, param="labs": self.generate_csv_from_excel(param))
        self.saturdays_button.clicked.connect(lambda _, param="sabatino": self.generate_csv_from_excel(param))
    
    def generate_csv_from_excel(self, name):
        """Open excel file, and return a new items list from excel"""
        file, _ = QFileDialog.getOpenFileName(self, 'Open File', 'c:\\', 'Excel Files (*.xlsx)')
        convertion.from_excel_to_csv(file, name)