# Установка базового образа
FROM python:3.11

# устанавливаем зависимости
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории внутри контейнера
WORKDIR /app

# Копирование зависимостей в контейнер
COPY requirements.txt .

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходных файлов в контейнер
COPY . .

# Определение переменной окружения для запуска приложения FastAPI
ENV PORT 8000

# Открытие порта для внешнего доступа
EXPOSE $PORT

# Запуск команды для запуска приложения FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

