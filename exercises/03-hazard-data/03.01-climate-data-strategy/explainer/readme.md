# Climate data strategy

## Slot architecture

Hazard data sits in a **swappable slot**. Training uses `firm/sample-hazard/county_hazard_scores.csv`. Live APIs or vendor files can replace the slot if provenance is updated.

## Resolution trade-offs

| Grid | Pros | Cons |
|------|------|------|
| County / coarse | Fast whole-book | Misses site nuance |
| High-res flood | Engineering detail | Costly; false precision if building data thin |

Match resolution to decision. Pricing triage can start coarse.

## Structure backward

Week 6 needs tables with: entity id, hazard scores, scenario severities, $ metric, lineage. Design week-3 tables for that join, not for pretty maps alone.
