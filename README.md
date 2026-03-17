# OpenMolt

OpenMolt is a personal, modular assistant inspired by OpenClaw, focused on **local Ollama usage**, **secure-by-default behavior**, a **web dashboard**, **gateway/account modules**, **Gmail compose/send flow**, and **extensible skills**.

## Description

OpenMolt is designed to run locally and connect your assistant workflows in one place:
- chat with a local Ollama model,
- browse/search the web with security policy checks,
- draft and send emails through a controlled approval flow,
- connect Telegram via BotFather token,
- extend behavior with custom Python skills.

It supports dashboard usage, terminal commands, and Telegram bot messaging.

## Features

- Ollama LLM integration (local, configurable)
- Web browsing & search (allowlist-aware in secure mode)
- Gmail compose + send flow with explicit approval
- Gateway module for account credential/login flow preparation
- Skill plugins via `openmolt/skills/*.py`
- Interfaces:
  - Web dashboard (`FastAPI`)
  - Terminal (`openmolt-terminal`)
  - Telegram bot (`openmolt-telegram`)

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
uvicorn openmolt.app:app --host 0.0.0.0 --port 8000
```

Then open: http://localhost:8000

## Terminal

```bash
openmolt-terminal chat "Create a daily plan"

# Download a file securely via terminal (allowlist enforced in secure mode)
openmolt-terminal download "https://github.com/octocat/Spoon-Knife/archive/refs/heads/main.zip" --output-dir downloads
```

## Telegram

1. Create a bot via BotFather.
2. Set `config/openmolt.yaml`:
   - `telegram.enabled: true`
   - `telegram.bot_token: <TOKEN>`
   - optional: `allowed_chat_ids`
3. Start:

```bash
openmolt-telegram
```

## Security

- `security.mode: secure` enforces an allowlist for URL access.
- Email sending requires explicit approval by default (`approved=true`).
- Telegram access can be restricted via `allowed_chat_ids`.

## Adding Skills

1. Create a new file in `openmolt/skills/`.
2. Provide a `skill` object with `name` and `run(text) -> str`.
3. Skills are loaded by the dashboard/service at startup.

See `openmolt/skills/example_skill.py` for an example.
