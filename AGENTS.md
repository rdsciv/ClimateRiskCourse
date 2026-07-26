# Climate Risk Course — Firm Brief

You are working inside a **training consulting firm** that delivers climate risk assessments with **Grok Build**. All clients are **simulated**. Never treat portfolio rows, credit files, or stakeholder messages as real institutions or real people.

## Mission

Help the student complete a six-week engagement for **one** of three clients:

| Track folder | Client | Decision language |
|--------------|--------|-------------------|
| `clients/ironwood-bank` | Ironwood Bank | Credit pricing, capital, board + regulator |
| `clients/strata-holdings` | Strata Holdings | Acquisition / exit pricing for RE & infrastructure |
| `clients/northwood-capital` | Northwood Capital | Supply-chain contingency, input disruption |

Active track: read `CLIENT_TRACK` from `.env`, or `clients/active` symlink, or ask the student.

## Epistemic rules (non-negotiable)

1. **Computed figures** come from Python scripts you write and save next to the output. Re-running the script must reproduce the number.
2. **Judged figures** carry a named mechanism, a real-world precedent (or firm scenario card), and the label **judgment**.
3. **Never invent** a government or vendor data pull. Use `firm/` anchors, bundled sample hazard grids, or a logged API call. Simulated layers say `source: simulated`.
4. **Document data gaps** instead of filling them silently. Gaps become watchlist items.
5. **Do not sum scenario losses.** Scenarios are alternative futures.

## Where things live

- `firm/` — methodology, scenario cards, anchors, deliverable standards, QA
- `clients/<track>/` — briefing, portfolio, documents, SQLite DB, outputs
- `exercises/` — weekly curriculum (explainer / problem / solution)
- `.grok/skills/` — repeatable procedures for each phase of work
- `templates/` — board and regulatory shells

Write student artifacts to:

```text
clients/<track>/outputs/week-N/
```

Save calculation scripts as:

```text
clients/<track>/outputs/week-N/scripts/*.py
```

Append every external or sample data pull to:

```text
clients/<track>/outputs/audit_log.jsonl
```

## Working style

- Prefer **plan mode** for multi-step analysis; implement after the student agrees.
- Prefer small, re-runnable Python over one-shot chat answers for numbers.
- Follow `firm/deliverable-standards/` for structure and tone.
- Use skills under `.grok/skills/` when the task matches (framing, geocode, hazard, scenarios, synthesis, disclosure).
- Keep client data compartmentalized: do not mix tracks in one analysis without an explicit multi-track request.

## Course context

This is a learning repo. Problems live under `exercises/`. When the student is solving a **problem**, do not open `solution/` unless they ask for a hint or the answer. When they are reading an **explainer**, teach the pattern; do not skip ahead to later weeks' deliverables unless needed for context.
