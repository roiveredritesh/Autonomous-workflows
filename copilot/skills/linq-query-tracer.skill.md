# LINQ Query Tracer

## Purpose
Analyzes LINQ queries to understand SQL translation, identify performance issues, and ensure optimal data access patterns.

## Input

```yaml
query_location: <file and method>
linq_query: <LINQ expression or code>
context: <Entity Framework|LINQ to SQL|other>
performance_concern: <yes|no>
```

## Analysis Process

### 1. Parse LINQ Expression

**Identify:**
- Query type (select, join, group, etc.)
- Data source (DbSet, IQueryable)
- Filters (Where clauses)
- Projections (Select)
- Joins
- Ordering
- Pagination

### 2. Trace SQL Translation

**Determine what SQL will be generated:**

**LINQ Expression:**
```csharp
var customers = context.Customers
    .Where(c => c.Status == "Active")
    .OrderBy(c => c.Name)
    .Take(50);
```

**Translates to:**
```sql
SELECT TOP 50 *
FROM Customers
WHERE Status = 'Active'
ORDER BY Name
```

### 3. Detect Common Issues

**Issue Detection:**

**❌ N+1 Query Problem**
```csharp
// BAD: Generates N+1 queries
var customers = context.Customers.ToList();
foreach (var customer in customers)
{
    var orders = customer.Orders.ToList(); // Separate query per customer!
}
```

**✅ Fix with Eager Loading**
```csharp
// GOOD: Single query with join
var customers = context.Customers
    .Include(c => c.Orders)
    .ToList();
```

**❌ Client-Side Filtering**
```csharp
// BAD: Loads ALL data then filters in memory
var customers = context.Customers.ToList()
    .Where(c => c.Status == "Active");
```

**✅ Fix with Server-Side Filter**
```csharp
// GOOD: Filter on database
var customers = context.Customers
    .Where(c => c.Status == "Active")
    .ToList();
```

**❌ Missing Index Opportunity**
```csharp
// Query that scans entire table
var customers = context.Customers
    .Where(c => c.Email == "test@example.com")
    .ToList();
// If Email is not indexed → full table scan
```

**✅ Recommendation**
```sql
-- Add index
CREATE INDEX IX_Customers_Email ON Customers(Email)
```

### 4. Identify Performance Patterns

**Good Patterns:**
- ✅ Filters before ToList()
- ✅ Projection (Select) to reduce data
- ✅ Include for related data
- ✅ Pagination with Skip/Take

**Bad Patterns:**
- ❌ ToList() then LINQ operations
- ❌ Lazy loading in loops
- ❌ Select N+1
- ❌ Unnecessary includes

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

## Common Query Patterns

### Pattern 1: Simple Filter

**LINQ:**
```csharp
var active = context.Customers
    .Where(c => c.Status == "Active")
    .ToList();
```

**Analysis:**
```yaml
generated_sql: "SELECT * FROM Customers WHERE Status = 'Active'"
execution: database
issues: none
recommendation: "Consider projection if not all columns needed"
```

### Pattern 2: Join with Projection

**LINQ:**
```csharp
var result = context.Orders
    .Join(context.Customers,
        o => o.CustomerId,
        c => c.Id,
        (o, c) => new { o.OrderNumber, c.Name })
    .ToList();
```

**Analysis:**
```yaml
generated_sql: |
  SELECT o.OrderNumber, c.Name
  FROM Orders o
  INNER JOIN Customers c ON o.CustomerId = c.Id
execution: database
issues: none
performance: good (projection reduces data transfer)
```

### Pattern 3: N+1 Detection

**LINQ:**
```csharp
var customers = context.Customers.ToList();
foreach (var c in customers)
{
    Console.WriteLine(c.Orders.Count);
}
```

**Analysis:**
```yaml
issue: N+1_query_problem
severity: high
explanation: |
  Initial query: SELECT * FROM Customers
  Then for EACH customer: SELECT * FROM Orders WHERE CustomerId = {id}
  If 100 customers → 101 queries total
fix: |
  var customers = context.Customers
      .Include(c => c.Orders)
      .ToList();
expected_improvement: "99% reduction in database round trips"
```

### Pattern 4: Inefficient Exists Check

**LINQ:**
```csharp
var hasOrders = context.Orders
    .Where(o => o.CustomerId == customerId)
    .ToList()
    .Any();
```

**Analysis:**
```yaml
issue: inefficient_existence_check
severity: medium
explanation: "Loads all orders just to check existence"
generated_sql: "SELECT * FROM Orders WHERE CustomerId = @p0"
fix: |
  var hasOrders = context.Orders
      .Any(o => o.CustomerId == customerId);
fixed_sql: "SELECT CASE WHEN EXISTS(SELECT 1 FROM Orders WHERE CustomerId = @p0) THEN 1 ELSE 0 END"
improvement: "Load minimal data, early termination"
```

