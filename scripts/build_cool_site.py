#!/usr/bin/env python3
"""Build Hallmark public site into site/ for GitHub Pages.

Hallmark · genre: editorial · macrostructure: Narrative Workflow
theme: custom field-report-after-dark · nav: N9 · footer: Ft5
enrichment: none
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "site"
TOKENS = (ROOT / "tokens.css").read_text(encoding="utf-8")

CSS = TOKENS + r"""
html, body { overflow-x: clip; }
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  font-family: var(--font-body);
  font-size: var(--text-base);
  font-weight: 400;
  line-height: 1.55;
  color: var(--color-ink);
  background: var(--color-paper);
  min-height: 100vh;
}
a {
  color: var(--color-accent);
  text-decoration-thickness: 1px;
  text-underline-offset: 0.18em;
}
a:hover { color: var(--color-ink); }
a:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 3px;
}
.skip {
  position: absolute; left: -999px; top: 0;
  background: var(--color-accent); color: var(--color-accent-ink);
  padding: var(--space-xs) var(--space-sm);
}
.skip:focus { left: var(--page-gutter); top: var(--space-sm); z-index: 100; }

/* N9 — edge-aligned minimal mast */
.nav {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: var(--space-md);
  padding: var(--space-lg) var(--page-gutter);
  border-bottom: var(--rule-hair) solid var(--color-rule);
  background: var(--color-paper);
}
.wordmark {
  font-family: var(--font-display);
  font-style: normal;
  font-weight: 600;
  font-size: var(--text-lg);
  letter-spacing: -0.02em;
  color: var(--color-ink);
  text-decoration: none;
}
.wordmark:hover { color: var(--color-ink); }
.nav-links {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-xs) var(--space-lg);
  justify-content: flex-end;
}
.nav-links a {
  color: var(--color-muted);
  text-decoration: none;
  font-size: var(--text-sm);
  font-weight: 500;
  white-space: nowrap;
}
.nav-links a:hover,
.nav-links a[aria-current="page"] {
  color: var(--color-ink);
}
.nav-links a[aria-current="page"] {
  box-shadow: inset 0 -2px 0 var(--color-accent);
}

.wrap {
  width: min(var(--max), 100%);
  margin-inline: auto;
  padding-inline: var(--page-gutter);
}

/* Narrative Workflow — stages */
.mast {
  padding: var(--space-3xl) var(--page-gutter) var(--space-2xl);
  border-bottom: var(--rule-thick) solid var(--color-rule);
}
.mast__meta {
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--color-muted);
  margin: 0 0 var(--space-md);
}
.mast h1 {
  font-family: var(--font-display);
  font-style: normal;
  font-weight: 500;
  font-size: var(--text-display);
  line-height: 1.05;
  letter-spacing: -0.025em;
  margin: 0 0 var(--space-md);
  max-width: 16ch;
  color: var(--color-ink);
}
.mast__lede {
  max-width: var(--measure);
  color: var(--color-ink-soft);
  font-size: var(--text-md);
  margin: 0 0 var(--space-xl);
}
.actions {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-sm);
}
.btn {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2xs);
  font-family: var(--font-body);
  font-size: var(--text-sm);
  font-weight: 600;
  padding: 0.7rem 1rem;
  border: var(--rule-hair) solid var(--color-rule);
  background: transparent;
  color: var(--color-ink);
  text-decoration: none;
  cursor: pointer;
  transition: background var(--dur) var(--ease-out), border-color var(--dur) var(--ease-out), color var(--dur) var(--ease-out);
}
.btn:hover { border-color: var(--color-muted); background: var(--color-paper-2); color: var(--color-ink); }
.btn:active { transform: translateY(1px); }
.btn:disabled { opacity: 0.45; cursor: not-allowed; }
.btn-primary {
  background: var(--color-accent);
  border-color: var(--color-accent);
  color: var(--color-accent-ink);
}
.btn-primary:hover {
  filter: brightness(1.05);
  background: var(--color-accent);
  color: var(--color-accent-ink);
  border-color: var(--color-accent);
}

