# Solution — Connect and query the book

## Pattern

```python
import sqlite3
from pathlib import Path

db = Path("clients/colorado-river-reservoirs/db/portfolio.sqlite")  # or active track
conn = sqlite3.connect(db)
print(conn.execute("SELECT COUNT(*) FROM counterparties").fetchone())
# GROUP BY sector / data_quality; SUM(outstanding_usd)
```

Adapt table names: Colorado `facilities`/`allocations`, Kerrville `facilities`/`exposures`, Datacenter `facilities`/`impact_topics`.

## Tip

Have Grok write the script, then **you** run it. The point is a reproducible artifact, not a chat transcript.
