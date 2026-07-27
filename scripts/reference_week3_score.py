#!/usr/bin/env python3
"""Reference: join sample hazard scores to geocoded entities for active track."""

from __future__ import annotations

import csv
import math
import sqlite3

from lib_common import ROOT, active_track, append_audit, client_dir

CITY_TO_COUNTY = {
    "Kerrville": "Kerr",
    "Abilene": "Taylor",
    "Midland": "Midland",
    "Temple": "Bell",
    "Taylor County": "Taylor",
    # Colorado system nodes use state-level sample rows
    "AZ": "Mohave-sim",
    "UT": "Kane-sim",
    "NV": "Clark-sim",
    "CA": "Imperial-sim",
    "CO": "Eagle-sim",
}


def scores_from_bucket(bucket: str | None) -> dict[str, float]:
    b = (bucket or "").lower()
    flood = 7.5 if "flood" in b or "flash" in b else 2.0
    wildfire = 5.0 if "wildfire" in b else 1.5
    heat = 8.0 if "heat" in b or "drought" in b or "grid" in b else 3.0
    hurricane = 1.0
    drought = 8.5 if "drought" in b else 3.0
    # fold drought into heat channel for sample grid compatibility
    heat = max(heat, drought * 0.9)
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
    out: list[dict] = []
    if track == "colorado":
        for r in conn.execute(
            "SELECT id, name, state, lat, lon, hazard_bucket, storage_kaf, criticality FROM facilities"
        ):
            dollars = float(r["storage_kaf"] or 0) * 1_000_000  # synthetic $ proxy for ranking
            if r["criticality"] == "critical":
                dollars *= 1.5
            out.append(
                {
                    "entity_id": r["id"],
                    "city": r["state"],
                    "lat": r["lat"],
                    "lon": r["lon"],
                    "dollars": dollars,
                    "hazard_bucket": r["hazard_bucket"],
                }
            )
    elif track == "kerrville":
        for r in conn.execute(
            """SELECT f.id, f.city, f.lat, f.lon, f.hazard_bucket, e.replacement_usd
               FROM facilities f JOIN exposures e ON e.facility_id=f.id"""
        ):
            out.append(
                {
                    "entity_id": r["id"],
                    "city": r["city"],
                    "lat": r["lat"],
                    "lon": r["lon"],
                    "dollars": float(r["replacement_usd"]),
                    "hazard_bucket": r["hazard_bucket"],
                }
            )
    else:
        for r in conn.execute(
            "SELECT id, city, lat, lon, hazard_bucket, mw_nameplate, water_mgy FROM facilities"
        ):
            dollars = float(r["mw_nameplate"] or 0) * 500_000 + float(r["water_mgy"] or 0) * 10_000
            out.append(
                {
                    "entity_id": r["id"],
                    "city": r["city"],
                    "lat": r["lat"],
                    "lon": r["lon"],
                    "dollars": max(dollars, 100_000),
                    "hazard_bucket": r["hazard_bucket"],
                }
            )
    conn.close()
    return out


def main() -> None:
    track = active_track()
    hazard = load_hazard()
    rows_out = []
    unmatched = 0
    for e in entities(track):
        county = CITY_TO_COUNTY.get(e["city"])
        h = hazard.get(county or "", {})
        score_source = "firm_sample_grid"
        if not h:
            unmatched += 1
            fb = scores_from_bucket(e.get("hazard_bucket"))
            flood, wildfire, heat, hurricane = (
                fb["flood_score"],
                fb["wildfire_score"],
                fb["heat_score"],
                fb["hurricane_score"],
            )
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
