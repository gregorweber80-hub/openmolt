# OpenMolt

OpenMolt is a personal, modular assistant inspired by OpenClaw, built for **local Ollama usage**, **secure-by-default execution**, a **web dashboard**, **account gateway modules**, **Gmail compose/send workflows**, and **extensible skills**.

## Description

OpenMolt runs locally and connects assistant workflows in one place:
- chat with a local Ollama model,
- browse/search the web under policy checks,
- draft/send emails with explicit approval,
- connect Telegram through BotFather,
- extend capabilities with custom Python skills.

It supports three entry points: dashboard, terminal, and Telegram bot.

## Features

- Local Ollama integration (default model: `qwen2.5-coder:latest`)
- Web browsing/search with allowlist checks in `secure` mode
- Gmail compose + send flow with approval guard
- Gateway module for credential/login flow preparation
- Skill plugin loading from `openmolt/skills/*.py`
- Interfaces:
  - Web dashboard (`FastAPI`)
  - Terminal (`openmolt-terminal`)
  - Telegram bot (`openmolt-telegram`)

## Installation

### Option A (recommended): install script

```bash
bash scripts/install_openmolt.sh
```

The script:
- creates `.venv`,
- installs OpenMolt using `pip install -e .`,
- pulls the default Ollama model if `ollama` is installed,
- prints next startup steps.

### Option B: manual install

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
ollama pull qwen2.5-coder:latest
```

## First Run

```bash
# 1) Start Ollama
ollama serve

# 2) Run one-time OpenMolt setup
openmolt-terminal init

# 3) Start dashboard
uvicorn openmolt.app:app --host 0.0.0.0 --port 8000
```

Open the dashboard at: http://localhost:8000

## Terminal Usage

On first productive command, OpenMolt auto-runs a one-time setup wizard (model + Telegram + safety acknowledgment) if not yet completed.

```bash
# explicit setup
openmolt-terminal init

# chat
openmolt-terminal chat "Create a daily plan"

# secure download (policy-aware)
openmolt-terminal download "https://github.com/octocat/Spoon-Knife/archive/refs/heads/main.zip" --output-dir downloads
```

## Telegram Usage

1. Create a Telegram bot via BotFather.
2. Run `openmolt-terminal init` and add your bot token (or edit `config/openmolt.yaml`).
3. Start the bot:

```bash
openmolt-telegram
```

If pairing is enabled, unauthorized chats receive a pairing code.
Confirm with `/pair <code>` and the chat ID is persisted into `allowed_chat_ids`.

## Security Model

- `security.mode: secure` enforces URL allowlist checks.
- Email sending is blocked unless explicitly approved (`approved=true`).
- Telegram access can be constrained to explicit `allowed_chat_ids`.

## Troubleshooting

- If `ollama serve` is not running, model requests fail.
- If dependencies like `pydantic`/`pyyaml` are missing, imports/tests fail.
- If Telegram token is invalid, bot startup fails.

## Adding Skills

1. Add a file in `openmolt/skills/`.
2. Expose a `skill` object with `name` and `run(text) -> str`.
3. Skills are loaded by the dashboard/service at startup.

See `openmolt/skills/example_skill.py` for a reference.
