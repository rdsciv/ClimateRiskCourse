# Climate Risk Course

**Six weeks to a climate risk assessment** — a Grok Build course that treats climate risk like a real consulting engagement, not a chatbot demo.

[![Docs](https://img.shields.io/badge/docs-mintlify-2EE6A6?style=for-the-badge)](https://rdsciv.github.io/ClimateRiskCourse/)
[![uv](https://img.shields.io/badge/python-uv-DE5FE9?style=for-the-badge&logo=python&logoColor=white)](https://docs.astral.sh/uv/)
[![Grok Build](https://img.shields.io/badge/agent-Grok%20Build-000000?style=for-the-badge)](https://x.ai)

> **All clients and data are simulated.** Built for training. Geography can be real; filings are not.

## Docs site

**Live site:** [rdsciv.github.io/ClimateRiskCourse](https://rdsciv.github.io/ClimateRiskCourse/)

Two layers:

| Layer | Path | Purpose |
|-------|------|---------|
| **Live site** | `site/` (GitHub Pages) | High-energy public UI |
| **Mintlify source** | `docs/` (`docs.json` + MDX) | Structured docs you can `mintlify dev` |

```bash
# Public site (what Pages deploys)
uv run scripts/build_cool_site.py
open site/index.html

# Mintlify authoring preview
cd docs && npx mintlify dev
```

## Day-1 setup (30 minutes)

### Requirements

- [Git](https://git-scm.com/)
- [uv](https://docs.astral.sh/uv/) — install once if needed:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- [Grok Build](https://x.ai) CLI authenticated

### Steps

```bash
# 1. Clone the course, then enter the folder
git clone https://github.com/rdsciv/ClimateRiskCourse.git
cd ClimateRiskCourse

# 2. Install dependencies with uv
uv sync

# 3. Seed all simulated clients
uv run scripts/seed_all_clients.py

# 4. Choose your track
uv run scripts/set_track.py colorado   # or kerrville | datacenter

# 5. Validate structure
uv run scripts/course_lint.py

# 6. List the syllabus
uv run scripts/list_exercises.py

# 7. Open Grok Build in this repo → exercises/00-orientation
```

Run every course script with **`uv run`**. No system `python3` / `pip`.

## Three client tracks

| Key | Client | Decision language |
|-----|--------|-------------------|
| `colorado` | Redrock Basin Authority — Colorado River reservoirs | Releases, allocations, hydropower |
| `kerrville` | City of Kerrville — flood risk (TX) | Mitigation, access, buyout vs defend |
| `datacenter` | Horizon Grid — Texas data center EIS | Alternatives, water, grid, receptors |

Same method. Different book.

## Curriculum

| Week | Question | Deliverable |
|------|----------|-------------|
| 0 | How do I take this? | Environment + track |
| 1 | What does the client need? | Framing & delivery plan |
| 2 | Where does risk concentrate? | Mapped book + hypotheses |
| 3 | Which hazard data matters? | Hazard dataset + audit log |
| 4 | Which scenarios bite? | Standard + bespoke results |
| 5 | What should change? | Synthesis + decisions |
| 6 | Will it stand up? | Board judgment + record |

## Epistemic rules

1. **Computed** figures come from saved scripts (`uv run`).
2. **Judged** figures carry mechanism + precedent + the word **judgment**.
3. Never invent government/vendor data pulls.
4. Document gaps; do not fill them silently.
5. **Do not sum** losses across scenarios.

## Repo map

```text
docs/              Mintlify documentation site
firm/              methodology, scenario cards, anchors, sample hazard
clients/           colorado-river-reservoirs | kerrville-flood | texas-datacenter-eis
exercises/         weeks 0–6 (explainer / problem / solution)
.grok/skills/      framing, geocode, hazard, scenarios, synthesis, disclosure
scripts/           seed, lint, track, export (always: uv run scripts/…)
templates/         board + regulatory shells
AGENTS.md          firm-level Grok brief
```

## Scripts

| Command | Purpose |
|---------|---------|
| `uv run scripts/seed_all_clients.py` | Build all SQLite books |
| `uv run scripts/set_track.py <track>` | `colorado` \| `kerrville` \| `datacenter` |
| `uv run scripts/course_lint.py` | Structure checks |
| `uv run scripts/list_exercises.py` | Print syllabus |
| `uv run scripts/export_deliverable.py FILE.md` | Markdown → HTML |
| `uv run scripts/build_docs_site.py` | Legacy MD→HTML helper (optional) |

## License

MIT — simulated training data; educational use.
