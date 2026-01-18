# Execution Control Specification

## Purpose
Defines how the autonomous hybrid execution model operates in practice.

---

## Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    EXECUTION FLOW                            │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  User Input + Optional Flags                                 │
│           ↓                                                   │
│  Orchestrator (parse flags, detect mode)                     │
│           ↓                                                   │
│  Target Agent (configured with flags)                        │
│           ↓                                                   │
│  ┌───────────────────┐                                       │
│  │ AUTONOMOUS BATCH  │                                       │
│  │ Execute Stages    │                                       │
│  │ Invoke Skills     │                                       │
│  │ Compile Results   │                                       │
│  └───────────────────┘                                       │
│           ↓                                                   │
│  Check Stop Conditions                                       │
│           ↓                                                   │
│  ┌─────────────┐     ┌──────────────┐                       │
│  │ Safe?       │ NO  │ CHECKPOINT   │                       │
│  │ Flag set?   ├────→│ Request      │                       │
│  │ Risk high?  │     │ Approval     │                       │
│  └──────┬──────┘     └──────┬───────┘                       │
│         │ YES               │                                 │
│         ↓                   ↓                                 │
│    Continue             Wait for User                        │
│                             │                                 │
│                             ↓                                 │
│                      ┌──────────────┐                        │
│                      │ User Decision│                        │
│                      └──────┬───────┘                        │
│                             ↓                                 │
│              Approve/Adjust/Spike/Reject                     │
│                             │                                 │
│                             ↓                                 │
│                      Continue or Stop                        │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## Execution Modes

### Mode 1: Full Autonomous (Default)

**Trigger:** No flags provided

**Behavior:**
```yaml
execute:
  - All analysis stages (1-5) in batch
  - All planning stages (6-9) in batch
  - All necessary skills automatically
  
pause_only_if:
  - Risk level: HIGH
  - Confidence: LOW
  - Safety violation detected
  - Unknown behavior encountered
  
output:
  - Complete consolidated analysis and plan
  - Single response with all results
  - Time: 30-90 seconds typically
```

**Example:**
```
User: "Add Excel export to customer list"

Agent: [Executes all stages]

Output after 45 seconds:
===================================
MODE: FEATURE
CONFIDENCE: HIGH

ANALYSIS COMPLETE (Stages 1-5):
- Requirements: [expanded criteria]
- Feasibility: HIGH
- Risk: LOW
- Legacy Impact: [detailed analysis]
- Data/Cache: [recommendations]

PLAN COMPLETE (Stages 6-9):
- Implementation: [minimal diff plan]
- Tests: [test scenarios]
- Documentation: [generated]
- Rollback: [procedure defined]

READY FOR: Implementation
===================================
```

---

### Mode 2: Checkpoint Before Implementation

**Trigger:** `approve_before_stage: [6]`

**Behavior:**
```yaml
execute:
  - Stages 1-5 in batch (analysis)
  
checkpoint:
  - Present analysis results
  - Request approval to continue
  - Wait for user response
  
if_approved:
  - Execute stages 6-9 (planning)
  - Return complete plan
```

**Example:**
```
User: "Add Excel export to customer list"
Flags:
  approve_before_stage: [6]

Agent: [Executes stages 1-5]

Output after 30 seconds:
===================================
CHECKPOINT: Analysis Complete

STAGES 1-5 COMPLETED:
[All analysis results]

DECISION REQUIRED:
Analysis shows LOW risk, HIGH feasibility.
Proceed with implementation planning?

[ ] Approve - Continue to stages 6-9
[ ] Adjust - Modify approach
[ ] Spike - Need investigation
[ ] Reject - Stop here
===================================

[User responds: "Approve"]

Agent: [Executes stages 6-9]

Output after 20 seconds:
===================================
PLANNING COMPLETE:
[Implementation plan, tests, docs, rollback]

READY FOR: Implementation
===================================
```

---

### Mode 3: Risk-Based Checkpoints

**Trigger:** `approve_at_risk: medium`

**Behavior:**
```yaml
execute:
  - Stages batch normally
  
monitor:
  - Track risk level at each stage
  
if_risk_threshold_met:
  - STOP immediately
  - Present risk analysis
  - Request decision
  
continue_if_approved:
  - Resume from stopped stage
```

