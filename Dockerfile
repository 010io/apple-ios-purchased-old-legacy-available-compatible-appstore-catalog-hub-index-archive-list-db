# Використовуємо Alpine Linux з Python 3.12
FROM python:3.12-alpine

# Встановлюємо робочу директорію
WORKDIR /app

# Встановлюємо системні залежності
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    sqlite-dev

# Копіюємо файл залежностей
COPY requirements.txt .

# Встановлюємо Python залежності
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо код додатку
COPY . .

# Створюємо директорію для бази даних
RUN mkdir -p /app/data

# Експонуємо порт
EXPOSE 8000

# Команда за замовчуванням - запускаємо API сервер
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
