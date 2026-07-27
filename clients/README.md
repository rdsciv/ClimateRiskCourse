# Clients — choose your track

You complete the **same six-week method** on **one** simulated client. Pick the world closest to your work.

| Track key | Folder | Who they are | Decision language |
|-----------|--------|--------------|-------------------|
| `colorado` | `colorado-river-reservoirs/` | Redrock Basin Authority — Colorado River–style multi-reservoir operations | Releases, allocations, compact-sensitive deliveries, hydropower |
| `kerrville` | `kerrville-flood/` | City of Kerrville, TX — municipal flood risk | Mitigation priority, critical facilities, access, buyout vs defend |
| `datacenter` | `texas-datacenter-eis/` | Horizon Grid LLC — Texas data center EIS | Alternatives, water, power/grid, receptors, mitigation |

## Activate a track

```bash
python3 scripts/set_track.py colorado   # or kerrville | datacenter
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

All data is **simulated** and labeled as such. Geography may reference real places (e.g. Kerrville, Texas) for realism; the books and figures are fictional training constructs.
