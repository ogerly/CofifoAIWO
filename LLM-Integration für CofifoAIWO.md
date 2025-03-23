LLM-Integration für CofifoAIWO
Konzept
Wir können CofifoAIWO um eine direkte LLM-Integration erweitern, sodass die generierte Textdatei automatisch an ein LLM-Modell gesendet wird und die Antwort angezeigt oder gespeichert wird. Das Vorhaben besteht aus zwei Teilen:

LLM-Anbindung im Backend
VS Code Extension

Teil 1: LLM-Integration
Erweiterung der Backend-Komponente (app.py)
pythonKopieren# Neue Abhängigkeiten für LLM-Integration
import requests
import os
from dotenv import load_dotenv

# Lade Umgebungsvariablen
load_dotenv()

# Füge neue Endpunkte hinzu
@app.route('/api/send_to_llm', methods=['POST'])
def api_send_to_llm():
    """API-Endpunkt zum Senden von Inhalten an ein LLM."""
    data = request.json
    
    if not data or 'content' not in data or 'prompt' not in data:
        return jsonify({'error': 'Ungültige Anfrage: Inhalt und Prompt erforderlich'}), 400
    
    content = data['content']
    prompt = data['prompt']
    model = data.get('model', 'gpt-3.5-turbo')  # Standardmodell
    
    try:
        # LLM-Anfrage senden
        response = send_to_llm(content, prompt, model)
        return jsonify({'success': True, 'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def send_to_llm(content, prompt, model="gpt-3.5-turbo"):
    """Sendet Inhalt und Prompt an ein LLM und gibt die Antwort zurück."""
    # API-Schlüssel aus Umgebungsvariable laden
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Kein API-Schlüssel gefunden. Bitte setze die OPENAI_API_KEY Umgebungsvariable.")
    
    # Wir unterstützen hier OpenAI, kann aber leicht für andere Anbieter erweitert werden
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Anfrage vorbereiten
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Du bist ein hilfreicher Assistent."},
            {"role": "user", "content": f"{prompt}\n\nHier ist der Quellcode/Inhalt:\n\n{content}"}
        ],
        "temperature": 0.7
    }
    
    # Anfrage senden
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=payload
    )
    
    # Fehlerbehandlung
    if response.status_code != 200:
        raise Exception(f"Fehler bei der API-Anfrage: {response.text}")
    
    # Antwort extrahieren
    result = response.json()
    return result["choices"][0]["message"]["content"]
Erweiterung der use_shortcut-Funktion in combine_files.py
pythonKopierendef use_shortcut(name, output_file, include_tree=False, send_to_llm=False, prompt="", model="gpt-3.5-turbo"):
    """Verwendet einen Shortcut, um Dateien zu kombinieren und optional an ein LLM zu senden."""
    # Bestehende Funktionalität...
    
    # Wenn send_to_llm aktiviert ist
    if send_to_llm:
        # Lese die generierte Datei
        with open(output_file, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Sende an LLM
        from app import send_to_llm as llm_sender
        response = llm_sender(content, prompt, model)
        
        # Speichere die Antwort
        llm_response_file = f"{os.path.splitext(output_file)[0]}_llm_response.txt"
        with open(llm_response_file, 'w', encoding='utf-8') as file:
            file.write(response)
        
        print(f"LLM-Antwort wurde in {llm_response_file} gespeichert.")
        return llm_response_file
Frontend-Erweiterung für die LLM-Integration (browser.html)
Füge diesen Abschnitt zum Modal für die Generierung der Textdatei hinzu:
htmlKopieren<div class="form-group">
    <div class="checkbox">
        <input type="checkbox" id="sendToLLM">
        <label for="sendToLLM">An LLM senden</label>
    </div>
</div>

<div id="llmOptions" style="display: none;">
    <div class="form-group">
        <label for="llmPrompt">Prompt für LLM:</label>
        <textarea 
            id="llmPrompt" 
            class="form-control" 
            rows="3" 
            placeholder="Gib deinen Prompt für das LLM ein. Beispiel: 'Analysiere diesen Code und schlage Verbesserungen vor.'"
        ></textarea>
    </div>
    
    <div class="form-group">
        <label for="llmModel">LLM-Modell:</label>
        <select id="llmModel" class="form-control">
            <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
            <option value="gpt-4">GPT-4</option>
            <option value="claude-3-opus">Claude 3 Opus</option>
            <option value="claude-3-sonnet">Claude 3 Sonnet</option>
        </select>
    </div>
</div>
Füge entsprechendes JavaScript hinzu:
javascriptKopieren// LLM-Checkbox Events
document.getElementById('sendToLLM').addEventListener('change', function() {
    document.getElementById('llmOptions').style.display = this.checked ? 'block' : 'none';
});

// Modifiziere die generateTextFile-Funktion
async function generateTextFile(event) {
    // ...bestehender Code...
    
    // LLM-Optionen einbeziehen
    const sendToLLM = document.getElementById('sendToLLM').checked;
    let llmData = null;
    
    if (sendToLLM) {
        const llmPrompt = document.getElementById('llmPrompt').value;
        const llmModel = document.getElementById('llmModel').value;
        
        if (!llmPrompt) {
            showNotification('danger', 'Bitte gib einen Prompt für das LLM ein.');
            return;
        }
        
        // Füge LLM-Parameter hinzu
        requestData.send_to_llm = true;
        requestData.llm_prompt = llmPrompt;
        requestData.llm_model = llmModel;
    }
    
    // ...Rest des Codes...
    
    // Nach erfolgreicher Generierung: Bei LLM-Nutzung zusätzliche Informationen anzeigen
    if (sendToLLM && result.llm_response_file) {
        // Zeige Download-Link für LLM-Antwort
        const llmDownloadLink = document.createElement('a');
        llmDownloadLink.href = `/api/download/${encodeURIComponent(result.llm_response_file)}`;
        llmDownloadLink.className = 'btn';
        llmDownloadLink.textContent = 'LLM-Antwort herunterladen';
        llmDownloadLink.download = true;
        
        // Füge den Link zum Modal hinzu
        document.querySelector('#download-modal .modal-body').appendChild(document.createElement('br'));
        document.querySelector('#download-modal .modal-body').appendChild(llmDownloadLink);
    }
}
