# Workflow Execution Guide

## Introduction

This guide explains how to use the autonomous workflow system with execution flags to control when GitHub Copilot pauses for your approval.

---

## Quick Start

### Default: Full Autonomous Execution

The simplest way to use the system - just describe what you want:

```
You: "Add Excel export to customer list"

Copilot: [Executes all analysis and planning stages]

Output (after 45 seconds):
===================================
MODE: FEATURE
CONFIDENCE: HIGH

ANALYSIS COMPLETE (Stages 1-5):
✓ Requirements expanded
✓ Feasibility: HIGH, Risk: LOW
✓ Legacy impact analyzed
✓ Data/Cache strategy defined

PLAN COMPLETE (Stages 6-9):
✓ Implementation plan created
✓ Test scenarios generated
✓ Documentation prepared
✓ Rollback procedure defined

READY FOR: Implementation
===================================
```

**When to use:** Low-risk changes, routine features, well-understood requirements

---

## Execution Modes

### Mode 1: Autonomous (Default)

**No flags needed** - Copilot executes everything and presents complete results.

```
You: "Add ability to filter customers by date range"

Copilot: [Analyzes, plans, documents - all automatically]
```

**Advantages:**
- Fastest workflow
- Single consolidated response
- Minimal interruptions

**Best for:**
- Low-risk features
- Standard bug fixes
- Well-defined requirements

---

### Mode 2: Checkpoint After Analysis

**Pause after analysis to review before planning**

```
You: "Add ability to filter customers by date range"
Flags:
  approve_before_stage: [6]

Copilot: [Executes analysis stages 1-5]

CHECKPOINT: Analysis Complete
─────────────────────────────
Requirements: [Details]
Risk: LOW
Feasibility: HIGH
Legacy Impact: Minimal changes to CustomerSearch.aspx

Approve implementation planning?
[ ] Approve  [ ] Adjust  [ ] Spike  [ ] Reject
─────────────────────────────

You: "Approve"

Copilot: [Executes planning stages 6-9]

PLANNING COMPLETE:
✓ Implementation plan
✓ Test scenarios
✓ Documentation
✓ Rollback plan
===================================
```

**Best for:**
- Medium-complexity features
- Changes to critical systems
- When you want to review analysis before committing to implementation

---

### Mode 3: Risk-Based Pausing

**Automatically pause if risk reaches threshold**

```
You: "Optimize the customer search query"
Flags:
  approve_at_risk: medium

Copilot: [Executes stages 1-4]
[Stage 4 detects MEDIUM risk]

CHECKPOINT: Risk Threshold Reached
─────────────────────────────────
RISK: MEDIUM

Root cause: N+1 query detected
Impact: Table scan on 50K+ rows
Performance: Current query takes 8.2 seconds

MITIGATION OPTIONS:
1. Add index (LOW risk, HIGH impact)
2. Rewrite query (MEDIUM risk, HIGH impact)
3. Add caching (LOW risk, MEDIUM impact)

RECOMMENDATION: Add index on Status column

Approve recommended approach?
[ ] Approve  [ ] Adjust  [ ] Spike  [ ] Reject
─────────────────────────────────

You: "Approve"

Copilot: [Continues with remaining stages]
```

**Best for:**
- Performance optimizations
- Database changes
- Code that could impact production
- Uncertain technical approaches

---

### Mode 4: Manual Step-by-Step

**Approve every stage individually**

```
You: "Add ability to filter customers by date range"
Flags:
  manual_mode: true

Copilot: [Executes stage 1 only]

STAGE 1 COMPLETE: Intake & Validation
─────────────────────────────────────
Jira ticket: PROJ-1234 validated
Story: "Add date range filter to customer search"

Continue to stage 2?
─────────────────────────────────────

You: "Yes"

Copilot: [Executes stage 2 only]

STAGE 2 COMPLETE: Requirement Clarity
─────────────────────────────────────
Acceptance Criteria:
- Date range picker with From/To fields
- Filter applied on Search click
- Validation: From <= To
- Clear filter button
- Empty range = no filter

Continue to stage 3?
─────────────────────────────────────

[... continues for all 9 stages ...]
```

