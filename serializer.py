import json
import os

DATA_FILE = "dan.json"


def _ensure_file():
    """Создаёт файл с пустой структурой, если его нет."""
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({"users": {}}, f)


def get_data():
    """Читает и возвращает данные из файла."""
    _ensure_file()
    with open(DATA_FILE, "r", encoding="UTF-8") as f:
        return json.load(f)


def write(new_data):
    """Записывает данные в файл."""
    with open(DATA_FILE, "w", encoding="UTF-8") as f:
        json.dump(new_data, f, ensure_ascii=False, indent=4)
