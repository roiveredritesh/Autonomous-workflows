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

**YOU DELIVER:**
- Validated requirements from PROJ-1234
- 7 acceptance criteria (export button, .xlsx format, filtered results, max 10K rows, error handling)
- HIGH feasibility with LOW risk
- 2 files affected, ~40 lines, minimal diff
- 8 test scenarios (happy path + edges)
- Complete documentation and rollback plan

**Output:** Complete feature plan (45-60 seconds)
**Risk:** LOW, **Confidence:** HIGH

---

## Workflow Phases

### Analysis Phase

**Requirement Validation**
- Use: `jira-story-intake` skill
- Delivers: Ticket ID, summary, acceptance criteria
- If unavailable: Create ticket or escalate to refinement

**Requirements Expansion**
- Use: `acceptance-criteria-expander` skill
- Delivers: Explicit functional requirements, edge cases, success criteria
- If unclear: Escalate to REFINEMENT mode for clarification

**Feasibility Assessment**
- Use: `feature-feasibility-analyzer` skill
- Delivers: Technical feasibility rating, risk level, complexity estimate
- If CRITICAL risk: Document mitigation approach or stop

**Legacy Impact Analysis**
- Use: `webforms-lifecycle-analyzer`, `telerik-impact-checker`, `safe-change-boundary-detector` skills
- Delivers: Affected pages, Telerik changes, safe boundaries, API changes
- If public API change: Provide justification or stop

**Data & Cache Impact**
- Use: `linq-query-tracer`, `sql-impact-analyzer`, `redis-cache-strategy-analyzer`, `cache-invalidation-mapper` skills
- Delivers: Data model changes, query performance assessment, cache strategy, stampede risk
- If performance impact unknown: Escalate to SPIKE mode

---

### Planning Phase

**Implementation Plan**
- Use: `minimal-diff-planner` skill
- Delivers: File-by-file changes, minimal diff strategy
- Constraints: Minimal changes, follow existing patterns, no unnecessary "improvements"

**Test Strategy**
- Use: `webforms-regression-analyzer`, `test-scenario-generator` skills
- Delivers: Regression scenarios, manual test steps, QA criteria

**Documentation**
- Use: `change-log-generator`, `decision-record-creator`, `risk-documentation-generator` skills
- Delivers: Change log, decision records, risk register, handoff notes

**Rollback Strategy**
- Use: `rollback-plan-generator`, `pr-metadata-generator` skills
- Delivers: Rollback procedure, validation criteria, PR metadata

---

## DO:
✅ Complete analysis before planning
✅ Stop immediately on safety violations
✅ Use minimal diff approach
✅ Follow existing WebForms patterns
✅ Document all decisions
✅ Create rollback plan before implementation
✅ Reference TEMPLATES.md for all outputs

## DON'T:
❌ Skip required analysis steps
❌ Make "improvements" outside scope
❌ Refactor code unnecessarily
❌ Change public APIs without justification
❌ Proceed with HIGH risk without review
❌ Optimize prematurely
❌ Skip documentation or rollback planning

---

## Error Handling

**IF analysis step fails:**
```
1. Stop at failed step
2. Capture error message
3. Present partial results
4. Offer options:
   [ ] Retry with different parameters
   [ ] Skip step (if non-critical)
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
1. Stop during requirements expansion
2. Escalate to REFINEMENT mode
3. Return with clarified requirements
```

---

## Skill Invocation

Use template from `instructions/output-templates.md` - "Skill Invocation Template"

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

Use template from `instructions/output-templates.md` - "Completion Template"

**Include:**
- Mode: FEATURE DELIVERY
- Execution time
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
ANALYSIS PHASE:

Requirement Validation
→ SKILL: jira-story-intake
→ OUTPUT: Ticket PROJ-1234 validated

Requirements Expansion
→ SKILL: acceptance-criteria-expander
→ OUTPUT: 7 criteria (export button, .xlsx format, filtered results, max 10K rows, error handling)

Feasibility Assessment
→ SKILL: feature-feasibility-analyzer
→ OUTPUT: HIGH feasibility, LOW risk, MEDIUM complexity, use EPPlus library

Legacy Impact Analysis
→ SKILL: webforms-lifecycle-analyzer
→ OUTPUT: CustomerList.aspx affected, button in toolbar, PostBack pattern, no Telerik changes

Data/Cache Impact
→ SKILL: linq-query-tracer
→ OUTPUT: Reuse existing query, no cache needed, acceptable for <10K rows

PLANNING PHASE:

Implementation Plan
→ SKILL: minimal-diff-planner
→ OUTPUT: 2 files (CustomerList.aspx, .cs), ~40 lines, server-side export

Test Strategy
→ SKILL: test-scenario-generator
→ OUTPUT: 8 scenarios (happy path, large dataset, timeout, filters)

Documentation
→ SKILL: change-log-generator
→ OUTPUT: Change log, inline comments, decision records

Rollback Strategy
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
- Templates: `instructions/output-templates.md`
- Execution rules: `specs/README.md (archived)`
- Integration: `instructions/integration-overview.md`
