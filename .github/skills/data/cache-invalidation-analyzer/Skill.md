---
name: cache-invalidation-analyzer
description: Analyzes cache invalidation correctness by identifying stale data risks, missing invalidation points, and over-invalidation patterns in the ASP.NET WebForms application.
---

# Cache Invalidation Analyzer

## Quick Example

**Input:** `customer:search:*` cache, CustomerRepository.Update() mutation
**Output:** CustomerRepository.Update() does NOT invalidate cache — stale search results will persist until TTL expiry (300s). 3 other mutation paths (import, bulk update, admin edit) also missing invalidation
**Time:** 3-5 minutes

---

## Purpose
Analyzes cache invalidation correctness by identifying stale data risks, missing invalidation points, and over-invalidation patterns in the ASP.NET WebForms application.

## Input

```yaml
input:
  cache_keys: <list of cache key patterns to analyze>
  data_mutation_operations: <list of operations that change the underlying data>
  invalidation_code_locations: <optional — files or methods where cache.Remove() is called>
  related_tables: <DB tables that the cached data reads from>
  invalidation_strategy: EXPLICIT_DELETE|TAG_BASED|TTL_ONLY|WRITE_THROUGH
```

## Output

```yaml
output:
  invalidation_coverage:
    operations_checked: <count>
    operations_with_invalidation: <count>
    operations_missing_invalidation: <count>
    coverage_percent: <%>
  missing_invalidation_points:
    - operation: <method or action name>
      location: <file:method>
      affected_cache_keys: [<patterns>]
      stale_data_risk: CRITICAL|HIGH|MEDIUM|LOW
      max_staleness_seconds: <TTL if no invalidation>
      impact: <what users see when data is stale>
  incorrect_invalidation:
    - issue: OVER_INVALIDATION|WRONG_KEY|MISSING_WILDCARD
      location: <file:method>
      description: <detail>
      fix: <what to change>
  stale_data_scenarios:
    - scenario: <user action or data mutation>
      probability: HIGH|MEDIUM|LOW
      user_impact: <description>
      duration_seconds: <how long stale>
  recommendations:
    - action: <what to add or change>
      location: <where in code>
      priority: critical|high|medium
  confidence: HIGH|MEDIUM|LOW
```

## DO:
✅ Trace all code paths that mutate the underlying data (not just the obvious one)
✅ Check for bulk mutation operations (imports, admin batch updates) that bypass normal code paths
✅ Verify wildcard invalidation when key pattern includes variable segments
✅ Check for race conditions between cache read and invalidation (read-invalidate-write window)
✅ Include indirect mutations: SQL jobs, direct DB updates, external API writes

## DON'T:
❌ Only check the primary mutation path — look for all paths to the same data
❌ Assume TTL-only invalidation is sufficient for mutable business data
❌ Over-invalidate by clearing entire cache namespaces on any change
❌ Forget to invalidate dependent/derived cache keys (e.g., search results when detail changes)
❌ Skip checking stored procedures — they may mutate data without triggering ORM events

## Error Conditions

**IF mutation operations are not listed:**
```
1. Search codebase for all INSERT/UPDATE/DELETE on related_tables
2. Search for Repository.Save(), Repository.Update(), Repository.Delete() methods
3. Flag: OPERATIONS_INFERRED — review list for completeness
```

**IF cache invalidation is entirely TTL-based:**
```
1. Assess maximum acceptable staleness for each cache type
2. For mutable business data with TTL > 30s, flag as HIGH risk
3. Recommend explicit invalidation for low-TTL or high-mutation-rate scenarios
```

**IF code is split across multiple projects:**
```
1. Check each project for mutation operations
2. Cross-project mutations are highest risk — no shared invalidation mechanism
3. Flag: CROSS_PROJECT_MUTATION — distributed invalidation strategy required
```

## Processing Steps

1. **Cache Key Inventory:** List all cache keys/patterns. For each key, identify: what data it represents, which DB table(s) it reads from, what filter parameters are encoded in the key.

2. **Mutation Discovery:** Search codebase for all operations that write to the related DB tables: direct SQL, EF SaveChanges, Repository.Save/Update/Delete, bulk import methods, SQL Server jobs. Also check REST APIs and background services.

3. **Invalidation Search:** For each cache key pattern, find all `cache.Remove(key)`, `db.KeyDelete(key)`, `cache.Clear()` calls. Verify the key patterns match exactly (including wildcards for pattern-based keys).

4. **Coverage Mapping:** For each mutation × cache key pair: does the mutation trigger an invalidation of that key? Record: YES (covered), NO (missing), PARTIAL (some paths covered).

5. **Gap Analysis:** For missing invalidations: calculate max staleness = cache TTL. Assess user impact: what does a user see if they read stale data after this mutation?

6. **Incorrect Invalidation Check:** Look for: invalidating on READ (wrong), invalidating entire namespace on single-record change (over-invalidation), invalidating with wrong key format (typos, format mismatch).

7. **Recommendations:** Ordered by stale_data_risk: CRITICAL → immediate fix, HIGH → fix in current sprint, MEDIUM → add to technical debt.

## Example

**Input:**
```yaml
cache_keys: ["customer:search:*", "customer:detail:{id}"]
data_mutation_operations:
  - "CustomerRepository.Update(customer)"
  - "CustomerRepository.BulkImport(customers)"
  - "Admin page: Customer_Admin.aspx → batch status update"
related_tables: [Customers]
invalidation_strategy: EXPLICIT_DELETE
```

**Output:**
```yaml
invalidation_coverage:
  operations_checked: 3
  operations_with_invalidation: 1
  operations_missing_invalidation: 2
  coverage_percent: 33%
missing_invalidation_points:
  - operation: "CustomerRepository.BulkImport()"
    location: "CustomerRepository.cs:BulkImport:line 234"
    affected_cache_keys: ["customer:search:*", "customer:detail:{id}"]
    stale_data_risk: CRITICAL
    max_staleness_seconds: 300
    impact: "After bulk import, search results show old customer data for up to 5 minutes"
  - operation: "Admin batch status update (Customer_Admin.aspx)"
    location: "Customer_Admin.aspx.cs:btnUpdateStatus_Click:line 89"
    affected_cache_keys: ["customer:search:*", "customer:detail:{id}"]
    stale_data_risk: HIGH
    max_staleness_seconds: 300
    impact: "Customers shown as 'Active' in search after admin marks them 'Inactive'"
incorrect_invalidation: []
stale_data_scenarios:
  - scenario: "Admin imports 500 new customers via bulk import"
    probability: HIGH
    user_impact: "New customers don't appear in search results for up to 5 minutes"
    duration_seconds: 300
recommendations:
  - action: "Add cache.RemoveByPattern('customer:search:*') at end of CustomerRepository.BulkImport()"
    location: "CustomerRepository.cs:BulkImport"
    priority: critical
  - action: "Add cache.RemoveByPattern('customer:search:*') and cache.Remove(key) in Customer_Admin status update handler"
    location: "Customer_Admin.aspx.cs:btnUpdateStatus_Click"
    priority: high
confidence: HIGH
```

---

**Related Skills:**
- `cache-invalidation-mapper` - Maps all cache keys to their invalidation trigger points
- `redis-behavior-checker` - Verifies actual Redis hit/miss behavior and TTL correctness
- `cache-correctness-validator` - Validates that cached data matches DB after invalidation
- `cache-miss-detector` - Detects miss patterns that may result from over-invalidation
