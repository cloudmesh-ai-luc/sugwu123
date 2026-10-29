"""Centralized configuration loader for SPORTSSTATS (config.yaml + env overrides)."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    yaml = None

CONFIG_PATH = Path(__file__).resolve().parent / "config.yaml"

DEFAULTS: dict[str, Any] = {
    "learning_rate": 0.05,
    "feature_scale": 20.0,
    "training_starts_after": 5,
    "minimum_history": 10,
    "default_model_threshold": 100.5,
    "default_player_threshold": 20.5,
    "default_team": "CHI",
    "host": "127.0.0.1",
    "port": 8000,
    "bootstrap_script": "install-guest.sh",
}


def load_config(path: Path | None = None) -> dict[str, Any]:
    """Load configuration from config.yaml with environment variable overrides."""
    cfg = dict(DEFAULTS)
    target = Path(path) if path else CONFIG_PATH
    if yaml is not None and target.exists():
        raw = yaml.safe_load(target.read_text(encoding="utf-8")) or {}
        for section in ("model", "server", "cloud"):
            if isinstance(raw.get(section), dict):
                cfg.update(raw[section])
    if "SPORTS_LEARNING_RATE" in os.environ:
        cfg["learning_rate"] = float(os.environ["SPORTS_LEARNING_RATE"])
    if "SPORTS_MODEL_THRESHOLD" in os.environ:
        cfg["default_model_threshold"] = float(os.environ["SPORTS_MODEL_THRESHOLD"])
    if "SPORTS_PLAYER_THRESHOLD" in os.environ:
        cfg["default_player_threshold"] = float(os.environ["SPORTS_PLAYER_THRESHOLD"])
    if "SPORTS_PORT" in os.environ:
        cfg["port"] = int(os.environ["SPORTS_PORT"])
    return cfg


CONFIG = load_config()
