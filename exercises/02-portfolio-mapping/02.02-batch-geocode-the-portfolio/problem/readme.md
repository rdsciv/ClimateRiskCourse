# Problem — Batch geocode the portfolio

## TODO

1. Read facilities/assets addresses from the DB or CSV.
2. Prefer `geocode_cache` (already seeded offline). Write a script that:
   - Joins cache to entities
   - Writes `outputs/week-2/geocoded_portfolio.csv`
   - Logs the operation to `outputs/audit_log.jsonl` with `source: simulated_offline` or `geocode_cache`
3. Optional stretch: if cache miss, use a public geocoder **and** log it; do not require this for pass.

## Acceptance criteria

- [ ] CSV has lat/lon for ≥95% of rows
- [ ] Script saved under `outputs/week-2/scripts/`
- [ ] Audit log entry present
