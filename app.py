from flask import Flask, request, jsonify, send_file, send_from_directory
import os
import sys
import importlib.util
import json
from pathlib import Path

# Pfad zum Basis-Verzeichnis (wo sich app.py befindet)
BASE_DIR = Path(__file__).resolve().parent

# Erstelle Flask-App 
app = Flask(__name__, static_folder='static', static_url_path='')

# Importiere das combine_files.py Skript als Modul, falls es existiert
try:
    spec = importlib.util.spec_from_file_location("combine_files", 
                                                BASE_DIR / "combine_files.py")
    combine_files = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(combine_files)
except Exception as e:
    print(f"Warnung: Konnte combine_files.py nicht importieren: {e}")
    
    # Dummy-Funktionen als Fallback
    class DummyCombineFiles:
        def add_shortcut(self, name, paths):
            return {"error": "combine_files.py konnte nicht geladen werden"}
        
        def remove_shortcut(self, name):
            return {"error": "combine_files.py konnte nicht geladen werden"}
        
        def list_shortcuts(self):
            return {"error": "combine_files.py konnte nicht geladen werden"}
        
        def use_shortcut(self, name, output_file, include_tree=False):
            return {"error": "combine_files.py konnte nicht geladen werden"}
    
    combine_files = DummyCombineFiles()

# Hilfsfunktion zum Laden der Shortcuts
def load_shortcuts():
    """Lädt die Shortcuts aus der JSON-Datei."""
    shortcuts_file = BASE_DIR / "shortcuts.json"
    if shortcuts_file.exists():
        with open(shortcuts_file, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {}

# Stelle sicher, dass shortcuts.json existiert
def ensure_shortcuts_file():
    shortcuts_file = BASE_DIR / "shortcuts.json"
    if not shortcuts_file.exists():
        with open(shortcuts_file, 'w', encoding='utf-8') as file:
            json.dump({}, file)

# Erstelle shortcuts.json, falls sie nicht existiert
ensure_shortcuts_file()

@app.route('/')
def index():
    """Serviert die Startseite."""
    return send_from_directory('static', 'index.html')

@app.route('/shortcuts')
def shortcuts_page():
    """Serviert die Shortcuts-Seite."""
    return send_from_directory('static', 'shortcuts.html')

@app.route('/browser')
def browser_page():
    """Serviert die Browser-Seite."""
    return send_from_directory('static', 'browser.html')

@app.route('/api/list_shortcuts', methods=['GET'])
def api_list_shortcuts():
    """API-Endpunkt zum Auflisten aller Shortcuts."""
    try:
        shortcuts = load_shortcuts()
        return jsonify(shortcuts)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/add_shortcut', methods=['POST'])
def api_add_shortcut():
    """API-Endpunkt zum Hinzufügen eines Shortcuts."""
    data = request.json
    
    if not data or 'name' not in data or 'paths' not in data:
        return jsonify({'error': 'Ungültige Anfrage: Name und Pfade erforderlich'}), 400
    
    name = data['name']
    paths = data['paths']
    
    try:
        # Lade aktuelle Shortcuts
        shortcuts = load_shortcuts()
        # Füge neuen Shortcut hinzu
        shortcuts[name] = paths
        # Speichere Shortcuts
        with open(BASE_DIR / "shortcuts.json", 'w', encoding='utf-8') as file:
            json.dump(shortcuts, file, indent=4)
        
        return jsonify({'success': True, 'message': f"Shortcut '{name}' wurde hinzugefügt."})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/remove_shortcut', methods=['DELETE'])
def api_remove_shortcut():
    """API-Endpunkt zum Entfernen eines Shortcuts."""
    data = request.json
    
    if not data or 'name' not in data:
        return jsonify({'error': 'Ungültige Anfrage: Name erforderlich'}), 400
    
    name = data['name']
    
    try:
        # Lade aktuelle Shortcuts
        shortcuts = load_shortcuts()
        
        # Prüfe, ob Shortcut existiert
        if name not in shortcuts:
            return jsonify({'error': f"Shortcut '{name}' existiert nicht."}), 404
        
        # Entferne Shortcut
        del shortcuts[name]
        
        # Speichere Shortcuts
        with open(BASE_DIR / "shortcuts.json", 'w', encoding='utf-8') as file:
            json.dump(shortcuts, file, indent=4)
        
        return jsonify({'success': True, 'message': f"Shortcut '{name}' wurde entfernt."})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/use_shortcut', methods=['POST'])
def api_use_shortcut():
    """API-Endpunkt zum Verwenden eines Shortcuts."""
    data = request.json
    
    if not data or 'name' not in data or 'output_file' not in data:
        return jsonify({'error': 'Ungültige Anfrage: Name und Ausgabedatei erforderlich'}), 400
    
    name = data['name']
    output_file = data['output_file']
    include_tree = data.get('include_tree', False)
    
    try:
        # Lade Shortcuts
        shortcuts = load_shortcuts()
        
        # Prüfe, ob Shortcut existiert
        if name not in shortcuts:
            return jsonify({'error': f"Shortcut '{name}' existiert nicht."}), 404
        
        paths = shortcuts[name]
        
        # Erstelle Ausgabedatei
        if hasattr(combine_files, 'use_shortcut'):
            combine_files.use_shortcut(name, output_file, include_tree)
        else:
            # Fallback-Implementierung, falls combine_files.py nicht verfügbar ist
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(f"=== Shortcuts '{name}' verwendet ===\n\n")
                file.write(f"Pfade:\n")
                for path in paths:
                    file.write(f"- {path}\n")
                    if os.path.isfile(path):
                        try:
                            with open(path, 'r', encoding='utf-8') as f:
                                content = f.read()
                            file.write(f"\n=== Datei: {path} ===\n")
                            file.write(content)
                            file.write("\n\n")
                        except Exception as e:
                            file.write(f"\nFehler beim Lesen der Datei: {str(e)}\n\n")
        
        # Erstelle absoluten Pfad zur Ausgabedatei
        abs_output_path = os.path.abspath(output_file)
        return jsonify({
            'success': True, 
            'message': f"Shortcut '{name}' wurde verwendet und in '{output_file}' gespeichert.",
            'output_file': abs_output_path
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/browse', methods=['GET'])
def api_browse():
    """API-Endpunkt zum Durchsuchen von Verzeichnissen."""
    path = request.args.get('path', os.getcwd())
    
    # Entferne die Sicherheitseinschränkung, die das Browsen auf base_path beschränkt
    # base_path = os.path.abspath(os.getcwd())
    # requested_path = os.path.abspath(path)
    # if not requested_path.startswith(base_path) and path != '/':
    #     path = base_path
    
    if not os.path.exists(path):
        return jsonify({'error': f"Pfad '{path}' existiert nicht."}), 404
    
    try:
        if os.path.isdir(path):
            # Zeige Inhalt des Verzeichnisses
            entries = []
            for entry in os.listdir(path):
                # Ignoriere versteckte Dateien/Ordner
                if entry.startswith('.'):
                    continue
                
                full_path = os.path.join(path, entry)
                entry_type = "directory" if os.path.isdir(full_path) else "file"
                entries.append({
                    'name': entry,
                    'path': full_path,
                    'type': entry_type
                })
            return jsonify({
                'path': path,
                'entries': entries
            })
        else:
            # Zeige Informationen zur Datei
            return jsonify({
                'path': path,
                'name': os.path.basename(path),
                'type': "file",
                'size': os.path.getsize(path)
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    


    

@app.route('/api/download/<path:filename>', methods=['GET'])
def download_file(filename):
    """API-Endpunkt zum Herunterladen einer Datei."""
    try:
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)