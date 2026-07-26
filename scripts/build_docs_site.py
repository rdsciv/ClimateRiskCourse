#!/usr/bin/env python3
"""Build docs/ reading pages from firm markdown and exercise explainers."""

from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
READING = DOCS / "reading"

NAV = """
  <header class="nav">
    <div class="wrap nav-inner">
      <a class="brand" href="../index.html"><span class="mark">CR</span><span>Climate Risk Course</span></a>
      <nav class="nav-links">
        <a href="../curriculum.html">Curriculum</a>
        <a href="../clients.html">Clients</a>
        <a href="../methodology.html">Methodology</a>
        <a href="../reading.html">Reading</a>
        <a href="../getting-started.html">Get started</a>
        <a class="nav-cta" href="https://github.com/rdsciv/ClimateRiskCourse">GitHub</a>
      </nav>
    </div>
  </header>
"""

NAV_ROOT = NAV.replace("../", "")


def md_inline(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    return text


def md_to_html(md: str) -> str:
    lines = md.splitlines()
    out: list[str] = []
    i = 0
    in_code = False
    code_buf: list[str] = []
    in_ul = False
    in_ol = False
    in_table = False

    def close_lists() -> None:
        nonlocal in_ul, in_ol
        if in_ul:
            out.append("</ul>")
            in_ul = False
        if in_ol:
            out.append("</ol>")
            in_ol = False

    def close_table() -> None:
        nonlocal in_table
        if in_table:
            out.append("</tbody></table></div>")
            in_table = False

    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            close_lists()
            close_table()
            if in_code:
                out.append("<pre><code>" + html.escape("\n".join(code_buf)) + "</code></pre>")
                code_buf = []
                in_code = False
            else:
                in_code = True
            i += 1
            continue
        if in_code:
            code_buf.append(line)
            i += 1
            continue

        if re.match(r"^\|", line) and i + 1 < len(lines) and re.match(r"^\|[\s\-:|]+$", lines[i + 1]):
            close_lists()
            headers = [c.strip() for c in line.strip("|").split("|")]
            i += 2
            out.append('<div class="table-wrap"><table><thead><tr>')
            for h in headers:
                out.append(f"<th>{md_inline(h)}</th>")
            out.append("</tr></thead><tbody>")
            in_table = True
            while i < len(lines) and re.match(r"^\|", lines[i]):
                cells = [c.strip() for c in lines[i].strip("|").split("|")]
                out.append("<tr>")
                for c in cells:
                    out.append(f"<td>{md_inline(c)}</td>")
                out.append("</tr>")
                i += 1
            close_table()
            continue

        if line.startswith("# "):
            close_lists()
            close_table()
            # skip top H1 — page hero uses title
            i += 1
            continue
        if line.startswith("## "):
            close_lists()
            close_table()
            out.append(f"<h2 id=\"{slug(line[3:])}\">{md_inline(line[3:])}</h2>")
        elif line.startswith("### "):
            close_lists()
            close_table()
            out.append(f"<h3 id=\"{slug(line[4:])}\">{md_inline(line[4:])}</h3>")
        elif re.match(r"^[-*] ", line):
            close_table()
            if in_ol:
                out.append("</ol>")
                in_ol = False
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{md_inline(line[2:])}</li>")
        elif re.match(r"^\d+\. ", line):
            close_table()
            if in_ul:
                out.append("</ul>")
                in_ul = False
            if not in_ol:
                out.append("<ol>")
                in_ol = True
            item = re.sub(r"^\d+\. ", "", line)
            out.append(f"<li>{md_inline(item)}</li>")
        elif line.startswith("> "):
            close_lists()
            close_table()
            out.append(f"<blockquote>{md_inline(line[2:])}</blockquote>")
        elif line.strip() == "":
            close_lists()
            close_table()
        elif line.strip() == "---":
            close_lists()
            close_table()
            out.append("<hr />")
        else:
            close_lists()
            close_table()
            out.append(f"<p>{md_inline(line)}</p>")
        i += 1

    close_lists()
    close_table()
    if in_code:
        out.append("<pre><code>" + html.escape("\n".join(code_buf)) + "</code></pre>")
    return "\n".join(out)


def slug(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    return re.sub(r"\s+", "-", s)


def page(title: str, subtitle: str, body_html: str, *, nested: bool = True) -> str:
    base = ".." if nested else "."
    nav = NAV if nested else NAV_ROOT
    css = f"{base}/assets/css/site.css" if nested else "assets/css/site.css"
    fav = f"{base}/assets/favicon.svg" if nested else "assets/favicon.svg"
    home = f"{base}/index.html" if nested else "index.html"
    reading = f"{base}/reading.html" if nested else "reading.html"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(title)} · Climate Risk Course</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="{css}" />
  <link rel="icon" href="{fav}" type="image/svg+xml" />
</head>
<body>
{nav}
  <main class="wrap">
    <div class="page-hero">
      <h1>{html.escape(title)}</h1>
      <p>{html.escape(subtitle)}</p>
    </div>
    <div class="prose">
{body_html}
    </div>
    <p style="margin:2rem 0 3rem;color:var(--muted)">
      <a href="{reading}">← Reading room</a> · <a href="{home}">Home</a>
    </p>
  </main>
  <footer>
    <div class="wrap">
      <div>Climate Risk Course · Grok Build</div>
      <div><a href="{reading}">Reading</a></div>
    </div>
  </footer>
</body>
</html>
"""


def write_reading(slug_name: str, title: str, subtitle: str, md_path: Path) -> Path:
    md = md_path.read_text(encoding="utf-8")
    out = READING / f"{slug_name}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page(title, subtitle, md_to_html(md)), encoding="utf-8")
    return out


def main() -> None:
    READING.mkdir(parents=True, exist_ok=True)
    items: list[tuple[str, str, str]] = []

    firm_pages = [
        ("methodology", "Firm methodology", "Decision-grade climate risk assessments", ROOT / "firm" / "methodology.md"),
        ("anchors", "Damage & LGD anchors", "Training anchors for computed scenario bands", ROOT / "firm" / "anchors" / "damage_and_lgd_bands.md"),
        ("deliverable-standards", "Deliverable standards", "Client-sendable form for every weekly output", ROOT / "firm" / "deliverable-standards" / "README.md"),
        ("qa-protocols", "QA protocols", "Re-run, lineage, label, gap, and scenario tests", ROOT / "firm" / "qa-protocols" / "README.md"),
        ("sample-hazard", "Sample hazard grids", "Offline firm_sample_grid v1", ROOT / "firm" / "sample-hazard" / "README.md"),
    ]
    for slug_name, title, sub, path in firm_pages:
        if path.is_file():
            write_reading(slug_name, title, sub, path)
            items.append((f"reading/{slug_name}.html", title, sub))

    # scenario cards
    cards_dir = ROOT / "firm" / "scenario-cards"
    for card in sorted(cards_dir.glob("*.md")):
        if card.name == "README.md":
            continue
        slug_name = f"scenario-{card.stem.lower()}"
        title = card.stem
        write_reading(slug_name, title, "Firm scenario card", card)
        items.append((f"reading/{slug_name}.html", title, "Scenario card"))

    # explainer exercises
    for readme in sorted((ROOT / "exercises").rglob("explainer/readme.md")):
        rel = readme.relative_to(ROOT / "exercises")
        # exercises/01-the-client/01.01-foo/explainer/readme.md
        parts = rel.parts
        section = parts[0]
        ex_id = parts[1]
        slug_name = f"ex-{ex_id}"
        title = ex_id
        # get first H1 from file
        text = readme.read_text(encoding="utf-8")
        m = re.search(r"^#\s+(.+)$", text, re.M)
        if m:
            title = m.group(1).strip()
        write_reading(slug_name, title, f"Exercise explainer · {section}", readme)
        items.append((f"reading/{slug_name}.html", title, section))

    # agents + clients readme
    write_reading("agents", "Root AGENTS.md", "Firm-level Grok brief for every session", ROOT / "AGENTS.md")
    items.insert(0, ("reading/agents.html", "Root AGENTS.md", "Project rules"))
    write_reading("clients-overview", "Clients overview", "How to choose a track", ROOT / "clients" / "README.md")
    items.insert(1, ("reading/clients-overview.html", "Clients overview", "Tracks"))

    # methodology page at docs root (mirror)
    meth = (ROOT / "firm" / "methodology.md").read_text(encoding="utf-8")
    (DOCS / "methodology.html").write_text(
        page(
            "Methodology",
            "The house brain: decisions, epistemology, scenarios, dual audiences.",
            md_to_html(meth),
            nested=False,
        ).replace('href="reading.html"', 'href="reading.html"'),
        encoding="utf-8",
    )

    # reading index
    rows = "\n".join(
        f'<tr><td><a href="{html.escape(href)}">{html.escape(title)}</a></td>'
        f"<td>{html.escape(desc)}</td></tr>"
        for href, title, desc in items
    )
    reading_index = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Reading · Climate Risk Course</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="assets/css/site.css" />
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml" />
</head>
<body>
{NAV_ROOT}
  <main class="wrap">
    <div class="page-hero">
      <h1>Reading room</h1>
      <p>Firm methodology, scenario cards, and exercise explainers — rendered for the web.</p>
    </div>
    <div class="banner">Problems and solutions stay in the repo for hands-on work with Grok Build. This room is for study and reference.</div>
    <div class="table-wrap" style="margin-bottom:3rem">
      <table>
        <thead><tr><th>Document</th><th>Section</th></tr></thead>
        <tbody>
{rows}
        </tbody>
      </table>
    </div>
  </main>
  <footer>
    <div class="wrap">
      <div>Climate Risk Course · Grok Build</div>
      <div><a href="getting-started.html">Get started</a></div>
    </div>
  </footer>
</body>
</html>
"""
    (DOCS / "reading.html").write_text(reading_index, encoding="utf-8")
    print(f"Built {len(items)} reading pages + methodology.html + reading.html")


if __name__ == "__main__":
    main()
