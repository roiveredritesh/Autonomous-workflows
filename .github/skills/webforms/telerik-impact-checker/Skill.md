---
name: telerik-impact-checker
description: Validates that proposed changes are compatible with Telerik controls and won't break their behavior or contracts.
---

# Telerik Impact Checker

## Quick Example

**Input:** Change RadGrid binding from server to AJAX
**Output:** Compatible with workaround - preserve ViewState settings
**Time:** 60 seconds

---

## Purpose
Validates that proposed changes are compatible with Telerik controls and won't break their behavior or contracts.

## Input

```yaml
change:
  description: <what's changing>
  affected_controls: [<Telerik control types>]
  control_methods: [<methods being called>]
```

## Output

```yaml
telerik_impact:
  compatible: yes|no|with_workaround

  controls_involved:
    - control: <RadGrid|RadComboBox|etc>
      risk: LOW|MEDIUM|HIGH

  blockers: [<if incompatible>]
  workarounds: [<if needed>]
  testing_needed: [<what to test>]

  confidence: HIGH|MEDIUM|LOW
```

## DO:
✅ Check Telerik control lifecycle
✅ Validate data binding patterns
✅ Verify event handlers intact
✅ Test with Telerik version in use
✅ Document any workarounds

## DON'T:
❌ Break Telerik control contracts
❌ Change binding without validation
❌ Skip lifecycle checks
❌ Ignore known limitations

## Common Telerik Constraints

### RadGrid
- Requires ViewState for state management
- Binding changes affect pagination
- AJAX updates need UpdatePanel

### RadComboBox
- Server binding vs client binding
- LoadOnDemand affects lifecycle
- Item templates must preserve structure

### RadEditor
- Content area modification restricted
- Toolbar customization specific API
- Client-side content access patterns

---

**Related Skills:**
- `webforms-lifecycle-analyzer` - Lifecycle validation
- `safe-change-boundary-detector` - Safe modifications
