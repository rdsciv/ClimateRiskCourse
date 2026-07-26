#!/usr/bin/env python3
"""Minimal markdown → HTML export for week-6 deliverables."""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def md_to_html(md: str, title: str) -> str:
    lines = md.splitlines()
    body: list[str] = []
    in_code = False
    in_list = False
    for line in lines:
        if line.startswith("```"):
            if in_code:
                body.append("</code></pre>")
                in_code = False
            else:
                body.append("<pre><code>")
                in_code = True
            continue
        if in_code:
            body.append(html.escape(line))
            continue
        if line.startswith("# "):
            if in_list:
                body.append("</ul>")
                in_list = False
            body.append(f"<h1>{html.escape(line[2:])}</h1>")
        elif line.startswith("## "):
            if in_list:
                body.append("</ul>")
                in_list = False
            body.append(f"<h2>{html.escape(line[3:])}</h2>")
        elif line.startswith("### "):
            if in_list:
                body.append("</ul>")
                in_list = False
            body.append(f"<h3>{html.escape(line[4:])}</h3>")
        elif re.match(r"^[-*] ", line):
            if not in_list:
                body.append("<ul>")
                in_list = True
            body.append(f"<li>{html.escape(line[2:])}</li>")
        elif line.strip() == "":
            if in_list:
                body.append("</ul>")
                in_list = False
            body.append("")
        else:
            if in_list:
                body.append("</ul>")
                in_list = False
            body.append(f"<p>{html.escape(line)}</p>")
    if in_list:
        body.append("</ul>")
    if in_code:
        body.append("</code></pre>")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>{html.escape(title)}</title>
  <style>
    body {{ font-family: system-ui, sans-serif; max-width: 800px; margin: 2rem auto; padding: 0 1rem; line-height: 1.5; color: #122; }}
    h1,h2,h3 {{ line-height: 1.2; }}
    .banner {{ background: #fff3cd; border: 1px solid #e6c200; padding: .75rem 1rem; margin-bottom: 1.5rem; }}
    pre {{ background: #f4f4f5; padding: 1rem; overflow: auto; }}
    table {{ border-collapse: collapse; }}
  </style>
</head>
<body>
  <div class="banner"><strong>SIMULATED TRAINING DATA</strong> — Not a real client deliverable.</div>
  {"".join(body)}
</body>
</html>
"""


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("input", type=Path, help="Markdown file")
    p.add_argument("-o", "--output", type=Path, help="HTML output path")
    p.add_argument("--title", default="Climate Risk Deliverable")
    args = p.parse_args()
    md = args.input.read_text(encoding="utf-8")
    out = args.output or args.input.with_suffix(".html")
    out.write_text(md_to_html(md, args.title), encoding="utf-8")
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
