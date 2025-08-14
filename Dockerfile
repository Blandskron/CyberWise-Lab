# Usamos Python 3.12 slim por compatibilidad estable con dependencias
FROM python:3.12-slim

# Variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8000

# Dependencias del sistema (opcionales, pero útiles para compilaciones)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiamos requirements primero para aprovechar cache
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip && \
    pip install -r /app/requirements.txt

# Copiamos el código
COPY app /app/app

# Crear carpeta de logs (si usas logging a archivo)
RUN mkdir -p /app/logs

# Exponemos puerto
EXPOSE 8000

# Usuario no root (opcional)
RUN useradd -ms /bin/bash appuser
USER appuser

# Comando
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
