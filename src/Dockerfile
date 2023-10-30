# Используем Docker - образ с  python 3.10
FROM python:3.10

# Установка рабочей директории
WORKDIR /app

# Копируем зависимости в контейнер
COPY ./requirements.txt /app/

# Копируем проект в контейнер
COPY ./src /app/

# Установка зависимостей
RUN pip install -r requirements.txt
