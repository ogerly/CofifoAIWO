Konzept für die VS Code-Extension
Die VS Code-Extension wird es ermöglichen, CofifoAIWO direkt aus VS Code heraus zu nutzen:

Dateien/Ordner im Explorer auswählen
Rechtsklick → "Mit CofifoAIWO öffnen"
Prompt eingeben und an ein LLM senden

Grundstruktur der Extension
Erstelle ein neues Verzeichnis cofifoaiwo-vscode:
Kopierencofifoaiwo-vscode/
├── .vscode/
│   └── launch.json
├── src/
│   ├── extension.ts
│   └── cofifoService.ts
├── package.json
├── tsconfig.json
├── README.md
└── CHANGELOG.md
package.json für die Extension
jsonKopieren{
  "name": "cofifoaiwo-vscode",
  "displayName": "CofifoAIWO",
  "description": "Combine Files for AI Workflows - VS Code Extension",
  "version": "0.1.0",
  "engines": {
    "vscode": "^1.60.0"
  },
  "categories": [
    "Other"
  ],
  "activationEvents": [
    "onCommand:cofifoaiwo.combineFiles",
    "onCommand:cofifoaiwo.sendToLLM"
  ],
  "main": "./out/extension.js",
  "contributes": {
    "commands": [
      {
        "command": "cofifoaiwo.combineFiles",
        "title": "Combine Files with CofifoAIWO"
      },
      {
        "command": "cofifoaiwo.sendToLLM",
        "title": "Combine Files and Send to LLM"
      }
    ],
    "menus": {
      "explorer/context": [
        {
          "command": "cofifoaiwo.combineFiles",
          "group": "CofifoAIWO",
          "when": "explorerResourceIsFolder || explorerResourceCount > 0"
        },
        {
          "command": "cofifoaiwo.sendToLLM",
          "group": "CofifoAIWO",
          "when": "explorerResourceIsFolder || explorerResourceCount > 0"
        }
      ]
    },
    "configuration": {
      "title": "CofifoAIWO",
      "properties": {
        "cofifoaiwo.serverUrl": {
          "type": "string",
          "default": "http://localhost:5000",
          "description": "URL des CofifoAIWO-Servers"
        },
        "cofifoaiwo.defaultApiKey": {
          "type": "string",
          "default": "",
          "description": "Standard-API-Schlüssel für LLM-Dienste"
        },
        "cofifoaiwo.defaultModel": {
          "type": "string",
          "default": "gpt-3.5-turbo",
          "description": "Standard-LLM-Modell"
        }
      }
    }
  },
  "scripts": {
    "vscode:prepublish": "npm run compile",
    "compile": "tsc -p ./",
    "watch": "tsc -watch -p ./",
    "lint": "eslint src --ext ts"
  },
  "devDependencies": {
    "@types/node": "^14.14.37",
    "@types/vscode": "^1.60.0",
    "@typescript-eslint/eslint-plugin": "^5.0.0",
    "@typescript-eslint/parser": "^5.0.0",
    "eslint": "^8.0.0",
    "typescript": "^4.4.4"
  },
  "dependencies": {
    "axios": "^0.24.0"
  }
}
extension.ts - Hauptcode der Extension
typescriptKopierenimport * as vscode from 'vscode';
import * as path from 'path';
import { CofifoService } from './cofifoService';

