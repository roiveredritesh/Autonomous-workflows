---
name: cache-performance-checker
description: Measures cache read/write performance and evaluates whether caching provides a net benefit by comparing cache overhead against database query cost savings.
---

# Cache Performance Checker

## Quick Example

**Input:** Redis GET/SET for product list, DB query baseline: 450ms, serialization: 380ms, Redis latency: 2ms
**Output:** Net benefit: +68ms per request. Cache is only marginally beneficial — reduce payload size (serialization-overhead-checker recommends DTO projection to reduce to 40ms overhead)
**Time:** 2-3 minutes

---

## Purpose
Measures cache read/write performance and evaluates whether caching provides a net benefit by comparing cache overhead against database query cost savings.

## Input

```yaml
input:
  cache_operation_type: GET|SET|GET_SET
  data_description: <what data is being cached>
  data_size_kb: <approximate size of cached value in KB>
  serialization_method: JSON|BINARY|VIEWSTATE|MESSAGEPACK
  redis_latency_ms: <measured or estimated Redis network latency>
  db_query_baseline_ms: <how long the DB query takes without cache>
  request_frequency_per_minute: <how often this cache key is accessed>
  cache_hit_rate_percent: <current or expected hit rate>
```

## Output

```yaml
output:
  cache_overhead:
    serialization_ms: <ms>
    network_ms: <ms>
    deserialization_ms: <ms>
    total_overhead_ms: <serialize + network + deserialize>
  net_benefit:
    per_cache_hit_ms: <db_baseline - overhead>
    per_cache_miss_ms: <-(overhead) — misses add cost, not savings>
    effective_benefit_ms: <weighted by hit rate>
    break_even_hit_rate: <%>
  verdict: HIGHLY_BENEFICIAL|BENEFICIAL|MARGINAL|NOT_BENEFICIAL
  verdict_reason: <explanation>
  total_time_saved_per_minute_ms: <net_benefit × hit_rate × frequency>
  recommendations:
    - action: <description>
      expected_improvement_ms: <ms>
      priority: critical|high|medium
  confidence: HIGH|MEDIUM|LOW
```

## DO:
✅ Calculate net benefit using effective hit rate — not theoretical maximum
✅ Include both serialization AND deserialization in overhead calculation
✅ Factor in cache miss cost — misses pay overhead without getting the benefit
✅ Compare against the break-even hit rate — if actual hit rate is below it, caching harms
✅ Project total savings per minute to quantify business value

## DON'T:
❌ Assume caching always helps — for fast queries (<20ms), cache overhead may exceed savings
❌ Use theoretical hit rates — use actual measured rates or conservative estimates
❌ Ignore miss cost — at low hit rates, misses dominate and negate savings
❌ Compare only serialization time vs DB time — include all overhead components
❌ Cache data with sub-5ms DB queries — overhead will typically exceed savings

## Error Conditions

**IF DB query baseline is unknown:**
```
1. Profile using sql-execution-analyzer or request-profiler
2. Flag: BASELINE_REQUIRED — cannot assess net benefit without DB query time
```

**IF hit rate is unknown:**
```
1. Check Redis INFO stats for keyspace_hits / (keyspace_hits + keyspace_misses)
2. Use conservative 50% estimate if not measurable
3. Flag: HIT_RATE_ESTIMATED
```

**IF serialization time is unknown:**
```
1. Use serialization-overhead-checker for actual measurement
2. Estimate: JSON = 0.5ms per 10KB, Binary = 0.2ms per 10KB
3. Flag: SERIALIZATION_ESTIMATED
```

## Processing Steps

1. **Overhead Calculation:** Serialization time = data_size × serialization_rate (JSON: ~1ms/20KB). Network time = redis_latency_ms. Deserialization time ≈ serialization × 1.2. Total overhead = sum.

2. **Net Benefit Per Hit:** `per_hit_saving = db_baseline_ms - total_overhead_ms`. If negative, cache costs more than it saves even on hits.

3. **Break-Even Hit Rate:** `break_even = overhead / db_baseline × 100`. If actual hit rate < break_even, caching is net negative. If > break_even, caching is beneficial.

4. **Effective Benefit:** `effective = (hit_rate/100 × per_hit_saving) - ((1 - hit_rate/100) × overhead)`. This accounts for misses that pay overhead with no savings.

5. **Total Savings Per Minute:** `total = effective_benefit_ms × request_frequency_per_minute`. Divide by 1000 for seconds saved per minute.

6. **Verdict Assignment:** HIGHLY_BENEFICIAL: effective > 50ms, hit rate > 70%. BENEFICIAL: effective > 20ms. MARGINAL: effective 5-20ms. NOT_BENEFICIAL: effective < 5ms or negative.

7. **Recommendations:** If NOT_BENEFICIAL: consider removing cache or fixing hit rate. If MARGINAL: reduce payload size to decrease overhead. If BENEFICIAL but overhead high: switch to binary serialization.

## Example

**Input:**
```yaml
cache_operation_type: GET_SET
data_description: "Product catalog list — 4500 items"
data_size_kb: 2800
serialization_method: JSON
redis_latency_ms: 2
db_query_baseline_ms: 450
request_frequency_per_minute: 200
cache_hit_rate_percent: 65
```

**Output:**
```yaml
cache_overhead:
  serialization_ms: 380
  network_ms: 2
  deserialization_ms: 420
  total_overhead_ms: 802
net_benefit:
  per_cache_hit_ms: -352
  per_cache_miss_ms: -802
  effective_benefit_ms: -509
  break_even_hit_rate: "178% (impossible — overhead exceeds DB cost even at 100% hit rate)"
verdict: NOT_BENEFICIAL
verdict_reason: "Cache overhead (802ms) exceeds DB query cost (450ms). Even at 100% hit rate, caching makes requests slower, not faster."
total_time_saved_per_minute_ms: -101800
recommendations:
  - action: "Remove caching for full product list OR reduce payload to <50KB via DTO projection"
    expected_improvement_ms: 802
    priority: critical
  - action: "If caching is needed for DB protection, use binary serialization (MessagePack) to reduce overhead to ~40ms"
    expected_improvement_ms: 760
    priority: high
  - action: "Cache only the 50 most-searched product IDs, not the full catalog"
    expected_improvement_ms: 750
    priority: high
confidence: HIGH
```

---

**Related Skills:**
- `serialization-overhead-checker` - Measures serialization cost that feeds into overhead calculation
- `cache-miss-detector` - Identifies the actual hit rate for accurate benefit calculation
- `redis-behavior-checker` - Measures actual Redis latency for overhead calculation
- `redis-key-strategy-analyzer` - Recommends key and TTL strategy to maximize hit rate
