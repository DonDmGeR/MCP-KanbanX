#!/usr/bin/env python3
"""
KanbanX MCP Server
Ein Model Context Protocol Server für das KanbanX Kanban-Tool
"""

import asyncio
import json
import uuid
import datetime
import re
from pathlib import Path
from typing import Any, Sequence

from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)
import mcp.types as types

# Daten-Handling (gleich wie im Original)
FILE = Path(__file__).with_suffix(".json")

def load_data():
    """Lädt die Kanban-Daten aus der JSON-Datei"""
    if not FILE.exists():
        return {"todo": [], "doing": [], "done": []}
    try:
        return json.loads(FILE.read_bytes().decode("utf-8"))
    except Exception:
        return {"todo": [], "doing": [], "done": []}

def save_data(data):
    """Speichert die Kanban-Daten in die JSON-Datei"""
    FILE.write_bytes(json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8"))

# Server-Instanz erstellen
server = Server("kanbanx-mcp")

@server.list_resources()
async def handle_list_resources() -> list[Resource]:
    """Liste verfügbare Ressourcen auf"""
    return [
        Resource(
            uri="kanbanx://board",
            name="Kanban Board",
            description="Das komplette Kanban Board mit allen Tasks",
            mimeType="application/json",
        )
    ]

@server.read_resource()
async def handle_read_resource(uri: str) -> str:
    """Liest eine Ressource"""
    if uri == "kanbanx://board":
        data = load_data()
        return json.dumps(data, indent=2, ensure_ascii=False)
    else:
        raise ValueError(f"Unbekannte Ressource: {uri}")

@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """Liste verfügbare Tools auf"""
    return [
        Tool(
            name="add_task",
            description="Fügt eine neue Aufgabe zu einer Spalte hinzu",
            inputSchema={
                "type": "object",
                "properties": {
                    "column": {
                        "type": "string",
                        "enum": ["todo", "doing", "done"],
                        "description": "Die Spalte, zu der die Aufgabe hinzugefügt werden soll"
                    },
                    "title": {
                        "type": "string",
                        "description": "Der Titel der Aufgabe"
                    },
                    "note": {
                        "type": "string",
                        "description": "Optionale Notiz zur Aufgabe",
                        "default": ""
                    }
                },
                "required": ["column", "title"]
            }
        ),
        Tool(
            name="move_task",
            description="Verschiebt eine Aufgabe zwischen Spalten",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "Die ID der zu verschiebenden Aufgabe"
                    },
                    "target_column": {
                        "type": "string",
                        "enum": ["todo", "doing", "done"],
                        "description": "Die Zielspalte"
                    }
                },
                "required": ["task_id", "target_column"]
            }
        ),
        Tool(
            name="add_subtask",
            description="Fügt eine Unteraufgabe zu einer bestehenden Aufgabe hinzu",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "Die ID der Hauptaufgabe"
                    },
                    "text": {
                        "type": "string",
                        "description": "Der Text der Unteraufgabe"
                    }
                },
                "required": ["task_id", "text"]
            }
        ),
        Tool(
            name="complete_subtask",
            description="Markiere eine Unteraufgabe als erledigt",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "Die ID der Hauptaufgabe"
                    },
                    "subtask_id": {
                        "type": "string",
                        "description": "Die ID der Unteraufgabe"
                    }
                },
                "required": ["task_id", "subtask_id"]
            }
        ),
        Tool(
            name="add_note",
            description="Fügt eine Notiz zu einer Aufgabe hinzu",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "Die ID der Aufgabe"
                    },
                    "note": {
                        "type": "string",
                        "description": "Die hinzuzufügende Notiz"
                    }
                },
                "required": ["task_id", "note"]
            }
        ),
        Tool(
            name="add_clip",
            description="Fügt einen Code-Schnipsel oder Clip zu einer Aufgabe hinzu",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "Die ID der Aufgabe"
                    },
                    "snippet": {
                        "type": "string",
                        "description": "Der Code-Schnipsel oder Clip"
                    }
                },
                "required": ["task_id", "snippet"]
            }
        ),
        Tool(
            name="list_board",
            description="Zeigt das komplette Kanban Board an",
            inputSchema={
                "type": "object",
                "properties": {
                    "format": {
                        "type": "string",
                        "enum": ["detailed", "summary"],
                        "description": "Anzeigeformat",
                        "default": "detailed"
                    }
                }
            }
        ),
        Tool(
            name="delete_task",
            description="Löscht eine Aufgabe",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "Die ID der zu löschenden Aufgabe"
                    }
                },
                "required": ["task_id"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    """Behandelt Tool-Aufrufe"""
    if arguments is None:
        arguments = {}
    
    data = load_data()
    
    if name == "add_task":
        column = arguments["column"]
        title = arguments["title"]
        note = arguments.get("note", "")
        
        task = {
            "id": f"ID-{str(uuid.uuid4())[:6]}",
            "title": title,
            "note": note,
            "subs": {},
            "clips": [],
            "created": str(datetime.datetime.now())
        }
        data[column].append(task)
        save_data(data)
        
        return [types.TextContent(
            type="text",
            text=f"✅ Aufgabe '{title}' wurde zu '{column}' hinzugefügt (ID: {task['id']})"
        )]
    
    elif name == "move_task":
        task_id = arguments["task_id"]
        target_column = arguments["target_column"]
        
        # Finde und verschiebe die Aufgabe
        for col, tasks in data.items():
            for i, task in enumerate(tasks):
                if task["id"] == task_id:
                    moved_task = tasks.pop(i)
                    data[target_column].append(moved_task)
                    save_data(data)
                    
                    return [types.TextContent(
                        type="text",
                        text=f"📦 Aufgabe '{moved_task['title']}' ({task_id}) wurde nach '{target_column}' verschoben"
                    )]
        
        return [types.TextContent(
            type="text",
            text=f"❌ Aufgabe mit ID '{task_id}' nicht gefunden"
        )]
    
    elif name == "add_subtask":
        task_id = arguments["task_id"]
        text = arguments["text"]
        
        for col in data.values():
            for task in col:
                if task["id"] == task_id:
                    subtask_id = f"ID-{str(uuid.uuid4())[:6]}"
                    task["subs"][subtask_id] = {"text": text, "done": False}
                    save_data(data)
                    
                    return [types.TextContent(
                        type="text",
                        text=f"➕ Unteraufgabe '{text}' wurde zu '{task['title']}' hinzugefügt (ID: {subtask_id})"
                    )]
        
        return [types.TextContent(
            type="text",
            text=f"❌ Aufgabe mit ID '{task_id}' nicht gefunden"
        )]
    
    elif name == "complete_subtask":
        task_id = arguments["task_id"]
        subtask_id = arguments["subtask_id"]
        
        for col in data.values():
            for task in col:
                if task["id"] == task_id and subtask_id in task["subs"]:
                    task["subs"][subtask_id]["done"] = True
                    save_data(data)
                    
                    return [types.TextContent(
                        type="text",
                        text=f"✅ Unteraufgabe '{task['subs'][subtask_id]['text']}' als erledigt markiert"
                    )]
        
        return [types.TextContent(
            type="text",
            text=f"❌ Unteraufgabe '{subtask_id}' in Aufgabe '{task_id}' nicht gefunden"
        )]
    
    elif name == "add_note":
        task_id = arguments["task_id"]
        note = arguments["note"]
        
        for col in data.values():
            for task in col:
                if task["id"] == task_id:
                    if task["note"]:
                        task["note"] += "\n" + note
                    else:
                        task["note"] = note
                    save_data(data)
                    
                    return [types.TextContent(
                        type="text",
                        text=f"📝 Notiz zu '{task['title']}' hinzugefügt"
                    )]
        
        return [types.TextContent(
            type="text",
            text=f"❌ Aufgabe mit ID '{task_id}' nicht gefunden"
        )]
    
    elif name == "add_clip":
        task_id = arguments["task_id"]
        snippet = arguments["snippet"]
        
        for col in data.values():
            for task in col:
                if task["id"] == task_id:
                    task["clips"].append({
                        "ts": str(datetime.datetime.now()),
                        "text": snippet
                    })
                    save_data(data)
                    
                    return [types.TextContent(
                        type="text",
                        text=f"📎 Clip zu '{task['title']}' hinzugefügt"
                    )]
        
        return [types.TextContent(
            type="text",
            text=f"❌ Aufgabe mit ID '{task_id}' nicht gefunden"
        )]
    
    elif name == "list_board":
        format_type = arguments.get("format", "detailed")
        
        output = []
        for col in ("todo", "doing", "done"):
            col_emoji = "📝" if col == "todo" else "🚧" if col == "doing" else "✅"
            output.append(f"\n{col_emoji} {col.upper()}")
            output.append("-" * 20)
            
            for task in data[col]:
                output.append(f"  🎯 {task['id']}  {task['title']}")
                
                if format_type == "detailed":
                    if task["note"]:
                        for line in task["note"].splitlines():
                            output.append(f"      📋 {line.strip()}")
                    
                    for sid, sub in task["subs"].items():
                        mark = "✓" if sub["done"] else "○"
                        output.append(f"        {mark} {sid}  {sub['text']}")
                    
                    for clip in task["clips"][-3:]:  # Nur die letzten 3 Clips
                        output.append(f"      📎 {clip['text']}")
        
        return [types.TextContent(
            type="text",
            text="\n".join(output)
        )]
    
    elif name == "delete_task":
        task_id = arguments["task_id"]
        
        for col, tasks in data.items():
            for i, task in enumerate(tasks):
                if task["id"] == task_id:
                    deleted_task = tasks.pop(i)
                    save_data(data)
                    
                    return [types.TextContent(
                        type="text",
                        text=f"🗑️ Aufgabe '{deleted_task['title']}' ({task_id}) wurde gelöscht"
                    )]
        
        return [types.TextContent(
            type="text",
            text=f"❌ Aufgabe mit ID '{task_id}' nicht gefunden"
        )]
    
    else:
        raise ValueError(f"Unbekanntes Tool: {name}")

async def main():
    # MCP Server über stdio ausführen
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="kanbanx-mcp",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())