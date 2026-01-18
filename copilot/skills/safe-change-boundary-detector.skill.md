# Safe Change Boundary Detector Skill

## Purpose
Identifies safe modification points in legacy WebForms code where changes can be made without breaking other functionality.

## Input Requirements
```yaml
change_scope:
  file_path: <file to modify>
  method_name: <method being changed>
  change_type: <add_feature|bug_fix|refactor>
  affected_controls: [<controls involved>]
```

## Processing Steps

1. **Analyze Code Structure**
   - Identify method dependencies
   - Check event handlers
   - Review control references

2. **Identify Public Interfaces**
   - What's exposed?
   - What's internal?
   - What's safe to change?

3. **Check Dependencies**
   - Who calls this?
   - What depends on this?
   - Where is data used?

4. **Determine Safe Boundaries**
   - What can change safely?
   - What must stay the same?
   - Where are the risks?

## Output Format

```yaml
safe_change_boundary:
  
  file_analyzed: <path>
  
  method_analysis:
    - method: <method name>
      safe_to_modify: <yes|no>
      safe_area: <description>
      unsafe_area: <description>
      public_interface: <what's exposed>
      dependencies: [<what depends>]
  
  boundary_recommendations:
    safe_modifications:
      - <modification>
      - <modification>
    
    unsafe_modifications:
      - <modification>
      - <modification>
  
  public_api_analysis:
    public_methods: [<list>]
    public_properties: [<list>]
    must_not_change: <what would break callers>
  
  internal_usage:
    - item: <internal usage>
      safe_to_change: <yes|no>
      reason: <why>
  
  risk_assessment:
    modification_risk: <low|medium|high>
    regression_risk: <low|medium|high>
    safety_recommendations: [<list>]
```

## Related Skills
- `webforms-lifecycle-analyzer` - Checks lifecycle compliance
- `minimal-diff-planner` - Plans minimal changes
