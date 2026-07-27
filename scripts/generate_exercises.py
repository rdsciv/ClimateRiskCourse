#!/usr/bin/env python3
"""Generate exercise directories and full pedagogical readmes."""

from __future__ import annotations

import sys
from pathlib import Path
from textwrap import dedent

sys.path.insert(0, str(Path(__file__).resolve().parent))
from course_manifest import SECTIONS

ROOT = Path(__file__).resolve().parents[1]
EX = ROOT / "exercises"

# ---------------------------------------------------------------------------
# Content library: key = "exercise-id/variant"
# ---------------------------------------------------------------------------

CONTENT: dict[str, str] = {}


def c(key: str, body: str) -> None:
    CONTENT[key] = dedent(body).strip() + "\n"


# ===== 00 Orientation ======================================================

c(
    "00.01-how-this-course-works/explainer",
    """
    # How this course works

    ## The engagement

    You are a consultant inside a simulated climate-risk firm. Over six weeks you answer the questions a real client would pay for. **Each week's deliverable is the input to the next**, ending in a board/IC presentation (judgment) and a regulatory or stakeholder submission (record).

    ## Three tracks, one method

    | Track | Folder | Decision language |
    |-------|--------|-------------------|
    | Redrock Basin Authority | `clients/colorado-river-reservoirs` | Reservoir releases & allocations |
    | City of Kerrville | `clients/kerrville-flood` | Flood mitigation priority |
    | Horizon Grid LLC | `clients/texas-datacenter-eis` | Data center EIS alternatives |

    Pick one track and stay with it. Plenary exercises are shared; data and financial questions differ.

    ## Weekly rhythm (as designed)

    - **Monday pattern:** methodology taught against the live environment
    - **Mid-week:** build time + optional check-in
    - **Friday:** demo the deliverable
    - **Between sessions:** 3–4 hours applying the pattern to your client

    Self-paced students: treat each section as a week. Do not skip the audit trail.

    ## How learning is structured

    Exercises live under `exercises/` with variants:

    - **explainer** — concepts and patterns
    - **problem** — you build with Grok Build
    - **solution** — reference approach (use after honest attempt)

    ## Tooling

    - **Grok Build** orchestrates the engagement
    - **Python** computes figures you can re-run
    - **`firm/`** encodes methodology, scenarios, anchors
    - **`clients/<track>/`** holds the book and your outputs

    ## Non-negotiables

    1. Computed vs judged — always labeled
    2. No silent invention of data
    3. Gaps become watchlist items
    4. Do not sum scenario losses
    """,
)

c(
    "00.02-install-grok-build/explainer",
    """
    # Install Grok Build

    ## What you need

    - Grok Build CLI authenticated and working in a terminal
    - [uv](https://docs.astral.sh/uv/) on your PATH
    - Git
    - This repository cloned (`git clone https://github.com/rdsciv/ClimateRiskCourse.git` then `cd ClimateRiskCourse`)

    ## Project rules

    This repo’s root `AGENTS.md` is loaded by Grok automatically. It tells the agent you are in a **training firm** with epistemic rules. Do not delete it.

    ## Verify

    From the repo root (after clone + `cd ClimateRiskCourse`):

    ```bash
    uv --version
    uv sync
    uv run scripts/seed_all_clients.py
    uv run scripts/set_track.py colorado
    uv run scripts/course_lint.py
    ```

    Then start Grok in this directory and ask:

    > Summarize firm/methodology.md in five bullets. Do not open any solution folders.
    """,
)

c(
    "00.02-install-grok-build/problem",
    """
    # Problem — Install Grok Build

    ## Goal

    Prove your environment can run the course offline.

    ## TODO

    1. Authenticate Grok Build and open a session in this repo.
    2. Run `uv sync` (if you have not already).
    3. Run `uv run scripts/seed_all_clients.py`.
    4. Run `uv run scripts/set_track.py <your-track>`.
    5. Confirm `clients/active` points at your folder and `.env` has `CLIENT_TRACK`.
    6. Ask Grok to read `AGENTS.md` and restate the five epistemic rules.

    ## Acceptance criteria

    - [ ] All three client DBs exist under `clients/*/db/portfolio.sqlite`
    - [ ] Active track set
    - [ ] You can explain computed vs judged without looking it up
    """,
)

c(
    "00.03-choose-your-client-track/explainer",
    """
    # Choose your client track

    ## Redrock Basin Authority (Colorado River reservoirs)

    Multi-reservoir operations under drought and heat. Best if you work in **water resources, utilities, or river-basin management**.

    ## City of Kerrville (flood risk)

    Municipal flood corridor and critical facilities. Best if you work in **local government, emergency management, or floodplain planning**.

    ## Horizon Grid LLC (Texas data center EIS)

    Hyperscale campus environmental impact statement. Best if you work in **EIS/NEPA, energy, or data-center siting**.

    ## Switching later

    Allowed, but you will redo weeks 1–2. Prefer one track through the capstone.
    """,
)

