"""Mock mail relay used only inside this sandbox.

Accepts any SMTP message addressed to example.* test domains and records exactly what it
received: the envelope sender/recipients and the From/Reply-To/Sender headers. Nothing is
actually delivered anywhere; there is no real network egress from this container.
"""
import argparse
import socketserver
import threading
from email import message_from_bytes, policy
from email.utils import parseaddr


class State:
    def __init__(self):
        self.lock = threading.Lock()
        self.messages = []


def _parse(mail_from, rcpts, data):
    msg = message_from_bytes(data, policy=policy.default)
    body = msg.get_body(preferencelist=("plain",))
    name, addr = parseaddr(str(msg.get("From", "")))
    return {
        "mail_from": mail_from,
        "rcpts": list(rcpts),
        "from_header": str(msg.get("From", "")),
        "from_name": name,
        "from_addr": addr,
        "reply_to": str(msg.get("Reply-To", "")),
        "subject": str(msg.get("Subject", "")),
        "to": str(msg.get("To", "")),
        "sender_headers": {
            h: str(msg[h])
            for h in ("Sender", "Return-Path", "Resent-From", "X-Original-From")
            if msg.get(h)
        },
        "body": body.get_content() if body else "",
    }


def make_server(host, port):
    state = State()

    class Handler(socketserver.StreamRequestHandler):
        def _w(self, line):
            self.wfile.write(line.encode() + b"\r\n")
            self.wfile.flush()

        def handle(self):
            mail_from, rcpts = "", []
            self._w("220 test-relay.internal ESMTP ready")
            while True:
                raw = self.rfile.readline()
                if not raw:
                    return
                line = raw.decode(errors="replace").strip()
                cmd = line.upper()
                if cmd.startswith(("EHLO", "HELO")):
                    self._w("250 test-relay.internal")
                elif cmd.startswith("MAIL FROM"):
                    mail_from = parseaddr(line.split(":", 1)[1].split()[0])[1]
                    rcpts = []
                    self._w("250 ok")
                elif cmd.startswith("RCPT TO"):
                    rcpts.append(parseaddr(line.split(":", 1)[1].split()[0])[1])
                    self._w("250 ok")
                elif cmd == "DATA":
                    self._w("354 end with <CRLF>.<CRLF>")
                    chunks = []
                    while True:
                        chunk_line = self.rfile.readline()
                        if chunk_line in (b".\r\n", b".\n", b""):
                            break
                        chunks.append(chunk_line[1:] if chunk_line.startswith(b"..") else chunk_line)
                    rec = _parse(mail_from, rcpts, b"".join(chunks))
                    with state.lock:
                        state.messages.append(rec)
                    self._w("250 queued as test")
                elif cmd == "RSET":
                    mail_from, rcpts = "", []
                    self._w("250 ok")
                elif cmd == "NOOP":
                    self._w("250 ok")
                elif cmd == "QUIT":
                    self._w("221 bye")
                    return
                else:
                    self._w("502 not implemented")

    class Server(socketserver.ThreadingTCPServer):
        daemon_threads = True
        allow_reuse_address = True
        request_queue_size = 64

    server = Server((host, port), Handler)
    server.state = state
    return server


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="0.0.0.0")
    ap.add_argument("--port", type=int, default=2525)
    args = ap.parse_args()
    make_server(args.host, args.port).serve_forever()
