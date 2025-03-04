# Utilisation de l'image Python officielle
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers de ton projet dans le conteneur
COPY . /app/

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port 8000
EXPOSE 8000

# Commande pour démarrer l'application Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
