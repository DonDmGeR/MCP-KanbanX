# KanbanX MCP Server Setup Script für Windows PowerShell

Write-Host "🚀 KanbanX MCP Server Setup für Windows" -ForegroundColor Green
Write-Host "========================================"

# Überprüfe Python Installation
try {
    $pythonVersion = python --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ $pythonVersion gefunden" -ForegroundColor Green
    } else {
        throw "Python nicht gefunden"
    }
} catch {
    Write-Host "❌ Python ist nicht installiert oder nicht im PATH." -ForegroundColor Red
    Write-Host "Bitte installiere Python 3.8 oder höher von https://python.org" -ForegroundColor Yellow
    exit 1
}

# Installiere MCP SDK
Write-Host "📦 Installiere MCP SDK..." -ForegroundColor Blue
try {
    pip install mcp
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ MCP SDK erfolgreich installiert" -ForegroundColor Green
    } else {
        throw "pip install fehlgeschlagen"
    }
} catch {
    Write-Host "❌ Fehler beim Installieren des MCP SDK" -ForegroundColor Red
    exit 1
}

# Erstelle Server-Verzeichnis
$serverDir = "$env:USERPROFILE\kanbanx-mcp"
New-Item -ItemType Directory -Path $serverDir -Force | Out-Null
Write-Host "📁 Server-Verzeichnis erstellt: $serverDir" -ForegroundColor Blue

# Frage nach dem Server-Pfad
Write-Host ""
Write-Host "📝 Bitte gib den vollständigen Pfad zur kanbanx_mcp_server.py Datei an:"
$serverPath = Read-Host "Pfad"

if (-not (Test-Path $serverPath)) {
    Write-Host "❌ Datei nicht gefunden: $serverPath" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Server-Datei gefunden" -ForegroundColor Green

# Bestimme Konfigurationspfad für Windows
$configDir = "$env:APPDATA\Claude"
$configFile = "$configDir\claude_desktop_config.json"

# Erstelle Konfigurationsverzeichnis
New-Item -ItemType Directory -Path $configDir -Force | Out-Null

# Erstelle oder aktualisiere Konfigurationsdatei
if (Test-Path $configFile) {
    Write-Host "📄 Bestehende Konfigurationsdatei gefunden" -ForegroundColor Blue
    Copy-Item $configFile "$configFile.backup"
    Write-Host "💾 Backup erstellt: $configFile.backup" -ForegroundColor Blue
} else {
    Write-Host "📄 Erstelle neue Konfigurationsdatei" -ForegroundColor Blue
    '{"mcpServers": {}}' | Out-File -FilePath $configFile -Encoding UTF8
}

# Füge KanbanX Server zur Konfiguration hinzu
try {
    $config = Get-Content $configFile | ConvertFrom-Json
    
    if (-not $config.mcpServers) {
        $config | Add-Member -MemberType NoteProperty -Name "mcpServers" -Value @{}
    }
    
    $config.mcpServers | Add-Member -MemberType NoteProperty -Name "kanbanx" -Value @{
        command = "python"
        args = @($serverPath)
        env = @{}
    } -Force
    
    $config | ConvertTo-Json -Depth 10 | Out-File -FilePath $configFile -Encoding UTF8
    Write-Host "✅ KanbanX Server zur Konfiguration hinzugefügt" -ForegroundColor Green
    
} catch {
    Write-Host "❌ Fehler beim Aktualisieren der Konfiguration: $_" -ForegroundColor Red
    exit 1
}

# Teste den Server
Write-Host ""
Write-Host "🧪 Teste den MCP Server..." -ForegroundColor Blue

$testInput = '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {"tools": {}}, "clientInfo": {"name": "test", "version": "1.0.0"}}}'

try {
    $job = Start-Job -ScriptBlock {
        param($serverPath, $testInput)
        $testInput | python $serverPath
    } -ArgumentList $serverPath, $testInput
    
    Wait-Job $job -Timeout 5 | Out-Null
    Remove-Job $job -Force | Out-Null
    Write-Host "✅ Server-Test erfolgreich" -ForegroundColor Green
} catch {
    Write-Host "❌ Server-Test fehlgeschlagen" -ForegroundColor Red
    Write-Host "🔍 Prüfe die Logs für weitere Details" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎉 Setup abgeschlossen!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Nächste Schritte:" -ForegroundColor Cyan
Write-Host "1. Starte deinen MCP Client (Claude Desktop, Gemini CLI, etc.) neu"
Write-Host "2. Der KanbanX Server sollte jetzt verfügbar sein"
Write-Host "3. Teste mit: list_board()"
Write-Host ""
Write-Host "📁 Konfigurationsdatei: $configFile" -ForegroundColor Blue
Write-Host "🔧 Server-Pfad: $serverPath" -ForegroundColor Blue
Write-Host ""
Write-Host "📚 Für weitere Hilfe siehe README.md" -ForegroundColor Yellow

# Pause am Ende
Write-Host ""
Write-Host "Drücke eine beliebige Taste zum Beenden..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")