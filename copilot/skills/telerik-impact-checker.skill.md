# Telerik Impact Checker Skill

## Purpose
Validates that proposed changes are compatible with Telerik controls and won't break their behavior.

## Input Requirements
```yaml
change:
  description: <what's changing>
  affected_controls: [<Telerik control types>]
  control_methods: [<methods being called>]
  data_bindings: [<binding points>]
```

## Processing Steps

1. **Identify Telerik Controls**
   - What Telerik controls are involved?
   - What versions in use?

2. **Check Control Lifecycle**
   - Does change affect initialization?
   - Does change affect binding?
   - Does change affect events?

3. **Validate Data Binding**
   - Is binding pattern preserved?
   - Are binding expressions valid?

4. **Assess Compatibility**
   - Is change compatible?
   - Any known limitations?

## Output Format

```yaml
telerik_impact_assessment:
  
  controls_involved:
    - control_name: <control>
      control_type: <RadGrid|RadComboBox|etc>
      version: <version>
      risk: <low|medium|high>
  
  compatibility_analysis:
    compatible: <yes|no|with_workaround>
    blockers: [<if incompatible>]
    limitations: [<known limitations>]
  
  binding_impact:
    binding_type: <server_binding|client_binding|ajax>
    change_affects_binding: <yes|no>
    binding_broken: <yes|no>
  
  recommendations:
    approach: <recommended approach>
    workarounds: [<if needed>]
    testing_needed: [<what to test>]
```

## Related Skills
- `webforms-lifecycle-analyzer` - For lifecycle issues
- `safe-change-boundary-detector` - For safe modification areas
