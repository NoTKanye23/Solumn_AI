import smtplib
from email.message import EmailMessage
from email.utils import parseaddr

from billmail import config


def send_raw(msg: EmailMessage, envelope_from: str = None) -> None:
    """Hand a finished message to the mail relay.

    The envelope sender (SMTP MAIL FROM, used for bounce routing) is taken from From
    unless envelope_from is given, in which case it overrides it -- the visible From
    header the recipient sees is unaffected either way.
    """
    from_addr = envelope_from or parseaddr(msg["From"])[1]
    with smtplib.SMTP(config.relay_host(), config.relay_port(), timeout=20) as smtp:
        smtp.send_message(msg, from_addr=from_addr)
