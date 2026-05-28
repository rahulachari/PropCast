FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN python manage.py migrate --no-input

EXPOSE 8000

CMD python manage.py runserver 0.0.0.0:$PORT
