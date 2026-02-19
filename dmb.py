import json
import os
from datetime import datetime, timedelta

DATA_FILE = "dan.json"


def _ensure_file():
    """Создаёт файл с пустой структурой, если его нет."""
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({"users": {}}, f)


def _read_data():
    _ensure_file()
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def _write_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def get_date(uid):
    """
    Возвращает (day, month, year) для пользователя uid,
    или None, если дата не установлена.
    """
    data = _read_data()
    user_data = data["users"].get(str(uid))
    if user_data and "dmb" in user_data:
        d = user_data["dmb"]
        return d.get("day"), d.get("month"), d.get("year")
    return None


def set_date(uid, day, month, year):
    """Сохраняет дату ДМБ для пользователя uid."""
    data = _read_data()
    if str(uid) not in data["users"]:
        data["users"][str(uid)] = {}
    data["users"][str(uid)]["dmb"] = {"day": day, "month": month, "year": year}
    _write_data(data)


def dmb(uid):
    """
    Формирует сообщение о прогрессе ДМБ для пользователя uid.
    Если дата не задана – возвращает сообщение-подсказку.
    """
    date_tuple = get_date(uid)
    if date_tuple is None or None in date_tuple:
        return "Дата ДМБ не установлена. Используйте /setdmb ДД ММ ГГГГ"

    day, month, year = date_tuple
    start_date = datetime(year, month, day)
    now = datetime.now()
    delta = now - start_date
    total_seconds = delta.total_seconds()
    days_in_year = 364
    percent = (total_seconds / timedelta(days=days_in_year).total_seconds()) * 100

    if percent <= 100:
        passed = str(delta)[:-7]
        remained = str(timedelta(days=days_in_year) - delta)[:-7]
        return f"{round(percent, 6)}%\nПрошло: {passed}\nОсталось: {remained}"
    else:
        # После дембеля
        over = str(delta - timedelta(days=days_in_year))[:-7]
        return f"100%\nПрошло после дембеля:\n{over}"
