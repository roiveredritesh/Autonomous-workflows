# Minimal Fix Planner Skill

## Purpose
Plans minimal, targeted fixes for bugs that address root cause without unnecessary refactoring.

## Input Requirements
```yaml
bug:
  root_cause: <identified root cause>
  affected_code: [<code locations>]
  fix_options: [<possible approaches>]
  constraints: [<constraints>]
```

## Processing Steps

1. **Analyze Root Cause**
   - Where is the bug?
   - Why is it happening?
   - What's the minimal fix?

2. **Evaluate Fix Options**
   - Direct fix
   - Workaround
   - Refactoring-based fix
   - Data fix

3. **Choose Minimal Approach**
   - What's the smallest change?
   - Does it address root cause?
   - Can we avoid refactoring?

4. **Plan Implementation**
   - What files change?
   - What lines change?
   - How to test fix?

## Output Format

```yaml
minimal_fix_plan:
  
  bug_analysis:
    root_cause: <explanation>
    bug_location: <file:line>
    why_occurred: <explanation>
  
  fix_options_evaluated:
    - option: <fix approach>
      description: <what it does>
      lines_changed: <estimate>
      refactoring_required: <yes|no>
      pros: [<advantages>]
      cons: [<disadvantages>]
    
    - option: <another approach>
      ...
  
  chosen_fix:
    option: <which option chosen>
    reasoning: <why this is best>
    why_minimal: <why this is minimal>
    why_alternatives_rejected: [<alternatives>]
  
  implementation_plan:
    files_affected: [<files>]
    lines_changed: <range>
    specific_changes:
      - file: <path>
        change: <what changes>
        lines: <line numbers>
    
    refactoring_avoided: [<what we did not refactor>]
    improvements_deferred: [<improvements for later>]
  
  testing_plan:
    verify_fix: <how to confirm bug fixed>
    verify_no_regression: [<what to check>]
  
  validation_checklist:
    - [ ] Fix addresses root cause
    - [ ] No unnecessary refactoring
    - [ ] Minimal changes only
    - [ ] Existing patterns preserved
    - [ ] Can be tested in isolation
```

## Related Skills
- `minimal-diff-planner` - For general minimal planning
- `safe-change-boundary-detector` - For safe modifications
