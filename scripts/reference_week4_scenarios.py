#!/usr/bin/env python3
"""Reference: apply STD scenario screens to week-3 entity hazard scores."""

from __future__ import annotations

import csv
from pathlib import Path

from lib_common import active_track, append_audit, client_dir

SEVERITY_RANK = {"S0": 0, "S1": 1, "S2": 2, "S3": 3}


def severity_for(std: str, primary: str, score: float) -> str:
    if std == "STD-01":
        if primary in ("flood", "hurricane") and score >= 8:
            return "S2"
        if primary in ("flood", "hurricane") and score >= 5:
            return "S1"
        return "S0"
    if std == "STD-02":
        if primary == "wildfire" and score >= 7:
            return "S2"
        if primary == "wildfire" and score >= 4:
            return "S1"
        return "S0"
    if std == "STD-03":
        if primary == "heat" and score >= 8:
            return "S2"
        if primary == "heat" and score >= 5:
            return "S1"
        return "S0"
    return "S0"


def damage_fraction(sev: str) -> float:
    return {"S0": 0.01, "S1": 0.10, "S2": 0.30, "S3": 0.65}[sev]


def main() -> None:
    track = active_track()
    scores_path = client_dir(track) / "outputs" / "week-3" / "entity_hazard_scores.csv"
    if not scores_path.is_file():
        raise SystemExit(f"Missing {scores_path}; run reference_week3_score.py first")

    with scores_path.open(encoding="utf-8") as f:
        entities = list(csv.DictReader(f))

    out_rows = []
    for std in ("STD-01", "STD-02", "STD-03"):
        for e in entities:
            sev = severity_for(std, e["primary_hazard"], float(e["primary_score"]))
            dollars = float(e["dollars"])
            loss = round(dollars * damage_fraction(sev), 2)
            out_rows.append(
                {
                    "scenario": std,
                    "entity_id": e["entity_id"],
                    "severity": sev,
                    "dollars": dollars,
                    "indicative_loss_usd": loss,
                    "kind": "computed_with_anchor_midpoints",
                }
            )

    out_dir = client_dir(track) / "outputs" / "week-4"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "standard_scenario_results.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
        w.writeheader()
        w.writerows(out_rows)

    # Summary per scenario (not additive across scenarios)
    lines = ["# Standard scenario summary", ""]
    for std in ("STD-01", "STD-02", "STD-03"):
        subset = [r for r in out_rows if r["scenario"] == std and r["severity"] in ("S2", "S3")]
        total = sum(r["indicative_loss_usd"] for r in subset)
        lines.append(f"## {std}")
        lines.append(f"- Entities at S2+: {len(subset)}")
        lines.append(f"- Indicative loss (anchor midpoints, **computed**): ${total:,.0f}")
        lines.append("")
    lines.append("Do not sum losses across scenarios.")
    (out_dir / "standard_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    append_audit(
        track,
        {
            "event": "standard_scenarios",
            "source": "firm/scenario-cards + anchors",
            "records": len(out_rows),
            "script": "scripts/reference_week4_scenarios.py",
        },
    )
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
