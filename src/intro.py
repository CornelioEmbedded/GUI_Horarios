from PyQt5 import uic
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
import sys
import pandas as pd
import convertion


class IntroScreen(QWidget):
    def __init__(self):
        super(IntroScreen, self).__init__()
        uic.loadUi('intro.ui', self)

        ## variables
        self.subject = None
        self.string_classes= None
        self.subject_list = []

        ## Texts
        self.subject_info = self.findChild(QLabel, 'subject_response')

        ## Buttons
        self.mecatronica_button = self.findChild(QPushButton, 'mecatronica_button')
        self.biomedica_button = self.findChild(QPushButton, 'biomedica_button')
        self.open_file_button = self.findChild(QPushButton, 'open_file_button_button')

        ## Combo Box
        self.subject_menu = self.findChild(QComboBox, 'subject_menu')
        self.subject_menu.addItems(self.try_open_csv())
        self.subject_menu.currentIndexChanged.connect(self.selection_change)

        ## Button actions
        self.mecatronica_button.clicked.connect(self.mecatronica_button_click)
        self.biomedica_button.clicked.connect(self.biomedica_button_click)
        self.open_file_button.clicked.connect(self.open_file)

        ## Initialize functions
        self.show()

    def try_open_csv(self):
        try:
            csv_file_read = pd.read_csv('csv_file.csv')
            self.parsing_csv_file(csv_file_read)
            self.items_list = self.make_subject_items()
            return self.items_list
        except FileNotFoundError:
            self.items_list = []
            return self.items_list

    def mecatronica_button_click(self):
        print('mecatronica')

    def biomedica_button_click(self):
        print('biomedica')

    def open_file(self):
        file, _ = QFileDialog.getOpenFileName(self, 'Open File', 'c:\\', 'Excel Files (*.xlsx)')
        csv_file = convertion.from_excel_to_csv(file)
        self.parsing_csv_file(csv_file)
        self.subject_list = self.make_subject_items()
        self.subject_menu.addItems(self.subject_list)

    def parsing_csv_file(self, csv_file):
        csv_dict = convertion.get_dict_from_csv(csv_file)
        self.string_classes = convertion.parse_classes(csv_dict)
    
    def make_subject_items(self):
        self.subject_list = convertion.get_subject_list(self.string_classes)
        return self.subject_list
    
    def selection_change(self):
        current_text = convertion.find_class(self.subject_menu.currentText(), self.string_classes)
        self.subject_info.setText(current_text)


app = QApplication(sys.argv) 
window = IntroScreen() 
app.exec_() 