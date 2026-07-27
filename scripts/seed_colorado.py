#!/usr/bin/env python3
"""Seed simulated Redrock Basin Authority — Colorado River reservoir operations."""

from __future__ import annotations

import csv
import random
import sqlite3

from lib_common import ROOT, append_audit, client_dir, write_json

SEED = 20260726
TRACK = "colorado"

# Simulated Colorado River system reservoirs / nodes (not real agency data)
NODES = [
    ("Lake Redrock Main Pool", "storage", "AZ", 36.05, -114.12, "drought_heat", 1.4),
    ("Canyon Reach Upper", "storage", "UT", 37.20, -111.30, "drought", 1.1),
    ("Desert Fork Intake", "diversion", "NV", 36.10, -114.85, "heat_drought", 0.9),
    ("Mesa Municipal Delivery", "delivery", "AZ", 33.45, -112.07, "heat", 0.8),
    ("Valley Ag District A", "ag_allocation", "CA", 33.00, -115.50, "drought_heat", 1.2),
    ("Valley Ag District B", "ag_allocation", "CA", 32.80, -115.40, "drought", 1.0),
    ("Tribal Settlement Reach", "delivery", "AZ", 34.50, -114.30, "drought", 0.7),
    ("Powerplant Tailwater", "hydropower", "AZ", 36.02, -114.74, "drought_heat", 1.3),
    ("Lower Basin Metering Hub", "delivery", "NV", 35.95, -114.90, "heat", 0.6),
    ("Upper Snowpack Proxy Node", "inflow_proxy", "CO", 39.20, -106.80, "drought", 1.0),
    ("Interbasin Transfer Gate", "transfer", "CO", 39.50, -106.20, "drought", 0.5),
    ("Environmental Pulse Reach", "environmental", "AZ", 36.15, -113.90, "heat_drought", 0.8),
]


def schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        DROP TABLE IF EXISTS facilities;
        DROP TABLE IF EXISTS allocations;
        DROP TABLE IF EXISTS geocode_cache;
        DROP TABLE IF EXISTS meta;

        CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);

        CREATE TABLE facilities (
          id TEXT PRIMARY KEY,
          name TEXT NOT NULL,
          node_type TEXT NOT NULL,
          state TEXT NOT NULL,
          address TEXT NOT NULL,
          lat REAL,
          lon REAL,
          hazard_bucket TEXT,
          storage_kaf REAL,
          criticality TEXT NOT NULL,
          data_quality TEXT NOT NULL,
          notes TEXT
        );

        CREATE TABLE allocations (
          id TEXT PRIMARY KEY,
          facility_id TEXT NOT NULL,
          beneficiary TEXT NOT NULL,
          annual_kaf REAL NOT NULL,
          priority_class TEXT NOT NULL,
          compact_sensitive INTEGER NOT NULL,
          FOREIGN KEY (facility_id) REFERENCES facilities(id)
        );

        CREATE TABLE geocode_cache (
          address_key TEXT PRIMARY KEY,
          lat REAL NOT NULL,
          lon REAL NOT NULL,
          source TEXT NOT NULL
        );
        """
    )


def seed() -> None:
    rng = random.Random(SEED)
    cdir = client_dir(TRACK)
    db_path = cdir / "db" / "portfolio.sqlite"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    schema(conn)
    conn.execute("INSERT INTO meta VALUES ('client', 'Redrock Basin Authority — SIMULATED')")
    conn.execute("INSERT INTO meta VALUES ('seed', ?)", (str(SEED),))
    conn.execute("INSERT INTO meta VALUES ('system', 'Colorado River multi-reservoir operations (training)')")
    conn.execute("INSERT INTO meta VALUES ('provenance', 'simulated')")

    catalog = list(NODES)
    while len(catalog) < 48:
        base = rng.choice(NODES)
        catalog.append(
            (
                f"{base[0]} Satellite {len(catalog)+1}",
                base[1],
                base[2],
                base[3] + rng.uniform(-0.15, 0.15),
                base[4] + rng.uniform(-0.15, 0.15),
                base[5],
                base[6] * rng.uniform(0.5, 1.1),
            )
        )

    rows = []
    total_kaf = 0.0
    for i, n in enumerate(catalog, start=1):
        name, ntype, state, lat, lon, hazard, w = n
        fid = f"CR-NOD-{i:03d}"
        storage = round(50 * w * rng.uniform(0.4, 2.5), 2) if ntype in ("storage", "hydropower") else 0.0
        total_kaf += storage
        quality = rng.choices(["clean", "incomplete", "contradictory"], weights=[0.5, 0.35, 0.15])[0]
        crit = rng.choices(["critical", "high", "medium", "low"], weights=[0.25, 0.35, 0.3, 0.1])[0]
        street = f"River Mile {100 + i} Ops Node {i}"
        notes = "Compact accounting incomplete." if quality != "clean" else ""
        conn.execute(
            """INSERT INTO facilities VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (fid, name, ntype, state, street, lat, lon, hazard, storage, crit, quality, notes),
        )
        for j in range(rng.randint(1, 3)):
            aid = f"CR-ALC-{i:03d}-{j}"
            conn.execute(
                """INSERT INTO allocations VALUES (?,?,?,?,?,?)""",
                (
                    aid,
                    fid,
                    rng.choice(["Municipal", "Irrigation", "Hydropower", "Environmental", "Tribal", "Industrial"]),
                    round(rng.uniform(5, 400) * w, 2),
                    rng.choice(["senior", "junior", "settlement", "surplus"]),
                    1 if rng.random() < 0.55 else 0,
                ),
            )
        key = f"{street}|{state}"
        conn.execute(
            "INSERT INTO geocode_cache VALUES (?,?,?,?)",
            (key, lat, lon, "simulated_offline"),
        )
        rows.append(
            {
                "facility_id": fid,
                "name": name,
                "node_type": ntype,
                "state": state,
                "storage_kaf": storage,
                "criticality": crit,
                "hazard_bucket": hazard,
                "data_quality": quality,
                "lat": lat,
                "lon": lon,
            }
        )

    conn.commit()
    conn.close()

    port = cdir / "portfolio"
    port.mkdir(parents=True, exist_ok=True)
    with (port / "reservoir_nodes.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    write_json(
        port / "summary.json",
        {
            "client": "Redrock Basin Authority",
            "simulated": True,
            "nodes": len(rows),
            "storage_kaf_sum": round(total_kaf, 2),
            "seed": SEED,
            "theme": "Colorado River reservoir management",
        },
    )

    docs = cdir / "documents"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "stakeholder_messages.md").write_text(
        """# Stakeholder messages — Redrock Basin Authority (SIMULATED)

## General manager

We need a decision pack before the spring operations call: if inflow stays at the dry-year envelope, which releases and deliveries break first, and what can we defend to municipal and ag boards?

## Compact counsel

Keep interstate accounting assumptions explicit. Do not invent BOR or Reclamation figures — use firm sample hazard and our simulated node book only, labeled as training data.

## Hydropower desk

Show which nodes couple storage drawdown to generation shortfall. We need contingency language, not a press release.
""",
        encoding="utf-8",
    )
    (docs / "ops_constraints.md").write_text(
        """# Ops constraints excerpt (SIMULATED)

- Minimum environmental pulse: seasonal; exact cfs schedule TBD (data gap).
- Ag District A has senior priority language in settlement term sheet (draft).
- Interbasin transfer gate: political approval required above threshold — model as binary option, not continuous.
""",
        encoding="utf-8",
    )

    briefing = cdir / "briefing"
    briefing.mkdir(parents=True, exist_ok=True)
    (briefing / "engagement.md").write_text(
        """# Engagement briefing — Redrock Basin Authority (SIMULATED)

**Client type:** Multi-reservoir operator on a Colorado River–style system (training construct)  
**Book:** ~48 storage, diversion, delivery, hydropower, and environmental nodes  
**Question:** Under drought and heat stress, which operating rules and allocations fail first — and what resilient release / allocation strategy should leadership take to boards?

## Decision language

Reservoir releases, allocation cuts, compact-sensitive deliveries, hydropower contingency, environmental pulse risk.

## Success

Mapped system, hazard scores (drought/heat), standard + bespoke water-operations scenarios, synthesis with priority actions, board pack + record for compact-aware stakeholders.

## Guardrails

All nodes and volumes are **simulated**. Do not present as official Reclamation, Compact, or state data.
""",
        encoding="utf-8",
    )

    (cdir / "outputs").mkdir(parents=True, exist_ok=True)
    (cdir / "outputs" / ".gitkeep").write_text("", encoding="utf-8")
    (cdir / "AGENTS.md").write_text(
        """# Redrock Basin Authority engagement (SIMULATED)

Colorado River–style **reservoir operations** climate risk assessment.

Decision language: **releases, allocations, compact-sensitive deliveries, hydropower contingency**.

- DB: `db/portfolio.sqlite`
- Nodes: `portfolio/reservoir_nodes.csv`
- Outputs: `outputs/week-N/`
""",
        encoding="utf-8",
    )

    append_audit(
        TRACK,
        {
            "event": "seed_client",
            "client": "colorado",
            "source": "scripts/seed_colorado.py",
            "records": len(rows),
            "db": str(db_path.relative_to(ROOT)),
        },
    )
    print(f"Seeded Redrock Basin Authority → {db_path} ({len(rows)} nodes)")


if __name__ == "__main__":
    seed()
