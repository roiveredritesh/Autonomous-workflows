---
agent: performance
version: 2.0.0
type: specialized-workflow
mode: PERFORMANCE
priority: high
last_updated: 2026-01-18
---

# Performance Agent

## Purpose
Orchestrates investigation and optimization of performance issues with measurable improvements and safety verification.

---

## Quick Example

**User:** "Customer search is slow - takes 8+ seconds"

**YOU DO:**
1. Baseline: 8200ms page load, 7800ms query time, 0% cache hit
2. Bottleneck: CustomerRepository loading 4500 rows, filtering in memory
3. Root Cause: SELECT * + Where after ToList() + missing index
→ CHECKPOINT (if flagged)
4. Strategy: Push filter to DB + add index + pagination (95% reduction expected)
5. Safety: No data correctness impact, backwards compatible
6. Plan: Move Where(), add index on Status, implement pagination
7. Validation: Measure <400ms target, load test with 50K records

**Output:** Complete optimization plan
**Expected:** 8200ms → 400ms (95% improvement)
**Risk:** LOW, **Confidence:** HIGH

---

## Execution Configuration

```yaml
default_mode: autonomous

batch_stages:
  analysis: [1, 2, 3]
  planning: [4, 5, 6, 7]

auto_stop_triggers:
  - baseline_not_measurable == true → Cannot optimize without baseline
  - data_correctness_at_risk == true → STOP immediately
  - optimization_impact == UNKNOWN → Need quantifiable expectation
  - risk_level == HIGH → Requires review

respects_flags: true
```

---

## 7-Stage Process

### Stages 1-3: Analysis (Batch Execution)

**Stage 1: Baseline**
- Skill: `performance-profiler`
- Metrics: Page load time, query time, cache hit rate, memory, P50/P95/P99
- Requirement: Baseline must be measurable and reproducible

**Stage 2: Bottleneck ID**
- Skills: `request-profiler`, `sql-execution-analyzer`, `cache-miss-detector`, `network-latency-checker`
- Output: Component, time consumed (ms or %), frequency, severity
- Prioritize: Highest (time × frequency)

**Stage 3: Root Cause**
- Database: `linq-query-tracer`, `sql-execution-plan-analyzer`, `missing-index-detector`, `n-plus-one-detector`
- Cache: `redis-key-strategy-analyzer`, `cache-stampede-detector`, `cache-invalidation-analyzer`
- Code: `webforms-viewstate-analyzer`, `serialization-overhead-checker`, `loop-optimization-scanner`
- Output: Specific issue, evidence, quantified impact, fix complexity

---

### Stages 4-7: Planning (Batch Execution)

**Stage 4: Strategy**
- Skill: `optimization-strategy-planner`
- Types: Query optimization (index/rewrite/caching), Caching strategy (redis/memory/output), Data access pattern (eager loading/batching/pagination)
- Output: Approach, expected improvement (% or ms), risk, complexity

**Stage 5: Safety**
- Skills: `safe-change-boundary-detector`, `query-behavior-validator`, `cache-correctness-validator`, `performance-regression-checker`
- Output: Data correctness (verified/at_risk/unknown), backwards compatibility, cache consistency, rollback safety
- Stop if: Data correctness at_risk or unknown

**Stage 6: Implementation**
- Skill: `performance-implementation-planner`
- Output: File changes, phased approach (low risk first), testing requirements
- Phases: Phase 1 (low risk, quick wins), Phase 2 (higher risk, bigger gains)

**Stage 7: Validation**
- Skill: `performance-validation-planner`
- Output: Metrics to track (baseline/target/acceptable), load scenarios (typical/peak), success criteria
- Requirement: Must have measurable success criteria

---

## DO:
✅ Measure baseline before optimizing
✅ Quantify expected improvement
✅ Verify data correctness after optimization
✅ Use phased approach (low risk first)
✅ Test with realistic load
✅ Have rollback plan ready
✅ Reference TEMPLATES.md for all outputs

## DON'T:
❌ Optimize without measurable baseline
❌ Sacrifice correctness for performance
❌ Skip safety verification
❌ Proceed with unknown impact
❌ Skip load testing
❌ Make changes without rollback plan
❌ Present results piecemeal (batch them)

---

## Error Handling

**IF baseline not measurable:**
```
1. Stop at stage 1
2. Present error:
   ⚠️ CANNOT OPTIMIZE WITHOUT BASELINE
   REASON: Performance metrics are not measurable
   REQUIRED: Establish monitoring/profiling first
   OPTIONS:
   [ ] Set up profiling tools
   [ ] Define measurable metrics
   [ ] Spike investigation: How to measure?
```

**IF data correctness at risk:**
```
1. Stop at stage 5 (safety)
2. CRITICAL STOP:
   🛑 DATA CORRECTNESS AT RISK
   OPTIMIZATION: {description}
   RISK: Optimization may produce incorrect results
   CANNOT PROCEED
   OPTIONS:
   [ ] Find alternative optimization
   [ ] Add correctness validation layer
   [ ] Abort optimization
```

**IF impact unknown:**
```
1. Stop at stage 4 (strategy)
2. Present issue:
   ⚠️ CANNOT QUANTIFY IMPROVEMENT
   REASON: Expected improvement is unknown
   REQUIRED: Must estimate impact before proceeding
   OPTIONS:
   [ ] Run spike to measure expected gain
   [ ] Find alternative with known impact
   [ ] Proceed with LOW confidence (not recommended)
```

---

## Common Patterns