.stage {
  padding: var(--space-3xl) var(--page-gutter);
  border-bottom: var(--rule-hair) solid var(--color-rule);
}
.stage__label {
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--color-accent);
  margin: 0 0 var(--space-sm);
  font-weight: 500;
}
.stage h2 {
  font-family: var(--font-display);
  font-style: normal;
  font-weight: 500;
  font-size: var(--text-display-s);
  line-height: 1.1;
  letter-spacing: -0.02em;
  margin: 0 0 var(--space-md);
  max-width: 22ch;
  overflow-wrap: anywhere;
  min-width: 0;
}
.stage p {
  max-width: var(--measure);
  color: var(--color-ink-soft);
  margin: 0 0 var(--space-md);
}
.stage h2 + p { margin-top: 0; }

.week-list {
  list-style: none;
  margin: var(--space-xl) 0 0;
  padding: 0;
  border-top: var(--rule-hair) solid var(--color-rule);
}
.week-list li {
  display: grid;
  grid-template-columns: 4.5rem 1fr;
  gap: var(--space-md);
  padding: var(--space-md) 0;
  border-bottom: var(--rule-hair) solid var(--color-rule);
  min-width: 0;
}
.week-list .n {
  font-family: var(--font-mono);
  font-size: var(--text-sm);
  color: var(--color-muted);
  font-variant-numeric: tabular-nums;
}
.week-list strong {
  display: block;
  font-family: var(--font-display);
  font-style: normal;
  font-weight: 600;
  font-size: var(--text-md);
  color: var(--color-ink);
  margin-bottom: var(--space-2xs);
}
.week-list span { color: var(--color-ink-soft); font-size: var(--text-sm); }

.track-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: var(--space-lg);
  font-size: var(--text-sm);
}
.track-table th,
.track-table td {
  text-align: left;
  vertical-align: top;
  padding: var(--space-sm) var(--space-sm) var(--space-sm) 0;
  border-bottom: var(--rule-hair) solid var(--color-rule);
}
.track-table th {
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--color-muted);
  font-weight: 500;
}
.track-table code {
  font-family: var(--font-mono);
  font-size: 0.9em;
  color: var(--color-accent);
}

pre, .cmd {
  font-family: var(--font-mono);
  font-size: var(--text-sm);
  line-height: 1.5;
  background: var(--color-paper-2);
  border: var(--rule-hair) solid var(--color-rule);
  padding: var(--space-md);
  overflow-x: auto;
  color: var(--color-ink-soft);
  margin: var(--space-md) 0;
}
code {
  font-family: var(--font-mono);
  font-size: 0.92em;
}
.prose p { max-width: var(--measure); color: var(--color-ink-soft); }
.prose h1, .prose h2, .prose h3 {
  font-family: var(--font-display);
  font-style: normal;
  font-weight: 500;
  letter-spacing: -0.02em;
  color: var(--color-ink);
}
.prose h1 { font-size: var(--text-display-s); margin: 0 0 var(--space-md); }
.prose h2 {
  font-size: var(--text-xl);
  margin: var(--space-2xl) 0 var(--space-sm);
  padding-top: var(--space-lg);
  border-top: var(--rule-hair) solid var(--color-rule);
}
.prose h2:first-of-type { margin-top: var(--space-xl); }
.prose ul, .prose ol { color: var(--color-ink-soft); max-width: var(--measure); }
.note {
  border-left: var(--rule-thick) solid var(--color-accent);
  padding: var(--space-sm) var(--space-md);
  margin: var(--space-lg) 0;
  color: var(--color-ink-soft);
  max-width: var(--measure);
  background: var(--color-paper-2);
}
.page {
  padding: var(--space-3xl) var(--page-gutter) var(--space-4xl);
}

/* Ft5 Statement */
.foot-stmt {
  padding: var(--space-3xl) var(--page-gutter) var(--space-2xl);
  border-top: var(--rule-thick) solid var(--color-rule);
  display: grid;
  gap: var(--space-xl);
}
.foot-stmt__line {
  font-family: var(--font-display);
  font-style: normal;
  font-weight: 500;
  font-size: clamp(1.5rem, 3.5vw, 2.5rem);
  line-height: 1.08;
  letter-spacing: -0.02em;
  max-width: 22ch;
  margin: 0;
  color: var(--color-ink);
}
.foot-stmt__meta {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: var(--space-sm);
  align-items: baseline;
  padding-block-start: var(--space-md);
  border-top: var(--rule-hair) solid var(--color-rule);
  font-size: var(--text-sm);
  color: var(--color-muted);
}
.foot-stmt__meta a { color: var(--color-muted); text-decoration: none; }
.foot-stmt__meta a:hover { color: var(--color-accent); }