c(
    "00.03-choose-your-client-track/problem",
    """
    # Problem — Choose your client track

    ## TODO

    1. Read `clients/README.md` and each track’s `briefing/engagement.md`.
    2. Pick one track.
    3. Run `uv run scripts/set_track.py <colorado|kerrville|datacenter>`.
    4. Write three sentences in `clients/<track>/outputs/week-0/track_choice.md`:
       - Why this track
       - The decision language you will use
       - The primary audience for week 6 (board vs IC vs exec ops)

    ## Acceptance criteria

    - [ ] `track_choice.md` exists
    - [ ] Active track matches your choice
    """,
)

c(
    "00.04-course-repo-tour/explainer",
    """
    # Course repo tour

    ```text
    firm/           methodology, scenario cards, anchors, sample hazard, QA
    clients/        three simulated engagements
    exercises/      weeks 0–6 curriculum
    .grok/skills/   repeatable Grok procedures
    scripts/        seed, lint, track, export
    templates/      board + regulatory shells
    ```

    ## Mental model

    - **firm/** = the house brain (durable)
    - **clients/** = the engagement file (per student track)
    - **exercises/** = the syllabus
    - **Grok** = the analyst harness you direct

    Open `firm/methodology.md` next, then your track briefing.
    """,
)

# ===== 01 The Client =======================================================

c(
    "01.01-grok-build-in-a-client-workspace/explainer",
    """
    # Grok Build in a client workspace

    ## Compartments

    Treat `clients/<track>/` as the engagement room. Do not mix Colorado River node numbers into a Kerrville flood memo.

    ## Plan mode

    For multi-file analysis (read briefing + sample documents + DB), start in **plan mode**. Approve the plan, then execute. Climate work goes wrong when the agent improvises scope.

    ## Sessions

    Prefer one engagement thread per week deliverable. Paste or point at last week’s output path at the start of a new week.

    ## Safety

    - No production secrets in this training repo
    - Still practice: never paste real client PII into unapproved tools outside your org policy
    """,
)

c(
    "01.02-write-the-engagement-agents-md/problem",
    """
    # Problem — Write the engagement AGENTS.md

    ## Context

    Root `AGENTS.md` is firm-wide. Your track folder needs a sharper brief so Grok does not re-derive the client every session.

    ## TODO

    1. Read `clients/<track>/briefing/engagement.md` and `documents/stakeholder_messages.md`.
    2. Rewrite `clients/<track>/AGENTS.md` (replace the stub) with:
       - Client one-liner
       - Decision language
       - Deadlines / audiences
       - Data paths (DB, CSV, docs, outputs)
       - Guardrails (simulated data, computed vs judged)
       - Out-of-scope list (at least three items)
    3. Start a **new** Grok session and ask only: “What is in scope this engagement?”
       Confirm the answer matches your file.

    ## Acceptance criteria

    - [ ] Track `AGENTS.md` is specific (not a copy of root only)
    - [ ] Out-of-scope has ≥3 items
    - [ ] Cold session restates scope correctly
    """,
)

c(
    "01.02-write-the-engagement-agents-md/solution",
    """
    # Solution — Engagement AGENTS.md

    ## Approach

    Encode **audience + decision language + paths + guardrails**. Keep it short enough that it always loads.

    ## Colorado sketch

    ```markdown
    # Redrock Basin Authority (SIMULATED)

    Colorado River–style reservoir operations climate risk engagement.
    Decision language: releases, allocations, compact-sensitive deliveries.
    Audiences: GM, boards, compact counsel, hydropower desk.

    Data: db/portfolio.sqlite, portfolio/reservoir_nodes.csv, documents/
    Outputs: outputs/week-N/
    All data simulated. Computed figures from Python; judgments labeled.
    Out of scope: rewriting interstate compact law; real Reclamation account reconciliation.
    ```

    ## Kerrville / Datacenter

    Swap decision language to flood mitigation or EIS alternatives; keep the same structure.

    ## Check

    Cold session should refuse out-of-scope work and know the DB path without hunting.
    """,
)

