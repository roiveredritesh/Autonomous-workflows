---
version: 1.1.0
last_updated: 2026-03-07
purpose: Exact copy-paste templates for consistent outputs
usage: Reference this file when presenting checkpoints, skills, or errors
---

# Exact Templates for Autonomous Workflow System

Use these EXACT templates for all outputs. Copy and replace {placeholders}.

---

## Checkpoint Template

### Standard Checkpoint

**When to use:** At any flagged checkpoint or auto-stop condition

**Template:**
```
═══════════════════════════════════════════════════════════════
CHECKPOINT: {checkpoint_name}
═══════════════════════════════════════════════════════════════

STAGES COMPLETED: {stage_numbers}

CONSOLIDATED RESULTS:
{all_outputs_from_completed_stages}

RISK ASSESSMENT:
  Level: {LOW|MEDIUM|HIGH}
  Factors:
    - {risk_factor_1}
    - {risk_factor_2}
    - {risk_factor_3}

CONFIDENCE: {HIGH|MEDIUM|LOW}
  Reasoning: {why_this_confidence_level}

DECISION REQUIRED:
  {specific_question_for_user}

OPTIONS:
  [ ] Approve - {what_happens_if_approved}
  [ ] Adjust - {what_can_be_modified}
  [ ] Spike - {what_needs_investigation}
  [ ] Reject - {stop_workflow_reason}

NEXT STEPS IF APPROVED:
  {clear_description_of_next_actions}

═══════════════════════════════════════════════════════════════
```

### Example:
```
═══════════════════════════════════════════════════════════════
CHECKPOINT: Analysis Complete
═══════════════════════════════════════════════════════════════

STAGES COMPLETED: 1, 2, 3, 4, 5

CONSOLIDATED RESULTS:

Stage 1 - Intake:
  ✓ Ticket: PROJ-1234 validated
  ✓ Mode: FEATURE detected
  ✓ Scope: Add Excel export to customer list

Stage 2 - Requirements:
  ✓ Acceptance criteria expanded (7 criteria)
  ✓ Edge cases identified (5 cases)
  ✓ Success criteria defined

Stage 3 - Feasibility:
  ✓ Technical approach: Server-side export using EPPlus
  ✓ Feasibility: HIGH
  ✓ Estimated complexity: MEDIUM

Stage 4 - Legacy Impact:
  ✓ Files affected: CustomerList.aspx, CustomerList.aspx.cs
  ✓ WebForms lifecycle: No violations
  ✓ Telerik controls: No changes needed

Stage 5 - Data/Cache:
  ✓ Database: Reuse existing customer query
  ✓ Caching: Not needed (export on-demand)
  ✓ Performance: Acceptable for <10K rows

RISK ASSESSMENT:
  Level: LOW
  Factors:
    - Well-established export pattern (used in InvoiceList)
    - No database schema changes
    - No public API modifications
    - Easily reversible

CONFIDENCE: HIGH
  Reasoning: Similar export feature exists in InvoiceList.aspx,
  proven pattern, minimal changes required

DECISION REQUIRED:
  Analysis shows LOW risk and HIGH feasibility. Proceed with
  implementation planning?

OPTIONS:
  [ ] Approve - Continue to stages 6-9 (implementation planning)
  [ ] Adjust - Modify approach (e.g., different export format)
  [ ] Spike - Investigate performance with large datasets
  [ ] Reject - Stop workflow, different solution needed

NEXT STEPS IF APPROVED:
  1. Create detailed implementation plan (stage 6)
  2. Generate test scenarios (stage 7)
  3. Prepare documentation (stage 8)
  4. Define rollback procedure (stage 9)

═══════════════════════════════════════════════════════════════
```

---

## Skill Invocation Template

### Standard Skill Invocation

**When to use:** Every time you invoke a skill

**Template:**
```
┌─────────────────────────────────────────────────────────────┐
│ SKILL: {skill-name}                                          │
└─────────────────────────────────────────────────────────────┘

INPUT:
  Context: {why_invoking_this_skill}
  Parameters:
    {parameter_1}: {value_1}
    {parameter_2}: {value_2}
    {parameter_3}: {value_3}

EXECUTING...

OUTPUT:
  Result:
    {structured_result_1}: {value}
    {structured_result_2}: {value}
    {structured_result_3}: {value}

  Risks Identified:
    - {RISK_LEVEL}: {risk_description_1}
    - {RISK_LEVEL}: {risk_description_2}

  Confidence: {HIGH|MEDIUM|LOW}
    Reasoning: {why_this_confidence}

  Recommendations:
    - {recommendation_1}
    - {recommendation_2}

┌─────────────────────────────────────────────────────────────┐
│ SKILL COMPLETE                                               │
└─────────────────────────────────────────────────────────────┘
```

