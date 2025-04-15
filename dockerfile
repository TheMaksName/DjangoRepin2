FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*





COPY . .


# Сборка статики и запуск
# Сборка статики
# RUN python /app/registration/manage.py collectstatic --noinput

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "registration.wsgi:application"]