## LINQ to SQL Translation Rules

### Translated to SQL (Executes on Database)

✅ **Where** → WHERE clause
✅ **Select** → SELECT columns
✅ **OrderBy/ThenBy** → ORDER BY
✅ **Take/Skip** → TOP/OFFSET
✅ **Count()** → COUNT(*)
✅ **Any()** → EXISTS
✅ **First/Single** → TOP 1
✅ **Join/GroupJoin** → JOIN
✅ **GroupBy** → GROUP BY

### Executed in Memory (After ToList/ToArray)

❌ **After ToList()** → Everything after is client-side
❌ **Complex expressions** → May not translate
❌ **Method calls** → Unless known by provider
❌ **Custom functions** → Unless mapped

## Performance Impact Assessment

### High Impact Issues
```yaml
n_plus_one:
  impact: "Exponential with data volume"
  typical_slowdown: "10-100x slower"
  
full_table_scan:
  impact: "Linear with table size"
  typical_slowdown: "5-50x slower"
  
client_side_filtering:
  impact: "Loads unnecessary data"
  typical_slowdown: "2-20x slower"
```

### Medium Impact Issues
```yaml
missing_projection:
  impact: "Transfers unnecessary data"
  typical_slowdown: "1.5-5x slower"
  
unnecessary_ordering:
  impact: "Database sorting overhead"
  typical_slowdown: "1.2-3x slower"
```

## Index Analysis

### When to Recommend Index

**Recommend index if:**
- Column used in WHERE clause frequently
- Column used in JOIN condition
- Table is large (>10,000 rows)
- Query scans entire table

**Example:**
```yaml
query: "WHERE Email = @email"
recommendation:
  index: "CREATE INDEX IX_Customers_Email ON Customers(Email)"
  reason: "Email used in equality filter, likely unique lookups"
  impact: "Scan → Index seek (100x+ faster for large tables)"
```

### Index Types

**Clustered:**
- Primary key (usually)
- One per table
- Physical row order

**Non-Clustered:**
- Additional indexes
- Many per table
- Pointer to clustered key

**Composite:**
- Multiple columns
- Order matters
```sql
-- For: WHERE Status = 'Active' AND City = 'NYC'
CREATE INDEX IX_Customers_Status_City ON Customers(Status, City)
```

## Optimization Strategies

### Strategy 1: Eager Loading
```csharp
// Use Include for related data
.Include(c => c.Orders)
.Include(c => c.Address)
```

### Strategy 2: Projection
```csharp
// Select only needed columns
.Select(c => new { c.Name, c.Email })
```

### Strategy 3: Pagination
```csharp
// Limit result set
.Skip(pageSize * pageNumber)
.Take(pageSize)
```

### Strategy 4: AsNoTracking
```csharp
// For read-only queries
.AsNoTracking()
```

## Usage Example

```
SKILL: linq-query-tracer

INPUT:
  query_location: "CustomerRepository.cs, GetActiveCustomers()"
  linq_query: |
    var customers = _context.Customers.ToList()
        .Where(c => c.Status == "Active")
        .OrderBy(c => c.Name);
  performance_concern: yes

OUTPUT:
  query_trace:
    generated_sql: "SELECT * FROM Customers" // Note: ALL rows!
    execution_type: mixed // Database query, then in-memory filter/sort
  
  issues_detected:
    - issue: client_side_filtering
      severity: high
      location: ".Where(c => c.Status == 'Active')"
      explanation: "ToList() loads ALL customers, then filters in memory"
      performance_impact: "Loading 100,000 rows to filter to 5,000"
      fix: "Move Where() before ToList()"
    
    - issue: client_side_ordering
      severity: medium
      location: ".OrderBy(c => c.Name)"
      explanation: "Sorting 5,000 rows in memory instead of database"
      fix: "Move OrderBy() before ToList()"
  
  recommendations:
    - recommendation: "Optimize query to execute on database"
      code_example: |
        var customers = _context.Customers
            .Where(c => c.Status == "Active")
            .OrderBy(c => c.Name)
            .ToList();
      expected_improvement: "95% reduction (load only needed rows)"
  
  index_recommendations:
    - table: "Customers"
      columns: ["Status", "Name"]
      type: nonclustered
      reason: "Frequent filter on Status, ordering by Name"

  safe_to_execute: needs_optimization
  confidence: high
```

## Confidence Levels

**High:** Clear SQL translation, issues identified
**Medium:** Some ambiguity in translation
**Low:** Complex expression, needs testing to confirm
