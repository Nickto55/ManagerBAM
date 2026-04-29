import os.path
import pandas as pd

from scripts.read_excel_file import ReadExcelFile


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
            self.sorting_completed_data()

        return self.sorted_data

    def sorting_completed_data(self):
        """
        Сортрирует данные получанные из полной версии файла
        """
        dse_data_2012 = {}

        for row, l_data in self.data.items():

            rc = l_data.get('Unnamed: 1', '')
            dse = l_data.get('Unnamed: 3', '')
            name_dse = l_data.get(' Отчет по наличию программ для станков с ЧПУ', '')
            yup = l_data.get('Unnamed: 6', '')
            file_name = self.name_file

            rc_data = {
                'rc': rc,
                'dse': dse,
                'name dse': name_dse,
                'yup': yup,
                'file name': file_name
            }

            if not dse in list(dse_data_2012.keys()): dse_data_2012[dse] = {"data_2012": {}}
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

    def detection_version_file(self, file_path):
        """
        Определяет к какой версии относится файл.
        :return: 'version half' or 'version complete'
        """
        first_line = self.data_for_read.get(0, "")
        list_keys_first_line = list(first_line.keys())
        if str(list_keys_first_line) == "['Unnamed: 0', 'Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4', ' Отчет по наличию программ для станков с ЧПУ', 'Unnamed: 6', 'Unnamed: 7', 'Unnamed: 8', '2012', 'Unnamed: 10']":
            print(f"version complete | {os.path.basename(file_path)}")
            return 'version complete'
        else:
            print(f"version half     | {os.path.basename(file_path)}")
            return 'version half'


if __name__ == "__main__":
    app = RprdHandlingScript(
        r"C:\Users\yakovlev_nd\Desktop\Test\БАМ менеджер\rprd00067mod лтия.464641.003 антенна укв 30-80.xls")
    app.main()
