# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app

# Installation des dépendances système
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gdal-bin \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

# Création de l'environnement virtuel
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Installation des dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Installation des dépendances système minimales
RUN apt-get update && apt-get install -y \
    libpq5 \
    gdal-bin \
    && rm -rf /var/lib/apt/lists/*

# Copie de l'environnement virtuel depuis le builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copie du code source
COPY . .

# Variables d'environnement
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Exposition du port
EXPOSE 8000

# Commande de démarrage
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 