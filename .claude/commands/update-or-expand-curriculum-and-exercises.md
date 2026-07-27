---
name: update-or-expand-curriculum-and-exercises
description: Workflow command scaffold for update-or-expand-curriculum-and-exercises in ClimateRiskCourse.
allowed_tools: ["Bash", "Read", "Write", "Grep", "Glob"]
---

# /update-or-expand-curriculum-and-exercises

Use this workflow when working on **update-or-expand-curriculum-and-exercises** in `ClimateRiskCourse`.

## Goal

Adds or updates curriculum content and exercises, including explainer/problem/solution files and corresponding documentation.

## Common Files

- `exercises/*/*/*/readme.md`
- `docs/reading/ex-*.html`
- `docs/reading/ex-*.mdx`
- `docs/curriculum.html`
- `docs/weeks/week-*.mdx`
- `scripts/generate_exercises.py`

## Suggested Sequence

1. Understand the current state and failure mode before editing.
2. Make the smallest coherent change that satisfies the workflow goal.
3. Run the most relevant verification for touched files.
4. Summarize what changed and what still needs review.

## Typical Commit Signals

- Add or update files in exercises/<module>/<exercise>/<type>/readme.md.
- Update docs/reading/ex-*.html and docs/reading/ex-*.mdx for corresponding curriculum readings.
- Update or add scripts/generate_exercises.py and related scripts.
- Update docs/curriculum.html and docs/weeks/week-*.mdx as needed.
- Update README.md and CONTRIBUTING.md to reflect curriculum changes.

## Notes

- Treat this as a scaffold, not a hard-coded script.
- Update the command if the workflow evolves materially.