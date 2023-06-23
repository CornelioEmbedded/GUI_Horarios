from PyQt5 import uic
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
import sys
import pandas as pd
from subjects import SubjectsScreen
from professors import ProfessorsScreen
import convertion
import configparser
import random


class ModifyScreen(QWidget):
    def __init__(self):
        super(ModifyScreen, self).__init__()
        uic.loadUi(r'ui_files\main_modify.ui', self)

        self.string_classes = None

        ## Buttons
        self.add_button = self.findChild(QPushButton, 'add')
        self.visualize_button = self.findChild(QPushButton, 'visualize')
        self.modifying_button = self.findChild(QPushButton, 'modifying')

        ##Buttons actions
        self.add_button.clicked.connect(self.add_button_click)
        self.visualize_button.clicked.connect(self.professors_button_click)
        self.modifying_button.clicked.connect(self.modifying_button_click)
        
        ## Initialize functions

        self.show()
    
    def add_button_click(self):
        pass
    
    def professors_button_click(self):
        pass
    
    def modifying_button_click(self):
        pass

    def _enable_all_buttons(self):
        self.add_button.setEnabled(True)
        self.visualize_button.setEnabled(True)
        self.modifying_button.setEnabled(True)