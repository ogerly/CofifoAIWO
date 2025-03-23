#!/usr/bin/env python
"""
CofifoAIWO CLI-Starter

Dieses Skript stellt eine interaktive Kommandozeile für CofifoAIWO bereit.
"""

import os
import sys
import subprocess
from pathlib import Path

# Pfad zum Basisverzeichnis
BASE_DIR = Path(__file__).resolve().parent
COMBINE_FILES_PY = BASE_DIR / "combine_files.py"

def print_header():
    """Druckt einen Kopf für die CLI."""
    print("\n" + "=" * 60)
    print(" CofifoAIWO CLI")
    print("=" * 60)
    print("Combine Files for AI Workflows - CLI-Mode")
    print("Entwickelt von: https://github.com/ogerly")
    print("-" * 60)

def print_commands():
    """Zeigt verfügbare Befehle an."""
    print("\nVerfügbare Befehle:")
    print("1: Shortcuts auflisten")
    print("2: Shortcut hinzufügen")
    print("3: Shortcut verwenden")
    print("4: Shortcut entfernen")
    print("5: Hilfe anzeigen")
    print("6: Web-Interface starten")
    print("0: Beenden")

def list_shortcuts():
    """Listet alle verfügbaren Shortcuts auf."""
    subprocess.run([sys.executable, COMBINE_FILES_PY, "--list"])

def add_shortcut():
    """Fügt einen neuen Shortcut hinzu."""
    name = input("\nName des Shortcuts: ")
    
    print("\nPfade eingeben (einer pro Zeile, leere Zeile zum Beenden):")
    paths = []
    while True:
        path = input("> ")
        if not path:
            break
        paths.append(path)
    
    if paths:
        command = [sys.executable, COMBINE_FILES_PY, "--add", name] + paths
        subprocess.run(command)
    else:
        print("Keine Pfade angegeben. Shortcut wurde nicht erstellt.")

def use_shortcut():
    """Verwendet einen Shortcut, um eine Ausgabedatei zu generieren."""
    # Zuerst alle verfügbaren Shortcuts anzeigen
    list_shortcuts()
    
    name = input("\nName des zu verwendenden Shortcuts: ")
    output_file = input("Name der Ausgabedatei: ")
    include_tree = input("Verzeichnisstruktur einbeziehen (j/n)? ").lower() in ["j", "ja"]
    
    command = [sys.executable, COMBINE_FILES_PY, "--use", name, output_file]
    if include_tree:
        command.append("--tree")
    
    subprocess.run(command)

def remove_shortcut():
    """Entfernt einen Shortcut."""
    # Zuerst alle verfügbaren Shortcuts anzeigen
    list_shortcuts()
    
    name = input("\nName des zu entfernenden Shortcuts: ")
    confirm = input(f"Möchtest du den Shortcut '{name}' wirklich entfernen (j/n)? ").lower()
    
    if confirm in ["j", "ja"]:
        subprocess.run([sys.executable, COMBINE_FILES_PY, "--remove", name])
    else:
        print("Löschvorgang abgebrochen.")

def show_help():
    """Zeigt die Hilfe an."""
    subprocess.run([sys.executable, COMBINE_FILES_PY, "--help"])

def start_web_interface():
    """Startet das Web-Interface."""
    app_py = BASE_DIR / "app.py"
    
    if not app_py.exists():
        print(f"Fehler: app.py nicht gefunden: {app_py}")
        return
    
    print("\nStarte Web-Interface...")
    print("Die Anwendung ist unter http://localhost:5000 erreichbar.")
    print("Drücke Strg+C, um zu beenden.")
    
    try:
        subprocess.run([sys.executable, app_py])
    except KeyboardInterrupt:
        print("\nWeb-Interface beendet.")

def main():
    """Hauptfunktion."""
    # Überprüfe, ob Kommandozeilenargumente übergeben wurden
    if len(sys.argv) > 1:
        # Wenn Argumente vorhanden sind, leite sie direkt an combine_files.py weiter
        subprocess.run([sys.executable, COMBINE_FILES_PY] + sys.argv[1:])
        return
    
    print_header()
    
    while True:
        print_commands()
        choice = input("\nWähle einen Befehl (0-6): ")
        
        if choice == "0":
            print("Auf Wiedersehen!")
            break
        elif choice == "1":
            list_shortcuts()
        elif choice == "2":
            add_shortcut()
        elif choice == "3":
            use_shortcut()
        elif choice == "4":
            remove_shortcut()
        elif choice == "5":
            show_help()
        elif choice == "6":
            start_web_interface()
        else:
            print("Ungültige Eingabe. Bitte wähle 0-6.")
        
        input("\nDrücke Enter, um fortzufahren...")

if __name__ == "__main__":
    main()