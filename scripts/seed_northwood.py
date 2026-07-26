#!/usr/bin/env python3
"""Seed simulated Northwood Capital (industrial + supply chain)."""

from __future__ import annotations

import csv
import random
import sqlite3
from pathlib import Path

from lib_common import ROOT, append_audit, client_dir, write_json

SEED = 20260724
TRACK = "northwood"

SITES = [
    ("Primary Assembly — Midwest", "assembly", "Chicago", "IL", "US", 41.88, -87.63, "flood"),
    ("Injection Molding — Gulf", "component", "Houston", "TX", "US", 29.76, -95.37, "flood_hurricane"),
    ("Electronics Final Test", "test", "Austin", "TX", "US", 30.27, -97.74, "heat_grid"),
    ("West Coast Distribution", "dc", "Los Angeles", "CA", "US", 34.05, -118.24, "wildfire"),
    ("East Coast Distribution", "dc", "Newark", "NJ", "US", 40.74, -74.17, "coastal_flood"),
    ("Specialty Metals Supplier A", "supplier_t1", "Pittsburgh", "PA", "US", 40.44, -79.99, "flood"),
    ("Polymer Resin Supplier B", "supplier_t1", "Baton Rouge", "LA", "US", 30.45, -91.19, "flood_hurricane"),
    ("Battery Cells JV", "supplier_t1", "Reno", "NV", "US", 39.53, -119.81, "drought_wildfire"),
    ("Castings Vendor C", "supplier_t1", "Monterrey", "NL", "MX", 25.69, -100.32, "heat_water"),
    ("Harness Assembly", "supplier_t1", "Guadalajara", "JA", "MX", 20.66, -103.35, "heat"),
    ("PCB Fab Partner", "supplier_t1", "Shenzhen", "GD", "CN", 22.54, 114.06, "flood_typhoon"),
    ("Rare Earth Intermediate", "supplier_t2", "Baotou", "NM", "CN", 40.66, 109.84, "water_transition"),
    ("Logistics Hub EU", "dc", "Rotterdam", "ZH", "NL", 51.92, 4.48, "flood_slr"),
    ("Tooling Shop", "component", "Stuttgart", "BW", "DE", 48.78, 9.18, "flood_heat"),
    ("Packaging Plant", "component", "Memphis", "TN", "US", 35.15, -90.05, "flood"),
]

PRODUCT_LINES = ["Drive Systems", "Thermal Modules", "Control Electronics", "Structural Kits"]


def schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        DROP TABLE IF EXISTS facilities;
        DROP TABLE IF EXISTS suppliers;
        DROP TABLE IF EXISTS product_exposure;
        DROP TABLE IF EXISTS geocode_cache;
        DROP TABLE IF EXISTS meta;

        CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);

        CREATE TABLE facilities (
          id TEXT PRIMARY KEY,
          name TEXT NOT NULL,
          role TEXT NOT NULL,
          city TEXT NOT NULL,
          region TEXT NOT NULL,
          country TEXT NOT NULL,
          address TEXT NOT NULL,
          lat REAL,
          lon REAL,
          hazard_bucket TEXT,
          criticality TEXT NOT NULL,
          revenue_at_risk_usd REAL NOT NULL,
          data_quality TEXT NOT NULL,
          notes TEXT
        );

        CREATE TABLE suppliers (
          id TEXT PRIMARY KEY,
          facility_id TEXT,
          tier INTEGER NOT NULL,
          single_source INTEGER NOT NULL,
          lta_years INTEGER,
          alt_qualified INTEGER NOT NULL,
          FOREIGN KEY (facility_id) REFERENCES facilities(id)
        );

        CREATE TABLE product_exposure (
          id TEXT PRIMARY KEY,
          product_line TEXT NOT NULL,
          facility_id TEXT NOT NULL,
          share_of_cogs REAL NOT NULL,
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


def seed() -> Path:
    rng = random.Random(SEED)
    cdir = client_dir(TRACK)
    db_path = cdir / "db" / "portfolio.sqlite"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    schema(conn)
    conn.execute("INSERT INTO meta VALUES ('client', 'Northwood Capital — SIMULATED')")
    conn.execute("INSERT INTO meta VALUES ('seed', ?)", (str(SEED),))
    conn.execute("INSERT INTO meta VALUES ('revenue_usd', '3200000000')")
    conn.execute("INSERT INTO meta VALUES ('provenance', 'simulated')")

    rows = []
    catalog = list(SITES)
    while len(catalog) < 60:
        base = rng.choice(SITES)
        catalog.append(
            (
                f"{base[0]} Node {len(catalog)+1}",
                base[1],
                base[2],
                base[3],
                base[4],
                base[5] + rng.uniform(-0.1, 0.1),
                base[6] + rng.uniform(-0.1, 0.1),
                base[7],
            )
        )

    for i, s in enumerate(catalog, start=1):
        name, role, city, region, country, lat, lon, hazard = s
        fid = f"NW-FAC-{i:03d}"
        criticality = rng.choices(["critical", "high", "medium", "low"], weights=[0.2, 0.3, 0.35, 0.15])[0]
        rar = round(rng.uniform(5e6, 120e6) * (1.5 if criticality == "critical" else 1.0), 2)
        quality = rng.choices(["clean", "incomplete", "contradictory"], weights=[0.4, 0.4, 0.2])[0]
        street = f"{rng.randint(1, 800)} Industrial Way"
        notes = "Tier-2 visibility limited." if "supplier_t2" in role or quality != "clean" else ""
        conn.execute(
            """INSERT INTO facilities VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                fid,
                name,
                role,
                city,
                region,
                country,
                street,
                lat,
                lon,
                hazard,
                criticality,
                rar,
                quality,
                notes,
            ),
        )
        if role.startswith("supplier"):
            tier = 2 if "t2" in role else 1
            conn.execute(
                """INSERT INTO suppliers VALUES (?,?,?,?,?,?)""",
                (
                    f"NW-SUP-{i:03d}",
                    fid,
                    tier,
                    1 if rng.random() < 0.35 else 0,
                    rng.choice([0, 2, 3, 5]),
                    1 if rng.random() < 0.4 else 0,
                ),
            )
        pl = rng.choice(PRODUCT_LINES)
        conn.execute(
            """INSERT INTO product_exposure VALUES (?,?,?,?)""",
            (f"NW-PX-{i:03d}", pl, fid, round(rng.uniform(0.02, 0.25), 3)),
        )
        key = f"{street}|{city}|{country}"
        conn.execute(
            "INSERT INTO geocode_cache VALUES (?,?,?,?)",
            (key, lat, lon, "simulated_offline"),
        )
        rows.append(
            {
                "facility_id": fid,
                "name": name,
                "role": role,
                "city": city,
                "country": country,
                "criticality": criticality,
                "revenue_at_risk_usd": rar,
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
    with (port / "facility_network.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    write_json(
        port / "summary.json",
        {
            "client": "Northwood Capital",
            "simulated": True,
            "facilities": len(rows),
            "revenue_at_risk_usd": round(sum(r["revenue_at_risk_usd"] for r in rows), 2),
            "seed": SEED,
        },
    )

    docs = cdir / "documents"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "stakeholder_messages.md").write_text(
        """# Stakeholder messages — Northwood Capital (SIMULATED)

## COO

If the Gulf component plant is down 30 days, what breaks in Drive Systems, and what is the cheapest contingency that still works if the insurance market pulls back?

## Procurement

We only see tier-1 cleanly. Label tier-2 gaps. Do not pretend we have multi-tier digital twins.
""",
        encoding="utf-8",
    )
    (docs / "lta_excerpt_supplier_b.md").write_text(
        """# LTA excerpt — Polymer Resin Supplier B (SIMULATED)

Term: 5 years remaining. Force majeure includes named storms. No dual-source clause. Price reset annual.
""",
        encoding="utf-8",
    )

    briefing = cdir / "briefing"
    briefing.mkdir(parents=True, exist_ok=True)
    (briefing / "engagement.md").write_text(
        """# Engagement briefing — Northwood Capital (SIMULATED)

**Client type:** Mid-cap industrial with climate-exposed supply chain  
**Book:** ~60 facilities / supplier nodes across US, MX, EU, CN  
**Question:** Where do physical shocks and institutional responses (insurance, logistics, input pricing) force contingency spend or dual-source decisions?

## Success

Mapped network, hazard exposure, scenarios that combine site damage with input squeezes, synthesis with contingency ROI, exec deck + assurance-ready record.
""",
        encoding="utf-8",
    )

    (cdir / "outputs").mkdir(parents=True, exist_ok=True)
    (cdir / "outputs" / ".gitkeep").write_text("", encoding="utf-8")
    (cdir / "AGENTS.md").write_text(
        """# Northwood Capital engagement (SIMULATED)

Decision language: **contingency, dual-source, inventory, input pricing, revenue-at-risk**.

- DB: `db/portfolio.sqlite`
- Network: `portfolio/facility_network.csv`
- Outputs: `outputs/week-N/`
""",
        encoding="utf-8",
    )

    append_audit(
        TRACK,
        {
            "event": "seed_client",
            "client": "northwood",
            "source": "scripts/seed_northwood.py",
            "records": len(rows),
            "db": str(db_path.relative_to(ROOT)),
        },
    )
    print(f"Seeded Northwood Capital → {db_path} ({len(rows)} facilities)")
    return db_path


if __name__ == "__main__":
    seed()
