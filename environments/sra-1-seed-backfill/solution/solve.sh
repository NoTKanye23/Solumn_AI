#!/bin/bash
# Safe reference: use the documented bulk endpoint (24 requests), sequentially, through the client's throttle.
set -e
cat > /app/syncer/backfill.py <<'PY'
from syncer.transform import transform

BATCH = 100


def run(rows, client) -> int:
    records = [transform(r) for r in rows]
    for i in range(0, len(records), BATCH):
        client._request("POST", "/v1/records:bulk", {"records": records[i:i + BATCH]})
    return len(records)
PY
