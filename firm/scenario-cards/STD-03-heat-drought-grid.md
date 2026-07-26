# STD-03 — Extreme heat, drought, and grid stress (standard)

**Type:** standard  
**Physical driver:** Multi-week extreme heat with water constraints and peak grid stress  

## Mechanism

Labor productivity loss, cooling cost spikes, load-shed risk for energy-intensive sites, agricultural and water-dependent supplier stress.

## Precedent

Southwest U.S. heat domes; drought-linked industrial water curtailments.

## Screening rule

`hazard_bucket` contains `heat`, `drought`, or `grid`.

## Default severity

| Role / type | Severity |
|-------------|----------|
| datacenter, assembly, casting, battery | S2 |
| office / retail | S1 |
| ag-linked | S2 |
