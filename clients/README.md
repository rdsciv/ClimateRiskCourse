# Clients — choose your track

You complete the **same six-week method** on **one** simulated client. Pick the world closest to your work.

| Track key | Folder | Who they are | Decision language |
|-----------|--------|--------------|-------------------|
| `ironwood` | `ironwood-bank/` | Commercial bank credit book | Pricing, capital, limits, board + regulator |
| `strata` | `strata-holdings/` | RE + infrastructure fund | Acquisition / hold / exit pricing, IC, LPs |
| `northwood` | `northwood-capital/` | Industrial + supply chain | Contingency, dual-source, input disruption |

## Activate a track

```bash
python3 scripts/set_track.py ironwood   # or strata | northwood
python3 scripts/seed_all_clients.py     # once after clone
```

This writes `CLIENT_TRACK` to `.env` and creates `clients/active` → your folder.

## What’s in each client folder

```text
briefing/     engagement context
portfolio/    CSV + summary JSON
documents/    messy real-world-style files
db/           portfolio.sqlite
outputs/      your weekly deliverables
AGENTS.md     track-specific agent brief
```

All data is **simulated** and labeled as such.
