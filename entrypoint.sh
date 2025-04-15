#!/bin/sh

# Ждем готовности PostgreSQL
until pg_isready -h $DB_HOST -p $DB_PORT; do
  echo "Waiting for PostgreSQL..."
  sleep 2
done

# Применяем миграции
python manage.py migrate

# Собираем статику
python manage.py collectstatic --noinput

# Запускаем Gunicorn
exec gunicorn --bind 0.0.0.0:8000 project.wsgi