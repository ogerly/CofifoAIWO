# CofifoAIWO Installationsanleitung

Diese Anleitung führt Sie durch die Installation und Einrichtung von CofifoAIWO.

## Voraussetzungen

- Python 3.7 oder höher
- Node.js 14.x oder höher und npm/yarn
- Git (optional, zum Klonen des Repositories)

## Methode 1: Direkte Installation

### 1. Repository klonen oder Dateien herunterladen

```bash
git clone https://github.com/ogerly/cofifoaiwo.git
cd cofifoaiwo
```

### 2. Setup ausführen

```bash
python setup.py
```

Das Setup-Skript führt folgende Schritte aus:
- Installation der Python-Abhängigkeiten
- Einrichtung des Frontends (Installation der npm-Pakete und Erstellung des Builds)
- Start der Anwendung (optional)

### 3. Anwendung manuell starten (falls nicht während des Setups gestartet)

```bash
python app.py
```

Die Anwendung ist dann unter http://localhost:5000 verfügbar.

## Methode 2: Mit Docker

Wenn Sie Docker und Docker Compose installiert haben, können Sie die Anwendung auch in einem Container ausführen:

### 1. Repository klonen oder Dateien herunterladen

```bash
git clone https://github.com/ogerly/cofifoaiwo.git
cd cofifoaiwo
```

### 2. Container starten

```bash
docker-compose up -d
```

Die Anwendung ist dann unter http://localhost:5000 verfügbar.

## Verzeichnisstruktur

Nach der Installation sollte Ihre Verzeichnisstruktur wie folgt aussehen:

```
cofifoaiwo/
├── app.py                     # Flask-Backend
├── combine_files.py           # CLI-Tool
├── create_frontend_structure.py # Hilfsskript für das Frontend
├── docker-compose.yml         # Docker Compose-Konfiguration
├── Dockerfile                 # Docker-Konfiguration
├── frontend/                  # Vue.js Frontend
│   ├── dist/                  # Gebautes Frontend
│   ├── node_modules/          # Frontend-Abhängigkeiten
│   ├── package.json           # Frontend-Konfiguration
│   └── src/                   # Frontend-Quellcode
├── INSTALLATION.md            # Diese Datei
├── README.md                  # Projektdokumentation
├── requirements.txt           # Python-Abhängigkeiten
├── setup.py                   # Setup-Skript
├── shortcuts.json             # Gespeicherte Shortcuts
└── start.py                   # Starter-Skript
```

## Fehlerbehebung

### Problem: Frontend wird nicht angezeigt

Überprüfen Sie, ob das Frontend gebaut wurde:
```bash
ls frontend/dist
```

Wenn das Verzeichnis nicht existiert oder leer ist, bauen Sie das Frontend manuell:
```bash
cd frontend
npm install
npm run build
```

### Problem: Flask-Server startet nicht

Überprüfen Sie, ob alle Abhängigkeiten installiert sind:
```bash
pip install -r requirements.txt
```

Stellen Sie auch sicher, dass der Port 5000 nicht bereits von einer anderen Anwendung verwendet wird.

### Problem: Shortcut-Funktionalität funktioniert nicht

Überprüfen Sie die Datei `shortcuts.json`. Wenn sie nicht existiert, erstellen Sie eine leere JSON-Datei:
```bash
echo "{}" > shortcuts.json
```

## Support

Bei Fragen oder Problemen erstellen Sie bitte ein Issue auf GitHub oder kontaktieren Sie den Entwickler über das Repository.