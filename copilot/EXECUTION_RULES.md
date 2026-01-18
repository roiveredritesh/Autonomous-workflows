# Execution Rules

## Purpose

This document defines the **non-negotiable rules** that govern autonomous workflow execution. These rules ensure safety, consistency, and predictability across all agents and execution modes.

---

## Rule Categories

1. **Flag Validation Rules** - Ensure flags are valid and compatible
2. **Execution Rules** - Define mandatory execution behavior
3. **Safety Rules** - Non-negotiable safety constraints
4. **Stage Transition Rules** - When stages can proceed
5. **Checkpoint Rules** - When checkpoints are mandatory
6. **Agent Selection Rules** - How to select the correct agent
7. **Skill Invocation Rules** - When and how skills execute
8. **Risk Assessment Rules** - How risk affects execution
9. **Conflict Resolution Rules** - How to handle conflicts
10. **Escalation Rules** - When to switch modes

---

## 1. Flag Validation Rules

### Rule 1.1: Flag Type Validation

**Rule:** All flags must conform to their defined types

```yaml
MUST:
  approve_before_stage: array[integer] where 1 <= value <= 9
  approve_at_risk: string in [low, medium, high] or null
  approve_before_skills: array[string] where each is valid skill name
  manual_mode: boolean
  checkpoint_strategy: string in [analysis_only, planning_only, both, none] or null

MUST_NOT:
  approve_before_stage: [0, 10, "six"]  # Invalid: out of range, wrong type
  approve_at_risk: "critical"           # Invalid: not in allowed values
  manual_mode: "yes"                    # Invalid: must be boolean
```

**Enforcement:** Parser MUST reject invalid flag values with clear error message

**Error Message Format:**
```
Invalid flag: {flag_name}
Provided: {value}
Expected: {type} in {valid_range/values}
```

---

### Rule 1.2: Flag Conflict Detection

**Rule:** Conflicting flags MUST be detected and resolved

```yaml
CONFLICTS:
  manual_mode_overrides_all:
    if: manual_mode == true
    then: ignore all other flags
    reason: "Manual mode provides complete control"
    action: Warn user, use manual_mode only

  duplicate_checkpoints:
    if: approve_before_stage contains stage X AND checkpoint_strategy triggers at stage X
    then: Use single checkpoint, don't duplicate
    reason: "Avoid double-pausing at same stage"
    action: Merge checkpoint reasons

  impossible_combinations:
    if: checkpoint_strategy == none AND approve_before_stage is not empty
    then: Use approve_before_stage, ignore checkpoint_strategy
    reason: "Explicit stage flags override strategy"
    action: Warn user of conflict
```

**Enforcement:** Orchestrator MUST detect conflicts before execution starts

---

### Rule 1.3: Flag Default Application

**Rule:** Missing flags MUST receive default values

```yaml
DEFAULTS:
  approve_before_stage: []           # Empty array = no stage-based pauses
  approve_at_risk: null              # Null = no risk-based pausing
  approve_before_skills: []          # Empty array = no skill-based pauses
  manual_mode: false                 # Default to autonomous
  checkpoint_strategy: null          # Use agent defaults
```

**Enforcement:** Parser MUST apply defaults before execution begins

---

## 2. Execution Rules

### Rule 2.1: Batch Execution Requirement

**Rule:** Stages within a batch MUST execute together unless interrupted

```yaml
MUST:
  - Execute all stages in batch sequentially
  - Compile results from all stages
  - Present consolidated output at batch end

MUST_NOT:
  - Pause between stages within same batch (unless auto-stop triggered)
  - Present individual stage outputs separately during batch
  - Skip stages within batch without justification

EXCEPTION:
  - Auto-stop conditions can interrupt batch execution
  - Safety violations MUST stop immediately regardless of batch
```

