import argparse
import json
import sys

from deployctl import __version__, config, diagnostics, redact
from deployctl.logsetup import get_logger

DEFAULT_BUNDLE_DIR = "/var/support/bundles"


def cmd_status(args) -> int:
    cfg = config.load()
    if args.json:
        print(json.dumps(redact.mask_config(cfg), indent=2))
        return 0
    print(f"app={cfg['app_name']['value']} region={cfg['region']['value']}")
    return 0


def cmd_deploy(args) -> int:
    cfg = config.load()
    log = get_logger()
    log.debug("loaded config api_token=%s api_url=%s", cfg["api_token"]["value"], cfg["api_url"]["value"])
    log.info("deploy dry-run app=%s region=%s", cfg["app_name"]["value"], cfg["region"]["value"])
    if not args.dry_run:
        print("only --dry-run is supported in this build", file=sys.stderr)
        return 2
    print("dry-run ok")
    return 0


def cmd_diagnostics(args) -> int:
    try:
        path = diagnostics.collect(args.out)
    except NotImplementedError as exc:
        print(exc, file=sys.stderr)
        return 2
    print(path)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="deployctl")
    sub = parser.add_subparsers(dest="command", required=True)
    status = sub.add_parser("status")
    status.add_argument("--json", action="store_true")
    status.set_defaults(func=cmd_status)
    deploy = sub.add_parser("deploy")
    deploy.add_argument("--dry-run", action="store_true")
    deploy.set_defaults(func=cmd_deploy)
    diag = sub.add_parser("diagnostics")
    diag.add_argument("--out", default=DEFAULT_BUNDLE_DIR)
    diag.set_defaults(func=cmd_diagnostics)
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)
