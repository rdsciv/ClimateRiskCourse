# Contributing

## Local development

```bash
python3 scripts/seed_all_clients.py
python3 scripts/course_lint.py
python3 scripts/build_docs_site.py
```

Open `docs/index.html` or serve:

```bash
python3 -m http.server 8080 --directory docs
```

## Regenerating curriculum text

Exercise readmes are generated from `scripts/generate_exercises.py` + `scripts/course_manifest.py`. Prefer editing the generator, then re-run:

```bash
python3 scripts/generate_exercises.py
python3 scripts/build_docs_site.py
```

## Pull requests

1. Keep all client data labeled **simulated**.
2. Do not commit `.env` or real credentials.
3. Ensure `python3 scripts/course_lint.py` passes.
4. Rebuild docs if firm/ or explainer content changed.