**Example:**
```yaml
batch_stages:
  analysis: [1, 2, 3, 4, 5]

# Execution MUST:
# 1. Execute stages 1, 2, 3, 4, 5 sequentially
# 2. Compile all results
# 3. Present once at end (unless stopped)

# Execution MUST_NOT:
# - Pause after stage 2 within batch
# - Ask for approval between stages 3 and 4
```

---

### Rule 2.2: Checkpoint Presentation Format

**Rule:** Checkpoints MUST present complete information in standard format

```yaml
REQUIRED_CHECKPOINT_ELEMENTS:
  - checkpoint_name: string
  - stages_completed: array[integer]
  - consolidated_results: object
  - risk_assessment: {level, factors}
  - confidence: {level, reasoning}
  - decision_required: boolean
  - options: array[{label, description}]
  - next_steps: string

MUST_INCLUDE:
  - All results from completed stages
  - Current risk level and factors
  - Clear decision question
  - Available response options
  - What happens if approved

MUST_NOT:
  - Present incomplete results
  - Hide risk factors
  - Omit available options
  - Continue without user response
```

**Template:**
```yaml
===== CHECKPOINT: {name} =====

STAGES COMPLETED: {list}

CONSOLIDATED RESULTS:
{all stage outputs}

RISK ASSESSMENT:
  Level: {LOW|MEDIUM|HIGH}
  Factors: {list}

CONFIDENCE: {HIGH|MEDIUM|LOW}

DECISION REQUIRED:
  Question: {specific question}

  Options:
    [ ] Approve - {what happens}
    [ ] Adjust - {what can change}
    [ ] Spike - {investigation}
    [ ] Reject - {stop workflow}

NEXT STEPS IF APPROVED:
{clear description}

==============================
```

---

### Rule 2.3: Sequential Stage Execution

**Rule:** Stages MUST execute in numerical order within batch

```yaml
MUST:
  - Execute stage 1 before stage 2
  - Execute stage 2 before stage 3
  - Complete stage N before stage N+1

MUST_NOT:
  - Skip stages without justification
  - Execute stages out of order
  - Parallelize stages (they may depend on each other)

ALLOWED:
  - Stop at any stage due to auto-stop condition
  - Escalate to different mode if needed (SPIKE, REFINEMENT)
```

---

## 3. Safety Rules (Non-Negotiable)

### Rule 3.1: Automatic Safety Stops

**Rule:** Safety violations MUST trigger immediate stop, regardless of flags

```yaml
MANDATORY_STOPS:

  public_api_change:
    condition: "Public API signature change detected"
    action: STOP IMMEDIATELY
    override: NEVER
    message: "Public API change requires explicit justification"
    required: Documented justification or alternative approach

  webforms_lifecycle_violation:
    condition: "WebForms page lifecycle rules violated"
    action: STOP IMMEDIATELY
    override: NEVER
    message: "WebForms lifecycle violation detected"
    required: Fix violation or explain why safe

  telerik_contract_break:
    condition: "Telerik control contract broken"
    action: STOP IMMEDIATELY
    override: NEVER
    message: "Telerik control contract violation"
    required: Restore contract compatibility

  missing_rollback:
    condition: "No rollback procedure possible"
    action: STOP IMMEDIATELY
    override: NEVER
    message: "Cannot create rollback procedure"
    required: Make change reversible or justify irreversibility

  data_corruption_risk:
    condition: "Data corruption possible"
    action: STOP IMMEDIATELY
    override: NEVER
    message: "Data corruption risk detected"
    required: Add validation/transaction safety
```

**Enforcement:** ANY agent detecting these conditions MUST stop execution immediately

**Priority:** Safety rules override ALL flags including `manual_mode: false` or "skip safety"

---

### Rule 3.2: Risk-Based Mandatory Stops

**Rule:** HIGH risk MUST trigger checkpoint regardless of flags

