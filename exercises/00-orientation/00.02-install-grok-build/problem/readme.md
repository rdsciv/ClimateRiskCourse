# Problem — Install Grok Build

## Goal

Prove your environment can run the course offline.

## TODO

1. Authenticate Grok Build and open a session in this repo.
2. Run `uv sync` (if you have not already).
3. Run `uv run scripts/seed_all_clients.py`.
4. Run `uv run scripts/set_track.py <your-track>`.
5. Confirm `clients/active` points at your folder and `.env` has `CLIENT_TRACK`.
6. Ask Grok to read `AGENTS.md` and restate the five epistemic rules.

## Acceptance criteria

- [ ] All three client DBs exist under `clients/*/db/portfolio.sqlite`
- [ ] Active track set
- [ ] You can explain computed vs judged without looking it up
