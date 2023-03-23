import pandas as pd
import re
from unidecode import unidecode

NAME_COLUMN = '        09/01/23                             UNIVERSIDAD AUTONOMA DE NUEVO LEON                                Pag  1'

def from_excel_to_csv(excel_file):
    read_excel = pd.read_excel(excel_file)
    read_excel.to_csv('csv_file.csv', index=None, header=True)
    csv_file = pd.DataFrame(pd.read_csv('csv_file.csv'))
    return csv_file

def get_dict_from_csv(csv_file):
    info_list = {}
    for index, rows in csv_file.iterrows():
        info_list[index] = rows[NAME_COLUMN]
    return info_list

def parse_classes(classes):
    class_list = []
    for items in classes.values():
        if type(items) == str:
            if '420' in items or '401' in items:
                class_list.append('&')
            if 'ESPAÑOL'in items or 'INGLES' in items:
                class_list.append(items)
                class_list.append('\n')
    string_classes = ''.join(class_list).replace('_','').split('&')
    return string_classes

def _get_subject_name(subject):
    pattern = r'(?P<suject>\D\w\D+)'
    try:
        subject_name = re.search(pattern, subject).group()
    except AttributeError:
        subject_name = re.search(pattern, subject)
    return subject_name

def get_subject_list(subjects):
    subject_list = []
    for subject in subjects:
        subject_list.append(_get_subject_name(subject))
    return subject_list

def find_class(subject, string_classes):
    for string in string_classes:
        if subject in string:
            ordered_string = string.split(_get_subject_name(subject))[1]
            # new_ordered_str = " ".join(ordered_string.split())
            list_of_classes = ordered_string.split('\n')
            return list_of_classes, ordered_string

def clean_list_of_classes(list_of_classes):
    new_subject_list = []
    for subject in list_of_classes:
        new_subject_list.append(" ".join(subject.split()))
    return new_subject_list

def get_classes_data(class_items):
    pattern = r'(?P<hour>[0-9A-Za-z]+),(?P<amount_hours>[0-9]+) (?P<day>[0-9]+) (?P<room>[0-9A-Za-z]+) (?P<id>[0-9A-Za-z]+) (?P<professor>([A-Za-z]+( [A-Za-z]+)+))'
    class_data = ('Hour', 'Amount of hours', 'Day', 'Classroom', 'Professor ID', 'Professor')
    list_dict = []
    try:
        for class_item in class_items:
            subject = unidecode(class_item)
            try:
                parsed_class_data = list(re.search(pattern, subject).groups())
            except AttributeError:
                parsed_class_data = list(re.search(pattern,  subject))        
            class_dict = dict(zip(class_data, parsed_class_data))
            list_dict.append(class_dict)
    except TypeError:
        pass
    return list_dict

