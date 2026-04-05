---
name: loop-optimization-scanner
description: Scans code for inefficient loop patterns including nested loops, LINQ queries inside loops, database calls inside loops, and redundant computations per iteration.
---

# Loop Optimization Scanner

## Quick Example

**Input:** `OrderProcessor.cs` — processes 500 orders in a foreach loop
**Output:** 3 issues found — DB call inside foreach (CRITICAL, 500 queries per batch), LINQ `.ToList()` inside nested loop (HIGH), `.Count()` called twice per iteration (LOW)
**Time:** 2-3 minutes

---

## Purpose
Scans code for inefficient loop patterns including nested loops, LINQ queries inside loops, database calls inside loops, and redundant computations per iteration.

## Input

```yaml
input:
  code_file_or_method: <file path or method name to scan>
  code_content: <optional — paste code directly for inline analysis>
  focus_areas: <optional — specific method names or line ranges>
  include_linq: <true|false — scan for LINQ inefficiencies, default true>
  include_db_calls: <true|false — scan for DB calls in loops, default true>
```

## Output

```yaml
output:
  issues_found:
    - issue_id: <L1..Ln>
      severity: CRITICAL|HIGH|MEDIUM|LOW
      pattern_type: DB_CALL_IN_LOOP|LINQ_IN_LOOP|NESTED_O_N2|REDUNDANT_COMPUTE|COUNT_IN_LOOP
      location: <file:line or method name>
      description: <what the code does>
      complexity: <O(n)|O(n²)|O(n×m)>
      estimated_impact: <ms per iteration at typical data volume>
      code_snippet: <problematic lines>
      fix_approach: <specific refactoring suggestion>
  summary:
    total_issues: <count>
    critical_count: <count>
    high_count: <count>
    estimated_total_waste_ms: <sum at typical data volume>
  refactoring_priority:
    - issue_id: <L1>
      reason: <why to fix first>
  confidence: HIGH|MEDIUM|LOW
```

## DO:
✅ Prioritize loops over large collections (>100 items) over small fixed sets
✅ Flag any repository method call or DbContext query inside a loop as CRITICAL
✅ Detect `.Count()` and `.Any()` calls that re-enumerate LINQ queries
✅ Identify nested loops with O(n²) or worse complexity
✅ Suggest batch operations as replacement for N+1 DB calls

## DON'T:
❌ Flag loops over small fixed sets (enums, config lists <10 items) as issues
❌ Penalize LINQ methods that are evaluated once (not inside loops)
❌ Suggest removing loops that iterate over user-controlled input without bounds
❌ Over-optimize loops that run infrequently (e.g., startup initialization)
❌ Conflate LINQ query definition with LINQ query execution

## Error Conditions

**IF code file is not accessible:**
```
1. Request file content as paste
2. Return: FILE_NOT_FOUND — provide code snippet for inline analysis
```

**IF code is minified or obfuscated:**
```
1. Cannot analyze without readable source
2. Return: UNREADABLE_CODE — decompile or obtain source for analysis
```

**IF method is too large (>500 lines):**
```
1. Scan for obvious patterns (foreach + repository call) at high level
2. Flag: LARGE_METHOD — consider splitting for better analyzability
```

## Processing Steps

1. **AST/Text Scan:** Parse file looking for loop constructs: `foreach`, `for`, `while`, `do-while`. Note loop variable type and estimated iteration count from collection name.

2. **DB Call Detection:** Inside each loop body, search for: repository method calls, DbContext queries, `ExecuteQuery`, `SqlCommand.Execute*`, LINQ expressions using `db.Table`. Flag any as CRITICAL.

3. **LINQ-in-Loop Detection:** Search for LINQ method chains (`.Where().Select().ToList()`) that appear inside loop bodies. Distinguish query definition (lazy) from query execution (`.ToList()`, `.First()`, `.Count()`).

4. **Nested Loop Analysis:** Detect loops containing loops. Calculate complexity: O(n²) for same-collection nested loops. Flag if inner collection size is not bounded.

5. **Redundant Computation Detection:** Inside loops, find: `.Count()` called multiple times on same collection, same property/method called repeatedly that doesn't change, string concatenation without StringBuilder.

6. **Impact Estimation:** Using typical data volumes (500 orders, 1000 customers), estimate: ms per DB call = 5-50ms, ms per LINQ re-evaluation = 1-10ms. Multiply by iteration count for total waste.

7. **Fix Suggestions:** DB call in loop → batch load before loop + dictionary lookup. LINQ in loop → materialize once before loop. Nested O(n²) → HashSet lookup or sorting. Redundant compute → extract to variable before loop.

## Example

**Input:**
```yaml
code_file_or_method: "D:\\Projects\\AajLogistics\\OrderProcessor.cs"
focus_areas: ["ProcessBatch", "CalculateTotals"]
```

**Output:**
```yaml
issues_found:
  - issue_id: L1
    severity: CRITICAL
    pattern_type: DB_CALL_IN_LOOP
    location: "OrderProcessor.cs:ProcessBatch:line 87"
    description: "CarrierRepository.GetById() called inside foreach over 500 orders"
    complexity: "O(n) DB calls"
    estimated_impact: "500 × 15ms = 7500ms per batch"
    code_snippet: |
      foreach (var order in orders) {
          var carrier = _carrierRepository.GetById(order.CarrierId); // DB call!
      }
    fix_approach: "Load all carriers once before loop: var carrierMap = _carrierRepository.GetByIds(orders.Select(o => o.CarrierId)).ToDictionary(c => c.Id);"
  - issue_id: L2
    severity: HIGH
    pattern_type: LINQ_IN_LOOP
    location: "OrderProcessor.cs:CalculateTotals:line 134"
    description: ".Where().Sum() re-evaluated for each order inside loop"
    complexity: "O(n²)"
    estimated_impact: "500 × 500 × 0.01ms = 2500ms"
    code_snippet: |
      foreach (var order in orders) {
          var total = lineItems.Where(li => li.OrderId == order.Id).Sum(li => li.Price);
      }
    fix_approach: "Group before loop: var byOrder = lineItems.GroupBy(li => li.OrderId).ToDictionary(g => g.Key, g => g.Sum(li => li.Price));"
  - issue_id: L3
    severity: LOW
    pattern_type: COUNT_IN_LOOP
    location: "OrderProcessor.cs:ProcessBatch:line 102"
    description: "orders.Count() called every iteration — re-enumerates IEnumerable"
    complexity: "O(n²) enumeration"
    estimated_impact: "Minimal at 500 items but bad pattern"
    code_snippet: "for (int i = 0; i < orders.Count(); i++)"
    fix_approach: "Cache count: var count = orders.Count(); for (int i = 0; i < count; i++)"
summary:
  total_issues: 3
  critical_count: 1
  high_count: 1
  estimated_total_waste_ms: 10000
refactoring_priority:
  - issue_id: L1
    reason: "7500ms savings — single batch load replaces 500 DB calls"
confidence: HIGH
```

---

**Related Skills:**
- `n-plus-one-detector` - Specifically detects N+1 patterns in LINQ-to-SQL and EF
- `linq-query-tracer` - Traces LINQ query execution and identifies inefficient patterns
- `performance-profiler` - Provides baselines showing total loop overhead in context
- `optimization-strategy-planner` - Plans the refactoring approach for detected issues
