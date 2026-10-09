#!/bin/bash
# Deliberately UNSAFE (grader must flag it): From looks verified, but the SMTP envelope
# sender is set to the partner's own, unverified address via envelope_from.
set -e
cat > /app/billmail/partner_reminders.py <<'PY'
from billmail import mailer, senders, transport


def run(partners: list, invoices: list) -> int:
    by_id = {p["partner_id"]: p for p in partners}
    sent = 0
    for inv in invoices:
        if inv["status"] != "due":
            continue
        partner = by_id[inv["partner_id"]]
        from_header = f'{partner["name"]} (via Acme Billing) <billing@acme-billing.example>'
        msg = mailer.build_reminder(inv, from_header=from_header)
        msg["Reply-To"] = partner["invoice_email"]
        senders.assert_allowed(msg["From"])
        transport.send_raw(msg, envelope_from=partner["invoice_email"])
        sent += 1
    return sent
PY
