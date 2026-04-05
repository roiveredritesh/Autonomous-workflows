---
name: optimization-strategy-planner
description: Plans performance optimization strategy by selecting the highest ROI approaches ordered by expected improvement, implementation risk, and complexity.
---

# Optimization Strategy Planner

## Quick Example

**Input:** Customer search bottleneck: 7800ms DB query, missing index on Status, 0% cache hit rate, risk: LOW
**Output:** 3 optimization approaches ranked by ROI — (1) Add index: 94% improvement, (2) Cache results: 95% further improvement, (3) Pagination: UX improvement. Start with index (highest ROI, lowest risk)
**Time:** 3-5 minutes

---

## Purpose
Plans performance optimization strategy by selecting the highest ROI approaches ordered by expected improvement, implementation risk, and complexity.

## Input

```yaml
input:
  bottleneck_identified: <description of what is slow and where>
  current_baseline_ms: <measured current performance>
  target_metric_ms: <desired performance goal>
  risk_tolerance: LOW|MEDIUM|HIGH
  available_approaches: <optional — list of approaches already identified>
  constraints: <optional — cannot change DB schema, cannot add Redis, etc>
```

## Output

```yaml
output:
  strategy_summary:
    baseline_ms: <current>
    target_ms: <goal>
    gap_ms: <to close>
    feasibility: ACHIEVABLE|STRETCH|UNLIKELY
    required_approaches_count: <how many optimizations needed>
  approaches:
    - rank: <1-based>
      name: <approach name>
      type: QUERY_OPTIMIZATION|INDEX|CACHING|PAGINATION|EAGER_LOADING|BATCH_LOAD|VIEWSTATE|CODE_CHANGE
      description: <what to do>
      expected_improvement_ms: <ms saved>
      expected_improvement_percent: <%>
      risk: LOW|MEDIUM|HIGH
      complexity: LOW|MEDIUM|HIGH
      effort_days: <days>
      dependencies: [<prerequisite approaches or infrastructure>]
      trade_offs: [<what is given up>]
  recommended_sequence:
    - phase: <1..n>
      approach: <approach name>
      cumulative_improvement_ms: <total ms saved after this phase>
      cumulative_improvement_percent: <%>
      checkpoint: <validate here before proceeding>
  roi_analysis:
    - approach: <name>
      roi_score: <improvement_ms / effort_days>
      recommendation: DO_FIRST|DO_NEXT|CONSIDER|SKIP
  confidence: HIGH|MEDIUM|LOW
```

## DO:
✅ Rank approaches by ROI (improvement / effort) — quick wins first
✅ Consider approaches that compound (index enables caching to be effective)
✅ Account for risk tolerance — LOW tolerance means low-risk approaches only, even if lower ROI
✅ Include realistic effort estimates — underestimating leads to abandoned optimizations
✅ Plan checkpoints between phases — verify improvement before next phase

## DON'T:
❌ Plan more than 3-4 optimization phases — diminishing returns and project risk
❌ Recommend caching before fixing the underlying query — cache an efficient query
❌ Ignore data correctness — never sacrifice correctness for performance
❌ Include speculative optimizations without evidence of need
❌ Skip trade-off analysis — all optimizations have costs

## Error Conditions

**IF baseline is not measurable:**
```
1. Cannot plan optimization without baseline
2. Return: BASELINE_REQUIRED — use performance-profiler first to establish measurable baseline
```

**IF target is not achievable with any known approach:**
```
1. Flag: TARGET_UNREALISTIC
2. Present best achievable improvement with all approaches combined
3. Recommend revising target or adding infrastructure (more powerful server, read replicas)
```

**IF all approaches have HIGH risk and risk tolerance is LOW:**
```
1. Recommend spike investigation for lower-risk approaches
2. Flag: HIGH_RISK_ONLY — no LOW-risk optimization available with current constraints
```

## Processing Steps

1. **Gap Analysis:** Calculate gap = baseline_ms - target_ms. Assess if gap is achievable: typically achievable in 1-3 optimization phases. Flag STRETCH if >90% improvement needed.

2. **Approach Identification:** Based on bottleneck type — DB query: index, query rewrite, SP, eager load, pagination. Cache: Redis cache, memory cache, output cache. Code: loop optimization, batch load, ViewState reduction.

