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
