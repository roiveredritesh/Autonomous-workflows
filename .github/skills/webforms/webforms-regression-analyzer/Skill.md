---
name: webforms-regression-analyzer
description: Identifies functionality that could regress from proposed changes and creates regression test scenarios.
---

## Purpose
Identifies functionality that could regress from proposed changes and creates regression test scenarios.

## Input Requirements
```yaml
change:
  description: <what's changing>
  affected_files: [<files modified>]
  affected_components: [<components>]
  change_type: <feature|bugfix|refactor>
```

## Processing Steps

1. **Map Change Impact**
   - What code changes?
   - What functionality uses this code?

2. **Identify Related Functionality**
   - What else could be affected?
   - What depends on this?

3. **Determine Regression Risks**
   - What could break?
   - How likely is regression?

4. **Plan Regression Testing**
   - What to test?
   - How to validate?

## Output Format

```yaml
regression_analysis:
  
  change_impact_map:
    modified_components: [<list>]
    related_functionality: [<list>]
    dependent_systems: [<list>]
  
  regression_risks:
    - risk: <what could break>
      probability: <high|medium|low>
      severity: <if it breaks>
      related_functionality: <what's at risk>
  
  regression_test_scenarios:
    - scenario: <test scenario>
      functionality: <what to test>
      criticality: <critical|high|medium|low>
      test_type: <manual|automated|both>
  
  test_coverage:
    functionality_to_test: <count>
    critical_tests: <count>
    estimated_test_effort: <hours>
  
  recommendations:
    must_test: [<critical tests>]
    should_test: [<important tests>]
    could_test: [<nice to have>]
```

## Related Skills
- `test-scenario-generator` - Creates test scenarios
- `minimal-diff-planner` - Minimizes change scope
- `safe-change-boundary-detector` - Identifies safe areas
