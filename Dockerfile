FROM node:16-alpine AS frontend-builder

WORKDIR /app/frontend

# Kopiere Frontend-Dateien
COPY frontend/package*.json ./
RUN npm install

COPY frontend/ ./
RUN npm run build

# Verwende ein Python-Image für das Backend
FROM python:3.9-slim

WORKDIR /app

# Kopiere Python-Anforderungen und installiere Abhängigkeiten
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere Backend-Dateien
COPY app.py combine_files.py ./
COPY shortcuts.json ./

# Kopiere das gebaute Frontend
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Port freigeben
EXPOSE 5000

# Starte die Anwendung
CMD ["python", "app.py"]