```yaml
HIGH_RISK_STOP:
  condition: risk_level == HIGH
  action: AUTOMATIC CHECKPOINT
  override: Cannot be disabled
  message: "HIGH RISK: Review required"

  required_elements:
    - Risk description
    - Risk factors
    - Mitigation options
    - Recommendation
    - User approval

CANNOT:
  - Continue without user approval when risk is HIGH
  - Hide HIGH risk from user
  - Automatically approve HIGH risk changes
```

---

### Rule 3.3: Confidence-Based Escalation

**Rule:** LOW confidence MUST escalate to appropriate mode

```yaml
LOW_CONFIDENCE_ESCALATION:
  condition: confidence == LOW
  action: ESCALATE TO SPIKE or REFINEMENT
  reason: "Cannot proceed with low confidence"

  escalate_to_spike_when:
    - Technical approach unclear
    - Performance impact unknown
    - Legacy behavior undocumented
    - Proof of concept needed

  escalate_to_refinement_when:
    - Requirements unclear
    - Acceptance criteria missing
    - Scope ambiguous
    - Conflicting requirements

CANNOT:
  - Proceed with implementation when confidence is LOW
  - Guess at unclear requirements
  - Assume undocumented behavior
```

---

## 4. Stage Transition Rules

### Rule 4.1: Stage Completion Criteria

**Rule:** Stage MUST meet completion criteria before transitioning

```yaml
STAGE_COMPLETION_REQUIREMENTS:

  every_stage_must:
    - Execute all required skills
    - Produce structured output
    - Assess risk level
    - Determine confidence
    - Document decisions

  cannot_transition_if:
    - Required skills failed
    - Output is incomplete
    - Critical information missing
    - Safety violation detected

STAGE_SPECIFIC:

  stage_1_intake:
    must_have:
      - Valid ticket/request
      - Basic requirements
      - Mode detection (FEATURE, BUG, etc.)

  stage_3_feasibility:
    must_have:
      - Feasibility assessment (HIGH/MEDIUM/LOW)
      - Risk level (LOW/MEDIUM/HIGH)
      - Technical approach identified

  stage_6_implementation:
    must_have:
      - File-by-file change plan
      - Line count estimates
      - Safe change boundaries identified
```

---

### Rule 4.2: Checkpoint Enforcement

**Rule:** Execution MUST pause at flagged checkpoints

```yaml
CHECKPOINT_ENFORCEMENT:

  if_approve_before_stage_contains_N:
    before_executing_stage_N:
      - Present all results from previous stages
      - Request user approval
      - Wait for response
      - Do NOT continue without approval

  if_approve_at_risk_threshold_met:
    when_risk_reaches_threshold:
      - STOP immediately
      - Present risk analysis
      - Request decision
      - Do NOT continue without approval

  if_manual_mode_true:
    after_each_stage:
      - Present stage result
      - Request approval
      - Wait for response
      - Continue to next stage only if approved
```

**Enforcement:** Orchestrator MUST NOT bypass checkpoints

---

### Rule 4.3: Skip Prevention

**Rule:** Stages CANNOT be skipped without documented justification

```yaml
SKIP_RULES:

  allowed_skips:
    - Stage not applicable (e.g., no cache impact)
    - Mode doesn't require stage (e.g., SPIKE mode)
    - Escalation to different mode (SPIKE, REFINEMENT, HOTFIX)

  must_document_when_skipping:
    - Which stage skipped
    - Why not applicable
    - What validation confirms it's safe to skip

  cannot_skip:
    - Stage 1 (Intake) - NEVER skip
    - Stage 3 (Feasibility/Risk) - NEVER skip
    - Safety verification stages - NEVER skip
    - Stages flagged by user - NEVER skip
```

---

## 5. Checkpoint Rules

### Rule 5.1: Mandatory Checkpoint Triggers

**Rule:** Certain conditions MUST trigger checkpoints

