import os

DEFAULT_CSV = "data/customers.csv"


def api_url() -> str:
    return os.environ.get("SYNC_API_URL", "http://api:9000")


def api_key() -> str:
    return os.environ.get("SYNC_API_KEY", "")
