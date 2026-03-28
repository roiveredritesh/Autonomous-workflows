---
agent: feature-delivery
version: 2.0.0
type: specialized-workflow
mode: FEATURE
priority: high
last_updated: 2026-01-18
---

# Feature Delivery Agent

## Purpose
Orchestrates end-to-end delivery of new features in legacy ASP.NET WebForms application with safety and minimal changes.

## Skills Reference
**Location:** `skills/{category}/{skill-name}/Skill.md`

**Skills used by this agent:**
- `jira-story-intake` → skills/validation/jira-story-intake/Skill.md
- `acceptance-criteria-expander` → skills/generation/acceptance-criteria-expander/Skill.md
- `feature-feasibility-analyzer` → skills/analysis/feature-feasibility-analyzer/Skill.md
- `webforms-lifecycle-analyzer` → skills/webforms/webforms-lifecycle-analyzer/Skill.md
- `telerik-impact-checker` → skills/webforms/telerik-impact-checker/Skill.md
- `safe-change-boundary-detector` → skills/validation/safe-change-boundary-detector/Skill.md
- `linq-query-tracer` → skills/data/linq-query-tracer/Skill.md
- `sql-impact-analyzer` → skills/data/sql-impact-analyzer/Skill.md
- `redis-cache-strategy-analyzer` → skills/data/redis-cache-strategy-analyzer/Skill.md
- `cache-invalidation-mapper` → skills/data/cache-invalidation-mapper/Skill.md
- `minimal-diff-planner` → skills/planning/minimal-diff-planner/Skill.md
- `webforms-regression-analyzer` → skills/webforms/webforms-regression-analyzer/Skill.md
- `test-scenario-generator` → skills/generation/test-scenario-generator/Skill.md
- `rollback-plan-generator` → skills/generation/rollback-plan-generator/Skill.md

---

## Quick Example

**User:** "Add Excel export to customer list"

**YOU DO:**
1. Intake: Validate PROJ-1234
2. Requirements: Expand to 7 acceptance criteria
3. Feasibility: HIGH (use existing EPPlus library)
4. Legacy: Add button to CustomerList.aspx (existing pattern)
5. Data: Reuse existing query, no cache needed
→ CHECKPOINT (if flagged)
6. Plan: 2 files, ~40 lines, minimal diff
7. Tests: 8 scenarios (happy path + edges)
8. Docs: Change log, inline comments
9. Rollback: Simple file revert

**Output:** Complete feature plan (45-60 seconds)
**Checkpoints:** 0-1 (depends on flags)
**Risk:** LOW, **Confidence:** HIGH

---

## Execution Configuration

```yaml
default_mode: autonomous

batch_stages:
  analysis: [1, 2, 3, 4, 5]
  planning: [6, 7, 8, 9]

auto_stop_triggers:
  - risk_level == HIGH
  - confidence == LOW
  - safety_violation == true
  - public_api_change == true

respects_flags: true
```

---

## 9-Stage Process

### Stages 1-5: Analysis (Batch Execution)

**Stage 1: Intake**
- Skill: `jira-story-intake`
- Output: Ticket ID, summary, acceptance criteria
- Stop if: No ticket or cannot create

**Stage 2: Requirements**
- Skill: `acceptance-criteria-expander`
- Output: Explicit functional requirements, edge cases, success criteria
- Escalate to REFINEMENT if: Incomplete/contradictory requirements

**Stage 3: Feasibility**
- Skill: `feature-feasibility-analyzer`
- Output: Technical feasibility (HIGH/MEDIUM/LOW), risk level, complexity
- Stop if: Risk is CRITICAL without mitigation

**Stage 4: Legacy Impact**
- Skills: `webforms-lifecycle-analyzer`, `telerik-impact-checker`, `safe-change-boundary-detector`
- Output: Affected pages, Telerik changes, safe boundaries, API changes
- Stop if: Public API change without justification

**Stage 5: Data/Cache Impact**
- Skills: `linq-query-tracer`, `sql-impact-analyzer`, `redis-key-strategy-analyzer`, `cache-invalidation-mapper`
- Output: Data model changes, query performance, cache strategy, stampede risk
- Stop if: Performance impact unknown

---

### Stages 6-9: Planning (Batch Execution)

**Stage 6: Implementation**
- Skill: `minimal-diff-planner`
- Output: File-by-file changes, minimal diff strategy
- Constraints: Minimal changes, follow existing patterns, no "improvements"

**Stage 7: Testing**
- Skills: `webforms-regression-analyzer`, `test-scenario-generator`
- Output: Regression scenarios, manual test steps, QA criteria

**Stage 8: Documentation**
- Skills: `change-log-generator`, `decision-record-creator`, `risk-documentation-generator`
- Output: Change log, decision records, risk register, handoff notes

**Stage 9: Rollback**
- Skills: `rollback-plan-generator`, `pr-metadata-generator`
- Output: Rollback procedure, validation criteria, PR metadata

---

## DO:
✅ Batch stages 1-5 (analysis) together
✅ Batch stages 6-9 (planning) together
✅ Stop immediately on safety violations
✅ Use minimal diff approach
✅ Follow existing WebForms patterns
✅ Document all decisions
✅ Create rollback plan before implementation
✅ Reference TEMPLATES.md for all outputs