@media (max-width: 640px) {
  .nav { flex-direction: column; align-items: flex-start; }
  .nav-links { justify-content: flex-start; }
  .week-list li { grid-template-columns: 1fr; gap: var(--space-2xs); }
  .actions { flex-direction: column; align-items: stretch; }
  .btn { justify-content: center; }
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
"""


def nav(active: str) -> str:
    items = [
        ("index.html", "Home"),
        ("quickstart.html", "Start"),
        ("curriculum.html", "Weeks"),
        ("clients.html", "Tracks"),
        ("methodology.html", "Method"),
    ]
    links = []
    for href, label in items:
        cur = ' aria-current="page"' if href == active else ""
        links.append(f'<a href="{href}"{cur}>{label}</a>')
    return f"""
<a class="skip" href="#main">Skip to content</a>
<header class="nav">
  <a class="wordmark" href="index.html">Climate Risk Course</a>
  <nav class="nav-links" aria-label="Primary">{"".join(links)}</nav>
</header>
"""


def footer() -> str:
    return """
<footer class="foot-stmt">
  <p class="foot-stmt__line">Ship the judgment. Keep the trail.</p>
  <div class="foot-stmt__meta">
    <span>Climate Risk Course · MIT</span>
    <span>
      <a href="https://github.com/rdsciv/ClimateRiskCourse">GitHub</a>
      · <a href="quickstart.html">Start</a>
    </span>
  </div>
</footer>
"""


def page(title: str, active: str, body: str, description: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>{title} · Climate Risk Course</title>
  <meta name="description" content="{description}"/>
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400&family=JetBrains+Mono:wght@400;500&family=Newsreader:opsz,wght@6..72,500;6..72,600&display=swap" rel="stylesheet"/>
  <link rel="stylesheet" href="assets/site.css"/>
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml"/>
</head>
<body>
{nav(active)}
<main id="main">
{body}
</main>
{footer()}
</body>
</html>
"""


def write(name: str, title: str, body: str, description: str) -> None:
    (OUT / name).write_text(page(title, name, body, description), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    assets = OUT / "assets"
    assets.mkdir(exist_ok=True)
    (assets / "site.css").write_text(CSS, encoding="utf-8")
    fav = ROOT / "docs" / "favicon.svg"
    if fav.is_file():
        (assets / "favicon.svg").write_text(fav.read_text(encoding="utf-8"), encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")

    write(
        "index.html",
        "Home",
        """
<section class="mast">
  <p class="mast__meta">Grok Build training · six weeks · three tracks</p>
  <h1>From client file to board pack.</h1>
  <p class="mast__lede">A climate-risk consulting engagement you run yourself — with Grok Build as the harness, uv for the environment, and a firm methodology that separates computed figures from judgment.</p>
  <div class="actions">
    <a class="btn btn-primary" href="quickstart.html">Start at stage 1</a>
    <a class="btn" href="https://github.com/rdsciv/ClimateRiskCourse">View on GitHub</a>
  </div>
</section>

<section class="stage" id="tracks">
  <p class="stage__label">1.0 · Choose the book</p>
  <h2>One track. Stay with it.</h2>
  <p>Same six-week method. Different decision language. All data is simulated training material.</p>
  <table class="track-table">
    <thead>
      <tr><th>Key</th><th>Client</th><th>You decide in terms of…</th></tr>
    </thead>
    <tbody>
      <tr>
        <td><code>colorado</code></td>
        <td>Redrock Basin Authority — Colorado River reservoirs</td>
        <td>Releases, allocations, hydropower contingency</td>
      </tr>
      <tr>
        <td><code>kerrville</code></td>
        <td>City of Kerrville — flood risk (TX)</td>
        <td>Mitigation priority, access, buyout vs defend</td>
      </tr>
      <tr>
        <td><code>datacenter</code></td>
        <td>Horizon Grid — Texas data center EIS</td>
        <td>Alternatives, water, grid, receptors</td>
      </tr>
    </tbody>
  </table>
</section>

<section class="stage" id="weeks">
  <p class="stage__label">2.0 · Run the engagement</p>
  <h2>Each week answers a paid question.</h2>
  <p>Deliverables chain. Week six produces judgment for the board and a record for reviewers.</p>
  <ol class="week-list">
    <li><span class="n">00</span><div><strong>Orientation</strong><span>Install, clone, pick a track.</span></div></li>
    <li><span class="n">01</span><div><strong>The client</strong><span>Framing and delivery plan.</span></div></li>
    <li><span class="n">02</span><div><strong>Portfolio mapping</strong><span>Geocode, classify, hypotheses.</span></div></li>
    <li><span class="n">03</span><div><strong>Hazard data</strong><span>Scores, joins, audit log.</span></div></li>
    <li><span class="n">04</span><div><strong>Scenarios</strong><span>Standard set + bespoke stresses.</span></div></li>
    <li><span class="n">05</span><div><strong>Synthesis</strong><span>Concentration and decisions.</span></div></li>
    <li><span class="n">06</span><div><strong>Delivery</strong><span>Board pack + record with lineage.</span></div></li>
  </ol>
  <p style="margin-top:var(--space-xl)"><a class="btn" href="curriculum.html">Full curriculum</a></p>
</section>

<section class="stage" id="rules">
  <p class="stage__label">3.0 · Hold the line</p>
  <h2>Epistemic rules travel with every deliverable.</h2>
  <p><strong style="color:var(--color-ink)">Computed</strong> figures come from scripts you re-run with <code>uv run</code>. <strong style="color:var(--color-ink)">Judged</strong> figures carry mechanism, precedent, and the word judgment. Gaps stay gaps. Scenario losses never sum.</p>
  <p><a class="btn" href="methodology.html">Read the method</a></p>
</section>
""",
        "Six-week climate risk assessment course for Grok Build.",
    )

    write(
        "quickstart.html",
        "Start",
        """
<div class="page prose">
  <p class="stage__label">Day one · about thirty minutes</p>
  <h1>Clone, sync, seed, open Grok.</h1>

  <h2>Requirements</h2>
  <ul>
    <li><a href="https://git-scm.com/">Git</a></li>
    <li><a href="https://docs.astral.sh/uv/">uv</a></li>
    <li><a href="https://x.ai">Grok Build</a> authenticated</li>
  </ul>

  <h2>Install uv once</h2>
<pre>curl -LsSf https://astral.sh/uv/install.sh | sh
uv --version</pre>

  <h2>1 · Clone the course</h2>
  <p>Two lines. First downloads the repo. Second enters it.</p>
<pre>git clone https://github.com/rdsciv/ClimateRiskCourse.git
cd ClimateRiskCourse</pre>

  <h2>2 · Install with uv</h2>
<pre>uv sync</pre>
  <div class="note">Use <strong>uv run</strong> for every script. Do not call system python3 or pip.</div>

  <h2>3 · Seed and pick a track</h2>
<pre>uv run scripts/seed_all_clients.py
uv run scripts/set_track.py colorado   # or kerrville | datacenter
uv run scripts/course_lint.py</pre>

  <h2>4 · Open Grok Build</h2>
  <p>In the <code>ClimateRiskCourse</code> folder:</p>
<pre>Summarize firm/methodology.md in five bullets.
Do not open any exercises/**/solution/ folders.</pre>

  <h2>5 · Orientation</h2>
  <p>Work through <code>exercises/00-orientation/</code>, then week 1. Explainers first, problems next, solutions only after an honest attempt. Outputs go to <code>clients/&lt;track&gt;/outputs/week-N/</code>.</p>
</div>
""",
        "Clone the Climate Risk Course and start Day 1 with uv.",
    )

    write(
        "curriculum.html",
        "Weeks",
        """
<div class="page prose">
  <p class="stage__label">Curriculum</p>
  <h1>Six stages. One chain.</h1>
  <p>Hands-on work lives under <code>exercises/</code> as explainer, problem, and solution variants.</p>

  <ol class="week-list" style="margin-top:var(--space-2xl)">
    <li><span class="n">00</span><div><strong>Orientation</strong><span>Environment ready; track chosen.</span></div></li>
    <li><span class="n">01</span><div><strong>The Client</strong><span>What does this client need? Framing &amp; delivery plan.</span></div></li>
    <li><span class="n">02</span><div><strong>Mapping</strong><span>Where does risk concentrate? Mapped book + hypotheses.</span></div></li>
    <li><span class="n">03</span><div><strong>Hazard</strong><span>Which data matters? Organized hazard dataset + audit log.</span></div></li>
    <li><span class="n">04</span><div><strong>Scenarios</strong><span>Standard for the record; bespoke for this book.</span></div></li>
    <li><span class="n">05</span><div><strong>Synthesis</strong><span>What should change? Concentration and decisions.</span></div></li>
    <li><span class="n">06</span><div><strong>Delivery</strong><span>Board judgment + regulatory-style record.</span></div></li>
  </ol>

  <h2>Mintlify source</h2>
  <p>Structured week and track pages also live in <code>docs/</code> for local Mintlify preview:</p>
<pre>cd docs && npx mintlify dev</pre>
</div>
""",
        "Six-week curriculum for the climate risk course.",
    )

    write(
        "clients.html",
        "Tracks",
        """
<div class="page prose">
  <p class="stage__label">Client tracks</p>
  <h1>Three books. One method.</h1>

  <h2>Colorado River reservoirs</h2>
  <p><code>colorado</code> · <code>clients/colorado-river-reservoirs/</code></p>
  <p>Redrock Basin Authority (simulated). Multi-reservoir operations under drought and heat. Releases, allocations, compact-sensitive deliveries, hydropower contingency.</p>
<pre>uv run scripts/set_track.py colorado</pre>

  <h2>Kerrville flood risk</h2>
  <p><code>kerrville</code> · <code>clients/kerrville-flood/</code></p>
  <p>City of Kerrville (simulated asset book; real geography). Critical facilities, access, mitigation priority, buyout vs defend.</p>
<pre>uv run scripts/set_track.py kerrville</pre>

  <h2>Texas data center EIS</h2>
  <p><code>datacenter</code> · <code>clients/texas-datacenter-eis/</code></p>
  <p>Horizon Grid LLC (simulated). Alternatives analysis, water supply, grid interconnect, receptors, mitigation commitments.</p>
<pre>uv run scripts/set_track.py datacenter</pre>

  <div class="note">Stay with one track through week six. Mixing books mid-engagement breaks the chain.</div>
</div>
""",
        "Colorado River, Kerrville flood, and Texas data center EIS tracks.",
    )

    write(
        "methodology.html",
        "Method",
        """
<div class="page prose">
  <p class="stage__label">Firm methodology</p>
  <h1>Decision-grade, not score-led.</h1>
  <p>Hazard signal joins to operations or capital questions. Disclosure falls out of the work; it is not the product.</p>

  <h2>What we optimize for</h2>
  <ol>
    <li><strong>Decisions, not scores.</strong></li>
    <li><strong>Legible epistemology</strong> — computed from scripts; judged with mechanism and precedent.</li>
    <li><strong>Assurability</strong> — a cold reviewer can re-run numbers without trusting the presenter.</li>
    <li><strong>Graceful degradation</strong> — thin data widens ranges and grows the watchlist.</li>
  </ol>

  <h2>Dual audiences</h2>
  <p>Board, council, or project exec get the judgment. Regulator, grant, or EIS administrative record get the lineage.</p>

  <h2>In the repo</h2>
  <p>Full library under <code>firm/</code> — methodology, scenario cards, anchors, QA protocols, sample hazard grids.</p>
</div>
""",
        "Firm methodology for climate risk assessments.",
    )

    # Project memory for Hallmark diversification
    hallmark = ROOT / ".hallmark"
    hallmark.mkdir(exist_ok=True)
    (hallmark / "log.json").write_text(
        """[
  {
    "date": "2026-07-27",
    "macrostructure": "Narrative Workflow",
    "theme": "custom",
    "theme_axes": "dark / roman-serif / warm",
    "vibe": "field report after dark",
    "enrichment": "none",
    "nav": "N9",
    "footer": "Ft5",
    "brief": "Climate Risk Course public site redesign"
  }
]
""",
        encoding="utf-8",
    )
    (hallmark / "preflight.json").write_text(
        """{
  "scanned": "2026-07-27",
  "framework": "vanilla HTML static site via scripts/build_cool_site.py",
  "fonts": "Newsreader + IBM Plex Sans + JetBrains Mono (Google Fonts)",
  "motion": "none (motion-cut)",
  "package_managers": ["uv", "npm scripts for mintlify"]
}
""",
        encoding="utf-8",
    )

    print(f"Built Hallmark site → {OUT}")


if __name__ == "__main__":
    main()
