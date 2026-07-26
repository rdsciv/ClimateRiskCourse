# STD-02 — Wildfire and prolonged smoke disruption (standard)

**Type:** standard  
**Physical driver:** Regional wildfire season with direct structure risk and multi-week air quality / power shutoff disruption  

## Mechanism

Direct loss for wildland-urban assets; productivity and logistics loss for others in smoke corridor; grid PSPS-style interruptions for datacenters and manufacturing.

## Precedent

Western U.S. wildfire seasons with multi-week smoke impacts and public safety power shutoffs.

## Screening rule

`hazard_bucket` contains `wildfire`.

## Default severity

| Match | Severity |
|-------|----------|
| wildfire with structure adjacency (RE, timber, hospitality) | S2 |
| smoke/PSPS-sensitive (datacenter, assembly) | S1 |
| others in bucket | S1 |
