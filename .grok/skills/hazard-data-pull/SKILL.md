---
name: hazard-data-pull
description: Load firm sample hazard grids or optional live APIs; score entities; audit log every pull.
---

# Hazard data pull

1. Default source: `firm/sample-hazard/county_hazard_scores.csv` (`firm_sample_grid` v1).
2. Join to geocoded entities; document unmatched.
3. Compute documented exposure index.
4. Append `outputs/audit_log.jsonl`.
5. Write `hazard_dataset_readme.md` as the deliverable index.

Never label sample grids as FEMA/NRI/NOAA.
