---
name: api-contract-analyzer
description: Analyzes public API contracts (method signatures, return types, exceptions) for breaking changes and provides migration paths for affected callers.
---

# API Contract Analyzer

## Quick Example

**Input:** Original: `Calculate(Order order, Carrier carrier)`, New: `Calculate(Order order, Carrier carrier, decimal defaultRate)`, 7 callers
**Output:** BREAKING CHANGE — new required parameter breaks all 7 callers. Migration: make defaultRate optional with default value, or update all callers before deploying.
**Time:** 3-5 minutes

---

## Purpose
Analyzes public API contracts (method signatures, return types, exceptions) for breaking changes and provides migration paths for affected callers.

## Input

```yaml
input:
  original_signatures:
    - method: <full signature including return type and parameters>
      access: public|internal|protected
      exceptions_documented: [<list>]
  new_signatures:
    - method: <full signature>
      access: public|internal|protected
      exceptions_documented: [<list>]
  caller_list: <list of files or classes that call these methods>
  change_context: HOTFIX|FEATURE|REFACTOR|PERFORMANCE
```

## Output

```yaml
output:
  breaking_changes:
    - change_id: <B1..Bn>
      severity: CRITICAL|HIGH|MEDIUM|LOW
      original_signature: <before>
      new_signature: <after>
      breaking_reason: <why callers break>
      affected_callers: [<list>]
      migration_path:
        option_1: <preferred migration>
        option_2: <alternative>
        breaking_if_not_migrated: <consequence>
  non_breaking_changes:
    - change: <description>
      reason_non_breaking: <explanation>
  caller_impact:
    - caller: <class or file>
      calls_affected: <count>
      required_changes: [<what caller must change>]
      estimated_change_effort: LOW|MEDIUM|HIGH
  overall_assessment:
    is_backward_compatible: true|false
    breaking_changes_count: <count>
    callers_affected: <count>
    can_deploy_safely: true|false
  recommendations:
    - recommendation: <description>
      priority: critical|high|medium
  confidence: HIGH|MEDIUM|LOW
```

## DO:
✅ Check all categories of breaking changes: added required parameters, removed methods, changed return types, changed exception contracts, narrowed access level
✅ Verify optional parameters (default values) don't break binary compatibility in .NET assemblies
✅ Check internal methods if callers are in different assemblies (friend assemblies)
✅ Flag exception contract changes — callers may handle specific exception types
✅ Verify interface implementations are still compatible if interface changed

## DON'T:
❌ Treat all changes as breaking — adding optional parameters is non-breaking
❌ Miss implicit contract changes — changing documented behavior without signature change
❌ Overlook ASP.NET WebForms-specific contracts: event handler signatures, ObjectDataSource TypeName methods
❌ Forget to check .aspx markup — ObjectDataSource TypeName references method by name
❌ Ignore inheritance — changes to base class methods affect all derived classes

## Error Conditions

**IF caller list is not provided:**
```
1. Search codebase for method name and class name usage
2. Flag: CALLERS_INFERRED — may miss dynamic invocation (reflection, late binding)
3. Return caller list found by grep for manual verification
```

**IF change is in a base class:**
```
1. Find all derived classes
2. Check if derived classes override the changed method
3. Flag: INHERITANCE_IMPACT — all derived classes are potential callers
```

**IF signatures use generics or complex types:**
```
1. Check covariance/contravariance rules for generic types
2. Flag: GENERIC_CONTRACT — generic type changes may have non-obvious breaking implications
```

## Processing Steps

1. **Signature Comparison:** For each method pair (original vs new): compare return type, parameter types, parameter count, parameter names, access modifier, generic constraints.

