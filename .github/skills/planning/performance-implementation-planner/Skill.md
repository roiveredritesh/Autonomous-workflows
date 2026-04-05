---
name: performance-implementation-planner
description: Creates a phased implementation plan for performance optimizations ordered low risk to high impact, with rollback procedures per phase.
---

# Performance Implementation Planner

## Quick Example

**Input:** Strategy: Add index + fix LINQ WHERE + cache results, 3 files to change, risk LOW/LOW/MEDIUM
**Output:** 2-phase plan — Phase 1 (quick wins, no risk): fix LINQ WHERE in 30min. Phase 2 (index + cache): DBA creates index, developer adds caching in 4 hours. Rollback per phase documented.
**Time:** 2-3 minutes

---

## Purpose
Creates a phased implementation plan for performance optimizations ordered low risk to high impact, with rollback procedures per phase.

## Input

```yaml
input:
  optimization_strategy: <output from optimization-strategy-planner or description>
  files_to_change: <list of files and what changes are needed>
  risk_per_optimization: <LOW|MEDIUM|HIGH per change>
  team_available: <hours available for implementation>
  deployment_window: <when the changes can be deployed>
```

## Output

```yaml
output:
  implementation_phases:
    - phase: <1..n>
      name: <phase name>
      objective: <what this phase achieves>
      changes:
        - file: <file path>
          change_type: CODE|SQL|CONFIG|INFRASTRUCTURE
          description: <what to change>
          estimated_hours: <hours>
          risk: LOW|MEDIUM|HIGH
          code_example:
            before: <snippet>
            after: <snippet>
      testing_required:
        - test: <specific test to run>
          type: UNIT|INTEGRATION|SMOKE|PERFORMANCE
      rollback:
        method: GIT_REVERT|FEATURE_FLAG|DB_ROLLBACK|CONFIG_CHANGE
        steps: [<exact steps>]
        estimated_rollback_minutes: <n>
      success_criteria:
        - metric: <what to measure>
          target: <value>
          how_to_measure: <specific measurement method>
  total_implementation:
    total_hours: <sum>
    total_files_changed: <count>
    deployment_recommendation: <sequential|parallel>
  confidence: HIGH|MEDIUM|LOW
```

## DO:
✅ Order phases by risk: lowest risk changes first — validate before higher risk
✅ Keep each phase independently deployable — don't require all phases to be deployed together
✅ Provide exact before/after code snippets for each code change
✅ Include performance measurements between phases — verify improvement before next phase
✅ Make rollback explicit and fast — each phase should roll back in <10 minutes

## DON'T:
❌ Combine high-risk and low-risk changes in one phase — keep them separate
❌ Plan phases that depend on each other being deployed simultaneously
❌ Omit rollback procedure for any phase
❌ Include refactoring in performance phases — separate concerns
❌ Estimate hours without accounting for testing and deployment time

## Error Conditions

**IF all changes HIGH risk:** Break into smallest units, add spike phase, wrap each in feature flag.
**IF files not accessible:** Create plan from strategy with placeholder; flag FILES_NOT_REVIEWED.

## Processing Steps

1. Sort changes by risk: LOW → Phase 1, MEDIUM → Phase 2, HIGH → Phase 3; within group by ROI then dependencies.
2. Each phase: name, objective, list of changes with code examples, testing, rollback, success criteria.
3. Code examples: show before (3-5 lines) and after (changed state); keep focused on the change.
4. Testing: unit tests for changed methods, integration/smoke for affected page, performance measurement.
5. Rollback: GIT_REVERT (code), DB_ROLLBACK (drop index), CONFIG_CHANGE (revert settings); estimate time.
6. Deploy sequentially with 24h between phases if independent; rapid succession if phases compound.

## Example

**Input:**
```yaml
optimization_strategy: "Phase 1: Fix LINQ WHERE. Phase 2: Add index on Status. Phase 3: Add Redis cache."
files_to_change:
  - {file: "CustomerRepository.cs", change: "Move .Where() before .ToList()", risk: LOW}
  - {file: "SQL: Customers table", change: "CREATE INDEX IX_Customers_Status", risk: LOW}
  - {file: "CustomerService.cs", change: "Add Redis cache for search results", risk: MEDIUM}
team_available: 8
deployment_window: "2026-04-06 off-peak 22:00-02:00"
```

