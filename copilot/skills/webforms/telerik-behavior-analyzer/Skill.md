# Telerik Behavior Analyzer Skill

## Purpose
Analyzes how Telerik controls behave in specific scenarios to troubleshoot issues or plan changes.

## Input Requirements
```yaml
analysis:
  control_type: <RadGrid|RadComboBox|etc>
  scenario: <what's being analyzed>
  observed_behavior: <what's happening>
  expected_behavior: <what should happen>
```

## Processing Steps

1. **Review Control Documentation**
   - Telerik behavior patterns
   - Known issues and workarounds
   - Version-specific behavior

2. **Analyze Lifecycle Interaction**
   - When does issue occur in lifecycle?
   - What events are involved?

3. **Identify Root Cause**
   - Telerik control issue?
   - Usage issue?
   - Configuration issue?

4. **Provide Analysis**
   - Why is this happening?
   - How to fix or workaround?

## Output Format

```yaml
telerik_behavior_analysis:
  
  control_analyzed: <control type>
  scenario: <scenario>
  
  observed_vs_expected:
    observed: <what's happening>
    expected: <what should happen>
  
  root_cause_analysis:
    cause: <what's causing it>
    confidence: <high|medium|low>
    evidence: [<supporting information>]
  
  control_behavior:
    documented_behavior: <what documentation says>
    actual_behavior: <what actually happens>
    discrepancy: <if different>
  
  recommendations:
    workaround: <how to fix>
    fix_approach: <proper solution>
    testing: [<how to verify>]
  
  related_issues:
    known_issues: [<list>]
    similar_scenarios: [<list>]
```

## Related Skills
- `linq-query-tracer` - For data binding issues
- `safe-change-boundary-detector` - For safe modifications