2. **Breaking Change Detection:** Breaking: added required parameter, removed parameter, changed parameter type, changed return type, narrowed access (public→internal), added checked exception (not applicable in C#), changed covariance.

3. **Non-Breaking Detection:** Non-breaking: added optional parameter (default value), widened access (internal→public), added method overload, changed parameter names only (in C# without named argument callers).

4. **Caller Impact Analysis:** For each breaking change: find each caller. Determine: what each caller must change (add argument, handle new type, handle removed method). Estimate effort: LOW = trivial, MEDIUM = requires logic change, HIGH = requires architectural change.

5. **Migration Path Generation:** For added required parameter: option 1 = make optional with default (backward compat), option 2 = update all callers. For removed method: option 1 = deprecate first and add new, option 2 = update all callers.

6. **ObjectDataSource Check:** In WebForms, ObjectDataSource references methods by string name. Search .aspx files for TypeName and SelectMethod/InsertMethod/etc. that reference changed methods.

7. **Deployment Safety Assessment:** can_deploy_safely = false if any breaking change detected and callers are not all updated. Include: estimated effort to migrate all callers.

## Example

**Input:**
```yaml
original_signatures:
  - method: "public decimal Calculate(Order order, Carrier carrier)"
    access: public
    exceptions_documented: [NullReferenceException]
  - method: "public List<Carrier> GetCarriers()"
    access: public
new_signatures:
  - method: "public decimal Calculate(Order order, Carrier carrier, decimal defaultRate = 0m)"
    access: public
    exceptions_documented: []
  - method: "public IEnumerable<Carrier> GetCarriers()"
    access: public
caller_list: ["OrderProcessor.cs", "BulkShipper.cs", "RateComparator.cs", "ShippingPage.aspx.cs"]
change_context: HOTFIX
```

**Output:**
```yaml
breaking_changes:
  - change_id: B1
    severity: HIGH
    original_signature: "public List<Carrier> GetCarriers()"
    new_signature: "public IEnumerable<Carrier> GetCarriers()"
    breaking_reason: "Return type narrowed from List<Carrier> to IEnumerable<Carrier>. Callers using List<T> methods (.Sort(), .RemoveAt(), index access) will fail to compile."
    affected_callers: ["RateComparator.cs", "ShippingPage.aspx.cs"]
    migration_path:
      option_1: "Change return type back to List<Carrier> — callers don't need to change"
      option_2: "Update callers: add .ToList() where List<T> methods are used"
      breaking_if_not_migrated: "Compile error in callers using List<T>-specific methods"
non_breaking_changes:
  - change: "Calculate() added optional parameter defaultRate = 0m"
    reason_non_breaking: "Optional parameter with default value — existing callers compile unchanged, behavior unchanged for existing calls"
  - change: "Calculate() exception contract: removed NullReferenceException documentation"
    reason_non_breaking: "Callers don't catch NullReferenceException (verified by inspection)"
caller_impact:
  - caller: "RateComparator.cs"
    calls_affected: 1
    required_changes: ["Change var carriers = GetCarriers() usage — add .ToList() if using List methods"]
    estimated_change_effort: LOW
  - caller: "ShippingPage.aspx.cs"
    calls_affected: 2
    required_changes: ["Add .ToList() after GetCarriers() where indexing is used"]
    estimated_change_effort: LOW
overall_assessment:
  is_backward_compatible: false
  breaking_changes_count: 1
  callers_affected: 2
  can_deploy_safely: false
recommendations:
  - recommendation: "Change GetCarriers() return type back to List<Carrier> for backward compatibility — IEnumerable has no benefit for callers"
    priority: critical
  - recommendation: "If IEnumerable is intentional, update RateComparator.cs and ShippingPage.aspx.cs before deploying"
    priority: high
confidence: HIGH
```

---

**Related Skills:**
- `safe-change-boundary-detector` - Determines safe change boundaries before API changes
- `dependency-mapper` - Maps all dependencies on changed components
- `webforms-lifecycle-validator` - Validates WebForms-specific API contract adherence
- `hotfix-validator` - Checks API contract as part of hotfix safety validation
