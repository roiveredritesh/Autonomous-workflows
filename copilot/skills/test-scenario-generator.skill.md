---
skill: test-scenario-generator
version: 2.0.0
category: generation
complexity: medium
estimated_time: 2-3 minutes
priority: high
last_updated: 2026-01-18
---

# Test Scenario Generator

## Quick Example

**Input:** Excel export feature with 4 acceptance criteria
**Output:** 8 test scenarios (happy path + 4 edge cases) with steps and data
**Time:** 2 minutes

---

## Purpose
Creates comprehensive test scenarios based on acceptance criteria, covering happy paths, edge cases, and error conditions.

## Input

```yaml
feature:
  description: <feature>
  acceptance_criteria: [<criteria>]
  edge_cases: [<edge cases>]
  user_roles: [<roles if relevant>]
```

## Output

```yaml
test_scenarios:
  scenarios:
    - id: TS-001
      name: <scenario name>
      criterion: <which criterion>
      type: happy_path|edge_case|error_condition
      priority: critical|high|medium|low

      steps:
        - <action>
        - <action>

      expected: [<results>]
      test_data: [<data needed>]

  coverage:
    criteria_covered: <count>/<total>
    edge_cases_covered: <count>/<total>

  test_data_needed:
    valid: [<examples>]
    invalid: [<examples>]
    boundary: [<examples>]

  confidence: HIGH|MEDIUM|LOW
```

## Scenario Types

### Happy Path
- User follows expected flow
- Valid inputs
- Successful outcome
- Priority: CRITICAL

### Edge Cases
- Boundary conditions
- Unusual but valid inputs
- Performance limits
- Priority: HIGH/MEDIUM

### Error Conditions
- Invalid inputs
- System errors
- User errors
- Priority: MEDIUM/LOW

## DO:
✅ Cover all acceptance criteria
✅ Include happy path for each criterion
✅ Add edge case scenarios
✅ Include error conditions
✅ Specify test data needed
✅ Mark automation feasibility
✅ Prioritize scenarios

## DON'T:
❌ Skip any acceptance criteria
❌ Omit edge cases
❌ Forget error handling
❌ Miss boundary conditions
❌ Leave steps vague
❌ Skip test data planning

## Error Conditions

**IF acceptance criteria incomplete:**
```
1. Flag incomplete criteria
2. Generate basic scenarios
3. Note gaps in coverage
4. Recommend criteria refinement
```

**IF edge cases missing:**
```
1. Infer common edge cases:
   - Empty/null inputs
   - Max/min boundaries
   - Concurrent operations
   - Timeout scenarios
2. Note inferred cases
3. Recommend validation
```

## Example: Excel Export Feature

**Input:**
```yaml
description: "Add Excel export to customer list"
acceptance_criteria:
  - "Export button visible on page"
  - "Export includes filtered results only"
  - "File format is .xlsx"
  - "Max 10,000 rows with warning"
edge_cases:
  - "Empty result set"
  - "Exactly 10,000 rows"
  - "Over 10,000 rows"
  - "Export during concurrent operations"
```

**Output:**
```yaml
scenarios:
  - id: TS-001
    name: "Happy path - export filtered results"
    criterion: "Export includes filtered results"
    type: happy_path
    priority: critical

    steps:
      - "Navigate to customer list"
      - "Apply filter: Status = Active"
      - "Click Export button"
      - "Download completes"

    expected:
      - "Excel file downloads"
      - "Contains only Active customers"
      - "All visible columns included"
      - "File opens in Excel"

    test_data:
      - "Database with 500 Active customers"
      - "Mixed Active/Inactive customers"

  - id: TS-002
    name: "Export empty result set"
    criterion: "Export handles no results"
    type: edge_case
    priority: high

    steps:
      - "Apply filter with no matches"
      - "Click Export button"

    expected:
      - "Excel file with headers only"
      - "OR friendly message: 'No data to export'"

    test_data:
      - "Filter that returns 0 results"

  - id: TS-003
    name: "Export exactly 10,000 rows"
    criterion: "Max 10,000 rows limit"
    type: edge_case
    priority: high

    steps:
      - "Filter returns exactly 10,000 customers"
      - "Click Export"

    expected:
      - "All 10,000 rows exported"
      - "NO warning shown"

    test_data:
      - "Database with 10,000+ customers"

  - id: TS-004
    name: "Export over 10,000 rows"
    criterion: "Warning for large export"
    type: edge_case
    priority: high

    steps:
      - "Filter returns 15,000 customers"
      - "Click Export"

    expected:
      - "Warning message displayed"
      - "Only first 10,000 exported"
      - "OR option to download in batches"

  - id: TS-005
    name: "Export with timeout"
    criterion: "Handle export errors"
    type: error_condition
    priority: medium

    steps:
      - "Start export"
      - "Simulate server timeout"

    expected:
      - "Error message shown"
      - "User can retry"
      - "No partial file downloaded"

coverage:
  criteria_covered: 4/4
  edge_cases_covered: 4/4

test_data_needed:
  valid:
    - "500 customer records"
    - "10,000 customer records"
    - "15,000 customer records"
  invalid:
    - "No matching records"
  boundary:
    - "Exactly 10,000 records"
    - "10,001 records"

confidence: HIGH
```

## Test Data Matrix

### Valid Data
- Typical production-like data
- Various data types
- Representative edge cases

### Invalid Data
- Null/empty values
- Wrong types
- Out of range values
- Special characters

### Boundary Data
- Minimum values
- Maximum values
- Just below/above limits

## Prioritization

### Critical
- Happy path for core functionality
- Data corruption risks
- Security scenarios

### High
- Common edge cases
- Performance limits
- User-facing errors

### Medium
- Rare edge cases
- Non-critical errors
- Recovery scenarios

### Low
- Cosmetic issues
- Documentation validation
- Nice-to-have validations

---

**Related Skills:**
- `acceptance-criteria-expander` - Expands criteria for testing
- `edge-case-detector` - Identifies edge cases
- `webforms-regression-analyzer` - Identifies regression scenarios
