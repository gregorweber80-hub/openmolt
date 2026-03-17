from __future__ import annotations

import asyncio

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

from openmolt.core.config import Settings, load_app_config
from openmolt.services.ollama_client import OllamaClient


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("OpenMolt Bot bereit. Schreibe mir eine Nachricht.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    settings = Settings()
    cfg = load_app_config(settings.config_path)
    allowed = set(cfg.telegram.allowed_chat_ids)
    chat_id = update.effective_chat.id
    if allowed and chat_id not in allowed:
        await update.message.reply_text("Chat nicht autorisiert.")
        return

    client = OllamaClient(cfg.ollama.host, cfg.ollama.model)
    answer = await client.chat(update.message.text)
    await update.message.reply_text(answer[:4000])


def run_bot() -> None:
    settings = Settings()
    cfg = load_app_config(settings.config_path)
    if not cfg.telegram.enabled or not cfg.telegram.bot_token:
        raise RuntimeError("Telegram ist nicht aktiviert. Bitte config/openmolt.yaml pflegen.")

    app = ApplicationBuilder().token(cfg.telegram.bot_token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    asyncio.run(app.run_polling())
