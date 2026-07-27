#!/usr/bin/env python3
"""Reference: book overview for active track (week 1)."""

from __future__ import annotations

import sqlite3

from lib_common import active_track, append_audit, client_dir


def main() -> None:
    track = active_track()
    db = client_dir(track) / "db" / "portfolio.sqlite"
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    lines = [f"# Book overview — {track}", f"DB: {db}", ""]

    if track == "colorado":
        n = conn.execute("SELECT COUNT(*) c FROM facilities").fetchone()["c"]
        total = conn.execute("SELECT SUM(storage_kaf) s FROM facilities").fetchone()["s"] or 0
        lines += [f"Nodes: {n}", f"Storage KAF (sum of storage-type nodes): {total:,.2f}", "", "## By node type"]
        for r in conn.execute(
            "SELECT node_type, COUNT(*) n, SUM(storage_kaf) s FROM facilities GROUP BY node_type ORDER BY n DESC"
        ):
            lines.append(f"- {r['node_type']}: n={r['n']}  storage_kaf={r['s'] or 0:,.1f}")
        lines += ["", "## Data quality"]
        for r in conn.execute("SELECT data_quality, COUNT(*) n FROM facilities GROUP BY data_quality"):
            lines.append(f"- {r['data_quality']}: {r['n']}")
    elif track == "kerrville":
        n = conn.execute("SELECT COUNT(*) c FROM facilities").fetchone()["c"]
        total = conn.execute("SELECT SUM(replacement_usd) s FROM exposures").fetchone()["s"] or 0
        lines += [f"Facilities: {n}", f"Replacement USD: {total:,.2f}", "", "## By facility type"]
        for r in conn.execute(
            """SELECT f.facility_type, COUNT(*) n, SUM(e.replacement_usd) s
               FROM facilities f JOIN exposures e ON e.facility_id=f.id
               GROUP BY f.facility_type ORDER BY s DESC"""
        ):
            lines.append(f"- {r['facility_type']}: n={r['n']}  ${r['s']:,.0f}")
        lines += ["", "## Data quality"]
        for r in conn.execute("SELECT data_quality, COUNT(*) n FROM facilities GROUP BY data_quality"):
            lines.append(f"- {r['data_quality']}: {r['n']}")
    else:  # datacenter
        n = conn.execute("SELECT COUNT(*) c FROM facilities").fetchone()["c"]
        mw = conn.execute("SELECT SUM(mw_nameplate) s FROM facilities").fetchone()["s"] or 0
        water = conn.execute("SELECT SUM(water_mgy) s FROM facilities").fetchone()["s"] or 0
        lines += [f"EIS elements: {n}", f"Nameplate MW (sum): {mw:,.1f}", f"Water MGY (sum): {water:,.1f}", "", "## By element type"]
        for r in conn.execute(
            "SELECT element_type, COUNT(*) n FROM facilities GROUP BY element_type ORDER BY n DESC"
        ):
            lines.append(f"- {r['element_type']}: n={r['n']}")
        lines += ["", "## By EIS alternative"]
        for r in conn.execute(
            "SELECT eis_alternative, COUNT(*) n FROM facilities GROUP BY eis_alternative"
        ):
            lines.append(f"- {r['eis_alternative']}: {r['n']}")

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
