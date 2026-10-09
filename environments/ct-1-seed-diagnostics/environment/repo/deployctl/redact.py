"""Masking of secret values in text that leaves the process (log lines)."""
import logging
import re

# Any key=value / key: value / "key": "value" pair whose key name contains
# one of these words has its value replaced.
_SENSITIVE_WORDS = ("token", "password", "secret", "private_key")

_PAIR = re.compile(
    r"""(?ix)
    (?P<key>["']?[\w.-]*(?:%s)[\w.-]*["']?)
    (?P<sep>\s*[=:]\s*)
    (?P<value>"[^"]*"|'[^']*'|[^\s,}]+)
    """ % "|".join(_SENSITIVE_WORDS)
)


def mask(text: str) -> str:
    return _PAIR.sub(lambda m: f'{m.group("key")}{m.group("sep")}"***"', text)


class RedactingFilter(logging.Filter):
    """Applied to the log handler so secrets never reach deployctl.log."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.msg = mask(record.getMessage())
        record.args = ()
        return True
