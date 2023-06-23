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


class AddClassScreen(QWidget):
    def __init__(self):
        super(AddClassScreen, self).__init__()
        uic.loadUi(r'ui_files\add_class.ui', self)

        ## Initialize functions

        self.show()
    