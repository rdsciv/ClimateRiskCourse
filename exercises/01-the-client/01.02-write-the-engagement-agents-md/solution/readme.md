# Solution — Engagement AGENTS.md

## Approach

Encode **audience + decision language + paths + guardrails**. Keep it short enough that it always loads.

## Ironwood sketch

```markdown
# Ironwood Bank (SIMULATED)

Commercial credit climate risk engagement.
Decision language: pricing, capital, limits.
Audiences: CRO, board, parent risk, regulator dry-run.

Data: db/portfolio.sqlite, portfolio/loan_book.csv, documents/
Outputs: outputs/week-N/
All data simulated. Computed figures from Python; judgments labeled.
Out of scope: full IFRS9 model rebuild; sovereign book; transition-only policy lobbying memo.
```

## Strata / Northwood

Swap decision language to exit pricing or contingency; keep the same structure.

## Check

Cold session should refuse out-of-scope work and know the DB path without hunting.
