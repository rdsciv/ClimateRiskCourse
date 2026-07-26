# Solution — Batch geocode

Training DBs already contain lat/lon and `geocode_cache`. The learning goal is the **pipeline + audit log**, not fighting Nominatim.

```python
# SELECT id, address, city, lat, lon FROM facilities/assets
# write CSV; append_audit(...)
```

If you clear lat/lon to practice, rebuild from cache by address key.