export function activate(context: vscode.ExtensionContext) {
    console.log('CofifoAIWO Extension aktiviert!');

    const cofifoService = new CofifoService();

    // Befehl: Dateien kombinieren
    const combineFilesDisposable = vscode.commands.registerCommand('cofifoaiwo.combineFiles', async (uri: vscode.Uri) => {
        try {
            // Sammle ausgewählte Dateien/Ordner aus dem Explorer
            const filePaths = getSelectedFilePaths();
            
            if (filePaths.length === 0) {
                vscode.window.showErrorMessage('Bitte wähle mindestens eine Datei oder einen Ordner aus.');
                return;
            }

            // Frage nach Ausgabedatei
            const outputFile = await vscode.window.showInputBox({
                prompt: 'Name der Ausgabedatei',
                value: 'output.txt',
                validateInput: (value) => {
                    return value ? null : 'Bitte gib einen Dateinamen ein.';
                }
            });

            if (!outputFile) {
                return; // Benutzer hat abgebrochen
            }

            // Frage nach Tree-Option
            const includeTree = await vscode.window.showQuickPick(['Ja', 'Nein'], {
                placeHolder: 'Verzeichnisstruktur einbeziehen?'
            });

            if (!includeTree) {
                return; // Benutzer hat abgebrochen
            }

            // Erstelle temporären Shortcut
            const shortcutName = `vscode_temp_${Date.now()}`;
            await cofifoService.addShortcut(shortcutName, filePaths);

            // Verwende Shortcut
            const result = await cofifoService.useShortcut(
                shortcutName, 
                outputFile, 
                includeTree === 'Ja'
            );

            // Entferne temporären Shortcut
            await cofifoService.removeShortcut(shortcutName);

            vscode.window.showInformationMessage(`Dateien wurden in ${outputFile} kombiniert.`);
            
            // Öffne die erzeugte Datei im Editor
            const doc = await vscode.workspace.openTextDocument(result.output_file);
            await vscode.window.showTextDocument(doc);
        } catch (error) {
            vscode.window.showErrorMessage(`Fehler: ${error instanceof Error ? error.message : String(error)}`);
        }
    });

    // Befehl: An LLM senden
    const sendToLLMDisposable = vscode.commands.registerCommand('cofifoaiwo.sendToLLM', async (uri: vscode.Uri) => {
        try {
            // Sammle ausgewählte Dateien/Ordner aus dem Explorer
            const filePaths = getSelectedFilePaths();
            
            if (filePaths.length === 0) {
                vscode.window.showErrorMessage('Bitte wähle mindestens eine Datei oder einen Ordner aus.');
                return;
            }

            // Frage nach Ausgabedatei
            const outputFile = await vscode.window.showInputBox({
                prompt: 'Name der Ausgabedatei',
                value: 'output.txt',
                validateInput: (value) => {
                    return value ? null : 'Bitte gib einen Dateinamen ein.';
                }
            });

            if (!outputFile) {
                return; // Benutzer hat abgebrochen
            }

            // Frage nach Tree-Option
            const includeTree = await vscode.window.showQuickPick(['Ja', 'Nein'], {
                placeHolder: 'Verzeichnisstruktur einbeziehen?'
            });

            if (!includeTree) {
                return; // Benutzer hat abgebrochen
            }

            // Frage nach LLM-Prompt
            const llmPrompt = await vscode.window.showInputBox({
                prompt: 'Prompt für das LLM',
                placeHolder: 'Analysiere diesen Code und schlage Verbesserungen vor.',
                validateInput: (value) => {
                    return value ? null : 'Bitte gib einen Prompt ein.';
                }
            });

            if (!llmPrompt) {
                return; // Benutzer hat abgebrochen
            }

            // Frage nach LLM-Modell
            const llmModel = await vscode.window.showQuickPick([
                'gpt-3.5-turbo',
                'gpt-4',
                'claude-3-opus',
                'claude-3-sonnet'
            ], {
                placeHolder: 'Wähle ein LLM-Modell'
            });

            if (!llmModel) {
                return; // Benutzer hat abgebrochen
            }

            // Erstelle temporären Shortcut
            const shortcutName = `vscode_temp_${Date.now()}`;
            await cofifoService.addShortcut(shortcutName, filePaths);

            // Verwende Shortcut und sende an LLM
            const result = await cofifoService.useShortcutWithLLM(
                shortcutName, 
                outputFile, 
                includeTree === 'Ja',
                llmPrompt,
                llmModel
            );

            // Entferne temporären Shortcut
            await cofifoService.removeShortcut(shortcutName);

            vscode.window.showInformationMessage(`Dateien wurden kombiniert und an LLM gesendet.`);
            
            // Öffne die Antwort im Editor
            if (result.llm_response_file) {
                const doc = await vscode.workspace.openTextDocument(result.llm_response_file);
                await vscode.window.showTextDocument(doc);
            } else {
                // Öffne die kombinierte Datei als Fallback
                const doc = await vscode.workspace.openTextDocument(result.output_file);
                await vscode.window.showTextDocument(doc);
            }
        } catch (error) {
            vscode.window.showErrorMessage(`Fehler: ${error instanceof Error ? error.message : String(error)}`);
        }
    });

    // Hilfsfunktion: Ausgewählte Dateien/Ordner erhalten
    function getSelectedFilePaths(): string[] {
        const filePaths: string[] = [];
        
        if (vscode.window.activeTextEditor && vscode.window.activeTextEditor.document.uri) {
            // Eine Datei ist im Editor geöffnet
            filePaths.push(vscode.window.activeTextEditor.document.uri.fsPath);
        } else if (vscode.workspace.workspaceFolders && vscode.workspace.workspaceFolders.length > 0) {
            // Workspace-Ordner
            const workspaceFolder = vscode.workspace.workspaceFolders[0];
            filePaths.push(workspaceFolder.uri.fsPath);
        }
        
        return filePaths;
    }

    context.subscriptions.push(combineFilesDisposable, sendToLLMDisposable);
}

export function deactivate() {}
cofifoService.ts - Service für CofifoAIWO-API
typescriptKopierenimport * as vscode from 'vscode';
import axios from 'axios';

