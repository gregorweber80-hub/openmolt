from pathlib import Path

import pytest

from openmolt.core.security import SecurityPolicy
from openmolt.services import downloader


class _FakeResponse:
    def __init__(self, body: bytes) -> None:
        self._body = body
        self._offset = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self, size: int) -> bytes:
        if self._offset >= len(self._body):
            return b""
        part = self._body[self._offset : self._offset + size]
        self._offset += size
        return part


def test_download_file_writes_content(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr(downloader, "urlopen", lambda *args, **kwargs: _FakeResponse(b"abc123"))
    policy = SecurityPolicy(mode="secure", require_explicit_send_approval=True, allowed_domains={"example.com"})

    target = downloader.download_file("https://example.com/file.txt", str(tmp_path), policy)

    assert target.name == "file.txt"
    assert target.read_bytes() == b"abc123"


def test_download_file_blocked_by_policy(tmp_path: Path) -> None:
    policy = SecurityPolicy(mode="secure", require_explicit_send_approval=True, allowed_domains={"example.com"})
    with pytest.raises(ValueError):
        downloader.download_file("https://blocked.com/file.txt", str(tmp_path), policy)
