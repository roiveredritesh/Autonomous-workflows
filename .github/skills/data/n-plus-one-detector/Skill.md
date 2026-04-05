---
name: n-plus-one-detector
description: Detects N+1 query patterns in LINQ-to-SQL or Entity Framework code where a collection is loaded and then each item triggers an additional lazy-load query.
---

# N+1 Query Detector

## Quick Example

**Input:** `OrderListPage.aspx.cs` — loads orders then accesses `order.Customer.Name` in a loop
**Output:** N+1 detected — 1 query to load 200 orders + 200 individual Customer queries = 201 queries. Fix: `.Include(o => o.Customer)` or DataLoadOptions in LINQ-to-SQL
**Time:** 2-3 minutes

---

## Purpose
Detects N+1 query patterns in LINQ-to-SQL or Entity Framework code where a collection is loaded and then each item triggers an additional lazy-load query.

## Input

```yaml
input:
  code_file: <file path to .cs file to analyze>
  code_content: <optional — paste code directly>
  linq_context: LINQ_TO_SQL|ENTITY_FRAMEWORK|BOTH
  datacontext_name: <optional — name of DataContext or DbContext class>
  typical_collection_size: <approximate number of items typically loaded>
```

## Output

```yaml
output:
  n_plus_one_patterns:
    - pattern_id: <N1..Nn>
      severity: CRITICAL|HIGH|MEDIUM
      location: <file:method:line>
      trigger_query: <the initial collection query>
      lazy_load_trigger: <the navigation property or method causing extra queries>
      queries_per_load: <1 + N where N is collection size>
      estimated_total_queries: <at typical_collection_size>
      estimated_total_time_ms: <at 5ms per query>
      code_snippet: <problematic code>
      fix_approach: INCLUDE|DATALOADOPTIONS|BATCH_LOAD|MANUAL_JOIN
      fix_example: <corrected code snippet>
  summary:
    total_patterns: <count>
    worst_case_queries_per_request: <sum of all patterns>
    estimated_worst_case_ms: <sum>
  confidence: HIGH|MEDIUM|LOW
```

## DO:
✅ Check all navigation property accesses inside loops or LINQ projections
✅ Look for `.Select(x => x.NavigationProperty)` patterns — deferred N+1
✅ Detect LINQ-to-SQL `DataLoadOptions` usage (or absence) on DataContext
✅ Find Entity Framework `.Include()` calls that are missing on loaded queries
✅ Check for lazy-load in WebForms GridView/ListView DataBound events

## DON'T:
❌ Flag navigation property access outside of loop context — may be single query
❌ Report patterns where `.Include()` or `DataLoadOptions` is already present
❌ Ignore deferred execution — LINQ queries in `Select()` may execute per-item
❌ Assume all lazy loads are bad — single-item detail pages may be acceptable
❌ Confuse eager loading with over-fetching — Include is not always the right fix

## Error Conditions

**IF code uses dynamic DataContext or late binding:**
```
1. Look for DataContext.GetTable<T>() patterns
2. Trace navigation property type to find related table
3. Flag: DYNAMIC_CONTEXT — N+1 analysis may be incomplete
```

**IF code uses stored procedures for all queries:**
```
1. N+1 pattern unlikely if using stored procs directly
2. Check for LINQ wrapping around SP results
3. Return: NO_ORM_DETECTED — N+1 not applicable to stored procedure pattern
```

**IF collection size is unknown:**
```
1. Use conservative estimate of 100 items
2. Flag: SIZE_ESTIMATED — actual query count may differ
```

## Processing Steps

1. **ORM Detection:** Identify LINQ-to-SQL (DataContext, Table<T>, EntityRef) or Entity Framework (DbContext, DbSet, IQueryable) patterns in the file.

2. **Collection Load Detection:** Find all LINQ queries that return IQueryable<T>, List<T>, or IEnumerable<T> collections. Record the entity type and query location.

3. **Loop/Projection Scan:** For each collection, scan the body of: foreach loops, for loops, .Select() projections, GridView/RadGrid DataBound events. Look for navigation property access (`order.Customer`, `item.Product.Price`).

4. **N+1 Classification:** If navigation property accessed N times (once per item) without prior Include/DataLoadOptions → N+1 confirmed. Calculate: total queries = 1 (collection) + N (per-item).

5. **Deferred Execution Check:** Check if lazy load happens inside a LINQ projection that's deferred — the N queries may execute at serialization time, not immediately. Flag if in RadGrid DataSource.

6. **Fix Determination:** LINQ-to-SQL → use DataLoadOptions.LoadWith. Entity Framework → use .Include(). Both → alternatively, batch load related entities separately and use dictionary lookup.

7. **Fix Example Generation:** Provide concrete corrected code showing either Include/DataLoadOptions addition or the batch load + dictionary pattern.

## Example

**Input:**
```yaml
code_file: "D:\\Projects\\AajLogistics\\Orders\\OrderListPage.aspx.cs"
linq_context: LINQ_TO_SQL
datacontext_name: AajLogisticsDataContext
typical_collection_size: 200
```

**Output:**
```yaml
n_plus_one_patterns:
  - pattern_id: N1
    severity: CRITICAL
    location: "OrderListPage.aspx.cs:BindGrid:line 68"
    trigger_query: "var orders = db.Orders.Where(o => o.Status == 'Pending').ToList()"
    lazy_load_trigger: "order.Customer.CompanyName — EntityRef lazy load per order"
    queries_per_load: "1 + 200"
    estimated_total_queries: 201
    estimated_total_time_ms: 1005
    code_snippet: |
      var orders = db.Orders.Where(o => o.Status == "Pending").ToList();
      foreach (var order in orders) {
          row["Customer"] = order.Customer.CompanyName; // lazy load!
      }
    fix_approach: DATALOADOPTIONS
    fix_example: |
      var opts = new DataLoadOptions();
      opts.LoadWith<Order>(o => o.Customer);
      db.LoadOptions = opts;
      var orders = db.Orders.Where(o => o.Status == "Pending").ToList();
  - pattern_id: N2
    severity: HIGH
    location: "OrderListPage.aspx.cs:BindGrid:line 70"
    trigger_query: "Same orders collection"
    lazy_load_trigger: "order.OrderItems — EntitySet lazy load per order"
    queries_per_load: "200"
    estimated_total_queries: 200
    estimated_total_time_ms: 1000
    fix_approach: DATALOADOPTIONS
    fix_example: "opts.LoadWith<Order>(o => o.OrderItems); // add to same DataLoadOptions"
summary:
  total_patterns: 2
  worst_case_queries_per_request: 401
  estimated_worst_case_ms: 2005
confidence: HIGH
```

---

**Related Skills:**
- `linq-query-tracer` - Traces full LINQ query execution and generated SQL
- `loop-optimization-scanner` - Scans for DB calls inside loops (related pattern)
- `sql-execution-analyzer` - Analyzes the SQL generated by each lazy-load query
- `performance-profiler` - Validates improvement after applying N+1 fixes
