from PyQt5 import uic
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
import sys
import pandas as pd
import tools.convertion
import random
import configparser
import os


class AddFilesScreen(QWidget):
    def __init__(self):
        super(AddFilesScreen, self).__init__()
        uic.loadUi(r'ui_files\add_files.ui', self)

        ## Buttons
        self.ordinary_class_button = self.findChild(QPushButton, 'add_ordinary_class')
        self.labs_button = self.findChild(QPushButton, 'add_labs')
        self.saturdays_button = self.findChild(QPushButton, 'add_saturday_class')

        self.ordinary_class_button.clicked.connect(self.generate_csv_from_excel_ordinary)
        self.labs_button.clicked.connect(self.generate_csv_from_excel_labs)
        self.saturdays_button.clicked.connect(self.generate_csv_from_excel_saturdays)

        self.check_existing_file()

    def generate_csv_from_excel_ordinary(self):
        """Open excel file, and return a new items list from excel"""
        try:
            file, _ = QFileDialog.getOpenFileName(self, 'Open File', 'c:\\', 'Excel Files (*.xlsx)')
            tools.convertion.from_excel_to_csv(file, "ordinarios")
        except FileNotFoundError:
            pass

    def generate_csv_from_excel_labs(self):
        """Open excel file, and return a new items list from excel"""
        try:
            file, _ = QFileDialog.getOpenFileName(self, 'Open File', 'c:\\', 'Excel Files (*.xlsx)')
            tools.convertion.from_excel_to_csv(file, "labs")
        except FileNotFoundError:
            pass

    def generate_csv_from_excel_saturdays(self):
        """Open excel file, and return a new items list from excel"""
        try:
            file, _ = QFileDialog.getOpenFileName(self, 'Open File', 'c:\\', 'Excel Files (*.xlsx)')
            tools.convertion.from_excel_to_csv(file, "sabatinos")
        except FileNotFoundError:
            pass

    def check_existing_file(self):
        csv_files = {'ordinarios': self.ordinary_class_button,
                        'labs': self.labs_button,
                        'sabatinos': self.saturdays_button}

        for file in csv_files.keys():
            file_exists = os.path.isfile(f'generated\csv_{file}.csv')
            if file_exists:
                button = csv_files[file]
                button.setEnabled(False)