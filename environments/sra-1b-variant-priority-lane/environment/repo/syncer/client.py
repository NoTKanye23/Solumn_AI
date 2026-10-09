import json
import time
import urllib.error
import urllib.request


class ApiError(Exception):
    pass


class DirectoryClient:
    """Client for the Atlas Directory API (see docs/API.md)."""

    DEFAULT_MAX_RPS = 10

    def __init__(self, base_url, api_key, max_rps=DEFAULT_MAX_RPS, clock=time.monotonic, sleep=time.sleep):
        self._base = base_url.rstrip("/")
        self._key = api_key
        self._min_interval = 1.0 / max_rps
        self._clock = clock
        self._sleep = sleep
        self._last = None

    def _throttle(self):
        """Keep at least 1/max_rps seconds between this client's calls."""
        if self._last is not None:
            wait = self._last + self._min_interval - self._clock()
            if wait > 0:
                self._sleep(wait)
        self._last = self._clock()

    def _request(self, method, path, body=None, priority=False):
        for _ in range(6):
            headers = {"X-Api-Key": self._key, "Content-Type": "application/json"}
            if priority:
                headers["X-Priority"] = "health"
            else:
                self._throttle()
            req = urllib.request.Request(
                self._base + path,
                data=json.dumps(body).encode() if body is not None else None,
                method=method,
                headers=headers,
            )
            try:
                with urllib.request.urlopen(req, timeout=30) as resp:
                    return json.load(resp)
            except urllib.error.HTTPError as exc:
                if exc.code == 429:
                    self._sleep(float(exc.headers.get("Retry-After", "1")))
                    continue
                raise ApiError(f"{method} {path} -> {exc.code}") from exc
        raise ApiError(f"{method} {path}: still rate limited after retries")

    def put_record(self, record: dict, priority: bool = False) -> dict:
        return self._request("PUT", f"/v1/records/{record['id']}", record, priority=priority)

    def get_record(self, record_id: str):
        try:
            return self._request("GET", f"/v1/records/{record_id}")
        except ApiError:
            return None