**Best for:**
- Learning the workflow system
- High-risk production hotfixes
- Compliance/audit requirements
- Complex debugging scenarios

---

## Execution Flags Reference

### Flag: approve_before_stage

**Pause before specific stages**

```yaml
# Pause before implementation planning
approve_before_stage: [6]

# Pause before multiple stages
approve_before_stage: [5, 7]

# Inline syntax
"Add Excel export [approve_before_stage: 6]"
```

**Stage Numbers:**
1. Intake & Validation
2. Requirement Clarity
3. Feasibility & Risk Assessment
4. System & Legacy Impact Analysis
5. Data & Cache Impact
6. Implementation Planning ← Common checkpoint
7. Regression & QA Planning
8. Documentation
9. Release & Rollback Readiness

---

### Flag: approve_at_risk

**Pause when risk meets threshold**

```yaml
# Pause on medium or high risk
approve_at_risk: medium

# Pause only on high risk
approve_at_risk: high

# Pause on any risk (including low)
approve_at_risk: low
```

**Risk Levels:**
- **LOW** - Minimal impact, easy rollback, well-tested pattern
- **MEDIUM** - Moderate impact, some complexity, requires testing
- **HIGH** - Significant impact, complex change, production risk

---

### Flag: approve_before_skills

**Pause before invoking specific skills**

```yaml
# Pause before database analysis
approve_before_skills: [linq-query-tracer, sql-execution-analyzer]

# Pause before cache decisions
approve_before_skills: [redis-cache-strategy-analyzer]
```

**Common Skills:**
- `linq-query-tracer` - Database query analysis
- `sql-execution-analyzer` - SQL performance review
- `redis-cache-strategy-analyzer` - Caching decisions
- `webforms-lifecycle-analyzer` - Page lifecycle impact
- `telerik-impact-checker` - Telerik control changes
- `minimal-diff-planner` - Implementation planning

---

### Flag: manual_mode

**Approve after every stage**

```yaml
manual_mode: true
```

Overrides all other flags.

---

### Flag: checkpoint_strategy

**Define checkpoint placement strategy**

```yaml
# Checkpoint after analysis only
checkpoint_strategy: analysis_only

# Checkpoint after analysis and planning
checkpoint_strategy: both

# No automatic checkpoints
checkpoint_strategy: none
```

---

## Common Workflows

### Workflow 1: New Feature (Standard)

**Scenario:** Adding a routine feature to the application

```
You: "Add Excel export button to customer list page"

[No flags - fully autonomous]

Expected Time: 30-60 seconds
Checkpoints: 0 (unless risk detected)
```

---

### Workflow 2: New Feature (Review Before Coding)

**Scenario:** Want to review analysis before implementation

```
You: "Add email notification when order status changes"
Flags:
  approve_before_stage: [6]

Expected Time: 30 sec + decision + 20 sec
Checkpoints: 1 (after analysis)

Checkpoint Question: "Analysis complete. Approve implementation planning?"
```

---

### Workflow 3: Bug Fix (Auto-pause on Risk)

**Scenario:** Fixing a bug, pause if risky

```
You: "Fix customer search returning wrong results"
Flags:
  approve_at_risk: medium

Expected Time: Variable (depends on risk level)
Checkpoints: 0-1 (only if medium/high risk detected)
```

---

### Workflow 4: Performance Optimization (Always Review)

**Scenario:** Performance work requires careful review

```
You: "Optimize customer search page load time"
Flags:
  approve_at_risk: low
  approve_before_stage: [6]

Expected Time: 30 sec + decision + 20 sec
Checkpoints: 1-2 (analysis + any risk)

Reason: Performance work often has unexpected risks
```

---

### Workflow 5: Production Hotfix (Maximum Control)

**Scenario:** Critical production issue, need full control

```
You: "Fix order submission failing in production"
Flags:
  manual_mode: true

Expected Time: 9 stages × (10 sec + decision time)
Checkpoints: 9 (after every stage)

Reason: Production fixes require careful oversight
```

---

### Workflow 6: Research/Spike (Autonomous Investigation)

**Scenario:** Investigating unknown behavior

