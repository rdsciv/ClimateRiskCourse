```markdown
# ClimateRiskCourse Development Patterns

> Auto-generated skill from repository analysis

## Overview
This skill teaches you how to contribute to the ClimateRiskCourse repository, a Python-based educational codebase for climate risk curriculum development. You'll learn the project's coding conventions, how to add or update client tracks, expand curriculum exercises, revamp the documentation site, and improve onboarding processes. The guide includes step-by-step workflows, code examples, and suggested commands for common tasks.

## Coding Conventions

**File Naming**
- Use camelCase for file names.
  - Example: `generateExercises.py`, `seedAllClients.py`

**Import Style**
- Use relative imports within modules.
  - Example:
    ```python
    from .utils import loadPortfolio
    ```

**Export Style**
- Use named exports (explicitly define what is exported from a module).
  - Example:
    ```python
    def calculateRisk(...):
        ...
    __all__ = ['calculateRisk']
    ```

**Directory Structure**
- Organized by feature: `clients/`, `docs/`, `exercises/`, `scripts/`
- Exercises are structured as `exercises/<module>/<exercise>/<type>/readme.md`

## Workflows

### Add or Update Client Track
**Trigger:** When introducing a new client scenario or revising client tracks  
**Command:** `/add-client-track`

1. Add or update directories under `clients/` with:
    - `AGENTS.md`
    - `briefing/engagement.md`
    - `db/portfolio.sqlite`
    - `documents/*.md`
    - `outputs/.gitkeep`
    - `portfolio/*.csv`
    - `portfolio/summary.json`
2. Update documentation:
    - `docs/clients.html`
    - `docs/reading/clients-overview.html`
    - `docs/reading/ex-00.03-choose-your-client-track.html`
3. Update exercises:
    - `exercises/00-orientation/00.03-choose-your-client-track/problem/readme.md`
    - `exercises/00-orientation/00.03-choose-your-client-track/explainer/readme.md`
4. Update or add seeding scripts:
    - `scripts/seed_<client>.py`
    - `scripts/seed_all_clients.py`
5. Update `README.md` and `clients/README.md` to reflect changes.

**Example:**
```bash
# Add a new client track
/add-client-track
```

---

### Update or Expand Curriculum and Exercises
**Trigger:** When adding new exercises, updating existing ones, or expanding curriculum  
**Command:** `/add-exercise`

1. Add or update exercise files:
    - `exercises/<module>/<exercise>/<type>/readme.md`
2. Update curriculum documentation:
    - `docs/reading/ex-*.html`
    - `docs/reading/ex-*.mdx`
    - `docs/curriculum.html`
    - `docs/weeks/week-*.mdx`
3. Update or add exercise generation scripts:
    - `scripts/generate_exercises.py`
4. Update `README.md` and `CONTRIBUTING.md` as needed.

**Example:**
```bash
# Add a new exercise to module 01
/add-exercise
```

---

### Docs Site Revamp or Content Sync
**Trigger:** When launching a new docs version, migrating docs framework, or syncing large content changes  
**Command:** `/update-docs-site`

1. Add or update files in `docs/` (HTML, MDX, CSS, JS, assets).
2. Update or add build scripts:
    - `scripts/build_docs_site.py`
    - `scripts/build_cool_site.py`
3. Update CI/CD workflow:
    - `.github/workflows/pages.yml`
4. Update `README.md` to document site changes.
5. Update docs configuration:
    - `docs/docs.json` or similar.

**Example:**
```bash
# Revamp documentation site
/update-docs-site
```

---

### Course Setup and Onboarding Improvement
**Trigger:** When improving onboarding or updating setup instructions  
**Command:** `/improve-onboarding`

1. Update onboarding documentation:
    - `README.md`
    - `CONTRIBUTING.md`
    - `INSTRUCTOR.md`
2. Update dependency management:
    - `package.json`
    - `pyproject.toml`
    - `uv.lock`
3. Update or add setup scripts:
    - `scripts/generate_exercises.py`
4. Update CI/CD workflow if needed:
    - `.github/workflows/pages.yml`

**Example:**
```bash
# Improve onboarding process
/improve-onboarding
```

## Testing Patterns

- **Framework:** Unknown (not explicitly detected)
- **File Pattern:** Test files use the pattern `*.test.*`
    - Example: `portfolio.test.py`
- Tests are likely placed alongside or near the modules they test.
- To run tests, look for standard Python test runners (e.g., `pytest`) or custom scripts.

## Commands

| Command              | Purpose                                                         |
|----------------------|-----------------------------------------------------------------|
| /add-client-track    | Add or update a client scenario and all related documentation   |
| /add-exercise        | Add or update curriculum exercises and related documentation    |
| /update-docs-site    | Revamp or sync the documentation site                          |
| /improve-onboarding  | Improve or standardize course setup and onboarding instructions |
```
