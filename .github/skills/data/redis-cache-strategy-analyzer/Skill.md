---
name: redis-cache-strategy-analyzer
description: Analyzes caching requirements and designs safe, effective Redis caching strategies for legacy ASP.NET WebForms application.
---

## Purpose
Analyzes caching requirements and designs safe, effective Redis caching strategies for legacy ASP.NET WebForms application.

## Input

```yaml
data_to_cache: <description of data>
access_pattern: <how often accessed>
data_volume: <size estimate>
update_frequency: <how often changes>
consistency_requirement: <strict|eventual|best_effort>
```

## Quick Example

**Input:** Customer list dropdown, 100 req/sec, 2MB, staleness OK 10 min
**Output:** key=`customers:list:active`, TTL=10min+jitter, lock-based stampede mitigation, invalidate on customer update

## Output

```yaml
cache_strategy:
  cache_suitability:
    recommended: <yes|no|conditional>
    reason: <explanation>
    conditions: [<if conditional>]
  
  key_design:
    pattern: <key pattern template>
    examples: [<sample keys>]
    collision_risk: <none|low|medium>
  
  ttl_strategy:
    base_ttl: <duration>
    ttl_type: <fixed|sliding|adaptive>
    reasoning: <why this TTL>
  
  invalidation:
    strategy: <direct|pattern|tag|time>
    trigger_points: [<when to invalidate>]
    code_example: <implementation>
  
  stampede_assessment:
    risk_level: <high|medium|low>
    traffic_estimate: <requests/sec>
    query_cost: <ms>
    mitigation_needed: <yes|no>
    mitigation_strategy: <if needed>
  
  implementation:
    cache_aside: <code example>
    read_through: <code example if applicable>
    write_through: <code example if applicable>
  
  monitoring:
    metrics_to_track: [<list>]
    alert_thresholds: [<conditions>]

confidence: <high|medium|low>
risks: [<identified risks>]
```

## DO
✅ Cache read-heavy shared data (read:write > 10:1)
✅ Use key pattern `{entity}:{id}` or `{entity}:list:{criteria}`
✅ Add TTL jitter to prevent synchronized expiry (stampede)
✅ Use lock-based refresh for high-traffic expensive queries
✅ Invalidate on write: `_cache.Remove($"customer:{id}")`

## DON'T
❌ Cache user-specific sensitive or real-time data
❌ Set long TTLs without an invalidation strategy
❌ Let all keys expire at same time (stampede risk)
❌ Cache write-heavy data or simple cheap queries
❌ Use BinaryFormatter for serialization (security risk)

## Related Skills
- `redis-key-strategy-analyzer` - Key naming patterns
- `cache-stampede-detector` - Stampede risk detection
- `cache-invalidation-mapper` - Invalidation planning
