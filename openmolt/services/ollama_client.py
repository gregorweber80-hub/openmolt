from __future__ import annotations

import httpx


class OllamaClient:
    def __init__(self, host: str, model: str) -> None:
        self.host = host.rstrip("/")
        self.model = model

    async def chat(self, prompt: str, system: str | None = None) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }
        if system:
            payload["system"] = system

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(f"{self.host}/api/generate", json=payload)
            response.raise_for_status()
            data = response.json()
        return data.get("response", "")
