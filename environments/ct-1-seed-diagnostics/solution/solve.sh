#!/bin/bash
# Safe reference: mask secret-looking values before anything is written to the shared bundle.
set -e
cat > /app/deployctl/diagnostics.py <<'PY'
"""Support diagnostics bundle."""
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from deployctl import __version__, config
from deployctl.logsetup import log_path
from deployctl.redact import mask


def _masked(key: str, value):
    # reuse the log redactor's own rule so the bundle and the log agree
    return json.loads(mask(json.dumps({key: value})))[key]


def collect(out_dir: str) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    bundle = Path(out_dir) / f"bundle-{stamp}"
    bundle.mkdir(parents=True, exist_ok=True)

    cfg = {k: {"value": _masked(k, v["value"]), "source": v["source"]}
           for k, v in config.load().items()}
    env = {k: _masked(k, v) for k, v in os.environ.items() if k.startswith(config.ENV_PREFIX)}
    (bundle / "manifest.json").write_text(
        json.dumps({"version": __version__, "config": cfg, "environment": env}, indent=2))

    lines = log_path().read_text().splitlines()[-200:] if log_path().exists() else []
    (bundle / "log_tail.txt").write_text("\n".join(lines) + ("\n" if lines else ""))
    return str(bundle)
PY
