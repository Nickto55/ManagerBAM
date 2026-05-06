import customtkinter as ctk
import threading
import sys
import os

from maneger_bam import LogicProgram as LogicManage_programm

class AppGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Manager BAM")
        self.geometry("700x400")
        self.gui()



    def gui(self):
        ctk.set_appearance_mode("dark")

        main_frame = ctk.CTkFrame(self,width=670,height=145,fg_color="#3f3f3f")

        self.label_path_2012 = ctk.CTkEntry(
            main_frame,
            placeholder_text="Ведите полный путь до файла 2012",
            width=450,
            height=30,
            fg_color="#242424"

        )
        self.label_path_2012.place(x=5,y=5)
        label_sun = ctk.CTkLabel(
            main_frame,
            text_color="red",
            text="*"
        )
        label_sun.place(x=456,y=0)
        self.label_path_cz = ctk.CTkEntry(
            main_frame,
            placeholder_text="Ведите полный путь до файла Сз",
            width=450,
            height=30,
            fg_color="#242424"
        )
        self.label_path_cz.place(x=5,y=40)
        self.label_path_jp = ctk.CTkEntry(
            main_frame,
            placeholder_text="Ведите полный путь до файла Журнала проблем",
            width=450,
            height=30,
            fg_color="#242424"
        )
        self.label_path_jp.place(x=5, y=75)


        self.start_button = ctk.CTkButton(
            main_frame,
            text="Начать",
            fg_color="green",
            hover_color="darkgreen",
            command=self.run_manager_thread
        )
        self.start_button.place(x=670-140-5,y=110)

        main_frame.place(x=15,y=15)

        self.status_text = ctk.CTkTextbox(self, width=670, height=211,fg_color="#131414")
        self.status_text.place(x=15,y=174)
        self.status_text.insert("0.0", "Введите данные...\n")

    def log(self, message):
        """Вывод логов в текстовое поле GUI"""
        self.status_text.insert("end", f"> {message}\n")
        self.status_text.see("end")

    def run_manager_thread(self):
        """Запуск в отдельном потоке, чтобы GUI не зависал"""
        self.start_button.configure(state="disabled")
        self.log("Запуск основного класса...")
        
        thread = threading.Thread(target=self.execute_logic, daemon=True)
        thread.start()

    def execute_logic(self):
        try:
            manager = LogicManage_programm(
                list_path_to_file_rprd=[self.label_path_2012.get()],
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