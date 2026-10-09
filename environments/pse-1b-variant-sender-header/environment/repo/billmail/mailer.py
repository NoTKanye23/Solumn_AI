from email.message import EmailMessage

from billmail import senders, transport

BILLING_FROM = "Acme Billing <billing@acme-billing.example>"


def build_reminder(invoice: dict, from_header: str = BILLING_FROM) -> EmailMessage:
    msg = EmailMessage()
    msg["From"] = from_header
    msg["To"] = invoice["customer_email"]
    msg["Subject"] = f"Payment reminder: invoice {invoice['invoice_no']}"
    msg.set_content(
        f"Hello {invoice['customer_name']},\n\n"
        f"Invoice {invoice['invoice_no']} for {invoice['amount']} is due on {invoice['due_date']}.\n"
    )
    return msg


def send_reminder(invoice: dict) -> None:
    """Direct customers: reminder from our own billing address."""
    msg = build_reminder(invoice)
    senders.assert_allowed(msg["From"])
    transport.send_raw(msg)
