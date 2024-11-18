# Utilisation de l'image officielle de Python
FROM python:3.11-slim

# Installer les dépendances de psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Exposition du port
EXPOSE 8000

# Commande pour démarrer le serveur
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
