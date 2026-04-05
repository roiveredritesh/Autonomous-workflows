---
name: serialization-overhead-checker
description: Measures overhead introduced by object serialization (ViewState, JSON, Redis cache, Session) to identify cases where serialization cost outweighs caching benefit.
---

# Serialization Overhead Checker

## Quick Example

**Input:** `CustomerList` object (4500 items), stored in Redis via JSON serialization
**Output:** Serialization: 380ms, payload size: 2.8MB, deserialization: 420ms — overhead exceeds DB query time; recommend projection to DTO with 15 fields instead of 80
**Time:** 2-3 minutes

---

## Purpose
Measures overhead introduced by object serialization (ViewState, JSON, Redis cache, Session) to identify cases where serialization cost outweighs caching benefit.

## Input

```yaml
input:
  object_type: <class name or description>
  serialization_method: VIEWSTATE|JSON|REDIS_BINARY|XML|SESSION
  object_size_estimate: <approximate item count or size>
  context: <where serialization occurs — Redis cache, ViewState, Session, API response>
  current_performance_ms: <optional — known serialization time if already measured>
```

## Output

```yaml
output:
  serialization:
    method: <VIEWSTATE|JSON|etc>
    estimated_time_ms: <ms>
    payload_size_bytes: <bytes>
    payload_size_human: <KB or MB>
  deserialization:
    estimated_time_ms: <ms>
  round_trip_overhead_ms: <serialize + deserialize>
  baseline_db_time_ms: <how long the DB query would take without cache>
  net_benefit_ms: <baseline_db_time - round_trip_overhead>
  is_beneficial: true|false
  bloat_sources:
    - field: <property name>
      reason: <why it's bloating — circular ref, large collection, binary data>
      estimated_size_bytes: <bytes>
  recommendations:
    - action: <what to change>
      expected_size_reduction_percent: <%>
      expected_time_saving_ms: <ms>
      priority: critical|high|medium
  confidence: HIGH|MEDIUM|LOW
```

## DO:
✅ Measure round-trip cost (serialize + deserialize) — not just one direction
✅ Compare overhead against the baseline DB query time to assess net benefit
✅ Identify object graph issues: circular references, large nested collections, binary blobs
✅ Check ViewState fields for Telerik RadGrid — it serializes entire control state
✅ Recommend DTO projection to reduce payload size before serialization

## DON'T:
❌ Assume caching is always beneficial — serialization overhead can exceed DB query time
❌ Serialize full entity objects — always project to minimal DTOs for cache
❌ Ignore payload size — large payloads consume Redis memory and increase network time
❌ Forget that ViewState is Base64-encoded — actual payload is larger than it appears
❌ Test with a single small object — test with realistic data volumes

## Error Conditions

**IF object type is not serializable:**
```
1. Check for [Serializable] attribute or JSON-incompatible types
2. Return: NOT_SERIALIZABLE — <type> contains non-serializable members: <list>
```

**IF serialization method is ViewState but page is not provided:**
```
1. Request page name to check EnableViewState settings
2. Return: PAGE_REQUIRED — ViewState analysis needs the hosting page context
```

**IF estimated object size is unknown:**
```
1. Estimate from table row count × average row size
2. Flag output: SIZE_ESTIMATED — actual measurement may differ
```

## Processing Steps

1. **Object Analysis:** Inspect the object type's property tree. Count properties, identify collection types, detect nested objects, flag binary or image fields.

2. **Serialization Estimation:** Based on method and object structure: JSON → estimate character count × 1.1 (overhead); ViewState → estimate binary size × 1.37 (Base64 factor); Binary → estimate raw size.

3. **Timing Estimation:** Use known benchmarks: JSON.NET serializes ~500MB/s, ViewState ~200MB/s, StackExchange.Redis binary ~800MB/s. Calculate estimated ms from payload size.

4. **Deserialization:** Estimate deserialization time — typically 1.2-1.5× serialization time due to object graph reconstruction.

5. **Net Benefit Calculation:** `net_benefit_ms = baseline_db_time_ms - round_trip_overhead_ms`. If negative, caching is harmful. If <20ms positive, caching provides minimal benefit.

6. **Bloat Detection:** Find properties that inflate size without value: binary fields, lazy-load collections that materialize, audit fields not needed by UI, circular references.

7. **Recommendations:** Suggest DTO projection, field exclusion attributes ([JsonIgnore]), enabling compression for large payloads, or switching serialization method.

## Example

**Input:**
```yaml
object_type: "CustomerEntity (EF entity with navigation properties)"
serialization_method: JSON
object_size_estimate: "4500 items in list"
context: "Redis cache for customer search results"
```

**Output:**
```yaml
serialization:
  method: JSON
  estimated_time_ms: 380
  payload_size_bytes: 2940000
  payload_size_human: "2.8 MB"
deserialization:
  estimated_time_ms: 420
round_trip_overhead_ms: 800
baseline_db_time_ms: 350
net_benefit_ms: -450
is_beneficial: false
bloat_sources:
  - field: "Orders"
    reason: "Navigation property — loads entire order history per customer"
    estimated_size_bytes: 2100000
  - field: "AuditFields"
    reason: "6 audit columns not used by UI"
    estimated_size_bytes: 280000
recommendations:
  - action: "Project to CustomerSearchDto with 12 fields instead of serializing full CustomerEntity"
    expected_size_reduction_percent: 85%
    expected_time_saving_ms: 700
    priority: critical
  - action: "Disable lazy loading before caching — materialize only needed navigation properties"
    expected_size_reduction_percent: 70%
    expected_time_saving_ms: 500
    priority: high
  - action: "Enable Redis compression for payloads >1MB using StackExchange.Redis.Extensions"
    expected_size_reduction_percent: 60%
    expected_time_saving_ms: 200
    priority: medium
confidence: HIGH
```

---

**Related Skills:**
- `webforms-viewstate-analyzer` - Specific analysis of ViewState size per Telerik control
- `redis-cache-strategy-analyzer` - Evaluates overall caching strategy including serialization fit
- `redis-key-strategy-analyzer` - Analyzes key structure and memory efficiency
- `cache-performance-checker` - Measures actual net benefit of cache including overhead