### Example:
```
┌─────────────────────────────────────────────────────────────┐
│ SKILL: linq-query-tracer                                     │
└─────────────────────────────────────────────────────────────┘

INPUT:
  Context: "Analyzing customer search performance issue"
  Parameters:
    query_file: "CustomerRepository.cs"
    method_name: "SearchCustomers"
    issue_reported: "Takes 8+ seconds to load results"

EXECUTING...

OUTPUT:
  Result:
    query_pattern: "N+1 query detected"
    execution_plan: "Table scan on Customers table"
    row_count: 50000
    columns_selected: "SELECT * (all columns)"
    filter_location: "After ToList() - in memory"
    estimated_time: "8.2 seconds"

  Risks Identified:
    - HIGH: Table scan on 50K+ row table
    - MEDIUM: Loading all columns unnecessarily
    - MEDIUM: Filtering in memory after data retrieval
    - LOW: No pagination implemented

  Confidence: HIGH
    Reasoning: Query pattern clearly visible in code, execution
    plan confirms table scan, performance matches reported issue

  Recommendations:
    1. Move .Where() before .ToList() (critical)
    2. Add index on Status column (high priority)
    3. Implement pagination (high priority)
    4. Select only needed columns (medium priority)

┌─────────────────────────────────────────────────────────────┐
│ SKILL COMPLETE                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## Error Handling Template

### Critical Error

**When to use:** Skill or stage fails critically

**Template:**
```
⚠️  CRITICAL ERROR ⚠️
═══════════════════════════════════════════════════════════════

ERROR TYPE: {error_type}
FAILED AT: {stage_or_skill_name}
SEVERITY: CRITICAL

WHAT HAPPENED:
{clear_description_of_error}

WHY IT FAILED:
{root_cause_explanation}

IMPACT:
Cannot proceed with workflow without resolving this error.

ATTEMPTED:
  - {what_was_tried_1}
  - {what_was_tried_2}

OPTIONS:
  [ ] Retry - {with_what_changes}
  [ ] Skip - {if_possible_why_or_why_not}
  [ ] Spike - Switch to investigation mode
  [ ] Abort - Stop workflow entirely

RECOMMENDATION:
{what_should_user_do}

═══════════════════════════════════════════════════════════════
```

### Example:
```
⚠️  CRITICAL ERROR ⚠️
═══════════════════════════════════════════════════════════════

ERROR TYPE: Skill Execution Failure
FAILED AT: linq-query-tracer skill
SEVERITY: CRITICAL

WHAT HAPPENED:
The linq-query-tracer skill failed while analyzing the customer
search query. Unable to parse the LINQ expression in
CustomerRepository.cs.

WHY IT FAILED:
The LINQ query uses a complex expression with nested lambda
functions and dynamic predicate building that the tracer cannot
analyze statically.

IMPACT:
Cannot determine query performance characteristics without this
analysis. Stage 5 (Data/Cache Impact) cannot be completed.

ATTEMPTED:
  - Standard LINQ tracing (failed)
  - Expression tree parsing (failed)
  - Fallback to static code analysis (insufficient data)

OPTIONS:
  [ ] Retry - Simplify query to standard LINQ pattern first
  [ ] Skip - Continue without query analysis (NOT RECOMMENDED)
  [ ] Spike - Investigate query pattern, run profiler manually
  [ ] Abort - Stop workflow, refine requirements

RECOMMENDATION:
Switch to SPIKE mode to:
1. Run query profiler in test environment
2. Capture actual execution plan
3. Return to workflow with findings

═══════════════════════════════════════════════════════════════
```

### Non-Critical Warning

**When to use:** Skill fails but workflow can continue with degraded info

**Template:**
```
⚠️  WARNING
───────────────────────────────────────────────────────────────

WARNING TYPE: {warning_type}
OCCURRED AT: {stage_or_skill_name}
SEVERITY: NON-CRITICAL

ISSUE:
{description_of_issue}

IMPACT:
{what_information_is_missing_or_degraded}

CONTINUING WITH:
{what_assumptions_or_fallback_being_used}

NOTED IN FINAL OUTPUT:
This limitation will be documented in the final analysis.

───────────────────────────────────────────────────────────────
```

---

## Safety Violation Template

**When to use:** Safety rule is violated

**Template:**
```
🛑 SAFETY VIOLATION - IMMEDIATE STOP 🛑
═══════════════════════════════════════════════════════════════

VIOLATION TYPE: {violation_type}
DETECTED AT: {stage_or_location}
SEVERITY: NON-NEGOTIABLE STOP

SAFETY RULE VIOLATED:
{which_safety_rule_from_EXECUTION_RULES}

WHAT WAS DETECTED:
{specific_violation_description}

WHY THIS IS NOT ALLOWED:
{explanation_of_why_rule_exists}

REQUIRED ACTION:
{what_must_be_done_to_proceed}