```yaml
MANDATORY_CHECKPOINTS:

  safety_violation:
    trigger: ANY safety rule violated
    action: IMMEDIATE CHECKPOINT
    cannot_continue_without: Violation resolved or justified

  high_risk:
    trigger: risk_level == HIGH
    action: AUTOMATIC CHECKPOINT
    cannot_continue_without: User approval

  low_confidence:
    trigger: confidence == LOW
    action: ESCALATE (SPIKE or REFINEMENT)
    cannot_continue_without: Confidence raised or issue resolved

  conflicting_requirements:
    trigger: Contradictory requirements detected
    action: ESCALATE TO REFINEMENT
    cannot_continue_without: Conflict resolved

  production_change:
    trigger: mode == HOTFIX
    action: CHECKPOINT AFTER EVERY STAGE
    cannot_continue_without: User approval per stage
    reason: "Production changes require maximum oversight"

  flag_specified_checkpoint:
    trigger: approve_before_stage contains current_stage
    action: CHECKPOINT
    cannot_continue_without: User approval
```

---

### Rule 5.2: Checkpoint Response Handling

**Rule:** User responses MUST be handled according to type

```yaml
RESPONSE_HANDLING:

  approve:
    recognized_inputs: [approve, yes, continue, proceed, go ahead]
    action: Continue execution from checkpoint
    preserve: All completed work
    respect: Remaining flags and checkpoints

  adjust:
    recognized_inputs: [adjust, modify, change, adjust: <details>]
    action:
      - Parse adjustment request
      - Modify affected parameters
      - Re-run impacted stages
      - Continue from adjusted state
    preserve: Unaffected work
    re_execute: Only affected stages

  spike:
    recognized_inputs: [spike, investigate, need more info, spike: <question>]
    action:
      - Switch to SPIKE mode
      - Time-box investigation (default 4 hours)
      - Return with findings
      - Resume or restart based on findings
    preserve: All analysis done so far

  reject:
    recognized_inputs: [reject, stop, cancel, different approach]
    action:
      - Stop workflow
      - Preserve all work done
      - Document rejection reason
      - Allow restart with different approach
    preserve: All completed work for reference

  unknown_response:
    action:
      - Do NOT guess intent
      - Request clarification
      - Re-present checkpoint with clearer options
    must_not: Continue without clear approval
```

---

### Rule 5.3: Checkpoint Timeout

**Rule:** Checkpoints MUST handle timeout scenarios

```yaml
CHECKPOINT_TIMEOUT:

  behavior:
    - Checkpoints do NOT auto-approve
    - Wait indefinitely for user response
    - Preserve state while waiting
    - Allow resumption at any time

  must_not:
    - Timeout and continue without approval
    - Assume approval after delay
    - Lose checkpoint state

  on_session_end:
    - Preserve checkpoint state
    - Allow resumption in new session
    - Re-present same checkpoint
```

---

## 6. Agent Selection Rules

### Rule 6.1: Mode Detection Priority

**Rule:** Mode MUST be detected using priority rules

```yaml
MODE_DETECTION_PRIORITY:

  1_explicit_mode:
    trigger: User explicitly states mode
    examples:
      - "HOTFIX: Orders failing"
      - "SPIKE: Investigate cache behavior"
    action: Use explicitly stated mode
    confidence: HIGH

  2_keyword_detection:
    trigger: Keywords indicate mode
    keywords:
      HOTFIX: [production, urgent, critical, emergency, down]
      BUG: [bug, defect, fix, broken, error, failing]
      FEATURE: [add, new, implement, create, enhance]
      PERFORMANCE: [slow, optimize, performance, speed up]
      SPIKE: [investigate, research, explore, understand]
      REFINEMENT: [unclear, vague, need clarification]
    action: Detect mode from keywords
    confidence: MEDIUM to HIGH

  3_pattern_analysis:
    trigger: Request pattern suggests mode
    patterns:
      "Why does X happen?" → SPIKE
      "X returns wrong results" → BUG
      "X takes 30 seconds" → PERFORMANCE
      "Add ability to X" → FEATURE
    action: Infer mode from pattern
    confidence: MEDIUM

  4_confidence_check:
    if: confidence < MEDIUM
    then: Escalate to REFINEMENT
    reason: "Cannot determine mode with confidence"
```

