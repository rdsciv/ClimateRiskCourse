# STD-01 — Acute coastal / riverine flood (standard)

**Type:** standard (for the record)  
**Physical driver:** Extreme flood event affecting coastal and riverine metros in the book  
**Horizon:** 0–12 months operational; multi-year repair for S2–S3 assets  

## Mechanism

Site inundation → asset damage and downtime → collateral / NAV / revenue impairment → secondary insurance friction.

## Precedent

Public record patterns consistent with major U.S. flood disasters (e.g., Hurricane Harvey-class urban flooding). Training uses **pattern**, not a claim that any simulated site was in a specific historical footprint.

## Screening rule

Include facilities where `hazard_bucket` contains `flood`, `coastal`, `hurricane`, or `slr`.

## Default severity mapping (training)

| hazard_bucket match | Default severity |
|---------------------|------------------|
| high_flood, flood_hurricane, hurricane_flood, hurricane_slr | S2 |
| flood, coastal_flood, coastal | S1 |
| others | S0 (out of scope for this card) |

## Notes

Pair with TR-01 (insurance withdrawal) for transmission-aware runs.
