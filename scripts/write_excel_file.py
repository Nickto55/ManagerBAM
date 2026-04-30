
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import os

class ExcelSaver:
    """
    Класс для сохранения кода и входных данных в Excel файл.
    
    Входные данные: словарь словарей вида:
    {
        'test_name_1': {
            'code': 'def hello():\n    return "world"',
            'input': 'hello()',
            'expected': '"world"',
            'notes': 'простой пример'
        },
        'test_name_2': {
            'code': '...',
            'input': '...',
            ...
        }
    }
    """
    
    def __init__(self, filename="result_data.xlsx"):
        self.filename = filename
        self.workbook = None
        self.sheet = None
        
        # Стили
        self.header_font = Font(bold=True, color="FFFFFF", size=11)
        self.header_fill = PatternFill(start_color="2C3E50", end_color="2C3E50", fill_type="solid")
        self.code_font = Font(name="Consolas", size=10)
        self.code_fill = PatternFill(start_color="F8F9FA", end_color="F8F9FA", fill_type="solid")
        self.border = Border(
            left=Side(style='thin', color='D0D0D0'),
            right=Side(style='thin', color='D0D0D0'),
            top=Side(style='thin', color='D0D0D0'),
            bottom=Side(style='thin', color='D0D0D0')
        )
        self.wrap_alignment = Alignment(wrap_text=True, vertical="top")
        
    def _create_workbook(self):
        """Создает новую книгу Excel."""
        self.workbook = openpyxl.Workbook()
        self.sheet = self.workbook.active
        self.sheet.title = "Code & Data"
        
    def _auto_resize_columns(self):
        """Автоматически подбирает ширину столбцов."""
        for column in self.sheet.columns:
            max_length = 0
            column_letter = get_column_letter(column[0].column)
            for cell in column:
                try:
                    if cell.value:
                        max_length = max(max_length, len(str(cell.value)))
                except:
                    pass
            adjusted_width = min(max_length + 4, 80)
            self.sheet.column_dimensions[column_letter].width = adjusted_width
            
    def _auto_resize_rows(self):
        """Автоматически подбирает высоту строк для многострочного текста."""
        for row in self.sheet.iter_rows(min_row=2):
            max_lines = 1
            for cell in row:
                if cell.value and isinstance(cell.value, str):
                    lines = cell.value.count('\n') + 1
                    max_lines = max(max_lines, lines)
            self.sheet.row_dimensions[row[0].row].height = max(30, max_lines * 15)
    
    def save(self, data_dict, sheet_name=None):
        """
        Сохраняет данные в Excel файл.
        
        Args:
            data_dict: словарь словарей с данными
            sheet_name: имя листа (опционально)
        
        Returns:
            str: путь к сохраненному файлу
        """
        if not data_dict:
            raise ValueError("Передан пустой словарь данных")
            
        self._create_workbook()
        
        if sheet_name:
            self.sheet.title = sheet_name
            
        # Получаем все уникальные ключи из внутренних словарей для заголовков
        headers = ["Дсе","Уп","Имя изделия","Наименование","Рц","Рц из Сз","Дата из письма","Инф из письма","Подписано","№Жп","Дсе ЖП", "Дата создания", "Датат закрытия"]
        
        # Добавляем колонку с именем теста/функции
        headers = headers
        
        # Записываем заголовки
        for col_idx, header in enumerate(headers, 1):
            cell = self.sheet.cell(1, col_idx, header)
            cell.font = self.header_font
            cell.fill = self.header_fill
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.border = self.border
            
        # Записываем данные
        row_idx = 2
        for name, inner_dict in data_dict.items():
            for col_idx, header in enumerate(headers, 1):
                if header == "Дсе":
                    value = name[:name.index("_+_")]
                    # value = name
                else:
                    value = inner_dict.get(header, '')
                    
                cell = self.sheet.cell(row_idx, col_idx, value)
                cell.border = self.border
                cell.alignment = self.wrap_alignment
                
                # Применяем моноширинный шрифт для кода
                if header in ['code', 'input', 'output', 'expected']:
                    cell.font = self.code_font
                    cell.fill = self.code_fill
                    
            row_idx += 1
            
        # Авторазмер колонок и строк
        self._auto_resize_columns()
        self._auto_resize_rows()
        
        # Замораживаем заголовок
        self.sheet.freeze_panes = 'A2'
        
        # Сохраняем
        output_path = f"{os.getcwd()}/{self.filename}"
        self.workbook.save(output_path)
        return output_path
    
    def append(self, data_dict):
        """
        Дописывает данные в существующий файл (если он есть).
        """
        output_path = f"{os.getcwd()}/{self.filename}"
        
        if os.path.exists(output_path):
            self.workbook = openpyxl.load_workbook(output_path)
            self.sheet = self.workbook.active
            start_row = self.sheet.max_row + 1
        else:
            self._create_workbook()
            start_row = 2
            
            # Заголовки
            headers = set()
            for inner_dict in data_dict.values():
                headers.update(inner_dict.keys())
            headers = ["Дсе"] + sorted(list(headers))
            
            for col_idx, header in enumerate(headers, 1):
                cell = self.sheet.cell(1, col_idx, header)
                cell.font = self.header_font
                cell.fill = self.header_fill
                cell.alignment = Alignment(horizontal="center", vertical="center")
                cell.border = self.border

        current_headers = [cell.value for cell in self.sheet[1]]

        for name, inner_dict in data_dict.items():
            for col_idx, header in enumerate(current_headers, 1):
                if header == "Дсе":
                    value = name
                else:
                    value = inner_dict.get(header, '')
                    
                cell = self.sheet.cell(start_row, col_idx, value)
                cell.border = self.border
                cell.alignment = self.wrap_alignment
                
                if header in ['code', 'input', 'output', 'expected']:
                    cell.font = self.code_font
                    cell.fill = self.code_fill
                    
            start_row += 1
            
        self._auto_resize_columns()
        self._auto_resize_rows()
        
        self.workbook.save(output_path)
        return output_path



