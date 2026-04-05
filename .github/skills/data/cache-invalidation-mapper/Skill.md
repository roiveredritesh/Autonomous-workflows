---
name: cache-invalidation-mapper
description: Maps all points where cache must be invalidated when data changes to ensure cache consistency.
---

## Purpose
Maps all points where cache must be invalidated when data changes to ensure cache consistency.

## Input Requirements
```yaml
data_change:
  affected_entity: <entity name>
  change_type: <create|update|delete>
  affected_fields: [<fields>]
  systems_involved: [<systems>]
```

## Processing Steps

1. **Identify Cache Keys**
   - What cache keys are affected?
   - Which caches store this data?

2. **Map Invalidation Points**
   - Where does data change?
   - Where must cache clear?

3. **Detect Dependencies**
   - What depends on this data?
   - What else needs invalidating?

4. **Plan Invalidation Strategy**
   - Immediate vs eventual consistency?
   - How to implement?

## Output Format

```yaml
cache_invalidation_map:
  
  affected_cache_keys:
    - key_pattern: <cache key>
      scope: <single|multiple|all>
      affected_by: <entity>
  
  invalidation_points:
    - trigger: <where data changes>
      location: <file:method>
      affected_keys: [<cache keys>]
      urgency: <immediate|eventual|batch>
    
    - trigger: <another point>
      ...
  
  dependency_chain:
    direct_impact:
      - entity: <entity>
        keys: [<keys to clear>]
    
    indirect_impact:
      - entity: <dependent entity>
        reason: <why invalidated>
        keys: [<keys to clear>]
  
  invalidation_strategy:
    approach: <immediate|eventual|batch>
    implementation: [<steps>]
    complexity: <low|medium|high>
  
  completeness_assessment:
    all_invalidation_points_identified: <yes|no>
    risk_of_stale_cache: <low|medium|high>
    stampede_risk: <yes|no>
  
  recommendations:
    - <recommendation>
    - <recommendation>
```

## Related Skills
- `redis-cache-strategy-analyzer` - For cache design
- `cache-stampede-detector` - For stampede risks
