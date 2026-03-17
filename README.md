# OpenMolt

OpenMolt is a personal modular assistant inspired by OpenClaw, focused on local model usage via Ollama, web search/browsing, controlled email sending, account gateway helpers, and extensible skills.

## Description

OpenMolt provides a small local-first assistant stack with:
- Ollama chat integration,
- a FastAPI dashboard,
- terminal commands,
- Telegram bot messaging,
- plugin-like Python skills.

## Features

- Ollama LLM integration (configurable host/model)
- Web browsing & search with security allowlist support
- Gmail compose + send flow with explicit approval checks
- Gateway module for account credential/login flow preparation
- Skill loading from `openmolt/skills/*.py`
- Interfaces:
  - Web dashboard (`FastAPI`)
  - Terminal (`openmolt-terminal`)
  - Telegram bot (`openmolt-telegram`)

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

## Configuration

Default config path: `config/openmolt.yaml`

Key values:
- `ollama.host` (default: `http://127.0.0.1:11434`)
- `ollama.model` (default: `llama3.1`)
- `security.mode` (`secure` by default)
- `telegram.enabled`, `telegram.bot_token`, `telegram.allowed_chat_ids`

## First Run

```bash
# 1) start Ollama
ollama serve

# 2) start dashboard
uvicorn openmolt.app:app --host 0.0.0.0 --port 8000
```

Open: http://localhost:8000

## Terminal Usage

```bash
openmolt-terminal chat "Create a daily plan"
openmolt-terminal download "https://github.com/octocat/Spoon-Knife/archive/refs/heads/main.zip" --output-dir downloads
```

## Telegram Usage

1. Create a bot via BotFather.
2. Put your token in `config/openmolt.yaml` and set `telegram.enabled: true`.
3. Start:

```bash
openmolt-telegram
```

## Security Model

- `security.mode: secure` enforces URL allowlist checks.
- Email sending is blocked unless explicitly approved (`approved=true`).
- Telegram access can be restricted via `allowed_chat_ids`.

## Adding Skills

1. Add a file in `openmolt/skills/`.
2. Expose a `skill` object with `name` and `run(text) -> str`.
3. Skills are loaded at startup.