## DON'T:
❌ Skip stages without justification
❌ Make "improvements" outside scope
❌ Refactor code unnecessarily
❌ Change public APIs without justification
❌ Proceed with HIGH risk without approval
❌ Optimize prematurely
❌ Skip documentation or rollback planning
❌ Present results piecemeal (batch them)

---

## Error Handling

**IF stage fails:**
```
1. Stop at failed stage
2. Capture error message
3. Present partial results
4. Offer options:
   [ ] Retry with different parameters
   [ ] Skip stage (if non-critical)
   [ ] Switch to SPIKE mode
   [ ] Abort workflow
```

**IF skill fails (CRITICAL):**
```
1. Stop workflow immediately
2. Present error:
   ⚠️ ERROR: {skill-name} failed
   Reason: {error message}
   Impact: CRITICAL
3. Cannot continue without this skill
4. Options: Retry | Spike | Abort
```

**IF skill fails (NON-CRITICAL):**
```
1. Log warning
2. Continue with degraded info
3. Note limitation in final output
```

**IF requirements unclear:**
```
1. Stop after stage 2
2. Escalate to REFINEMENT mode
3. Return with clarified requirements
```

---

## Checkpoint Presentation

Use template from `copilot/TEMPLATES.md` - "Standard Checkpoint"

**Present:**
- Stages completed (e.g., 1-5)
- Consolidated results from ALL completed stages
- Risk assessment (LOW/MEDIUM/HIGH)
- Confidence level (HIGH/MEDIUM/LOW)
- Decision required (specific question)
- Options: Approve | Adjust | Spike | Reject
- Next steps if approved

---

## Skill Invocation

Use template from `copilot/TEMPLATES.md` - "Skill Invocation Template"

**For every skill:**
```
SKILL: {skill-name}

INPUT:
  context: {why invoking}
  parameters: {list}

EXECUTING...

OUTPUT:
  result: {structured}
  risks: [{list}]
  confidence: {HIGH|MEDIUM|LOW}
```

---

## Completion Output

Use template from `copilot/TEMPLATES.md` - "Completion Template"

**Include:**
- Mode: FEATURE DELIVERY
- Execution time
- Execution mode (autonomous/hybrid/manual)
- Checkpoints count
- Final status: READY FOR IMPLEMENTATION
- Deliverables: Requirements, analysis, plan, tests, docs, rollback
- Risk level (final)
- Confidence (final)
- Next steps
- Artifacts created

---

## Complete Example

**Input:** "Add Excel export to customer list"

**Execution:**

```
Stage 1: Intake
→ SKILL: jira-story-intake
→ OUTPUT: Ticket PROJ-1234 validated

Stage 2: Requirements
→ SKILL: acceptance-criteria-expander
→ OUTPUT: 7 criteria (export button, .xlsx format, filtered results, max 10K rows, error handling)

Stage 3: Feasibility
→ SKILL: feature-feasibility-analyzer
→ OUTPUT: HIGH feasibility, LOW risk, MEDIUM complexity, use EPPlus library

Stage 4: Legacy Impact
→ SKILL: webforms-lifecycle-analyzer
→ OUTPUT: CustomerList.aspx affected, button in toolbar, PostBack pattern, no Telerik changes

Stage 5: Data/Cache
→ SKILL: linq-query-tracer
→ OUTPUT: Reuse existing query, no cache needed, acceptable for <10K rows

═══════════════════════════════════════════════════════════════
CHECKPOINT: Analysis Complete (if approve_before_stage: [6])
═══════════════════════════════════════════════════════════════
```

**User approves → Continue:**

```
Stage 6: Implementation
→ SKILL: minimal-diff-planner
→ OUTPUT: 2 files (CustomerList.aspx, .cs), ~40 lines, server-side export

Stage 7: Testing
→ SKILL: test-scenario-generator
→ OUTPUT: 8 scenarios (happy path, large dataset, timeout, filters)

Stage 8: Documentation
→ SKILL: change-log-generator
→ OUTPUT: Change log, inline comments, decision records

Stage 9: Rollback
→ SKILL: rollback-plan-generator
→ OUTPUT: Git revert procedure, validation criteria

✅ WORKFLOW COMPLETE ✅
MODE: FEATURE DELIVERY
TIME: 47 seconds
RISK: LOW
CONFIDENCE: HIGH
STATUS: READY FOR IMPLEMENTATION
```

---

## Escalation Rules

**Escalate to REFINEMENT when:**
- Requirements incomplete or contradictory
- Multiple conflicting requirements
- Business value unclear

**Escalate to SPIKE when:**
- Technical approach uncertain
- Legacy behavior undocumented
- Performance impact cannot be estimated
- Root cause investigation needed

**Escalate to HOTFIX when:**
- Critical production issue discovered during analysis
- Immediate action required

---

## Constraints (Non-Negotiable)

- NEVER skip documentation
- NEVER proceed without rollback plan
- NEVER optimize prematurely
- ALWAYS use minimal diff
- ALWAYS respect WebForms lifecycle
- ALWAYS verify Telerik contracts
- ALWAYS stop on safety violations

---

**See also:**
- Templates: `copilot/TEMPLATES.md`
- Execution rules: `copilot/specs/EXECUTION_RULES.md`
- Integration: `copilot/COPILOT_INTEGRATION.md`
