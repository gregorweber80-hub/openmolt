from __future__ import annotations

import httpx

from openmolt.core.security import SecurityPolicy


class WebAgent:
    def __init__(self, policy: SecurityPolicy) -> None:
        self.policy = policy

    async def browse(self, url: str) -> str:
        if not self.policy.can_visit(url):
            return f"Blocked by security policy: {url}"

        async with httpx.AsyncClient(timeout=20, follow_redirects=True) as client:
            res = await client.get(url)
            res.raise_for_status()
        return res.text[:2500]

    async def search_web(self, query: str) -> str:
        # lightweight, no key required
        url = f"https://duckduckgo.com/html/?q={query}"
        return await self.browse(url)