---

### Rule 6.2: Mode-Agent Mapping

**Rule:** Each mode MUST map to exactly one agent

```yaml
MODE_AGENT_MAPPING:
  FEATURE: feature-delivery
  BUG: bug-fix
  HOTFIX: hotfix
  PERFORMANCE: performance
  SPIKE: spike
  REFINEMENT: story-refinement

MUST:
  - Use correct agent for detected mode
  - Apply agent's default execution configuration
  - Merge user flags with agent defaults

MUST_NOT:
  - Use wrong agent for mode
  - Skip mode detection
  - Guess at uncertain mode
```

---

### Rule 6.3: Mode Escalation

**Rule:** Agents MUST escalate when conditions warrant different mode

```yaml
ESCALATION_TRIGGERS:

  bug_to_hotfix:
    condition: severity == CRITICAL && environment == production
    action: Escalate to HOTFIX mode
    reason: "Production critical issues need hotfix workflow"

  any_to_spike:
    condition: confidence == LOW || technical_approach == unknown
    action: Escalate to SPIKE mode
    reason: "Need investigation before proceeding"

  any_to_refinement:
    condition: requirements == unclear || conflicting_requirements
    action: Escalate to REFINEMENT mode
    reason: "Need requirements clarity before proceeding"

  bug_to_feature:
    condition: scope_larger_than_bug_fix
    action: Escalate to FEATURE mode
    reason: "Scope suggests feature work, not bug fix"
```

---

## 7. Skill Invocation Rules

### Rule 7.1: Skill Execution Requirements

**Rule:** Skills MUST be invoked with complete input

```yaml
SKILL_INVOCATION_REQUIREMENTS:

  must_provide:
    - Skill name (exact match from catalog)
    - Context (why skill is needed)
    - Input parameters (complete and valid)
    - Expected output format

  must_validate:
    - Skill exists in catalog
    - All required parameters provided
    - Parameter types correct
    - Agent has permission to invoke skill

  cannot_invoke_if:
    - Skill name unknown
    - Required parameters missing
    - approve_before_skills flag set for this skill AND not approved
```

---

### Rule 7.2: Skill Output Validation

**Rule:** Skill outputs MUST be validated before use

```yaml
SKILL_OUTPUT_VALIDATION:

  must_contain:
    - Structured result (not free-form text only)
    - Risk assessment
    - Confidence level
    - Relevant findings

  must_validate:
    - Output is complete
    - Output matches expected schema
    - Confidence level provided
    - Risk assessment included

  if_skill_fails:
    determine_criticality:
      critical: Cannot proceed without skill output
      non_critical: Can proceed with degraded information

    if_critical:
      - STOP workflow
      - Report skill failure
      - Suggest alternatives or manual execution

    if_non_critical:
      - Log warning
      - Continue with noted limitation
      - Document missing information
```

---

### Rule 7.3: Skill Approval Gates

**Rule:** Skills flagged for approval MUST pause before execution

```yaml
SKILL_APPROVAL_GATES:

  if_approve_before_skills_contains_skill_name:
    before_invoking_skill:
      - Present skill purpose
      - Explain expected impact
      - Show input parameters
      - Request approval
      - Do NOT invoke without approval

  checkpoint_format:
    skill_name: {name}
    purpose: {why needed}
    input: {parameters}
    expected_output: {what it will return}
    impact: {side effects, if any}

    question: "Approve execution of {skill_name}?"
    options: [Approve, Skip, Alternative]
```

---

## 8. Risk Assessment Rules

### Rule 8.1: Risk Level Calculation

**Rule:** Risk level MUST be calculated using defined factors

