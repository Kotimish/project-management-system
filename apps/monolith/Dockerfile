# Базовый образ
FROM python:3.12-slim

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Рабочая директория
WORKDIR /app

# Устанавливаем Poetry
RUN pip install --upgrade pip wheel poetry
RUN poetry config virtualenvs.create false

# Копируем файлы конфигурации
COPY pyproject.toml poetry.lock README.md ./

# Устанавливаем только зависимости
RUN poetry install --no-root

# Копируем код
COPY src/monolith ./src/monolith

# Копируем Alembic и entrypoint
COPY alembic ./alembic
COPY alembic.ini ./
COPY scripts/entrypoint.sh ./

# Копирует файл окружения
COPY .env.default .env

# Делаем скрипт исполняемым
RUN chmod +x entrypoint.sh

# Устанавливаем модули
RUN poetry install

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]

CMD ["poetry", "run", "uvicorn", "monolith.app:app", "--host", "0.0.0.0", "--port", "8000"]