### Pattern 1: N+1 Query
- **Symptoms:** Multiple queries for related data, scales with result count
- **Detection:** `n-plus-one-detector`
- **Solution:** Eager loading (.Include()), batch queries, or caching

### Pattern 2: Missing Index
- **Symptoms:** Table scans, query time scales with table size
- **Detection:** `missing-index-detector`
- **Solution:** Add indexes, update statistics, consider stored procedures

### Pattern 3: Cache Stampede
- **Symptoms:** Periodic drops, DB spikes on cache expiry
- **Detection:** `cache-stampede-detector`
- **Solution:** Staggered expiration, lock-based refresh, probabilistic early refresh

### Pattern 4: Large ViewState
- **Symptoms:** Large page size, slow loads, high bandwidth
- **Detection:** `webforms-viewstate-analyzer`
- **Solution:** Disable ViewState where not needed, server-side cache, control state only

---

## Optimization Decision Matrix

```
Impact | Risk  | Complexity | Decision
-------|-------|------------|---------------------------
HIGH   | LOW   | LOW        | Implement immediately
HIGH   | LOW   | HIGH       | Plan for next sprint
HIGH   | HIGH  | LOW        | Spike first, then implement
HIGH   | HIGH  | HIGH       | Consider alternatives
MEDIUM | LOW   | LOW        | Include in current work
MEDIUM | *     | HIGH       | Defer unless critical
LOW    | *     | *          | Defer indefinitely
```

---

## Checkpoint Presentation

Use template from `copilot/TEMPLATES.md` - "Standard Checkpoint"

**Present after stages 1-3 (if flagged):**
- Stages completed: 1 (Baseline), 2 (Bottleneck), 3 (Root Cause)
- Consolidated results: Current metrics, bottleneck identified, root cause analysis
- Expected improvement estimate
- Risk assessment
- Options: Approve optimization planning | Adjust approach | Spike | Reject

---

## Complete Example

**Input:** "Customer search is slow"

**Execution:**

```
Stage 1: Baseline
→ SKILL: performance-profiler
→ OUTPUT:
  page_load: 8200ms
  query_time: 7800ms
  cache_hit_rate: 0%
  result_count: 4500 rows
  p95: 9500ms

Stage 2: Bottleneck
→ SKILL: request-profiler
→ OUTPUT:
  component: "CustomerRepository.GetByFilter()"
  time_consumed: 95% (7800ms)
  frequency: Every search
  severity: CRITICAL

Stage 3: Root Cause
→ SKILL: linq-query-tracer
→ OUTPUT:
  root_cause: "SELECT * then filter in memory"
  query: "SELECT * FROM Customers; .Where(Status == 'Active') after .ToList()"
  evidence: "Loading 4500 rows, filtering to 1200"
  missing_index: "Status column not indexed"
  impact: "7800ms for query alone"

═══════════════════════════════════════════════════════════════
CHECKPOINT: Analysis Complete (if approve_before_stage: [4])
═══════════════════════════════════════════════════════════════
```

**User approves → Continue:**

```
Stage 4: Strategy
→ SKILL: optimization-strategy-planner
→ OUTPUT:
  approach: "Push filter to DB + add index + pagination"
  changes:
    1. Move .Where() before .ToList()
    2. Add index on Status column
    3. Implement pagination (50 rows/page)
  expected: "8200ms → 400ms (95% reduction)"
  risk: LOW
  complexity: MEDIUM

Stage 5: Safety
→ SKILLS: query-behavior-validator, safe-change-boundary-detector
→ OUTPUT:
  data_correctness: VERIFIED (same results, filtered at DB)
  backwards_compatible: YES
  cache_consistency: N/A (no cache currently)
  rollback_safe: YES

Stage 6: Implementation
→ SKILL: performance-implementation-planner
→ OUTPUT:
  Phase 1 (Quick win):
    - Move .Where() before .ToList() (2 line change)
    - Expected: 8200ms → 2000ms
  Phase 2 (Bigger gain):
    - Add index on Status column
    - Implement pagination
    - Expected: 2000ms → 400ms

Stage 7: Validation
→ SKILL: performance-validation-planner
→ OUTPUT:
  metrics:
    - page_load: baseline 8200ms, target <400ms, acceptable <1000ms
    - query_time: baseline 7800ms, target <200ms
  load_scenarios:
    - Typical: 10 concurrent users, 50K customers
    - Peak: 50 concurrent users, 50K customers
  success_criteria:
    - ≥90% improvement from baseline
    - No regression in data correctness
    - P95 under 600ms

✅ WORKFLOW COMPLETE ✅
MODE: PERFORMANCE
TIME: 52 seconds
EXPECTED IMPROVEMENT: 95% (8200ms → 400ms)
RISK: LOW
CONFIDENCE: HIGH
STATUS: READY FOR IMPLEMENTATION
```

---

## Escalation Rules

**Escalate to SPIKE when:**
- Baseline cannot be established (need investigation)
- Root cause unclear despite profiling
- Optimization approach unknown
- Expected impact cannot be estimated

**Escalate to FEATURE when:**
- Performance fix requires significant new functionality
- Optimization reveals architectural changes needed

---

## Constraints (Non-Negotiable)

- NEVER optimize without baseline measurement
- NEVER sacrifice correctness for performance
- NEVER skip safety verification
- ALWAYS quantify expected improvement
- ALWAYS have rollback plan
- ALWAYS validate with realistic load
- ALWAYS stop on data correctness risk

---

**See also:**
- Templates: `copilot/TEMPLATES.md`
- Execution rules: `copilot/specs/EXECUTION_RULES.md`
- Integration: `copilot/COPILOT_INTEGRATION.md`
