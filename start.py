#!/usr/bin/env python
"""
CofifoAIWO Starter-Skript

Dieses Skript überprüft, ob alle notwendigen Komponenten vorhanden sind,
und startet dann die Anwendung.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# Konstanten
BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"
FRONTEND_DIST_DIR = FRONTEND_DIR / "dist"
APP_PY = BASE_DIR / "app.py"
SETUP_PY = BASE_DIR / "setup.py"
CREATE_FRONTEND_STRUCTURE_PY = BASE_DIR / "create_frontend_structure.py"

def print_header(text):
    """Gibt eine formatierte Überschrift aus."""
    print("\n" + "=" * 60)
    print(f" {text}")
    print("=" * 60)

def run_command(command, cwd=None):
    """Führt einen Befehl aus und gibt die Ausgabe zurück."""
    print(f"Ausführen: {command}")
    
    try:
        process = subprocess.run(
            command,
            shell=True,
            check=True,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        if process.stdout:
            print(process.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Fehler bei der Ausführung von '{command}':")
        print(e.stderr)
        return False

def check_components():
    """Überprüft, ob alle notwendigen Komponenten vorhanden sind."""
    print_header("Überprüfe Komponenten")
    
    # Überprüfe, ob app.py existiert
    if not APP_PY.exists():
        print(f"Fehler: app.py nicht gefunden: {APP_PY}")
        return False
    
    # Überprüfe, ob das Frontend-Verzeichnis existiert
    if not FRONTEND_DIR.exists():
        print(f"Frontend-Verzeichnis nicht gefunden: {FRONTEND_DIR}")
        print("Erstelle Frontend-Verzeichnis...")
        os.makedirs(FRONTEND_DIR, exist_ok=True)
    
    # Überprüfe, ob das Frontend-Dist-Verzeichnis existiert
    if not FRONTEND_DIST_DIR.exists():
        print(f"Frontend-Dist-Verzeichnis nicht gefunden: {FRONTEND_DIST_DIR}")
        
        # Überprüfe, ob setup.py existiert
        if SETUP_PY.exists():
            print("Führe setup.py aus, um das Frontend zu erstellen...")
            run_command(f"{sys.executable} {SETUP_PY}")
        else:
            print("Fehler: setup.py nicht gefunden. Frontend kann nicht erstellt werden.")
            return False
    
    # Überprüfe erneut, ob das Frontend-Dist-Verzeichnis jetzt existiert
    if not FRONTEND_DIST_DIR.exists():
        print(f"Fehler: Frontend-Dist-Verzeichnis konnte nicht erstellt werden: {FRONTEND_DIST_DIR}")
        
        # Überprüfe, ob create_frontend_structure.py existiert
        if CREATE_FRONTEND_STRUCTURE_PY.exists():
            print("Führe create_frontend_structure.py aus, um die Frontend-Struktur zu erstellen...")
            run_command(f"{sys.executable} {CREATE_FRONTEND_STRUCTURE_PY}")
            
            # Überprüfe, ob npm oder yarn verfügbar ist
            npm_or_yarn = "yarn" if shutil.which("yarn") else "npm"
            
            # Installiere Frontend-Abhängigkeiten und erstelle Frontend
            print(f"Installiere Frontend-Abhängigkeiten mit {npm_or_yarn}...")
            run_command(f"{npm_or_yarn} install", cwd=FRONTEND_DIR)
            
            print(f"Erstelle Frontend mit {npm_or_yarn}...")
            run_command(f"{npm_or_yarn} run build", cwd=FRONTEND_DIR)
        else:
            print("Fehler: create_frontend_structure.py nicht gefunden. Frontend-Struktur kann nicht erstellt werden.")
            return False
    
    return True

def start_application():
    """Startet die Anwendung."""
    print_header("Starte Anwendung")
    
    print("CofifoAIWO wird gestartet...")
    print("Die Anwendung ist unter http://localhost:5000 erreichbar.")
    
    run_command(f"{sys.executable} {APP_PY}")

def main():
    """Hauptfunktion."""
    print_header("CofifoAIWO Starter")
    
    if not check_components():
        print("Fehler beim Überprüfen der Komponenten. CofifoAIWO kann nicht gestartet werden.")
        return
    
    start_application()

if __name__ == "__main__":
    main()