---
name: linq-query-tracer
description: Analyzes LINQ queries to understand SQL translation, identify performance issues, and ensure optimal data access patterns.
---

## Purpose
Analyzes LINQ queries to understand SQL translation, identify performance issues, and ensure optimal data access patterns.

## Input

```yaml
query_location: <file and method>
linq_query: <LINQ expression or code>
context: <Entity Framework|LINQ to SQL|other>
performance_concern: <yes|no>
```

## Quick Example

**Input:** `var customers = _context.Customers.ToList().Where(c => c.Status == "Active").OrderBy(c => c.Name);`
**Output:** client_side_filtering (high), client_side_ordering (medium) — fix: move `.Where().OrderBy()` before `.ToList()`

## Output

```yaml
query_trace:
  linq_expression: <formatted LINQ>
  generated_sql: <predicted SQL>
  execution_type: <database|in_memory|mixed>
  
issues_detected:
  - issue: <N+1|client_side_filter|missing_index|etc>
    severity: <high|medium|low>
    location: <specific line>
    explanation: <why this is an issue>
    performance_impact: <description>
    fix: <recommended solution>
  
recommendations:
  - recommendation: <specific action>
    code_example: <corrected code>
    expected_improvement: <percentage or description>
  
performance_assessment:
  current_approach: <description>
  estimated_complexity: <O(n)|O(n²)|etc>
  data_volume_sensitivity: <high|medium|low>
  database_load: <heavy|moderate|light>
  
index_recommendations:
  - table: <table name>
    columns: [<column list>]
    type: <clustered|nonclustered>
    reason: <justification>

safe_to_execute: <yes|no|needs_optimization>
confidence: <high|medium|low>
```

## DO
✅ Filter, order, and project before `.ToList()`
✅ Use `.Include()` for related data instead of lazy loading in loops
✅ Use `.Any()` instead of `.ToList().Any()` for existence checks
✅ Use `.Skip().Take()` for pagination
✅ Recommend indexes for frequently filtered unindexed columns

## DON'T
❌ Call `.ToList()` before `.Where()` or `.OrderBy()`
❌ Access navigation properties in a loop without eager loading (N+1)
❌ Load all columns when only a few are needed
❌ Use `.Count()` when `.Any()` suffices
❌ Ignore missing index recommendations for large tables

## Error Conditions

**IF query cannot be translated to SQL:**
- Flag execution_type as `in_memory` — all data loaded from DB
- Explain which expression breaks SQL translation
- Recommend refactor to IQueryable chain

**IF N+1 detected:**
- Flag severity: high
- Provide `.Include()` fix with expected improvement estimate

## Related Skills
- `n-plus-one-detector` - Specialised N+1 detection
- `missing-index-detector` - Index recommendations
- `sql-execution-analyzer` - SQL query analysis
