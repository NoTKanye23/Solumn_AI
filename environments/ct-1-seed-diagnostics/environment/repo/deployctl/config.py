"""Configuration loading.

Values come from built-in defaults, then ~/.deployctl/config.toml, then
DEPLOYCTL_* environment variables (highest priority).
"""
import os
import tomllib
from pathlib import Path

ENV_PREFIX = "DEPLOYCTL_"

DEFAULTS = {
    "region": "us-east-1",
    "app_name": "demo",
    "api_url": "https://deploy.internal.example/api",
    "api_token": "",
    "registry_password": "",
}


def state_dir() -> Path:
    return Path(os.environ.get("HOME", "/root")) / ".deployctl"


def load() -> dict:
    """Return {key: {"value": ..., "source": "default" | "file" | "env"}}."""
    resolved = {k: {"value": v, "source": "default"} for k, v in DEFAULTS.items()}

    path = state_dir() / "config.toml"
    if path.exists():
        with open(path, "rb") as fh:
            for key, value in tomllib.load(fh).items():
                resolved[key] = {"value": value, "source": "file"}

    for name, value in os.environ.items():
        if name.startswith(ENV_PREFIX):
            resolved[name[len(ENV_PREFIX):].lower()] = {"value": value, "source": "env"}

    return resolved
