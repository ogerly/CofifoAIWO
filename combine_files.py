#!/usr/bin/env python
"""
CofifoAIWO - Combine Files for AI Workflows

Dieses Skript kombiniert den Inhalt mehrerer Dateien oder Verzeichnisse
in einer einzigen Textdatei. Dies ist besonders nützlich für die Arbeit
mit KI-Modellen, bei der häufig der Inhalt mehrerer Dateien als Eingabe
benötigt wird.
"""

import os
import sys
import json
from pathlib import Path

# Konstante für die Shortcut-Datei
SHORTCUTS_FILE = "shortcuts.json"

# Verzeichnisse, die ignoriert werden sollen
IGNORED_DIRS = {"dist", "node_modules", ".git", "__pycache__", "venv"}

def load_shortcuts():
    """Lädt die Shortcuts aus der JSON-Datei."""
    if os.path.exists(SHORTCUTS_FILE):
        with open(SHORTCUTS_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {}

def save_shortcuts(shortcuts):
    """Speichert die Shortcuts in der JSON-Datei."""
    with open(SHORTCUTS_FILE, 'w', encoding='utf-8') as file:
        json.dump(shortcuts, file, indent=4)

def add_shortcut(name, paths):
    """Fügt einen neuen Shortcut hinzu."""
    shortcuts = load_shortcuts()
    if name in shortcuts:
        print(f"Warnung: Shortcut '{name}' existiert bereits und wird überschrieben.")
    shortcuts[name] = paths
    save_shortcuts(shortcuts)
    print(f"Shortcut '{name}' wurde hinzugefügt.")

def remove_shortcut(name):
    """Entfernt einen Shortcut."""
    shortcuts = load_shortcuts()
    if name in shortcuts:
        del shortcuts[name]
        save_shortcuts(shortcuts)
        print(f"Shortcut '{name}' wurde entfernt.")
    else:
        print(f"Fehler: Shortcut '{name}' existiert nicht.")

def list_shortcuts():
    """Listet alle verfügbaren Shortcuts auf."""
    shortcuts = load_shortcuts()
    if not shortcuts:
        print("Keine Shortcuts verfügbar.")
    else:
        print("Verfügbare Shortcuts:")
        for name, paths in shortcuts.items():
            print(f"- {name}: {', '.join(paths)}")

def generate_tree_structure(path, prefix=""):
    """Generiert die Verzeichnisstruktur im 'tree'-Format und ignoriert bestimmte Verzeichnisse."""
    tree = []
    if os.path.isdir(path):
        entries = os.listdir(path)
        entries = [e for e in entries if e not in IGNORED_DIRS]  # Ignoriere bestimmte Verzeichnisse
        for i, entry in enumerate(entries):
            full_path = os.path.join(path, entry)
            if i == len(entries) - 1:
                tree.append(f"{prefix}└── {entry}")
                if os.path.isdir(full_path) and entry not in IGNORED_DIRS:
                    tree.extend(generate_tree_structure(full_path, prefix + "    "))
            else:
                tree.append(f"{prefix}├── {entry}")
                if os.path.isdir(full_path) and entry not in IGNORED_DIRS:
                    tree.extend(generate_tree_structure(full_path, prefix + "│   "))
    return tree

def use_shortcut(name, output_file, include_tree=False):
    """Verwendet einen Shortcut, um Dateien zu kombinieren."""
    shortcuts = load_shortcuts()
    if name not in shortcuts:
        print(f"Fehler: Shortcut '{name}' existiert nicht.")
        sys.exit(1)

    paths = shortcuts[name]
    file_contents = get_files_from_paths(paths)

    with open(output_file, 'w', encoding='utf-8') as file:
        if include_tree:
            # Füge die Verzeichnisstruktur hinzu
            file.write("=== Verzeichnisstruktur ===\n")
            for path in paths:
                if os.path.isdir(path):
                    tree_structure = generate_tree_structure(path)
                    file.write("\n".join(tree_structure) + "\n")
                else:
                    file.write(f"└── {os.path.basename(path)}\n")
            file.write("\n\n")

        # Füge den Inhalt der Dateien hinzu
        for path, content in file_contents:
            file.write(f"=== Datei: {path} ===\n")
            file.write(content)
            file.write("\n\n")

    print(f"Der Inhalt von {len(file_contents)} Dateien wurde in {output_file} gespeichert.")

def read_file_content(file_path):
    """Liest den Inhalt einer Datei und gibt ihn als String zurück."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        return f"Fehler beim Lesen der Datei {file_path}: {str(e)}"

def get_files_from_paths(paths):
    """Verarbeitet eine Liste von Pfaden (Dateien oder Verzeichnisse) und gibt eine Liste von Tupeln zurück:
    (relativer Pfad, Dateiinhalt)."""
    file_contents = []
    for path in paths:
        if os.path.isfile(path):
            # Wenn es eine Datei ist, lies den Inhalt
            relative_path = os.path.basename(path)
            content = read_file_content(path)
            file_contents.append((relative_path, content))
        elif os.path.isdir(path):
            # Wenn es ein Verzeichnis ist, durchsuche es rekursiv
            for dirpath, dirnames, filenames in os.walk(path):
                # Kopiere Dirnames, damit wir sie ändern können
                dirnames_copy = dirnames.copy()
                # Entferne ignorierte Verzeichnisse
                for ignored_dir in IGNORED_DIRS:
                    if ignored_dir in dirnames_copy:
                        dirnames.remove(ignored_dir)  # Ändert dirnames in-place
                
                for filename in filenames:
                    # Ignoriere versteckte Dateien
                    if filename.startswith('.'):
                        continue
                    
                    full_path = os.path.join(dirpath, filename)
                    relative_path = os.path.relpath(full_path, start=os.path.dirname(path))
                    content = read_file_content(full_path)
                    file_contents.append((relative_path, content))
        else:
            print(f"Warnung: {path} ist weder eine Datei noch ein Verzeichnis und wird ignoriert.")
    return file_contents

def show_help():
    """Zeigt die Hilfe für das CLI-Tool an."""
    print("Verwendung: python combine_files.py <befehl> [argumente]")
    print("\nBefehle:")
    print("  --add <n> <pfad1> <pfad2> ...  Fügt einen neuen Shortcut hinzu.")
    print("  --remove <n>                   Entfernt einen Shortcut.")
    print("  --list                            Listet alle Shortcuts auf.")
    print("  --use <n> <output_file>        Verwendet einen Shortcut um eine Textdatei zu erstellen.")
    print("  --tree                            Fügt die Verzeichnisstruktur in die Ausgabedatei ein.")
    print("  --help                            Zeigt diese Hilfe an.")
    print("\nBeispiele:")
    print("  python combine_files.py --add my_project /pfad/zum/verzeichnis /pfad/zur/datei.txt")
    print("  python combine_files.py --use my_project output.txt --tree")
    print("  python combine_files.py --list")
    print("\nWeb-Interface:")
    print("  Starte die Webanwendung mit: python app.py")
    print("  Die Anwendung ist dann unter http://localhost:5000 erreichbar.")

def main():
    """Hauptfunktion für die CLI-Verarbeitung."""
    if len(sys.argv) < 2 or sys.argv[1] == "--help":
        show_help()
        sys.exit(0)

    command = sys.argv[1]

    if command == "--add":
        if len(sys.argv) < 4:
            print("Fehler: Ungültige Anzahl von Argumenten für --add.")
            print("Verwendung: python combine_files.py --add <n> <pfad1> <pfad2> ...")
            sys.exit(1)
        name = sys.argv[2]
        paths = sys.argv[3:]
        add_shortcut(name, paths)
    elif command == "--remove":
        if len(sys.argv) != 3:
            print("Fehler: Ungültige Anzahl von Argumenten für --remove.")
            print("Verwendung: python combine_files.py --remove <n>")
            sys.exit(1)
        name = sys.argv[2]
        remove_shortcut(name)
    elif command == "--list":
        list_shortcuts()
    elif command == "--use":
        if len(sys.argv) < 4:
            print("Fehler: Ungültige Anzahl von Argumenten für --use.")
            print("Verwendung: python combine_files.py --use <n> <output_file> [--tree]")
            sys.exit(1)
        name = sys.argv[2]
        output_file = sys.argv[3]
        include_tree = "--tree" in sys.argv
        use_shortcut(name, output_file, include_tree)
    else:
        print(f"Fehler: Unbekannter Befehl '{command}'.")
        show_help()
        sys.exit(1)

if __name__ == "__main__":
    main()