**Example:**
```
User: "Optimize customer search query"
Flags:
  approve_at_risk: medium

Agent: [Executes stages 1-4]
Agent: [Stage 4 detects MEDIUM risk]

Output:
===================================
CHECKPOINT: Risk Threshold Reached

STAGES 1-4 COMPLETED:
- N+1 query detected
- Missing index identified
- RISK: MEDIUM (table scan on large table)

RISK FACTORS:
- Query affects 50K+ rows
- No index on filter column
- High traffic endpoint

MITIGATION AVAILABLE:
- Add index (low risk)
- Or optimize query (medium risk)

RECOMMENDATION: Proceed with index addition

DECISION REQUIRED:
Risk is MEDIUM. Review and approve?

[ ] Approve - Continue with recommended mitigation
[ ] Adjust - Choose different approach
[ ] Spike - Investigate alternatives
===================================
```

---

### Mode 4: Manual Step-by-Step

**Trigger:** `manual_mode: true`

**Behavior:**
```yaml
execute:
  - One stage at a time
  
checkpoint_after_each:
  - Present stage result
  - Request approval
  - Wait for response
  
repeat:
  - For all 9 stages
```

**Example:**
```
User: "Add Excel export"
Flags:
  manual_mode: true

Agent: [Executes stage 1]
Output:
===== STAGE 1 COMPLETE =====
Ticket validated: PROJ-1234
Continue to stage 2?
============================

[User: "Yes"]

Agent: [Executes stage 2]
Output:
===== STAGE 2 COMPLETE =====
Acceptance criteria expanded: [...]
Continue to stage 3?
============================

[Repeat for stages 3-9]
```

---

## Flag Syntax Reference

### Flag Structure

Flags are provided as structured data with user input:

```yaml
# Option 1: Inline with request
User: "Add Excel export to customer list [approve_before_stage: 6]"

# Option 2: Separate declaration
Request: "Add Excel export to customer list"
Flags:
  approve_before_stage: [6]

# Option 3: Multiple flags
Request: "Optimize query performance"
Flags:
  approve_at_risk: medium
  approve_before_skills: [sql-execution-analyzer]
```

### Available Flags

```yaml
approve_before_stage:
  type: list[int]
  description: "Pause before executing these stage numbers"
  example: [6, 9]
  usage: "Stop before implementation planning and before final rollback"

approve_at_risk:
  type: string
  values: [low, medium, high]
  description: "Pause if risk meets or exceeds this level"
  example: medium
  usage: "Stop if risk is medium or higher"

approve_before_skills:
  type: list[string]
  description: "Pause before executing these specific skills"
  example: [linq-query-tracer, redis-cache-strategy-analyzer]
  usage: "Stop before expensive or critical skill invocations"

manual_mode:
  type: boolean
  description: "Require approval after every stage"
  example: true
  usage: "Full manual control, approve each stage"

checkpoint_strategy:
  type: string
  values: [analysis_only, planning_only, both, none]
  description: "Where to place automatic checkpoints"
  example: both
  usage: "Stop after analysis and after planning"
```

---

## Automatic Stop Conditions

These trigger checkpoints **regardless of flags**:

```yaml
safety_violations:
  - Public API change without justification
  - WebForms lifecycle violation
  - Telerik contract breakage
  - Missing Redis invalidation
  - Unobservable SQL behavior
  - Impossible rollback
  
  action: IMMEDIATE STOP
  output: "SAFETY VIOLATION: [description]"

high_risk:
  - Risk level: HIGH
  - Data corruption possible
  - Performance degradation likely
  - Breaking change required
  
  action: AUTOMATIC CHECKPOINT
  output: "HIGH RISK: Review required"

low_confidence:
  - Confidence: LOW
  - Unknown behavior encountered
  - Contradictory requirements
  - Missing critical information
  
  action: ESCALATE TO SPIKE
  output: "LOW CONFIDENCE: Investigation needed"

conflicting_requirements:
  - Multiple contradictory acceptance criteria
  - Incompatible constraints
  - Unclear priorities
  
  action: ESCALATE TO REFINEMENT
  output: "CONFLICT: Clarification needed"
```

---

## Checkpoint Response Handling

### User Response Types

