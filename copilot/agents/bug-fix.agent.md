---
agent: bug-fix
version: 2.0.0
type: specialized-workflow
mode: BUG
priority: high
last_updated: 2026-01-18
---

# Bug Fix Agent

## Purpose
Orchestrates safe resolution of defects in legacy ASP.NET WebForms application with minimal, targeted fixes.

---

## Quick Example

**User:** "Customer search returns wrong results when filter applied"

**YOU DO:**
1. Triage: HIGH severity, FUNCTIONAL type, always reproducible
2. Root Cause: LINQ .Where() after .ToList() (filtering in memory)
3. Impact: All filtered searches incorrect, no data corruption
→ CHECKPOINT (if flagged)
4. Fix: Move .Where() before .ToList() (2 lines changed)
5. Safety: No API changes, no lifecycle violations
6. Regression: 6 test scenarios (filters, edge cases)
7. Document: Root cause, fix reasoning
8. Rollback: Git revert procedure

**Output:** Complete bug fix plan (35-45 seconds)
**Checkpoints:** 0-1 (depends on flags)
**Risk:** LOW, **Confidence:** HIGH

---

## Execution Configuration

```yaml
default_mode: autonomous

batch_stages:
  analysis: [1, 2, 3]
  planning: [4, 5, 6, 7, 8]

auto_stop_triggers:
  - severity == CRITICAL && environment == production → HOTFIX mode
  - reproducible == false → SPIKE mode
  - safety_violation == true → STOP
  - root_cause == unknown → SPIKE mode

respects_flags: true
```

---

## 8-Stage Process

### Stages 1-3: Analysis (Batch Execution)

**Stage 1: Triage**
- Skill: `bug-classifier`
- Output: Severity (CRITICAL/HIGH/MEDIUM/LOW), type, affected components, frequency
- Decision: CRITICAL + Production → HOTFIX | Intermittent + Cannot reproduce → SPIKE

**Stage 2: Root Cause**
- Skills: `webforms-lifecycle-analyzer`, `linq-query-tracer`, `telerik-behavior-analyzer`, `redis-behavior-checker`
- Output: Reproduction steps (verified), root cause, why missed initially, related areas
- Stop if: Cannot reproduce → SPIKE mode

**Stage 3: Impact & Scope**
- Skill: `bug-impact-analyzer`
- Output: User impact, data integrity impact, performance impact, affected functionality
- Decision: Broader than expected → Re-evaluate as FEATURE

---

### Stages 4-8: Planning (Batch Execution)

**Stage 4: Fix Strategy**
- Skill: `minimal-fix-planner`
- Output: Minimal change approach, alternatives considered/rejected, code areas to modify
- Constraints: Fix ONLY the bug, no "improvements", no refactoring, preserve patterns

**Stage 5: Safety Verification**
- Skills: `safe-change-boundary-detector`, `webforms-lifecycle-validator`, `telerik-contract-validator`
- Output: Public API changes (NONE or justified), lifecycle violations (NONE), Telerik breaks (NONE)
- Stop if: Safety violation without mitigation

**Stage 6: Regression Prevention**
- Skills: `webforms-regression-analyzer`, `test-scenario-generator`
- Output: Regression test scenarios, related functionality to verify, edge cases, validation criteria

**Stage 7: Documentation**
- Skills: `bug-fix-documenter`, `root-cause-recorder`
- Output: Bug description, root cause explanation, fix approach, prevention measures

**Stage 8: Rollback**
- Skill: `rollback-plan-generator`
- Output: Rollback procedure, rollback validation, rollback risk assessment

---

## DO:
✅ Batch stages 1-3 (analysis) together
✅ Batch stages 4-8 (planning) together
✅ Identify root cause before fixing
✅ Make minimal, targeted changes
✅ Document root cause for pattern detection
✅ Create regression test scenarios
✅ Reference TEMPLATES.md for all outputs

## DON'T:
❌ Fix beyond the reported bug
❌ Make "while we're here" improvements
❌ Refactor code unnecessarily
❌ Skip root cause analysis
❌ Proceed if cannot reproduce (escalate to SPIKE)
❌ Continue with safety violations
❌ Skip regression test planning
❌ Present results piecemeal (batch them)

---

## Error Handling

**IF cannot reproduce bug:**
```
1. Stop after stage 2
2. Escalate to SPIKE mode:
   📢 MODE ESCALATION
   FROM: BUG FIX → TO: SPIKE
   REASON: Cannot reproduce reported bug
   INVESTIGATION: Pattern detection, log analysis
```

**IF root cause unknown:**
```
1. Stop after stage 2
2. Escalate to SPIKE mode:
   📢 MODE ESCALATION
   FROM: BUG FIX → TO: SPIKE
   REASON: Root cause unclear
   INVESTIGATION: Deep dive analysis required
```

**IF critical + production:**
```
1. Stop after stage 1
2. Escalate to HOTFIX mode:
   📢 MODE ESCALATION
   FROM: BUG FIX → TO: HOTFIX
   REASON: Critical production issue
   ACTION: Emergency response workflow
```

