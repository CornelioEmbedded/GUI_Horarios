from PyQt5 import uic
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
import sys
import pandas as pd
from subjects import SubjectsScreen
from professors import ProfessorsScreen
import tools.convertion
import configparser
import random
import json


class AddClassScreen(QWidget):
    def __init__(self, subjects, professors):
        super(AddClassScreen, self).__init__()
        uic.loadUi(r'ui_files\add_class.ui', self)

        self.subject = subjects
        self.professors = professors
        self.plan = ['','401', '420']
        self.hour = ['',
                     'M1',
                     'M2',
                     'M3',
                     'M4',
                     'M5',
                     'M6',
                     'V1',
                     'V2',
                     'V3',
                     'V4',
                     'V5',
                     'V6',
                     'N1',
                     'N2',
                     'N3',
                     'N4',
                     'N5',
                     'N6']
        self.days = ['',
                     'L-M-V',
                     'M',
                     'J',
                     'Sab']
        self.offer = ['','Escolarizada', 'No Escolar']
        self.platform = ['','N/A','NEXUS']
        self.modality = ['','ESPANOL', 'INGLES']

        # Combo Box subjects
        self.subject_menu = self.findChild(QComboBox, 'subject')
        self.subject_menu.addItems(self.subject)
        self.subject_menu.currentIndexChanged.connect(self._selection_change)
        self.count_selections_subjects = [0] * self.subject_menu.count()

        # Combo Box professors
        self.professor_menu = self.findChild(QComboBox, 'professor')
        self.professor_menu.addItems(self.professors)
        self.professor_menu.currentIndexChanged.connect(self._selection_change)
        self.count_selections_professors = [0] * self.professor_menu.count()

        # Combo Box plan
        self.plan_menu = self.findChild(QComboBox, 'plan')
        self.plan_menu.addItems(self.plan)
        self.plan_menu.currentIndexChanged.connect(self._selection_change)
        self.count_selections_professors = [0] * self.plan_menu.count()

        # Combo Box hour
        self.hour_menu = self.findChild(QComboBox, 'hour')
        self.hour_menu.addItems(self.hour)
        self.hour_menu.currentIndexChanged.connect(self._selection_change)
        self.count_selections_professors = [0] * self.hour_menu.count()

        # Combo Box day
        self.day_menu = self.findChild(QComboBox, 'day')
        self.day_menu.addItems(self.days)
        self.day_menu.currentIndexChanged.connect(self._selection_change)
        self.count_selections_professors = [0] * self.day_menu.count()

        # Combo Box offer
        self.offer_menu = self.findChild(QComboBox, 'offer')
        self.offer_menu.addItems(self.offer)
        self.offer_menu.currentIndexChanged.connect(self._selection_change)
        self.count_selections_professors = [0] * self.offer_menu.count()

        # Combo Box platform
        self.platform_menu = self.findChild(QComboBox, 'platform')
        self.platform_menu.addItems(self.platform)
        self.platform_menu.currentIndexChanged.connect(self._selection_change)
        self.count_selections_professors = [0] * self.platform_menu.count()

        # Combo Box modality
        self.modality_menu = self.findChild(QComboBox, 'modality')
        self.modality_menu.addItems(self.modality)
        self.modality_menu.currentIndexChanged.connect(self._selection_change)
        self.count_selections_professors = [0] * self.offer_menu.count()

        ## Line Text
        self.group = self.findChild(QLineEdit, 'group')
        self.room = self.findChild(QLineEdit, 'room')

        ## Buttons
        self.accept_button = self.findChild(QPushButton, 'accept')

        ## Buttons actions
        self.accept_button.clicked.connect(self.accept_button_click)

        ## Initialize functions

    def _selection_change(self):
        pass

    def accept_button_click(self):
        self.added_data = {'Hour':self.hour_menu.currentText(), 
                      'Day':self.day_menu.currentText(),
                      'Professor':self.professor_menu.currentText(),
                      'Subject':self.subject_menu.currentText(),
                      'Plan':self.plan_menu.currentText(),
                      'Offer':self.offer_menu.currentText(),
                      'Platform':self.platform_menu.currentText(),
                      'Modality':self.modality_menu.currentText(),
                      'Group':self.group.text(),
                      'Room':self.room.text()}
        
        # Store the dictionary as JSON
        with open("data\data.json", "a") as file:
            json.dump(self.added_data, file, indent=2, separators=(",\n", ": "))
            file.write("\n")

        print(f'{self.added_data}')
