from PyQt5 import uic
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
import sys
import pandas as pd
import convertion
import csv

class IntroScreen(QWidget):
    def __init__(self):
        super(IntroScreen, self).__init__()
        uic.loadUi('intro.ui', self)

        ## Line Edit
        self.writer_subject = self.findChild(QLineEdit, 'line_writer')

        ## Texts
        self.subject_info = self.findChild(QLabel, 'subject_response')

        ## Buttons
        self.mecatronica_button = self.findChild(QPushButton, 'mecatronica_button')
        self.biomedica_button = self.findChild(QPushButton, 'biomedica_button')
        self.open_file_button = self.findChild(QPushButton, 'open_file_button_button')
        self.enter_button = self.findChild(QPushButton, 'enter_button')

        ## Button actions
        self.mecatronica_button.clicked.connect(self.mecatronica_button_click)
        self.biomedica_button.clicked.connect(self.biomedica_button_click)
        self.open_file_button.clicked.connect(self.open_file)
        self.enter_button.clicked.connect(self.try_open_csv)

        ## variables
        self.subject = None
        self.string_classes= None

        self.try_open_csv()
        self.show()

    def try_open_csv(self):
        try:
            csv_file_read = pd.read_csv('csv_file.csv')
            self.parsing_csv_file(csv_file_read)
            self.get_subject()
        except FileNotFoundError:
            print('Archivo no encontrado')

    def mecatronica_button_click(self):
        print('mecatronica')

    def biomedica_button_click(self):
        print('biomedica')

    def open_file(self):
        file, _ = QFileDialog.getOpenFileName(self, 'Open File', 'c:\\', 'Excel Files (*.xlsx)')
        csv_file = convertion.from_excel_to_csv(file)
        self.parsing_csv_file(csv_file)

    def parsing_csv_file(self, csv_file):
        csv_dict = convertion.get_dict_from_csv(csv_file)
        self.string_classes = convertion.parse_classes(csv_dict)

    def get_subject(self):
        self.subject = convertion.find_class(self.writer_subject.text(), self.string_classes)
        self.subject_info.setText(self.subject)



app = QApplication(sys.argv) 
window = IntroScreen() 
app.exec_() 