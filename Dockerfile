FROM python:3.9-slim

WORKDIR /app

# Копируем только requirements для кеширования слоя с зависимостями
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код
COPY . .

CMD ["python", "main.py"]