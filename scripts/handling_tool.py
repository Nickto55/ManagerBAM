import os.path

import pandas as pd

from scripts.read_excel_file import ReadExcelFile

class ToolHandlingScript:
    def __init__(self, path_file: str):
        self.path_file = path_file
        self.name_file =  os.path.basename(path_file)
        self.sorted_data_tool = {}

    def main(self):
        read_excel = ReadExcelFile()
        self.data_for_read = read_excel.read_excel_to_dict(self.path_file, str_start=2)
        self.sorting_completed_data()

        return self.sorted_data_tool


    def sorting_completed_data(self):
        dse_data_tool = {}


        for row_n, row in self.data_for_read.items():
            dse =str(row.get('Артикул', ''))
            rc = row.get('ВидРабочегоЦентра', '')
            id_tex =row.get('СБ_ИДТехпроцесса', '')
            type_tex =row.get('Тип техпроцесса','')

            if not type_tex in ["Основной", "не указан"]: continue

            rc_data = {
                'rc': rc,
                'dse': dse,
                'type tex': type_tex,
                'id tex': id_tex
            }
            if not dse in list(dse_data_tool.keys()): dse_data_tool[dse] = {"data_tool": {}}
            dse_data_tool[dse]["data_tool"][f"{rc}_+_{id_tex}_++_{dse}"] = rc_data

        self.sorted_data_tool = dse_data_tool.copy()


if __name__=="__main__":
    app =  ToolHandlingScript(r"C:\Users\yakovlev_nd\Desktop\Test\БАМ менеджер\ЧПУ без инструмента - добавлен тип техпроцесса (15.04.26).xlsx")
    data = app.main()
    for row_m, row in data.items():
        print(row_m)
        for row_n, roerw in row.items():
            print(f"          {row_n}")
            for ropi, iweorp in roerw.items():
                print(f"                  {ropi}|{iweorp}")
    print("---------------------")
    print(data.keys())
    print("---------------------")
    print(data.get('data',''))
