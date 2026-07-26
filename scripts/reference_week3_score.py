#!/usr/bin/env python3
"""Reference: join sample hazard scores to geocoded entities for active track."""

from __future__ import annotations

import csv
import sqlite3
from pathlib import Path

from lib_common import ROOT, active_track, append_audit, client_dir

# City → approximate sample county row (training shortcut)
CITY_TO_COUNTY = {
    "Houston": "Harris",
    "Miami": "Miami-Dade",
    "New Orleans": "Orleans",
    "Tampa": "Hillsborough",
    "Charleston": "Charleston",
    "Norfolk": "Norfolk city",
    "New York": "New York",
    "Boston": "Suffolk",
    "Chicago": "Cook",
    "Dallas": "Dallas",
    "Phoenix": "Maricopa",
    "Denver": "Denver",
    "Sacramento": "Sacramento",
    "Los Angeles": "Los Angeles",
    "Seattle": "King",
    "Atlanta": "Fulton",
    "Memphis": "Shelby",
    "Kansas City": "Jackson",
    "Minneapolis": "Hennepin",
    "Portland": "Multnomah",
    "Key West": "Monroe",
    "Ashburn": "Loudoun",
    "Austin": "Travis",
    "Newark": "Essex",
    "Pittsburgh": "Allegheny",
    "Baton Rouge": "East Baton Rouge",
    "Reno": "Washoe",
    "Monterrey": "Monterrey-sim",
    "Guadalajara": "Guadalajara-sim",
    "Shenzhen": "Shenzhen-sim",
    "Baotou": "Baotou-sim",
    "Rotterdam": "Rotterdam-sim",
    "Stuttgart": "Stuttgart-sim",
}


def scores_from_bucket(bucket: str | None) -> dict[str, float]:
    """Fallback when city is not in the sample grid (documented gap path)."""
    b = (bucket or "").lower()
    flood = 7.0 if "flood" in b or "slr" in b or "coastal" in b else 2.0
    wildfire = 7.0 if "wildfire" in b else 1.0
    heat = 7.5 if "heat" in b or "drought" in b or "grid" in b else 3.0
    hurricane = 8.0 if "hurricane" in b or "typhoon" in b else 1.0
    return {
        "flood_score": flood,
        "wildfire_score": wildfire,
        "heat_score": heat,
        "hurricane_score": hurricane,
    }


def load_hazard() -> dict[str, dict]:
    path = ROOT / "firm" / "sample-hazard" / "county_hazard_scores.csv"
    by_name: dict[str, dict] = {}
    with path.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            by_name[row["county_name"]] = row
    return by_name


def entities(track: str) -> list[dict]:
    db = client_dir(track) / "db" / "portfolio.sqlite"
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    if track == "ironwood":
        rows = conn.execute(
            "SELECT id, city, state, lat, lon, hazard_bucket FROM facilities"
        ).fetchall()
        money = {
            r["counterparty_id"]: r["outstanding_usd"]
            for r in conn.execute(
                "SELECT id AS counterparty_id, outstanding_usd FROM counterparties"
            )
        }
        fac_cp = {
            r["id"]: r["counterparty_id"]
            for r in conn.execute("SELECT id, counterparty_id FROM facilities")
        }
        out = []
        for r in rows:
            out.append(
                {
                    "entity_id": r["id"],
                    "city": r["city"],
                    "lat": r["lat"],
                    "lon": r["lon"],
                    "dollars": money.get(fac_cp[r["id"]], 0),
                    "hazard_bucket": r["hazard_bucket"],
                }
            )
        conn.close()
        return out
    if track == "strata":
        rows = conn.execute(
            "SELECT id, city, lat, lon, nav_usd, hazard_bucket FROM assets"
        ).fetchall()
        conn.close()
        return [
            {
                "entity_id": r["id"],
                "city": r["city"],
                "lat": r["lat"],
                "lon": r["lon"],
                "dollars": r["nav_usd"],
                "hazard_bucket": r["hazard_bucket"],
            }
            for r in rows
        ]
    rows = conn.execute(
        "SELECT id, city, lat, lon, revenue_at_risk_usd, hazard_bucket FROM facilities"
    ).fetchall()
    conn.close()
    return [
        {
            "entity_id": r["id"],
            "city": r["city"],
            "lat": r["lat"],
            "lon": r["lon"],
            "dollars": r["revenue_at_risk_usd"],
            "hazard_bucket": r["hazard_bucket"],
        }
        for r in rows
    ]


def main() -> None:
    import math

    track = active_track()
    hazard = load_hazard()
    rows_out = []
    unmatched = 0
    for e in entities(track):
        county = CITY_TO_COUNTY.get(e["city"])
        h = hazard.get(county or "", {})
        score_source = "firm_sample_grid"
        if not h:
            # Training fallback: derive coarse scores from seeded hazard_bucket.
            # Document as gap-path so students practice labeling thin data.
            unmatched += 1
            fb = scores_from_bucket(e.get("hazard_bucket"))
            flood = fb["flood_score"]
            wildfire = fb["wildfire_score"]
            heat = fb["heat_score"]
            hurricane = fb["hurricane_score"]
            score_source = "hazard_bucket_fallback"
        else:
            flood = float(h["flood_score"])
            wildfire = float(h["wildfire_score"])
            heat = float(h["heat_score"])
            hurricane = float(h["hurricane_score"])
        primary = max(
            ("flood", flood),
            ("wildfire", wildfire),
            ("heat", heat),
            ("hurricane", hurricane),
            key=lambda x: x[1],
        )
        idx = (primary[1] / 10.0) * math.log10(1 + float(e["dollars"]))
        rows_out.append(
            {
                "entity_id": e["entity_id"],
                "city": e["city"],
                "primary_hazard": primary[0],
                "primary_score": primary[1],
                "flood_score": flood,
                "wildfire_score": wildfire,
                "heat_score": heat,
                "hurricane_score": hurricane,
                "dollars": e["dollars"],
                "exposure_index": round(idx, 4),
                "score_source": score_source,
            }
        )

    out_dir = client_dir(track) / "outputs" / "week-3"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "entity_hazard_scores.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows_out[0].keys()))
        w.writeheader()
        w.writerows(rows_out)

    append_audit(
        track,
        {
            "event": "hazard_score",
            "source": "firm_sample_grid",
            "version": "v1",
            "records": len(rows_out),
            "unmatched": unmatched,
            "script": "scripts/reference_week3_score.py",
        },
    )
    print(f"Wrote {path} ({len(rows_out)} rows, unmatched={unmatched})")


if __name__ == "__main__":
    main()