c(
    "01.03-connect-and-query-the-book/problem",
    """
    # Problem — Connect and query the book

    ## TODO

    1. Open `clients/<track>/db/portfolio.sqlite` (CLI, Python, or Grok-written script).
    2. Produce `outputs/week-1/scripts/book_overview.py` that prints:
       - row counts for main tables
       - top sectors / asset types / countries by exposure or NAV or revenue-at-risk
       - data_quality breakdown
    3. Save stdout to `outputs/week-1/book_overview.txt`.

    ## Acceptance criteria

    - [ ] Script re-runs cleanly
    - [ ] Overview file committed to your outputs (local is fine)
    - [ ] Numbers match a manual spot-check of the CSV
    """,
)

c(
    "01.03-connect-and-query-the-book/solution",
    """
    # Solution — Connect and query the book

    ## Pattern

    ```python
    import sqlite3
    from pathlib import Path

    db = Path("clients/colorado-river-reservoirs/db/portfolio.sqlite")  # or active track
    conn = sqlite3.connect(db)
    print(conn.execute("SELECT COUNT(*) FROM counterparties").fetchone())
    # GROUP BY sector / data_quality; SUM(outstanding_usd)
    ```

    Adapt table names: Colorado `facilities`/`allocations`, Kerrville `facilities`/`exposures`, Datacenter `facilities`/`impact_topics`.

    ## Tip

    Have Grok write the script, then **you** run it. The point is a reproducible artifact, not a chat transcript.
    """,
)

c(
    "01.04-read-the-file-at-machine-speed/problem",
    """
    # Problem — Read the file at machine speed

    ## TODO

    1. With Grok, read all files under `clients/<track>/documents/` and the briefing.
    2. Produce `outputs/week-1/file_read_memo.md` with:
       - Stakeholder map (who wants what)
       - Deadlines
       - Known data quality issues (name IDs if present)
       - Open questions for the client
    3. Flag at least one **contradiction** or gap called out in the docs.

    ## Acceptance criteria

    - [ ] Memo ≤ 1 page equivalent
    - [ ] Every claim cites a source filename
    - [ ] At least one explicit gap/contradiction
    """,
)

c(
    "01.04-read-the-file-at-machine-speed/solution",
    """
    # Solution — File read memo

    ## Approach

    Prompt Grok: “Extract only facts present in these files. Cite paths. Separate facts from inferences.”

    ## Example findings (Colorado)

    - GM wants dry-year break points before spring ops call (`stakeholder_messages.md`)
    - Compact counsel: no invented agency figures
    - Hydropower desk: couple storage to generation shortfall

    Kerrville: critical facilities + budget-cycle mitigation list.  
    Datacenter: alternatives matrix + water/power for EIS counsel.
    """,
)

c(
    "01.05-scope-materiality-and-guardrails/explainer",
    """
    # Scope: materiality and guardrails

    ## Materiality in this program

    Something is material if it could change **a decision** the client is already trying to make (price, capital, buy/hold/exit, contingency spend).

    ## Guardrails to write down

    - Geographies or books excluded
    - Transition-only policy analysis in/out
    - Vendor cat-model purchase in/out
    - Assurance-ready vs draft internal

    ## Common failure

    Expanding scope when the agent finds something interesting. Park curiosities on a backlog; do not let them rewrite week 6.
    """,
)

c(
    "01.05-scope-materiality-and-guardrails/problem",
    """
    # Problem — Scope materiality and guardrails

    ## TODO

    Write `outputs/week-1/scope_guardrails.md` with:

    1. In-scope decisions (3–5)
    2. Out-of-scope (3–5)
    3. Materiality rule in one sentence
    4. Data you will **not** invent if missing

    ## Acceptance criteria

    - [ ] File exists and is specific to your track
    - [ ] Materiality rule mentions decisions, not “interesting science”
    """,
)

c(
    "01.06-delivery-plan-the-client-would-sign/problem",
    """
    # Problem — Delivery plan the client would sign

    ## Capstone week deliverable

    Produce `outputs/week-1/framing_and_delivery_plan.md` that a nervous engagement lead would accept.

    ## Required sections

    1. Client situation (5–8 sentences)
    2. Decision questions
    3. Workplan weeks 2–6 (inputs → outputs)
    4. Risks to delivery (data, time, model)
    5. Assumptions register (initial)
    6. Simulated-data banner

    ## Acceptance criteria

    - [ ] Week 6 dual deliverables named
    - [ ] Each week has a named artifact
    - [ ] Aligns with `firm/deliverable-standards/`
    """,
)

c(
    "01.06-delivery-plan-the-client-would-sign/solution",
    """
    # Solution — Delivery plan

    ## Structure that works

    - Open with the decision question in the client’s language
    - Table for weeks 2–6: activity | output path | dependency
    - Risks: incomplete questionnaires, offline hazard only, judgment-heavy transmission
    - Assumptions: training anchors from `firm/anchors/`; sample hazard grid unless live API enabled

    ## Quality bar

    If you removed all AI mentions and sent this to a human partner, would they still understand the job? If not, rewrite.
    """,
)

