#!/usr/bin/env python3
"""Seed simulated Strata Holdings portfolio (RE + infrastructure fund)."""

from __future__ import annotations

import csv
import random
import sqlite3
from pathlib import Path

from lib_common import ROOT, append_audit, client_dir, write_json

SEED = 20260724
TRACK = "strata"

ASSETS = [
    # (name, type, city, state, lat, lon, hazard, aum_weight)
    ("Harbor Point Office Tower", "office", "Miami", "FL", 25.77, -80.19, "hurricane_flood", 1.2),
    ("Bayou Logistics Park", "industrial", "Houston", "TX", 29.75, -95.36, "flood", 1.0),
    ("Sunbelt Multifamily I", "multifamily", "Tampa", "FL", 27.95, -82.45, "hurricane", 0.9),
    ("Piedmont Data Campus", "datacenter", "Atlanta", "GA", 33.76, -84.39, "heat_grid", 1.5),
    ("Desert Edge Solar + BESS", "renewables", "Phoenix", "AZ", 33.44, -112.08, "heat_drought", 1.1),
    ("Cascade Wind Ridge", "renewables", "Portland", "OR", 45.52, -122.67, "wildfire", 0.8),
    ("Central Valley Cold Storage", "industrial", "Sacramento", "CA", 38.58, -121.49, "wildfire_flood", 0.7),
    ("Great Lakes Warehouse Cluster", "industrial", "Chicago", "IL", 41.87, -87.64, "flood", 0.9),
    ("Capital Corridor Medical RE", "healthcare_re", "Boston", "MA", 42.36, -71.06, "coastal", 0.8),
    ("Gulfport Terminal Leasehold", "infra", "New Orleans", "LA", 29.95, -90.08, "flood_hurricane", 1.3),
    ("Front Range Business Park", "office_flex", "Denver", "CO", 39.74, -104.99, "wildfire_hail", 0.7),
    ("Norfolk Port Adjacent Yard", "infra", "Norfolk", "VA", 36.85, -76.29, "flood", 1.0),
    ("SoCal Last-Mile Hub", "logistics", "Los Angeles", "CA", 34.05, -118.24, "wildfire", 0.9),
    ("Empire State Floor Plate", "office", "New York", "NY", 40.75, -73.99, "coastal_flood", 1.4),
    ("Carolinas Retail Strip", "retail", "Charleston", "SC", 32.78, -79.93, "hurricane", 0.5),
    ("Prairie Grain Elevator REIT", "ag_infra", "Kansas City", "MO", 39.10, -94.58, "flood_tornado", 0.6),
    ("PNW Timberland Note", "timber", "Seattle", "WA", 47.60, -122.33, "wildfire", 0.4),
    ("Texas Interchange Industrial", "industrial", "Dallas", "TX", 32.78, -96.80, "heat_hail", 0.8),
    ("Florida Keys Hospitality", "hospitality", "Key West", "FL", 24.56, -81.78, "hurricane_slr", 0.6),
    ("Mid-Atlantic Fiber Hut", "datacenter", "Ashburn", "VA", 39.04, -77.49, "grid", 1.2),
]


def schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        DROP TABLE IF EXISTS assets;
        DROP TABLE IF EXISTS valuations;
        DROP TABLE IF EXISTS geocode_cache;
        DROP TABLE IF EXISTS meta;

        CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);

        CREATE TABLE assets (
          id TEXT PRIMARY KEY,
          name TEXT NOT NULL,
          asset_type TEXT NOT NULL,
          city TEXT NOT NULL,
          state TEXT NOT NULL,
          address TEXT NOT NULL,
          lat REAL,
          lon REAL,
          hazard_bucket TEXT,
          nav_usd REAL NOT NULL,
          hold_period_years INTEGER NOT NULL,
          insurance_status TEXT NOT NULL,
          data_quality TEXT NOT NULL,
          notes TEXT
        );

        CREATE TABLE valuations (
          asset_id TEXT PRIMARY KEY,
          entry_cap_rate REAL,
          underwritten_exit_year INTEGER,
          climate_adjustment_bps INTEGER DEFAULT 0,
          FOREIGN KEY (asset_id) REFERENCES assets(id)
        );

        CREATE TABLE geocode_cache (
          address_key TEXT PRIMARY KEY,
          lat REAL NOT NULL,
          lon REAL NOT NULL,
          source TEXT NOT NULL
        );
        """
    )


def seed() -> Path:
    rng = random.Random(SEED)
    cdir = client_dir(TRACK)
    db_path = cdir / "db" / "portfolio.sqlite"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    schema(conn)
    conn.execute("INSERT INTO meta VALUES ('client', 'Strata Holdings — SIMULATED')")
    conn.execute("INSERT INTO meta VALUES ('seed', ?)", (str(SEED),))
    conn.execute("INSERT INTO meta VALUES ('aum_target_usd', '2400000000')")
    conn.execute("INSERT INTO meta VALUES ('provenance', 'simulated')")

    rows = []
    # Expand base list to ~45 with variants
    catalog = list(ASSETS)
    while len(catalog) < 45:
        base = rng.choice(ASSETS)
        catalog.append(
            (
                f"{base[0]} Extension {len(catalog)+1}",
                base[1],
                base[2],
                base[3],
                base[4] + rng.uniform(-0.05, 0.05),
                base[5] + rng.uniform(-0.05, 0.05),
                base[6],
                base[7] * rng.uniform(0.6, 1.1),
            )
        )

    total_nav = 0.0
    for i, a in enumerate(catalog, start=1):
        name, atype, city, state, lat, lon, hazard, weight = a
        aid = f"ST-AST-{i:03d}"
        nav = round(15e6 * weight * rng.uniform(0.8, 1.4), 2)
        total_nav += nav
        quality = rng.choices(["clean", "incomplete", "contradictory"], weights=[0.5, 0.35, 0.15])[0]
        insurance = rng.choice(["full", "sublimited", "exclusions_flood", "in_market_review"])
        street = f"{rng.randint(50, 4000)} Portfolio Drive"
        notes = ""
        if quality != "clean":
            notes = "PCRA incomplete; elevation certificate pending."
        conn.execute(
            """INSERT INTO assets VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                aid,
                name,
                atype,
                city,
                state,
                street,
                lat,
                lon,
                hazard,
                nav,
                rng.randint(3, 10),
                insurance,
                quality,
                notes,
            ),
        )
        conn.execute(
            """INSERT INTO valuations VALUES (?,?,?,?)""",
            (aid, round(rng.uniform(0.045, 0.085), 4), rng.randint(2028, 2035), 0),
        )
        key = f"{street}|{city}|{state}"
        conn.execute(
            "INSERT INTO geocode_cache VALUES (?,?,?,?)",
            (key, lat, lon, "simulated_offline"),
        )
        rows.append(
            {
                "asset_id": aid,
                "name": name,
                "asset_type": atype,
                "city": city,
                "state": state,
                "nav_usd": nav,
                "hazard_bucket": hazard,
                "insurance_status": insurance,
                "data_quality": quality,
                "lat": lat,
                "lon": lon,
            }
        )

    conn.commit()
    conn.close()

    port = cdir / "portfolio"
    port.mkdir(parents=True, exist_ok=True)
    with (port / "asset_register.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    write_json(
        port / "summary.json",
        {
            "client": "Strata Holdings",
            "simulated": True,
            "assets": len(rows),
            "nav_usd": round(total_nav, 2),
            "seed": SEED,
        },
    )

    docs = cdir / "documents"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "stakeholder_messages.md").write_text(
        """# Stakeholder messages — Strata Holdings (SIMULATED)

## IC chair

We will not buy another Gulf Coast industrial without a climate-adjusted exit case. Show me which assets already fail that bar, and which insurance markets are quietly retreating.

## LP letter excerpt

Request: physical risk mapped to **acquisition and exit pricing**, not a standalone hazard score.
""",
        encoding="utf-8",
    )
    (docs / "insurance_program_summary.md").write_text(
        """# Insurance program summary (SIMULATED)

- Master property program with flood sublimits on coastal assets.
- Two Florida assets in market review after non-renewal notices (2025).
- Parametric hurricane cover pilot on Harbor Point only.
""",
        encoding="utf-8",
    )

    briefing = cdir / "briefing"
    briefing.mkdir(parents=True, exist_ok=True)
    (briefing / "engagement.md").write_text(
        """# Engagement briefing — Strata Holdings (SIMULATED)

**Client type:** Diversified real estate and infrastructure fund  
**Book:** ~45 assets; training NAV on the order of a multi-hundred-million slice of a $2.4B-style AUM franchise  
**Question:** Which sites change acquisition, hold, or exit pricing once physical risk and insurance transmission are explicit?

## Success

Mapped assets, hazard scores, standard + bespoke scenarios, IC-ready synthesis, board/IC deck + LP-grade record.
""",
        encoding="utf-8",
    )

    (cdir / "outputs").mkdir(parents=True, exist_ok=True)
    (cdir / "outputs" / ".gitkeep").write_text("", encoding="utf-8")
    (cdir / "AGENTS.md").write_text(
        """# Strata Holdings engagement (SIMULATED)

Decision language: **acquisition / hold / exit pricing**, insurance market transmission, IC narrative.

- DB: `db/portfolio.sqlite`
- Register: `portfolio/asset_register.csv`
- Outputs: `outputs/week-N/`
""",
        encoding="utf-8",
    )

    append_audit(
        TRACK,
        {
            "event": "seed_client",
            "client": "strata",
            "source": "scripts/seed_strata.py",
            "records": len(rows),
            "db": str(db_path.relative_to(ROOT)),
        },
    )
    print(f"Seeded Strata Holdings → {db_path} ({len(rows)} assets)")
    return db_path


if __name__ == "__main__":
    seed()
