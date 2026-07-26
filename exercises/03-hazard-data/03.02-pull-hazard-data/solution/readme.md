# Solution — Pull hazard data

## Approach

1. Read the problem acceptance criteria.
2. Implement with a re-runnable Python script under `clients/<track>/outputs/week-3/scripts/`.
3. Save tables/markdown next to the script.
4. Append provenance to `outputs/audit_log.jsonl`.
5. Cross-check a sample of rows manually against CSV/DB.

## Track deltas

- **Ironwood:** join on counterparties / facilities / exposures; $. = outstanding/drawn.
- **Strata:** join on assets / valuations; $. = nav_usd.
- **Northwood:** join on facilities / suppliers; $. = revenue_at_risk_usd.

## Done when

Problem acceptance criteria pass on your active track without opening this file during the first attempt.
