FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Копирование requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Загрузка spaCy модели
RUN python -m spacy download ru_core_news_sm

# Копирование кода
COPY . .

# Создание директории для uploads
RUN mkdir -p uploads

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

