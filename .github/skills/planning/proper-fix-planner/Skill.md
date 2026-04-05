---
name: proper-fix-planner
description: Plans the proper (non-emergency) fix after a hotfix, including comprehensive tests, refactoring, and elimination of technical debt introduced by the emergency fix.
---

# Proper Fix Planner

## Quick Example

**Input:** Hotfix: null guard added to ShippingCalculator, root cause: missing test + missing guard, technical debt: fix is temporary workaround
**Output:** Proper fix scope (add comprehensive null guards + full test suite + refactor to defensive design), story points: 3, sprint: next, no technical debt created
**Time:** 2-3 minutes

---

## Purpose
Plans the proper (non-emergency) fix after a hotfix, including comprehensive tests, refactoring, and elimination of technical debt introduced by the emergency fix.

## Input

```yaml
input:
  hotfix_description: <what the hotfix did>
  root_cause: <the underlying root cause>
  quick_fix_applied: <the minimal fix applied under pressure>
  technical_debt_created: <what shortcuts were taken in the hotfix>
  affected_component: <class, module, or feature>
  related_code_areas: <other areas with similar patterns that should be fixed>
```

## Output

```yaml
output:
  proper_fix_scope:
    goal: <what the proper fix achieves beyond the hotfix>
    not_in_scope: [<explicitly excluded items>]
  work_items:
    - id: <W1..Wn>
      type: BUG_FIX|UNIT_TEST|REFACTOR|DOCUMENTATION|MONITORING
      description: <what to do>
      files: [<files to modify>]
      estimated_hours: <hours>
      depends_on: [<W1|etc>]
      acceptance_criteria: [<how to verify complete>]
  technical_debt_resolution:
    debt_items: [<what technical debt exists from hotfix>]
    resolution_per_item: [<how to resolve each>]
  test_requirements:
    unit_tests: [<specific tests to add>]
    integration_tests: [<specific integration tests>]
    regression_tests: [<specific regression tests>]
  refactoring_plan:
    - component: <what to refactor>
      current_problem: <what's wrong>
      target_state: <what it should look like>
      risk: LOW|MEDIUM|HIGH
  timeline:
    recommended_sprint: CURRENT|NEXT|WITHIN_2_WEEKS
    total_estimated_hours: <sum>
    story_points_estimate: <SP>
  confidence: HIGH|MEDIUM|LOW
```

## DO:
✅ Plan tests FIRST — the hotfix exposed a test gap; fill it immediately
✅ Look for similar patterns in related code that have the same vulnerability
✅ Plan refactoring only if it reduces future risk — not for cosmetic improvement
✅ Keep proper fix scoped — don't turn it into a full rewrite
✅ Schedule in the very next sprint — technical debt compounds quickly

## DON'T:
❌ Skip the proper fix — hotfixes are band-aids, not permanent solutions
❌ Use the proper fix as an excuse to refactor unrelated code
❌ Plan more than 1 sprint of work — proper fix should be focused
❌ Defer to "someday" — set a specific sprint or date
❌ Forget to check related components for the same pattern

## Error Conditions

**IF hotfix is already the proper fix (no shortcuts taken):**
```
1. Verify: were comprehensive tests added? Were similar patterns fixed?
2. If yes: document as PROPER_FIX_COMPLETE — no additional work needed
3. If tests missing: create test-only work item
```

**IF proper fix requires architectural changes:**
```
1. Flag: ARCHITECTURAL_CHANGE — escalate to feature-delivery process
2. Keep as quick fix for now with ACCEPTED_TECHNICAL_DEBT documented
3. Create architecture spike for proper solution
```

## Processing Steps

1. **Gap Analysis:** Compare hotfix to proper solution. Hotfix was minimal under pressure. Proper fix adds: missing tests, handles all edge cases, removes shortcuts, ensures pattern is consistent across codebase.

2. **Work Item Identification:** Break proper fix into discrete items: (1) Unit tests for all null input combinations, (2) Integration test for the affected workflow, (3) Fix same pattern in related components, (4) Refactor if applicable.

3. **Related Pattern Scan:** Search codebase for similar code patterns that have the same vulnerability. Example: if ShippingCalculator needed null guard, check all other calculators and similar access patterns.

4. **Test Plan:** For each gap identified by the hotfix: write a specific test name and assertion. Tests should cover: the broken scenario, edge cases, boundary conditions, and the fix's correctness.

5. **Refactoring Plan:** If the hotfix revealed a design issue (not just a missing guard), plan targeted refactoring: defensive design pattern, factory method for safe construction, validation at entry point rather than each access.

