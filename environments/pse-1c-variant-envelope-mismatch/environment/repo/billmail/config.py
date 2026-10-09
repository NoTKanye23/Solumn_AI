import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def relay_host() -> str:
    return os.environ.get("MAIL_RELAY_HOST", "relay")


def relay_port() -> int:
    return int(os.environ.get("MAIL_RELAY_PORT", "2525"))


def verified_domains() -> set:
    """Domains we have SPF/DKIM set up for (config/verified_domains.txt)."""
    path = ROOT / "config" / "verified_domains.txt"
    return {line.strip().lower() for line in path.read_text().splitlines() if line.strip()}
