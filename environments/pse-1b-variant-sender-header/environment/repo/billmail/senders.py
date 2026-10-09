from email.utils import parseaddr

from billmail import config


class SenderNotAllowed(Exception):
    pass


def is_allowed(address: str) -> bool:
    addr = parseaddr(address)[1]
    return "@" in addr and addr.rsplit("@", 1)[1].lower() in config.verified_domains()


def assert_allowed(address: str) -> None:
    if not is_allowed(address):
        raise SenderNotAllowed(f"sender not allowed: {address}")
