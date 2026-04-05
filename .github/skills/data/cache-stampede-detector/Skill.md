---
name: cache-stampede-detector
description: Detects conditions that cause cache stampede (thundering herd) on cache expiry and recommends mitigation strategies including TTL jitter, locking, and early refresh.
---

# Cache Stampede Detector

## Quick Example

**Input:** Redis TTL: 300s, concurrent users: 500, product catalog query: 2000ms
**Output:** HIGH stampede risk — at TTL expiry, 500 concurrent requests hit DB simultaneously for 2000ms each = 1M request-ms DB spike. Recommend: jitter ±15%, probabilistic early refresh
**Time:** 2-3 minutes

---

## Purpose
Detects conditions that cause cache stampede (thundering herd) on cache expiry and recommends mitigation strategies including TTL jitter, locking, and early refresh.

## Input

```yaml
input:
  cache_ttl_seconds: <TTL of the cache key in seconds>
  concurrent_request_rate: <requests per second hitting this cache key>
  db_query_cost_ms: <how long the DB query takes when cache misses>
  cache_key_count: <how many distinct keys expire at similar times>
  current_mitigation: <NONE|JITTER|LOCK|EARLY_REFRESH>
  data_volatility: HIGH|MEDIUM|LOW
```

## Output

```yaml
output:
  stampede_risk:
    level: CRITICAL|HIGH|MEDIUM|LOW
    probability: <%>
    explanation: <why this risk level>
  impact_assessment:
    simultaneous_db_hits_estimate: <count>
    db_overload_duration_ms: <how long DB is overwhelmed>
    requests_failed_or_slow_estimate: <count>
    revenue_impact: <description if significant>
  mitigation_strategies:
    - strategy: TTL_JITTER
      description: <how to implement>
      effectiveness: HIGH|MEDIUM|LOW
      implementation_example: <code snippet>
      risk: LOW
    - strategy: PROBABILISTIC_EARLY_REFRESH
      description: <how to implement>
      effectiveness: HIGH
      implementation_example: <code snippet>
      risk: MEDIUM
    - strategy: DISTRIBUTED_LOCK
      description: <how to implement>
      effectiveness: HIGH
      implementation_example: <code snippet>
      risk: MEDIUM
    - strategy: BACKGROUND_REFRESH
      description: <how to implement>
      effectiveness: HIGH
      implementation_example: <code snippet>
      risk: LOW
  recommended_strategy: <strategy name>
  recommended_reason: <why this strategy best fits the scenario>
  confidence: HIGH|MEDIUM|LOW
```

## DO:
✅ Calculate simultaneous DB hits as: concurrent_rate × db_query_cost_ms / 1000
✅ Consider key_count when multiple keys expire at the same time (bulk-loaded data)
✅ Recommend jitter as the first mitigation — it's simple, low risk, highly effective
✅ Suggest probabilistic early refresh for high-value, slowly-changing data
✅ Recommend distributed lock (RedLock) for very expensive or data-critical operations

## DON'T:
❌ Ignore stampede risk for infrequently accessed data — it's a problem for popular keys only
❌ Recommend distributed lock for all scenarios — it adds latency and complexity
❌ Suggest infinite TTL to avoid expiry — it trades stampede risk for stale data risk
❌ Overlook the impact of bulk cache loads with identical TTLs (e.g., on deploy)
❌ Ignore the DB capacity — stampede impact depends on DB's ability to absorb spikes

## Error Conditions

**IF concurrent request rate is unknown:**
```
1. Estimate from page views per minute / number of distinct cache keys
2. Flag: RATE_ESTIMATED — stampede risk calculation is approximate
```

**IF DB query cost is unknown:**
```
1. Use baseline from performance-profiler or sql-execution-analyzer
2. Flag: COST_ESTIMATED — use 200ms as conservative estimate
```

**IF cache TTL is very long (>1 hour):**
```
1. Stampede risk is lower due to infrequency
2. Focus on impact magnitude rather than probability
3. Still recommend jitter for bulk-loaded keys
```

## Processing Steps

1. **Risk Calculation:** Simultaneous hits estimate = `concurrent_rate × db_query_cost_ms / 1000`. Risk levels: CRITICAL > 100 simultaneous hits, HIGH 20-100, MEDIUM 5-20, LOW < 5.

2. **Impact Assessment:** DB overload duration = `db_query_cost_ms` (all concurrent requests wait). Requests affected = `concurrent_rate × db_query_cost_ms / 1000`. Revenue impact = affected users × conversion rate.

3. **Jitter Strategy:** Simple: `TTL = base_ttl + random.Next(-base_ttl*0.15, base_ttl*0.15)`. For 300s TTL: jitter range 255-345s. Spreads expiry over 90-second window, reducing peak simultaneous hits by ~90%.

4. **Probabilistic Early Refresh:** When remaining TTL < random threshold, proactively refresh in background. Formula: refresh if `Random() < Math.Exp(-remaining_ttl / (beta × db_query_cost))`. Ensures fresh data without lock contention.

5. **Distributed Lock:** Use RedLock via StackExchange.Redis. First miss acquires lock, refreshes cache, releases lock. Others wait/return stale data during lock. Risk: lock holder failure leaves waiters stuck.

6. **Background Refresh:** Scheduled job refreshes cache before expiry (at 80% of TTL). Most effective for slowly-changing, high-value data. Risk: requires background task management.

7. **Strategy Selection:** For high-traffic, simple data → Jitter. For expensive queries, tolerable staleness → Background Refresh. For critical correctness → Distributed Lock. For best UX → Probabilistic Early Refresh.

## Example

**Input:**
```yaml
cache_ttl_seconds: 300
concurrent_request_rate: 50
db_query_cost_ms: 2000
cache_key_count: 10
current_mitigation: NONE
data_volatility: LOW
```

**Output:**
```yaml
stampede_risk:
  level: HIGH
  probability: 85%
  explanation: "50 req/s × 2s query = 100 simultaneous DB hits at expiry. 10 keys with same TTL amplifies to 1000 hits if loaded at same time (e.g., after deploy)"
impact_assessment:
  simultaneous_db_hits_estimate: 100
  db_overload_duration_ms: 2000
  requests_failed_or_slow_estimate: 100
  revenue_impact: "~100 users experience 2s+ delay every 5 minutes"
mitigation_strategies:
  - strategy: TTL_JITTER
    description: "Add ±15% random jitter to 300s TTL — spreads expiry over 90-second window"
    effectiveness: HIGH
    implementation_example: |
      var jitter = new Random().Next(-45, 45); // ±15% of 300s
      db.StringSet(key, value, TimeSpan.FromSeconds(300 + jitter));
    risk: LOW
  - strategy: BACKGROUND_REFRESH
    description: "Refresh cache at 80% TTL (240s) via background timer — keeps cache always warm"
    effectiveness: HIGH
    implementation_example: |
      // In startup: schedule refresh every 240s
      _timer = new Timer(RefreshProductCache, null, 0, 240000);
    risk: LOW
recommended_strategy: TTL_JITTER
recommended_reason: "Data volatility is LOW — simple jitter is sufficient and lowest risk. Background refresh is overkill for data that changes infrequently."
confidence: HIGH
```

---

**Related Skills:**
- `cache-miss-detector` - Detects the miss patterns that trigger stampede conditions
- `redis-cache-strategy-analyzer` - Evaluates overall caching strategy including stampede prevention
- `redis-key-strategy-analyzer` - Analyzes key TTL patterns that contribute to stampede risk
- `cache-invalidation-analyzer` - Ensures invalidation strategy doesn't create additional stampede risk