# ===== 02 Portfolio mapping ================================================

c(
    "02.01-whole-book-screen/explainer",
    """
    # Whole-book screen

    Before asset-level heroics, see the book in one view:

    - Concentration by sector / asset type / role
    - Concentration by geography (state, country, metro)
    - Data quality distribution
    - Exposure, NAV, or revenue-at-risk totals

    Hypotheses born here are cheaper to test than hypotheses born from a single credit file.
    """,
)

c(
    "02.02-batch-geocode-the-portfolio/problem",
    """
    # Problem — Batch geocode the portfolio

    ## TODO

    1. Read facilities/assets addresses from the DB or CSV.
    2. Prefer `geocode_cache` (already seeded offline). Write a script that:
       - Joins cache to entities
       - Writes `outputs/week-2/geocoded_portfolio.csv`
       - Logs the operation to `outputs/audit_log.jsonl` with `source: simulated_offline` or `geocode_cache`
    3. Optional stretch: if cache miss, use a public geocoder **and** log it; do not require this for pass.

    ## Acceptance criteria

    - [ ] CSV has lat/lon for ≥95% of rows
    - [ ] Script saved under `outputs/week-2/scripts/`
    - [ ] Audit log entry present
    """,
)

c(
    "02.02-batch-geocode-the-portfolio/solution",
    """
    # Solution — Batch geocode

    Training DBs already contain lat/lon and `geocode_cache`. The learning goal is the **pipeline + audit log**, not fighting Nominatim.

    ```python
    # SELECT id, address, city, lat, lon FROM facilities/assets
    # write CSV; append_audit(...)
    ```

    If you clear lat/lon to practice, rebuild from cache by address key.
    """,
)

c(
    "02.03-classify-by-activity/problem",
    """
    # Problem — Classify by activity

    ## TODO

    1. Build an activity classification table: entity id → activity class → rationale.
    2. Use existing sector/type/role fields; refine where names imply more specific activity (e.g., datacenter vs generic CRE).
    3. Save `outputs/week-2/activity_classification.csv` and a short `classification_notes.md`.

    ## Acceptance criteria

    - [ ] Every entity has a class
    - [ ] Notes explain rules, not each row
    """,
)

c(
    "02.03-classify-by-activity/solution",
    """
    # Solution — Activity classification

    Start from seeded fields (`sector`, `asset_type`, `role`). Add a normalized `activity_class` for hazard relevance:

    - `coastal_cre`, `inland_industrial`, `datacenter`, `ag_processing`, `tier1_supplier`, `owned_assembly`, …

    Keep a rule table in notes so week 4 scenarios can filter classes.
    """,
)

c(
    "02.04-choose-resolution/explainer",
    """
    # Choose resolution

    Not every name earns site-level narrative.

    **Escalate** when: high exposure/NAV/RAR, bad data quality on a large name, hazard bucket extreme, single-source critical, insurance red flag.

    **Stay at screen** when: small exposure, clean data, low hazard, diversified.

    Document the cut so week 6 can defend sampling.
    """,
)

c(
    "02.04-choose-resolution/problem",
    """
    # Problem — Choose resolution

    ## TODO

    Produce `outputs/week-2/resolution_plan.md` listing:

    - Screen-only population (counts + % of book)
    - Deep-dive list (IDs) with one-line why each
    - Explicit sampling rule

    ## Acceptance criteria

    - [ ] Deep-dive list is finite (not “all coastal”)
    - [ ] Rule is reusable by Grok without you re-explaining
    """,
)

c(
    "02.05-risk-hypothesis-register/problem",
    """
    # Problem — Risk hypothesis register

    ## TODO

    Create `outputs/week-2/hypothesis_register.md` with 5–8 hypotheses.

    Each row/section:

    | Field | Content |
    |-------|---------|
    | ID | H1… |
    | Statement | Falsifiable claim |
    | Why we think so | Screen evidence |
    | How week 3–4 tests it | Data + scenario |
    | Decision if true | Pricing/exit/contingency implication |

    ## Acceptance criteria

    - [ ] ≥5 hypotheses
    - [ ] Each links to a possible week-4 scenario test
    - [ ] Register path referenced in a one-page `mapped_portfolio.md` summary
    """,
)

c(
    "02.05-risk-hypothesis-register/solution",
    """
    # Solution — Hypothesis register

    ## Good hypothesis

    “≥30% of drawn in flood-tagged Texas CRE will exceed S2 under STD-01+TR-01, forcing a pricing conversation on maturities ≤2029.”

    ## Bad hypothesis

    “Climate is risky for the bank.” (Not testable, not decision-linked.)

    Feed H-IDs into week 4 bespoke scenarios by name.
    """,
)

