# Anchors — damage bands and credit / economic transmission

**Status:** Training anchors for simulated clients. Not a regulatory model.  
**Use:** Scenario engines may apply these bands when site-level engineering is unavailable. Always disclose.

## Physical damage bands (site-level severity → loss fraction of replacement / NAV)

| Severity | Description | Indicative damage fraction |
|----------|-------------|----------------------------|
| S0 | Nuisance / short interruption | 0–2% |
| S1 | Moderate repairable damage, days–weeks downtime | 5–15% |
| S2 | Major damage, months downtime | 20–40% |
| S3 | Severe / constructive total for vulnerable assets | 50–80% |

Apply **judgment** if construction type is unknown: use midpoint and widen range.

## Credit book (Ironwood) — LGD / rating migration sketch

When collateral is RE or operating assets in the affected geography:

| Hazard severity on facility | Drawn exposure impact (training default) |
|-----------------------------|------------------------------------------|
| S1 | +50 to +150 bps risk premium (judgment band); watchlist |
| S2 | 10–25% of drawn treated as elevated default risk for staging discussion |
| S3 | 25–50% of drawn flagged for capital / limit action discussion |

These are **not** PD models. They force a pricing/capital conversation, not a Basel number.

## Fund book (Strata) — exit cap-rate / NAV sketch

| Severity | Training exit impact |
|----------|----------------------|
| S1 | +10 to +25 bps exit cap (judgment) |
| S2 | +25 to +75 bps; hold vs exit revisit |
| S3 | Walk-away or recap case; insurance non-renewal multiplies severity one step |

## Industrial network (Northwood) — revenue-at-risk sketch

| Node criticality × severity | Training outcome |
|----------------------------|------------------|
| critical × S2+ | Full `revenue_at_risk_usd` for 30–90 day horizon in scenario |
| high × S2 | 50% of RAR |
| single-source tier-1 × S2+ | Add 1.5× multiplier for dual-source gap (judgment) |

## Insurance transmission (all tracks)

If `insurance_status` in {`exclusions_flood`, `in_market_review`, `sublimited`} or facility `insured=0`:

- Increase effective severity **one step** (cap at S3)
- Document as institutional transmission, not physical science

## Prohibitions

- Do not present anchor midpoints as engineering truth.
- Do not invent tighter bands without a logged data source.
