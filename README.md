# Climate Risk Course (Grok Build)

**Six weeks to a climate risk assessment** — a hands-on Grok Build course. You operate as a consultant for one of three simulated clients, shipping a weekly deliverable that becomes the input to the next, through a board/IC presentation and a regulatory-style record in week six.

**All clients and portfolio data are simulated.** Built as a hands-on Grok Build training course for climate risk assessment work.

## What you will build

| Week | Question | Deliverable |
|------|----------|-------------|
| 0 | How do I take this course? | Environment + track choice |
| 1 | What does the client need? | Framing & delivery plan |
| 2 | Where does risk concentrate? | Mapped portfolio + hypothesis register |
| 3 | Which hazard data matters? | Organized hazard dataset + audit log |
| 4 | Which scenarios bite? | Standard + bespoke scenario results |
| 5 | What should change? | Portfolio synthesis + decision implications |
| 6 | Will it stand up? | Board judgment + record pack |

## Three client tracks

| Key | Client | Best if you work in… |
|-----|--------|----------------------|
| `colorado` | Redrock Basin Authority — Colorado River reservoirs | Water resources, utilities, basin ops |
| `kerrville` | City of Kerrville — flood risk (TX) | Local government, emergency mgmt, floodplain |
| `datacenter` | Horizon Grid — Texas data center EIS | EIS/NEPA, energy, data-center siting |

Same method. Different data and decision language.

## Day-1 setup (30 minutes)

### Requirements

- [Git](https://git-scm.com/)
- [uv](https://docs.astral.sh/uv/) — install once if you do not have it:
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

# 7. Open Grok Build in this repo and start exercises/00-orientation
```

Copy `.env.example` to `.env` if you want to pin `CLIENT_TRACK` by hand.

Run every course script with **`uv run`** (not bare system Python).

## How to take the course

1. Work **one track** through week 6.
2. For each exercise, read **explainer** (if any), then do **problem** with Grok Build.
3. Compare **solution** only after an honest attempt.
4. Write artifacts under `clients/<track>/outputs/week-N/`.
5. Keep the audit log honest (`outputs/audit_log.jsonl`).

### Epistemic rules (memorize)

1. **Computed** figures come from saved Python scripts.
2. **Judged** figures carry mechanism + precedent + the word **judgment**.
3. Never invent government/vendor data pulls.
4. Document gaps; do not fill them silently.
5. **Do not sum** losses across scenarios.

## Repo map

```text
firm/              methodology, scenario cards, anchors, sample hazard, QA
clients/           colorado-river-reservoirs | kerrville-flood | texas-datacenter-eis
exercises/         00 orientation → 06 delivery
.grok/skills/      framing, geocode, hazard, scenarios, synthesis, disclosure
scripts/           seed, lint, track, export
templates/         board + regulatory shells
AGENTS.md          firm-level Grok brief
```

## Scripts

| Command | Purpose |
|---------|---------|
| `uv run scripts/seed_all_clients.py` | Build all SQLite books + docs |
| `uv run scripts/set_track.py <track>` | Activate colorado \| kerrville \| datacenter |
| `uv run scripts/course_lint.py` | Structure checks |
| `uv run scripts/list_exercises.py` | Print syllabus |
| `uv run scripts/export_deliverable.py FILE.md` | Markdown → HTML |
| `uv run scripts/generate_exercises.py` | Regenerate exercise readmes from generator |
| `uv run scripts/build_docs_site.py` | Rebuild GitHub Pages reading room |

## Grok skills

Project skills under `.grok/skills/` activate when relevant:

- `climate-engagement-framing`
- `portfolio-geocode-classify`
- `hazard-data-pull`
- `scenario-runner`
- `portfolio-synthesis`
- `disclosure-pack`

## Requirements

- [Grok Build](https://x.ai) CLI
- [uv](https://docs.astral.sh/uv/) (manages Python + dependencies)
- Git

No paid climate-data subscription required. Offline sample hazard grids ship in `firm/sample-hazard/`.

## Docs site (GitHub Pages)

Branded course docs live in `docs/` and deploy automatically on push to `main`:

- Home, curriculum, clients, methodology
- Reading room (firm files + exercise explainers)
- Getting started

```bash
uv run scripts/build_docs_site.py   # regenerate reading pages locally
# open docs/index.html
```

**Site URL (after Pages is enabled):** https://rdsciv.github.io/ClimateRiskCourse/

## License / attribution

Training materials and simulated data are provided for education. Client names, portfolios, and documents are fictional.
