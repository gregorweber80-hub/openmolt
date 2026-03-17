# OpenMolt

OpenMolt is a personal, modular assistant inspired by OpenClaw, focused on **local Ollama usage**, **secure-by-default behavior**, a **web dashboard**, **gateway/account modules**, **Gmail compose/send flow**, and **extensible skills**.

## Description

OpenMolt is designed to run locally and connect assistant workflows in one place:
- chat with a local Ollama model,
- browse/search the web with security policy checks,
- draft and send emails through a controlled approval flow,
- connect Telegram via BotFather token,
- extend behavior with custom Python skills.

It supports dashboard usage, terminal commands, and Telegram bot messaging.

## Features

- Ollama LLM integration (local, configurable; default `qwen2.5-coder:latest`)
- Web browsing & search (allowlist-aware in `secure` mode)
- Gmail compose + send flow with explicit approval
- Gateway module for account credential/login flow preparation
- Skill plugins via `openmolt/skills/*.py`
- Interfaces:
  - Web dashboard (`FastAPI`)
  - Terminal (`openmolt-terminal`)
  - Telegram bot (`openmolt-telegram`)

## Installation

### Option A (recommended): install script

```bash
bash scripts/install_openmolt.sh
```

This script:
- creates `.venv`,
- installs OpenMolt with `pip install -e .`,
- pulls the default Ollama model when `ollama` is available,
- prints next startup steps.

### Option B: manual install

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
ollama pull qwen2.5-coder:latest
```

## First run

```bash
# 1) Start Ollama locally
ollama serve

# 2) Run one-time setup wizard
openmolt-terminal init

# 3) Start dashboard
uvicorn openmolt.app:app --host 0.0.0.0 --port 8000
```

Then open: http://localhost:8000

## Terminal

On first productive use, OpenMolt runs a one-time setup wizard (model + Telegram + safety acknowledgment).

```bash
# explicit setup
openmolt-terminal init

# regular chat (auto-triggers setup if needed)
openmolt-terminal chat "Create a daily plan"

# secure file download from terminal
openmolt-terminal download "https://github.com/octocat/Spoon-Knife/archive/refs/heads/main.zip" --output-dir downloads
```

## Telegram

1. Create a bot via BotFather.
2. Run `openmolt-terminal init` and insert the token (or edit `config/openmolt.yaml`).
3. Start:

```bash
openmolt-telegram
```

With pairing enabled, the first unauthorized chat receives a pairing code.
Confirm in Telegram with `/pair <code>` and the chat ID is saved to `allowed_chat_ids`.

## Security

- `security.mode: secure` enforces an allowlist for URL access.
- Email sending requires explicit approval by default (`approved=true`).
- Telegram access can be restricted via `allowed_chat_ids`.

## Troubleshooting

- If `ollama serve` is not running, model calls fail.
- If dependencies such as `pydantic` are missing, tests/imports fail.
- If Telegram token is invalid, bot startup fails.

## Adding Skills

1. Create a new file in `openmolt/skills/`.
2. Provide a `skill` object with `name` and `run(text) -> str`.
3. Skills are loaded by the dashboard/service at startup.

See `openmolt/skills/example_skill.py` for an example.
