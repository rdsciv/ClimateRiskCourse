# Climate Risk Course (Grok Build)

**Six weeks to a climate risk assessment** — a hands-on Grok Build course. You operate as a consultant for one of three simulated clients, shipping a weekly deliverable that becomes the input to the next, through a board/IC presentation and a regulatory-style record in week six.

Inspired by the Kith Climate risk curriculum structure. **All clients and portfolio data are simulated.** This is an educational fork for Grok Build, not an official Kith product.

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
| `ironwood` | Commercial bank credit book | Banking, credit, financial risk |
| `strata` | RE + infrastructure fund | Funds, property, insurance |
| `northwood` | Industrial + supply chain | Corporate climate, ops, procurement |

Same method. Different data and decision language.

## Day-1 setup (30 minutes)

```bash
# 1. Clone and enter
cd ClimateRiskCourse

# 2. Python deps (optional; stdlib is enough for seed + lint)
python3 -m venv .venv && source .venv/bin/activate   # optional
pip install pandas httpx pydantic python-dotenv         # optional extras

# 3. Seed all simulated clients
python3 scripts/seed_all_clients.py

# 4. Choose your track
python3 scripts/set_track.py ironwood   # or strata | northwood

# 5. Validate structure
python3 scripts/course_lint.py

# 6. List the syllabus
python3 scripts/list_exercises.py

# 7. Open Grok Build in this repo and start exercises/00-orientation
```

Copy `.env.example` to `.env` if you want to pin `CLIENT_TRACK` by hand.

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
clients/           ironwood-bank | strata-holdings | northwood-capital
exercises/         00 orientation → 06 delivery
.grok/skills/      framing, geocode, hazard, scenarios, synthesis, disclosure
scripts/           seed, lint, track, export
templates/         board + regulatory shells
AGENTS.md          firm-level Grok brief
```

## Scripts

| Command | Purpose |
|---------|---------|
| `python3 scripts/seed_all_clients.py` | Build all SQLite books + docs |
| `python3 scripts/set_track.py <track>` | Activate ironwood \| strata \| northwood |
| `python3 scripts/course_lint.py` | Structure checks |
| `python3 scripts/list_exercises.py` | Print syllabus |
| `python3 scripts/export_deliverable.py FILE.md` | Markdown → HTML |
| `python3 scripts/generate_exercises.py` | Regenerate exercise readmes from generator |

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
- Python 3.11+
- Git

No paid climate-data subscription required. Offline sample hazard grids ship in `firm/sample-hazard/`.

## Docs site (GitHub Pages)

Branded course docs live in `docs/` and deploy automatically on push to `main`:

- Home, curriculum, clients, methodology
- Reading room (firm files + exercise explainers)
- Getting started

```bash
python3 scripts/build_docs_site.py   # regenerate reading pages locally
# open docs/index.html
```

**Site URL (after Pages is enabled):** https://rdsciv.github.io/ClimateRiskCourse/

## License / attribution

Training materials and simulated data are provided for education. Curriculum structure inspired by publicly described Kith Climate risk programming. Not affiliated with or endorsed by Kith Climate unless separately stated.
