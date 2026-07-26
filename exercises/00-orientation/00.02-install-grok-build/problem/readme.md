# Problem — Install Grok Build

## Goal

Prove your environment can run the course offline.

## TODO

1. Authenticate Grok Build and open a session in this repo.
2. Run `python3 scripts/seed_all_clients.py`.
3. Run `python3 scripts/set_track.py <your-track>`.
4. Confirm `clients/active` points at your folder and `.env` has `CLIENT_TRACK`.
5. Ask Grok to read `AGENTS.md` and restate the five epistemic rules.

## Acceptance criteria

- [ ] All three client DBs exist under `clients/*/db/portfolio.sqlite`
- [ ] Active track set
- [ ] You can explain computed vs judged without looking it up
