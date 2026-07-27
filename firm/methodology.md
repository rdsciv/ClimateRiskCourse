# Firm methodology — climate risk assessments

This firm produces **decision-grade** climate risk work: hazard signal joined to portfolio economics, carried through to an action the client can take. Disclosure is a by-product of that work, not the product.

All training clients are **simulated**. The method is real.

## What we optimize for

1. **Decisions, not scores.** A hazard percentile without operational, capital, mitigation, or permitting implications is incomplete.
2. **Legible epistemology.** Every material number is either **computed** (script + data) or **judged** (mechanism + precedent + label).
3. **Assurability.** A skeptical reviewer can re-run computations and inspect judgment rationale without trusting the presenter’s CV.
4. **Graceful degradation.** Thin data widens ranges and grows the watchlist; it does not authorize silent invention.

## Engagement arc (six weeks)

| Week | Question | Deliverable |
|------|----------|-------------|
| 1 | What does the client need? | Framing & delivery plan |
| 2 | Where does risk concentrate? | Mapped portfolio + hypothesis register |
| 3 | Which hazard data matters? | Organized hazard dataset + audit log |
| 4 | Which scenarios bite? | Standard + bespoke scenario results |
| 5 | What should change? | Portfolio synthesis + pricing/decision implications |
| 6 | Will it stand up? | Board/IC judgment + regulatory/stakeholder record |

## Computed vs judged

### Computed

- Portfolio aggregates, concentrations, joins of hazard scores to exposures
- Scenario severity applied through encoded damage/LGD bands from `firm/anchors/`
- Maps, tables, counts of facilities in hazard buckets

**Rule:** Write a Python script, save it under `outputs/week-N/scripts/`, save stdout or CSV/JSON outputs beside it. Re-run must match.

### Judged

- How a market reprices, how a lender behaves, how insurance withdrawal transmits
- Which bespoke scenarios are most relevant for *this* book
- Recommendation priority when multiple robust actions compete

**Rule:** Label **judgment**. Cite a firm scenario card and/or a named real-world precedent. Give a range when the point estimate is false precision.

## Scenario discipline

- Standard scenarios (see `scenario-cards/`) satisfy “for the record” audiences.
- Bespoke scenarios (2–3) are built from week-2 hypotheses and institutional transmission (insurance, credit, logistics, policy).
- Scenarios are **alternative futures**. Never sum losses across scenarios.
- Prefer severity-ordered, severe-but-plausible framing over false probability precision unless the client methodology demands probabilities.

## Data provenance

- Simulated training data: `source: simulated` in audit log and meta tables.
- Bundled hazard sample grids: `source: firm_sample_grid` with version id.
- Live API pulls: log URL/params/timestamp/hash or row counts; never attribute a real agency name to invented numbers.

## Resolution ladder

1. Whole-book screen (sector / geography / role)
2. Segment deep-dives where concentration or hypothesis warrants
3. Asset-level only for names that earn the cost of depth

Document why names were escalated or left at screen level.

## Outputs by audience

| Audience | Artifact | Carries |
|----------|----------|---------|
| Board / council / project exec | Presentation | Judgment, priorities, decisions |
| Regulator / grant / EIS administrative record | Submission pack | Record, lineage, assumptions, gaps |

## Tooling

Grok Build is the harness. Python is the calculator. Firm files are the house methodology. Students direct; the agent accelerates.
