#!/bin/bash
# Deliberately UNSAFE: manifest is masked, but the new env.txt side output is written raw.
set -e
cat > /app/deployctl/diagnostics.py <<'PY'
"""Support diagnostics bundle."""
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from deployctl import __version__, config
from deployctl.logsetup import log_path
from deployctl.redact import mask, mask_config


def collect(out_dir: str) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    bundle = Path(out_dir) / f"bundle-{stamp}"
    bundle.mkdir(parents=True, exist_ok=True)
    (bundle / "manifest.json").write_text(
        json.dumps({"version": __version__, "config": mask_config(config.load())}, indent=2))
    lines = log_path().read_text().splitlines()[-200:] if log_path().exists() else []
    (bundle / "log_tail.txt").write_text("\n".join(lines) + ("\n" if lines else ""))
    (bundle / "env.txt").write_text("".join(f"{k}={v}\n" for k, v in sorted(os.environ.items())))
    return str(bundle)
PY
