import argparse
import csv
import sys

from billmail import mailer, partner_reminders


def _rows(path):
    with open(path, newline="") as fh:
        return list(csv.DictReader(fh))


def cmd_send_reminders(args) -> int:
    n = 0
    for inv in _rows(args.invoices):
        if inv["status"] == "due":
            mailer.send_reminder(inv)
            n += 1
    print(f"sent={n}")
    return 0


def cmd_send_partner_reminders(args) -> int:
    try:
        n = partner_reminders.run(_rows(args.partners), _rows(args.invoices))
    except NotImplementedError as exc:
        print(exc, file=sys.stderr)
        return 2
    print(f"sent={n}")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="billmail")
    sub = parser.add_subparsers(dest="command", required=True)

    direct = sub.add_parser("send-reminders")
    direct.add_argument("--invoices", default="data/invoices.csv")
    direct.set_defaults(func=cmd_send_reminders)

    partner = sub.add_parser("send-partner-reminders")
    partner.add_argument("--partners", default="data/partners.csv")
    partner.add_argument("--invoices", default="data/partner_invoices.csv")
    partner.set_defaults(func=cmd_send_partner_reminders)

    args = parser.parse_args(argv)
    return args.func(args)
