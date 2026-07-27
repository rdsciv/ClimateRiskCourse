---
name: docs-site-revamp-or-content-sync
description: Workflow command scaffold for docs-site-revamp-or-content-sync in ClimateRiskCourse.
allowed_tools: ["Bash", "Read", "Write", "Grep", "Glob"]
---

# /docs-site-revamp-or-content-sync

Use this workflow when working on **docs-site-revamp-or-content-sync** in `ClimateRiskCourse`.

## Goal

Major update or overhaul of the documentation site, including new content, site structure, and build scripts.

## Common Files

- `docs/**/*`
- `scripts/build_docs_site.py`
- `scripts/build_cool_site.py`
- `.github/workflows/pages.yml`
- `README.md`
- `docs/docs.json`

## Suggested Sequence

1. Understand the current state and failure mode before editing.
2. Make the smallest coherent change that satisfies the workflow goal.
3. Run the most relevant verification for touched files.
4. Summarize what changed and what still needs review.

## Typical Commit Signals

- Add or update files in docs/ (HTML, MDX, CSS, JS, assets).
- Update or add scripts/build_docs_site.py or scripts/build_cool_site.py.
- Update .github/workflows/pages.yml for CI/CD deployment.
- Update README.md to document site changes.
- Update docs/docs.json or similar config for docs frameworks.

## Notes

- Treat this as a scaffold, not a hard-coded script.
- Update the command if the workflow evolves materially.