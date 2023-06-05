from PyQt5 import uic
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
import sys
import pandas as pd
from subjects import SubjectsScreen
import convertion
import configparser
import random


class MainScreen(QMainWindow):
    def __init__(self):
        super(MainScreen, self).__init__()
        uic.loadUi(r'ui_files\main.ui', self)

        self.string_classes = None

        ## Buttons
        self.subjects_button = self.findChild(QPushButton, 'subjects')
        self.professor_button = self.findChild(QPushButton, 'professors')
        self.modifying_button = self.findChild(QPushButton, 'modifying')
        self.information_button = self.findChild(QPushButton, 'information')
        self.configuration_button = self.findChild(QPushButton, 'configuration')
        self.open_file_button = self.findChild(QPushButton, 'open_files')
        self.clean_button = self.findChild(QPushButton, 'clean')

        ##Buttons actions
        self.subjects_button.clicked.connect(self.subjects_button_click)
        self.professor_button.clicked.connect(self.professors_button_click)
        self.modifying_button.clicked.connect(self.modifying_button_click)
        self.information_button.clicked.connect(self.information_button_click)
        self.configuration_button.clicked.connect(self.configuration_button_click)
        self.open_file_button.clicked.connect(self.open_file)
        self.clean_button.clicked.connect(self.clean_gui)
        
        ## Initialize functions
        self.items_list = self.get_previous_data()
        self.show()
    
    def subjects_button_click(self):
        spot = self.findChild(QFrame, 'frame_4')
        new_spot = QVBoxLayout(spot)
        new_items_list = self.get_previous_data()
        new_spot.addWidget(SubjectsScreen(new_items_list, self.string_classes))
        self.subjects_button.setEnabled(False)
    
    def professors_button_click(self):
        print('professors')
    
    def modifying_button_click(self):
        print('modifying')
    
    def information_button_click(self):
        print('information')
    
    def configuration_button_click(self):
        print('configuration')

    def clean_gui(self):
        pass

    def open_file(self):
        """Open excel file, and return a new items list from excel"""
        file, _ = QFileDialog.getOpenFileName(self, 'Open File', 'c:\\', 'Excel Files (*.xlsx)')
        csv_file = convertion.from_excel_to_csv(file)
        self._parsing_csv_file(csv_file)
        self.new_item_list = self._make_subject_items()
        self.new_item_list_prof, _ = self._make_professor_items()
        self.set_default_colors()

    def get_previous_data(self):
        """"Gets previous data from past csv_file"""
        try:
            csv_file_read = pd.read_csv('csv_file.csv')
            self._parsing_csv_file(csv_file_read)
            items_list = self._make_subject_items()
            return items_list
        except FileNotFoundError:
            items_list = []
            return items_list

    def _parsing_csv_file(self, csv_file):
        """Parse in csv file to return string of classes"""
        csv_dict = convertion.get_dict_from_csv(csv_file)
        self.string_classes = convertion.parse_classes(csv_dict)

    def _make_subject_items(self):
        """Convert string classes into a list to use in items"""
        self.subject_list = convertion.get_subject_list(self.string_classes)
        return self.subject_list

    def _make_professor_items(self):
        self.professor_list, professor_list_ini = convertion.get_professors_list(self.string_classes)
        return self.professor_list, professor_list_ini

    def set_default_colors(self):
        config = configparser.ConfigParser()
        config.add_section('professors_colors')
        _, professors_names = self._make_professor_items()
        for item in professors_names:
            color = f'#{random.randint(0, 0xFFFFFF):06x}'  # Assigning random colors
            config.set('professors_colors',  item, color)

            with open(r'parameters\config.ini', 'w') as configfile:
                config.write(configfile)



app = QApplication(sys.argv)
window = MainScreen() 
app.exec_() 
