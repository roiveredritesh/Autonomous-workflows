---
name: cache-miss-detector
description: Detects cache miss patterns that cause repeated expensive database calls, distinguishing cold cache misses from structural misses indicating broken cache logic.
---

# Cache Miss Detector

## Quick Example

**Input:** `product:catalog:*` Redis keys, DB query frequency 800/min, Redis logs from last hour
**Output:** 72% miss rate detected, cold-start misses: 5% — remaining 67% are structural misses (cache never being populated), 800 unnecessary DB queries/min
**Time:** 2-3 minutes

---

## Purpose
Detects cache miss patterns that cause repeated expensive database calls, distinguishing cold cache misses from structural misses indicating broken cache logic.

## Input

```yaml
input:
  cache_key_patterns: <list of Redis key patterns to analyze>
  db_query_frequency: <observed DB queries per minute for the operation>
  redis_logs: <optional — Redis log file or MONITOR output>
  expected_cache_coverage: <percent of requests that should be served from cache>
  operation_name: <name of the operation being cached (for context)>
  cache_warming_strategy: <NONE|ON_DEMAND|BACKGROUND|PRELOAD>
```

## Output

```yaml
output:
  miss_analysis:
    overall_miss_rate_percent: <%>
    cold_start_misses_percent: <%>
    structural_misses_percent: <%>
    eviction_misses_percent: <%>
    key_not_set_misses_percent: <%>
  miss_patterns:
    - pattern: <description of recurring miss scenario>
      frequency_per_minute: <count>
      db_cost_per_miss_ms: <ms>
      total_db_cost_per_minute_ms: <ms>
      root_cause: <why the cache is missing>
  wasted_db_calls:
    per_minute: <count>
    per_hour: <count>
    estimated_db_load_percent: <%>
  recommendations:
    - action: <cache warming, TTL extension, fix key construction, etc>
      expected_miss_reduction_percent: <%>
      priority: critical|high|medium
  confidence: HIGH|MEDIUM|LOW
```

## DO:
✅ Distinguish structural misses (cache not populated) from cold-start misses (normal first access)
✅ Calculate the DB cost of each miss in milliseconds to quantify business impact
✅ Check if the same key is being missed repeatedly — indicates cache not being set on read-through
✅ Verify that cache writes happen on the same code path as cache reads
✅ Check for cache key construction bugs — subtle format differences cause consistent misses

## DON'T:
❌ Treat all misses as a problem — cold-start misses after deploy are expected
❌ Attempt to eliminate all misses — some data should not be cached
❌ Ignore the cost-per-miss — a 5ms miss on infrequent data is not worth fixing
❌ Confuse low hit rate with low coverage — some key patterns may be intentionally uncached
❌ Skip checking the cache-write path — misses are often caused by SET never being called

## Error Conditions

**IF Redis MONITOR is unavailable (production restriction):**
```
1. Analyze hit/miss rates from INFO stats instead
2. Infer patterns from DB query frequency vs expected cache rate
3. Flag: MONITOR_UNAVAILABLE — analysis based on aggregate stats, not per-key
```

**IF DB query frequency baseline is unknown:**
```
1. Estimate from page load frequency × data access per page
2. Flag: FREQUENCY_ESTIMATED — actual DB query count may differ
```

**IF multiple key patterns overlap:**
```
1. Analyze each pattern independently
2. Note overlap in output and combine totals for summary
```

## Processing Steps

1. **Miss Rate Baseline:** From Redis `INFO stats`: extract `keyspace_hits` and `keyspace_misses`. Calculate `miss_rate = misses / (hits + misses)`. Compare against `expected_cache_coverage`.

2. **Miss Pattern Classification:** Analyze miss types:
   - Cold-start: Keys missing right after deploy (check key age via object idletime)
   - Structural: Keys consistently absent for specific patterns (never SET)
   - Eviction: Keys present then missing (check `evicted_keys` counter trend)
   - Key-not-set: Read path checks cache but write path doesn't set it

3. **Key Construction Audit:** For each pattern, verify key format: `{namespace}:{entity}:{id}`. Compare key format in GET vs SET operations in code. Detect format inconsistencies (e.g., different ID types, case differences).

4. **DB Cost Calculation:** For each miss pattern: `cost = db_query_ms × miss_frequency_per_minute`. Sum across all patterns for total wasted DB load.

5. **Code Path Tracing:** Verify cache-aside pattern is implemented correctly: `GET → if null → DB → SET → return`. Check that SET uses same key format as GET. Verify SET is not conditional on other flags.

6. **Recommendations:** For structural misses: fix SET logic. For eviction: increase TTL or Redis memory. For cold-start: implement cache warming. For key bugs: fix key construction.

## Example

**Input:**
```yaml
cache_key_patterns: ["product:catalog:*", "product:detail:{id}"]
db_query_frequency: 800
expected_cache_coverage: 80%
operation_name: "Product Catalog Load"
cache_warming_strategy: NONE
```

**Output:**
```yaml
miss_analysis:
  overall_miss_rate_percent: 72%
  cold_start_misses_percent: 5%
  structural_misses_percent: 67%
  eviction_misses_percent: 0%
  key_not_set_misses_percent: 67%
miss_patterns:
  - pattern: "product:catalog:* keys are checked on GET but never SET — ProductService.GetCatalog() reads cache but cache-aside SET is commented out"
    frequency_per_minute: 536
    db_cost_per_miss_ms: 450
    total_db_cost_per_minute_ms: 241200
    root_cause: "Cache SET line commented out during a debugging session, never re-enabled"
  - pattern: "product:detail:{id} key format uses int ID in code but string ID in Redis — key mismatch causes consistent miss"
    frequency_per_minute: 38
    db_cost_per_miss_ms: 120
    total_db_cost_per_minute_ms: 4560
    root_cause: "ID type mismatch: code uses $'product:detail:{id}' where id is int, but set uses id.ToString('D8') — format differs"
wasted_db_calls:
  per_minute: 574
  per_hour: 34440
  estimated_db_load_percent: 72%
recommendations:
  - action: "Re-enable cache SET in ProductService.GetCatalog() — restore the commented line"
    expected_miss_reduction_percent: 67%
    priority: critical
  - action: "Fix key format: use id.ToString() consistently in both GET and SET for product:detail"
    expected_miss_reduction_percent: 5%
    priority: high
  - action: "Implement cache warming on application startup for product catalog"
    expected_miss_reduction_percent: 5%
    priority: medium
confidence: HIGH
```

---

**Related Skills:**
- `redis-behavior-checker` - Verifies Redis connection health and overall cache behavior
- `cache-stampede-detector` - Detects thundering herd conditions caused by simultaneous misses
- `cache-invalidation-analyzer` - Analyzes whether invalidation is causing unexpected misses
- `redis-cache-strategy-analyzer` - Evaluates overall caching strategy for correctness
