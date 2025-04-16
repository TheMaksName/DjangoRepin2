FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Сборка статики и запуск
# Сборка статики
#RUN python /app/registration/manage.py collectstatic --noinput

CMD ["gunicorn","--pythonpath","registration", "--bind", "0.0.0.0:8000", "registration.wsgi:application"]
