# Problem — Asset-level exposure scoring

## TODO

Combine hazard scores with book $ metrics into `outputs/week-3/exposure_scores.csv`:

- entity id
- primary hazard and score
- $ metric (outstanding / nav / revenue_at_risk)
- composite `exposure_index` = f(score, $) — define and document
- data_quality

Write `outputs/week-3/scoring_method.md` explaining the formula (**computed**).

## Acceptance criteria

- [ ] Method file defines formula
- [ ] Top 10 by exposure_index listed in a short summary md
