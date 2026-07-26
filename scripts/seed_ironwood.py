#!/usr/bin/env python3
"""Seed simulated Ironwood Bank portfolio (commercial credit book)."""

from __future__ import annotations

import csv
import random
import sqlite3
from pathlib import Path

from lib_common import ROOT, append_audit, client_dir, write_json

SEED = 20260724
TRACK = "ironwood"

# US cities with coarse lat/lon for offline geocode
CITIES = [
    ("Houston", "TX", 29.76, -95.37, "high_flood"),
    ("Miami", "FL", 25.76, -80.19, "high_flood_hurricane"),
    ("New Orleans", "LA", 29.95, -90.07, "high_flood"),
    ("Tampa", "FL", 27.95, -82.46, "hurricane"),
    ("Charleston", "SC", 32.78, -79.93, "hurricane"),
    ("Norfolk", "VA", 36.85, -76.29, "flood"),
    ("New York", "NY", 40.71, -74.01, "coastal"),
    ("Boston", "MA", 42.36, -71.06, "coastal"),
    ("Chicago", "IL", 41.88, -87.63, "inland"),
    ("Dallas", "TX", 32.78, -96.80, "heat_hail"),
    ("Phoenix", "AZ", 33.45, -112.07, "heat_drought"),
    ("Denver", "CO", 39.74, -104.99, "wildfire_hail"),
    ("Sacramento", "CA", 38.58, -121.49, "wildfire_flood"),
    ("Los Angeles", "CA", 34.05, -118.24, "wildfire_quake"),
    ("Seattle", "WA", 47.61, -122.33, "flood"),
    ("Atlanta", "GA", 33.75, -84.39, "inland"),
    ("Memphis", "TN", 35.15, -90.05, "flood"),
    ("Kansas City", "MO", 39.10, -94.58, "tornado_flood"),
    ("Minneapolis", "MN", 44.98, -93.27, "inland"),
    ("Portland", "OR", 45.52, -122.68, "wildfire"),
]

SECTORS = [
    ("Commercial Real Estate", "CRE", "office_retail_multifamily"),
    ("Manufacturing", "MFG", "light_heavy_industrial"),
    ("Energy Midstream", "ENR", "pipelines_terminals"),
    ("Agriculture", "AGR", "farms_processing"),
    ("Logistics", "LOG", "warehouses_ports"),
    ("Municipal / Public", "MUN", "utilities_infra"),
    ("Datacenter / Tech RE", "DC", "colocation_campus"),
    ("Hospitality", "HOS", "hotels_resorts"),
    ("Healthcare Facilities", "HLT", "hospitals_clinics"),
    ("Retail Trade", "RTL", "stores_distribution"),
]

DATA_QUALITY = ["clean", "incomplete", "contradictory"]


def schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        DROP TABLE IF EXISTS facilities;
        DROP TABLE IF EXISTS counterparties;
        DROP TABLE IF EXISTS exposures;
        DROP TABLE IF EXISTS geocode_cache;
        DROP TABLE IF EXISTS meta;

        CREATE TABLE meta (
          key TEXT PRIMARY KEY,
          value TEXT NOT NULL
        );

        CREATE TABLE counterparties (
          id TEXT PRIMARY KEY,
          name TEXT NOT NULL,
          sector TEXT NOT NULL,
          sector_code TEXT NOT NULL,
          activity_hint TEXT NOT NULL,
          state TEXT NOT NULL,
          city TEXT NOT NULL,
          data_quality TEXT NOT NULL,
          outstanding_usd REAL NOT NULL,
          risk_rating TEXT NOT NULL,
          notes TEXT
        );

        CREATE TABLE facilities (
          id TEXT PRIMARY KEY,
          counterparty_id TEXT NOT NULL,
          address TEXT NOT NULL,
          city TEXT NOT NULL,
          state TEXT NOT NULL,
          postal TEXT NOT NULL,
          lat REAL,
          lon REAL,
          hazard_bucket TEXT,
          facility_type TEXT NOT NULL,
          insured INTEGER NOT NULL DEFAULT 1,
          FOREIGN KEY (counterparty_id) REFERENCES counterparties(id)
        );

        CREATE TABLE exposures (
          id TEXT PRIMARY KEY,
          counterparty_id TEXT NOT NULL,
          facility_id TEXT,
          product TEXT NOT NULL,
          commitment_usd REAL NOT NULL,
          drawn_usd REAL NOT NULL,
          maturity_year INTEGER NOT NULL,
          collateral_type TEXT,
          FOREIGN KEY (counterparty_id) REFERENCES counterparties(id)
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
    conn.execute(
        "INSERT INTO meta(key, value) VALUES (?, ?)",
        ("client", "Ironwood Bank — SIMULATED"),
    )
    conn.execute(
        "INSERT INTO meta(key, value) VALUES (?, ?)",
        ("seed", str(SEED)),
    )
    conn.execute(
        "INSERT INTO meta(key, value) VALUES (?, ?)",
        ("provenance", "simulated"),
    )

    portfolio_rows = []
    n = 100
    for i in range(1, n + 1):
        city, state, lat, lon, hazard = rng.choice(CITIES)
        sector, code, activity = rng.choice(SECTORS)
        # jitter lat/lon slightly
        jlat = lat + rng.uniform(-0.08, 0.08)
        jlon = lon + rng.uniform(-0.08, 0.08)
        quality = rng.choices(DATA_QUALITY, weights=[0.45, 0.35, 0.20])[0]
        outstanding = round(rng.uniform(2.5e6, 85e6), 2)
        rating = rng.choice(["BBB", "BB", "B", "A-", "BBB+", "BB+"])
        cid = f"IW-CP-{i:03d}"
        name = f"{sector.split()[0]} Holdings {i:03d} LLC"
        if sector == "Municipal / Public":
            name = f"City of {city} Utility Authority {i:03d}"
        notes = ""
        if quality == "incomplete":
            notes = "Missing building-level occupancy; questionnaire half-complete."
        elif quality == "contradictory":
            notes = "Insurance schedule conflicts with facility list; flood zone disputed."

        conn.execute(
            """INSERT INTO counterparties VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            (
                cid,
                name,
                sector,
                code,
                activity,
                state,
                city,
                quality,
                outstanding,
                rating,
                notes,
            ),
        )

        fid = f"IW-FAC-{i:03d}"
        street_no = rng.randint(100, 9900)
        address = f"{street_no} Main Industrial Blvd"
        postal = f"{rng.randint(10000, 99999)}"
        ftype = activity.split("_")[0]
        conn.execute(
            """INSERT INTO facilities VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            (
                fid,
                cid,
                address,
                city,
                state,
                postal,
                jlat,
                jlon,
                hazard,
                ftype,
                1 if rng.random() > 0.15 else 0,
            ),
        )
        # prefill geocode cache (offline)
        addr_key = f"{address}|{city}|{state}|{postal}"
        conn.execute(
            "INSERT OR REPLACE INTO geocode_cache VALUES (?,?,?,?)",
            (addr_key, jlat, jlon, "simulated_offline"),
        )

        eid = f"IW-EXP-{i:03d}"
        product = rng.choice(["Term Loan", "Revolver", "CRE Mortgage", "Construction"])
        commitment = round(outstanding * rng.uniform(1.0, 1.25), 2)
        drawn = outstanding
        maturity = rng.randint(2027, 2034)
        collateral = rng.choice(["RE", "All-assets", "Equipment", "Unsecured", "RE+Guarantor"])
        conn.execute(
            """INSERT INTO exposures VALUES (?,?,?,?,?,?,?,?)""",
            (eid, cid, fid, product, commitment, drawn, maturity, collateral),
        )

        portfolio_rows.append(
            {
                "counterparty_id": cid,
                "name": name,
                "sector": sector,
                "city": city,
                "state": state,
                "outstanding_usd": outstanding,
                "data_quality": quality,
                "lat": jlat,
                "lon": jlon,
                "hazard_bucket": hazard,
            }
        )

    conn.commit()
    conn.close()

    # CSV export for easy reading
    port_dir = cdir / "portfolio"
    port_dir.mkdir(parents=True, exist_ok=True)
    csv_path = port_dir / "loan_book.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(portfolio_rows[0].keys()))
        w.writeheader()
        w.writerows(portfolio_rows)

    write_json(
        cdir / "portfolio" / "summary.json",
        {
            "client": "Ironwood Bank",
            "simulated": True,
            "counterparties": n,
            "total_outstanding_usd": round(sum(r["outstanding_usd"] for r in portfolio_rows), 2),
            "seed": SEED,
        },
    )

    # Messy documents
    docs = cdir / "documents"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "stakeholder_messages.md").write_text(
        """# Stakeholder messages — Ironwood Bank (SIMULATED)

## CRO → Engagement lead (2026-06-12)

Board wants a clear answer before Q4: which names force a pricing conversation, and can we show the parent (Frankfurt) a clean trail for the ECB climate stress dialogue?

Regulator window: internal dry-run for climate risk disclosure by **week of Oct 13**. Do not over-claim data quality — half the CRE book questionnaires are incomplete.

## Board chair note (2026-06-18)

We do not need a science lecture. We need: concentration, break points, and what changes in pricing or limits. Keep NGFS-style standard scenarios for the record; give us the 2–3 stresses that actually matter for *this* book.

## Credit risk — contested file (IW-CP-014)

Insurance schedule says flood coverage full replacement. Facilities list shows a second warehouse not on the schedule. Data quality flag: contradictory.
""",
        encoding="utf-8",
    )

    (docs / "credit_file_sample_IW-CP-014.md").write_text(
        """# Credit file excerpt — IW-CP-014 (SIMULATED)

**Name:** Manufacturing Holdings 014 LLC  
**Sector:** Manufacturing  
**City/State:** Houston, TX  
**Outstanding:** see loan_book.csv  

## Questionnaire (partial)

- Primary site elevation: *blank*
- Flood insurance: "Yes — full" (attached schedule dated 2023)
- Business continuity plan: "In progress"
- Supplier concentration: top 3 suppliers = 62% of COGS (self-reported)

## Underwriter note

Second facility on industrial spur may be uninsured. Borrower disputes flood zone. Recommend site visit — not yet scheduled.
""",
        encoding="utf-8",
    )

    (docs / "regulatory_deadlines.md").write_text(
        """# Regulatory & governance deadlines — Ironwood (SIMULATED)

| Milestone | Date | Audience |
|-----------|------|----------|
| Internal climate risk dry-run pack | 2026-10-13 week | CRO / Risk committee |
| Board risk deep-dive | 2026-11-05 | Board |
| Parent group climate data call | 2026-11-20 | Frankfurt risk |
| Public disclosure narrative draft | 2026-12-15 | Legal + Sustainability |

Assumptions for the engagement: deliver board judgment and a framework-aligned record that can feed the dry-run pack.
""",
        encoding="utf-8",
    )

    briefing = cdir / "briefing"
    briefing.mkdir(parents=True, exist_ok=True)
    (briefing / "engagement.md").write_text(
        """# Engagement briefing — Ironwood Bank (SIMULATED)

**Client type:** U.S. commercial bank, subsidiary of a Frankfurt-based financial group  
**Book:** ~100 counterparties (training slice of a larger book)  
**Question you are paid to answer:** Where does physical climate risk force credit pricing, capital, or limit action — and can the board and regulator trust the trail?

## Context

- Tiered data quality: clean / incomplete / contradictory questionnaires.
- Parent group expects ECB-aware discipline: standard scenarios for the record, portfolio-specific stress for decisions.
- Sustainability priority has dropped; **CFO and CRO** own the questions: should we act, when, how?

## Success looks like

1. Week 1 framing & delivery plan signed conceptually by the engagement lead.
2. Mapped book + hypothesis register.
3. Hazard dataset with audit log.
4. Standard + bespoke scenario results.
5. Portfolio synthesis with pricing implications.
6. Board presentation (judgment) + regulatory-style submission (record).

## Guardrails

- All data is **simulated**.
- Computed numbers from code; judged numbers labeled.
- Gaps documented, not invented.
""",
        encoding="utf-8",
    )

    (cdir / "outputs").mkdir(parents=True, exist_ok=True)
    (cdir / "outputs" / ".gitkeep").write_text("", encoding="utf-8")
    (cdir / "AGENTS.md").write_text(
        """# Ironwood Bank engagement (SIMULATED)

You are supporting a climate risk assessment for **Ironwood Bank**.

- Portfolio DB: `db/portfolio.sqlite`
- Loan book CSV: `portfolio/loan_book.csv`
- Documents: `documents/`
- Outputs: `outputs/week-N/`

Follow repo root `AGENTS.md` epistemic rules. Decision language: **credit pricing, capital, limits, board + regulator**.
""",
        encoding="utf-8",
    )

    append_audit(
        TRACK,
        {
            "event": "seed_client",
            "client": "ironwood",
            "source": "scripts/seed_ironwood.py",
            "records": n,
            "db": str(db_path.relative_to(ROOT)),
        },
    )
    print(f"Seeded Ironwood Bank → {db_path} ({n} counterparties)")
    return db_path


if __name__ == "__main__":
    seed()
