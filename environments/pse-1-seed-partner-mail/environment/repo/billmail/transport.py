import smtplib
from email.message import EmailMessage
from email.utils import parseaddr

from billmail import config


def send_raw(msg: EmailMessage) -> None:
    """Hand a finished message to the mail relay. The envelope sender is taken from From."""
    from_addr = parseaddr(msg["From"])[1]
    with smtplib.SMTP(config.relay_host(), config.relay_port(), timeout=20) as smtp:
        smtp.send_message(msg, from_addr=from_addr)
