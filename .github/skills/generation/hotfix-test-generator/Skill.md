---
name: hotfix-test-generator
description: Generates rapid smoke tests for hotfix validation focused on critical paths, enabling fast go/no-go decision before production deployment.
---

# Hotfix Test Generator

## Quick Example

**Input:** Hotfix: null guard added to ShippingCalculator, affected feature: order submission, critical path: checkout
**Output:** 5-item smoke test checklist, 2 automated test suggestions, validation criteria — all focused on critical path verification, completable in <10 minutes
**Time:** 1-2 minutes

---

## Purpose
Generates rapid smoke tests for hotfix validation focused on critical paths, enabling fast go/no-go decision before production deployment.

## Input

```yaml
input:
  affected_feature: <feature or page that was changed>
  hotfix_description: <what the hotfix does>
  critical_user_paths: <list of user workflows that must continue working>
  test_environment: STAGING|PRE_PROD|PRODUCTION_CANARY
  time_budget_minutes: <max time available for testing, default 15>
  automated_tests_available: true|false
```

## Output

```yaml
output:
  smoke_test_checklist:
    - id: <S1..Sn>
      priority: MUST_PASS|SHOULD_PASS
      description: <what to test>
      how_to_test: <exact steps or URL>
      expected_result: <what success looks like>
      time_estimate_minutes: <minutes>
  automated_tests:
    - test_name: <method name>
      test_class: <class name>
      assertion: <what it verifies>
      why_critical: <why this test is essential for this hotfix>
  validation_criteria:
    go_criteria: [<conditions that make deployment safe>]
    no_go_criteria: [<conditions that block deployment>]
  total_time_estimate_minutes: <sum of all tests>
  confidence: HIGH|MEDIUM|LOW
```

## DO:
✅ Focus on the exact failure scenario the hotfix addresses — test that it's fixed
✅ Include regression tests for the most critical adjacent feature paths
✅ Keep smoke tests to <15 minutes total — speed matters for hotfixes
✅ Mark each test as MUST_PASS or SHOULD_PASS — MUST_PASS failures block deployment
✅ Provide exact steps, not vague "test the feature" instructions

## DON'T:
❌ Write comprehensive test suites — this is smoke testing for rapid validation
❌ Include tests for unrelated features — focus on affected paths only
❌ Allow any MUST_PASS test to fail — escalate to rollback if they do
❌ Skip regression testing — hotfixes can break adjacent features
❌ Require more than 15 minutes for smoke testing — time pressure is real in hotfixes

## Error Conditions

**IF no test environment is available:**
```
1. Generate production canary test steps with minimal user impact
2. Flag: NO_STAGING — testing in production canary requires extra caution
3. Add NO_GO criterion: any new error in canary triggers immediate rollback
```

**IF affected feature is completely down:**
```
1. First smoke test must be: "Does the feature load without error?"
2. All other tests depend on passing this first gate
```

**IF time budget is under 5 minutes:**
```
1. Limit to 3 MUST_PASS tests only
2. Flag: EXTREMELY_LIMITED — only minimum critical path tested
3. Recommend extended monitoring post-deployment as compensation
```

## Processing Steps

1. **Critical Path Analysis:** Identify the primary user workflow that was broken. List the 3-5 most critical paths: the broken scenario, adjacent paths that use same code, downstream paths that depend on this feature.

2. **Smoke Test Design:** For each critical path: write 1 smoke test. Each test has: what to test (user action), exact URL or test data, expected result (specific, not "works"). Estimate time: simple navigation = 1min, form submission = 2min, complex workflow = 3min.

3. **Priority Classification:** MUST_PASS: the specific scenario that was broken, core business flow (order submission, login, main navigation). SHOULD_PASS: related features, secondary workflows.

4. **Automated Test Identification:** From existing test suite, identify tests that cover: the fixed method directly, callers of the fixed method, integration tests covering the affected page.

5. **Time Budget Allocation:** Sum test times. If exceeds budget: remove SHOULD_PASS tests first. Keep all MUST_PASS tests regardless of time. Flag if MUST_PASS alone exceeds budget.

6. **Validation Criteria:** GO: all MUST_PASS tests pass, error rate in monitoring returns to baseline. NO_GO: any MUST_PASS test fails, new errors appear in logs, performance significantly degrades.

## Example

**Input:**
```yaml
affected_feature: "Order submission and shipping rate calculation"
hotfix_description: "Added null guard to ShippingCalculator.Calculate() — returns DefaultRate when carrier is null"
critical_user_paths:
  - "Customer submits order with assigned carrier"
  - "Customer submits order with no carrier (draft)"
  - "Admin creates order from back office"
test_environment: STAGING
time_budget_minutes: 15
automated_tests_available: true
```

**Output:**
```yaml
smoke_test_checklist:
  - id: S1
    priority: MUST_PASS
    description: "Order with no carrier submits successfully (the fixed scenario)"
    how_to_test: "Create order, leave Carrier field empty, click Submit Order"
    expected_result: "Order created successfully with $0.00 shipping. No error page."
    time_estimate_minutes: 3
  - id: S2
    priority: MUST_PASS
    description: "Order with carrier assigned submits with correct rate (regression)"
    how_to_test: "Create order, select 'DHL Express' carrier, click Submit Order"
    expected_result: "Order created with DHL rate applied. Check TotalAmount includes shipping."
    time_estimate_minutes: 3
  - id: S3
    priority: MUST_PASS
    description: "Order list page loads — no JavaScript errors"
    how_to_test: "Navigate to /Orders/OrderList.aspx — check browser console for errors"
    expected_result: "Page loads in <3s, RadGrid populates, no console errors"
    time_estimate_minutes: 2
  - id: S4
    priority: SHOULD_PASS
    description: "Admin order creation from back office"
    how_to_test: "Login as admin, navigate to /Admin/CreateOrder.aspx, submit order"
    expected_result: "Order created successfully"
    time_estimate_minutes: 3
  - id: S5
    priority: SHOULD_PASS
    description: "Bulk order import with no carrier"
    how_to_test: "Import test CSV with empty carrier column via /Admin/BulkImport.aspx"
    expected_result: "Import completes, orders created with DefaultRate"
    time_estimate_minutes: 3
automated_tests:
  - test_name: "Calculate_ReturnsDefaultRate_WhenCarrierIsNull"
    test_class: "ShippingCalculatorTests"
    assertion: "Assert.AreEqual(DefaultRate, result) when carrier param is null"
    why_critical: "Directly tests the fixed null guard"
  - test_name: "Calculate_ReturnsCorrectRate_WhenCarrierAssigned"
    test_class: "ShippingCalculatorTests"
    assertion: "Assert rate matches expected DHL rate for test order"
    why_critical: "Regression test — ensure fix didn't break the happy path"
validation_criteria:
  go_criteria:
    - "S1 and S2 and S3 all pass"
    - "Automated tests pass"
    - "No new ERROR or CRITICAL entries in staging logs after smoke test"
  no_go_criteria:
    - "Any MUST_PASS test fails"
    - "New exceptions appear in log that weren't present before hotfix"
    - "Order submission time exceeds 10s (performance regression)"
total_time_estimate_minutes: 14
confidence: HIGH
```

---

**Related Skills:**
- `test-scenario-generator` - Generates comprehensive test scenarios (for normal bug fixes)
- `hotfix-validator` - Validates overall hotfix safety including test results
- `production-verification-checker` - Verifies production health after hotfix deployment
- `minimal-fix-implementer` - Generates the code fix that these tests validate
