#!/usr/bin/env python3
"""Seed simulated City of Kerrville flood-risk engagement (Guadalupe River corridor)."""

from __future__ import annotations

import csv
import random
import sqlite3

from lib_common import ROOT, append_audit, client_dir, write_json

SEED = 20260726
TRACK = "kerrville"

# Kerrville / Kerr County area — simulated parcels & facilities (training)
# Center ~ Kerrville, TX 30.0474, -99.1403
BASE_LAT, BASE_LON = 30.0474, -99.1403

FACILITY_TYPES = [
    ("critical_facility", "Hospital / clinic"),
    ("critical_facility", "Fire / EMS station"),
    ("critical_facility", "Water treatment"),
    ("critical_facility", "Wastewater plant"),
    ("critical_facility", "Electrical substation"),
    ("residential", "Single-family cluster"),
    ("residential", "Multifamily"),
    ("commercial", "Downtown retail block"),
    ("commercial", "Riverfront lodging"),
    ("industrial", "Light industrial yard"),
    ("infrastructure", "Bridge / low-water crossing"),
    ("infrastructure", "River park & trailhead"),
    ("school", "Public school campus"),
    ("residential", "RV / mobile home park"),
]


def schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        DROP TABLE IF EXISTS facilities;
        DROP TABLE IF EXISTS exposures;
        DROP TABLE IF EXISTS geocode_cache;
        DROP TABLE IF EXISTS meta;

        CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);

        CREATE TABLE facilities (
          id TEXT PRIMARY KEY,
          name TEXT NOT NULL,
          facility_type TEXT NOT NULL,
          use_class TEXT NOT NULL,
          address TEXT NOT NULL,
          city TEXT NOT NULL,
          state TEXT NOT NULL,
          lat REAL,
          lon REAL,
          hazard_bucket TEXT,
          flood_zone_hint TEXT NOT NULL,
          insured INTEGER NOT NULL,
          data_quality TEXT NOT NULL,
          notes TEXT
        );

        CREATE TABLE exposures (
          id TEXT PRIMARY KEY,
          facility_id TEXT NOT NULL,
          replacement_usd REAL NOT NULL,
          population_served INTEGER,
          road_access_critical INTEGER NOT NULL,
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
    conn.execute("INSERT INTO meta VALUES ('client', 'City of Kerrville — SIMULATED')")
    conn.execute("INSERT INTO meta VALUES ('seed', ?)", (str(SEED),))
    conn.execute("INSERT INTO meta VALUES ('geography', 'Kerrville / Guadalupe River corridor, TX')")
    conn.execute("INSERT INTO meta VALUES ('provenance', 'simulated')")

    rows = []
    total_usd = 0.0
    n = 80
    for i in range(1, n + 1):
        use, label = rng.choice(FACILITY_TYPES)
        fid = f"KV-FAC-{i:03d}"
        # Jitter around Kerrville; pull some toward river corridor (slightly lower elev / south-east)
        lat = BASE_LAT + rng.uniform(-0.08, 0.08)
        lon = BASE_LON + rng.uniform(-0.10, 0.10)
        near_river = rng.random() < 0.45
        if near_river:
            lat = BASE_LAT + rng.uniform(-0.04, 0.02)
            lon = BASE_LON + rng.uniform(-0.05, 0.06)
            hazard = rng.choice(["flood", "high_flood", "flood_flash"])
            zone = rng.choice(["AE", "A", "AO", "X_shaded"])
        else:
            hazard = rng.choice(["flood", "inland", "heat"])
            zone = rng.choice(["X", "X", "X_shaded", "A"])
        quality = rng.choices(["clean", "incomplete", "contradictory"], weights=[0.4, 0.4, 0.2])[0]
        street_no = rng.randint(100, 2400)
        address = f"{street_no + i} {rng.choice(['Water', 'Guadalupe', 'Main', 'Junction', 'Sidney Baker', 'River'])} St"
        name = f"{label} {i:03d}"
        insured = 1 if rng.random() > 0.2 else 0
        notes = ""
        if quality == "contradictory":
            notes = "Elevation certificate conflicts with older survey."
        elif quality == "incomplete":
            notes = "No first-floor elevation on file."
        repl = round(rng.uniform(0.4e6, 45e6) * (1.4 if use == "critical_facility" else 1.0), 2)
        total_usd += repl
        conn.execute(
            """INSERT INTO facilities VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                fid,
                name,
                use,
                label,
                address,
                "Kerrville",
                "TX",
                lat,
                lon,
                hazard,
                zone,
                insured,
                quality,
                notes,
            ),
        )
        conn.execute(
            """INSERT INTO exposures VALUES (?,?,?,?,?)""",
            (
                f"KV-EXP-{i:03d}",
                fid,
                repl,
                rng.randint(0, 12000) if use == "critical_facility" else rng.randint(0, 200),
                1 if use in ("critical_facility", "infrastructure") else 0,
            ),
        )
        key = f"{address}|Kerrville|TX"
        conn.execute(
            "INSERT INTO geocode_cache VALUES (?,?,?,?)",
            (key, lat, lon, "simulated_offline"),
        )
        rows.append(
            {
                "facility_id": fid,
                "name": name,
                "facility_type": use,
                "flood_zone_hint": zone,
                "replacement_usd": repl,
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
    with (port / "flood_assets.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    write_json(
        port / "summary.json",
        {
            "client": "City of Kerrville",
            "simulated": True,
            "facilities": len(rows),
            "replacement_usd": round(total_usd, 2),
            "seed": SEED,
            "theme": "Municipal flood risk — Kerrville, TX",
        },
    )

    docs = cdir / "documents"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "stakeholder_messages.md").write_text(
        """# Stakeholder messages — City of Kerrville (SIMULATED)

## City manager

After the Hill Country flood disasters, council wants a clear list: which critical facilities and neighborhoods need action this budget cycle, and what is still a watchlist because data is thin.

## Emergency management

Prioritize life-safety and access (bridges, low-water crossings, hospital, water plant). Separate flash-flood corridor risk from wide AE-zone residual risk.

## Finance

We need mitigation ROI language for bonds and grants — not a hazard score dump.
""",
        encoding="utf-8",
    )
    (docs / "floodplain_notes.md").write_text(
        """# Floodplain notes (SIMULATED)

- Training flood_zone_hint values are labels for exercises, not official FEMA map products.
- Guadalupe corridor parcels flagged high_flood / flood_flash for scenario screening.
- Several elevation certificates missing — document as data gaps.
""",
        encoding="utf-8",
    )

    briefing = cdir / "briefing"
    briefing.mkdir(parents=True, exist_ok=True)
    (briefing / "engagement.md").write_text(
        """# Engagement briefing — City of Kerrville flood risk (SIMULATED)

**Client type:** Municipal government, Kerrville, Texas (Guadalupe River / Hill Country)  
**Book:** ~80 critical facilities, neighborhoods, and infrastructure assets (simulated)  
**Question:** Where does flood risk force capital projects, buyouts, or operational changes — and can council and grant reviewers trust the trail?

## Decision language

Mitigation priority, access resilience, critical-facility continuity, buyout vs defend, insurance gaps.

## Success

Mapped asset book, flood-oriented hazard scores, standard + flash-flood bespoke scenarios, synthesis with budget-actionable recommendations, council presentation + grant-ready record.

## Guardrails

Asset list and dollars are **simulated**. Do not present as official City GIS or FEMA products unless you log a real pull (course default is offline sample grids).
""",
        encoding="utf-8",
    )

    (cdir / "outputs").mkdir(parents=True, exist_ok=True)
    (cdir / "outputs" / ".gitkeep").write_text("", encoding="utf-8")
    (cdir / "AGENTS.md").write_text(
        """# City of Kerrville flood engagement (SIMULATED)

**Municipal flood risk** along the Guadalupe / Hill Country corridor (training data).

Decision language: **mitigation priority, critical facilities, access, buyout vs defend**.

- DB: `db/portfolio.sqlite`
- Assets: `portfolio/flood_assets.csv`
- Outputs: `outputs/week-N/`
""",
        encoding="utf-8",
    )

    append_audit(
        TRACK,
        {
            "event": "seed_client",
            "client": "kerrville",
            "source": "scripts/seed_kerrville.py",
            "records": len(rows),
            "db": str(db_path.relative_to(ROOT)),
        },
    )
    print(f"Seeded City of Kerrville → {db_path} ({len(rows)} facilities)")


if __name__ == "__main__":
    seed()
