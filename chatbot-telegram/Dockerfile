# Imagem base para Python
FROM python:3.9

# Atualizar o sistema e instalar dependências
USER root
RUN apt-get update && apt-get install -y \
    ffmpeg \
    tesseract-ocr \
    libtesseract-dev

# Definir diretório de trabalho
WORKDIR /app

# Copiar e instalar dependências
COPY requirements.txt .
RUN pip install aiohttp
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código para o container
COPY . .

# Definir variável para garantir que Flask reconheça o diretório correto
ENV PYTHONPATH=/app

# Definir caminho do Tesseract para o pytesseract
ENV TESSERACT_CMD=/usr/bin/tesseract

# Definir diretório correto para rodar o app
WORKDIR /app/flask_app

# Expor a porta para o app Flask
EXPOSE 5000

# Comando padrão para rodar o container
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:5000", "flask_app.app:app"]