```yaml
approve:
  syntax: "approve" | "yes" | "continue" | "proceed"
  action:
    - Continue execution
    - Apply next batch
    - Respect remaining flags
  
adjust:
  syntax: "adjust" | "modify" | "change approach"
  action:
    - Present adjustment options
    - Allow parameter changes
    - Re-execute affected stages
  examples:
    - "Adjust: Use different TTL for cache"
    - "Adjust: Skip caching, use direct query"

spike:
  syntax: "spike" | "investigate" | "need more info"
  action:
    - Switch to SPIKE mode
    - Time-box investigation
    - Return with findings
  usage: "When uncertainty is high, need proof of concept"

reject:
  syntax: "reject" | "stop" | "cancel"
  action:
    - Stop workflow
    - Preserve work done
    - Document reason
  usage: "Approach not viable, need different solution"
```

### Response Processing

```python
def handle_checkpoint_response(response, context):
    """Process user response at checkpoint"""
    
    if response.lower() in ['approve', 'yes', 'continue', 'proceed']:
        return execute_next_batch(context)
    
    elif response.lower() in ['adjust', 'modify', 'change']:
        return present_adjustment_options(context)
    
    elif response.lower() in ['spike', 'investigate']:
        return switch_to_spike_mode(context)
    
    elif response.lower() in ['reject', 'stop', 'cancel']:
        return stop_workflow(context, reason=response)
    
    else:
        return clarify_response_needed()
```

---

## Batch Execution Strategy

### Analysis Batch (Stages 1-5)

**Purpose:** Gather all information before decisions

```yaml
batch_1_analysis:
  stages: [1, 2, 3, 4, 5]
  parallel_possible: partially
  
  stage_1_intake:
    - Validate ticket/request
    - Extract basic info
    
  stage_2_requirements:
    skill: acceptance-criteria-expander
    output: comprehensive criteria
    
  stage_3_feasibility:
    skill: feature-feasibility-analyzer
    assess: technical viability
    
  stage_4_legacy_impact:
    skills:
      - webforms-lifecycle-analyzer
      - telerik-impact-checker
      - safe-change-boundary-detector
    output: legacy safety assessment
    
  stage_5_data_cache:
    skills:
      - linq-query-tracer (if data)
      - redis-cache-strategy-analyzer (if cache)
    output: data/cache strategy
  
  consolidated_output:
    - All analysis results
    - Risk assessment
    - Confidence level
    - Ready for planning decision
```

### Planning Batch (Stages 6-9)

**Purpose:** Create implementation plan

```yaml
batch_2_planning:
  stages: [6, 7, 8, 9]
  depends_on: batch_1_approval
  
  stage_6_implementation:
    skill: minimal-diff-planner
    output: file-by-file change plan
    
  stage_7_testing:
    skills:
      - webforms-regression-analyzer
      - test-scenario-generator
    output: test plan
    
  stage_8_documentation:
    skills:
      - decision-record-creator
      - change-log-generator
      - risk-documenter
    output: documentation artifacts
    
  stage_9_rollback:
    skill: rollback-plan-generator
    output: rollback procedure
  
  consolidated_output:
    - Complete implementation plan
    - Test scenarios
    - Documentation
    - Rollback steps
    - Ready for execution
```

---

## Skill Execution in Batch

### Parallel Skill Invocation

When multiple skills are needed in a stage:

```yaml
stage_4_example:
  required_skills:
    - webforms-lifecycle-analyzer
    - telerik-impact-checker
    - safe-change-boundary-detector
  
  execution:
    type: sequential (skills may depend on each other)
    
  skill_1:
    name: webforms-lifecycle-analyzer
    input: page details
    output: lifecycle compliance
    
  skill_2:
    name: telerik-impact-checker
    input: control changes + skill_1 output
    output: telerik compatibility
    
  skill_3:
    name: safe-change-boundary-detector
    input: proposed changes
    output: safe modification points
  
  consolidate:
    - Combine all skill outputs
    - Assess overall legacy impact
    - Determine if safe to proceed
```

### Skill Output Aggregation

```yaml
aggregation_pattern:
  
  per_skill:
    skill_name: <n>
    input: <what was provided>
    output:
      result: <structured data>
      risks: [<list>]
      confidence: <level>
  
  aggregated:
    all_results: [<skill outputs>]
    combined_risks: [<deduplicated>]
    overall_confidence: <lowest confidence>
    recommendation: <proceed|investigate|stop>
```

---

## Error Handling

### Skill Execution Failure