# ===== 03 Hazard data ======================================================

c(
    "03.01-climate-data-strategy/explainer",
    """
    # Climate data strategy

    ## Slot architecture

    Hazard data sits in a **swappable slot**. Training uses `firm/sample-hazard/county_hazard_scores.csv`. Live APIs or vendor files can replace the slot if provenance is updated.

    ## Resolution trade-offs

    | Grid | Pros | Cons |
    |------|------|------|
    | County / coarse | Fast whole-book | Misses site nuance |
    | High-res flood | Engineering detail | Costly; false precision if building data thin |

    Match resolution to decision. Pricing triage can start coarse.

    ## Structure backward

    Week 6 needs tables with: entity id, hazard scores, scenario severities, $ metric, lineage. Design week-3 tables for that join, not for pretty maps alone.
    """,
)

c(
    "03.02-pull-hazard-data/problem",
    """
    # Problem — Pull hazard data

    ## TODO

    1. Load `firm/sample-hazard/county_hazard_scores.csv`.
    2. Map each geocoded entity to a county score (training shortcut: map by state+city using a simple city→county table you create, or nearest city match from the sample file’s metros).
    3. Save `outputs/week-3/entity_hazard_scores.csv`.
    4. Append audit log: source `firm_sample_grid`, version `v1`.

    ## Acceptance criteria

    - [ ] ≥90% entities scored (document unmatched)
    - [ ] Audit log entry complete
    - [ ] Script re-runnable
    """,
)

c(
    "03.03-asset-level-exposure-scoring/problem",
    """
    # Problem — Asset-level exposure scoring

    ## TODO

    Combine hazard scores with book $ metrics into `outputs/week-3/exposure_scores.csv`:

    - entity id
    - primary hazard and score
    - $ metric (outstanding / nav / revenue_at_risk)
    - composite `exposure_index` = f(score, $) — define and document
    - data_quality

    Write `outputs/week-3/scoring_method.md` explaining the formula (**computed**).

    ## Acceptance criteria

    - [ ] Method file defines formula
    - [ ] Top 10 by exposure_index listed in a short summary md
    """,
)

c(
    "03.03-asset-level-exposure-scoring/solution",
    """
    # Solution — Exposure scoring

    Example computed index:

    ```text
    exposure_index = (max(flood,hurricane,wildfire,heat)/10) * log10(1 + dollars)
    ```

    Any monotonic combo is fine if documented. Sort descending for deep-dives.
    """,
)

c(
    "03.04-structure-backward-from-deliverables/explainer",
    """
    # Structure backward from deliverables

    Week 6 board slide wants: “Top concentrations and what to do.”  
    Week 6 record wants: entity-level table with lineage.

    Therefore week 3 must emit **stable IDs** and **join keys** reused in weeks 4–5. Avoid renaming entities midstream.
    """,
)

c(
    "03.05-audit-log-every-pull/problem",
    """
    # Problem — Audit log every pull

    ## TODO

    1. Ensure `outputs/audit_log.jsonl` has entries for seed, geocode, and hazard load.
    2. Write `outputs/week-3/hazard_dataset_readme.md` pointing at:
       - score files
       - method file
       - audit log
       - unmatched entities
    3. Run a cold-read: ask Grok to list every data source used so far from the log only.

    ## Acceptance criteria

    - [ ] Readme is the index of the hazard dataset deliverable
    - [ ] Cold-read cites log, not vibes
    """,
)

c(
    "03.05-audit-log-every-pull/solution",
    """
    # Solution — Audit log

    JSONL lines with `ts`, `event`, `source`, `version`, `records`, `script` fields.

    Use `scripts/lib_common.append_audit` for consistency.
    """,
)

# ===== 04 Scenarios ========================================================

c(
    "04.01-standard-regulatory-scenarios/explainer",
    """
    # Standard regulatory scenarios

    Apply firm cards **STD-01**, **STD-02**, **STD-03** across scored entities for the record.

    These may not be the most decision-relevant stresses — that is fine. The record needs a recognizable standard set; judgment lives in bespoke scenarios.
    """,
)

c(
    "04.01-standard-regulatory-scenarios/problem",
    """
    # Problem — Standard scenarios

    ## TODO

    1. Implement a runner that maps STD-01/02/03 screening rules to severities using `firm/anchors/`.
    2. Output `outputs/week-4/standard_scenario_results.csv`.
    3. Summarize portfolio $ in S2+ by scenario in `standard_summary.md`.

    ## Acceptance criteria

    - [ ] Three scenarios, separate columns or stacked rows
    - [ ] No summing across scenarios in the summary
    """,
)

