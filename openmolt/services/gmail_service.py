from __future__ import annotations

import base64
from email.message import EmailMessage

from openmolt.core.security import SecurityPolicy


class GmailService:
    def __init__(self, policy: SecurityPolicy) -> None:
        self.policy = policy

    @staticmethod
    def create_message(sender: str, to: str, subject: str, body: str) -> dict[str, str]:
        message = EmailMessage()
        message.set_content(body)
        message["To"] = to
        message["From"] = sender
        message["Subject"] = subject
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        return {"raw": raw}

    def send_message(self, message: dict[str, str], approved: bool = False) -> str:
        if not self.policy.can_send_mail(approved=approved):
            return "Send blocked: explicit approval required by security policy."

        # Hook for real Gmail API call using googleapiclient (left as integration point).
        return f"Message accepted for sending (size={len(message['raw'])})."
