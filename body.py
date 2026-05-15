import sys
import os
import threading
import time
from tkinter import filedialog, END, BooleanVar

import customtkinter as ctk
import pandas as pd
import plyer
import asyncio

from maneger_bam import LogicProgram as LogicManage_programm
from scripts.config_handler import ConfigMainProgram, ConfigHistoryFile


def send_notification(title, message, settime=15):
    plyer.notification.notify(title=title, message=message, app_name="Bam Manager", timeout=settime)


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class AppGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.path_outfile = None
        self.main_config_program = ConfigMainProgram()
        self.config_size = self.main_config_program.get_size_config()


    def main(self):

        self.size_window()



        self.title("Bam Manager")
        self.geometry(f"{self.window_size_x}x{self.window_size_y}")
        try:
            # Используйте resource_path для корректного пути в .exe
            icon_path = resource_path(r"static/ico/bam_manager.ico")
            self.iconbitmap(default=icon_path)
        except Exception as error:
            print(f"Не удалось загрузить иконку: {error}")

        # self.iconwindow(r"static/ico/bam_manager.ico")
        self.config_history = ConfigHistoryFile()

        self.var_view_yup = BooleanVar(value=self.main_config_program.get_all_config_program().get("view yup"))


        self.gui()

    def size_window(self):
        self.window_size_x = int(self.config_size.get('x', ''))
        self.window_size_y = int(self.config_size.get('y', ''))
        self.main_frame_pad_x = 15
        # self.main_frame_pad_y = 15

    def gui(self):
        ctk.set_appearance_mode(self.main_config_program.get_all_config_program().get('theme', ''))

        main_frame = ctk.CTkFrame(
            self,
            width=self.window_size_x - self.main_frame_pad_x * 2,
            height=145,
            fg_color="#3f3f3f"
        )

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
            fg_color="#4a4a4a",
            hover_color="#242424",
            command=lambda: self.button_path_commands("path_2012")
        )
        self.batton_path_2012.place(x=465, y=5)

        self.switch_yup = ctk.CTkSwitch(
            main_frame,
            text="Отображение УП",
            height=30,
            variable=self.var_view_yup,
            button_color=("green", "#565b5e"),
            progress_color=("#4a4a4a", "#242424"),
            button_hover_color=("#ffffff", "#242424"),
            command=self.command_switch_yup
        )
        self.switch_yup.place(x=550, y=5)

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
            fg_color="#4a4a4a",
            hover_color="#242424",
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
            fg_color="#4a4a4a",
            hover_color="#242424",
            command=lambda: self.button_path_commands("path_jp")
        )
        self.batton_path_jp.place(x=465, y=75)

        self.label_path_tool = ctk.CTkEntry(
            main_frame,
            placeholder_text="Ведите полный путь до файла ЧПУ без инструмента",
            width=450,
            height=30,
            fg_color="#242424"
        )
        self.label_path_tool.place(x=5, y=110)
        self.batton_path_tool = ctk.CTkButton(
            main_frame,
            text='Открыть',
            width=30,
            height=30,
            fg_color="#4a4a4a",
            hover_color="#242424",
            command=lambda: self.button_path_commands("path_tool")
        )
        self.batton_path_tool.place(x=465, y=110)

        self.start_button = ctk.CTkButton(
            main_frame,
            text="Начать",
            fg_color="green",
            hover_color="darkgreen",
            command=self.run_manager_thread
        )
        self.start_button.place(x=self.window_size_x - self.main_frame_pad_x * 2 - 140 - 5, y=110)

        main_frame.place(x=15, y=15)

        self.status_text = ctk.CTkTextbox(self, width=self.window_size_x - self.main_frame_pad_x * 2, height=211,
                                          fg_color="#131414")
        self.status_text.place(x=15, y=174)

        if self.config_history.get_2012_hist() != "":
            self.label_path_2012.delete(0, END)
            self.label_path_2012.insert(0, self.config_history.get_2012_hist())

            self.log("-сохранённый путь к 2012 успешо загружен", color_log="#0ccc00")
        else:
            self.log("-нет сохраненного пути к 2012", color_log="#ffa645")
        if self.config_history.get_cz_hist() != "":
            self.label_path_cz.delete(0, END)
            self.label_path_cz.insert(0, self.config_history.get_cz_hist())

            self.log("-сохранённый путь к СЗ успешо загружен", color_log="#0ccc00")
        else:
            self.log("-нет сохраненного пути к СЗ", color_log="#ffa645")
        if self.config_history.get_jp_hist() != "":
            self.label_path_jp.delete(0, END)
            self.label_path_jp.insert(0, self.config_history.get_jp_hist())

            self.log("-сохранённый путь к Журналу Проблем успешо загружен", color_log="#0ccc00")
        else:
            self.log("-нет сохраненного пути к Журналу Проблем", color_log="#ffa645")
        if self.config_history.get_tool_hist() != "":
            self.label_path_tool.delete(0, END)
            self.label_path_tool.insert(0, self.config_history.get_tool_hist())

            self.log("-сохранённый путь к ЧПУ без инструмента успешо загружен", color_log="#0ccc00")
        else:
            self.log("-нет сохраненного пути к ЧПУ без инструмента", color_log="#ffa645")

        self.batton_oprn_result_tabl = ctk.CTkButton(
            main_frame,
            text="Открыть результат",
            command=self.command_batton_open_result,
            fg_color='#b69765',
            hover_color='#8f764f'
        )

    def merge_color(self):
        self.batton_oprn_result_tabl.configure(fg_color='#8f764f', hover_color='#5c4b32')
    def command_batton_open_result(self):
        if not self.path_outfile is None:
            self.start_button.configure(state="disabled")
            self.batton_oprn_result_tabl.configure(fg_color='green', hover_color='darkgreen')

            self.batton_oprn_result_tabl.after(1000, self.merge_color)


            try:

                os.startfile(self.path_outfile)
                self.log("-Файл открыт", color_log="#788084")
            except Exception as e:
                self.log(f"Ошибка при открытии файла: {e}", color_log="red")
                self.start_button.configure(state="normal")
                return

            try:
                send_notification(f"Файл открыт: {os.path.basename(self.path_outfile).replace('.xlsx','')}","ヾ(￣▽￣) ",  16)
            except:
                send_notification(f"Файл открыт: {os.path.basename(self.path_outfile)}","ヾ(￣▽￣) ",  16)
            self.batton_oprn_result_tabl.after(5000, self.start_button.configure(state="normal"))
        else:
            self.log("Ошибка при открытии файла, отсссуствует путь", color_log="red")
            self.batton_oprn_result_tabl.place_forget()



    def command_switch_yup(self):
        if self.var_view_yup.get():
            self.log(f"-Файлы с уп, отображены", color_log="#788084")
        else:
            self.log(f"-Файлы с уп, скрыты", color_log="#788084")
        self.main_config_program.set_config_progrm('view yup', self.var_view_yup.get())

    def log(self, message, color_log=None):
        """Вывод логов в текстовое поле GUI с цветом"""
        self.status_text.insert("end", f"{message}\n")

        if color_log:
            # Получаем позицию только что вставленной строки
            end_index = self.status_text.index("end-1c")  # конец текста без \n
            line_num = end_index.split('.')[0]
            start_pos = f"{int(line_num) - 1}.0"  # начало вставленной строки
            end_pos = f"{int(line_num) - 1}.end"  # конец строки

            # Создаём/настраиваем тег и применяем
            tag_name = f"color_{color_log}"
            self.status_text.tag_config(tag_name, foreground=color_log)
            self.status_text.tag_add(tag_name, start_pos, end_pos)

        self.status_text.see("end")

    def run_manager_thread(self):
        """Запуск в отдельном потоке, чтобы GUI не зависал"""
        self.batton_oprn_result_tabl.place_forget()
        self.start_button.configure(state="disabled")
        self.log("Запуск программы...")
        if pd.isna(
                self.label_path_2012.get()) or self.label_path_2012.get() is None or self.label_path_2012.get() == '':
            self.log("Ошибка, укажите файл 2012", color_log="red")
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

            self.config_history.set_history("2012", self.label_path_2012.get())
        if label_batton == 'path_cz':
            str_path = self.open_file_to_path()
            self.label_path_cz.delete(0, END)
            self.label_path_cz.insert(0, str_path)

            self.config_history.set_history("cz", self.label_path_cz.get())
        if label_batton == 'path_jp':
            str_path = self.open_file_to_path()
            self.label_path_jp.delete(0, END)
            self.label_path_jp.insert(0, str_path)

            self.config_history.set_history("jp", self.label_path_jp.get())
        if label_batton == 'path_tool':
            str_path = self.open_file_to_path()
            self.label_path_tool.delete(0, END)
            self.label_path_tool.insert(0, str_path)

            self.config_history.set_history("tool", self.label_path_tool.get())

    def execute_logic(self):
        self.path_outfile = None
        try:
            self.config_history.set_history("2012", self.label_path_2012.get())
            self.config_history.set_history("cz", self.label_path_cz.get())
            self.config_history.set_history("jp", self.label_path_jp.get())
            self.config_history.set_history("tool", self.label_path_tool.get())
        except Exception as er:
            self.log(f"Ошибка при сохранении", color_log="red")
            self.log(f"ERROR: {str(er)}", color_log="red")

        try:
            manager = LogicManage_programm(
                list_path_to_file_rprd=self.label_path_2012.get().replace(", ", ",").split(","),
                need_yup=self.var_view_yup.get(),
                path_to_file_cz=self.label_path_cz.get(),
                path_to_file_jp=self.label_path_jp.get(),
                path_to_file_tool=self.label_path_tool.get()
            )

            if hasattr(manager, 'main'):
                self.path_outfile = manager.main()
            self.batton_oprn_result_tabl.place(x=self.window_size_x - self.main_frame_pad_x * 2 - 140 - 5, y=110 - 30 - 5)

            self.log("Complete!", color_log="green")
            self.log("Процесс успешно завершен.", color_log="green")
            send_notification("Программа завершена", "Программа завершена, проверте файл", 16)
            self.start_button.configure(state="normal")
        except Exception as e:
            self.log(f"ERROR: {str(e)}", color_log="red")
        finally:
            self.start_button.configure(state="normal")


if __name__ == "__main__":
    app = AppGUI()
    app.main()
    app.mainloop()
