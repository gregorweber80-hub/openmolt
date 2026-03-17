from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen

from openmolt.core.security import SecurityPolicy


def _filename_from_url(url: str) -> str:
    parsed = urlparse(url)
    name = Path(parsed.path).name
    return name or "download.bin"


def download_file(url: str, destination_dir: str, policy: SecurityPolicy) -> Path:
    if not policy.can_visit(url):
        raise ValueError(f"Download blocked by security policy: {url}")

    target_dir = Path(destination_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / _filename_from_url(url)

    with urlopen(url, timeout=60) as response, target.open("wb") as f:  # nosec B310
        while True:
            chunk = response.read(8192)
            if not chunk:
                break
            f.write(chunk)

    return target
