import threading
from tkinter import filedialog, END

import customtkinter as ctk
import pandas as pd

from maneger_bam import LogicProgram as LogicManage_programm
from scripts.config_handler import ConfigMainProgram,ConfigHistoryFile


class AppGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.main_config_program = ConfigMainProgram()
        self.config_size = self.main_config_program.get_size_config()

        self.title("Bam Manager")
        self.geometry(f"{self.config_size.get('x','')}x{self.config_size.get('y','')}")
        try:
            self.iconbitmap(r"static/ico/bam_manager.ico")
        except:
            pass
        # self.iconwindow(r"static/ico/bam_manager.ico")
        self.config_history = ConfigHistoryFile()
        self.gui()

    def gui(self):
        ctk.set_appearance_mode(self.main_config_program.get_all_config_program().get('theme',''))
        # ctk.set_appearance_mode('light')

        main_frame = ctk.CTkFrame(self, width=int(self.config_size.get('x',''))-30, height=145, fg_color="#3f3f3f")

        self.label_path_2012 = ctk.CTkEntry(
            main_frame,
            placeholder_text="Ведите полный путь до файла 2012",
            width=450,
            height=30,
            fg_color="#242424"

        )
        self.label_path_2012.place(x=5, y=5)
        label_sun = ctk.CTkLabel(
            main_frame,
            text_color="red",
            text="*"
        )

        self.batton_path_2012 = ctk.CTkButton(
            main_frame,
            text='Открыть',
            width=30,
            height=30,
            command=lambda: self.button_path_commands("path_2012")
        )
        self.batton_path_2012.place(x=465, y=5)

        label_sun.place(x=456, y=0)
        self.label_path_cz = ctk.CTkEntry(
            main_frame,
            placeholder_text="Ведите полный путь до файла Сз",
            width=450,
            height=30,
            fg_color="#242424"
        )
        self.label_path_cz.place(x=5, y=40)
        self.batton_path_cz = ctk.CTkButton(
            main_frame,
            text='Открыть',
            width=30,
            height=30,
            command=lambda: self.button_path_commands("path_cz")
        )
        self.batton_path_cz.place(x=465, y=40)


        self.label_path_jp = ctk.CTkEntry(
            main_frame,
            placeholder_text="Ведите полный путь до файла Журнала проблем",
            width=450,
            height=30,
            fg_color="#242424"
        )
        self.label_path_jp.place(x=5, y=75)
        self.batton_path_jp = ctk.CTkButton(
            main_frame,
            text='Открыть',
            width=30,
            height=30,
            command=lambda: self.button_path_commands("path_jp")
        )
        self.batton_path_jp.place(x=465, y=75)

        self.start_button = ctk.CTkButton(
            main_frame,
            text="Начать",
            fg_color="green",
            hover_color="darkgreen",
            command=self.run_manager_thread
        )
        self.start_button.place(x=670 - 140 - 5, y=110)

        main_frame.place(x=15, y=15)

        self.status_text = ctk.CTkTextbox(self, width=670, height=211, fg_color="#131414")
        self.status_text.place(x=15, y=174)

        if self.config_history.get_cz_hist() != "":
            self.label_path_cz.delete(0,END)
            self.label_path_cz.insert(0, self.config_history.get_cz_hist())
        else:
            self.log("--нет сохраненного пути к cz")
        if self.config_history.get_jp_hist() != "":
            self.label_path_jp.delete(0,END)
            self.label_path_jp.insert(0, self.config_history.get_jp_hist())
        else:
            self.log("--нет сохраненного пути к jp")

    def log(self, message):
        """Вывод логов в текстовое поле GUI"""
        self.status_text.insert("end", f"{message}\n")
        self.status_text.see("end")

    def run_manager_thread(self):
        """Запуск в отдельном потоке, чтобы GUI не зависал"""

        self.start_button.configure(state="disabled")
        self.log("Запуск программы...")
        if pd.isna(
                self.label_path_2012.get()) or self.label_path_2012.get() is None or self.label_path_2012.get() == '':
            self.log("Ошибка, укажите файл 2012")
            self.start_button.configure(state="normal")
            return

        thread = threading.Thread(target=self.execute_logic, daemon=True)
        thread.start()

    def open_fils_to_path(self):
        filepaths = filedialog.askopenfilenames(
            title="Выберите Excel файлы",
            filetypes=(("Excel files", "*.xlsx *.xls *.xlsm"), ("All files", "*.*"))
        )
        if not filepaths:
            return
        return filepaths

    def open_file_to_path(self):
        filepaths = filedialog.askopenfilename(
            title="Выберите Excel файлы",
            filetypes=(("Excel files", "*.xlsx *.xls *.xlsm"), ("All files"))
        )
        if not filepaths:
            return
        return filepaths

    def button_path_commands(self, label_batton: str):
        if label_batton == 'path_2012':
            path_list_filr = list(self.open_fils_to_path())

            str_paths = ""
            for path in path_list_filr: str_paths += f"{path}, "
            str_paths = str_paths[:-2]

            self.label_path_2012.delete(0, END)
            self.label_path_2012.insert(0, str_paths)
            self.log(f"Установлен путь для файла 2012")
        if label_batton == 'path_cz':
            str_path = self.open_file_to_path()
            self.label_path_cz.delete(0, END)
            self.label_path_cz.insert(0, str_path)
        if label_batton == 'path_jp':
            str_path = self.open_file_to_path()
            self.label_path_jp.delete(0, END)
            self.label_path_jp.insert(0, str_path)

    def execute_logic(self):
        try:
            self.config_history.set_history("cz",self.label_path_cz.get())
            self.config_history.set_history("jp",self.label_path_jp.get())


            manager = LogicManage_programm(
                list_path_to_file_rprd=self.label_path_2012.get().replace(", ", ",").split(","),
                path_to_file_cz=self.label_path_cz.get(),
                path_to_file_jp=self.label_path_jp.get()
            )

            if hasattr(manager, 'main'):
                manager.main()

            self.log("Процесс успешно завершен.")
        except Exception as e:
            self.log(f"ОШИБКА: {str(e)}")
        finally:
            self.start_button.configure(state="normal")


if __name__ == "__main__":
    app = AppGUI()
    app.mainloop()
