import json
import os
import tkinter as tk
from tkinter import messagebox, filedialog

from static.config import configProgram


class HandlerConfig:
    def __init__(self):
        """
        Обработчик базы данных
        """
        self.CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".BamManagerWork")
        self.file_path = os.path.join(self.CONFIG_DIR, "config.json")
        self.data = configProgram

        self._ensure_file_exists()
        self.load()

    def save(self):
        """Сохраняет текущие данные в файл."""
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)
        self.load()

    def _ensure_file_exists(self):
        """Создаёт файл и структуру данных, если их нет."""
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)

    def load(self):
        """Загружает данные из файла."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) :
            print("Config файл пуст")

    def recoveryLoseKeyAndValue(self, dictionary: str, key_for_dictionary: str, value_for_key: str):
        print("Recovery:", dictionary, key_for_dictionary, value_for_key)


        if dictionary not in self.data:
            self.data[dictionary] = {}

        self.data[dictionary][key_for_dictionary] = value_for_key
        self.save()

