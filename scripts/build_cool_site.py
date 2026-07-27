#!/usr/bin/env python3
"""Build a high-energy static docs site into site/ for GitHub Pages."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "site"

CSS = r"""
:root {
  --bg: #05080f;
  --bg2: #0a1220;
  --card: rgba(16, 28, 48, 0.72);
  --stroke: rgba(140, 170, 210, 0.16);
  --text: #edf3ff;
  --muted: #93a4bd;
  --mint: #2ee6a6;
  --mint2: #7cffd4;
  --blue: #5b8cff;
  --amber: #ffc14d;
  --pink: #ff6bcb;
  --radius: 18px;
  --font: "Space Grotesk", "IBM Plex Sans", system-ui, sans-serif;
  --mono: "IBM Plex Mono", ui-monospace, monospace;
  --max: 1120px;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  color: var(--text);
  font-family: var(--font);
  line-height: 1.6;
  background: var(--bg);
  min-height: 100vh;
  overflow-x: hidden;
}
body::before {
  content: "";
  position: fixed; inset: 0; z-index: -2;
  background:
    radial-gradient(900px 520px at 8% -8%, rgba(46,230,166,.22), transparent 55%),
    radial-gradient(800px 480px at 92% 0%, rgba(91,140,255,.20), transparent 50%),
    radial-gradient(700px 500px at 50% 110%, rgba(255,107,203,.10), transparent 45%),
    linear-gradient(180deg, #05080f 0%, #070d18 50%, #05080f 100%);
}
body::after {
  content: "";
  position: fixed; inset: 0; z-index: -1; pointer-events: none;
  background-image:
    linear-gradient(rgba(255,255,255,.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,.03) 1px, transparent 1px);
  background-size: 48px 48px;
  mask-image: radial-gradient(ellipse at center, black 20%, transparent 75%);
  opacity: .55;
}
a { color: var(--mint); text-decoration: none; }
a:hover { color: var(--mint2); }
.wrap { width: min(var(--max), calc(100% - 2rem)); margin: 0 auto; }

/* NAV */
.nav {
  position: sticky; top: 0; z-index: 50;
  backdrop-filter: blur(16px) saturate(1.2);
  background: rgba(5,8,15,.72);
  border-bottom: 1px solid var(--stroke);
}
.nav-inner {
  display: flex; align-items: center; justify-content: space-between;
  gap: 1rem; padding: .85rem 0;
}
.brand {
  display: flex; align-items: center; gap: .7rem;
  color: var(--text); font-weight: 700; letter-spacing: -.01em;
}
.brand:hover { color: var(--text); }
.mark {
  width: 36px; height: 36px; border-radius: 11px;
  background: linear-gradient(135deg, var(--mint), var(--blue));
  display: grid; place-items: center; color: #041018; font-weight: 800; font-size: .85rem;
  box-shadow: 0 0 24px rgba(46,230,166,.35);
}
.nav-links { display: flex; flex-wrap: wrap; gap: .35rem 1rem; align-items: center; }
.nav-links a { color: var(--muted); font-size: .94rem; font-weight: 500; }
.nav-links a:hover, .nav-links a.active { color: var(--text); }
.nav-cta {
  border: 1px solid rgba(46,230,166,.45) !important;
  background: linear-gradient(135deg, rgba(46,230,166,.18), rgba(91,140,255,.12));
  color: var(--mint2) !important;
  padding: .42rem .85rem; border-radius: 999px; font-weight: 700 !important;
}

/* HERO */
.hero { padding: 4.5rem 0 2.5rem; position: relative; }
.eyebrow {
  display: inline-flex; align-items: center; gap: .5rem;
  font-size: .78rem; font-weight: 700; letter-spacing: .12em; text-transform: uppercase;
  color: var(--mint); margin-bottom: 1rem;
  padding: .35rem .7rem; border-radius: 999px;
  border: 1px solid rgba(46,230,166,.28);
  background: rgba(46,230,166,.08);
}
.hero h1 {
  font-size: clamp(2.6rem, 6.5vw, 4.2rem);
  line-height: 1.02; letter-spacing: -.04em; margin: 0 0 1.1rem;
  max-width: 14ch;
  background: linear-gradient(120deg, #fff 10%, var(--mint2) 45%, var(--blue) 90%);
  -webkit-background-clip: text; background-clip: text; color: transparent;
}
.lede { font-size: 1.18rem; color: var(--muted); max-width: 48ch; margin: 0 0 1.75rem; }
.actions { display: flex; flex-wrap: wrap; gap: .75rem; margin-bottom: 2.2rem; }
.btn {
  display: inline-flex; align-items: center; gap: .45rem;
  padding: .85rem 1.2rem; border-radius: 999px; font-weight: 700;
  border: 1px solid transparent;
}
.btn-primary {
  background: linear-gradient(135deg, var(--mint), #1bbf8c);
  color: #041018 !important;
  box-shadow: 0 10px 30px rgba(46,230,166,.28);
}
.btn-primary:hover { filter: brightness(1.05); color: #041018 !important; }
.btn-ghost {
  border-color: var(--stroke); color: var(--text) !important;
  background: rgba(255,255,255,.03);
}
.stats {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: .75rem; max-width: 760px;
}
.stat {
  padding: 1rem; border-radius: var(--radius);
  border: 1px solid var(--stroke);
  background: linear-gradient(180deg, rgba(255,255,255,.05), transparent 55%), var(--card);
  backdrop-filter: blur(10px);
}
.stat strong {
  display: block; font-size: 1.55rem; letter-spacing: -.02em;
  background: linear-gradient(90deg, var(--mint2), var(--blue));
  -webkit-background-clip: text; background-clip: text; color: transparent;
}
.stat span { color: var(--muted); font-size: .9rem; }

/* SECTIONS */
section { padding: 2.4rem 0; }
.section-title {
  margin: 0 0 .35rem; font-size: clamp(1.5rem, 3vw, 2rem);
  letter-spacing: -.025em;
}
.section-sub { color: var(--muted); margin: 0 0 1.4rem; max-width: 58ch; }
.grid-3 {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1rem;
}
.card {
  position: relative; overflow: hidden;
  background: linear-gradient(165deg, rgba(255,255,255,.06), transparent 42%), var(--card);
  border: 1px solid var(--stroke);
  border-radius: calc(var(--radius) + 2px);
  padding: 1.25rem 1.3rem;
  backdrop-filter: blur(12px);
  transition: transform .18s ease, border-color .18s ease, box-shadow .18s ease;
}
.card:hover {
  transform: translateY(-3px);
  border-color: rgba(46,230,166,.35);
  box-shadow: 0 20px 50px rgba(0,0,0,.35), 0 0 0 1px rgba(46,230,166,.08);
}
.card .tag {
  display: inline-block; font-size: .72rem; font-weight: 800;
  letter-spacing: .08em; text-transform: uppercase;
  color: var(--blue); margin-bottom: .5rem;
}
.card h3 { margin: 0 0 .4rem; font-size: 1.12rem; letter-spacing: -.01em; }
.card p { margin: 0; color: var(--muted); }
.card a.stretch { position: absolute; inset: 0; }

/* TIMELINE */
.timeline { display: grid; gap: .7rem; }
.week {
  display: grid; grid-template-columns: 96px 1fr; gap: 1rem;
  border: 1px solid var(--stroke); border-radius: var(--radius);
  background: var(--card); padding: 1rem 1.15rem;
  transition: border-color .15s ease;
}
.week:hover { border-color: rgba(91,140,255,.4); }
.week-num {
  font-weight: 800; color: var(--mint);
  font-size: .95rem; letter-spacing: .04em;
}
.week h3 { margin: 0 0 .2rem; font-size: 1.05rem; }
.week p { margin: 0; color: var(--muted); font-size: .95rem; }

/* PROSE */
.page-hero {
  padding: 2.8rem 0 1.2rem;
  border-bottom: 1px solid var(--stroke);
  margin-bottom: 1.5rem;
}
.page-hero h1 {
  margin: 0 0 .5rem; font-size: clamp(2rem, 4vw, 2.8rem);
  letter-spacing: -.03em;
}
.page-hero p { margin: 0; color: var(--muted); max-width: 62ch; }
.prose {
  background: var(--card);
  border: 1px solid var(--stroke);
  border-radius: calc(var(--radius) + 4px);
  padding: 1.5rem 1.6rem 2rem;
  backdrop-filter: blur(10px);
}
.prose h2 {
  margin-top: 1.7rem; padding-top: .5rem;
  border-top: 1px solid var(--stroke);
  font-size: 1.3rem; letter-spacing: -.02em;
}
.prose h2:first-child { margin-top: 0; border: 0; padding-top: 0; }
.prose h3 { margin-top: 1.2rem; }
.prose p, .prose li { color: #d4deef; }
.prose code, code {
  font-family: var(--mono); font-size: .88em;
  background: rgba(46,230,166,.1);
  border: 1px solid rgba(46,230,166,.18);
  padding: .1rem .35rem; border-radius: 6px; color: var(--mint2);
}
.prose pre {
  font-family: var(--mono); font-size: .86rem;
  background: #04070e; border: 1px solid var(--stroke);
  border-radius: 12px; padding: 1rem; overflow-x: auto; color: #d7e3f4;
}
.prose pre code { background: none; border: 0; padding: 0; color: inherit; }
.banner {
  background: rgba(255,193,77,.1);
  border: 1px solid rgba(255,193,77,.35);
  color: #ffe2a0;
  padding: .8rem 1rem; border-radius: 12px; margin: 1rem 0;
}
.table-wrap {
  overflow-x: auto; border: 1px solid var(--stroke);
  border-radius: var(--radius); background: rgba(0,0,0,.25);
}
table { width: 100%; border-collapse: collapse; font-size: .95rem; }
th, td {
  text-align: left; padding: .85rem 1rem;
  border-bottom: 1px solid var(--stroke); vertical-align: top;
}
th { color: var(--muted); font-weight: 600; background: rgba(255,255,255,.02); }
tr:last-child td { border-bottom: 0; }

footer {
  border-top: 1px solid var(--stroke);
  padding: 2rem 0 3rem; color: var(--muted); font-size: .92rem; margin-top: 2rem;
}
footer .wrap {
  display: flex; flex-wrap: wrap; justify-content: space-between; gap: 1rem;
}

@media (max-width: 720px) {
  .week { grid-template-columns: 1fr; }
}
"""

NAV_LINKS = [
    ("index.html", "Home"),
    ("quickstart.html", "Quickstart"),
    ("curriculum.html", "Curriculum"),
    ("clients.html", "Clients"),
    ("methodology.html", "Method"),
]


def nav(active: str) -> str:
    links = []
    for href, label in NAV_LINKS:
        cls = ' class="active"' if href == active else ""
        links.append(f'<a href="{href}"{cls}>{label}</a>')
    return f"""
<header class="nav">
  <div class="wrap nav-inner">
    <a class="brand" href="index.html"><span class="mark">CR</span><span>Climate Risk Course</span></a>
    <nav class="nav-links">
      {"".join(links)}
      <a class="nav-cta" href="https://github.com/rdsciv/ClimateRiskCourse" target="_blank" rel="noopener">GitHub</a>
    </nav>
  </div>
</header>
"""


def page(title: str, active: str, body: str, description: str = "") -> str:
    desc = description or title
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>{title} · Climate Risk Course</title>
  <meta name="description" content="{desc}"/>
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet"/>
  <link rel="stylesheet" href="assets/site.css"/>
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml"/>
</head>
<body>
{nav(active)}
<main>
{body}
</main>
<footer>
  <div class="wrap">
    <div><strong style="color:var(--text)">Climate Risk Course</strong><br/>Mintlify source in <code>docs/</code> · Grok Build training</div>
    <div><a href="quickstart.html">Quickstart</a> · <a href="https://github.com/rdsciv/ClimateRiskCourse">Repo</a></div>
  </div>
</footer>
</body>
</html>
"""


def write(name: str, title: str, body: str, description: str = "") -> None:
    (OUT / name).write_text(page(title, name, body, description), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "assets").mkdir(exist_ok=True)
    (OUT / "assets" / "site.css").write_text(CSS, encoding="utf-8")
    fav = ROOT / "docs" / "favicon.svg"
    if fav.is_file():
        (OUT / "assets" / "favicon.svg").write_text(fav.read_text(encoding="utf-8"), encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")

    write(
        "index.html",
        "Home",
        """
<section class="hero wrap">
  <div class="eyebrow">Grok Build · Six-week residency format</div>
  <h1>Climate risk, end to end.</h1>
  <p class="lede">Not a chat tutorial. A consulting engagement you run with Grok Build — hazard signal through to decisions your client can take.</p>
  <div class="actions">
    <a class="btn btn-primary" href="quickstart.html">Start Day 1 →</a>
    <a class="btn btn-ghost" href="curriculum.html">See curriculum</a>
  </div>
  <div class="stats">
    <div class="stat"><strong>6</strong><span>weeks · chained deliverables</span></div>
    <div class="stat"><strong>3</strong><span>original client tracks</span></div>
    <div class="stat"><strong>36</strong><span>guided exercises</span></div>
    <div class="stat"><strong>2</strong><span>capstone audiences</span></div>
  </div>
</section>

<section class="wrap">
  <h2 class="section-title">Pick your battlefield</h2>
  <p class="section-sub">Same method. Different decision language. Stay with one track through the capstone.</p>
  <div class="grid-3">
    <div class="card">
      <div class="tag">colorado</div>
      <h3>Colorado River reservoirs</h3>
      <p>Redrock Basin Authority. Drought ops, releases, allocations, hydropower contingency.</p>
      <a class="stretch" href="clients.html#colorado" aria-label="Colorado track"></a>
    </div>
    <div class="card">
      <div class="tag">kerrville</div>
      <h3>Kerrville flood risk</h3>
      <p>City of Kerrville. Critical facilities, access, mitigation priority, buyout vs defend.</p>
      <a class="stretch" href="clients.html#kerrville" aria-label="Kerrville track"></a>
    </div>
    <div class="card">
      <div class="tag">datacenter</div>
      <h3>Texas data center EIS</h3>
      <p>Horizon Grid. Alternatives analysis, water, power/grid, community receptors.</p>
      <a class="stretch" href="clients.html#datacenter" aria-label="Datacenter track"></a>
    </div>
  </div>
</section>

<section class="wrap">
  <h2 class="section-title">The engagement arc</h2>
  <p class="section-sub">Each week answers a question the client would pay for. Deliverables chain.</p>
  <div class="timeline">
    <article class="week"><div class="week-num">WEEK 1</div><div><h3>The Client</h3><p>Scope the engagement. Brief Grok. Ship framing &amp; delivery plan.</p></div></article>
    <article class="week"><div class="week-num">WEEK 2</div><div><h3>Portfolio mapping</h3><p>Geocode, classify, screen the book, form risk hypotheses.</p></div></article>
    <article class="week"><div class="week-num">WEEK 3</div><div><h3>Hazard data</h3><p>Pull and organize asset-level exposure with a full audit trail.</p></div></article>
    <article class="week"><div class="week-num">WEEK 4</div><div><h3>Scenarios</h3><p>Standard for the record. Bespoke for <em>this</em> book.</p></div></article>
    <article class="week"><div class="week-num">WEEK 5</div><div><h3>Synthesis</h3><p>Concentration, priorities, decision language, recommendations.</p></div></article>
    <article class="week"><div class="week-num">WEEK 6</div><div><h3>Delivery</h3><p>Board judgment pack + regulatory-style record with lineage.</p></div></article>
  </div>
</section>

<section class="wrap">
  <h2 class="section-title">Built for Grok Build</h2>
  <div class="grid-3">
    <div class="card"><h3>AGENTS.md + skills</h3><p>Firm brief and phase skills so every session inherits methodology, not vibes.</p></div>
    <div class="card"><h3>Computed vs judged</h3><p><code>uv run</code> scripts for re-runnable numbers. Judgment labeled with mechanism + precedent.</p></div>
    <div class="card"><h3>Assurable trail</h3><p>Audit logs, figure lineage, dual-audience packs that survive cold review.</p></div>
  </div>
</section>
""",
        "Six weeks to a climate risk assessment — Grok Build course.",
    )

    write(
        "quickstart.html",
        "Quickstart",
        """
<div class="wrap">
  <div class="page-hero">
    <h1>Quickstart</h1>
    <p>About 30 minutes. Exact clone URL. uv only. No system Python circus.</p>
  </div>
  <div class="prose">
    <h2>0. Install uv (once)</h2>
    <pre><code>curl -LsSf https://astral.sh/uv/install.sh | sh
uv --version</code></pre>
    <h2>1. Clone the course</h2>
    <p>Copy these two lines exactly:</p>
    <pre><code>git clone https://github.com/rdsciv/ClimateRiskCourse.git
cd ClimateRiskCourse</code></pre>
    <h2>2. Install with uv</h2>
    <pre><code>uv sync</code></pre>
    <div class="banner">Use <strong>uv run</strong> for every script. Do not call system python3 or pip.</div>
    <h2>3. Seed + pick a track</h2>
    <pre><code>uv run scripts/seed_all_clients.py
uv run scripts/set_track.py colorado   # or kerrville | datacenter
uv run scripts/course_lint.py</code></pre>
    <h2>4. Open Grok Build</h2>
    <p>In the <code>ClimateRiskCourse</code> folder, ask:</p>
    <pre><code>Summarize firm/methodology.md in five bullets.
Do not open any exercises/**/solution/ folders.</code></pre>
    <h2>5. Orientation</h2>
    <p>Work through <code>exercises/00-orientation/</code>, then week 1. Explainers → problems → solutions only after an honest attempt.</p>
  </div>
</div>
""",
    )

    write(
        "curriculum.html",
        "Curriculum",
        """
<div class="wrap">
  <div class="page-hero">
    <h1>Curriculum</h1>
    <p>Three phases: the client, the analysis, the delivery.</p>
  </div>
  <div class="table-wrap" style="margin-bottom:2rem">
    <table>
      <thead><tr><th>Week</th><th>Question</th><th>Deliverable</th></tr></thead>
      <tbody>
        <tr><td><strong>0</strong></td><td>How do I take this?</td><td>Environment + track</td></tr>
        <tr><td><strong>1</strong></td><td>What does the client need?</td><td>Framing &amp; delivery plan</td></tr>
        <tr><td><strong>2</strong></td><td>Where does risk concentrate?</td><td>Mapped book + hypotheses</td></tr>
        <tr><td><strong>3</strong></td><td>Which hazard data matters?</td><td>Hazard dataset + audit log</td></tr>
        <tr><td><strong>4</strong></td><td>Which scenarios bite?</td><td>Standard + bespoke results</td></tr>
        <tr><td><strong>5</strong></td><td>What should change?</td><td>Synthesis + decisions</td></tr>
        <tr><td><strong>6</strong></td><td>Will it stand up?</td><td>Board judgment + record</td></tr>
      </tbody>
    </table>
  </div>
  <div class="prose">
    <p>Hands-on exercises live in <code>exercises/</code> as explainer / problem / solution variants. Full week guides also exist as Mintlify MDX under <code>docs/weeks/</code>.</p>
  </div>
</div>
""",
    )

    write(
        "clients.html",
        "Clients",
        """
<div class="wrap">
  <div class="page-hero">
    <h1>Client tracks</h1>
    <p>Original training worlds — not franchise clones.</p>
  </div>
  <article id="colorado" class="card" style="margin-bottom:1rem">
    <div class="tag">colorado</div>
    <h3>Redrock Basin Authority</h3>
    <p>Colorado River–style multi-reservoir operations. ~48 nodes. Releases, allocations, hydropower contingency.</p>
    <p style="margin-top:.6rem"><code>uv run scripts/set_track.py colorado</code></p>
  </article>
  <article id="kerrville" class="card" style="margin-bottom:1rem">
    <div class="tag">kerrville</div>
    <h3>City of Kerrville — flood risk</h3>
    <p>Guadalupe / Hill Country corridor. ~80 facilities. Mitigation priority, access, buyout vs defend.</p>
    <p style="margin-top:.6rem"><code>uv run scripts/set_track.py kerrville</code></p>
  </article>
  <article id="datacenter" class="card" style="margin-bottom:2rem">
    <div class="tag">datacenter</div>
    <h3>Horizon Grid — Texas data center EIS</h3>
    <p>~55 EIS elements across alternatives. Water, power/grid, receptors, mitigation.</p>
    <p style="margin-top:.6rem"><code>uv run scripts/set_track.py datacenter</code></p>
  </article>
</div>
""",
    )

    write(
        "methodology.html",
        "Methodology",
        """
<div class="wrap">
  <div class="page-hero">
    <h1>Firm methodology</h1>
    <p>Decision-grade climate risk. Computed vs judged. Dual audiences.</p>
  </div>
  <div class="prose">
    <h2>Rules that don't bend</h2>
    <ol>
      <li><strong>Decisions, not scores.</strong></li>
      <li><strong>Computed</strong> from <code>uv run</code> scripts you can re-run. <strong>Judged</strong> labeled with mechanism + precedent.</li>
      <li><strong>Assurable trail</strong> — cold review without trusting the presenter's CV.</li>
      <li><strong>Gaps</strong> become watchlist items — never silent invention.</li>
      <li><strong>Do not sum scenario losses.</strong></li>
    </ol>
    <h2>Dual audiences</h2>
    <p><strong>Board / council / exec</strong> gets judgment. <strong>Regulator / grant / EIS record</strong> gets lineage.</p>
    <p>Full library: <code>firm/</code> in the repo · Mintlify pages in <code>docs/</code>.</p>
  </div>
</div>
""",
    )

    print(f"Built cool site → {OUT}")


if __name__ == "__main__":
    main()
