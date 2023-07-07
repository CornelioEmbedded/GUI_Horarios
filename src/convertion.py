import pandas as pd
import re
from unidecode import unidecode

NAME_COLUMN = '        01/07/23                             UNIVERSIDAD AUTONOMA DE NUEVO LEON                                Pag  1'
MAIN_PATTERN = r'(?P<hour>[0-9A-Za-z]+),(?P<amount_hours>[0-9]+) (?P<day>[0-9]+) (?P<room>[0-9A-Za-z-]+) (?P<id>[0-9A-Za-z]+) (?P<professor>([A-Za-z]+( [A-Za-z]+)+))'

# Main Function for Parsing Data

def from_excel_to_csv(excel_file, name:str):
    read_excel = pd.read_excel(excel_file)
    read_excel.to_csv(f'..\src\generated\csv_{name}.csv', index=None, header=True)

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

# Main functions for getting data from SUBJECTS

def find_class(subject, string_classes):
    for string in string_classes:
        if subject in string:
            ordered_string = string.split(_get_subject_name(subject))[1]
            list_of_classes = ordered_string.split('\n')
            return list_of_classes, ordered_string

def clean_list_of_classes(list_of_classes):
    new_subject_list = []
    for subject in list_of_classes:
        new_subject_list.append(" ".join(subject.split()))
    return new_subject_list

def get_classes_data(class_items):
    pattern = MAIN_PATTERN
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

# Support functions for SUBJECTS

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
        if subject == '':
            pass
        else:
            subject_list.append(_get_subject_name(subject))
    sorted_list = sorted(subject_list)
    sorted_list.insert(0, '')
    return sorted_list

# Main functions for getting data from PROFESSORS

def find_professors(professor, string_classes):
    pattern = MAIN_PATTERN
    class_data = ('Subject','Hour', 'Amount of hours', 'Day', 'Classroom', 'Professor ID', 'Professor')
    list_dict = []
    for string in string_classes:
        cleaned_string = unidecode(string)
        if professor in cleaned_string:
            cleaned_string = ' '.join(cleaned_string.split())
            subject = _get_subject_name(cleaned_string)
            try:
                parsed_class_data = list(re.findall(pattern, cleaned_string).groups())
            except AttributeError:
                parsed_class_data = list(re.findall(pattern, cleaned_string))
            for i in parsed_class_data:
                new_parsed = list(i)
                new_parsed.insert(0, subject)
                new_parsed = tuple(new_parsed)
                class_dict = dict(zip(class_data, tuple(new_parsed)))
                list_dict.append(class_dict)
    professor_list = _get_professors_hours(professor, list_dict)
    return professor_list

def _get_professors_hours(professor, list_dict):
    professor_hours = []
    for item in list_dict:
        if professor in item['Professor']:
            professor_hours.append(item)
    return professor_hours        

def get_professors_list(subject):
    new_subject_str = ''.join(subject)
    pattern = r'(?P<professor>\w\w\d\d\d\d\D\w\D+)'
    try:
        professor_names = re.findall(pattern, new_subject_str)
    except AttributeError:
        professor_names = re.findall(pattern, new_subject_str)
    professor_names_ini, professor_names_gui = _make_professor_list_readable(professor_names)
    og_professor_names = sorted(list(set(professor_names_gui)))
    og_professor_names_ini = sorted(list(set(professor_names_ini)))
    og_professor_names.insert(0, '')
    return og_professor_names, og_professor_names_ini

def _make_professor_list_readable(professor_list):
    new_list_underscore = []
    new_list_normal = []
    for item in professor_list:
        new_item = unidecode(item)
        cleaned_string = ' '.join(new_item.split())
        cleaned_list = cleaned_string.split(' ')
        del cleaned_list[0]
        recleaned_string = ' '.join(cleaned_list)
        recleaned_string_underscore = '_'.join(cleaned_list)
        new_list_normal.append(recleaned_string)
        new_list_underscore.append(recleaned_string_underscore)
    return new_list_underscore, new_list_normal