```
You: "Investigate why customer cache expires randomly"

[No flags - spike agent handles investigation]

Expected Time: Variable (time-boxed by spike charter)
Checkpoints: 1 (at end, presenting findings)
```

---

## Checkpoint Response Options

When Copilot pauses at a checkpoint, you have these options:

### Option 1: Approve

**Continue execution as planned**

```
CHECKPOINT: Analysis Complete
[... results ...]
Approve implementation planning?

You: "Approve"
You: "Yes"
You: "Continue"
You: "Proceed"

→ Copilot continues to next phase
```

---

### Option 2: Adjust

**Modify approach before continuing**

```
CHECKPOINT: Analysis Complete
[... results ...]
Recommendation: Add Redis caching with 5-minute TTL

You: "Adjust: Use 10-minute TTL instead"

→ Copilot adjusts configuration and continues
```

**Common Adjustments:**
- Change TTL values
- Modify scope
- Skip optional stages
- Add additional constraints

---

### Option 3: Spike

**Need more investigation**

```
CHECKPOINT: Risk Detected
Risk: MEDIUM - Performance impact unknown

You: "Spike"
You: "Need more investigation"

→ Copilot switches to SPIKE mode
→ Time-boxes investigation
→ Returns with findings
→ Can resume original workflow
```

**When to Spike:**
- Uncertain technical approach
- Unknown legacy behavior
- Performance impact unclear
- Need proof-of-concept

---

### Option 4: Reject

**Stop the workflow**

```
CHECKPOINT: Analysis Complete
[... results ...]

You: "Reject"
You: "Stop"
You: "Cancel"

→ Workflow stops
→ Work done so far is preserved
→ Can start different approach
```

**When to Reject:**
- Approach not viable
- Requirements changed
- Different solution needed
- Found better alternative

---

## Automatic Stop Conditions

Some conditions **always** trigger a checkpoint, regardless of flags:

### Safety Violations

```yaml
auto_stops:
  public_api_change:
    trigger: "Public API change without justification"
    action: IMMEDIATE STOP

  webforms_lifecycle_violation:
    trigger: "WebForms lifecycle rules broken"
    action: IMMEDIATE STOP

  telerik_contract_break:
    trigger: "Telerik control contract violated"
    action: IMMEDIATE STOP

  missing_rollback:
    trigger: "Cannot create rollback procedure"
    action: IMMEDIATE STOP
```

**These cannot be overridden - they protect system integrity**

---

### High Risk

```yaml
high_risk_stop:
  trigger: "Risk level: HIGH"
  action: AUTOMATIC CHECKPOINT
  message: "HIGH RISK: Review required before continuing"
```

---

### Low Confidence

```yaml
low_confidence_stop:
  trigger: "Confidence: LOW"
  action: ESCALATE TO SPIKE
  message: "LOW CONFIDENCE: Investigation needed"
```

---

### Conflicting Requirements

```yaml
conflict_stop:
  trigger: "Contradictory requirements detected"
  action: ESCALATE TO REFINEMENT
  message: "CONFLICT: Clarification needed"
```

---

## Flag Syntax Examples

### Inline Format

```
"Add Excel export [approve_before_stage: 6]"

"Fix customer search [approve_at_risk: medium]"

"Add email notifications [manual_mode: true]"

"Optimize query performance [approve_before_stage: 6, approve_at_risk: medium]"
```

---

### YAML Block Format

```
Add Excel export to customer list
Flags:
  approve_before_stage: [6]
```

```
Optimize customer search query
Flags:
  approve_at_risk: medium
  approve_before_skills: [linq-query-tracer]
```

```
Add email notifications when order ships
Flags:
  approve_before_stage: [5, 7]
  checkpoint_strategy: both
```

---

### Natural Language Format

```
"Add Excel export, but pause before implementation"
→ Translates to: approve_before_stage: [6]

"Fix customer search, pause if risky"
→ Translates to: approve_at_risk: medium

"Add email notifications, step by step"
→ Translates to: manual_mode: true

"Optimize query performance, review after analysis"
→ Translates to: checkpoint_strategy: analysis_only
```

---

## Execution Time Expectations

### Full Autonomous Mode