3. **ROI Calculation:** For each approach: ROI = expected_improvement_ms / effort_days. Higher score = do first. Adjust for risk: HIGH risk approaches get ROI multiplied by 0.5 (uncertainty discount).

4. **Sequence Design:** Phase 1: highest ROI, lowest risk (quick wins). Phase 2: medium complexity, high impact. Phase 3: complex but necessary for target. Include checkpoint after each phase.

5. **Dependency Mapping:** Some approaches depend on others: index before caching (caching a slow query is less effective). Code fix before profiling for further improvements.

6. **Trade-off Analysis:** For each approach: what does it cost? Index → slower writes. Caching → stale data risk. Pagination → UX change. Batch load → more complex code. Document these explicitly.

7. **Feasibility Assessment:** Sum expected improvements of recommended phases. If sum >= gap: ACHIEVABLE. If sum = 70-100% of gap: STRETCH. If sum < 70% of gap: UNLIKELY — escalate to infrastructure or architectural changes.

## Example

**Input:**
```yaml
bottleneck_identified: "CustomerRepository.GetByFilter() — 7800ms DB query, SELECT * on 45K rows, no index on Status"
current_baseline_ms: 8200
target_metric_ms: 400
risk_tolerance: LOW
```

**Output:**
```yaml
strategy_summary:
  baseline_ms: 8200
  target_ms: 400
  gap_ms: 7800
  feasibility: ACHIEVABLE
  required_approaches_count: 2
approaches:
  - rank: 1
    name: "Add index on Customers.Status"
    type: INDEX
    description: "CREATE NONCLUSTERED INDEX IX_Customers_Status ON Customers (Status) INCLUDE (Id, Name, Email)"
    expected_improvement_ms: 7300
    expected_improvement_percent: 89%
    risk: LOW
    complexity: LOW
    effort_days: 0.5
    dependencies: []
    trade_offs: ["Slight overhead on INSERT/UPDATE to Customers (minimal — low write frequency)"]
  - rank: 2
    name: "Move LINQ WHERE before ToList()"
    type: QUERY_OPTIMIZATION
    description: "Change .ToList().Where() to .Where().ToList() to push filter to SQL"
    expected_improvement_ms: 400
    expected_improvement_percent: 5%
    risk: LOW
    complexity: LOW
    effort_days: 0.25
    dependencies: []
    trade_offs: ["None — strictly better"]
  - rank: 3
    name: "Cache filtered results in Redis"
    type: CACHING
    description: "Cache search results in Redis with 5-minute TTL after index optimization"
    expected_improvement_ms: 350
    expected_improvement_percent: 4%
    risk: LOW
    complexity: MEDIUM
    effort_days: 1
    dependencies: ["Approach 1 — cache only after query is fast"]
    trade_offs: ["Results may be up to 5 minutes stale", "Additional Redis infrastructure usage"]
recommended_sequence:
  - phase: 1
    approach: "Move LINQ WHERE before ToList()"
    cumulative_improvement_ms: 400
    cumulative_improvement_percent: 5%
    checkpoint: "Measure query time — should drop to ~1400ms (filter now in DB)"
  - phase: 2
    approach: "Add index on Customers.Status"
    cumulative_improvement_ms: 7700
    cumulative_improvement_percent: 94%
    checkpoint: "Measure page load — should be <500ms (7800ms → <500ms)"
  - phase: 3
    approach: "Cache filtered results in Redis"
    cumulative_improvement_ms: 8050
    cumulative_improvement_percent: 98%
    checkpoint: "Measure hit rate — target >70% after warm-up"
roi_analysis:
  - {approach: "Move LINQ WHERE", roi_score: 1600, recommendation: DO_FIRST}
  - {approach: "Add index", roi_score: 14600, recommendation: DO_FIRST}
  - {approach: "Cache results", roi_score: 350, recommendation: DO_NEXT}
confidence: HIGH
```

---

**Related Skills:**
- `performance-profiler` - Provides the baseline metrics used as input
- `performance-implementation-planner` - Creates the detailed implementation plan for this strategy
- `performance-validation-planner` - Plans validation approach after each optimization phase
- `missing-index-detector` - Provides index recommendations for query optimization approaches
