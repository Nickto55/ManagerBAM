import pandas as pd
import os

class ReadExcelFile:
    def __init__(self) -> None:
        pass

    def read_excel_to_dict(self,full_path_to_file,str_start = 0):
        self.path_file = full_path_to_file
        if not os.path.exists(self.path_file): return "no path to file"
        try:
            df = pd.read_excel(self.path_file,header=str_start)
            data_return =  df.to_dict(orient='index')
            return data_return
        except Exception as error:
            print(error)
            return error

if __name__ == "__main__":
    app = ReadExcelFile()
    print(app.read_excel_to_dict(r"C:\Users\yakovlev_nd\Desktop\Test\БАМ менеджер\rprd00067mod лтия.464641.003 антенна укв 30-80.xls"))