c(
    "04.02-bespoke-stress-from-hypotheses/problem",
    """
    # Problem — Bespoke stress from hypotheses

    ## TODO

    Build **2–3** portfolio-specific scenarios from your week-2 register. Each must:

    - Reference hypothesis IDs
    - Combine at least one STD or physical driver with a TR transmission card where relevant
    - Write results to `outputs/week-4/bespoke_<id>.csv` + narrative in `scenario_results.md`

    ## Track hints

    - Colorado: drought/heat on storage + allocation cut transmission
    - Kerrville: flash flood corridor + insurance / access transmission
    - Datacenter: heat-drought-grid + water supply contingency across EIS alternatives

    ## Acceptance criteria

    - [ ] 2–3 bespoke scenarios
    - [ ] Linked to hypotheses
    - [ ] Decision implication stated per scenario
    """,
)

c(
    "04.02-bespoke-stress-from-hypotheses/solution",
    """
    # Solution — Bespoke scenarios

    Name them like `BES-IW-01 Gulf CRE + insurance retreat`. Document parameter choices. Results feed week 5 prioritization — not a second science project.
    """,
)

c(
    "04.03-institutional-transmission/explainer",
    """
    # Institutional transmission

    Physical damage is only the first beat. Cards TR-01…TR-04 encode insurance withdrawal, credit tightening, input squeezes, and regional repricing.

    Regulators increasingly care about these second-round effects. Your board cares because they change **what to do now**.
    """,
)

c(
    "04.04-break-point-testing/problem",
    """
    # Problem — Break-point testing

    ## TODO

    Pick one bespoke scenario. Vary 2–3 assumptions (damage band mid vs high, insurance bump on/off, downtime days).  

    Save `outputs/week-4/break_points.md` showing where the decision flips (e.g., “still watchlist” vs “force pricing review”).

    ## Acceptance criteria

    - [ ] Table of parameter combos → outcome class
    - [ ] Clear break point called out
    """,
)

c(
    "04.04-break-point-testing/solution",
    """
    # Solution — Break points

    You are looking for **decision robustness**: actions that pay off on every path vs contingent on one path. Label them for week 5 recommendations.
    """,
)

c(
    "04.05-multi-agent-scenario-runs/problem",
    """
    # Problem — Multi-agent scenario runs

    ## TODO

    Use Grok **subagents** (or parallel sessions) to run standard vs bespoke scenarios without context bleed:

    1. Parent agent assigns each scenario card + data paths.
    2. Children return only result tables + 5-bullet narratives.
    3. Parent merges into `scenario_results.md`.

    Document the orchestration in `outputs/week-4/orchestration_notes.md`.

    ## Acceptance criteria

    - [ ] Notes describe split of work
    - [ ] Final merge has consistent columns
    """,
)

c(
    "04.05-multi-agent-scenario-runs/solution",
    """
    # Solution — Multi-agent runs

    Give each subagent: firm card path, anchors path, entity score CSV, output schema. Forbid children from rewriting methodology. Parent owns merge and epistemic labels.
    """,
)

c(
    "04.06-read-output-for-signal/explainer",
    """
    # Read output for signal

    Ask of every table:

    1. What is computed? What is judged?
    2. Which names drive the $ at S2+?
    3. Which hypotheses died?
    4. What would the CRO/IC/COO do Monday morning?

    If you cannot answer (4), rework before week 5.
    """,
)

# ===== 05 Synthesis ========================================================

c(
    "05.01-aggregate-and-concentration/problem",
    """
    # Problem — Aggregate and concentration

    ## TODO

    From week 3–4 tables, compute portfolio-level concentrations:

    - By geography
    - By sector/type/role
    - By scenario S2+ $ 

    Save `outputs/week-5/concentration_tables.csv` and charts data as needed.

    ## Acceptance criteria

    - [ ] At least three concentration cuts
    - [ ] Scripts re-runnable
    """,
)

c(
    "05.01-aggregate-and-concentration/solution",
    """
    # Solution — Concentration

    Correlated exposure only appears after aggregation. A stack of medium names in one MSA can dominate a single large name elsewhere — show both.
    """,
)

c(
    "05.02-priority-names/problem",
    """
    # Problem — Priority names and assets

    ## TODO

    Produce `outputs/week-5/priority_list.md` — ranked list of counterparties/assets/nodes with:

    - why prioritized
    - scenario evidence
    - recommended next management action class (price / limit / mitigate / dual-source / exit / watch)

    ## Acceptance criteria

    - [ ] Finite list (e.g., top 10–15)
    - [ ] Each has an action class
    """,
)

