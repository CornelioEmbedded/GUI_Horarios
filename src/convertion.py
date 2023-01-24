import pandas as pd

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

def find_classes(classes):
    class_list = []
    for items in classes.values():
        if type(items) == str:
                if 'ESPAÑOL'in items or 'INGLES' in items:
                    class_list.append(items)
    string_classes = ''.join(class_list)
    return string_classes
        

# def accomodate_classes(class_list):
#     separate_class_list = []
#     count = 0
#     for items in class_list:
#         count += 1
#         if '420' in items or '401' in items:
#             items_list = []
#             items_list.append(items)
#             for  
        