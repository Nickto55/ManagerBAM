import os.path

from scripts.handling_cz import CzHandlingScript
from scripts.handling_jp import JpHandlingScript
from scripts.handling_rprd import RprdHandlingScript
from scripts.write_excel_file import ExcelSaver
from scripts.filter_data import FiltretedData
from CTkMessagebox import CTkMessagebox


class LogicProgram:
    def __init__(self, list_path_to_file_rprd: list, path_to_file_cz: str = None, path_to_file_jp: str = None):
        """
        Основная логика программы
        :param list_path_to_file_rprd: Список полных ссылок, файлов 2012
        :param path_to_file_cz: Полный путь до файла сз
        :param path_to_file_jp: Полный путь до файла журнала проблем
        """
        print([list_path_to_file_rprd,path_to_file_cz,path_to_file_jp])
        self.list_path_file = list_path_to_file_rprd
        self.path_to_file_cz = path_to_file_cz
        self.path_to_file_jp = path_to_file_jp

        if not self.path_to_file_cz is None and not self.path_to_file_cz == "":
            cz_handling = CzHandlingScript(self.path_to_file_cz)
            self.data_cz = cz_handling.main()
            self.list_keys_data_cz = list(self.data_cz.keys())
        if not self.path_to_file_jp is None and not self.path_to_file_jp == "":
            jp_handling = JpHandlingScript(self.path_to_file_jp)
            self.data_jp = jp_handling.main()
            self.list_keys_data_jp = list(self.data_jp.keys())

    def main(self):
        save_excel = ExcelSaver('result_data.xlsx')

        for file_path in self.list_path_file:
            rprd_handling = RprdHandlingScript(file_path)
            rprd_data = rprd_handling.main()


            if not self.path_to_file_cz is None and not self.path_to_file_cz == "":
                for num_row_dse, row in rprd_data.items():
                    if num_row_dse in self.list_keys_data_cz:
                        for key_cz in list(self.data_cz[num_row_dse].keys()):
                            rprd_data[num_row_dse][key_cz] = self.data_cz[num_row_dse].get(key_cz, "")
            if not self.path_to_file_jp is None and not self.path_to_file_jp == "":
                for num_row_dse, row in rprd_data.items():
                    if num_row_dse in self.list_keys_data_jp:
                        for key_jp in list(self.data_jp[num_row_dse].keys()):
                            rprd_data[num_row_dse][key_jp] = self.data_jp[num_row_dse].get(key_jp, "")


            flter = FiltretedData(rprd_data)
            main_data = flter.main()
            bas_name_file = f"{os.path.basename(file_path)}"[f"{os.path.basename(file_path)}".index("rprd00067mod ")+13:]
            if len(bas_name_file)>30:
                sheet_n = bas_name_file[-30:]
                sheet_n = sheet_n[sheet_n.index(" "):]
            else:
                sheet_n = bas_name_file

            path = save_excel.save(main_data, sheet_name=sheet_n)
            print(f" Файл сохранен: {path}")
            print(f'Всего записей:{len(list(main_data.keys()))}')




if __name__ == "__main__":
    app = LogicProgram(
        [r"C:\Users\yakovlev_nd\Desktop\Test\БАМ менеджер\rprd00067mod лтия.464641.003 антенна укв 30-80.xls",r"C:\Users\yakovlev_nd\Desktop\Test\БАМ менеджер\rprd00067mod пта 2.xls"],
        path_to_file_cz=r"C:\Users\yakovlev_nd\Desktop\Test\БАМ менеджер\ДСЕ по СЗ и Извещениям.xlsx",
        path_to_file_jp=r"C:\Users\yakovlev_nd\Desktop\Test\БАМ менеджер\Проблемы и задачи УП и технологии.xlsx"
    )
    app.main()
    # app = LogicProgram([r"C:\Users\yakovlev_nd\Desktop\Test\БАМ менеджер\rprd00067mod пта.xls"])
    # app.main()
    # app = LogicProgram([r"C:\Users\yakovlev_nd\Desktop\Test\БАМ менеджер\rprd00067mod пта 2.xls"])
    # app.main()