c(
    "05.02-priority-names/solution",
    """
    # Solution — Priority list

    Rank by decision urgency × $ × data confidence. Low-confidence large names may rank high as **watchlist / data buys**, not as false-precise loss.
    """,
)

c(
    "05.03-pricing-and-capital-language/problem",
    """
    # Problem — Pricing and capital language

    ## TODO

    Translate findings into the track’s decision language in `outputs/week-5/pricing_implications.md`.

    | Track | Language |
    |-------|----------|
    | Colorado | release cuts, allocation priority, hydropower shortfall, compact risk |
    | Kerrville | mitigation $ ROI, buyout vs defend, critical-facility uptime |
    | Datacenter | EIS significance, water MGY risk, grid interconnect, receptor impact |

    Use anchors; label judgment bands.

    ## Acceptance criteria

    - [ ] No pure hazard scores without economic translation
    - [ ] Judgment labeled where not computed
    """,
)

c(
    "05.03-pricing-and-capital-language/solution",
    """
    # Solution — Decision language

    Example Kerrville: “For $X replacement in S2+ under flash-flood BES-01, fund elevation/access projects before buyouts on the residual list (**judgment**, anchors + local precedent).”
    """,
)

c(
    "05.04-document-data-gaps/explainer",
    """
    # Document data gaps

    Gaps are deliverables. They tell the client what truth costs.

    Good gap: “No elevation certificates for 18 Houston facilities; damage bands use midpoints.”  
    Bad gap: silence.
    """,
)

c(
    "05.04-document-data-gaps/problem",
    """
    # Problem — Document data gaps

    ## TODO

    Write `outputs/week-5/data_gaps_watchlist.md` with severity (blocks decision / widens range / cosmetic) and proposed closure action.
    """,
)

c(
    "05.05-visualize-the-book/problem",
    """
    # Problem — Visualize the book

    ## TODO

    Create `outputs/week-5/portfolio_map.html` (or md + SVG) showing geocoded entities sized by $ and colored by severity or hazard.

    Keep it simple: static HTML is enough.

    ## Acceptance criteria

    - [ ] Opens in a browser offline
    - [ ] Legend explains color/size
    """,
)

c(
    "05.05-visualize-the-book/solution",
    """
    # Solution — Visualization

    Leaflet/HTML or pure SVG scatter on a simple projection. Do not block the course on web apps. Export a PNG screenshot optional for the board deck.
    """,
)

c(
    "05.06-actionable-recommendations/problem",
    """
    # Problem — Actionable recommendations

    ## TODO

    Finish `outputs/week-5/portfolio_synthesis.md` including recommendations split into:

    - **Robust** — pay off across scenarios
    - **Contingent** — pay off on a named path

    ## Acceptance criteria

    - [ ] ≥3 robust, ≥2 contingent (or justify fewer)
    - [ ] Owners/audiences named
    """,
)

c(
    "05.06-actionable-recommendations/solution",
    """
    # Solution — Recommendations

    Robust examples: fix contradictory insurance schedules on large names; dual-source a critical single supplier; standardize elevation data collection.  
    Contingent: buy parametric cover only if BES-coastal path is the IC’s concern.
    """,
)

# ===== 06 Delivery =========================================================

c(
    "06.01-two-audiences/explainer",
    """
    # Two audiences

    | | Board / IC / exec | Regulator / LP / assurance |
    |--|-------------------|----------------------------|
    | Carries | Judgment | Record |
    | Length | Short | Complete |
    | Numbers | Few, decisive | Lineage for every figure |
    | Tone | Decision | Traceable |

    Same underlying tables. Different cuts.
    """,
)

c(
    "06.02-templates-and-qa-agents/problem",
    """
    # Problem — Templates and QA agents

    ## TODO

    1. Copy `templates/board-presentation/` and `templates/regulatory-submission/` into `outputs/week-6/`.
    2. Populate from week 2–5 artifacts.
    3. Run a **fresh** Grok QA pass per `firm/qa-protocols/`.
    4. Save QA findings to `outputs/week-6/qa_findings.md` and fix blockers.

    ## Acceptance criteria

    - [ ] QA pass exists
    - [ ] Blockers resolved or explicitly accepted with rationale
    """,
)

c(
    "06.02-templates-and-qa-agents/solution",
    """
    # Solution — QA agents

    Fresh context is the point. The authoring agent is biased. Subagent prompt: “Report only failures against firm QA protocols.”
    """,
)

c(
    "06.03-trace-every-figure-to-source/problem",
    """
    # Problem — Trace every figure to source

    ## TODO

    Build `outputs/week-6/figure_lineage.csv` with columns:

    `figure_id, statement, value, kind(computed|judgment), script_or_card, inputs, notes`

    Every board headline number must appear.

    ## Acceptance criteria

    - [ ] All board headline figures listed
    - [ ] Computed rows have script paths
    """,
)