OPTIONS:
  [ ] Fix violation and retry
  [ ] Change approach to avoid violation
  [ ] Provide explicit justification (if applicable)
  [ ] Abort workflow

CANNOT CONTINUE WITHOUT:
{specific_requirement_to_proceed}

═══════════════════════════════════════════════════════════════
```

### Example:
```
🛑 SAFETY VIOLATION - IMMEDIATE STOP 🛑
═══════════════════════════════════════════════════════════════

VIOLATION TYPE: Public API Change Without Justification
DETECTED AT: Stage 6 - Implementation Planning
SEVERITY: NON-NEGOTIABLE STOP

SAFETY RULE VIOLATED:
"Public APIs must not change without justification"
(From EXECUTION_RULES.md - Safety Rules, Rule 3.1)

WHAT WAS DETECTED:
Implementation plan proposes changing the signature of
CustomerRepository.SearchCustomers() method from:

  Current:  SearchCustomers(string status)
  Proposed: SearchCustomers(SearchCriteria criteria)

This method is public and used by 15+ callers across the codebase.

WHY THIS IS NOT ALLOWED:
Public API changes can break existing consumers, cause runtime
errors, and require coordinated updates across multiple teams.
In a legacy WebForms application, this can cause cascade failures.

REQUIRED ACTION:
Either:
1. Keep existing public API, add new overload method
2. Provide explicit justification with impact analysis
3. Change approach to avoid API modification

OPTIONS:
  [ ] Fix - Add new overload, keep existing method
  [ ] Justify - Provide impact analysis and justification
  [ ] Different approach - Modify implementation without API change
  [ ] Abort - Stop workflow, reconsider requirements

CANNOT CONTINUE WITHOUT:
Either fixing the violation OR providing documented justification
with impact analysis and migration plan.

═══════════════════════════════════════════════════════════════
```

---

## Mode Escalation Template

**When to use:** Escalating from one mode to another

**Template:**
```
📢 MODE ESCALATION
═══════════════════════════════════════════════════════════════

ESCALATING FROM: {current_mode}
ESCALATING TO: {new_mode}
REASON: {escalation_trigger}

WHY ESCALATING:
{detailed_explanation}

TRIGGER CONDITION:
{specific_condition_from_EXECUTION_RULES}

WORK PRESERVED:
Stages completed: {list}
Results saved: {what_results_are_preserved}

NEW MODE BEHAVIOR:
{what_will_happen_in_new_mode}

═══════════════════════════════════════════════════════════════
```

### Example:
```
📢 MODE ESCALATION
═══════════════════════════════════════════════════════════════

ESCALATING FROM: BUG FIX
ESCALATING TO: SPIKE (Investigation)
REASON: Cannot reproduce reported bug

WHY ESCALATING:
Bug report: "Customer search sometimes returns wrong results"

After analysis:
- Cannot reproduce in test environment
- Intermittent behavior reported
- No clear pattern identified
- Root cause unclear

This matches escalation condition: "Intermittent bug cannot be
reproduced" → Switch to SPIKE mode

TRIGGER CONDITION:
From EXECUTION_RULES.md - Escalation Rules 10.1:
"to_spike: conditions: root_cause == unknown"

WORK PRESERVED:
Stages completed: 1 (Triage), 2 (Attempted Reproduction)
Results saved:
  - Bug classification: HIGH severity, FUNCTIONAL type
  - Reproduction attempts: 0/5 successful
  - Environment details: Captured
  - User reports: Documented

NEW MODE BEHAVIOR:
Switching to SPIKE mode with:
  - Research question: "Why does customer search return wrong
    results intermittently?"
  - Time box: 4 hours
  - Success criteria: Identify reproduction pattern OR root cause
  - Investigation approach: Log analysis, user session replay,
    database query monitoring

After SPIKE completion, will return to BUG FIX mode with findings.

═══════════════════════════════════════════════════════════════
```

---

## Completion Template

**When to use:** Workflow successfully completed

**Template:**
```
✅ WORKFLOW COMPLETE ✅
═══════════════════════════════════════════════════════════════

MODE: {workflow_mode}
EXECUTION TIME: {duration}
EXECUTION MODE: {autonomous|hybrid|manual}
CHECKPOINTS: {number_of_checkpoints}

FINAL STATUS: READY FOR IMPLEMENTATION

DELIVERABLES:
  ✓ {deliverable_1}
  ✓ {deliverable_2}
  ✓ {deliverable_3}
  ✓ {deliverable_4}

SUMMARY:
{brief_summary_of_what_was_accomplished}

RISK LEVEL: {FINAL_RISK_LEVEL}
CONFIDENCE: {FINAL_CONFIDENCE}

NEXT STEPS:
1. {next_step_1}
2. {next_step_2}
3. {next_step_3}

ARTIFACTS CREATED:
  - {artifact_1_location}
  - {artifact_2_location}
  - {artifact_3_location}

