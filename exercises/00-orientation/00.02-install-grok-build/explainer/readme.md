# Install Grok Build

## What you need

- Grok Build CLI authenticated and working in a terminal
- Python 3.11+
- Git
- This repository cloned

## Project rules

This repo’s root `AGENTS.md` is loaded by Grok automatically. It tells the agent you are in a **training firm** with epistemic rules. Do not delete it.

## Verify

From the repo root:

```bash
python3 --version
python3 scripts/seed_all_clients.py
python3 scripts/set_track.py colorado
python3 scripts/course_lint.py
```

Then start Grok in this directory and ask:

> Summarize firm/methodology.md in five bullets. Do not open any solution folders.
