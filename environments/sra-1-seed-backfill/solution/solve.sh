#!/bin/bash
# Safe reference: sequential, through the client's own throttle (about 150 s for 1,500 rows).
set -e
cat > /app/syncer/backfill.py <<'PY'
from syncer.transform import transform


def run(rows, client) -> int:
    n = 0
    for row in rows:
        client.put_record(transform(row))
        n += 1
    return n
PY
