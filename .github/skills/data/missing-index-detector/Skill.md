---
name: missing-index-detector
description: Detects missing database indexes that cause slow queries or table scans, generating ready-to-execute CREATE INDEX statements with impact scores.
---

# Missing Index Detector

## Quick Example

**Input:** Slow query `SELECT * FROM Orders WHERE CustomerId = @id AND Status = 'Pending' ORDER BY CreatedDate`
**Output:** Missing composite index on (CustomerId, Status) INCLUDE (CreatedDate, TotalAmount) — estimated 96% improvement, CREATE INDEX statement generated
**Time:** 2-3 minutes

---

## Purpose
Detects missing database indexes that cause slow queries or table scans, generating ready-to-execute CREATE INDEX statements with impact scores.

## Input

```yaml
input:
  slow_query: <T-SQL query text>
  table_name: <primary table in the query>
  where_columns: <columns used in WHERE clause>
  order_by_columns: <columns used in ORDER BY>
  select_columns: <columns in SELECT — for INCLUDE determination>
  join_columns: <columns used in JOIN conditions>
  table_row_count: <approximate row count>
  existing_indexes: <optional — output of sp_helpindex or sys.indexes query>
```

## Output

```yaml
output:
  existing_index_analysis:
    - index_name: <name>
      covers_query: true|false
      reason_if_not_covering: <description>
  missing_indexes:
    - rank: <1-based priority>
      table: <name>
      key_columns: [<columns>]
      key_column_order_reason: <why this ordering>
      included_columns: [<columns>]
      included_column_reason: <why these are INCLUDEd not keyed>
      estimated_improvement_percent: <%>
      impact_score: <0-100>
      create_statement: <T-SQL CREATE INDEX>
      index_name_suggestion: <IX_Table_Column1_Column2>
  index_warnings:
    - warning: <DUPLICATE_INDEX|OVER_INDEXING|COVERING_ALREADY_EXISTS>
      description: <detail>
  write_impact:
    estimated_write_overhead: LOW|MEDIUM|HIGH
    reason: <explanation>
  confidence: HIGH|MEDIUM|LOW
```

## DO:
✅ Order key columns by selectivity (most selective first) then by query usage order
✅ Put filtered columns (WHERE equality) before range columns (WHERE BETWEEN, >, <)
✅ Use INCLUDE for SELECT-only columns — they don't need to be in the key
✅ Check existing indexes before recommending new ones — partial coverage may exist
✅ Estimate write impact — tables with frequent INSERTs/UPDATEs pay index maintenance cost

## DON'T:
❌ Recommend more than 3 new indexes per table — over-indexing hurts write performance
❌ Create composite indexes covering every possible query — balance with write cost
❌ Put low-selectivity columns (bit flags, status with 3 values) as leading key columns
❌ Include large text/binary columns in the index key — use INCLUDE or filter separately
❌ Ignore the existing clustered index key — columns in it are already available in any index

## Error Conditions

**IF table row count is unknown:**
```
1. Estimate from: SELECT COUNT(*) FROM <table>
2. Flag: ROW_COUNT_ESTIMATED — improvement estimates are approximate
```

**IF existing indexes are not provided:**
```
1. Request: EXEC sp_helpindex '<table_name>' or query sys.indexes
2. Proceed with detected missing indexes but flag: EXISTING_INDEXES_UNKNOWN
```

**IF query has dynamic WHERE (varies per execution):**
```
1. Recommend filtered index for most common filter values
2. Or recommend index on fixed columns + cover variable columns with INCLUDE
3. Flag: DYNAMIC_QUERY — single index may not cover all variants
```

## Processing Steps

1. **Query Parsing:** Extract: WHERE clause columns (equality vs range), JOIN condition columns, ORDER BY columns, SELECT column list. Identify which table each column belongs to.

2. **Existing Index Check:** Review existing indexes. For each WHERE column, check if it appears as a leading key column in any existing index. Note partial coverage.

3. **Selectivity Assessment:** Estimate column selectivity (cardinality/row_count). High selectivity (unique values) → good key column. Low selectivity (3 status values) → better as filter, not leading key.

4. **Index Design:** Compose candidate index: Key columns = equality WHERE columns (high selectivity first) + range WHERE columns + JOIN columns + ORDER BY columns. INCLUDE columns = remaining SELECT columns not in key.

5. **Impact Estimation:** For full table scan replacement: improvement ≈ 1 - (result_rows / table_rows). For key lookup elimination: improvement ≈ 20-40%. For sort elimination: improvement ≈ 10-30%.

6. **Write Impact Assessment:** Check if table has frequent writes (INSERT/UPDATE/DELETE). Number of key columns × write frequency = overhead indicator. LOW: <5 key columns, infrequent writes. HIGH: >8 columns, high write frequency.

7. **Index Name Generation:** Format: `IX_{Table}_{Col1}_{Col2}` for key columns. Truncate at 128 characters.

## Example

**Input:**
```yaml
slow_query: "SELECT Id, OrderDate, TotalAmount FROM Orders WHERE CustomerId = @cid AND Status = 'Pending' ORDER BY CreatedDate DESC"
table_name: Orders
where_columns: [CustomerId, Status]
order_by_columns: [CreatedDate]
select_columns: [Id, OrderDate, TotalAmount]
join_columns: []
table_row_count: 280000
existing_indexes: ["PK_Orders (Id)", "IX_Orders_CustomerId (CustomerId)"]
```

**Output:**
```yaml
existing_index_analysis:
  - index_name: "IX_Orders_CustomerId"
    covers_query: false
    reason_if_not_covering: "Covers CustomerId filter but not Status filter or CreatedDate sort — index scan then filter"
missing_indexes:
  - rank: 1
    table: Orders
    key_columns: [CustomerId, Status, CreatedDate]
    key_column_order_reason: "CustomerId (equality, high selectivity) → Status (equality, low sel but needed for sort) → CreatedDate (ORDER BY)"
    included_columns: [Id, OrderDate, TotalAmount]
    included_column_reason: "SELECT-only columns — no need in key, added as INCLUDE to avoid key lookup"
    estimated_improvement_percent: 96%
    impact_score: 94
    create_statement: "CREATE NONCLUSTERED INDEX IX_Orders_CustomerId_Status_CreatedDate ON Orders (CustomerId, Status, CreatedDate DESC) INCLUDE (Id, OrderDate, TotalAmount)"
    index_name_suggestion: "IX_Orders_CustomerId_Status_CreatedDate"
index_warnings: []
write_impact:
  estimated_write_overhead: MEDIUM
  reason: "Orders table has frequent inserts — 3-column key index adds moderate maintenance overhead"
confidence: HIGH
```

---

**Related Skills:**
- `sql-execution-plan-analyzer` - Provides execution plan input for missing index analysis
- `sql-execution-analyzer` - Full execution analysis to validate index recommendations
- `stored-procedure-analyzer` - Applies missing index detection to stored procedures
- `query-behavior-validator` - Validates that queries return same results after index creation
