from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class AccountCredential:
    service: str
    username: str
    password: str


@dataclass
class Gateway:
    """Credential gateway abstraction for account logins."""

    credentials: dict[str, AccountCredential] = field(default_factory=dict)

    def register(self, service: str, username: str, password: str) -> None:
        self.credentials[service] = AccountCredential(service=service, username=username, password=password)

    def login(self, service: str) -> str:
        cred = self.credentials.get(service)
        if not cred:
            return f"No credentials stored for {service}."
        return f"Login flow prepared for {service} as {cred.username}."
