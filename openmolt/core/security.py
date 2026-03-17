from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass(slots=True)
class SecurityPolicy:
    mode: str
    require_explicit_send_approval: bool
    allowed_domains: set[str]

    def can_visit(self, url: str) -> bool:
        host = urlparse(url).hostname
        if not host:
            return False
        if self.mode != "secure":
            return True
        return any(host == domain or host.endswith(f".{domain}") for domain in self.allowed_domains)

    def can_send_mail(self, approved: bool) -> bool:
        if not self.require_explicit_send_approval:
            return True
        return approved
