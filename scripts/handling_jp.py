import os.path

from scripts.read_excel_file import ReadExcelFile

class JpHandlingScript:
    def __init__(self, path_file: str):
        self.path_file = path_file
        self.name_file =  os.path.basename(path_file)
        self.sorted_data_jp = {}

    def main(self):
        read_excel = ReadExcelFile()
        self.data_for_read = read_excel.read_excel_to_dict(self.path_file)
        self.sorting_completed_data()

        return self.sorted_data_jp


    def sorting_completed_data(self):
        dse_data_jp = {}

        for row_n, row in self.data_for_read.items():
            numpe_jp = row.get('Unnamed: 0', '')
            dse =str(row.get('Unnamed: 3', ''))
            data_create =row.get('Проблемы и задачи УП и технологии', '')
            data_close =row.get('Unnamed: 23', '')

            rc_data = {
                'numpe jp': numpe_jp,
                'dse': dse,
                'data create': data_create,
                'data close': data_close
            }
            if not dse in list(dse_data_jp.keys()): dse_data_jp[dse] = {"data_jp": {}}
            dse_data_jp[dse]["data_jp"][numpe_jp] = rc_data

        self.sorted_data_jp = dse_data_jp.copy()


if __name__=="__main__":
    app =  JpHandlingScript(r"C:\Users\yakovlev_nd\Desktop\Test\БАМ менеджер\Проблемы и задачи УП и технологии.xlsx")
    for row_m, row in app.main().items():
        print(row_m)
        for row_n, roerw in row.items():
            print(f"          {row_n}")
            for ropi, iweorp in roerw.items():
                print(f"                  {ropi}|{iweorp}")
