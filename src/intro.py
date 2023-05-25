from PyQt5 import uic
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
import sys
import pandas as pd
import convertion
import random
import configparser


class IntroScreen(QWidget):
    def __init__(self):
        super(IntroScreen, self).__init__()
        uic.loadUi('intro.ui', self)

        ## variables
        self.subject = None
        self.string_classes= None

        ## Buttons
        self.mecatronica_button = self.findChild(QPushButton, 'mecatronica_button')
        self.biomedica_button = self.findChild(QPushButton, 'biomedica_button')
        self.open_file_button = self.findChild(QPushButton, 'open_file_button_button')

        ## Combo Box Subjects
        self.subject_menu = self.findChild(QComboBox, 'subject_menu')
        self.subject_menu.addItems(self.get_previous_data()[0])
        self.subject_menu.currentIndexChanged.connect(self._selection_change)
        self.count_selections_classes = [0] * self.subject_menu.count()

        ## Combo Box Professors
        self.subject_menu_prof = self.findChild(QComboBox, 'subject_menu_2')
        self.subject_menu_prof.addItems(self.get_previous_data()[1])
        self.subject_menu_prof.currentIndexChanged.connect(self._selection_change)
        self.count_selections_classes_prof = [0] * self.subject_menu_prof.count()

        ## Button actions
        self.mecatronica_button.clicked.connect(self.mecatronica_button_click)
        self.biomedica_button.clicked.connect(self.biomedica_button_click)
        self.open_file_button.clicked.connect(self.open_file)

        ## Schedule grid
        self.schedule_grid = self.findChild(QGridLayout, 'grid_schedule')
        self.rows = {'M1': 1,
                     'M2': 2,
                     'M3': 3,
                     'M4': 4,
                     'M5': 5,
                     'M6': 6,
                     'V1': 7,
                     'V2': 8,
                     'V3': 9,
                     'V4': 10,
                     'V5': 11,
                     'V6': 12,
                     'N1': 13,
                     'N2': 14,
                     'N3': 15,
                     'N4': 16,
                     'N5': 17,
                     'N6': 18}
        
        self.columns = {'1': 1,
                        '2': 2,
                        '3': 3,
                        '4': 4,
                        '5': 5,
                        '6': 6}

        self.set_grid_dimmensions()

        ## Initialize functions
        self.show()

################# SETUP METHODS ##########################

    def set_default_colors(self):
        config = configparser.ConfigParser()
        config.add_section('professors_colors')
        _, professors_names = self._make_professor_items()
        for item in professors_names:
            color = f'#{random.randint(0, 0xFFFFFF):06x}'  # Assigning random colors
            config.set('professors_colors',  item, color)

            with open(r'parameters\config.ini', 'w') as configfile:
                config.write(configfile)

    def get_previous_data(self):
        """"Gets previous data from past csv_file"""
        try:
            csv_file_read = pd.read_csv('csv_file.csv')
            self._parsing_csv_file(csv_file_read)
            self.items_list = self._make_subject_items()
            self.items_list_prof, _ = self._make_professor_items()
            return self.items_list, self.items_list_prof
        except FileNotFoundError:
            self.items_list = []
            return self.items_list

    def mecatronica_button_click(self):
        print('mecatronica')

    def biomedica_button_click(self):
        print('biomedica')

    def open_file(self):
        """Open excel file, and return a new items list from excel"""
        file, _ = QFileDialog.getOpenFileName(self, 'Open File', 'c:\\', 'Excel Files (*.xlsx)')
        csv_file = convertion.from_excel_to_csv(file)
        self._parsing_csv_file(csv_file)
        self.new_item_list = self._make_subject_items()
        self.new_item_list_prof, _ = self._make_professor_items()
        self.set_default_colors()
        self.subject_menu.addItems(self.new_item_list)
        self.subject_menu_prof.addItems(self.new_item_list_prof)

    def _parsing_csv_file(self, csv_file):
        """Parse in csv file to return string of classes"""
        csv_dict = convertion.get_dict_from_csv(csv_file)
        self.string_classes = convertion.parse_classes(csv_dict)

    def _make_professor_items(self):
        self.professor_list, professor_list_ini = convertion.get_professors_list(self.string_classes)
        return self.professor_list, professor_list_ini
    
    def _make_subject_items(self):
        """Convert string classes into a list to use in items"""
        self.subject_list = convertion.get_subject_list(self.string_classes)
        return self.subject_list
    
    def _selection_change(self, index):
        """Select from items combo box a subject and print it in GUI"""
        self.changes_classes_in_comboBox = self.times_selection_changed(index)
        try:
            self.clean_data_from_schedule()
            list_of_classes, current_text = convertion.find_class(self.subject_menu.currentText(), self.string_classes)
            self.cleaned_list_of_classes = convertion.clean_list_of_classes(list_of_classes)
            self.list_dict = convertion.get_classes_data(self.cleaned_list_of_classes)
            new_ordered_list = self.order_classes(self.list_dict)
            self.professors_list = self.get_professor_list(new_ordered_list)
            self.display_classes(new_ordered_list)
        except IndexError:
            pass

    def times_selection_changed(self, index):
        selectedOption = self.subject_menu.itemText(index)
        self.count_selections_classes[index] += 1
        changed_class =  self.count_selections_classes[index]
        return changed_class

