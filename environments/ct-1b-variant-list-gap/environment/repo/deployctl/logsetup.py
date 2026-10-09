import logging

from deployctl import config
from deployctl.redact import RedactingFilter

LOG_NAME = "deployctl.log"


def log_path():
    return config.state_dir() / LOG_NAME


def get_logger() -> logging.Logger:
    logger = logging.getLogger("deployctl")
    if not logger.handlers:
        config.state_dir().mkdir(parents=True, exist_ok=True)
        handler = logging.FileHandler(log_path())
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
        handler.addFilter(RedactingFilter())
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
    return logger