```yaml
simple_feature: "30-60 seconds"
complex_feature: "60-120 seconds"
bug_fix: "20-40 seconds"
performance_issue: "40-90 seconds"
spike: "Variable (time-boxed)"

total_checkpoints: 0
human_decision_time: 0
```

---

### Checkpoint After Analysis

```yaml
analysis_batch: "20-40 seconds"
[CHECKPOINT - human decision time]
planning_batch: "15-30 seconds"

total_checkpoints: 1
total_time: "35-70 seconds + decision time"
```

---

### Risk-Based Pausing

```yaml
until_risk_detected: "Variable"
[CHECKPOINT - human decision time]
remaining_work: "Variable"

total_checkpoints: 0-1 (depends on risk)
total_time: "Variable + decision time if risk detected"
```

---

### Manual Mode

```yaml
per_stage: "5-15 seconds"
total_stages: 9
[CHECKPOINT after each stage]

total_checkpoints: 9
total_time: "45-135 seconds + 9 × decision time"
```

---

## Best Practices

### Start Autonomous, Add Flags as Needed

```
First time: "Add Excel export"
[See how it works]

If you want more control: "Add email notifications [approve_before_stage: 6]"
```

---

### Use Risk Flags for Uncertain Work

```
Good: "Optimize database query [approve_at_risk: medium]"
Why: Performance work often has unexpected complexity
```

---

### Use Manual Mode for Critical Production Changes

```
Good: "Fix production order submission bug [manual_mode: true]"
Why: Production hotfixes need careful oversight
```

---

### Combine Flags for Complex Work

```
"Migrate customer data to new schema"
Flags:
  approve_before_stage: [5, 7]
  approve_at_risk: medium

Why: Data migration is risky, want multiple review points
```

---

### Don't Over-Control Routine Work

```
Bad: "Add export button [manual_mode: true]"
Why: Simple features don't need 9 approval points

Good: "Add export button"
Why: Let autonomous workflow handle routine work
```

---

## Troubleshooting

### "Copilot keeps pausing when I don't want it to"

**Cause:** manual_mode is enabled or risk threshold is too low

**Solution:**
```
# Remove manual_mode
"Add feature" instead of "Add feature [manual_mode: true]"

# Raise risk threshold
approve_at_risk: high instead of approve_at_risk: low
```

---

### "Copilot doesn't pause when I want it to"

**Cause:** No flags set, or risk level below threshold

**Solution:**
```
# Add explicit checkpoint
"Add feature [approve_before_stage: 6]"

# Or lower risk threshold
approve_at_risk: low
```

---

### "I want to change my mind mid-execution"

**Solution:** At any checkpoint, choose "Adjust" or "Spike"

```
CHECKPOINT: Analysis Complete

You: "Adjust: Let's use caching instead of optimization"

→ Copilot adjusts approach
```

---

### "The workflow stopped unexpectedly"

**Cause:** Auto-stop condition triggered (safety violation, high risk, low confidence)

**What to do:**
1. Read the stop reason
2. Address the issue
3. Resume or start fresh

```
AUTOMATIC STOP: Safety Violation
Reason: Public API change requires justification

You: "Spike: Investigate alternative that doesn't change API"

→ Copilot investigates alternatives
```

---

## Summary

### Key Principles

1. **Autonomous by default** - Fast execution for low-risk work
2. **Flags enable control** - Add checkpoints where needed
3. **Risk-aware pausing** - Automatic stops for high-risk situations
4. **Flexible modes** - From fully autonomous to step-by-step
5. **Safety preserved** - Some stops are non-negotiable

### Flag Quick Reference

```yaml
approve_before_stage: [6]        # Pause before specific stages
approve_at_risk: medium          # Pause if risk threshold met
approve_before_skills: [skill]   # Pause before specific skills
manual_mode: true                # Approve every stage
checkpoint_strategy: both        # Automatic checkpoint placement
```

### Execution Modes

```yaml
Autonomous: No flags → Full batch execution
Hybrid:     Some flags → Checkpoints at specified points
Manual:     manual_mode: true → Approve every stage
```

**The system adapts to your needs: fast when safe, careful when necessary.**