═══════════════════════════════════════════════════════════════
```

### Example:
```
✅ WORKFLOW COMPLETE ✅
═══════════════════════════════════════════════════════════════

MODE: FEATURE DELIVERY
EXECUTION TIME: 47 seconds
EXECUTION MODE: Autonomous (no flags provided)
CHECKPOINTS: 0 (no stops triggered)

FINAL STATUS: READY FOR IMPLEMENTATION

DELIVERABLES:
  ✓ Complete requirements (7 acceptance criteria)
  ✓ Implementation plan (2 files, ~40 lines)
  ✓ Test scenarios (8 scenarios covering happy path + edges)
  ✓ Documentation (inline comments, change log)
  ✓ Rollback procedure (simple file revert)

SUMMARY:
Add Excel export functionality to CustomerList.aspx page.
Server-side export using EPPlus library (already in project).
Pattern matches existing InvoiceList export feature. Low risk,
high feasibility, straightforward implementation.

RISK LEVEL: LOW
CONFIDENCE: HIGH

NEXT STEPS:
1. Review implementation plan
2. Create feature branch
3. Implement changes (estimated: 2-3 hours)
4. Test scenarios (estimated: 1 hour)
5. Code review and merge

ARTIFACTS CREATED:
  - Implementation plan: [detailed file changes]
  - Test scenarios: [8 test cases]
  - Documentation: [inline and changelog]
  - Rollback procedure: [git revert instructions]

═══════════════════════════════════════════════════════════════
```


---

## Mandatory Structured Payload (Machine-Checkable)

For **Checkpoint**, **Skill Invocation**, **Safety Violation**, and **Completion** outputs,
append this `STRUCTURED_PAYLOAD` block after the visual template.

### Checkpoint Payload
```yaml
STRUCTURED_PAYLOAD:
  type: checkpoint
  checkpoint_name: "{checkpoint_name}"
  stages_completed: [{stage_numbers}]
  risk_level: "{LOW|MEDIUM|HIGH}"
  confidence: "{HIGH|MEDIUM|LOW}"
  decision_required: "{specific_question_for_user}"
  options: ["approve", "adjust", "spike", "reject"]
```

### Skill Invocation Payload
```yaml
STRUCTURED_PAYLOAD:
  type: skill_invocation
  skill_name: "{skill-name}"
  input_context: "{why_invoking_this_skill}"
  parameters: {parameter_map}
  risks_identified: [{risk_items}]
  confidence: "{HIGH|MEDIUM|LOW}"
```

### Safety Violation Payload
```yaml
STRUCTURED_PAYLOAD:
  type: safety_violation
  violation_type: "{violation_type}"
  detected_at: "{stage_or_location}"
  severity: "NON-NEGOTIABLE STOP"
  required_action: "{what_must_be_done_to_proceed}"
```

### Completion Payload
```yaml
STRUCTURED_PAYLOAD:
  type: completion
  mode: "{workflow_mode}"
  execution_time: "{duration}"
  execution_mode: "{autonomous|hybrid|manual}"
  checkpoints: {number_of_checkpoints}
  final_status: "READY FOR IMPLEMENTATION"
  risk_level: "{FINAL_RISK_LEVEL}"
  confidence: "{FINAL_CONFIDENCE}"
```

---

## Usage Guidelines

### When to Use Each Template

**Checkpoint Template:**
- Before executing any flagged stage (approve_before_stage)
- When risk threshold met (approve_at_risk)
- Before flagged skill (approve_before_skills)
- On safety violations
- On automatic stop conditions

**Skill Invocation Template:**
- Every single skill invocation
- No exceptions
- Always show input/output/risks/confidence

**Error Handling Template:**
- Critical Error: Skill/stage fails, cannot proceed
- Non-Critical Warning: Skill fails, can continue with degraded info

**Safety Violation Template:**
- Any safety rule from EXECUTION_RULES.md violated
- Immediate stop required

**Mode Escalation Template:**
- Switching from one mode to another
- Document why and what's preserved

**Completion Template:**
- Workflow successfully finished
- All stages complete
- Ready for implementation

---

## Copy-Paste Rules

✅ **DO:**
- Copy templates EXACTLY as shown
- Replace {placeholders} with actual values
- Keep formatting (boxes, lines, spacing)
- Maintain section order
- Use specified emoji/symbols

❌ **DON'T:**
- Modify template structure
- Remove sections
- Change formatting
- Abbreviate or summarize
- Skip placeholders

---

## Version History

- v1.1.0 (2026-03-07): Added mandatory structured payload blocks for machine-checkable outputs
- v1.0.0 (2026-01-18): Initial templates created
  - Checkpoint template
  - Skill invocation template
  - Error handling templates
  - Safety violation template
  - Mode escalation template
  - Completion template
