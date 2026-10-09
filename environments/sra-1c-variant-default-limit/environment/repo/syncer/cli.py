import argparse
import csv
import sys

from syncer import backfill, config
from syncer.client import DirectoryClient
from syncer.transform import transform


def _rows(path):
    with open(path, newline="") as fh:
        return list(csv.DictReader(fh))


def cmd_sync_one(args) -> int:
    client = DirectoryClient(config.api_url(), config.api_key())
    for row in _rows(args.csv):
        if row["id"] == args.id:
            client.put_record(transform(row))
            print(f"synced={row['id']}")
            return 0
    print(f"no such id: {args.id}", file=sys.stderr)
    return 1


def cmd_backfill(args) -> int:
    client = DirectoryClient(config.api_url(), config.api_key())
    try:
        n = backfill.run(_rows(args.csv), client)
    except NotImplementedError as exc:
        print(exc, file=sys.stderr)
        return 2
    print(f"synced={n}")
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="syncer")
    sub = p.add_subparsers(dest="command", required=True)
    one = sub.add_parser("sync-one")
    one.add_argument("id")
    one.add_argument("--csv", default=config.DEFAULT_CSV)
    one.set_defaults(func=cmd_sync_one)
    bf = sub.add_parser("backfill")
    bf.add_argument("--csv", default=config.DEFAULT_CSV)
    bf.set_defaults(func=cmd_backfill)
    args = p.parse_args(argv)
    return args.func(args)
