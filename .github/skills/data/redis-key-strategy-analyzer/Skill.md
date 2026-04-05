---
name: redis-key-strategy-analyzer
description: Analyzes Redis key naming strategy, TTL patterns, and memory usage to identify inefficiencies and recommend optimizations for the ASP.NET WebForms caching layer.
---

# Redis Key Strategy Analyzer

## Quick Example

**Input:** Redis key patterns: `Customer_12345_Search_Active_North`, TTL: 3600s, memory: 450MB used
**Output:** Flat key naming (no namespace separator), inconsistent casing, no eviction budget planned — recommend `customer:search:{region}:{status}` pattern, TTL reduction to 300s saves 80% memory
**Time:** 2-3 minutes

---

## Purpose
Analyzes Redis key naming strategy, TTL patterns, and memory usage to identify inefficiencies and recommend optimizations for the ASP.NET WebForms caching layer.

## Input

```yaml
input:
  key_patterns: <list of observed or designed Redis key patterns>
  ttl_values: <map of key pattern to TTL in seconds>
  memory_usage_mb: <total Redis memory used>
  memory_limit_mb: <Redis maxmemory setting>
  key_count: <approximate total keys>
  eviction_policy: <noeviction|allkeys-lru|volatile-lru|etc>
```

## Output

```yaml
output:
  key_naming_analysis:
    current_pattern: <description>
    follows_namespace_convention: true|false
    namespace_separator: <colon|underscore|none>
    inconsistencies: [<list>]
    recommended_pattern: <format string>
    examples:
      before: <current key example>
      after: <recommended key example>
  ttl_analysis:
    by_category:
      - category: <search results|user session|reference data>
        current_ttl_s: <s>
        recommended_ttl_s: <s>
        reason: <why>
    hot_keys_at_risk: [<keys that expire at same time causing stampede>]
    jitter_recommended: true|false
  memory_efficiency:
    current_usage_mb: <mb>
    estimated_optimal_mb: <mb>
    efficiency_percent: <%>
    largest_key_categories: [<category: size_mb>]
    compression_beneficial: true|false
  recommendations:
    - action: <description>
      expected_benefit: <memory savings or hit rate improvement>
      priority: critical|high|medium
  confidence: HIGH|MEDIUM|LOW
```

## DO:
✅ Enforce colon `:` as namespace separator — it's the Redis community standard
✅ Use lowercase keys consistently — case-sensitive keys cause lookup failures
✅ Design TTLs based on data volatility — not uniform 1-hour for everything
✅ Add random jitter (±10-15%) to TTLs on bulk-loaded keys to prevent stampede
✅ Include the entity ID as the last namespace segment for debuggability

## DON'T:
❌ Use underscores or dots as namespace separators — colons are standard
❌ Encode entire objects in key names — only use identifiers and filter values
❌ Set TTL to 0 (no expiry) unless data is truly immutable configuration
❌ Use Redis as a primary data store — it should be a cache with TTL on all keys
❌ Ignore memory limits — exceeding maxmemory causes unexpected eviction

## Error Conditions

**IF Redis is not accessible for live key analysis:**
```
1. Analyze key patterns from code review only
2. Flag: CODE_ANALYSIS_ONLY — memory and TTL data unavailable
```

**IF memory usage is within 10% of maxmemory:**
```
1. Flag: MEMORY_PRESSURE — eviction is imminent
2. Prioritize memory reduction recommendations
3. Add: URGENT — reduce TTLs or increase maxmemory before cache starts evicting hot keys
```

**IF key naming is entirely inconsistent:**
```
1. Categorize by functional area (search, session, reference)
2. Propose namespace schema for each category
3. Recommend migration plan (dual-write during transition)
```

## Processing Steps

1. **Key Pattern Inventory:** Collect all observed key patterns from code (Redis.Set/Get calls) or from `redis-cli --scan`. Categorize by functional purpose (search results, session data, reference data, computed data).

2. **Naming Convention Check:** Verify: uses `:` separator, lowercase, no spaces, includes entity type and identifier. Flag deviations. Count inconsistencies per category.

3. **TTL Assessment:** For each category, assess data volatility: reference data (product catalog, carrier list) → 1-4 hours; search results → 5-15 minutes; user-specific data → session lifetime; computed aggregates → 30-60 minutes.

4. **Stampede Risk:** Identify bulk-loaded keys with identical TTL. If 1000+ keys expire simultaneously, flag stampede risk. Recommend jitter formula: `TTL = base + Random.Next(-base*0.1, base*0.1)`.

5. **Memory Efficiency:** From `INFO memory` and `DEBUG OBJECT <key>`: estimate average key+value size per category. Multiply by key count. Identify largest memory consumers. Estimate savings from TTL reduction or compression.

6. **Compression Assessment:** If average value size >1KB and values are JSON strings, recommend LZ4/Gzip compression. StackExchange.Redis.Extensions supports transparent compression.

7. **Recommendations:** Prioritize by: (1) memory pressure, (2) stampede risk, (3) naming inconsistency, (4) TTL optimization.

## Example

**Input:**
```yaml
key_patterns:
  - "Customer_12345_Search_Active_North"
  - "CUSTOMER_DETAIL_67890"
  - "orders:pending:page:1"
ttl_values:
  "Customer_*": 3600
  "CUSTOMER_DETAIL_*": 3600
  "orders:*": 3600
memory_usage_mb: 450
memory_limit_mb: 512
eviction_policy: "volatile-lru"
```

**Output:**
```yaml
key_naming_analysis:
  current_pattern: "Mixed — underscores + uppercase in customer keys, colons in orders"
  follows_namespace_convention: false
  namespace_separator: mixed
  inconsistencies:
    - "Customer_ keys use underscore, orders: keys use colon"
    - "CUSTOMER_DETAIL_ uses uppercase"
    - "Customer_ keys embed full filter values in key name"
  recommended_pattern: "{entity}:{sub-type}:{identifier}"
  examples:
    before: "Customer_12345_Search_Active_North"
    after: "customer:search:12345:active:north"
ttl_analysis:
  by_category:
    - category: "Customer search results"
      current_ttl_s: 3600
      recommended_ttl_s: 300
      reason: "Search results change frequently — 1h TTL risks stale data; 5min is appropriate"
    - category: "Customer detail"
      current_ttl_s: 3600
      recommended_ttl_s: 900
      reason: "Customer detail changes infrequently — 15min balances freshness and cache effectiveness"
  hot_keys_at_risk: ["All Customer_ keys set at same time expire simultaneously"]
  jitter_recommended: true
memory_efficiency:
  current_usage_mb: 450
  estimated_optimal_mb: 90
  efficiency_percent: 20%
  largest_key_categories: ["Customer search results: 380MB (84%)"]
  compression_beneficial: true
recommendations:
  - action: "Reduce customer:search TTL from 3600s to 300s — eliminates 80% of memory usage"
    expected_benefit: "360MB memory reduction"
    priority: critical
  - action: "Standardize key naming to colon-separated lowercase: customer:search:{id}:{filter}"
    expected_benefit: "Debuggability and consistent lookup"
    priority: high
  - action: "Add ±10% jitter to all cache SET operations to prevent stampede"
    expected_benefit: "Eliminates thundering herd on cache expiry"
    priority: high
confidence: HIGH
```

---

**Related Skills:**
- `redis-behavior-checker` - Verifies actual Redis behavior against expected TTL and hit rates
- `cache-stampede-detector` - Detects thundering herd conditions related to key expiry
- `cache-invalidation-mapper` - Maps where keys should be invalidated when data changes
- `serialization-overhead-checker` - Analyzes value size and serialization overhead
