#!/usr/bin/env python3
"""Seed simulated Horizon Grid LLC — Texas data center EIS engagement."""

from __future__ import annotations

import csv
import random
import sqlite3

from lib_common import ROOT, append_audit, client_dir, write_json

SEED = 20260726
TRACK = "datacenter"

# Proposed / alternative Texas data-center campus elements (SIMULATED)
SITES = [
    ("Primary Campus Pad A", "building_pad", "Abilene", "TX", 32.45, -99.73, "heat_drought_grid", 1.5),
    ("Primary Campus Pad B", "building_pad", "Abilene", "TX", 32.46, -99.72, "heat_grid", 1.4),
    ("Alt Site — Midland Spur", "building_pad", "Midland", "TX", 31.99, -102.08, "heat_drought", 1.2),
    ("Alt Site — Temple Corridor", "building_pad", "Temple", "TX", 31.10, -97.34, "heat_flood", 1.0),
    ("Water Supply Option — Municipal", "water", "Abilene", "TX", 32.45, -99.75, "drought", 1.3),
    ("Water Supply Option — Aquifer", "water", "Abilene", "TX", 32.40, -99.80, "drought", 1.1),
    ("Reclaimed Water Lateral", "water", "Abilene", "TX", 32.48, -99.70, "drought_heat", 0.9),
    ("230kV Interconnect Point", "power", "Abilene", "TX", 32.50, -99.68, "grid_heat", 1.4),
    ("Backup Gas Generation Parcel", "power", "Abilene", "TX", 32.44, -99.71, "heat", 0.8),
    ("Fiber Hut East", "telecom", "Abilene", "TX", 32.47, -99.69, "heat", 0.5),
    ("Construction Staging Yard", "construction", "Abilene", "TX", 32.43, -99.74, "heat_flood", 0.6),
    ("Community Receptor — School", "receptor", "Abilene", "TX", 32.45, -99.76, "heat", 0.7),
    ("Community Receptor — Neighborhood", "receptor", "Abilene", "TX", 32.46, -99.77, "heat", 0.7),
    ("Wetland / Playa Buffer", "environment", "Abilene", "TX", 32.42, -99.78, "flood_drought", 0.9),
    ("Transmission Corridor Segment 1", "transmission", "Taylor County", "TX", 32.55, -99.60, "heat_grid", 1.0),
    ("Transmission Corridor Segment 2", "transmission", "Taylor County", "TX", 32.60, -99.55, "heat", 0.9),
]


def schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        DROP TABLE IF EXISTS facilities;
        DROP TABLE IF EXISTS impact_topics;
        DROP TABLE IF EXISTS geocode_cache;
        DROP TABLE IF EXISTS meta;

        CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);

        CREATE TABLE facilities (
          id TEXT PRIMARY KEY,
          name TEXT NOT NULL,
          element_type TEXT NOT NULL,
          city TEXT NOT NULL,
          state TEXT NOT NULL,
          address TEXT NOT NULL,
          lat REAL,
          lon REAL,
          hazard_bucket TEXT,
          eis_alternative TEXT NOT NULL,
          mw_nameplate REAL,
          water_mgy REAL,
          data_quality TEXT NOT NULL,
          notes TEXT
        );

        CREATE TABLE impact_topics (
          id TEXT PRIMARY KEY,
          facility_id TEXT NOT NULL,
          topic TEXT NOT NULL,
          significance_hint TEXT NOT NULL,
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
    conn.execute("INSERT INTO meta VALUES ('client', 'Horizon Grid LLC — SIMULATED')")
    conn.execute("INSERT INTO meta VALUES ('seed', ?)", (str(SEED),))
    conn.execute("INSERT INTO meta VALUES ('project', 'Texas hyperscale campus EIS training case')")
    conn.execute("INSERT INTO meta VALUES ('provenance', 'simulated')")

    catalog = list(SITES)
    while len(catalog) < 55:
        base = rng.choice(SITES)
        catalog.append(
            (
                f"{base[0]} Variant {len(catalog)+1}",
                base[1],
                base[2],
                base[3],
                base[4] + rng.uniform(-0.08, 0.08),
                base[5] + rng.uniform(-0.08, 0.08),
                base[6],
                base[7] * rng.uniform(0.6, 1.15),
            )
        )

    rows = []
    for i, s in enumerate(catalog, start=1):
        name, etype, city, state, lat, lon, hazard, w = s
        fid = f"DC-ELM-{i:03d}"
        alt = rng.choice(["Proposed Action", "Alt A — Midland", "Alt B — Temple", "No Action"])
        if "Midland" in name:
            alt = "Alt A — Midland"
        if "Temple" in name:
            alt = "Alt B — Temple"
        mw = round(rng.uniform(50, 300) * w, 1) if etype in ("building_pad", "power") else 0.0
        water = round(rng.uniform(50, 800) * w, 1) if etype in ("building_pad", "water") else 0.0
        quality = rng.choices(["clean", "incomplete", "contradictory"], weights=[0.45, 0.4, 0.15])[0]
        street = f"EIS Element {i} / County Rd {i}"
        notes = "Water availability letter pending." if quality != "clean" and etype == "water" else ""
        conn.execute(
            """INSERT INTO facilities VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                fid,
                name,
                etype,
                city,
                state,
                street,
                lat,
                lon,
                hazard,
                alt,
                mw,
                water,
                quality,
                notes,
            ),
        )
        topics = rng.sample(
            ["water_supply", "energy_grid", "air_quality", "noise", "land_use", "socioeconomic", "biological", "cultural"],
            k=rng.randint(2, 4),
        )
        for t in topics:
            conn.execute(
                """INSERT INTO impact_topics VALUES (?,?,?,?)""",
                (
                    f"DC-IMP-{i:03d}-{t[:4]}",
                    fid,
                    t,
                    rng.choice(["low", "moderate", "high", "unknown"]),
                ),
            )
        key = f"{street}|{city}|{state}"
        conn.execute(
            "INSERT INTO geocode_cache VALUES (?,?,?,?)",
            (key, lat, lon, "simulated_offline"),
        )
        rows.append(
            {
                "facility_id": fid,
                "name": name,
                "element_type": etype,
                "city": city,
                "eis_alternative": alt,
                "mw_nameplate": mw,
                "water_mgy": water,
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
    with (port / "eis_elements.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    write_json(
        port / "summary.json",
        {
            "client": "Horizon Grid LLC",
            "simulated": True,
            "elements": len(rows),
            "seed": SEED,
            "theme": "Texas data center environmental impact statement",
        },
    )

    docs = cdir / "documents"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "stakeholder_messages.md").write_text(
        """# Stakeholder messages — Horizon Grid LLC (SIMULATED)

## Project director

EIS schedule is tight. We need climate and physical-risk inputs that map to alternatives (Proposed Action vs Midland vs Temple vs No Action): water, heat/grid stress, and flood on staging parcels.

## Environmental counsel

Label every figure. Agencies will ask where numbers came from. No silent invention of TCEQ or ERCOT data — use firm sample grids and documented assumptions.

## Community liaison

Receptor nodes (school, neighborhood) need plain-language impact ranges under heat and construction scenarios.
""",
        encoding="utf-8",
    )
    (docs / "purpose_and_need.md").write_text(
        """# Purpose and need excerpt (SIMULATED)

Horizon Grid proposes a hyperscale compute campus in Texas to meet contracted cloud demand. The EIS must compare site and water/power alternatives, including No Action.

Training note: project description is fictional for coursework.
""",
        encoding="utf-8",
    )

    briefing = cdir / "briefing"
    briefing.mkdir(parents=True, exist_ok=True)
    (briefing / "engagement.md").write_text(
        """# Engagement briefing — Horizon Grid Texas data center EIS (SIMULATED)

**Client type:** Private developer preparing an environmental impact statement for a Texas data center campus  
**Book:** ~55 EIS elements (pads, water options, power, transmission, receptors)  
**Question:** How do heat, drought, grid stress, and flood change the significance of impacts across alternatives — and what should the EIS and project board emphasize?

## Decision language

Alternatives analysis, water supply reliability, grid interconnection risk, receptor impacts, mitigation commitments.

## Success

Mapped elements by alternative, hazard scores, scenarios that stress water/power/flood, synthesis feeding EIS sections, board pack + administrative record-style appendix.

## Guardrails

All campus elements are **simulated**. Not a real filing. Not affiliated with any utility or agency.
""",
        encoding="utf-8",
    )

    (cdir / "outputs").mkdir(parents=True, exist_ok=True)
    (cdir / "outputs" / ".gitkeep").write_text("", encoding="utf-8")
    (cdir / "AGENTS.md").write_text(
        """# Horizon Grid Texas data center EIS (SIMULATED)

**EIS support** for a fictional Texas hyperscale campus.

Decision language: **alternatives, water, power/grid, receptors, mitigation**.

- DB: `db/portfolio.sqlite`
- Elements: `portfolio/eis_elements.csv`
- Outputs: `outputs/week-N/`
""",
        encoding="utf-8",
    )

    append_audit(
        TRACK,
        {
            "event": "seed_client",
            "client": "datacenter",
            "source": "scripts/seed_datacenter.py",
            "records": len(rows),
            "db": str(db_path.relative_to(ROOT)),
        },
    )
    print(f"Seeded Horizon Grid EIS → {db_path} ({len(rows)} elements)")


if __name__ == "__main__":
    seed()
