# Используем базовый образ Python 3.12
FROM python:3.12-slim
RUN groupadd -r football_team && useradd -r -g football_team football_team
# Устанавливаем рабочую директорию
WORKDIR /app
# Копируем файл requirements.txt в рабочую директорию
COPY requirements.txt .
# Устанавливаем зависимости
RUN pip install -r requirements.txt
# Копируем все файлы проекта в рабочую директорию
COPY . .
USER football_team
# Запускаем сервер Django
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

