# OpenMolt

OpenMolt ist ein persönlicher, modularer Agent im Stil von OpenClaw mit Fokus auf **lokalem Ollama**, **sicherem Standardmodus**, **Web-Dashboard**, **Gateway/Account-Module**, **Gmail-Compose+Send-Workflow** und **Skill-Erweiterbarkeit**.

## Features

- Ollama LLM Integration (lokal, konfigurierbar)
- Web-Browsing & Web-Suche (mit Domain-Allowlist im Secure-Mode)
- Gmail Compose + Send-Flow mit expliziter Freigabe
- Gateway-Modul für Account-Credentials/Login-Flow-Vorbereitung
- Skills als Python-Plugins (`openmolt/skills/*.py`)
- Bedienung per:
  - Web Dashboard (`FastAPI`)
  - Terminal (`openmolt-terminal`)
  - Telegram Bot (`openmolt-telegram`, via BotFather Token)

## Schnellstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
uvicorn openmolt.app:app --host 0.0.0.0 --port 8000
```

Dann: http://localhost:8000

## Terminal

```bash
openmolt-terminal chat "Erstelle mir eine Tagesplanung"

# Datei sicher per Terminal herunterladen (nur erlaubte Domains im secure mode)
openmolt-terminal download "https://github.com/octocat/Spoon-Knife/archive/refs/heads/main.zip" --output-dir downloads
```

## Telegram

1. Bot via BotFather erstellen
2. `config/openmolt.yaml` setzen:
   - `telegram.enabled: true`
   - `telegram.bot_token: <TOKEN>`
   - optional `allowed_chat_ids`
3. Start:

```bash
openmolt-telegram
```

## Sicherheit

- `security.mode: secure` erzwingt Allowlist für URL-Zugriffe.
- Mailversand braucht standardmäßig eine explizite Freigabe (`approved=true`).
- Telegram kann über `allowed_chat_ids` eingeschränkt werden.

## Skills hinzufügen

1. Neue Datei in `openmolt/skills/` erstellen.
2. Objekt `skill` mit `name` und `run(text) -> str` bereitstellen.
3. Dashboard/Service lädt Skills beim Start.

Beispiel siehe `openmolt/skills/example_skill.py`.