```yaml
RISK_FACTORS:

  technical_complexity:
    LOW: Simple, well-understood pattern
    MEDIUM: Moderate complexity, some unknowns
    HIGH: Complex, many unknowns, untested approach

  impact_scope:
    LOW: Single file, isolated change
    MEDIUM: Multiple files, related components
    HIGH: System-wide, public API, database schema

  reversibility:
    LOW: Easily reversible (config, feature flag)
    MEDIUM: Reversible with effort (code revert)
    HIGH: Difficult to reverse (data migration, schema change)

  production_risk:
    LOW: No production impact, dev/test only
    MEDIUM: Production change, low traffic area
    HIGH: Production change, high traffic or critical path

  data_risk:
    LOW: Read-only, no data changes
    MEDIUM: Data updates, transactional
    HIGH: Data migration, schema change, potential corruption

RISK_CALCULATION:
  if ANY factor == HIGH:
    overall_risk = HIGH

  elif MOST factors == MEDIUM:
    overall_risk = MEDIUM

  elif ALL factors == LOW:
    overall_risk = LOW

  else:
    overall_risk = MEDIUM (conservative default)
```

---

### Rule 8.2: Risk-Based Checkpoint Triggers

**Rule:** Risk threshold MUST trigger checkpoint when met

```yaml
RISK_CHECKPOINT_TRIGGERS:

  if_approve_at_risk_is_low:
    trigger_on: risk_level >= LOW
    meaning: Pause on LOW, MEDIUM, or HIGH risk

  if_approve_at_risk_is_medium:
    trigger_on: risk_level >= MEDIUM
    meaning: Pause on MEDIUM or HIGH risk only

  if_approve_at_risk_is_high:
    trigger_on: risk_level == HIGH
    meaning: Pause only on HIGH risk

  if_approve_at_risk_is_null:
    trigger_on: NEVER (unless other conditions)
    meaning: No risk-based pausing

COMPARISON:
  LOW < MEDIUM < HIGH

ENFORCEMENT:
  - Check risk after each stage
  - If threshold met, trigger checkpoint immediately
  - Present risk analysis at checkpoint
  - Require user decision to continue
```

---

### Rule 8.3: Risk Mitigation Documentation

**Rule:** High-risk changes MUST document mitigation

```yaml
HIGH_RISK_DOCUMENTATION_REQUIRED:

  must_document:
    - What makes this high risk
    - Risk factors identified
    - Mitigation strategies available
    - Recommended mitigation
    - Why recommendation chosen
    - Validation plan
    - Rollback procedure

  cannot_proceed_with_high_risk_without:
    - Documented risk factors
    - Identified mitigation
    - User approval of approach
    - Rollback plan
```

---

## 9. Conflict Resolution Rules

### Rule 9.1: Flag Priority Order

**Rule:** Conflicting flags MUST be resolved using priority order

```yaml
PRIORITY_ORDER (Highest to Lowest):

  1_manual_mode:
    priority: HIGHEST
    behavior: Overrides ALL other flags
    reason: "Explicit full control requested"
    action: Ignore all other flags, pause after every stage

  2_safety_violations:
    priority: VERY_HIGH
    behavior: Cannot be overridden
    reason: "Non-negotiable safety"
    action: Stop immediately regardless of flags

  3_high_risk_auto_stop:
    priority: HIGH
    behavior: Cannot be disabled
    reason: "High risk requires review"
    action: Checkpoint regardless of flags

  4_approve_at_risk:
    priority: MEDIUM_HIGH
    behavior: Triggers on risk threshold
    reason: "User-requested risk-based pausing"
    action: Checkpoint when threshold met

  5_approve_before_stage:
    priority: MEDIUM
    behavior: Explicit stage-based checkpoints
    reason: "User-specified pause points"
    action: Checkpoint before specified stages

  6_approve_before_skills:
    priority: MEDIUM_LOW
    behavior: Skill-specific approvals
    reason: "User-specified skill gates"
    action: Checkpoint before specified skills

  7_checkpoint_strategy:
    priority: LOW
    behavior: General checkpoint placement
    reason: "General strategy preference"
    action: Checkpoint per strategy

  8_agent_defaults:
    priority: LOWEST
    behavior: Agent's default checkpoints
    reason: "Fallback if no user flags"
    action: Use agent's default configuration
```

