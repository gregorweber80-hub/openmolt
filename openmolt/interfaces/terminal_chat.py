from __future__ import annotations

import asyncio

import typer
from rich import print

from openmolt.core.config import Settings, load_app_config
from openmolt.core.security import SecurityPolicy
from openmolt.services.downloader import download_file
from openmolt.services.ollama_client import OllamaClient

app = typer.Typer(help="Terminal chat with OpenMolt via Ollama")


@app.command()
def chat(prompt: str) -> None:
    settings = Settings()
    cfg = load_app_config(settings.config_path)
    client = OllamaClient(cfg.ollama.host, cfg.ollama.model)
    response = asyncio.run(client.chat(prompt))
    print(f"[bold green]OpenMolt:[/bold green] {response}")


@app.command()
def download(url: str, output_dir: str = "downloads") -> None:
    settings = Settings()
    cfg = load_app_config(settings.config_path)
    policy = SecurityPolicy(
        mode=cfg.security.mode,
        require_explicit_send_approval=cfg.security.require_explicit_send_approval,
        allowed_domains=set(cfg.security.allowed_domains),
    )
    path = download_file(url=url, destination_dir=output_dir, policy=policy)
    print(f"[bold cyan]Download abgeschlossen:[/bold cyan] {path}")


if __name__ == "__main__":
    app()
