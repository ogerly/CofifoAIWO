#!/usr/bin/env python
"""
CofifoAIWO Setup-Skript
Dieses Skript bereitet die Anwendung für die Verwendung vor, indem es:
1. Die Abhängigkeiten installiert
2. Das Frontend erstellt
3. Die Anwendung startet
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# Konstanten
BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"
REQUIREMENTS_FILE = BASE_DIR / "requirements.txt"

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

def install_python_dependencies():
    """Installiert die Python-Abhängigkeiten."""
    print_header("Installiere Python-Abhängigkeiten")
    
    if not run_command(f"{sys.executable} -m pip install -r {REQUIREMENTS_FILE}"):
        print("Fehler beim Installieren der Python-Abhängigkeiten. Bitte prüfe die Fehlermeldung.")
        return False
    
    return True

def setup_frontend():
    """Richtet das Frontend ein und erstellt es."""
    print_header("Richte Frontend ein")
    
    # Überprüfe, ob npm oder yarn verfügbar ist
    npm_or_yarn = "yarn" if shutil.which("yarn") else "npm"
    
    if not os.path.exists(FRONTEND_DIR):
        print(f"Frontend-Verzeichnis nicht gefunden: {FRONTEND_DIR}")
        print("Erstelle Frontend-Verzeichnis...")
        os.makedirs(FRONTEND_DIR, exist_ok=True)
    
    # Erstelle package.json, wenn noch nicht vorhanden
    package_json = FRONTEND_DIR / "package.json"
    if not os.path.exists(package_json):
        print("Erstelle package.json...")
        with open(package_json, "w") as f:
            f.write("""
{
  "name": "cofifoaiwo-frontend",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "serve": "vue-cli-service serve",
    "build": "vue-cli-service build",
    "lint": "vue-cli-service lint"
  },
  "dependencies": {
    "axios": "^0.27.2",
    "core-js": "^3.25.0",
    "vue": "^3.2.38",
    "vue-router": "^4.1.5",
    "vuex": "^4.0.2"
  },
  "devDependencies": {
    "@vue/cli-plugin-babel": "~5.0.8",
    "@vue/cli-plugin-eslint": "~5.0.8",
    "@vue/cli-plugin-router": "~5.0.8",
    "@vue/cli-plugin-vuex": "~5.0.8",
    "@vue/cli-service": "~5.0.8",
    "@vue/compiler-sfc": "^3.2.38",
    "eslint": "^8.23.0",
    "eslint-plugin-vue": "^9.4.0"
  }
}
            """.strip())
    
    # Installiere Frontend-Abhängigkeiten
    print(f"Installiere Frontend-Abhängigkeiten mit {npm_or_yarn}...")
    if not run_command(f"{npm_or_yarn} install", cwd=FRONTEND_DIR):
        print("Fehler beim Installieren der Frontend-Abhängigkeiten. Bitte prüfe die Fehlermeldung.")
        return False
    
    # Erstelle Frontend
    print(f"Erstelle Frontend mit {npm_or_yarn}...")
    if not run_command(f"{npm_or_yarn} run build", cwd=FRONTEND_DIR):
        print("Fehler beim Erstellen des Frontends. Bitte prüfe die Fehlermeldung.")
        return False
    
    return True

def start_application():
    """Startet die Anwendung."""
    print_header("Starte Anwendung")
    
    print("CofifoAIWO wird gestartet...")
    print("Die Anwendung ist unter http://localhost:5000 erreichbar.")
    
    run_command(f"{sys.executable} app.py")

def main():
    """Hauptfunktion."""
    print_header("CofifoAIWO Setup")
    
    print("Dieses Skript bereitet CofifoAIWO für die Verwendung vor.")
    print("Es installiert die Abhängigkeiten, erstellt das Frontend und startet die Anwendung.")
    
    # Frage nach Bestätigung
    choice = input("\nMöchtest du fortfahren? (j/n): ").lower()
    if choice != 'j' and choice != 'ja':
        print("Setup abgebrochen.")
        return
    
    # Führe alle Setup-Schritte aus
    if not install_python_dependencies():
        print("Fehler beim Installieren der Python-Abhängigkeiten. Setup wird abgebrochen.")
        return
    
    if not setup_frontend():
        print("Fehler beim Einrichten des Frontends. Setup wird abgebrochen.")
        return
    
    print("\nSetup erfolgreich abgeschlossen!")
    
    # Frage, welche Ausführungsart gewünscht ist
    print("\nWie möchtest du CofifoAIWO starten?")
    print("1: Webanwendung (GUI im Browser)")
    print("2: Kommandozeile (CLI)")
    print("3: Nicht jetzt starten")
    
    while True:
        choice = input("\nWähle eine Option (1-3): ")
        
        if choice == "1":
            start_application()
            break
        elif choice == "2":
            print("\nBeispiel-Befehle für die CLI-Nutzung:")
            print(f"  {sys.executable} combine_files.py --list")
            print(f"  {sys.executable} combine_files.py --add my_project /pfad/zum/verzeichnis")
            print(f"  {sys.executable} combine_files.py --use my_project output.txt --tree")
            
            cmd = input("\nGib deinen gewünschten CLI-Befehl ein (oder drücke Enter, um zu beenden): ")
            if cmd.strip():
                os.system(f"{sys.executable} combine_files.py {cmd}")
            break
        elif choice == "3":
            print("\nDu kannst die Anwendung später starten mit:")
            print(f"  GUI:  {sys.executable} app.py")
            print(f"  CLI:  {sys.executable} combine_files.py --help")
            print("\nDie Webanwendung ist dann unter http://localhost:5000 erreichbar.")
            break
        else:
            print("Ungültige Eingabe. Bitte wähle 1, 2 oder 3.")

if __name__ == "__main__":
    main()