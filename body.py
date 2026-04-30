import customtkinter as ctk
import os

class ManagerBAM_GUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ManagerBAM - Signature Tool")
        self.geometry("400x300")

        # Настройка сетки
        self.grid_columnconfigure(0, weight=1)
        
        # Заголовок
        self.label = ctk.CTkLabel(self, text="Введите данные для записи в body:", font=("Arial", 16))
        self.label.grid(row=0, column=0, padx=20, pady=20)

        # Поле ввода
        self.entry = ctk.CTkEntry(self, placeholder_text="Ваша подпись или текст...", width=300)
        self.entry.grid(row=1, column=0, padx=20, pady=10)

        # Кнопка записи
        self.button = ctk.CTkButton(self, text="Записать в файл", command=self.write_to_body)
        self.button.grid(row=2, column=0, padx=20, pady=20)

        # Статус
        self.status_label = ctk.CTkLabel(self, text="", text_color="gray")
        self.status_label.grid(row=3, column=0, padx=20, pady=10)

    def write_to_body(self):
        content = self.entry.get()
        if not content:
            self.status_label.configure(text="Ошибка: Поле пустое!", text_color="red")
            return

        try:
            # Путь к файлу body в корне проекта
            file_path = "body"
            
            with open(file_path, "a", encoding="utf-8") as f:
                f.write(content + "\n")
            
            self.status_label.configure(text="Успешно записано в body", text_color="green")
            self.entry.delete(0, 'end') # Очистить поле после записи
        except Exception as e:
            self.status_label.configure(text=f"Ошибка: {e}", text_color="red")

if __name__ == "__main__":
    app = ManagerBAM_GUI()
    app.mainloop()