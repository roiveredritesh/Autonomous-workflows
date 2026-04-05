---
name: bug-fix-documenter
description: Generates structured bug fix documentation including root cause analysis, fix description, and prevention measures for traceability and team knowledge sharing.
---

# Bug Fix Documenter

## Quick Example

**Input:** NullReferenceException in ShippingCalculator.Calculate, root cause: missing null guard on Carrier, fix: added null check, file: ShippingCalculator.cs line 87
**Output:** Structured bug report with root cause explanation, before/after code diff, prevention measures, and code review checklist item
**Time:** 30-60 seconds

---

## Purpose
Generates structured bug fix documentation including root cause analysis, fix description, and prevention measures for traceability and team knowledge sharing.

## Input

```yaml
input:
  bug_description: <what the bug was — symptoms and error message>
  root_cause: <the underlying cause identified during investigation>
  fix_applied: <description of the code change made to fix the bug>
  affected_files: <list of files changed in the fix>
  ticket_id: <optional — Jira or other tracking system ID>
  severity: CRITICAL|HIGH|MEDIUM|LOW
  reporter: <optional — who reported the bug>
  fixer: <optional — who fixed the bug>
```

## Output

```yaml
output:
  bug_report:
    title: <concise bug title>
    ticket_id: <ID>
    severity: <level>
    reported_by: <name>
    fixed_by: <name>
    date_fixed: <ISO date>
  summary:
    bug_description: <plain English description>
    user_impact: <what users experienced>
    affected_component: <class or page>
    root_cause_category: LOGIC_ERROR|NULL_REFERENCE|LIFECYCLE|CACHE|DATA_TYPE|CONFIGURATION|CONCURRENCY
  root_cause_analysis:
    root_cause: <detailed explanation>
    why_it_happened: <contributing factors>
    why_it_was_missed: <gap in testing or review>
  fix_description:
    approach: <what was changed and why>
    files_changed: [<list>]
    lines_changed_estimate: <count>
    before_code: <key code before fix (1-3 lines)>
    after_code: <key code after fix (1-3 lines)>
  prevention_measures:
    - measure: <what to add or change to prevent recurrence>
      type: UNIT_TEST|CODE_REVIEW_CHECKLIST|VALIDATION|MONITORING
  code_review_notes:
    - note: <what reviewers should check in similar code>
  confidence: HIGH|MEDIUM|LOW
```

## DO:
✅ Write the bug description in plain English suitable for non-technical stakeholders
✅ Include the before/after code snippet even if it's just 1-2 lines — it's most valuable
✅ Categorize the root cause type — helps identify patterns across multiple bugs
✅ Specify concrete prevention measures, not vague recommendations
✅ Include a code review checklist note so the same pattern is caught in future PRs

## DON'T:
❌ Omit the "why it was missed" section — it improves development processes
❌ Write technical jargon in the user impact section — keep it user-facing language
❌ Leave prevention measures vague ("write more tests") — be specific about what test
❌ Skip documenting if the bug was low severity — patterns matter across severities
❌ Document only the fix — the root cause explanation is the most valuable part

## Error Conditions

**IF root cause is still unclear:**
```
1. Flag document as PRELIMINARY
2. Note root cause as UNDER_INVESTIGATION
3. Return: INCOMPLETE_RCA — update document after root cause confirmed
```

**IF no fix has been applied yet:**
```
1. Document as bug report with investigation findings only
2. Leave fix_description empty with placeholder
3. Return: FIX_PENDING — complete document after fix is implemented
```

## Processing Steps

1. **Title Generation:** Create a concise, searchable title: `{component}: {error type} when {condition}`. Example: `ShippingCalculator: NullReferenceException when Carrier is null`

2. **Root Cause Categorization:** Map root cause to standard categories: Logic Error, Null Reference, Lifecycle (WebForms), Cache, Data Type, Configuration, Concurrency.

3. **User Impact:** Translate technical symptoms to user-facing impact. "NullReferenceException" → "Users could not complete orders — checkout failed with an error page".

4. **Before/After Code:** Extract the key lines changed. Show the problematic code before and the corrected code after. Keep to 1-5 lines each.

5. **Prevention Measures:** For each root cause category, apply standard prevention: Null Reference → add null guard unit test. Lifecycle → add lifecycle phase documentation. Cache → add cache invalidation test.

6. **Code Review Notes:** Identify the pattern that should be caught in code review: "Check for null guards when accessing navigation properties from LINQ-to-SQL EntityRef".

7. **Document Assembly:** Combine all sections into structured output. Set confidence based on completeness of information.

## Example

**Input:**
```yaml
bug_description: "NullReferenceException in ShippingCalculator.Calculate — orders failing 100% since deployment at 14:19"
root_cause: "ShippingCalculator.Calculate accessed carrier.RateCode without null check. Carrier can be null when no carrier is assigned to a shipment."
fix_applied: "Added null guard: if (carrier == null) return DefaultRate; before accessing carrier.RateCode"
affected_files: ["ShippingCalculator.cs"]
ticket_id: "PROJ-4521"
severity: CRITICAL
```

**Output:**
```yaml
bug_report:
  title: "ShippingCalculator: NullReferenceException when Order has no assigned Carrier"
  ticket_id: PROJ-4521
  severity: CRITICAL
  date_fixed: "2026-04-05"
summary:
  bug_description: "The shipping cost calculation failed with an unhandled NullReferenceException when an order had no carrier assigned, causing all order submissions to fail."
  user_impact: "100% of order submissions failed with an error page. Customers could not complete purchases."
  affected_component: "ShippingCalculator.Calculate()"
  root_cause_category: NULL_REFERENCE
root_cause_analysis:
  root_cause: "ShippingCalculator.Calculate() accessed carrier.RateCode without checking if carrier was null first. Orders with no carrier assignment (a valid state for draft orders) triggered the null dereference."
  why_it_happened: "A recent refactor removed a null guard that was previously present. The guard was accidentally deleted during simplification."
  why_it_was_missed: "No unit test covered the null carrier scenario. The test suite only tested orders with an assigned carrier."
fix_description:
  approach: "Added null guard check before accessing Carrier properties. Returns DefaultRate when carrier is null."
  files_changed: ["ShippingCalculator.cs"]
  lines_changed_estimate: 2
  before_code: "var rate = carrier.RateCode;"
  after_code: |
    if (carrier == null) return DefaultRate;
    var rate = carrier.RateCode;
prevention_measures:
  - measure: "Add unit test: ShippingCalculator_Calculate_ReturnsDefaultRate_WhenCarrierIsNull"
    type: UNIT_TEST
  - measure: "Add to code review checklist: verify null guards on navigation properties from LINQ-to-SQL EntityRef"
    type: CODE_REVIEW_CHECKLIST
code_review_notes:
  - note: "Whenever accessing a nullable LINQ-to-SQL EntityRef (e.g., Order.Carrier), verify null guard is present before property access"
confidence: HIGH
```

---

**Related Skills:**
- `root-cause-recorder` - Records root cause in a structured format for pattern tracking
- `rollback-plan-generator` - Generates rollback procedure documented alongside the fix
- `test-scenario-generator` - Generates the test scenarios referenced in prevention measures
- `change-log-generator` - Creates the changelog entry for this bug fix
