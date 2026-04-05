---
name: query-behavior-validator
description: Validates that an optimized query or rewritten SQL returns identical results to the original, ensuring correctness before deploying performance improvements.
---

# Query Behavior Validator

## Quick Example

**Input:** Original: `customers.ToList().Where(c => c.Status == "Active")`, Optimized: `customers.Where(c => c.Status == "Active").ToList()`
**Output:** MATCH — row counts identical (1,847), random sample of 50 rows: all fields match, order preserved, CONFIDENT results are equivalent
**Time:** 2-3 minutes

---

## Purpose
Validates that an optimized query or rewritten SQL returns identical results to the original, ensuring correctness before deploying performance improvements.

## Input

```yaml
input:
  original_query: <original LINQ or SQL query>
  optimized_query: <new LINQ or SQL query>
  test_dataset: <description of test data to use — production sample, staging, specific records>
  result_comparison_method: ROW_COUNT|FULL_COMPARISON|SAMPLE|HASH
  order_sensitive: <true|false — must results be in same order>
  null_handling: <how nulls are handled — include, exclude, coerce>
```

## Output

```yaml
output:
  validation_result: MATCH|MISMATCH|PARTIAL_MATCH|UNABLE_TO_VALIDATE
  confidence_level: HIGH|MEDIUM|LOW
  comparison_details:
    original_row_count: <count>
    optimized_row_count: <count>
    row_count_match: true|false
    column_count_match: true|false
    mismatched_rows: <count>
    mismatched_columns: [<list if mismatch>]
    sample_checked: <rows sampled>
    order_preserved: true|false
  edge_case_checks:
    - check: <edge case tested>
      result: PASS|FAIL
      detail: <what was found>
  data_integrity_assessment:
    all_expected_rows_present: true|false
    no_extra_rows: true|false
    field_values_match: true|false
  deploy_recommendation: SAFE_TO_DEPLOY|NOT_SAFE|INVESTIGATE_FURTHER
  issues_found:
    - issue: <description>
      severity: CRITICAL|HIGH|MEDIUM
      fix: <correction>
  confidence: HIGH|MEDIUM|LOW
```

## DO:
✅ Test with representative data including edge cases (nulls, empty sets, large datasets)
✅ Test with the same parameters/filters that production uses most often
✅ Verify NULL handling is consistent between original and optimized
✅ Check ordering if the caller depends on result order
✅ Test with boundary data (0 results, 1 result, maximum expected results)

## DON'T:
❌ Only test with small "happy path" datasets — edge cases expose bugs
❌ Skip null/empty result testing — LINQ rewrites often break on empty sets
❌ Assume row count match = full correctness — sample column values too
❌ Ignore ordering differences if the result is consumed as an ordered list
❌ Test only in development — validate in staging with production-scale data

## Error Conditions

**IF queries cannot be run in test environment:**
```
1. Perform static analysis of LINQ expression trees for equivalence
2. Flag: STATIC_ANALYSIS_ONLY — cannot guarantee runtime equivalence without execution
3. Recommend: run comparison in staging before production deployment
```

**IF original query produces non-deterministic results:**
```
1. Run original query multiple times to establish expected variability
2. Verify optimized query has same variability range
3. Flag: NON_DETERMINISTIC — comparison based on multiple runs
```

**IF dataset is too large for full comparison:**
```
1. Use hash comparison or statistical sampling (1000 random rows)
2. Flag: SAMPLED_VALIDATION — full comparison not feasible; using statistical sample
```

## Processing Steps

1. **Query Normalization:** Parse both queries. Identify: what tables/entities are accessed, what filters are applied, what columns are selected, what ordering is applied. Note any differences in structure.

2. **Static Equivalence Check:** Before execution, verify: both queries touch same tables, apply equivalent filter conditions (even if expressed differently), select same columns. Flag any structural differences.

3. **Test Dataset Selection:** Use: production sample (anonymized if needed), or staging data matching production volume pattern. Include: typical records, records matching filter boundary, records with nulls, empty result scenarios.

4. **Execution Comparison:** Run both queries against same dataset. Collect: row count, column names, random sample of 50 rows. Compare row by row for sample.

5. **Edge Case Testing:** Run both with: empty result filter (WHERE 1=0), single result filter, null parameter values, maximum expected result count. Verify both handle identically.

6. **Order Verification:** If order_sensitive: compare first 20 and last 20 rows of ordered result. Verify same ORDER BY effective behavior even if expressed differently.

7. **Recommendation:** SAFE_TO_DEPLOY if all checks pass. NOT_SAFE if any CRITICAL mismatch. INVESTIGATE_FURTHER if partial match with unclear cause.

## Example

**Input:**
```yaml
original_query: |
  var customers = _db.Customers.ToList()
      .Where(c => c.Status == filter.Status && c.Region == filter.Region)
      .OrderBy(c => c.Name)
      .ToList();
optimized_query: |
  var customers = _db.Customers
      .Where(c => c.Status == filter.Status && c.Region == filter.Region)
      .OrderBy(c => c.Name)
      .ToList();
test_dataset: "Staging DB — 45,000 customers, filter: Status=Active, Region=North"
result_comparison_method: SAMPLE
order_sensitive: true
null_handling: "Exclude null Status records"
```

**Output:**
```yaml
validation_result: MATCH
confidence_level: HIGH
comparison_details:
  original_row_count: 1847
  optimized_row_count: 1847
  row_count_match: true
  column_count_match: true
  mismatched_rows: 0
  mismatched_columns: []
  sample_checked: 50
  order_preserved: true
edge_case_checks:
  - {check: "Empty result (Status=Deleted filter)", result: PASS, detail: "Both return 0 rows"}
  - {check: "Single result (specific Name filter)", result: PASS, detail: "Both return same 1 row"}
  - {check: "Null Region records", result: PASS, detail: "Both exclude null Region — WHERE clause identical"}
  - {check: "Maximum result set (no Status filter)", result: PASS, detail: "Both return 45,000 rows in same order"}
data_integrity_assessment:
  all_expected_rows_present: true
  no_extra_rows: true
  field_values_match: true
deploy_recommendation: SAFE_TO_DEPLOY
issues_found: []
confidence: HIGH
```

---

**Related Skills:**
- `sql-execution-analyzer` - Analyzes the SQL generated by both queries for comparison
- `cache-correctness-validator` - Validates cached results match DB after query optimization
- `performance-regression-checker` - Checks performance impact of the optimized query
- `n-plus-one-detector` - Uses this validator to confirm N+1 fixes return identical results
