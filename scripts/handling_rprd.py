import os.path

import pandas as pd

from scripts.read_excel_file import ReadExcelFile
from scripts.config_handler import ConfigMainProgram


class RprdHandlingScript:
    def __init__(self, path_to_file: str):
        """
        Скрипт по обработки одного файла rprd 2012, сканирует и возращет базу данных(словарь) со структурой :
        {
            dse:{
                '2012':{
                    rc{
                        'rc':         rc,
                        'dse':        dse,
                        'name dse':   name_dse,
                        'yup':        yup,
                        'file name':  file_name
                        }
                    }
                }
            }
        :param path_to_file прямой путь до файла:
        """

        self.file_path = path_to_file

        self.data_for_read = {}
        self.data = {}
        self.sorted_data = {}
        self.config_porog = ConfigMainProgram()

        self.name_file = ""

    def main(self):
        """
        Основная функция скрипта
        :return: возращет базу данных(словарь) со структурой :
            {
                dse:{
                    2012:{
                        rc{
                            'rc':rc,
                            'dse':dse,
                            'name dse':name_dse,
                            'yup':yup,
                            'file name':file_name
                            }
                        }
                    }
                }
        """
        read_excel = ReadExcelFile()
        self.data_for_read = read_excel.read_excel_to_dict(self.file_path).copy()

        if self.detection_version_file(self.file_path) == 'version complete':
            self.read_complite_tabel()
            self.sorting_data_2012()
        if self.detection_version_file(self.file_path) == 'version half':
            self.read_half_tabel()
            self.sorting_data_2012()

        return self.sorted_data

    def sorting_data_2012(self):
        """
        Сортрирует данные получанные из полной версии файла
        """
        dse_data_2012 = {}

        for row, l_data in self.data.items():

            rc = l_data.get('Unnamed: 1', '')
            dse = l_data.get('Unnamed: 3', '')
            name_dse = l_data.get(' Отчет по наличию программ для станков с ЧПУ', '')
            yup = l_data.get('Unnamed: 6', '')
            if yup is None or yup == 'nan' or pd.isna(yup):
                yup = ''
            rc_data = {
                'rc': rc,
                'dse': dse,
                'name dse': name_dse,
                'yup': yup,
                'file name': self.name_file
            }

            if not dse in list(dse_data_2012.keys()): dse_data_2012[dse] = {"data_2012": {}}
            if rc in list(dse_data_2012[dse]["data_2012"].keys()):
                if yup != ' ' and not pd.isna(yup):
                    rc_data['yup'] = f"{dse_data_2012[dse]["data_2012"][rc].get('yup', '')}, {rc_data['yup']}"
                else:
                    rc_data['yup'] = f"{dse_data_2012[dse]["data_2012"][rc].get('yup', '')}"
            dse_data_2012[dse]["data_2012"][rc] = rc_data

        self.sorted_data = dse_data_2012.copy()

    def read_complite_tabel(self):
        """
        Читает файл полной версии
        :return:
        """
        for row, now_line in self.data_for_read.items():
            if row == 1: self.name_file = now_line.get(' Отчет по наличию программ для станков с ЧПУ')
            if not pd.isna(now_line.get('Unnamed: 2')) and not pd.isna(now_line.get('Unnamed: 3')):
                self.data[len(self.data.keys())] = now_line

    def read_half_tabel(self):
        """
        читет файл не полной версии
        :return:
        """
        first_line = self.data_for_read.get(0, "")
        list_keys_first_line = list(first_line.keys())

        try:
            self.name_file = os.path.basename(self.file_path).replace("rprd00067mod ", "").replace('.xls','')
        except:
            self.name_file = os.path.basename(self.file_path)

        for row_num, row in self.data_for_read.items():
            row_return = {
                'Unnamed: 1': row.get(list_keys_first_line[1], ''),
                'Unnamed: 3': row.get(list_keys_first_line[3], ''),
                ' Отчет по наличию программ для станков с ЧПУ': row.get(list_keys_first_line[4], ''),
                'Unnamed: 6': row.get(list_keys_first_line[5], '')
            }
            self.data[len(self.data.keys())] = row_return

    def detection_version_file(self, file_path):
        """
        Определяет к какой версии относится файл.
        :return: 'version half' or 'version complete'
        """
        first_line = self.data_for_read.get(0, "")
        list_keys_first_line = list(first_line.keys())
        if str(list_keys_first_line) == "['Unnamed: 0', 'Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4', ' Отчет по наличию программ для станков с ЧПУ', 'Unnamed: 6', 'Unnamed: 7', 'Unnamed: 8', '2012', 'Unnamed: 10']":
            return 'version complete'
        if int(list_keys_first_line[0]) == 1:
            return 'version half'
        return None


if __name__ == "__main__":
    # app = RprdHandlingScript(r"C:\Users\yakovlev_nd\Desktop\Test\БАМ менеджер\rprd00067mod лтия.464641.003 антенна укв 30-80.xls")
    app = RprdHandlingScript(r"C:\Users\yakovlev_nd\Desktop\Test\БАМ менеджер\rprd00067mod пта 2.xls")
    app.main()
