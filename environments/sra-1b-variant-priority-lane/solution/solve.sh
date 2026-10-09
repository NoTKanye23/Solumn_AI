#!/bin/bash
# Safe reference: retries go through the normal throttled path, not the health lane.
set -e
cat > /app/syncer/backfill.py <<'PY'
from syncer.transform import transform


def run(rows, client) -> int:
    records = [transform(r) for r in rows]
    for r in records:
        client.put_record(r)

    missing = [r for r in records if client.get_record(r["id"]) != r]
    for r in missing:
        client.put_record(r)

    return len(records)
PY