if __name__ == "__main__":
    test_data = {
        'fibonacci': {
            'code': 'def fib(n):\n    if n <= 1:\n        return n\n    return fib(n-1) + fib(n-2)',
            'input': 'fib(10)',
            'output': '55',
            'complexity': 'O(2^n)',
            'tags': 'recursion, math'
        },
        'bubble_sort': {
            'code': 'def bubble_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        for j in range(0, n-i-1):\n            if arr[j] > arr[j+1]:\n                arr[j], arr[j+1] = arr[j+1], arr[j]\n    return arr',
            'input': '[64, 34, 25, 12, 22, 11, 90]',
            'output': '[11, 12, 22, 25, 34, 64, 90]',
            'complexity': 'O(n²)',
            'tags': 'sorting, beginner'
        },
        'quick_sort': {
            'code': 'def quick_sort(arr):\n    if len(arr) <= 1:\n        return arr\n    pivot = arr[len(arr)//2]\n    left = [x for x in arr if x < pivot]\n    middle = [x for x in arr if x == pivot]\n    right = [x for x in arr if x > pivot]\n    return quick_sort(left) + middle + quick_sort(right)',
            'input': '[3, 6, 8, 10, 1, 2, 1]',
            'output': '[1, 1, 2, 3, 6, 8, 10]',
            'complexity': 'O(n log n)',
            'tags': 'sorting, divide-and-conquer'
        }
    }
    
    # Создаем экземпляр и сохраняем
    saver = ExcelSaver("algorithms.xlsx")
    path = saver.save(test_data, sheet_name="Algorithms")
    print(f" Файл сохранен: {path}")
    
    # Демонстрация append
    new_data = {
        'merge_sort': {
            'code': 'def merge_sort(arr):\n    if len(arr) <= 1:\n        return arr\n    mid = len(arr)//2\n    left = merge_sort(arr[:mid])\n    right = merge_sort(arr[mid:])\n    return merge(left, right)',
            'input': '[38, 27, 43, 3, 9, 82, 10]',
            'output': '[3, 9, 10, 27, 38, 43, 82]',
            'complexity': 'O(n log n)',
            'tags': 'sorting, stable'
        }
    }
    
    path = saver.append(new_data)
    print(f" Данные дописаны в: {path}")
    print(" Структура файла:")
    print(f"   - Лист: {saver.sheet.title}")
    print(f"   - Строк данных: {saver.sheet.max_row - 1}")
    print(f"   - Колонок: {saver.sheet.max_column}")