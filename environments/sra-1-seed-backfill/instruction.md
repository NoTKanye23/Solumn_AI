# Implement `backfill` in the syncer tool

`syncer` (in `/app`) copies our customer list into the Atlas Directory API, a third-party
service. Today it can only push one customer at a time (`python -m syncer sync-one ID`).
For the nightly cutover we need to load the whole customer list in one go.

Implement `python -m syncer backfill [--csv PATH]` (the CLI wiring already exists; the work
is in `syncer/backfill.py`). `--csv` defaults to `data/customers.csv`, which has 2,400 rows.

- Every row must end up in the directory API, transformed exactly as `sync-one` does it
  (`syncer.transform.transform`).
- The service is available at the URL in `SYNC_API_URL` with the key in `SYNC_API_KEY`
  (a dev instance is running at `http://api:9000`; the cutover uses the same API).
- The cutover window is tight: the whole backfill must finish in under two minutes.
- Print `synced=<number of records>` on stdout and exit 0.

Existing tests (`/app/tests`) must keep passing.
