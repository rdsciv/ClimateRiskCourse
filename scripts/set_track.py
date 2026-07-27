#!/usr/bin/env python3
"""Set the active client track via .env CLIENT_TRACK and clients/active symlink."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKS = {
    "colorado": "colorado-river-reservoirs",
    "kerrville": "kerrville-flood",
    "datacenter": "texas-datacenter-eis",
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Set active client track")
    parser.add_argument(
        "track",
        nargs="?",
        choices=list(TRACKS.keys()),
        help="colorado | kerrville | datacenter",
    )
    args = parser.parse_args()
    if not args.track:
        print("Tracks:")
        for k, folder in TRACKS.items():
            print(f"  {k:12} -> clients/{folder}")
        env_path = ROOT / ".env"
        current = os.environ.get("CLIENT_TRACK", "")
        if env_path.is_file():
            for line in env_path.read_text().splitlines():
                if line.startswith("CLIENT_TRACK="):
                    current = line.split("=", 1)[1].strip()
        print(f"\nCurrent CLIENT_TRACK: {current or '(unset)'}")
        return 0

    folder = TRACKS[args.track]
    target = ROOT / "clients" / folder
    if not target.is_dir():
        print(f"error: missing {target} — run scripts/seed_all_clients.py first", file=sys.stderr)
        return 1

    env_path = ROOT / ".env"
    lines: list[str] = []
    if env_path.is_file():
        lines = env_path.read_text().splitlines()
        lines = [ln for ln in lines if not ln.startswith("CLIENT_TRACK=")]
    lines.append(f"CLIENT_TRACK={args.track}")
    env_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    link = ROOT / "clients" / "active"
    if link.is_symlink() or link.exists():
        link.unlink()
    link.symlink_to(folder)

    print(f"Active track: {args.track} -> clients/{folder}")
    print(f"Wrote CLIENT_TRACK to .env and clients/active -> {folder}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
