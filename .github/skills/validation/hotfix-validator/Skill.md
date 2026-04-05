---
name: hotfix-validator
description: Validates that a hotfix is safe to deploy by checking: change is minimal, no regressions introduced, rollback is ready, and all safety criteria are met.
---

# Hotfix Validator

## Quick Example

**Input:** 2 files changed, 3 lines changed, null guard fix, rollback: git revert, tests: 2 smoke tests passed
**Output:** Safety score: 95/100 — GO for deployment. All validation criteria met: minimal change, tested, rollback ready, no API changes, no lifecycle violations.
**Time:** 2-3 minutes

---

## Purpose
Validates that a hotfix is safe to deploy by checking: change is minimal, no regressions introduced, rollback is ready, and all safety criteria are met.

## Input

```yaml
input:
  files_changed: <list of files modified>
  lines_changed_count: <total lines added + removed>
  test_results: <summary of smoke tests run — passed/failed>
  rollback_plan: <description of rollback procedure>
  change_description: <what the hotfix does>
  has_passed_staging: <true|false>
  time_pressure: LOW|MEDIUM|HIGH
```

## Output

```yaml
output:
  safety_score: <0-100>
  deployment_recommendation: GO|NO_GO|GO_WITH_CONDITIONS
  recommendation_reason: <explanation>
  validation_checklist:
    - criterion: <safety criterion>
      result: PASS|FAIL|WARNING
      detail: <explanation>
  blocking_issues:
    - issue: <what prevents deployment>
      severity: CRITICAL|HIGH
      resolution: <what to do>
  conditions: [<conditions for GO_WITH_CONDITIONS>]
  risk_summary:
    change_risk: LOW|MEDIUM|HIGH
    test_coverage: LOW|MEDIUM|HIGH
    rollback_readiness: LOW|MEDIUM|HIGH
    overall_risk: LOW|MEDIUM|HIGH
  confidence: HIGH|MEDIUM|LOW
```

## DO:
✅ Verify rollback procedure is tested, not just documented
✅ Check that lines_changed_count is under 20 for a true hotfix
✅ Validate that no public API signatures were changed
✅ Confirm staging deployment and smoke tests passed before production approval
✅ Apply extra scrutiny to changes in high-traffic or payment-critical paths

## DON'T:
❌ Approve a hotfix with untested rollback procedure
❌ Deploy more than 20 lines of change as a hotfix — it's not minimal
❌ Skip staging validation even under time pressure — it takes 10 minutes
❌ Override NO_GO without escalating to engineering manager
❌ Combine multiple fixes into one hotfix — one fix per hotfix

## Error Conditions

**IF test results are not provided:**
```
1. Downgrade recommendation to GO_WITH_CONDITIONS
2. Require: run minimum smoke tests before production deployment
3. Flag: NO_TEST_RESULTS — cannot recommend GO without any test evidence
```

**IF rollback plan is absent:**
```
1. HARD BLOCK — set recommendation to NO_GO
2. Return: ROLLBACK_REQUIRED — no hotfix deployment without verified rollback
```

**IF staging is unavailable:**
```
1. Increase required monitoring post-deploy to 60 minutes
2. Require: 2 engineering approvals instead of 1
3. Flag: NO_STAGING — elevated risk, compensate with extended monitoring
```

## Processing Steps

1. **Change Size Validation:** Count lines_changed_count. Score: 1-5 lines = 100, 6-10 lines = 90, 11-20 lines = 80, 21-50 lines = 60 (WARNING), >50 lines = 40 (NOT a hotfix).

2. **API Contract Check:** Scan changed files for: method signature changes, new parameters, removed methods, changed return types. Any API change → FAIL (20-point deduction).

3. **Test Coverage Assessment:** Evaluate: smoke tests passed (covers fixed scenario + 1 regression) = HIGH. Only unit tests = MEDIUM. No tests = LOW. LOW → BLOCKING unless acknowledged with escalation.

4. **Rollback Readiness:** Verify: rollback procedure is documented, rollback has been tested (not just theoretically possible), estimated rollback time <15 minutes. Untested rollback → 20-point deduction.

5. **Staging Validation:** has_passed_staging = true → no deduction. false → 30-point deduction. Staging validation is required unless unavailable (then compensate with other controls).

6. **Safety Score Calculation:** Start at 100. Deductions: >20 lines changed (-20), API change (-30), no tests (-20), untested rollback (-20), no staging (-30), single-fix rule violated (-20). Minimum 0. Score 90+ = GO, 70-89 = GO_WITH_CONDITIONS, <70 = NO_GO.

7. **Final Recommendation:** Assemble blocking issues (any FAIL criterion). Conditions for GO_WITH_CONDITIONS (WARNING criteria). Clear explanation of recommendation.

## Example

**Input:**
```yaml
files_changed: ["ShippingCalculator.cs", "ShippingCalculatorTests.cs"]
lines_changed_count: 4
test_results: "2/2 smoke tests passed: S1 (null carrier) and S2 (carrier assigned). Automated test added and passing."
rollback_plan: "Trigger CI/CD pipeline 'Deploy v2.14.1' — tested in staging, estimated 8 minutes"
change_description: "Added null guard: if (carrier == null) return DefaultRate"
has_passed_staging: true
time_pressure: HIGH
```

**Output:**
```yaml
safety_score: 97
deployment_recommendation: GO
recommendation_reason: "Hotfix meets all safety criteria: minimal change (4 lines), tested (smoke + automated), rollback tested and ready, staging passed."
validation_checklist:
  - {criterion: "Change is minimal (≤20 lines)", result: PASS, detail: "4 lines changed — excellent, well under 20-line hotfix limit"}
  - {criterion: "No public API changes", result: PASS, detail: "Method signature unchanged: Calculate(Order, Carrier) returns decimal"}
  - {criterion: "Smoke tests passed", result: PASS, detail: "2/2 smoke tests passed including the fixed scenario and regression test"}
  - {criterion: "Rollback procedure documented and tested", result: PASS, detail: "CI/CD rollback pipeline tested in staging, 8-minute estimated rollback"}
  - {criterion: "Staging validation passed", result: PASS, detail: "Deployed to staging, smoke tests run, no new errors"}
  - {criterion: "Single fix only", result: PASS, detail: "Fix addresses exactly one root cause: null carrier guard"}
blocking_issues: []
conditions: []
risk_summary:
  change_risk: LOW
  test_coverage: HIGH
  rollback_readiness: HIGH
  overall_risk: LOW
confidence: HIGH
```

---

**Related Skills:**
- `hotfix-deployment-planner` - Plans the deployment after validator gives GO recommendation
- `safe-change-boundary-detector` - Validates API contract and change boundary safety
- `hotfix-test-generator` - Generates the smoke tests that this validator checks
- `production-verification-checker` - Verifies production health after deployment
