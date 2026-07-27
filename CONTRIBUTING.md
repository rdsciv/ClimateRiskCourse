# Contributing

## Local development

```bash
git clone https://github.com/rdsciv/ClimateRiskCourse.git
cd ClimateRiskCourse
uv sync
uv run scripts/seed_all_clients.py
uv run scripts/course_lint.py
```

Docs (Mintlify):

```bash
cd docs && npx mintlify dev
```

## Regenerating curriculum text

Exercise readmes are generated from `scripts/generate_exercises.py` + `scripts/course_manifest.py`. Prefer editing the generator, then re-run:

```bash
uv run scripts/generate_exercises.py
# update docs/*.mdx if curriculum copy changes
```

## Pull requests

1. Keep all client data labeled **simulated**.
2. Do not commit `.env` or real credentials.
3. Ensure `uv run scripts/course_lint.py` passes.
4. Rebuild docs if firm/ or explainer content changed.
5. Document student-facing commands with **`uv run`**, not system `python3` / `pip`.
