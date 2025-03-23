# CofifoAIWO - Developer Handover Documentation

## Projektübersicht

CofifoAIWO (Combine Files for AI Workflows) ist ein Tool, das Dateien und Verzeichnisse zu einer einzelnen Textdatei kombiniert. Es wurde speziell für den KI-Workflow entwickelt, wo Benutzer häufig mehrere Dateien in einem Format bereitstellen müssen, das von LLMs verarbeitet werden kann.

## Kernfunktionalitäten

1. **Dateikombination**: Mehrere Dateien oder Verzeichnisse werden zu einer Textdatei zusammengefasst
2. **Shortcuts**: Speichern häufig verwendeter Pfadkombinationen für schnellen Zugriff
3. **Verzeichnisstruktur**: Option zum Einbeziehen der Tree-Struktur in die Ausgabe
4. **Dual-Interface**: Sowohl CLI als auch Web-GUI verfügbar

## Projektarchitektur

### Dateistruktur
```
CofifoAIWO/
├── app.py                     # Flask-Backend
├── combine_files.py           # CLI-Tool und Kernfunktionalität
├── cli.py                     # Interaktives CLI-Interface
├── setup.py                   # Setup und Installation
├── start.py                   # Starter-Skript
├── requirements.txt           # Python-Abhängigkeiten
├── README.md                  # Projektdokumentation
├── INSTALLATION.md            # Installationsanleitung
├── Dockerfile                 # Container-Definition
├── docker-compose.yml         # Container-Orchestrierung
└── static/                    # Frontend-Dateien
    ├── index.html             # Startseite
    ├── shortcuts.html         # Shortcuts-Seite
    └── browser.html           # File-Browser-Seite
```

### Technologiestack

- **Backend**: Python mit Flask
- **Frontend**: HTML, CSS, JavaScript (Vanilla, kein Framework)
- **Datenbank**: Keine - Shortcuts werden in JSON-Datei gespeichert
- **Container**: Docker-Support für einfache Bereitstellung

## Komponenten im Detail

### 1. Core-Logik (`combine_files.py`)

Diese Datei enthält die Kernfunktionalität zum Kombinieren von Dateien. Wichtige Funktionen:

- `get_files_from_paths()`: Sammelt Dateien rekursiv aus Pfaden
- `generate_tree_structure()`: Erstellt eine Baumdarstellung für Verzeichnisse
- `use_shortcut()`: Verwendet gespeicherte Pfadkombinationen
- `add_shortcut()`, `remove_shortcut()`, `list_shortcuts()`: Shortcut-Verwaltung

Die Datei kann als eigenständiges CLI-Tool verwendet werden, wird aber auch vom Web-Backend genutzt.

### 2. Web-Backend (`app.py`)

Flask-Server mit RESTful API-Endpunkten:

- `/api/browse`: Durchsuchen von Verzeichnissen
- `/api/list_shortcuts`: Abrufen aller Shortcuts
- `/api/add_shortcut`: Hinzufügen eines neuen Shortcuts
- `/api/remove_shortcut`: Entfernen eines Shortcuts
- `/api/use_shortcut`: Verwenden eines Shortcuts
- `/api/download/<filename>`: Herunterladen generierter Dateien

Besondere Beachtung: Die `api_browse`-Funktion ist aktuell so konfiguriert, dass sie beliebige Verzeichnisse durchsuchen kann, was potenziell unsicher sein könnte. Bei Bedarf kann hier eine Sicherheitseinschränkung implementiert werden.

### 3. Frontend (static/*)

Die Web-GUI besteht aus drei Hauptseiten:

- **index.html**: Startseite mit Übersicht der Funktionen
- **browser.html**: File-Browser zum Auswählen von Dateien und Verzeichnissen
- **shortcuts.html**: Verwaltung von gespeicherten Shortcuts

Alle Seiten nutzen Vanilla-JavaScript für die Kommunikation mit der Backend-API. Die Hauptfunktionen im JavaScript:

- Verzeichnisse und Dateien durchsuchen
- Dateien auswählen und zur Liste hinzufügen
- Shortcuts erstellen und verwalten
- Textdateien generieren und herunterladen

### 4. CLI-Interface (`cli.py`)

Ein interaktives Kommandozeilen-Interface, das eine benutzerfreundlichere Alternative zum direkten Aufruf von `combine_files.py` bietet.

### 5. Installer und Starter (`setup.py`, `start.py`)

`setup.py` installiert die Abhängigkeiten und richtet die Umgebung ein.
`start.py` bietet einen einfachen Weg, die Anwendung zu starten.

## Datenmanagement

- **Shortcuts**: Gespeichert in `shortcuts.json` im Hauptverzeichnis
- **Ausgabedateien**: Im Arbeitsverzeichnis gespeichert, nicht dauerhaft in der Anwendung

## Bekannte Probleme und Einschränkungen

1. **Sicherheit**: Die Anwendung erlaubt das Browsen beliebiger Verzeichnisse
2. **Große Dateien**: Keine spezielle Behandlung für sehr große Dateien
3. **Zeichenkodierung**: Kann bei bestimmten Dateien zu Problemen führen
4. **Shortcuts**: Werden lokal in einer JSON-Datei gespeichert, keine Benutzerverwaltung

## Deployment

### Lokale Ausführung

```bash
# Backend starten
python app.py

# CLI verwenden
python cli.py

# Oder direkte Befehle
python combine_files.py --help
```

### Docker-Deployment

```bash
# Container bauen und starten
docker-compose up -d
```

## Weiterentwicklungspotenzial

1. **Erweiterte Filterfunktionen**: Nach Dateityp, Größe, Änderungsdatum
2. **Benutzerverwaltung**: Mehrbenutzerunterstützung mit separaten Shortcuts
3. **Export-Formate**: Unterstützung für andere Ausgabeformate (Markdown, JSON)
4. **Vorschauanzeige**: Inhalt von Dateien direkt im Browser anzeigen
5. **Verbesserte Sicherheit**: Pfadbeschränkungen und Zugriffskontrollen
6. **Internationalisierung**: Mehrsprachige Benutzeroberfläche
7. **Progressive Web App**: Offline-Funktionalität

## Nächste Schritte für neue Entwickler

1. **Einrichtung**: Repository klonen, `python setup.py` ausführen
2. **Funktionsweise verstehen**: Die Anwendung durch die CLI und Web-GUI erkunden
3. **Codeüberblick**: Die Kernkomponenten durchgehen (`combine_files.py`, `app.py`)
4. **Test-Instanz**: Eine eigene Testinstanz starten: `python app.py`

## Kontakt

Bei Fragen zur Weiterentwicklung kontaktiere: 
- Projekt-Repository: [github.com/ogerly/cofifoaiwo](https://github.com/ogerly/cofifoaiwo)
- Entwickler: [ogerly](https://github.com/ogerly)

---

Diese Dokumentation sollte dir einen umfassenden Überblick über das CofifoAIWO-Projekt geben. Das Tool ist bereits voll funktionsfähig, aber es gibt Raum für Verbesserungen und neue Features. Viel Erfolg bei der Weiterentwicklung!