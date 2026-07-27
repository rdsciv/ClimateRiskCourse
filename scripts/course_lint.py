#!/usr/bin/env python3
"""Validate course structure: exercise folders, nonempty readmes, no broken relative links."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from course_manifest import SECTIONS  # noqa: E402

LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def main() -> int:
    errors: list[str] = []
    exercises_root = ROOT / "exercises"
    if not exercises_root.is_dir():
        errors.append("missing exercises/")

    for section in SECTIONS:
        sec_dir = exercises_root / section["id"]
        if not sec_dir.is_dir():
            errors.append(f"missing section {section['id']}")
            continue
        for ex in section["exercises"]:
            ex_dir = sec_dir / ex["id"]
            if not ex_dir.is_dir():
                errors.append(f"missing exercise {section['id']}/{ex['id']}")
                continue
            variants = set(ex["variants"])
            if not (variants & {"problem", "explainer", "solution"}):
                errors.append(f"{ex['id']}: no primary variant")
            primary = None
            for pref in ("problem", "explainer", "solution"):
                if pref in variants and (ex_dir / pref).is_dir():
                    primary = pref
                    break
            if primary is None:
                # allow solution-only if listed, but require at least one listed folder
                for v in variants:
                    if (ex_dir / v).is_dir():
                        primary = v
                        break
            if primary is None:
                errors.append(f"{ex['id']}: no variant folders present")
                continue
            for v in variants:
                vdir = ex_dir / v
                if not vdir.is_dir():
                    errors.append(f"{ex['id']}: missing variant folder {v}/")
                    continue
                readme = vdir / "readme.md"
                if not readme.is_file():
                    errors.append(f"{ex['id']}/{v}: missing readme.md")
                    continue
                text = readme.read_text(encoding="utf-8").strip()
                if not text:
                    errors.append(f"{ex['id']}/{v}: empty readme.md")
                if "speaker-notes" in text.lower() and "speaker-notes.md" in text:
                    pass
                for m in LINK_RE.finditer(text):
                    href = m.group(2).split("#", 1)[0].split("?", 1)[0]
                    if not href or href.startswith(("http://", "https://", "mailto:")):
                        continue
                    target = (vdir / href).resolve()
                    try:
                        target.relative_to(ROOT.resolve())
                    except ValueError:
                        # outside root — still check exists
                        pass
                    if not target.exists():
                        # also try relative to exercise and repo root
                        alt = (ex_dir / href).resolve()
                        alt2 = (ROOT / href).resolve()
                        if not alt.exists() and not alt2.exists():
                            errors.append(f"{ex['id']}/{v}: broken link {href}")

            # ban .gitkeep and speaker-notes.md in exercise trees
            for p in ex_dir.rglob("*"):
                if p.name == ".gitkeep":
                    errors.append(f"forbidden .gitkeep: {p.relative_to(ROOT)}")
                if p.name == "speaker-notes.md":
                    errors.append(f"forbidden speaker-notes.md: {p.relative_to(ROOT)}")

    required = [
        "README.md",
        "AGENTS.md",
        "firm/methodology.md",
        "clients/README.md",
        "clients/colorado-river-reservoirs/briefing/engagement.md",
        "clients/kerrville-flood/briefing/engagement.md",
        "clients/texas-datacenter-eis/briefing/engagement.md",
    ]
    for rel in required:
        if not (ROOT / rel).is_file():
            errors.append(f"missing required file: {rel}")

    if errors:
        print(f"FAIL — {len(errors)} issue(s):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("OK — course structure lint passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