**Output:**
```yaml
implementation_phases:
  - phase: 1
    name: "LINQ Query Fix (Quick Win)"
    objective: "Move filtering to DB — estimated 5% improvement, validates approach"
    changes:
      - file: "CustomerRepository.cs"
        change_type: CODE
        description: "Move .Where() before .ToList() to filter in SQL not memory"
        estimated_hours: 0.5
        risk: LOW
        code_example:
          before: |
            var customers = _db.Customers.ToList()
                .Where(c => c.Status == filter.Status)
                .OrderBy(c => c.Name)
                .ToList();
          after: |
            var customers = _db.Customers
                .Where(c => c.Status == filter.Status)
                .OrderBy(c => c.Name)
                .ToList();
    testing_required:
      - {test: "CustomerRepository_GetByFilter_ReturnsCorrectResults", type: UNIT}
      - {test: "Customer search returns correct filtered results in staging", type: SMOKE}
    rollback:
      method: GIT_REVERT
      steps: ["git revert <commit>", "deploy reverted version"]
      estimated_rollback_minutes: 10
    success_criteria:
      - {metric: "Customer search response time", target: "<1500ms", how_to_measure: "MiniProfiler in staging"}
  - phase: 2
    name: "Database Index (Primary Optimization)"
    objective: "Add covering index — estimated 89% improvement"
    changes:
      - file: "SQL Server: Customers table"
        change_type: SQL
        description: "Add index on Status with INCLUDE columns"
        estimated_hours: 0.5
        risk: LOW
        code_example:
          before: "-- No index on Status column"
          after: "CREATE NONCLUSTERED INDEX IX_Customers_Status ON Customers (Status) INCLUDE (Id, Name, Email, Region)"
    testing_required:
      - {test: "Customer search response time <500ms with 45K records", type: PERFORMANCE}
      - {test: "Customer INSERT/UPDATE performance not significantly degraded", type: PERFORMANCE}
    rollback:
      method: DB_ROLLBACK
      steps: ["DROP INDEX IX_Customers_Status ON Customers"]
      estimated_rollback_minutes: 2
    success_criteria:
      - {metric: "Customer search P95 response time", target: "<500ms", how_to_measure: "Application Insights after deploy"}
  - phase: 3
    name: "Redis Caching (Final Optimization)"
    objective: "Cache frequent search results — estimated 95% cache hit rate"
    changes:
      - file: "CustomerService.cs"
        change_type: CODE
        description: "Add cache-aside pattern for search results with 5-min TTL"
        estimated_hours: 3
        risk: MEDIUM
        code_example:
          before: "return _customerRepository.GetByFilter(filter);"
          after: |
            var cacheKey = $"customer:search:{filter.Status}:{filter.Region}";
            return _cache.GetOrSet(cacheKey, () => _customerRepository.GetByFilter(filter), TimeSpan.FromMinutes(5));
    testing_required:
      - {test: "Cache hit returns correct results", type: INTEGRATION}
      - {test: "Cache miss falls back to DB correctly", type: INTEGRATION}
      - {test: "Cache invalidation works on customer update", type: INTEGRATION}
    rollback:
      method: FEATURE_FLAG
      steps: ["Set CacheCustomerSearch=false in AppSettings", "Recycle app pools"]
      estimated_rollback_minutes: 5
    success_criteria:
      - {metric: "Cache hit rate", target: ">70% after 10 minute warmup", how_to_measure: "Redis INFO stats"}
      - {metric: "Customer search P95 response time", target: "<100ms for cache hits", how_to_measure: "Application Insights"}
total_implementation:
  total_hours: 4
  total_files_changed: 2
  deployment_recommendation: "Sequential — Phase 1, validate, then Phase 2 (off-peak with DBA), then Phase 3 next day"
confidence: HIGH
```

---

**Related Skills:**
- `optimization-strategy-planner` - Provides the strategy that this skill turns into an implementation plan
- `performance-validation-planner` - Plans validation testing after each phase
- `safe-change-boundary-detector` - Validates each phase stays within safe boundaries
- `rollback-plan-generator` - Generates detailed rollback documentation per phase
