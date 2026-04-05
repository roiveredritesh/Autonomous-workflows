---
name: data-model-explorer
description: Explores database schema relationships, constraints, and data model structure to understand table design before making code or schema changes.
---

# Data Model Explorer

## Quick Example

**Input:** `Orders` table
**Output:** 18 columns, FK to Customers (ON DELETE RESTRICT), FK to Carriers (nullable), cascade to OrderItems. No index on CustomerId+Status. 3 related entity classes in LINQ-to-SQL
**Time:** 2-4 minutes

---

## Purpose
Explores database schema relationships, constraints, and data model structure to understand table design before making code or schema changes.

## Input

```yaml
input:
  table_names: <list of table names to explore>
  entity_class_names: <optional — C# entity class names to cross-reference>
  include_related_tables: <true|false — auto-discover FK-related tables, default true>
  depth: <how many FK hops to follow, default 1>
  database_name: <SQL Server database name>
```

## Output

```yaml
output:
  tables:
    - name: <table name>
      schema: <dbo|etc>
      row_count_estimate: <count>
      columns:
        - name: <column name>
          data_type: <SQL type>
          nullable: true|false
          is_primary_key: true|false
          is_identity: true|false
          default_value: <value if any>
      indexes:
        - name: <index name>
          type: CLUSTERED|NONCLUSTERED|UNIQUE
          columns: [<list>]
          is_covering: true|false
      foreign_keys:
        - name: <FK name>
          column: <local column>
          references_table: <table>
          references_column: <column>
          on_delete: CASCADE|RESTRICT|SET_NULL|NO_ACTION
          on_update: CASCADE|RESTRICT|NO_ACTION
      check_constraints:
        - name: <constraint name>
          expression: <T-SQL expression>
      entity_class_mapping:
        class_name: <C# class>
        property_count: <count>
        unmapped_columns: [<columns in DB but not in entity>]
        unmapped_properties: [<properties in entity but not in DB>]
  relationships:
    - type: ONE_TO_MANY|MANY_TO_MANY|ONE_TO_ONE
      from_table: <table>
      to_table: <table>
      via_column: <FK column>
      description: <plain English relationship>
  schema_notes:
    - note: <observation about design — missing PK, no FK constraint, soft delete pattern, etc>
      severity: INFO|WARNING|CONCERN
  confidence: HIGH|MEDIUM|LOW
```

## DO:
✅ Check both the DB schema and the C# entity mapping for discrepancies
✅ Note soft-delete patterns (IsDeleted column) — they affect all query filters
✅ Identify tables with no foreign key constraints — data integrity risk
✅ Check for missing indexes on FK columns — common performance issue
✅ Note nullable FK columns — they indicate optional relationships

## DON'T:
❌ Modify any schema during exploration — read-only analysis only
❌ Assume entity class properties match DB columns — map explicitly and note gaps
❌ Ignore check constraints — they enforce business rules that code must respect
❌ Skip the row count — it affects index strategy and query planning
❌ Overlook computed columns — they may not be updatable

## Error Conditions

**IF table does not exist:**
```
1. Check schema prefix (dbo vs other schema)
2. Check if table was recently renamed or is in a different database
3. Return: TABLE_NOT_FOUND — verify table name and database context
```

**IF entity class is not found:**
```
1. Search for partial class name in LINQ-to-SQL .dbml or EF DbContext
2. Flag: ENTITY_NOT_FOUND — cross-reference may be incomplete
```

**IF database is not accessible:**
```
1. Request schema script: Information_Schema query or sp_help output
2. Return: DB_ACCESS_REQUIRED — provide CREATE TABLE scripts for analysis
```

## Processing Steps

1. **Schema Query:** Execute: `SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '<table>'`. Repeat for each table.

2. **Constraint Discovery:** Query `INFORMATION_SCHEMA.TABLE_CONSTRAINTS` and `INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS` for PKs, FKs, and check constraints. Map ON DELETE/UPDATE actions.

3. **Index Discovery:** Query `sys.indexes` and `sys.index_columns` for all indexes. Determine if clustered, unique, and what columns are included. Note covering vs non-covering.

4. **Row Count Estimate:** Query `sys.dm_db_partition_stats` for row count estimate. Flag as estimate to avoid locking production.

5. **Entity Class Mapping:** Find the C# entity class in the LINQ-to-SQL .dbml or EF code. Compare: DB columns vs entity properties. List unmapped on each side.

6. **Relationship Mapping:** From FK data, construct relationship descriptions: `Orders has many OrderItems (1:N, cascade delete)`. Identify junction tables for M:N.

7. **Schema Notes:** Flag: tables with no PK, nullable FK without corresponding entity navigation, missing index on FK column (JOIN performance), columns with no constraints on string length.

## Example

**Input:**
```yaml
table_names: [Orders]
entity_class_names: [Order]
include_related_tables: true
depth: 1
database_name: AajLogistics
```

**Output:**
```yaml
tables:
  - name: Orders
    schema: dbo
    row_count_estimate: 280000
    columns:
      - {name: Id, data_type: int, nullable: false, is_primary_key: true, is_identity: true}
      - {name: CustomerId, data_type: int, nullable: false, is_primary_key: false}
      - {name: Status, data_type: varchar(20), nullable: false, default_value: "'Pending'"}
      - {name: TotalAmount, data_type: decimal(18,2), nullable: false}
      - {name: CreatedDate, data_type: datetime, nullable: false}
      - {name: IsDeleted, data_type: bit, nullable: false, default_value: "0"}
    indexes:
      - {name: PK_Orders, type: CLUSTERED, columns: [Id], is_covering: false}
      - {name: IX_Orders_CustomerId, type: NONCLUSTERED, columns: [CustomerId], is_covering: false}
    foreign_keys:
      - {name: FK_Orders_Customers, column: CustomerId, references_table: Customers, references_column: Id, on_delete: RESTRICT, on_update: NO_ACTION}
    check_constraints:
      - {name: CK_Orders_Status, expression: "Status IN ('Pending','Processing','Shipped','Delivered','Cancelled')"}
    entity_class_mapping:
      class_name: Order
      property_count: 7
      unmapped_columns: []
      unmapped_properties: []
relationships:
  - {type: ONE_TO_MANY, from_table: Customers, to_table: Orders, via_column: CustomerId, description: "A Customer has many Orders"}
  - {type: ONE_TO_MANY, from_table: Orders, to_table: OrderItems, via_column: OrderId, description: "An Order has many OrderItems"}
schema_notes:
  - {note: "IsDeleted soft-delete pattern detected — all queries must filter WHERE IsDeleted = 0", severity: WARNING}
  - {note: "Missing index on Status column — filtered queries on Status will scan 280K rows", severity: CONCERN}
  - {note: "IX_Orders_CustomerId is not covering — key lookup needed for most queries", severity: WARNING}
confidence: HIGH
```

---

**Related Skills:**
- `sql-impact-analyzer` - Analyzes impact of schema changes on dependent queries and code
- `missing-index-detector` - Uses schema info to recommend missing indexes
- `dependency-mapper` - Maps code dependencies on tables and stored procedures
- `stored-procedure-analyzer` - Analyzes stored procedures that operate on these tables
