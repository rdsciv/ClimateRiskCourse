---
name: add-or-update-client-track
description: Workflow command scaffold for add-or-update-client-track in ClimateRiskCourse.
allowed_tools: ["Bash", "Read", "Write", "Grep", "Glob"]
---

# /add-or-update-client-track

Use this workflow when working on **add-or-update-client-track** in `ClimateRiskCourse`.

## Goal

Adds a new client track or updates existing client tracks, including all related data, documentation, and seed scripts.

## Common Files

- `clients/*/AGENTS.md`
- `clients/*/briefing/engagement.md`
- `clients/*/db/portfolio.sqlite`
- `clients/*/documents/*.md`
- `clients/*/outputs/.gitkeep`
- `clients/*/portfolio/*.csv`

## Suggested Sequence

1. Understand the current state and failure mode before editing.
2. Make the smallest coherent change that satisfies the workflow goal.
3. Run the most relevant verification for touched files.
4. Summarize what changed and what still needs review.

## Typical Commit Signals

- Add or update directories under clients/ with AGENTS.md, briefing, db, documents, outputs, portfolio, and summary files.
- Update docs/clients.html, docs/reading/clients-overview.html, and related docs/reading/ex-00.03-choose-your-client-track.html.
- Update exercises/00-orientation/00.03-choose-your-client-track/problem/readme.md and explainer/readme.md.
- Update or add scripts/seed_<client>.py and scripts/seed_all_clients.py.
- Update README.md and clients/README.md to reflect new tracks.

## Notes

- Treat this as a scaffold, not a hard-coded script.
- Update the command if the workflow evolves materially.