6. **Technical Debt Resolution:** List all shortcuts from the hotfix (no tests, hardcoded default, missing edge cases) and specify how each is resolved in the proper fix.

7. **Timeline Estimation:** Sum hours per work item. Convert to story points (3h=1SP, 6h=2SP, etc.). Recommend NEXT sprint unless component is too risky to leave unresolved (then CURRENT).

## Example

**Input:**
```yaml
hotfix_description: "Added null guard: if (carrier == null) return DefaultRate"
root_cause: "Null guard on Carrier removed during refactor"
quick_fix_applied: "Minimal guard — does not cover all null scenarios, uses hardcoded DefaultRate constant"
technical_debt_created: "DefaultRate is hardcoded to 0m — should be configurable. Only one guard added — other calculators may have same issue."
affected_component: "ShippingCalculator"
related_code_areas: ["FreightCalculator", "InsuranceCalculator", "HandlingFeeCalculator"]
```

**Output:**
```yaml
proper_fix_scope:
  goal: "Add comprehensive null safety to all calculator classes, full unit test coverage, and make DefaultRate configurable"
  not_in_scope: ["Calculator rewrite", "UI changes", "New calculation features"]
work_items:
  - id: W1
    type: UNIT_TEST
    description: "Add unit test suite for ShippingCalculator — all null input combinations"
    files: ["ShippingCalculatorTests.cs"]
    estimated_hours: 2
    depends_on: []
    acceptance_criteria: ["Tests cover: null carrier, null order, both null, typical inputs. All tests pass in CI."]
  - id: W2
    type: BUG_FIX
    description: "Make DefaultRate configurable — read from AppSettings instead of hardcoded 0m"
    files: ["ShippingCalculator.cs", "Web.config"]
    estimated_hours: 1
    depends_on: [W1]
    acceptance_criteria: ["DefaultRate reads from config key 'ShippingCalculator.DefaultRate', falls back to 0m"]
  - id: W3
    type: BUG_FIX
    description: "Audit and fix null guards in FreightCalculator, InsuranceCalculator, HandlingFeeCalculator"
    files: ["FreightCalculator.cs", "InsuranceCalculator.cs", "HandlingFeeCalculator.cs"]
    estimated_hours: 3
    depends_on: []
    acceptance_criteria: ["Each calculator has null guard with unit test. No NullReferenceException possible on null inputs."]
  - id: W4
    type: DOCUMENTATION
    description: "Add code comment documenting null-safety contract for all calculator classes"
    files: ["ShippingCalculator.cs", "FreightCalculator.cs"]
    estimated_hours: 0.5
    depends_on: [W1, W3]
    acceptance_criteria: ["XML doc comment on each Calculate() method documents null handling behavior"]
technical_debt_resolution:
  debt_items: ["DefaultRate hardcoded to 0m", "Only ShippingCalculator fixed — other calculators untested"]
  resolution_per_item: ["W2 makes DefaultRate configurable", "W3 audits all related calculators"]
test_requirements:
  unit_tests:
    - "ShippingCalculator_Calculate_ReturnsDefaultRate_WhenCarrierIsNull"
    - "ShippingCalculator_Calculate_ReturnsDefaultRate_WhenOrderIsNull"
    - "ShippingCalculator_Calculate_ReturnsCorrectRate_WhenBothProvided"
    - "FreightCalculator_Calculate_ReturnsDefaultRate_WhenCarrierIsNull"
  integration_tests:
    - "OrderSubmission_WithNullCarrier_CompletesWithDefaultShipping"
  regression_tests:
    - "OrderSubmission_WithCarrierAssigned_CalculatesCorrectShipping"
refactoring_plan:
  - component: "Calculator classes (ShippingCalculator, FreightCalculator, etc.)"
    current_problem: "Null checks scattered inconsistently — some have guards, some don't"
    target_state: "All calculators validate inputs at method entry using consistent pattern"
    risk: LOW
timeline:
  recommended_sprint: NEXT
  total_estimated_hours: 6.5
  story_points_estimate: 3
confidence: HIGH
```

---

**Related Skills:**
- `postmortem-planner` - Uses proper fix plan as action items in postmortem
- `minimal-fix-planner` - The hotfix planner that the proper fix supersedes
- `test-scenario-generator` - Generates detailed test scenarios for the proper fix test plan
- `safe-change-boundary-detector` - Validates the proper fix scope is safe to change
