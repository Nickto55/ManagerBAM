import os.path

import pandas as pd

from scripts.read_excel_file import ReadExcelFile


class CzHandlingScript:
    def __init__(self, path_file: str):
        self.path_file = path_file
        self.name_file = os.path.basename(path_file)
        self.sorted_data_cz = {}

    def main(self):
        read_excel = ReadExcelFile()
        self.data_for_read = read_excel.read_excel_to_dict(self.path_file)
        self.sorting_completed_data()

        return self.sorted_data_cz

    def sorting_completed_data(self):
        dse_data_cz = {}

        for row_n, row in self.data_for_read.items():
            rc = [str(row.get('РЦ', ''))]
            dse = row.get('ДСЕ', '')
            date_latter = row.get('Дата пиьсма', '')
            info_from_latter = row.get('Инф из письма', '')
            signed = row.get('Подписано', '')
            coment = row.get('Комментарии', '')

            if "," in str(rc[0]):
                rc = rc[0].replace(' ', '').split(",")
            if pd.isna(coment): coment = ''
            if pd.isna(info_from_latter): info_from_latter = ''
            if pd.isna(signed): signed = ''

            if not pd.isna(row.get('Выполнено', '')) or not pd.isna(row.get('Закрыто', '')): continue

            for rc_cell in rc:
                rc_data = {
                    'rc': rc_cell,
                    'date latter': str(date_latter)[:10],
                    'info from latter': info_from_latter,
                    'signed': str(signed),
                    'coment': str(coment)
                }
                if not dse in list(dse_data_cz.keys()): dse_data_cz[dse] = {"data_cz": {}}
                dse_data_cz[dse]["data_cz"][rc_cell] = rc_data

        self.sorted_data_cz = dse_data_cz.copy()


if __name__ == "__main__":
    app = CzHandlingScript(r"C:\Users\yakovlev_nd\Desktop\Test\БАМ менеджер\ДСЕ по СЗ и Извещениям.xlsx")
    app.main()
