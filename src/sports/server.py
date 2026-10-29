"""Demonstration HTTP server with FastAPI + Pydantic validation and standard library compatibility."""

from __future__ import annotations

import json
import logging
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlsplit

from .analytics import analyze
from .config import CONFIG
from .model import analyze_model

try:
    from fastapi import FastAPI, Request, Response
    from pydantic import BaseModel, Field, ValidationError
except ImportError:
    FastAPI = None
    BaseModel = object

logger = logging.getLogger("sports.server")

STATIC = Path(__file__).resolve().parent / "web"
ASSETS = {
    "/": ("index.html", "text/html; charset=utf-8"),
    "/app.js": ("app.js", "text/javascript; charset=utf-8"),
    "/style.css": ("style.css", "text/css; charset=utf-8"),
}
ALLOWED_PARAMS = {"team", "player", "opponent", "threshold"}
SECURITY_HEADERS = {
    "Cache-Control": "no-store",
    "X-Content-Type-Options": "nosniff",
    "Content-Security-Policy": (
        "default-src 'self'; script-src 'self'; style-src 'self'; "
        "img-src 'self'; object-src 'none'; frame-ancestors 'none'"
    ),
}

if FastAPI is not None:
    class AnalysisQuery(BaseModel):
        team: str = Field(default="")
        player: str | None = Field(default=None)
        opponent: str | None = Field(default=None)
        threshold: float = Field(default=float(CONFIG["default_player_threshold"]))


def _parse_single_query_args(query_string: str, default_threshold: float) -> dict[str, Any]:
    arguments = parse_qs(query_string, keep_blank_values=True)
    if set(arguments) - ALLOWED_PARAMS:
        raise ValueError("Unknown analysis parameter")
    if any(len(values) != 1 for values in arguments.values()):
        raise ValueError("Supply each parameter once")
    values = {key: value[0] for key, value in arguments.items()}
    threshold = float(values.get("threshold", str(default_threshold)))
    params = {
        "team": values.get("team", ""),
        "player": values.get("player") or None,
        "opponent": values.get("opponent") or None,
        "threshold": threshold,
    }
    if FastAPI is not None:
        validated = AnalysisQuery(**params)
        return validated.model_dump()
    return params


def create_app(store) -> Any:
    """Create the FastAPI application with Pydantic query validation and Swagger docs."""
    if FastAPI is None:
        raise RuntimeError("FastAPI is not installed")

    app = FastAPI(
        title="SPORTSSTATS API",
        description="Basketball threshold rate and online logistic probability forecasting API",
        version="0.2.0",
    )

    def _json_response(status_code: int, payload: dict[str, Any]) -> Response:
        data = json.dumps(payload, allow_nan=False).encode("utf-8")
        return Response(
            content=data,
            status_code=status_code,
            media_type="application/json; charset=utf-8",
            headers=SECURITY_HEADERS,
        )

    @app.get("/", include_in_schema=False)
    @app.get("/app.js", include_in_schema=False)
    @app.get("/style.css", include_in_schema=False)
    async def serve_asset(request: Request) -> Response:
        filename, content_type = ASSETS[request.url.path]
        data = (STATIC / filename).read_bytes()
        return Response(content=data, status_code=200, media_type=content_type, headers=SECURITY_HEADERS)

    @app.get("/api/health")
    async def health() -> Response:
        return _json_response(200, {"status": "ok", "dataset": store.metadata()})

    @app.get("/api/options")
    async def options() -> Response:
        return _json_response(200, store.options())

    @app.get("/api/analyze")
    async def api_analyze(request: Request) -> Response:
        try:
            default_t = float(CONFIG["default_player_threshold"])
            params = _parse_single_query_args(request.url.query, default_t)
            result = analyze(store, params["team"], params["player"], params["opponent"], params["threshold"])
            return _json_response(200, result)
        except (ValueError, ValidationError) as error:
            return _json_response(400, {"error": str(error)})

    @app.get("/api/model")
    async def api_model(request: Request) -> Response:
        try:
            default_t = float(CONFIG["default_model_threshold"])
            params = _parse_single_query_args(request.url.query, default_t)
            result = analyze_model(store, params["team"], params["player"], params["opponent"], params["threshold"])
            return _json_response(200, result)
        except (ValueError, ValidationError) as error:
            return _json_response(400, {"error": str(error)})

    return app


def make_server(store, host=None, port=None):
    if host is None:
        host = str(CONFIG["host"])
    if port is None:
        port = int(CONFIG["port"])

    class Handler(BaseHTTPRequestHandler):
        def respond(self, status, payload, content_type="application/json; charset=utf-8"):
            data = json.dumps(payload, allow_nan=False).encode() if isinstance(payload, dict) else payload
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(data)))
            for header_name, header_val in SECURITY_HEADERS.items():
                self.send_header(header_name, header_val)
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
                elif request.path in {"/api/analyze", "/api/model"}:
                    default_t = (
                        float(CONFIG["default_model_threshold"])
                        if request.path == "/api/model"
                        else float(CONFIG["default_player_threshold"])
                    )
                    params = _parse_single_query_args(request.query, default_t)
                    operation = analyze_model if request.path == "/api/model" else analyze
                    self.respond(
                        200,
                        operation(
                            store,
                            params["team"],
                            params["player"],
                            params["opponent"],
                            params["threshold"],
                        ),
                    )
                else:
                    self.respond(404, {"error": "Not found"})
            except ValueError as error:
                self.respond(400, {"error": str(error)})

        def log_message(self, format_string, *args):
            logger.info("%s - %s", self.address_string(), format_string % args)

    return ThreadingHTTPServer((host, port), Handler)
