from PyQt5 import uic
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
import sys
import pandas as pd
from subjects import SubjectsScreen


class MainScreen(QMainWindow):
    def __init__(self):
        super(MainScreen, self).__init__()
        uic.loadUi(r'ui_files\main.ui', self)

        ## Buttons
        self.subjects_button = self.findChild(QPushButton, 'subjects')
        self.professor_button = self.findChild(QPushButton, 'professors')
        self.modifying_button = self.findChild(QPushButton, 'modifying')
        self.information_button = self.findChild(QPushButton, 'information')
        self.configuration_button = self.findChild(QPushButton, 'configuration')

        ##Buttons actions
        self.subjects_button.clicked.connect(self.subjects_button_click)
        self.professor_button.clicked.connect(self.professors_button_click)
        self.modifying_button.clicked.connect(self.modifying_button_click)
        self.information_button.clicked.connect(self.information_button_click)
        self.configuration_button.clicked.connect(self.configuration_button_click)
        
        ## Initialize functions
        self.show()
    
    def subjects_button_click(self):
        spot = self.findChild(QFrame, 'frame_4')
        new_spot = QVBoxLayout(spot)
        new_spot.addWidget(SubjectsScreen())
        self.subjects_button.setEnabled(False)
    
    def professors_button_click(self):
        print('professors')
    
    def modifying_button_click(self):
        print('modifying')
    
    def information_button_click(self):
        print('information')
    
    def configuration_button_click(self):
        print('configuration')


app = QApplication(sys.argv)
window = MainScreen() 
app.exec_() 