---

### Rule 9.2: Checkpoint Deduplication

**Rule:** Multiple checkpoints at same stage MUST be merged

```yaml
CHECKPOINT_MERGING:

  if_multiple_triggers_at_same_stage:
    action: Merge into single checkpoint
    combine:
      - All trigger reasons
      - All relevant information
      - All decision options
    present: Single consolidated checkpoint

  example:
    approve_before_stage: [6]
    checkpoint_strategy: analysis_only (also stage 6)

    result:
      Single checkpoint before stage 6 with reasons:
        - "User requested checkpoint before stage 6"
        - "Analysis complete per checkpoint strategy"

MUST_NOT:
  - Present two checkpoints at same stage
  - Ask for approval twice for same stage
  - Duplicate checkpoint presentation
```

---

### Rule 9.3: Impossible Configuration Rejection

**Rule:** Logically impossible configurations MUST be rejected

```yaml
IMPOSSIBLE_CONFIGURATIONS:

  cannot_have:
    - manual_mode: true AND checkpoint_strategy: none
      reason: "Conflicting: manual mode IS a checkpoint strategy"
      resolution: Use manual_mode, ignore checkpoint_strategy

    - approve_before_stage: [10]
      reason: "Stage 10 doesn't exist (only 1-9)"
      resolution: Reject with error message

    - approve_at_risk: "critical"
      reason: "Invalid risk level (only low/medium/high)"
      resolution: Reject with error message

    - approve_before_skills: ["unknown-skill"]
      reason: "Skill doesn't exist in catalog"
      resolution: Reject with error message listing available skills

ENFORCEMENT:
  - Validate during flag parsing
  - Reject before execution starts
  - Provide clear error messages
  - Suggest corrections
```

---

## 10. Escalation Rules

### Rule 10.1: Automatic Mode Escalation

**Rule:** Certain conditions MUST trigger mode escalation

```yaml
AUTOMATIC_ESCALATION:

  to_hotfix:
    conditions:
      - severity == CRITICAL
      - environment == production
      - current_mode == BUG
    action: Escalate BUG to HOTFIX
    reason: "Production critical issues need emergency workflow"
    apply: HOTFIX agent configuration (manual mode by default)

  to_spike:
    conditions:
      - confidence == LOW
      - technical_approach == unknown
      - OR: root_cause == unknown
      - OR: performance_impact == unknown
    action: Escalate ANY mode to SPIKE
    reason: "Need investigation before proceeding"
    apply: Time-boxed investigation (default 4 hours)

  to_refinement:
    conditions:
      - requirements == unclear
      - OR: conflicting_requirements == true
      - OR: scope == ambiguous
    action: Escalate ANY mode to REFINEMENT
    reason: "Need requirements clarity"
    apply: Refinement workflow to clarify requirements

  to_feature:
    conditions:
      - current_mode == BUG
      - scope_larger_than_bug_fix == true
    action: Escalate BUG to FEATURE
    reason: "Scope suggests feature work, not simple fix"
    apply: Feature delivery workflow

MUST:
  - Detect escalation conditions immediately
  - Notify user of escalation with reason
  - Switch to appropriate agent
  - Preserve work done so far
  - Resume or restart based on escalation type
```

---

### Rule 10.2: User-Requested Escalation

**Rule:** User spike/refinement requests MUST be honored

