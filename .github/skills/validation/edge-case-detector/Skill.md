---
name: edge-case-detector
description: Identifies edge cases, boundary conditions, and error scenarios that must be handled in acceptance criteria and implementation.
---

## Quick Example

**Input:** "Add Excel export to customer list"
**Output:** core_need: export filtered data to xlsx; 3 must-have requirements; 2 questions (columns? row limit?)

---

## Purpose
Identifies edge cases, boundary conditions, and error scenarios that must be handled in acceptance criteria and implementation.

## Input Requirements
```yaml
feature:
  description: <feature description>
  requirements: [<requirements>]
  data_involved: [<types of data>]
  user_roles: [<roles that interact>]
  systems_involved: [<systems>]
```

## Processing Steps

1. **Boundary Analysis**
   - Empty values
   - Null values
   - Maximum values
   - Minimum values

2. **State Analysis**
   - Initial state
   - State transitions
   - Invalid states

3. **Concurrency Analysis**
   - Simultaneous operations
   - Race conditions
   - Timing issues

4. **Permission Analysis**
   - No access
   - Partial access
   - Full access

5. **Data Quality Analysis**
   - Invalid formats
   - Special characters
   - Malformed data

## Output Format

```yaml
edge_case_analysis:
  
  boundary_conditions:
    empty_values:
      - scenario: <empty condition>
        handling: <what should happen>
        risk: <low|medium|high>
    
    null_values:
      - scenario: <null condition>
        handling: <what should happen>
        risk: <low|medium|high>
    
    maximum_values:
      - scenario: <max condition>
        handling: <what should happen>
        risk: <low|medium|high>
    
    minimum_values:
      - scenario: <min condition>
        handling: <what should happen>
        risk: <low|medium|high>
  
  state_edge_cases:
    - edge_case: <specific state scenario>
      description: <what's special about it>
      handling: <required behavior>
      acceptance_criterion: <testable criterion>
  
  concurrency_scenarios:
    - scenario: <concurrent operation>
      risk: <low|medium|high>
      handling: <how to prevent/handle>
      test_approach: <how to test>
  
  permission_scenarios:
    - scenario: <permission case>
      user_type: <user without this permission>
      expected_behavior: <what should happen>
      error_message: <if applicable>
  
  data_quality_edge_cases:
    - case: <invalid data scenario>
      example: <concrete example>
      handling: <validation or error>
      user_message: <what user sees>
  
  error_scenarios:
    - error: <possible error>
      trigger: <what causes it>
      handling: <how to handle>
      user_experience: <what user sees>
  
  edge_cases_summary:
    total_edge_cases_identified: <count>
    critical_edge_cases: [<must handle>]
    important_edge_cases: [<should handle>]
    nice_to_have: [<could handle>]
    acceptance_criteria_added: <count>
```

## Edge Case Categories

### Boundary Conditions
Empty/null values, maximum/minimum values, zero items, single item.

### State Edge Cases
Initial state (no data), invalid state transitions, archived-but-cached, locked records.

### Concurrency Scenarios
Multiple users on same data, rapid-fire requests, operation timeouts.

### Permission Scenarios
No access, partial access (view-only), permission revoked mid-operation.

### Data Quality Edge Cases
Invalid formats, special characters, duplicate values, referential integrity violations.

## DO
✅ Identify at least one edge case per Processing Step category
✅ Assign risk level (high/medium/low) to each case
✅ Convert critical edge cases to acceptance criteria
✅ Cover permission and data quality scenarios
✅ Consider concurrent operations for shared data

## DON'T
❌ Only analyze the happy path
❌ Skip empty/null boundary conditions
❌ Ignore concurrent operation scenarios
❌ Omit risk levels from identified cases
❌ Forget permission-denied scenarios

## Error Conditions

**IF no requirements provided:**
- Apply generic edge case patterns (empty, null, max, permissions, concurrent)
- Flag: INFERRED_CASES — validate with stakeholder

## Related Skills
- `acceptance-criteria-generator` - Converts to criteria
- `requirement-extractor` - Identifies requirements
- `test-scenario-generator` - Creates test cases
