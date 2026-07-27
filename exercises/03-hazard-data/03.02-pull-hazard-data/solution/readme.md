# Solution — Pull hazard data

## Approach

1. Read the problem acceptance criteria.
2. Implement with a re-runnable Python script under `clients/<track>/outputs/week-3/scripts/`.
3. Save tables/markdown next to the script.
4. Append provenance to `outputs/audit_log.jsonl`.
5. Cross-check a sample of rows manually against CSV/DB.

## Track deltas

- **Colorado:** join on facilities / allocations; $. proxy = storage_kaf or allocation kaf.
- **Kerrville:** join on facilities / exposures; $. = replacement_usd.
- **Datacenter:** join on facilities / impact_topics; $. proxy = mw_nameplate / water_mgy.

## Done when

Problem acceptance criteria pass on your active track without opening this file during the first attempt.