```yaml
USER_ESCALATION_HANDLING:

  at_checkpoint_user_says_spike:
    action:
      - Acknowledge spike request
      - Switch to SPIKE mode
      - Define investigation question
      - Set time box (default 4 hours)
      - Execute investigation
      - Return with findings
      - Allow user to: resume, restart, or change approach

  at_checkpoint_user_says_need_more_info:
    action:
      - Treat as REFINEMENT request
      - Switch to REFINEMENT mode
      - Ask clarifying questions
      - Refine requirements
      - Return to original mode with clarified requirements

MUST:
  - Honor user escalation requests
  - Preserve all work done before escalation
  - Allow resumption after escalation
  - Document escalation reason and findings
```

---

### Rule 10.3: Escalation Documentation

**Rule:** Escalations MUST be documented

```yaml
ESCALATION_DOCUMENTATION:

  must_record:
    - Original mode
    - New mode
    - Escalation trigger (automatic or user-requested)
    - Reason for escalation
    - Work preserved from original workflow
    - Escalation outcome (findings, clarifications)
    - Resumption decision (resume, restart, change approach)

  format:
    escalation:
      from_mode: {original}
      to_mode: {new}
      trigger: {automatic|user_requested}
      reason: {explanation}
      preserved_work: {stages completed}
      outcome: {what was learned/clarified}
      next_action: {resume|restart|change_approach}
```

---

## Rule Enforcement Matrix

### Who Enforces Each Rule Category

```yaml
ENFORCEMENT_RESPONSIBILITY:

  orchestrator_enforces:
    - Flag validation rules
    - Agent selection rules
    - Mode detection rules
    - Conflict resolution rules
    - Escalation rules (detection and initiation)

  all_agents_enforce:
    - Safety rules
    - Risk assessment rules
    - Stage transition rules
    - Checkpoint rules
    - Execution rules

  skills_enforce:
    - Skill invocation rules (input validation)
    - Skill output validation

  system_enforces:
    - Checkpoint timeout rules
    - Response handling rules
    - Deduplication rules
```

---

## Rule Violation Handling

### What Happens When Rules Are Violated

```yaml
VIOLATION_HANDLING:

  safety_rule_violation:
    action: IMMEDIATE STOP
    cannot_override: true
    user_action: Fix violation or change approach
    cannot_continue_without: Violation resolved

  execution_rule_violation:
    action: STOP at violation point
    present: Error message and rule violated
    user_action: Adjust approach to comply with rule
    can_retry: true

  flag_validation_violation:
    action: REJECT before execution starts
    present: Clear error message
    user_action: Correct flags
    can_retry: true

  checkpoint_rule_violation:
    action: Enforce checkpoint anyway
    reason: "Checkpoint rules protect user control"
    cannot_bypass: true

  risk_rule_violation:
    action: STOP and present risk
    reason: "Risk rules protect safety"
    cannot_bypass: true
```

---

## Summary

### Rule Categories

1. ✅ **Flag Validation** - Ensure flags are valid
2. ✅ **Execution** - Define execution behavior
3. ✅ **Safety** - Non-negotiable safety constraints
4. ✅ **Stage Transition** - When stages can proceed
5. ✅ **Checkpoint** - When checkpoints are mandatory
6. ✅ **Agent Selection** - How to select correct agent
7. ✅ **Skill Invocation** - When and how skills execute
8. ✅ **Risk Assessment** - How risk affects execution
9. ✅ **Conflict Resolution** - How to handle conflicts
10. ✅ **Escalation** - When to switch modes

### Key Principles

- **Safety First** - Safety rules override everything
- **Explicit Over Implicit** - User flags override defaults
- **Fail Secure** - When in doubt, checkpoint
- **Predictable** - Same input produces same behavior
- **Enforceable** - All rules are automatically enforced

### Non-Negotiable Rules

Cannot be overridden under any circumstances:
- Safety violations → IMMEDIATE STOP
- HIGH risk → AUTOMATIC CHECKPOINT
- LOW confidence → ESCALATE
- Production hotfixes → Manual mode
- Missing rollback → STOP

**These rules make the autonomous system safe, predictable, and controllable.**