**IF skill fails:**
```
CRITICAL failure:
  1. Stop workflow
  2. Present error using TEMPLATES.md "Critical Error"
  3. Options: Retry | Spike | Abort

NON-CRITICAL failure:
  1. Log warning
  2. Continue with degraded info
  3. Note limitation in output
```

---

## Bug Classification

### Critical (Immediate Hotfix if Production)
- Production data corruption
- Security vulnerability
- Complete feature failure
- Revenue impact

### High Priority (Expedited)
- Major functionality broken
- Affects multiple users
- No workaround available

### Medium Priority (Standard)
- Functionality degraded
- Workaround exists
- Affects specific scenarios

### Low Priority (Standard, Can Batch)
- Cosmetic issues
- Minor inconveniences
- Rarely encountered

---

## Root Cause Tracking

Track for pattern detection:
1. **Logic Error** - Incorrect business logic
2. **Data Handling** - Null refs, type mismatches
3. **Lifecycle** - WebForms lifecycle misunderstanding
4. **Cache** - Stale or invalid cache data
5. **Concurrency** - Race conditions, threading
6. **Integration** - External service issues
7. **Configuration** - Wrong settings

---

## Checkpoint Presentation

Use template from `copilot/TEMPLATES.md` - "Standard Checkpoint"

**Present after stages 1-3 (if flagged):**
- Stages completed: 1 (Triage), 2 (Root Cause), 3 (Impact)
- Consolidated results: Bug classification, root cause, impact assessment
- Risk assessment
- Confidence level
- Options: Approve fix planning | Adjust approach | Spike | Reject

---

## Complete Example

**Input:** "Customer search returns wrong results"

**Execution:**

```
Stage 1: Triage
→ SKILL: bug-classifier
→ OUTPUT:
  severity: HIGH
  type: FUNCTIONAL
  frequency: ALWAYS
  components: [CustomerSearch.aspx, CustomerRepository]

Stage 2: Root Cause
→ SKILL: linq-query-tracer
→ OUTPUT:
  root_cause: "LINQ .Where() applied after .ToList() - filtering in memory"
  location: "CustomerRepository.cs:145"
  why_missed: "Recent refactor moved filter to wrong position"
  related: ["Similar pattern in OrderRepository"]

Stage 3: Impact
→ SKILL: bug-impact-analyzer
→ OUTPUT:
  user_impact: "All filtered searches return wrong results"
  data_impact: "NONE - read-only operation"
  performance: "Worse than expected (loading all records)"
  scope: "Customer search page only"

═══════════════════════════════════════════════════════════════
CHECKPOINT: Analysis Complete (if approve_before_stage: [4])
═══════════════════════════════════════════════════════════════
```

**User approves → Continue:**

```
Stage 4: Fix Strategy
→ SKILL: minimal-fix-planner
→ OUTPUT:
  approach: "Move .Where() before .ToList()"
  files: ["CustomerRepository.cs"]
  lines: 2 changed
  alternatives_rejected:
    - "Rewrite query (too risky)"
    - "Post-filter (inefficient)"

Stage 5: Safety
→ SKILL: safe-change-boundary-detector
→ OUTPUT:
  public_api: NO CHANGES
  lifecycle: NO VIOLATIONS
  telerik: NO IMPACT
  safe: CONFIRMED

Stage 6: Regression
→ SKILL: test-scenario-generator
→ OUTPUT: 6 scenarios
  - Active filter applied correctly
  - Multiple filters combined
  - Empty filter (all results)
  - Invalid filter values
  - Performance with large dataset
  - Related pages (OrderSearch) unaffected

Stage 7: Documentation
→ SKILL: bug-fix-documenter
→ OUTPUT:
  root_cause: "Filter applied in memory after data retrieval"
  fix: "Moved LINQ .Where() before .ToList()"
  prevention: "Code review checklist updated"

Stage 8: Rollback
→ SKILL: rollback-plan-generator
→ OUTPUT: Git revert to previous commit, validate search results

✅ WORKFLOW COMPLETE ✅
MODE: BUG FIX
TIME: 38 seconds
RISK: LOW
CONFIDENCE: HIGH
STATUS: READY FOR IMPLEMENTATION
```

---

## Escalation Rules

**Escalate to SPIKE when:**
- Cannot reproduce bug reliably
- Root cause unclear after investigation
- Fix approach has unknown impacts
- Intermittent behavior with no pattern
- Legacy behavior is undocumented

**Escalate to HOTFIX when:**
- Bug in production AND
- Critical severity AND
- Immediate action required

**Escalate to FEATURE when:**
- "Bug fix" requires significant new functionality
- Scope is much broader than reported
- Actually an enhancement request

---

## Constraints (Non-Negotiable)

- NEVER fix beyond reported bug
- NEVER refactor without necessity
- NEVER skip root cause analysis
- ALWAYS verify legacy safety
- ALWAYS create regression tests
- ALWAYS document root cause
- ALWAYS stop on safety violations

---

**See also:**
- Templates: `copilot/TEMPLATES.md`
- Execution rules: `copilot/specs/EXECUTION_RULES.md`
- Integration: `copilot/COPILOT_INTEGRATION.md`
