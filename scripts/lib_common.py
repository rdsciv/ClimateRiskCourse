"""Shared helpers for seed scripts and analysis utilities."""

from __future__ import annotations

import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TRACK_FOLDERS = {
    "ironwood": "ironwood-bank",
    "strata": "strata-holdings",
    "northwood": "northwood-capital",
}


def repo_root() -> Path:
    return ROOT


def client_dir(track: str) -> Path:
    folder = TRACK_FOLDERS.get(track, track)
    return ROOT / "clients" / folder


def active_track() -> str:
    env = os.environ.get("CLIENT_TRACK", "").strip()
    if env in TRACK_FOLDERS:
        return env
    env_file = ROOT / ".env"
    if env_file.is_file():
        for line in env_file.read_text().splitlines():
            if line.startswith("CLIENT_TRACK="):
                val = line.split("=", 1)[1].strip()
                if val in TRACK_FOLDERS:
                    return val
    link = ROOT / "clients" / "active"
    if link.is_symlink():
        name = link.resolve().name
        for k, v in TRACK_FOLDERS.items():
            if v == name:
                return k
    return "ironwood"


def connect_db(track: str) -> sqlite3.Connection:
    path = client_dir(track) / "db" / "portfolio.sqlite"
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def append_audit(track: str, event: dict) -> None:
    out = client_dir(track) / "outputs"
    out.mkdir(parents=True, exist_ok=True)
    path = out / "audit_log.jsonl"
    payload = {
        "ts": datetime.now(timezone.utc).isoformat(),
        **event,
    }
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload) + "\n")


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
