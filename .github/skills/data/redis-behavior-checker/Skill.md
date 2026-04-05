---
name: redis-behavior-checker
description: Verifies Redis cache behavior including hit/miss rates, key expiry, data consistency, and connection health for the ASP.NET WebForms application.
---

# Redis Behavior Checker

## Quick Example

**Input:** Cache key pattern `customer:search:*`, expected TTL 300s, GET operation
**Output:** Hit rate: 12% (expected 70%), actual TTL: 45s (expected 300s), 88% of requests bypass cache — TTL misconfiguration detected
**Time:** 2-3 minutes

---

## Purpose
Verifies Redis cache behavior including hit/miss rates, key expiry, data consistency, and connection health for the ASP.NET WebForms application.

## Input

```yaml
input:
  cache_key_pattern: <Redis key or glob pattern, e.g. "customer:search:*">
  expected_ttl_seconds: <what TTL the code should be setting>
  operation_type: GET|SET|GET_SET|ALL
  redis_connection: <optional — connection string or StackExchange.Redis config>
  sample_window_minutes: <how long to observe, default 10>
  expected_hit_rate_percent: <what hit rate the application expects>
```

## Output

```yaml
output:
  connection_health:
    status: HEALTHY|DEGRADED|UNREACHABLE
    latency_ms_p50: <ms>
    latency_ms_p95: <ms>
    connected_clients: <count>
  key_analysis:
    keys_matching_pattern: <count>
    actual_ttl_seconds:
      min: <s>
      p50: <s>
      max: <s>
    ttl_matches_expected: true|false
    ttl_anomalies: [<description>]
  hit_miss_rates:
    hit_rate_percent: <%>
    miss_rate_percent: <%>
    hit_rate_meets_expectation: true|false
  data_consistency:
    sample_keys_checked: <count>
    consistent_with_db: true|false|UNKNOWN
    stale_keys_found: <count>
  anomalies:
    - type: <TTL_TOO_SHORT|KEY_NOT_FOUND|WRONG_DATA_TYPE|EVICTION_DETECTED>
      description: <detail>
      severity: HIGH|MEDIUM|LOW
  recommendations:
    - action: <what to fix>
      priority: critical|high|medium
  confidence: HIGH|MEDIUM|LOW
```

## DO:
✅ Sample actual TTL from Redis using `TTL <key>` — don't trust code alone
✅ Verify hit rate against expected rate from application monitoring
✅ Check for key eviction if Redis memory is constrained (maxmemory policy)
✅ Test with the exact key format the application uses — key naming bugs are common
✅ Check `OBJECT ENCODING` to verify data type matches expectations

## DON'T:
❌ Assume TTL is being set correctly — always verify with `TTL <key>` command
❌ Ignore memory pressure — low hit rates can be caused by eviction, not just cold cache
❌ Test with empty cache — warm cache behavior is what matters in production
❌ Conflate connection health with data correctness — test both separately
❌ Skip consistency check — stale cache data causes silent data integrity bugs

## Error Conditions

**IF Redis is unreachable:**
```
1. Check StackExchange.Redis connection string and firewall
2. Try `redis-cli ping` from app server
3. Return: REDIS_UNREACHABLE — verify Redis server status and network connectivity
```

**IF no keys match the pattern:**
```
1. Cache may be cold or key naming is wrong
2. Check application code for actual key construction format
3. Return: NO_KEYS_FOUND — cache may be cold or key pattern is incorrect
```

**IF hit rate is 0% despite keys existing:**
```
1. Check if application reads from same Redis instance it writes to
2. Verify key prefix matches between read and write operations
3. Flag: ZERO_HIT_RATE — possible key mismatch between write and read paths
```

## Processing Steps

1. **Connection Verification:** Establish StackExchange.Redis connection. Send `PING`. Measure latency. Check `CLIENT LIST` for active connections. Verify `INFO server` for version and memory stats.

2. **Key Discovery:** Run `SCAN 0 MATCH <pattern> COUNT 1000`. Collect matching keys. Count them. Sample up to 50 for detailed analysis.

3. **TTL Sampling:** For each sampled key, run `TTL <key>`. Collect distribution. Compare against `expected_ttl_seconds`. Flag keys with TTL significantly shorter than expected (evicted early or set incorrectly).

4. **Hit Rate Measurement:** From Redis `INFO stats`: get `keyspace_hits` and `keyspace_misses`. Calculate hit rate. Compare against `expected_hit_rate_percent`. Alternatively monitor in real-time using `MONITOR` for `sample_window_minutes`.

5. **Data Consistency Sampling:** For 10 sampled keys, deserialize cached value and compare against live DB query for the same key's entity. Flag any mismatches.

6. **Anomaly Detection:** Check `INFO memory` for eviction stats (`evicted_keys > 0` with `allkeys-lru` policy). Check `INFO keyspace` for expiry patterns. Detect wrong data types with `TYPE <key>`.

7. **Recommendations:** Map findings to actions: low hit rate → warm-up strategy or TTL increase; TTL mismatch → fix code; stale data → fix invalidation; eviction → increase Redis memory.

## Example

**Input:**
```yaml
cache_key_pattern: "customer:search:*"
expected_ttl_seconds: 300
operation_type: GET_SET
expected_hit_rate_percent: 70
sample_window_minutes: 10
```

**Output:**
```yaml
connection_health:
  status: HEALTHY
  latency_ms_p50: 1
  latency_ms_p95: 2
  connected_clients: 8
key_analysis:
  keys_matching_pattern: 142
  actual_ttl_seconds: {min: 40, p50: 45, max: 48}
  ttl_matches_expected: false
  ttl_anomalies: ["Actual TTL ~45s vs expected 300s — likely set with wrong unit (ms vs s)"]
hit_miss_rates:
  hit_rate_percent: 12%
  miss_rate_percent: 88%
  hit_rate_meets_expectation: false
data_consistency:
  sample_keys_checked: 20
  consistent_with_db: true
  stale_keys_found: 0
anomalies:
  - type: TTL_TOO_SHORT
    description: "Keys expire after ~45s instead of expected 300s — TimeSpan.FromSeconds vs TimeSpan.FromMilliseconds bug"
    severity: HIGH
recommendations:
  - action: "Fix TTL setting in CustomerCache.Set() — change TimeSpan.FromMilliseconds(300) to TimeSpan.FromSeconds(300)"
    priority: critical
  - action: "Add integration test that verifies TTL using StackExchange.Redis after cache set"
    priority: high
confidence: HIGH
```

---

**Related Skills:**
- `redis-cache-strategy-analyzer` - Evaluates the overall Redis caching strategy for correctness
- `cache-invalidation-mapper` - Maps where cache keys should be invalidated on data mutation
- `cache-miss-detector` - Identifies patterns in cache misses that cause DB overload
- `redis-key-strategy-analyzer` - Analyzes key naming and TTL strategy for optimization
