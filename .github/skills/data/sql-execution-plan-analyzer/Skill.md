---
name: sql-execution-plan-analyzer
description: Analyzes SQL Server execution plans for table scans, key lookups, nested loops, and other inefficiencies to prescribe targeted index and query improvements.
---

# SQL Execution Plan Analyzer

## Quick Example

**Input:** XML execution plan for customer search query, 8-second runtime
**Output:** TableScan on Customers (78% cost), Key Lookup on Orders (15% cost), missing covering index — CREATE INDEX recommended with 94% improvement estimate
**Time:** 3-5 minutes

---

## Purpose
Analyzes SQL Server execution plans for table scans, key lookups, nested loops, and other inefficiencies to prescribe targeted index and query improvements.

## Input

```yaml
input:
  sql_query: <T-SQL query text>
  execution_plan_xml: <optional — XML from SET STATISTICS XML ON or SSMS>
  estimated_plan_only: <true|false — if actual plan unavailable>
  table_row_counts: <optional map of table name to approximate row count>
```

## Output

```yaml
output:
  plan_summary:
    total_estimated_cost: <optimizer cost units>
    plan_type: ESTIMATED|ACTUAL
    parallelism_used: true|false
  costly_operations:
    - rank: <1-based>
      operator: <TableScan|IndexScan|KeyLookup|NestedLoops|HashJoin|Sort>
      table_or_index: <name>
      cost_percent: <%>
      rows_in: <count>
      rows_out: <count>
      issue: <SCAN_INSTEAD_OF_SEEK|KEY_LOOKUP|LARGE_SORT|CARTESIAN>
      severity: CRITICAL|HIGH|MEDIUM
  scan_vs_seek:
    scans: [<table names>]
    seeks: [<table names with index names>]
  key_lookups:
    - table: <name>
      lookup_columns: [<columns needed that aren't in index>]
      fix: <add columns to index as INCLUDE>
  implicit_conversions:
    - column: <name>
      from_type: <type>
      to_type: <type>
      index_disabled: true|false
  recommended_indexes:
    - table: <name>
      key_columns: [<list>]
      included_columns: [<list>]
      estimated_improvement: <%>
      create_statement: <T-SQL>
  query_rewrites:
    - issue: <description>
      original_pattern: <SQL fragment>
      suggested_pattern: <SQL fragment>
  confidence: HIGH|MEDIUM|LOW
```

## DO:
✅ Focus on the highest-cost operators first (top 3 by cost percentage)
✅ Identify key lookups — they indicate a non-covering index needs INCLUDE columns
✅ Flag implicit data type conversions — they prevent index seek usage
✅ Check for Sort operators on large row sets — indicates missing ORDER BY index
✅ Detect nested loop joins on large tables — hash join or merge join may be better

## DON'T:
❌ Optimize low-cost operators (<5% of plan cost) — marginal return
❌ Add INCLUDE columns blindly — only add columns actually needed by the query
❌ Ignore the Estimated Rows vs Actual Rows divergence — it reveals stale statistics
❌ Recommend parallel plans without checking server core count and MAXDOP setting
❌ Suggest non-clustered index on columns already in the clustered index key

## Error Conditions

**IF execution plan XML is not provided:**
```
1. Use SSMS: Query → Include Actual Execution Plan → run query
2. Or: SET STATISTICS XML ON; <query>; SET STATISTICS XML OFF
3. Return: PLAN_REQUIRED — paste XML from SSMS for full analysis
```

**IF plan shows Parallelism operator with high cost:**
```
1. Check MAXDOP setting and CPU count
2. Flag: PARALLEL_PLAN — may indicate query is too expensive for single-thread
```

**IF estimated cost is 0 or plan is trivial:**
```
1. Query may be cached or parameterized to a different plan
2. Request fresh execution with OPTION (RECOMPILE)
```

## Processing Steps

1. **Plan Parsing:** Parse execution plan XML (ShowPlanXML). Walk RelOp nodes. Extract: operator name, estimated cost, rows in/out, warnings.

2. **Cost Ranking:** Sort all operators by EstimatedTotalSubtreeCost descending. Calculate each operator's percentage of root cost. Flag top 3 as primary analysis targets.

3. **Scan Detection:** For each PhysicalOp="Table Scan" or "Index Scan", flag as inefficiency. Note table name and row count. Check if a seek alternative exists (correct index).

4. **Key Lookup Detection:** Find Lookup operator nodes. Extract which columns are being fetched from the base table (not in the non-clustered index). Generate INCLUDE recommendation.

5. **Implicit Conversion Detection:** Look for CONVERT_IMPLICIT warnings in XML. These occur when query parameter type differs from column type (e.g., VARCHAR vs NVARCHAR). Flag column and types.

6. **Join Analysis:** For nested loops on >10,000 row estimates, recommend hash join (`OPTION (HASH JOIN)`) or index to avoid loops. For hash joins with large memory grants, investigate row estimate accuracy.

7. **Index Recommendations:** Combine scan tables with filter columns (WHERE) and sort columns (ORDER BY). Generate CREATE INDEX with key columns (filter/sort) and INCLUDE columns (SELECT list not in key).

## Example

**Input:**
```yaml
sql_query: "SELECT c.Id, c.Name, o.OrderDate FROM Customers c LEFT JOIN Orders o ON c.Id = o.CustomerId WHERE c.Status = 'Active'"
estimated_plan_only: true
table_row_counts: {Customers: 45000, Orders: 280000}
```

**Output:**
```yaml
plan_summary:
  total_estimated_cost: 28.4
  plan_type: ESTIMATED
  parallelism_used: false
costly_operations:
  - rank: 1
    operator: TableScan
    table_or_index: Customers
    cost_percent: 78%
    rows_in: 45000
    rows_out: 45000
    issue: SCAN_INSTEAD_OF_SEEK
    severity: CRITICAL
  - rank: 2
    operator: NestedLoops
    table_or_index: "Customers × Orders"
    cost_percent: 15%
    rows_in: 45000
    rows_out: 45000
    issue: LARGE_NESTED_LOOP
    severity: HIGH
scan_vs_seek:
  scans: [Customers]
  seeks: ["Orders (PK_Orders)"]
key_lookups: []
implicit_conversions: []
recommended_indexes:
  - table: Customers
    key_columns: [Status]
    included_columns: [Id, Name]
    estimated_improvement: 94%
    create_statement: "CREATE NONCLUSTERED INDEX IX_Customers_Status ON Customers (Status) INCLUDE (Id, Name)"
query_rewrites:
  - issue: "LEFT JOIN Orders loads all orders — filter with TOP 1 or EXISTS if only checking existence"
    original_pattern: "LEFT JOIN Orders o ON c.Id = o.CustomerId"
    suggested_pattern: "OUTER APPLY (SELECT TOP 1 OrderDate FROM Orders WHERE CustomerId = c.Id ORDER BY OrderDate DESC) o"
confidence: HIGH
```

---

**Related Skills:**
- `sql-execution-analyzer` - Full execution analysis including I/O stats and actual row counts
- `missing-index-detector` - Dedicated scoring and ranking of missing index opportunities
- `stored-procedure-analyzer` - Applies execution plan analysis to stored procedures
- `query-behavior-validator` - Validates that rewrites return identical results
