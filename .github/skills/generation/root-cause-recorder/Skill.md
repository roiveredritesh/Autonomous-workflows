---
name: root-cause-recorder
description: Records root cause analysis findings in a structured format for pattern tracking across multiple bugs, enabling systemic improvement over time.
---

# Root Cause Recorder

## Quick Example

**Input:** Bug PROJ-4521, root cause: missing null guard on Carrier in ShippingCalculator, contributing factor: refactor removed existing guard
**Output:** Structured RCA document with root cause category NULL_REFERENCE, contributing factors, timeline, prevention recommendations, stored for pattern tracking
**Time:** 30-60 seconds

---

## Purpose
Records root cause analysis findings in a structured format for pattern tracking across multiple bugs, enabling systemic improvement over time.

## Input

```yaml
input:
  bug_id: <ticket or incident ID>
  bug_symptoms: <what users or monitors observed>
  investigation_steps: <list of steps taken to diagnose>
  root_cause_identified: <the specific underlying cause>
  contributing_factors: <list of conditions that allowed the bug to occur>
  environment: PRODUCTION|STAGING|DEVELOPMENT
  detection_method: USER_REPORT|MONITORING|CODE_REVIEW|TESTING
```

## Output

```yaml
output:
  rca_document:
    id: <RCA-{bug_id}>
    date: <ISO date>
    bug_id: <reference>
    environment: <env>
  classification:
    root_cause_category: LOGIC_ERROR|NULL_REFERENCE|LIFECYCLE|CACHE|DATA_TYPE|CONFIGURATION|CONCURRENCY|EXTERNAL_DEPENDENCY
    sub_category: <more specific classification>
    detection_method: <how it was found>
    time_to_detect_hours: <if known>
    time_to_resolve_hours: <if known>
  root_cause_detail:
    primary_cause: <specific technical cause>
    affected_component: <class, method, or system>
    trigger_condition: <what caused the code path to execute>
    precondition: <what state had to exist for the bug to manifest>
  contributing_factors:
    - factor: <description>
      category: MISSING_TEST|MISSING_REVIEW|PROCESS_GAP|TECHNICAL_DEBT|KNOWLEDGE_GAP
  prevention_recommendations:
    - recommendation: <specific action>
      owner: DEVELOPER|QA|TEAM_LEAD|PROCESS
      timeframe: IMMEDIATE|NEXT_SPRINT|QUARTERLY
  pattern_tags: [<list of tags for pattern matching>]
  confidence: HIGH|MEDIUM|LOW
```

## DO:
✅ Record every root cause even for low-severity bugs — patterns emerge over time
✅ Tag the root cause with searchable labels (null-reference, missing-test, lifecycle)
✅ Assign ownership to prevention recommendations — unowned items don't get done
✅ Distinguish primary cause from contributing factors — both matter for prevention
✅ Note the detection method — user-reported vs monitoring reveals detection gaps

## DON'T:
❌ Write vague root causes like "developer error" — be specific about the technical cause
❌ Skip contributing factors — they reveal systemic issues beyond the individual bug
❌ Assign all prevention to QA — developers own code quality, tests, and code review
❌ Record RCA days after the incident — details fade; record immediately after fix
❌ Duplicate with bug-fix-documenter — RCA recorder focuses on pattern tracking, not fix docs

## Error Conditions

**IF root cause is still uncertain:**
```
1. Record as PRELIMINARY with confidence LOW
2. Note: ROOT_CAUSE_UNCERTAIN — update after further investigation
```

**IF investigation steps are not documented:**
```
1. Reconstruct from memory or logs
2. Flag: STEPS_RECONSTRUCTED — may be incomplete
```

## Processing Steps

1. **RCA ID Generation:** Create ID: `RCA-{bug_id}-{date}`. Use as primary reference.

2. **Classification:** Map root cause to standard category and sub-category. Assign detection method. Calculate time-to-detect and time-to-resolve from timestamps.

3. **Root Cause Detail:** Identify: the specific code or configuration that was wrong, which component contains it, what condition triggered the bug, what precondition had to exist.

4. **Contributing Factor Mapping:** For each factor, assign a category: MISSING_TEST (no test covered this case), MISSING_REVIEW (pattern not in review checklist), PROCESS_GAP (deployment verification missing), TECHNICAL_DEBT (known issue deferred), KNOWLEDGE_GAP (developer unaware of constraint).

5. **Prevention Recommendations:** One recommendation per contributing factor. Be specific: not "add tests" but "add unit test verifying null Carrier returns DefaultRate in ShippingCalculator.Calculate". Assign owner and timeframe.

6. **Pattern Tags:** Generate searchable tags: `null-reference`, `linq-to-sql`, `navigation-property`, `missing-null-guard`. These enable pattern detection across multiple RCAs.

7. **Output Assembly:** Combine into structured document ready for storage in bug tracking or wiki.

## Example

**Input:**
```yaml
bug_id: "PROJ-4521"
bug_symptoms: "100% order submission failures — NullReferenceException in ShippingCalculator"
investigation_steps:
  - "Checked production logs — all errors same stack trace"
  - "Identified onset at 14:23 — 4 minutes after deployment"
  - "Reviewed git diff — found null guard removed in commit a3f92b1"
root_cause_identified: "ShippingCalculator.Calculate() accessed carrier.RateCode without null check. Guard removed in recent refactor commit."
contributing_factors:
  - "No unit test for null carrier scenario"
  - "Code reviewer did not notice guard removal"
environment: PRODUCTION
detection_method: USER_REPORT
```

**Output:**
```yaml
rca_document:
  id: "RCA-PROJ-4521-2026-04-05"
  date: "2026-04-05"
  bug_id: "PROJ-4521"
  environment: PRODUCTION
classification:
  root_cause_category: NULL_REFERENCE
  sub_category: "Navigation property access without null guard"
  detection_method: USER_REPORT
  time_to_detect_hours: 0.07
  time_to_resolve_hours: 0.5
root_cause_detail:
  primary_cause: "Null guard on Carrier navigation property was accidentally removed during refactoring of ShippingCalculator.Calculate()"
  affected_component: "ShippingCalculator.Calculate()"
  trigger_condition: "Order submitted with no carrier assigned (draft orders)"
  precondition: "Order.CarrierId is null — valid state for draft orders"
contributing_factors:
  - factor: "No unit test covered the null carrier scenario"
    category: MISSING_TEST
  - factor: "Code reviewer did not notice the guard removal in the diff"
    category: MISSING_REVIEW
prevention_recommendations:
  - recommendation: "Add unit test: ShippingCalculator_Calculate_ReturnsDefaultRate_WhenCarrierIsNull"
    owner: DEVELOPER
    timeframe: IMMEDIATE
  - recommendation: "Add to code review checklist: verify null guards preserved when refactoring navigation property access"
    owner: TEAM_LEAD
    timeframe: NEXT_SPRINT
pattern_tags: [null-reference, linq-to-sql, navigation-property, missing-null-guard, refactor-regression]
confidence: HIGH
```

---

**Related Skills:**
- `bug-fix-documenter` - Generates full bug fix documentation that includes this RCA
- `error-pattern-detector` - Uses pattern tags to identify recurring root cause types
- `bug-classifier` - Provides the severity and classification that feeds into this recorder
- `postmortem-planner` - Uses RCA output to plan postmortem for critical incidents
