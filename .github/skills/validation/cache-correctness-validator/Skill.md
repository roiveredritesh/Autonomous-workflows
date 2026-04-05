---
name: cache-correctness-validator
description: Validates that cached data matches the source of truth (database) and that cache invalidation is correctly implemented to prevent stale data issues.
---

# Cache Correctness Validator

## Quick Example

**Input:** Cache key `customer:detail:12345`, cached customer object, DB query: `SELECT * FROM Customers WHERE Id = 12345`
**Output:** MATCH — 18 fields compared, all match. Staleness risk: TTL is 300s but customer updated 120s ago — data is current. Invalidation coverage: verified on Customer.Update()
**Time:** 2-3 minutes

---

## Purpose
Validates that cached data matches the source of truth (database) and that cache invalidation is correctly implemented to prevent stale data issues.

## Input

```yaml
input:
  cache_key: <Redis key to validate>
  cached_value: <current value in Redis (deserialized)>
  db_query: <SQL or LINQ query to fetch the source of truth>
  invalidation_triggers: <list of operations that should invalidate this key>
  staleness_tolerance_seconds: <how old cached data can be — equal to TTL>
  comparison_fields: <optional — specific fields to compare, default all>
```

## Output

```yaml
output:
  correctness_result:
    data_matches: true|false
    match_confidence: HIGH|MEDIUM|LOW
    fields_compared: <count>
    fields_matching: <count>
    fields_mismatching: <count>
    mismatch_details:
      - field: <field name>
        cached_value: <value>
        db_value: <value>
        severity: CRITICAL|HIGH|MEDIUM
  staleness_assessment:
    cache_age_seconds: <how old the cached data is>
    last_mutation_seconds_ago: <when data was last changed in DB>
    is_current: true|false
    staleness_risk: LOW|MEDIUM|HIGH
  invalidation_coverage:
    triggers_checked: [<list>]
    triggers_with_invalidation: [<list>]
    triggers_missing_invalidation: [<list>]
    coverage_percent: <%>
  overall_correctness_score: <0-100>
  issues:
    - issue: <description>
      severity: CRITICAL|HIGH|MEDIUM
      fix: <correction>
  confidence: HIGH|MEDIUM|LOW
```

## DO:
✅ Compare all fields including timestamps, status flags, and audit fields
✅ Check the last mutation timestamp against cache age — is the cache current?
✅ Test invalidation by mutating data and verifying the cache key is removed
✅ Check all code paths that mutate the data, not just the primary one
✅ Verify field types match — int cached as string will cause data type bugs

## DON'T:
❌ Accept "row count matches" as proof of correctness — field values must match too
❌ Skip timestamp fields — they often differ and reveal staleness issues
❌ Assume invalidation works — execute the mutation and verify cache is removed
❌ Test only the happy path — test edge cases like concurrent updates
❌ Forget to check the deserialization type — cached JSON may not deserialize correctly

## Error Conditions

**IF cache key doesn't exist:**
```
1. Check if TTL has expired or cache is cold
2. Run the DB query to get expected value
3. Return: KEY_MISSING — cache is cold or expired; cannot validate correctness
```

**IF DB query cannot be executed:**
```
1. Compare against a known-good data snapshot
2. Flag: DB_UNAVAILABLE — correctness validation requires DB access
```

**IF cached value cannot be deserialized:**
```
1. This is a CRITICAL issue — application cannot read the cache
2. Return: DESERIALIZATION_FAILED — cached data type mismatch with expected type
3. Flag: CORRUPTION_RISK — clear this key immediately
```

## Processing Steps

1. **Cache Read:** Retrieve value from Redis using the cache key. Deserialize using the same method the application uses (JSON.NET, MessagePack, etc.). Note deserialization success/failure.

2. **DB Query Execution:** Run the source-of-truth query. Parse results into the same object type. Record all field values.

3. **Field Comparison:** Compare cached object vs DB result field by field. For each field: record match/mismatch. Flag mismatches by severity: primary key mismatch = CRITICAL, status/name mismatch = HIGH, audit field mismatch = MEDIUM.

4. **Staleness Assessment:** If cache key has creation timestamp or version: calculate cache age. Query DB for last update timestamp (UpdatedAt, RowVersion). If cache age > last mutation age: data is current. If cache age < last mutation age: data is stale.

5. **Invalidation Testing:** For each listed invalidation_trigger: simulate the operation in test environment, verify the cache key is deleted or updated after the operation. Record coverage.

6. **Score Calculation:** Start 100. Deduct: each field mismatch (-5 to -30 based on severity), missing invalidation trigger (-15 per trigger), deserialization failure (-100). Score 90+ = CORRECT, 70-89 = MOSTLY_CORRECT, <70 = INCORRECT.

## Example

**Input:**
```yaml
cache_key: "customer:detail:12345"
db_query: "SELECT * FROM Customers WHERE Id = 12345"
invalidation_triggers:
  - "CustomerRepository.Update(customer)"
  - "CustomerRepository.BulkImport()"
staleness_tolerance_seconds: 900
comparison_fields: [Id, CompanyName, Status, Email, Region, UpdatedAt]
```

**Output:**
```yaml
correctness_result:
  data_matches: true
  match_confidence: HIGH
  fields_compared: 6
  fields_matching: 6
  fields_mismatching: 0
  mismatch_details: []
staleness_assessment:
  cache_age_seconds: 240
  last_mutation_seconds_ago: 7200
  is_current: true
  staleness_risk: LOW
invalidation_coverage:
  triggers_checked: ["CustomerRepository.Update(customer)", "CustomerRepository.BulkImport()"]
  triggers_with_invalidation: ["CustomerRepository.Update(customer)"]
  triggers_missing_invalidation: ["CustomerRepository.BulkImport()"]
  coverage_percent: 50%
overall_correctness_score: 85
issues:
  - issue: "CustomerRepository.BulkImport() does not invalidate customer:detail:{id} keys"
    severity: HIGH
    fix: "Add cache.Remove(key) for each affected customer ID in BulkImport(), or clear customer:detail:* pattern after bulk import"
confidence: HIGH
```

---

**Related Skills:**
- `query-behavior-validator` - Validates the DB query that serves as the source of truth
- `cache-invalidation-analyzer` - Analyzes all invalidation points for completeness
- `redis-behavior-checker` - Checks Redis TTL and hit/miss rates alongside correctness
- `redis-key-inspector` - Inspects the raw key content used in validation
