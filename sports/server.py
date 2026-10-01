"""Local demonstration HTTP server; analyses also work through the CLI."""

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from .analytics import analyze


STATIC = Path(__file__).resolve().parent / "web"
ASSETS = {"/": ("index.html", "text/html; charset=utf-8"),
          "/app.js": ("app.js", "text/javascript; charset=utf-8"),
          "/style.css": ("style.css", "text/css; charset=utf-8")}


def make_server(store, host="127.0.0.1", port=8000):
    class Handler(BaseHTTPRequestHandler):
        def respond(self, status, payload, content_type="application/json; charset=utf-8"):
            data = json.dumps(payload, allow_nan=False).encode() if isinstance(payload, dict) else payload
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Content-Security-Policy",
                             "default-src 'self'; script-src 'self'; style-src 'self'; "
                             "img-src 'self'; object-src 'none'; frame-ancestors 'none'")
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            request = urlsplit(self.path)
            try:
                if request.path in ASSETS:
                    filename, content_type = ASSETS[request.path]
                    self.respond(200, (STATIC / filename).read_bytes(), content_type)
                elif request.path == "/api/health":
                    self.respond(200, {"status": "ok", "dataset": store.metadata()})
                elif request.path == "/api/options":
                    self.respond(200, store.options())
                elif request.path == "/api/analyze":
                    arguments = parse_qs(request.query, keep_blank_values=True)
                    if set(arguments) - {"team", "player", "opponent", "threshold"}:
                        raise ValueError("Unknown analysis parameter")
                    if any(len(values) != 1 for values in arguments.values()):
                        raise ValueError("Supply each parameter once")
                    values = {key: value[0] for key, value in arguments.items()}
                    threshold = float(values.get("threshold", "20.5"))
                    self.respond(200, analyze(store, values.get("team", ""),
                                              values.get("player") or None,
                                              values.get("opponent") or None, threshold))
                else:
                    self.respond(404, {"error": "Not found"})
            except ValueError as error:
                self.respond(400, {"error": str(error)})

        def log_message(self, format_string, *args):
            pass

    return ThreadingHTTPServer((host, port), Handler)
