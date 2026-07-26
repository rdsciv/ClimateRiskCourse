#!/usr/bin/env python3
"""Reference: book overview for active track (week 1)."""

from __future__ import annotations

import sqlite3
from collections import Counter

from lib_common import active_track, append_audit, client_dir


def main() -> None:
    track = active_track()
    db = client_dir(track) / "db" / "portfolio.sqlite"
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    lines = [f"# Book overview — {track}", f"DB: {db}", ""]

    if track == "ironwood":
        n = conn.execute("SELECT COUNT(*) c FROM counterparties").fetchone()["c"]
        total = conn.execute("SELECT SUM(outstanding_usd) s FROM counterparties").fetchone()["s"]
        lines += [f"Counterparties: {n}", f"Total outstanding USD: {total:,.2f}", "", "## By sector"]
        for r in conn.execute(
            "SELECT sector, COUNT(*) n, SUM(outstanding_usd) s FROM counterparties GROUP BY sector ORDER BY s DESC"
        ):
            lines.append(f"- {r['sector']}: n={r['n']}  ${r['s']:,.0f}")
        lines += ["", "## Data quality"]
        for r in conn.execute(
            "SELECT data_quality, COUNT(*) n FROM counterparties GROUP BY data_quality"
        ):
            lines.append(f"- {r['data_quality']}: {r['n']}")
    elif track == "strata":
        n = conn.execute("SELECT COUNT(*) c FROM assets").fetchone()["c"]
        total = conn.execute("SELECT SUM(nav_usd) s FROM assets").fetchone()["s"]
        lines += [f"Assets: {n}", f"Total NAV USD: {total:,.2f}", "", "## By type"]
        for r in conn.execute(
            "SELECT asset_type, COUNT(*) n, SUM(nav_usd) s FROM assets GROUP BY asset_type ORDER BY s DESC"
        ):
            lines.append(f"- {r['asset_type']}: n={r['n']}  ${r['s']:,.0f}")
        lines += ["", "## Data quality"]
        for r in conn.execute("SELECT data_quality, COUNT(*) n FROM assets GROUP BY data_quality"):
            lines.append(f"- {r['data_quality']}: {r['n']}")
    else:
        n = conn.execute("SELECT COUNT(*) c FROM facilities").fetchone()["c"]
        total = conn.execute("SELECT SUM(revenue_at_risk_usd) s FROM facilities").fetchone()["s"]
        lines += [f"Facilities: {n}", f"Total revenue-at-risk USD: {total:,.2f}", "", "## By country"]
        for r in conn.execute(
            "SELECT country, COUNT(*) n, SUM(revenue_at_risk_usd) s FROM facilities GROUP BY country ORDER BY s DESC"
        ):
            lines.append(f"- {r['country']}: n={r['n']}  ${r['s']:,.0f}")
        lines += ["", "## Criticality"]
        for r in conn.execute(
            "SELECT criticality, COUNT(*) n FROM facilities GROUP BY criticality"
        ):
            lines.append(f"- {r['criticality']}: {r['n']}")

    conn.close()
    out_dir = client_dir(track) / "outputs" / "week-1"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "book_overview.txt"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    append_audit(
        track,
        {"event": "book_overview", "script": "scripts/reference_week1_overview.py", "track": track},
    )
    print(path.read_text())
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
