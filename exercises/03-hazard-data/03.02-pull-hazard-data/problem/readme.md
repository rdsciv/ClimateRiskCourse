# Problem — Pull hazard data

## TODO

1. Load `firm/sample-hazard/county_hazard_scores.csv`.
2. Map each geocoded entity to a county score (training shortcut: map by state+city using a simple city→county table you create, or nearest city match from the sample file’s metros).
3. Save `outputs/week-3/entity_hazard_scores.csv`.
4. Append audit log: source `firm_sample_grid`, version `v1`.

## Acceptance criteria

- [ ] ≥90% entities scored (document unmatched)
- [ ] Audit log entry complete
- [ ] Script re-runnable