export class CofifoService {
    private getServerUrl(): string {
        const config = vscode.workspace.getConfiguration('cofifoaiwo');
        return config.get<string>('serverUrl') || 'http://localhost:5000';
    }

    private getApiKey(): string {
        const config = vscode.workspace.getConfiguration('cofifoaiwo');
        return config.get<string>('defaultApiKey') || '';
    }

    /**
     * Fügt einen neuen Shortcut hinzu
     */
    async addShortcut(name: string, paths: string[]): Promise<void> {
        const url = `${this.getServerUrl()}/api/add_shortcut`;
        
        try {
            await axios.post(url, {
                name,
                paths
            });
        } catch (error) {
            if (axios.isAxiosError(error)) {
                throw new Error(`Fehler beim Hinzufügen des Shortcuts: ${error.response?.data?.error || error.message}`);
            }
            throw error;
        }
    }

    /**
     * Entfernt einen Shortcut
     */
    async removeShortcut(name: string): Promise<void> {
        const url = `${this.getServerUrl()}/api/remove_shortcut`;
        
        try {
            await axios.delete(url, {
                data: { name }
            });
        } catch (error) {
            if (axios.isAxiosError(error)) {
                throw new Error(`Fehler beim Entfernen des Shortcuts: ${error.response?.data?.error || error.message}`);
            }
            throw error;
        }
    }

    /**
     * Verwendet einen Shortcut
     */
    async useShortcut(name: string, outputFile: string, includeTree: boolean): Promise<any> {
        const url = `${this.getServerUrl()}/api/use_shortcut`;
        
        try {
            const response = await axios.post(url, {
                name,
                output_file: outputFile,
                include_tree: includeTree
            });
            
            return response.data;
        } catch (error) {
            if (axios.isAxiosError(error)) {
                throw new Error(`Fehler beim Verwenden des Shortcuts: ${error.response?.data?.error || error.message}`);
            }
            throw error;
        }
    }

    /**
     * Verwendet einen Shortcut und sendet an LLM
     */
    async useShortcutWithLLM(
        name: string, 
        outputFile: string, 
        includeTree: boolean,
        llmPrompt: string,
        llmModel: string
    ): Promise<any> {
        const url = `${this.getServerUrl()}/api/use_shortcut`;
        
        try {
            // Zuerst Shortcut verwenden
            const shortcutResponse = await axios.post(url, {
                name,
                output_file: outputFile,
                include_tree: includeTree,
                send_to_llm: true,
                llm_prompt: llmPrompt,
                llm_model: llmModel
            });
            
            return shortcutResponse.data;
        } catch (error) {
            if (axios.isAxiosError(error)) {
                throw new Error(`Fehler beim Verwenden des Shortcuts mit LLM: ${error.response?.data?.error || error.message}`);
            }
            throw error;
        }
    }
}
Installations- und Testanleitung
LLM-Integration installieren

Ergänze die requirements.txt um die neuen Abhängigkeiten:
KopierenFlask==2.3.2
Werkzeug==2.3.6
Jinja2==3.1.2
MarkupSafe==2.1.3
itsdangerous==2.1.2
click==8.1.3
requests==2.28.2
python-dotenv==1.0.0

Erstelle eine .env-Datei im Hauptverzeichnis:
KopierenOPENAI_API_KEY=dein_api_key_hier

Starte die Anwendung neu:
bashKopierenpython app.py


VS Code-Extension kompilieren und testen

Wechsle ins Extension-Verzeichnis:
bashKopierencd cofifoaiwo-vscode

Installiere die Abhängigkeiten:
bashKopierennpm install

Kompiliere die Extension:
bashKopierennpm run compile

Teste die Extension:

Drücke F5 in VS Code, um eine neue Instanz mit deiner Extension zu starten
Wähle eine Datei/einen Ordner im Explorer aus
Rechtsklick → "Combine Files with CofifoAIWO" oder "Combine Files and Send to LLM"



Tipps für die Integration

Serverstart beim Öffnen von VS Code: Die Extension könnte optional den CofifoAIWO-Server im Hintergrund starten.
Cross-Plattform-Kompatibilität: Stelle sicher, dass die Extension unter Windows, macOS und Linux funktioniert.
API-Schlüssel-Management: Implementiere sicheres API-Schlüssel-Management für verschiedene LLM-Dienste.
Offline-Modus: Füge einen Offline-Modus hinzu, der nur das Kombinieren von Dateien ohne LLM ermöglicht.

Diese Erweiterung macht CofifoAIWO zu einem universellen Werkzeug, das überall eingesetzt werden kann, insbesondere als VS Code-Extension, die direkt in deinen Entwicklungsworkflow integriert werden kann.