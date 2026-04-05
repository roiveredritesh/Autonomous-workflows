---
name: sql-execution-analyzer
description: Analyzes SQL query execution details including actual execution plan, row estimates vs actuals, and index usage to identify the root cause of slow queries.
---

# SQL Execution Analyzer

## Quick Example

**Input:** `SELECT * FROM Customers WHERE Status = 'Active' ORDER BY LastName`
**Output:** Table scan on 45,000 rows (no index on Status), estimated 7,200 row reads vs 1,200 actuals, missing index on (Status, LastName) — 95% improvement possible
**Time:** 3-5 minutes

---

## Purpose
Analyzes SQL query execution details including actual execution plan, row estimates vs actuals, and index usage to identify the root cause of slow queries.

## Input

```yaml
input:
  sql_query: <T-SQL query text or stored procedure name>
  table_names: <optional list of tables involved>
  database_name: <SQL Server database name>
  execution_context: <ENTITY_FRAMEWORK|LINQ_TO_SQL|ADO_NET|STORED_PROC>
  include_actual_plan: <true|false — requires query execution, default false>
  parameter_values: <optional — parameter values for parameterized queries>
```

## Output

```yaml
output:
  query_summary:
    type: SELECT|INSERT|UPDATE|DELETE|STORED_PROC
    tables_accessed: [<list>]
    estimated_rows_returned: <count>
    actual_rows_returned: <count if available>
    estimated_cost: <query optimizer cost>
  execution_plan_highlights:
    operators:
      - operator: <TableScan|IndexSeek|IndexScan|NestedLoops|HashJoin|etc>
        table: <name>
        cost_percent: <%>
        rows_estimated: <count>
        rows_actual: <count if available>
        is_bottleneck: true|false
  index_usage:
    indexes_used: [<index name>]
    missing_indexes:
      - table: <name>
        columns: [<list>]
        included_columns: [<list>]
        estimated_improvement: <%>
        create_statement: <CREATE INDEX ...>
    full_scans: [<table names with scans>]
  statistics_health:
    outdated_stats: [<table names>]
    recommendation: <UPDATE STATISTICS recommendation>
  performance_assessment:
    severity: CRITICAL|HIGH|MEDIUM|LOW
    primary_issue: <description>
    estimated_improvement_percent: <%>
  recommendations:
    - action: <what to change>
      priority: critical|high|medium
  confidence: HIGH|MEDIUM|LOW
```

## DO:
✅ Use `SET STATISTICS IO ON` and `SET STATISTICS TIME ON` to get actual I/O metrics
✅ Compare estimated vs actual row counts — large divergence indicates stale statistics
✅ Focus on operators with highest cost percentage in the plan
✅ Check for key lookups — they indicate a non-covering index
✅ Verify parameter sniffing issues by testing with different parameter values

## DON'T:
❌ Analyze estimated plan only — actual plan reveals row count accuracy
❌ Ignore warnings in execution plan (missing index hints, implicit conversions)
❌ Assume adding an index always helps — over-indexing hurts write performance
❌ Skip checking for implicit data type conversions — they prevent index usage
❌ Overlook join operators — Nested Loops on large sets are a common bottleneck

## Error Conditions

**IF execution plan cannot be obtained:**
```
1. Use estimated plan from SSMS: SET SHOWPLAN_XML ON
2. Flag: ESTIMATED_PLAN_ONLY — actual row counts unavailable
```

**IF query uses dynamic SQL:**
```
1. Extract the actual SQL from sp_executesql calls
2. Analyze each dynamic variant separately
3. Flag: DYNAMIC_SQL — plan caching may be suboptimal
```

**IF stored procedure is large (>200 lines):**
```
1. Focus on the highest-cost sections identified in execution plan
2. Flag: LARGE_PROC — analyze in sections; check for recompilation hints
```

## Processing Steps

1. **Query Parsing:** Identify query type, tables referenced, JOIN conditions, WHERE predicates, ORDER BY columns, GROUP BY columns. Note any subqueries or CTEs.

2. **Execution Plan Retrieval:** Execute with `SET STATISTICS IO ON; SET STATISTICS TIME ON`. Capture XML execution plan via `SET STATISTICS XML ON` or SSMS. If production (no execution allowed), use estimated plan.

3. **Operator Analysis:** Walk execution plan tree. Identify: physical operators (scan vs seek), join algorithms (nested loops vs hash join vs merge join), row count estimates vs actuals. Calculate cost percentage per operator.

4. **Index Analysis:** For each table access, determine: what index (if any) is used, whether a seek or scan is performed, whether a key lookup follows (non-covering index), whether index covers the query.

5. **Missing Index Detection:** Parse the MissingIndexes node in XML plan. For each missing index suggestion: extract table, columns, included columns, estimated improvement percentage. Generate CREATE INDEX statement.

6. **Statistics Assessment:** Check `sys.stats` for last update date. If statistics are >7 days old on volatile tables, flag for update. Large estimate/actual divergence is a statistics indicator.

7. **Recommendations:** Prioritize by impact: missing index (highest), statistics update, query rewrite (remove implicit conversion, push predicates down, split complex query).

## Example

**Input:**
```yaml
sql_query: "SELECT c.*, o.OrderDate FROM Customers c LEFT JOIN Orders o ON c.Id = o.CustomerId WHERE c.Status = 'Active' ORDER BY c.LastName"
database_name: "AajLogistics"
execution_context: LINQ_TO_SQL
include_actual_plan: false
```

**Output:**
```yaml
query_summary:
  type: SELECT
  tables_accessed: [Customers, Orders]
  estimated_rows_returned: 45000
  estimated_cost: 28.4
execution_plan_highlights:
  operators:
    - operator: TableScan
      table: Customers
      cost_percent: 78%
      rows_estimated: 45000
      is_bottleneck: true
    - operator: NestedLoops
      table: "Customers × Orders"
      cost_percent: 18%
      rows_estimated: 45000
      is_bottleneck: false
index_usage:
  indexes_used: ["PK_Customers", "PK_Orders"]
  missing_indexes:
    - table: Customers
      columns: [Status]
      included_columns: [Id, LastName, FirstName, Email]
      estimated_improvement: 94%
      create_statement: "CREATE INDEX IX_Customers_Status ON Customers (Status) INCLUDE (LastName, FirstName, Email)"
  full_scans: [Customers]
statistics_health:
  outdated_stats: [Orders]
  recommendation: "UPDATE STATISTICS Orders WITH FULLSCAN"
performance_assessment:
  severity: CRITICAL
  primary_issue: "Full table scan on 45,000-row Customers table — no index on Status column"
  estimated_improvement_percent: 94%
recommendations:
  - action: "Create index: CREATE INDEX IX_Customers_Status ON Customers (Status) INCLUDE (LastName, FirstName, Email)"
    priority: critical
  - action: "In LINQ: project to DTO instead of SELECT * — avoid loading unused columns"
    priority: high
  - action: "UPDATE STATISTICS Orders WITH FULLSCAN"
    priority: medium
confidence: HIGH
```

---

**Related Skills:**
- `sql-execution-plan-analyzer` - Deep analysis of the XML execution plan structure
- `missing-index-detector` - Dedicated detection and scoring of missing indexes
- `linq-query-tracer` - Identifies the LINQ code generating inefficient SQL
- `stored-procedure-analyzer` - Analyzes stored procedures for similar execution issues
