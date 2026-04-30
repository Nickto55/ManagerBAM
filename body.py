import customtkinter as ctk
import threading
import sys
import os

# Импортируем твой класс из соседнего файла
# Если главный класс называется иначе, замени ManagerBAM на свое название
try:
    from manager_bam import ManagerBAM 
except ImportError:
    print("Файл manager_bam.py не найден в текущей директории.")

class AppGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ManagerBAM Control Panel")
        self.geometry("500x400")
        ctk.set_appearance_mode("dark")

        # Настройка интерфейса
        self.label = ctk.CTkLabel(self, text="Управление ManagerBAM", font=("Arial", 20, "bold"))
        self.label.pack(pady=20)

        self.status_text = ctk.CTkTextbox(self, width=400, height=200)
        self.status_text.pack(pady=10)
        self.status_text.insert("0.0", "Готов к запуску...\n")

        self.start_button = ctk.CTkButton(
            self, 
            text="ЗАПУСТИТЬ MANAGER", 
            fg_color="green", 
            hover_color="darkgreen",
            command=self.run_manager_thread
        )
        self.start_button.pack(pady=20)

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
            # Создаем экземпляр твоего класса
            # Если конструктор требует аргументы, передай их здесь
            manager = ManagerBAM()
            
            # Вызываем главный метод (например, run() или start())
            # Замени .run(), если метод называется по-другому
            if hasattr(manager, 'run'):
                manager.run()
            
            self.log("Процесс успешно завершен.")
        except Exception as e:
            self.log(f"ОШИБКА: {str(e)}")
        finally:
            self.start_button.configure(state="normal")

if __name__ == "__main__":
    app = AppGUI()
    app.mainloop()