---
name: safe-change-boundary-detector
description: Identifies safe modification points in legacy WebForms code where changes won't break existing functionality or violate public contracts.
---

# Safe Change Boundary Detector

## Quick Example

**Input:** Modify `CustomerList.aspx.cs` - add export method
**Output:** Safe: Add new private method | Unsafe: Change public interface
**Time:** 90 seconds

---

## Purpose
Identifies safe modification points in legacy WebForms code where changes won't break existing functionality or violate public contracts.

## Input

```yaml
change_scope:
  file_path: <file to modify>
  method_name: <method being changed>
  change_type: add|modify|delete
  affected_controls: [<controls>]
```

## Output

```yaml
safe_boundaries:
  file_analyzed: <path>

  public_api:
    exposed_methods: [<list>]
    exposed_properties: [<list>]
    must_not_change: [<what would break callers>]

  safe_modifications:
    - area: <description>
      safety: SAFE
      reason: <why safe>

  unsafe_modifications:
    - area: <description>
      safety: UNSAFE
      reason: <why unsafe>
      impact: <what breaks>

  recommendations:
    - <actionable recommendation>

  risk_assessment:
    change_risk: LOW|MEDIUM|HIGH
    regression_risk: LOW|MEDIUM|HIGH

  confidence: HIGH|MEDIUM|LOW
```

## Safe Change Categories

### ALWAYS SAFE
- Add new private methods
- Add new private fields
- Modify method internals (if behavior unchanged)
- Add new event handlers
- Add new controls to page

### USUALLY SAFE
- Add optional parameters (with defaults)
- Add new public methods (not breaking existing)
- Add ViewState items

### RISKY (Needs Validation)
- Change method signatures
- Modify return types
- Remove ViewState items

### NEVER SAFE (Requires Justification)
- Change public API contracts
- Break WebForms lifecycle
- Remove public methods

## DO:
✅ Check for public API exposure
✅ Validate WebForms lifecycle compliance
✅ Verify Telerik control contracts
✅ Identify all callers/dependents
✅ Assess regression risk
✅ Document safe boundaries clearly

## DON'T:
❌ Assume internal methods are safe to change
❌ Skip checking for event handler usage
❌ Ignore ViewState dependencies
❌ Miss control tree dependencies
❌ Overlook data binding impacts

## Error Conditions

**IF public API change detected:**
```
1. Flag as UNSAFE
2. List impacted callers
3. Require explicit justification
4. Document breaking change
```

**IF lifecycle violation detected:**
```
1. Flag as UNSAFE
2. Explain violation
3. Suggest safe alternative
4. Document risk
```

## Example 1: Safe Addition

**Input:**
```yaml
file_path: CustomerList.aspx.cs
change_type: add
description: "Add private ExportToExcel method"
```

**Output:**
```yaml
public_api:
  must_not_change: [GetCustomers, OnPageLoad]

safe_modifications:
  - area: "Add private ExportToExcel() method"
    safety: SAFE
    reason: "New private method, no public exposure"

recommendations:
  - "Follow existing export pattern from OrderList"
  - "Keep method private"
  - "Test with existing page lifecycle"

change_risk: LOW
confidence: HIGH
```

## Example 2: Unsafe Modification

**Input:**
```yaml
file_path: CustomerRepository.cs
change_type: modify
description: "Change GetCustomers() return type from List to IEnumerable"
```

**Output:**
```yaml
public_api:
  exposed_methods: [GetCustomers, SaveCustomer]
  must_not_change: [GetCustomers signature]

unsafe_modifications:
  - area: "Change GetCustomers() return type"
    safety: UNSAFE
    reason: "Public API change - breaks 15 callers"
    impact: "All pages using GetCustomers will break"

recommendations:
  - "Add new GetCustomersEnumerable() method instead"
  - "Deprecate old method gradually"
  - "Or keep List<T> return type"

change_risk: HIGH
regression_risk: HIGH
confidence: HIGH
```

---

**Related Skills:**
- `webforms-lifecycle-analyzer` - Validates lifecycle compliance
- `telerik-impact-checker` - Checks Telerik contracts
- `minimal-diff-planner` - Plans minimal safe changes