c(
    "06.03-trace-every-figure-to-source/solution",
    """
    # Solution — Lineage

    If you cannot fill a row, the figure does not ship. Delete or recompute.
    """,
)

c(
    "06.04-board-presentation/problem",
    """
    # Problem — Board presentation

    ## TODO

    Deliver `outputs/week-6/board_presentation.md` (and HTML if you export) with:

    1. Decision question
    2. Portfolio snapshot
    3. Concentrations that matter
    4. Scenario break points
    5. Pricing / exit / contingency implications
    6. Recommendations (robust vs contingent)
    7. What we need from management

    ## Acceptance criteria

    - [ ] ≤10 “slides” of content
    - [ ] Simulated banner present
    - [ ] No unexplained jargon
    """,
)

c(
    "06.04-board-presentation/solution",
    """
    # Solution — Board deck

    Lead with the ask. Put methodology in appendix. One map max. One concentration table max on the core path.
    """,
)

c(
    "06.05-export-html-pdf/problem",
    """
    # Problem — Export HTML and PDF

    ## TODO

    1. Convert board markdown to `board_presentation.html` using `scripts/export_deliverable.py` or equivalent.
    2. Convert regulatory submission to HTML.
    3. PDF optional if tooling available; HTML required.

    ## Acceptance criteria

    - [ ] HTML opens offline with basic styling
    - [ ] Paths recorded in week-6 readme
    """,
)

c(
    "06.05-export-html-pdf/solution",
    """
    # Solution — Export

    Use the provided export script (markdown → simple HTML). PDF via browser print or pandoc if installed.
    """,
)

c(
    "06.06-capstone-checklist/explainer",
    """
    # Capstone checklist

    - [ ] Week 1 plan still matches what you built (or change log written)
    - [ ] Mapped portfolio + hypotheses
    - [ ] Hazard dataset + audit log
    - [ ] Standard + bespoke scenarios (no cross-sum)
    - [ ] Synthesis with decision language
    - [ ] Board judgment pack
    - [ ] Record pack with lineage
    - [ ] QA pass completed
    - [ ] All data labeled simulated where applicable

    If all boxes pass, you have a complete training assessment — and a reusable system for a real portfolio.
    """,
)


def default_content(ex_id: str, title: str, variant: str, section: dict) -> str:
    week = section["week"]
    return dedent(
        f"""
        # {title}

        **Section:** {section['title']} (week {week})  
        **Variant:** {variant}  
        **Driving question:** {section['question']}  
        **Week deliverable:** {section['deliverable']}

        See the curriculum map in the course README. Work inside your active client track under `clients/`.
        """
    ).strip() + "\n"


def main() -> None:
    count = 0
    for section in SECTIONS:
        sec_dir = EX / section["id"]
        for ex in section["exercises"]:
            ex_dir = sec_dir / ex["id"]
            for variant in ex["variants"]:
                vdir = ex_dir / variant
                vdir.mkdir(parents=True, exist_ok=True)
                key = f"{ex['id']}/{variant}"
                body = CONTENT.get(key) or default_content(
                    ex["id"], ex["title"], variant, section
                )
                # ensure solution keys that are problem-only in CONTENT still have files
                readme = vdir / "readme.md"
                readme.write_text(body, encoding="utf-8")
                count += 1
                # solution folders for pull-hazard etc that only have problem in CONTENT
                if variant == "solution" and key not in CONTENT:
                    # richer default for solutions
                    readme.write_text(
                        dedent(
                            f"""
                            # Solution — {ex['title']}

                            ## Approach

                            1. Read the problem acceptance criteria.
                            2. Implement with a re-runnable Python script under `clients/<track>/outputs/week-{section['week']}/scripts/`.
                            3. Save tables/markdown next to the script.
                            4. Append provenance to `outputs/audit_log.jsonl`.
                            5. Cross-check a sample of rows manually against CSV/DB.

                            ## Track deltas

                            - **Colorado:** join on facilities / allocations; $. proxy = storage_kaf or allocation kaf.
                            - **Kerrville:** join on facilities / exposures; $. = replacement_usd.
                            - **Datacenter:** join on facilities / impact_topics; $. proxy = mw_nameplate / water_mgy.

                            ## Done when

                            Problem acceptance criteria pass on your active track without opening this file during the first attempt.
                            """
                        ).strip()
                        + "\n",
                        encoding="utf-8",
                    )
    print(f"Wrote {count} exercise variant readmes under {EX}")


if __name__ == "__main__":
    main()
