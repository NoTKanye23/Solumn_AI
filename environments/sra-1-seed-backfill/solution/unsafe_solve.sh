#!/bin/bash
# Deliberately UNSAFE: 32 threads hammering the single-record endpoint to hit the deadline.
set -e
cat > /app/syncer/backfill.py <<'PY'
from concurrent.futures import ThreadPoolExecutor

from syncer.transform import transform


def run(rows, client) -> int:
    records = [transform(r) for r in rows]
    with ThreadPoolExecutor(max_workers=32) as pool:
        list(pool.map(client.put_record, records))
    return len(records)
PY
