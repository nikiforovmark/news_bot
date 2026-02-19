import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла (если он есть)
load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
BASE_ID = os.getenv('BASE_ID')

# Если переменные не найдены, можно выбросить понятную ошибку
if TOKEN is None:
    raise ValueError("Не задан BOT_TOKEN в переменных окружения или .env файле")
if BASE_ID is None:
    raise ValueError("Не задан BASE_ID в переменных окружения или .env файле")