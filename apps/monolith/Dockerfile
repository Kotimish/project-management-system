# Базовый образ
FROM python:3.12-slim

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Рабочая директория
WORKDIR /app

# Устанавливаем Poetry
RUN pip install poetry

# Копируем файлы конфигурации
COPY pyproject.toml poetry.lock README.md ./

# Устанавливаем только зависимости
RUN poetry install --no-root

# Копируем код
COPY src/monolith ./src/monolith

# Устанавливаем модули
RUN poetry install

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "monolith.presentation.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]