# KanbanX MCP Server 📋

> Ein vollständiger Model Context Protocol (MCP) Server für KanbanX - Dein persönliches Kanban Task Management System mit erweiterten Features wie Subtasks, Notizen und Code-Clips.

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-2024--11--05-green.svg)](https://modelcontextprotocol.io/)
[![Windows](https://img.shields.io/badge/platform-Windows-blue.svg)](https://www.microsoft.com/windows)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 🌟 Features

### 📊 Kanban Board Management
- **Drei-Spalten-System**: TODO, DOING, DONE
- **Drag-and-Drop-ähnlich**: Verschiebe Tasks zwischen Spalten
- **Eindeutige IDs**: Jede Task erhält eine unveränderliche ID
- **Timestamps**: Automatische Zeitstempel für alle Aktionen

### 📝 Erweiterte Task-Features
- **Hierarchische Subtasks**: Erstelle Unteraufgaben mit eigenem Status
- **Detaillierte Notizen**: Füge mehrzeilige Notizen zu Tasks hinzu
- **Code Clips**: Speichere Code-Schnipsel, Links und wichtige Informationen
- **Rich Text Support**: Unicode-Support für Emojis und Sonderzeichen

### 🔌 MCP Integration
- **Vollständige MCP 2024-11-05 Kompatibilität**
- **RESTful-ähnliche Tools**: Intuitive Tool-Namen und Parameter
- **Ressourcen-Zugriff**: Direkter JSON-Zugriff auf das komplette Board
- **Fehlerbehandlung**: Robuste Fehlerbehandlung und Logging

### 💾 Daten-Persistierung
- **JSON-basiert**: Einfach lesbare und editierbare Datenspeicherung
- **Automatische Backups**: Sichere Datenspeicherung
- **Portable**: Alle Daten in einer einzigen JSON-Datei
- **Versionskontrolle-freundlich**: Git-kompatible Datenstruktur

## 🚀 Schnellstart (Windows)

### Voraussetzungen
- **Windows 10/11** (PowerShell 5.1+ oder PowerShell 7+)
- **Python 3.8+** ([Download hier](https://www.python.org/downloads/))
- **MCP-kompatibler Client** (Claude Desktop, Gemini CLI, etc.)

### ⚡ Automatische Installation

1. **Repository klonen oder herunterladen**
   ```powershell
   git clone https://github.com/yourusername/kanbanx-mcp.git
   cd kanbanx-mcp
   ```

2. **Setup-Script ausführen**
   ```powershell
   .\setup.ps1
   ```

3. **Pfad zur Server-Datei eingeben** (ohne Anführungszeichen!)
   ```
   Pfad: C:\path\to\kanbanx_mcp_server.py
   ```

4. **MCP Client neu starten** und testen:
   ```
   list_board()
   ```

### 🔧 Manuelle Installation

<details>
<summary>Klicke hier für detaillierte manuelle Installation</summary>

#### Schritt 1: Python und Dependencies installieren

```powershell
# Python Version prüfen
python --version

# MCP SDK installieren
pip install mcp
```

#### Schritt 2: Server-Datei erstellen

Erstelle `kanbanx_mcp_server.py` mit dem bereitgestellten Code im Repository.

#### Schritt 3: Konfiguration erstellen

```powershell
# Konfigurationsverzeichnis erstellen
$configDir = "$env:APPDATA\Claude"
New-Item -ItemType Directory -Path $configDir -Force

# Konfigurationsdatei erstellen
$config = @{
    mcpServers = @{
        kanbanx = @{
            command = "python"
            args = @("C:\full\path\to\kanbanx_mcp_server.py")
            env = @{}
        }
    }
}

$config | ConvertTo-Json -Depth 10 | Out-File -FilePath "$configDir\claude_desktop_config.json" -Encoding UTF8
```

#### Schritt 4: Server testen

```powershell
# Server direkt testen
python kanbanx_mcp_server.py

# Konfiguration prüfen
Get-Content "$env:APPDATA\Claude\claude_desktop_config.json"
```

</details>

## 📖 Verfügbare Tools

### 🆕 Task Management

#### `add_task`
Erstellt eine neue Aufgabe in der gewünschten Spalte.

**Parameter:**
- `column` (string, required): `"todo"`, `"doing"`, oder `"done"`
- `title` (string, required): Titel der Aufgabe
- `note` (string, optional): Zusätzliche Beschreibung

**Beispiel:**
```javascript
add_task({
  column: "todo",
  title: "Website entwickeln",
  note: "Responsive React-App mit modernem Design"
})
```

#### `move_task`
Verschiebt eine Aufgabe zwischen Spalten.

**Parameter:**
- `task_id` (string, required): ID der Aufgabe (z.B. `"ID-abc123"`)
- `target_column` (string, required): Zielspalte

**Beispiel:**
```javascript
move_task({
  task_id: "ID-abc123",
  target_column: "doing"
})
```

#### `delete_task`
Löscht eine Aufgabe permanent.

**Parameter:**
- `task_id` (string, required): ID der zu löschenden Aufgabe

**Beispiel:**
```javascript
delete_task({
  task_id: "ID-abc123"
})
```

### 📋 Subtask Management

#### `add_subtask`
Fügt eine Unteraufgabe zu einer bestehenden Aufgabe hinzu.

**Parameter:**
- `task_id` (string, required): ID der Hauptaufgabe
- `text` (string, required): Beschreibung der Unteraufgabe

**Beispiel:**
```javascript
add_subtask({
  task_id: "ID-abc123",
  text: "Navigation komponente erstellen"
})
```

#### `complete_subtask`
Markiert eine Unteraufgabe als erledigt.

**Parameter:**
- `task_id` (string, required): ID der Hauptaufgabe
- `subtask_id` (string, required): ID der Unteraufgabe

**Beispiel:**
```javascript
complete_subtask({
  task_id: "ID-abc123",
  subtask_id: "ID-def456"
})
```

### 📝 Content Management

#### `add_note`
Fügt eine Notiz zu einer Aufgabe hinzu oder erweitert bestehende Notizen.

**Parameter:**
- `task_id` (string, required): ID der Aufgabe
- `note` (string, required): Notiztext (unterstützt Mehrzeilen)

**Beispiel:**
```javascript
add_note({
  task_id: "ID-abc123",
  note: "Wichtig: Mobile-First Ansatz verwenden\nFarben: #3498db, #2ecc71"
})
```

#### `add_clip`
Speichert Code-Schnipsel, Links oder wichtige Informationen zu einer Aufgabe.

**Parameter:**
- `task_id` (string, required): ID der Aufgabe
- `snippet` (string, required): Code, Link oder Information

**Beispiel:**
```javascript
add_clip({
  task_id: "ID-abc123",
  snippet: "npm install react-router-dom @types/react-router-dom"
})
```

### 👁️ Viewing Tools

#### `list_board`
Zeigt das komplette Kanban Board an.

**Parameter:**
- `format` (string, optional): `"detailed"` (Standard) oder `"summary"`

**Beispiel:**
```javascript
// Detaillierte Ansicht
list_board({ format: "detailed" })

// Zusammenfassung
list_board({ format: "summary" })
```

## 🔧 Konfiguration

### MCP Client-spezifische Konfiguration

<details>
<summary>Claude Desktop</summary>

**Konfigurationsdatei:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "kanbanx": {
      "command": "python",
      "args": ["C:\\path\\to\\kanbanx_mcp_server.py"],
      "env": {}
    }
  }
}
```

</details>

<details>
<summary>Gemini CLI</summary>

**Installiere Gemini CLI:**
```powershell
npm install -g @google/gemini-cli
```

**Konfiguration:** Siehe [Gemini CLI MCP Dokumentation](https://github.com/google/gemini-cli)

</details>

<details>
<summary>Custom MCP Clients</summary>

Für eigene MCP Clients verwende die Standard MCP 2024-11-05 Spezifikation:

```python
import asyncio
from mcp.client import ClientSession
from mcp.client.stdio import stdio_client

async def main():
    async with stdio_client("python", "kanbanx_mcp_server.py") as streams:
        async with ClientSession(streams[0], streams[1]) as session:
            await session.initialize()
            
            # Tools verwenden
            result = await session.call_tool("list_board", {})
            print(result)

asyncio.run(main())
```

</details>

### Erweiterte Konfiguration

#### Umgebungsvariablen

```powershell
# Datenverzeichnis anpassen
$env:KANBANX_DATA_DIR = "C:\MyProjects\kanban-data"

# Debug-Modus aktivieren
$env:KANBANX_DEBUG = "true"
```

#### Mehrere Board-Instanzen

```json
{
  "mcpServers": {
    "kanbanx-work": {
      "command": "python",
      "args": ["C:\\path\\to\\kanbanx_mcp_server.py"],
      "env": {
        "KANBANX_DATA_FILE": "work_board.json"
      }
    },
    "kanbanx-personal": {
      "command": "python",
      "args": ["C:\\path\\to\\kanbanx_mcp_server.py"],
      "env": {
        "KANBANX_DATA_FILE": "personal_board.json"
      }
    }
  }
}
```

## 📊 Ressourcen

### `kanbanx://board`
Direkter Zugriff auf das komplette Board als JSON.

**Verwendung:**
```javascript
// Board-Daten abrufen
const boardData = await client.readResource("kanbanx://board");
console.log(JSON.parse(boardData));
```

**Datenstruktur:**
```json
{
  "todo": [
    {
      "id": "ID-abc123",
      "title": "Website entwickeln",
      "note": "Responsive Design mit React",
      "subs": {
        "ID-def456": {
          "text": "Navigation erstellen",
          "done": false
        }
      },
      "clips": [
        {
          "ts": "2024-01-15T10:30:00",
          "text": "npm install react"
        }
      ],
      "created": "2024-01-15T09:00:00"
    }
  ],
  "doing": [],
  "done": []
}
```

## 🎯 Anwendungsbeispiele

### Beispiel 1: Neues Projekt Setup

```javascript
// 1. Hauptaufgabe erstellen
add_task({
  column: "todo",
  title: "E-Commerce Website",
  note: "Online-Shop mit React und Node.js"
})

// 2. Subtasks hinzufügen
add_subtask({
  task_id: "ID-abc123",
  text: "Database Schema entwerfen"
})

add_subtask({
  task_id: "ID-abc123", 
  text: "API Endpoints implementieren"
})

add_subtask({
  task_id: "ID-abc123",
  text: "Frontend Komponenten erstellen"
})

// 3. Wichtige Links und Commands speichern
add_clip({
  task_id: "ID-abc123",
  snippet: "Database: PostgreSQL 14, Redis für Caching"
})

add_clip({
  task_id: "ID-abc123",
  snippet: "git clone https://github.com/project/ecommerce-template"
})
```

### Beispiel 2: Sprint Planning

```javascript
// Sprint Board übersicht
list_board({ format: "summary" })

// Task in Bearbeitung nehmen
move_task({
  task_id: "ID-abc123",
  target_column: "doing"
})

// Progress-Update
add_note({
  task_id: "ID-abc123",
  note: "Sprint 1 - Tag 3: Database Schema 80% fertig"
})

// Subtask abhaken
complete_subtask({
  task_id: "ID-abc123",
  subtask_id: "ID-def456"
})
```

### Beispiel 3: Bug Tracking

```javascript
// Bug-Report erstellen
add_task({
  column: "todo",
  title: "🐛 Login-Validation Bug",
  note: "Users können sich mit leeren Feldern einloggen"
})

// Investigation Details
add_clip({
  task_id: "ID-bug001",
  snippet: "Reproduktion: Chrome 120, leere Email + Passwort → Login successful"
})

add_clip({
  task_id: "ID-bug001", 
  snippet: "Betroffene Datei: /src/components/LoginForm.tsx Zeile 45"
})

// Fix-Tasks hinzufügen
add_subtask({
  task_id: "ID-bug001",
  text: "Input validation implementieren"
})

add_subtask({
  task_id: "ID-bug001",
  text: "Unit tests für validation schreiben"
})
```

## 🛠️ Troubleshooting

### Häufige Probleme

<details>
<summary>❌ "Server nicht erreichbar"</summary>

**Lösung:**
```powershell
# 1. Python-Pfad prüfen
where python

# 2. Server direkt testen
python "C:\path\to\kanbanx_mcp_server.py"

# 3. Port-Konflikte prüfen
netstat -an | findstr :LISTENING

# 4. Neustart des MCP Clients
```

</details>

<details>
<summary>❌ "Tools nicht verfügbar"</summary>

**Lösung:**
```powershell
# 1. MCP SDK Version prüfen
pip show mcp

# 2. Konfigurationsdatei validieren
Get-Content "$env:APPDATA\Claude\claude_desktop_config.json" | ConvertFrom-Json

# 3. Server-Logs prüfen
python kanbanx_mcp_server.py 2>&1 | Tee-Object -FilePath debug.log
```

</details>

<details>
<summary>❌ "Daten gehen verloren"</summary>

**Lösung:**
```powershell
# 1. Backup-Datei suchen
Get-ChildItem -Path "." -Filter "*.json.backup" -Recurse

# 2. Manuelle Wiederherstellung
Copy-Item "kanbanx_mcp_server.json.backup" "kanbanx_mcp_server.json"

# 3. Automatische Backups einrichten (in Server-Code)
```

</details>

<details>
<summary>❌ "Unicode/Emoji Probleme"</summary>

**Lösung:**
```powershell
# PowerShell UTF-8 Encoding setzen
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$PSDefaultParameterValues['Out-File:Encoding'] = 'utf8'

# Oder PowerShell 7+ verwenden
winget install Microsoft.PowerShell
```

</details>

### Debug-Modus

Aktiviere erweiterte Logs:

```powershell
# Umgebungsvariable setzen
$env:KANBANX_DEBUG = "true"

# Server mit Logs starten
python kanbanx_mcp_server.py 2>&1 | Tee-Object debug.log
```

### Performance-Optimierung

Für große Boards (1000+ Tasks):

```json
{
  "mcpServers": {
    "kanbanx": {
      "command": "python",
      "args": ["kanbanx_mcp_server.py"],
      "env": {
        "KANBANX_CACHE_SIZE": "1000",
        "KANBANX_LAZY_LOAD": "true"
      }
    }
  }
}
```

## 🔒 Sicherheit

### Daten-Schutz
- **Lokale Speicherung**: Alle Daten bleiben auf deinem Computer
- **Keine Cloud-Verbindung**: Server kommuniziert nur über lokale Pipes
- **Backup-System**: Automatische Sicherung bei kritischen Operationen

### Access Control
```powershell
# Datei-Berechtigungen setzen (optional)
icacls "kanbanx_mcp_server.json" /grant:r "$env:USERNAME:(R,W)"
icacls "kanbanx_mcp_server.json" /remove "Everyone"
```

## 🚀 Erweiterte Features

### Custom Commands

Erweitere den Server mit eigenen Tools:

```python
@server.call_tool()
async def handle_custom_tool(name: str, arguments: dict):
    if name == "export_csv":
        # CSV Export implementieren
        return export_board_as_csv(arguments)
    
    elif name == "import_github_issues":
        # GitHub Issues importieren
        return import_from_github(arguments)
```

### Integrationen

<details>
<summary>GitHub Integration</summary>

```python
# GitHub Issues als Tasks importieren
def import_github_issues(repo_url, token):
    issues = fetch_github_issues(repo_url, token)
    for issue in issues:
        add_task({
            "column": "todo",
            "title": f"#{issue.number} {issue.title}",
            "note": issue.body
        })
```

</details>

<details>
<summary>Jira Integration</summary>

```python
# Jira Tickets synchronisieren
def sync_with_jira(jira_url, credentials):
    tickets = fetch_jira_tickets(jira_url, credentials)
    for ticket in tickets:
        update_or_create_task(ticket)
```

</details>

### Plugins

Erstelle eigene Plugin-Dateien:

```python
# plugins/time_tracking.py
class TimeTrackingPlugin:
    def start_timer(self, task_id):
        # Timer für Task starten
        pass
    
    def stop_timer(self, task_id):
        # Timer stoppen und Zeit loggen
        pass
```

## 📈 Roadmap

### Version 1.1 (geplant)
- [ ] **Time Tracking**: Eingebaute Zeiterfassung
- [ ] **Tags System**: Kategorisierung mit Tags
- [ ] **Board Templates**: Vorgefertigte Board-Layouts
- [ ] **Export Features**: PDF, CSV, Markdown Export

### Version 1.2 (geplant)
- [ ] **Team Collaboration**: Multi-User Support
- [ ] **Real-time Sync**: WebSocket-basierte Synchronisation
- [ ] **Mobile App**: React Native App
- [ ] **API Gateway**: REST API für externe Tools

### Version 2.0 (Vision)
- [ ] **AI Integration**: Automatische Task-Priorisierung
- [ ] **Analytics Dashboard**: Produktivitäts-Metriken
- [ ] **Workflow Automation**: IFTTT-ähnliche Regeln
- [ ] **Plugin Marketplace**: Community-Plugins

## 🤝 Contributing

Beiträge sind willkommen! Siehe [CONTRIBUTING.md](CONTRIBUTING.md) für Details.

### Development Setup

```powershell
# Repository forken und klonen
git clone https://github.com/yourusername/kanbanx-mcp.git
cd kanbanx-mcp

# Development-Dependencies installieren
pip install -r requirements-dev.txt

# Pre-commit hooks einrichten
pre-commit install

# Tests ausführen
python -m pytest tests/
```

### Code Style

```powershell
# Code formatieren
black kanbanx_mcp_server.py

# Linting
flake8 kanbanx_mcp_server.py

# Type checking
mypy kanbanx_mcp_server.py
```

## 📄 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert - siehe [LICENSE](LICENSE) für Details.

## 🙏 Danksagungen

- [Model Context Protocol](https://modelcontextprotocol.io/) Team
- [Anthropic](https://anthropic.com/) für Claude und MCP
- Python Community für die großartigen Tools
- Alle Contributors und Beta-Tester

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/kanbanx-mcp/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/kanbanx-mcp/discussions)
- **Email**: support@kanbanx-mcp.com
- **Discord**: [KanbanX Community](https://discord.gg/kanbanx)

---

**⭐ Star this repo wenn es dir hilft!**

Made with ❤️ for the productivity community