################# DISPLAY CLASSES METHODS ##########################

    def set_label_in_schedule(self):
        """"Set Professor name in schedule"""
        professor_list = self.dict['Professor'].split(' ')
        short_name = ' '.join(professor_list[0:3:2])
        self.label = QLabel(short_name)
        self.set_color_class(professor_list)
        return self.label

    def set_repeated_label_in_schedule(self, index, list_dict):
        professor_list = list_dict[index]['Professor'].split(' ')
        short_name = ' '.join(professor_list[0:3:2])
        self.label = QLabel(short_name)
        self.set_color_class(professor_list)
        return self.label

    def set_color_class(self, name):
        """Set a color in label"""
        config = configparser.ConfigParser()
        config.read(r'parameters\config.ini')
        new_name = ' '.join(name)
        lower_new_name = new_name.replace(' ', '_').lower()
        color = config.get('professors_colors', f'{lower_new_name}')
        return self.label.setStyleSheet(f"background-color: {color};")

    def times_class_appears(self, list_dict, hour):
        count = 0
        for item in list_dict:
            if item.get('Hour') == hour:
                count += 1
        return f'{hour} appears {count} times'

    def get_professor_list(self, list_dict):
        professor_list = []
        for item in list_dict:
            professor_list.append(item['Professor'])
        not_repeating_professor = list(set(professor_list))
        return not_repeating_professor

    def display_classes(self, list_dict):
        """Display classes in schedule"""
        for index in range(len(list_dict)):
            self.dict = list_dict[index]
            if self.dict['Day'] == '135':
                if list_dict[index] == list_dict[-1]:
                    repeated = None
                    self.set_LMV_classes(repeated)
                if self.not_in_previous_hour(index, list_dict) is not True:
                    continue
                else:
                    self.LMV_display_labels(index, list_dict)
            else:
                if list_dict[index] == list_dict[-1]:
                    repeated = None
                    self.set_MJ_classes(repeated)
                if self.not_in_previous_hour(index, list_dict) is not True:
                    continue
                else:
                    self.MJ_display_labels(index, list_dict)

    def LMV_display_labels(self, index, list_dict):
        if self.not_repeated_hour(index, list_dict) is not True:
            repeated = True
            list_days = self.set_LMV_classes(repeated)
            self.check_repeated_hour_classes(index, list_dict, list_days)
        else:
            repeated = False
            list_days = self.set_LMV_classes(repeated)

    def MJ_display_labels(self, index, list_dict):
        if self.not_repeated_hour(index, list_dict) is not True:
            repeated = True
            list_days = self.set_MJ_classes(repeated)
            self.check_repeated_hour_classes(index, list_dict, list_days)
        else:
            repeated = False
            list_days = self.set_MJ_classes(repeated)

    def not_repeated_hour(self, index, list_dict):
        next = index + 1
        first_hour = self.dict['Hour']
        next_hour = list_dict[next]['Hour']
        state = False
        if first_hour != next_hour:
            state = True
        return state

    def not_in_previous_hour(self, index, list_dict):
        previous = index - 1
        actual_hour = self.dict['Hour']
        previous_hour = list_dict[previous]['Hour']
        state = False
        if actual_hour != previous_hour:
            state = True
        return state

    def check_repeated_hour_classes(self, index, list_dict, list_days):
        next = index + 1
        first_hour = self.dict['Hour']
        next_hour = list_dict[next]['Hour']
        day = self.dict['Day']
        if first_hour == next_hour and day == list_dict[next]['Day']:
            if list_days == 'Class of three hours':
                three_hour = self.separate_hour_from_class(next_hour)
                for hour in three_hour:
                    self.find_replace_repeated_data(hour, day, next, list_dict)
            elif type(list_days) == list:
                for day in list_days:
                    self.find_replace_repeated_data(next_hour, day, next, list_dict)

    def find_replace_repeated_data(self, hour, day, index, list_dict):
        spot = self.findChild(QHBoxLayout, f'{hour}_{day}')
        if self.changes_classes_in_comboBox > 1 and spot.count() >= 2:
            old_label = spot.itemAt(0).widget()
            spot.removeWidget(old_label)
        label = self.set_repeated_label_in_schedule(index, list_dict)
        spot.addWidget(label)

    def set_LMV_classes(self, state):
        """Set Monday, Wednesday and Friday classes"""
        days = self.dict['Day']
        hour = self.dict['Hour']
        days_list = [int(days[0]), int(days[1]), int(days[2])]
        # real_color = self.get_professor_color()
        for day in days_list:
            self.find_hour_replace_data(hour, day, state)
        return days_list

    def set_MJ_classes(self, status):
        """Set Tuesday and Thursday classes"""
        day = self.dict['Day']
        real_hour = self.dict['Hour']
        three_hour = self.separate_hour_from_class(real_hour)
        # real_color = self.get_professor_color()
        for hour in three_hour:
            self.find_hour_replace_data(hour, day, status)
        return 'Class of three hours'

    def separate_hour_from_class(self, hour):
        numeric_part = int(hour[1:])
        letter_part = str(hour[:1])
        next_numbers = [numeric_part, numeric_part+1, numeric_part+2]
        three_hour = [letter_part + str(num) for num in next_numbers]
        return three_hour

    def clean_labels_from_no_repeated_class(self, spot):
        oldest_label_1 = spot.itemAt(spot.count() - 1).widget()
        oldest_label_2 = spot.itemAt(spot.count() - 2).widget()
        spot.removeWidget(oldest_label_1)
        spot.removeWidget(oldest_label_2)

    def find_hour_replace_data(self, hour:str, day:str, state):
        spot = self.findChild(QHBoxLayout, f'{hour}_{day}')
        if spot.count() >= 2 and state is False:
            self.clean_labels_from_no_repeated_class(spot)
        else:
            old_label = spot.itemAt(0).widget()
            spot.removeWidget(old_label)
        label = self.set_label_in_schedule()
        spot.addWidget(label)

    def clean_data_from_schedule(self):
        """Clean data from schedule"""
        for i in range(self.schedule_grid.count()):
            item = self.schedule_grid.itemAt(i)
            if item is not None:
                layout = item.layout()
                if layout is not None:
                    for j in range(layout.count()):
                        widget = layout.itemAt(j).widget()
                        if isinstance(widget, QLabel):
                            widget.setStyleSheet("")
                            widget.setText("")

################# ORDER CLASSES METHODS ##########################

    def _order_key(self, order_dict, dict):
        return order_dict[dict['Hour']]

    def order_classes_by_hour(self, list_dict):
        sorted_list = sorted(list_dict, key=lambda dict: self._order_key(self.rows, dict))
        return sorted_list

    def order_classes_by_day(self, list_dict):
        list_135 = []
        list_24 = []

        for dict in list_dict:
            if '135' in dict['Day']:
                list_135.append(dict)
            elif '2' in dict['Day'] or '4' in dict['Day']:
                list_24.append(dict)
        new_order = list_135 + list_24
        return new_order

    def order_classes(self, list_dict):
        list_by_hour = self.order_classes_by_hour(list_dict)
        list_by_day = self.order_classes_by_day(list_by_hour)
        return list_by_day

################# GRID METHODS ##########################

    def set_grid_dimmensions(self):
        factor = 1
        for column in self.columns.values():
            self.schedule_grid.setColumnStretch(column, factor)
        for row in self.rows.values():
            self.schedule_grid.setRowStretch(row, factor)



app = QApplication(sys.argv) 
window = IntroScreen() 
app.exec_() 