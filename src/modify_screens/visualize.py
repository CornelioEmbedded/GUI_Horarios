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


class VisualizeScreen(QWidget):
    def __init__(self):
        super(VisualizeScreen, self).__init__()
        uic.loadUi(r'ui_files\schedule_grid.ui', self)