```yaml
if_skill_fails:
  capture_error: true
  
  assess_impact:
    critical: "Cannot proceed without this skill"
    non_critical: "Can proceed with warnings"
  
  if_critical:
    - STOP workflow
    - Present error
    - Suggest alternatives
  
  if_non_critical:
    - Log warning
    - Continue with degraded info
    - Note in final output
```

### Stage Execution Failure

```yaml
if_stage_fails:
  identify_failure_point: <stage number>
  
  determine_cause:
    - Missing information
    - Skill failure
    - Safety violation
    - Unknown error
  
  action:
    - STOP at current stage
    - Present partial results
    - Request decision:
      [ ] Retry with more info
      [ ] Skip stage (if non-critical)
      [ ] Switch to SPIKE
      [ ] Abort workflow
```

---

## Performance Characteristics

### Expected Execution Times

```yaml
full_autonomous_mode:
  simple_feature: "30-60 seconds"
  complex_feature: "60-120 seconds"
  bug_fix: "20-40 seconds"
  performance_issue: "40-90 seconds"
  spike: "2-8 hours (time-boxed)"

with_checkpoints:
  analysis_batch: "20-40 seconds"
  wait_for_approval: "variable (human time)"
  planning_batch: "15-30 seconds"
  total: "35-70 seconds + human decision time"

manual_mode:
  per_stage: "5-15 seconds"
  total_stages: 9
  human_approvals: 9
  total: "45-135 seconds + 9 × human time"
```

### Optimization Tips

```yaml
minimize_latency:
  - Use analysis_only checkpoint strategy
  - Batch as much as possible
  - Only flag high-stakes decisions

maximize_control:
  - Use approve_at_risk: low
  - Flag critical skills
  - Review all legacy impacts

balance_speed_control:
  - Use approve_before_stage: [6]
  - Let analysis run autonomous
  - Approve before implementation
```

---

## Integration with Existing Agents

### Required Agent Updates

Each agent file needs this section added:

```yaml
# Add to agent.md header

---
execution_configuration:
  default_mode: autonomous
  
  batch_stages:
    analysis: [1, 2, 3, 4, 5]
    planning: [6, 7, 8, 9]
  
  default_checkpoints:
    - after_stage: 5
      reason: "Analysis complete, approve planning"
  
  auto_stop_triggers:
    - condition: risk_level == HIGH
      reason: "High risk requires review"
    - condition: confidence == LOW
      reason: "Low confidence needs investigation"
    - condition: safety_violation == true
      reason: "Safety violation must be addressed"
  
  respects_flags: true
---
```

### Orchestrator Integration

The orchestrator must:

```python
def orchestrator_main(user_input):
    # 1. Parse input and flags
    request, flags = parse_user_input(user_input)
    
    # 2. Detect mode
    mode = detect_mode(request)
    
    # 3. Load agent with flags
    agent = load_agent(mode, flags)
    
    # 4. Execute
    if flags.manual_mode:
        return execute_manual(agent, request)
    elif flags.has_checkpoints():
        return execute_with_checkpoints(agent, request, flags)
    else:
        return execute_autonomous(agent, request)
```

---

## Testing Strategy

### Test Scenarios

```yaml
test_1_full_autonomous:
  input: "Add Excel export"
  flags: none
  expected: Complete plan in single response
  
test_2_checkpoint_before_impl:
  input: "Add Excel export"
  flags: {approve_before_stage: [6]}
  expected: Checkpoint after stage 5
  
test_3_risk_based_stop:
  input: "Optimize slow query"
  flags: {approve_at_risk: medium}
  expected: Stop when medium risk detected
  
test_4_safety_violation:
  input: "Change public API contract"
  flags: none
  expected: Automatic stop at safety violation
  
test_5_manual_mode:
  input: "Add Excel export"
  flags: {manual_mode: true}
  expected: Checkpoint after each of 9 stages
```

---

## Summary

This execution model provides:

✅ **Speed:** Full autonomous execution for low-risk work
✅ **Control:** Flags enable intervention at any point
✅ **Safety:** Automatic stops for high-risk situations
✅ **Flexibility:** From fully autonomous to fully manual
✅ **Intelligence:** Risk-aware checkpoint placement
✅ **Efficiency:** Batch execution reduces latency
✅ **Transparency:** Clear checkpoints with consolidated results

**The system adapts to your needs: fast when safe, careful when necessary.**
