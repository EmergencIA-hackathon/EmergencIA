FROM python:3.9

USER root

RUN apt-get update && apt-get install -y \
    ffmpeg \
    tesseract-ocr \
    libtesseract-dev

WORKDIR /app

COPY requirements.txt .

COPY set_webhook.sh /app/

RUN pip install aiohttp

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app

ENV TESSERACT_CMD=/usr/bin/tesseract

WORKDIR /app/flask_app

EXPOSE 5000

CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:5000", "flask_app.app:app"]

