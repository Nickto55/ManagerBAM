from scripts.handling_cz import CzHandlingScript
from scripts.handling_jp import JpHandlingScript
from scripts.handling_rprd import RprdHandlingScript


class LogicProgram:
    def __init__(self, list_path_to_file_rprd: list, path_to_file_cz: str = None, path_to_file_jp: str = None):
        self.list_path_file = list_path_to_file_rprd
        self.path_to_file_cz = path_to_file_cz
        self.path_to_file_jp = path_to_file_jp
        if not self.path_to_file_cz is None:
            cz_handling = CzHandlingScript(self.path_to_file_cz)
            self.data_cz = cz_handling.main()
            self.list_keys_data_cz = list(self.data_cz.keys())
        if not self.path_to_file_jp is None:
            jp_handling = JpHandlingScript(self.path_to_file_jp)
            self.data_jp = jp_handling.main()
            self.list_keys_data_jp = list(self.data_jp.keys())

    def main(self):
        for file_path in self.list_path_file:
            rprd_handling = RprdHandlingScript(file_path)
            rprd_data = rprd_handling.main()

            if not self.path_to_file_cz is None:
                for num_row_dse, row in rprd_data.items():
                    if num_row_dse in self.list_keys_data_cz:
                        for key_cz in list(self.data_cz[num_row_dse].keys()):
                            rprd_data[num_row_dse][key_cz] = self.data_cz[num_row_dse].get(key_cz, "")
            if not self.path_to_file_jp is None:
                for num_row_dse, row in rprd_data.items():
                    if num_row_dse in self.list_keys_data_jp:
                        for key_jp in list(self.data_jp[num_row_dse].keys()):
                            rprd_data[num_row_dse][key_jp] = self.data_jp[num_row_dse].get(key_jp, "")
                            print(num_row_dse)

            for row_num_dse, row_dse in rprd_data.items():
                print(row_num_dse)
                for row_num_file, row_file in row_dse.items():
                    print("         ", row_num_file)
                    for row_num_rc, row_rc in row_file.items():
                        print("             ", row_num_rc, row_rc)


if __name__ == "__main__":
    app = LogicProgram(
        [r"C:\Users\yakovlev_nd\Desktop\Test\БАМ менеджер\rprd00067mod лтия.464641.003 антенна укв 30-80.xls",
         r"C:\Users\yakovlev_nd\Desktop\Test\БАМ менеджер\rprd00067mod пта.xls"],
        path_to_file_cz=r"C:\Users\yakovlev_nd\Desktop\Test\БАМ менеджер\ДСЕ по СЗ и Извещениям.xlsx",
        path_to_file_jp=r"C:\Users\yakovlev_nd\Desktop\Test\БАМ менеджер\Проблемы и задачи УП и технологии.xlsx")
    app.main()
    # app = LogicProgram([r"C:\Users\yakovlev_nd\Desktop\Test\БАМ менеджер\rprd00067mod пта.xls"])
    # app.main()
    # app = LogicProgram([r"C:\Users\yakovlev_nd\Desktop\Test\БАМ менеджер\rprd00067mod пта 2.xls"])
    # app.main()
