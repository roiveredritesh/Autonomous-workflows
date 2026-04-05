---
name: stored-procedure-analyzer
description: Analyzes SQL Server stored procedures for performance issues, correctness, side effects, and dependencies to assess safety of modification or usage.
---

# Stored Procedure Analyzer

## Quick Example

**Input:** `usp_GetCustomerOrders` stored procedure
**Output:** 2 table scans (Orders, OrderItems), missing index on Orders.CustomerId+Status, implicit varchar→nvarchar conversion blocking index, side effect: updates LastAccessed column — not idempotent
**Time:** 3-5 minutes

---

## Purpose
Analyzes SQL Server stored procedures for performance issues, correctness, side effects, and dependencies to assess safety of modification or usage.

## Input

```yaml
input:
  stored_procedure_name: <usp_ProcedureName or full T-SQL code>
  database_name: <SQL Server database name>
  sample_parameters: <optional — representative parameter values for plan analysis>
  check_side_effects: <true|false — check for UPDATE/INSERT/DELETE within proc, default true>
```

## Output

```yaml
output:
  procedure_summary:
    name: <name>
    parameter_count: <count>
    parameters:
      - name: <@param>
        type: <SQL type>
        direction: INPUT|OUTPUT
        default_value: <if any>
    estimated_lines: <count>
    has_transaction: true|false
    has_error_handling: true|false
    recompile_hint: true|false
  side_effects:
    reads_tables: [<list>]
    writes_tables: [<list>]
    is_idempotent: true|false
    side_effect_details: [<description of each write>]
  performance_issues:
    - issue: <description>
      severity: CRITICAL|HIGH|MEDIUM|LOW
      table: <affected table>
      recommendation: <fix>
  dependencies:
    tables: [<list>]
    other_procedures: [<list>]
    functions: [<list>]
  parameter_sniffing_risk: true|false
  parameter_sniffing_detail: <explanation if risk exists>
  missing_indexes:
    - table: <name>
      columns: [<list>]
      create_statement: <T-SQL>
  recommendations:
    - action: <description>
      priority: critical|high|medium
  confidence: HIGH|MEDIUM|LOW
```

## DO:
✅ Check for side effects (writes) — procedures called as "reads" may silently write
✅ Verify error handling — unhandled exceptions in SP leave transactions open
✅ Test for parameter sniffing by running with different parameter values
✅ Check for implicit type conversions in WHERE clauses
✅ Verify if SP is called in transaction context from application code

## DON'T:
❌ Assume SPs are read-only without checking for UPDATE/INSERT/DELETE
❌ Ignore OPTION (RECOMPILE) — it prevents plan caching but may be intentional
❌ Overlook dynamic SQL inside SPs — it bypasses plan cache and may have injection risk
❌ Skip transaction analysis — unterminated transactions cause blocking
❌ Miss cursors — they're often a performance anti-pattern that loops should replace

## Error Conditions

**IF stored procedure does not exist:**
```
1. Check schema prefix: EXEC dbo.usp_ProcedureName vs EXEC usp_ProcedureName
2. Search sys.procedures for partial name match
3. Return: PROC_NOT_FOUND — verify name and database context
```

**IF procedure uses dynamic SQL:**
```
1. Extract and analyze the dynamic SQL strings
2. Flag: DYNAMIC_SQL — execution plan varies; parameter injection risk if user input used
```

**IF procedure is very long (>300 lines):**
```
1. Analyze top-level structure and most expensive operations
2. Flag: LARGE_PROC — full analysis may require manual review of specific sections
```

## Processing Steps

1. **SP Retrieval:** Execute `sp_helptext '<proc_name>'` or `OBJECT_DEFINITION(OBJECT_ID('<proc_name>'))` to get full T-SQL. Parse parameters from CREATE PROCEDURE signature.

2. **Side Effect Analysis:** Scan for DML statements: UPDATE, INSERT, DELETE, MERGE, TRUNCATE. Record which tables are affected. Check if writes are conditional or always executed. Assess idempotency.

3. **Error Handling Check:** Look for TRY/CATCH blocks. Check if CATCH re-throws or swallows error. Verify ROLLBACK is called on error. Flag missing error handling.

4. **Transaction Analysis:** Look for BEGIN TRANSACTION / COMMIT / ROLLBACK. Verify all code paths reach COMMIT or ROLLBACK. Check for nested transactions (SAVE TRANSACTION).

5. **Performance Analysis:** Apply `sql-execution-plan-analyzer` logic to each major query within the SP. Look for: table scans, cursor usage, WHILE loops with DML, N+1 subqueries in loop.

6. **Parameter Sniffing Assessment:** Identify parameters used in WHERE clauses with high selectivity variance (date ranges, optional filters). Assess if plan cached for one parameter set would be wrong for another. Check for OPTION (RECOMPILE) or local variable workaround.

7. **Dependency Mapping:** Parse all table references and EXEC calls to other procedures. Build dependency list.

## Example

**Input:**
```yaml
stored_procedure_name: "usp_GetCustomerOrders"
database_name: AajLogistics
sample_parameters: {"@CustomerId": 12345, "@StatusFilter": "Pending"}
check_side_effects: true
```

**Output:**
```yaml
procedure_summary:
  name: "usp_GetCustomerOrders"
  parameter_count: 3
  parameters:
    - {name: "@CustomerId", type: "int", direction: INPUT}
    - {name: "@StatusFilter", type: "varchar(20)", direction: INPUT, default_value: "NULL"}
    - {name: "@RowCount", type: "int", direction: OUTPUT}
  estimated_lines: 45
  has_transaction: false
  has_error_handling: false
  recompile_hint: false
side_effects:
  reads_tables: [Orders, Customers, OrderItems]
  writes_tables: [CustomerActivityLog]
  is_idempotent: false
  side_effect_details: ["Inserts a row into CustomerActivityLog on every call — unexpected side effect for a 'get' procedure"]
performance_issues:
  - issue: "Table scan on Orders — Status filter uses varchar but column is nvarchar causing implicit conversion"
    severity: CRITICAL
    table: Orders
    recommendation: "Change @StatusFilter to nvarchar(20) or cast column, or fix data type mismatch"
  - issue: "No error handling — exceptions will bubble up with open connections"
    severity: HIGH
    table: null
    recommendation: "Wrap in TRY/CATCH and close connections properly"
dependencies:
  tables: [Orders, Customers, OrderItems, CustomerActivityLog]
  other_procedures: []
  functions: []
parameter_sniffing_risk: false
missing_indexes:
  - table: Orders
    columns: [CustomerId, Status]
    create_statement: "CREATE INDEX IX_Orders_CustomerId_Status ON Orders (CustomerId, Status)"
recommendations:
  - action: "Fix implicit conversion: change @StatusFilter from varchar(20) to nvarchar(20)"
    priority: critical
  - action: "Remove CustomerActivityLog INSERT from GET procedure — side effects belong in a separate audit procedure"
    priority: high
  - action: "Add TRY/CATCH with proper error logging"
    priority: high
confidence: HIGH
```

---

**Related Skills:**
- `sql-execution-plan-analyzer` - Analyzes execution plans of queries within stored procedures
- `sql-execution-analyzer` - Full analysis of individual queries found in the SP
- `missing-index-detector` - Detects missing indexes on tables the SP accesses
- `data-model-explorer` - Explores the tables the SP depends on
