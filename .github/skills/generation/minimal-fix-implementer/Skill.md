---
name: minimal-fix-implementer
description: Generates the exact code change for a minimal bug fix with before/after diff, ensuring the change is targeted, safe, and limited to the root cause only.
---

# Minimal Fix Implementer

## Quick Example

**Input:** ShippingCalculator.cs line 87, null carrier causes NullReferenceException, fix: add null guard
**Output:** Exact before/after diff, 2-line change, implementation notes, verification steps
**Time:** 2-3 minutes

---

## Purpose
Generates the exact code change for a minimal bug fix with before/after diff, ensuring the change is targeted, safe, and limited to the root cause only.

## Input

```yaml
input:
  file_path: <path to file to fix>
  line_numbers: <line range of the fix>
  root_cause: <specific technical root cause>
  fix_approach: <chosen fix strategy from minimal-fix-planner>
  existing_code: <the current code to be replaced>
  context_before: <3-5 lines before the change for context>
  context_after: <3-5 lines after the change for context>
```

## Output

```yaml
output:
  fix_summary:
    file: <path>
    lines_changed: <count>
    lines_added: <count>
    lines_removed: <count>
    change_type: GUARD_CLAUSE|NULL_CHECK|FILTER_MOVE|INITIALIZATION|CONDITION_FIX
  before_code: |
    <exact code that will be replaced>
  after_code: |
    <exact replacement code>
  diff: |
    <unified diff format>
  implementation_notes:
    - note: <important consideration about this fix>
  verification_steps:
    - step: <how to verify the fix works>
  side_effects_checked:
    - check: <what was verified to ensure no side effects>
  confidence: HIGH|MEDIUM|LOW
```

## DO:
✅ Show the complete before/after code — not just the changed line
✅ Include 3 lines of context in the diff to show the fix in context
✅ Limit the fix to the minimum lines needed to address the root cause
✅ Verify the fix matches the existing code style (indentation, naming, spacing)
✅ Include explicit verification steps for manual or automated testing

## DON'T:
❌ Change anything beyond the minimum required to fix the root cause
❌ Rename variables or improve code style as part of the fix
❌ Add logging or comments beyond what's needed to understand the fix
❌ Refactor surrounding code "while you're there"
❌ Leave TODO comments in the fix — resolve them now or create a separate ticket

## Error Conditions

**IF existing code does not match the provided line numbers:**
```
1. Re-read the file at the specified path
2. Check if file has been modified since analysis
3. Return: CODE_MISMATCH — re-run analysis with current file content
```

**IF fix requires changes to multiple files:**
```
1. Generate separate before/after for each file
2. Note: MULTI_FILE_FIX — verify all files are changed atomically
```

**IF fix approach changes public method signature:**
```
1. STOP — do not implement
2. Return: SIGNATURE_CHANGE_DETECTED — consult safe-change-boundary-detector first
```

## Processing Steps

1. **Root Cause Mapping:** Identify the exact lines that contain the root cause. Verify the fix approach addresses only those lines.

2. **Minimal Change Design:** Design the smallest possible code change. Prefer: adding a guard clause (2 lines) over restructuring the method. Adding a null check over refactoring the calling code.

3. **Style Matching:** Match exactly: indentation (spaces vs tabs, count), brace style (Allman vs K&R), variable naming convention (`camelCase`, `_prefix`), line endings.

4. **Before/After Generation:** Show: 3 lines of context before the change, the changed lines with `- ` (removed) and `+ ` (added) markers, 3 lines of context after.

5. **Unified Diff:** Generate standard unified diff format: `--- a/path/to/file`, `+++ b/path/to/file`, `@@ -line,count +line,count @@`.

6. **Side Effects Check:** Verify: does the fix change any method signature? Does it affect any other callers? Does it change any behavior beyond the bug case?

7. **Verification Steps:** Generate specific, executable steps: "Call ShippingCalculator.Calculate(null) and verify returns DefaultRate", "Run ShippingCalculator unit test suite", "Submit test order with no carrier in staging".

## Example

**Input:**
```yaml
file_path: "AajLogistics\\Shipping\\ShippingCalculator.cs"
line_numbers: "85-90"
root_cause: "carrier.RateCode accessed without null check — carrier can be null for draft orders"
fix_approach: "Add null guard before property access, return DefaultRate"
existing_code: |
  public decimal Calculate(Order order, Carrier carrier)
  {
      var rate = carrier.RateCode;
      return _rateEngine.GetRate(rate, order.Weight);
  }
context_before: "// Calculate shipping cost for given order and carrier"
context_after: "// Returns decimal rate in USD"
```

**Output:**
```yaml
fix_summary:
  file: "AajLogistics\\Shipping\\ShippingCalculator.cs"
  lines_changed: 1
  lines_added: 2
  lines_removed: 0
  change_type: GUARD_CLAUSE
before_code: |
  public decimal Calculate(Order order, Carrier carrier)
  {
      var rate = carrier.RateCode;
      return _rateEngine.GetRate(rate, order.Weight);
  }
after_code: |
  public decimal Calculate(Order order, Carrier carrier)
  {
      if (carrier == null) return DefaultRate;
      var rate = carrier.RateCode;
      return _rateEngine.GetRate(rate, order.Weight);
  }
diff: |
  --- a/AajLogistics/Shipping/ShippingCalculator.cs
  +++ b/AajLogistics/Shipping/ShippingCalculator.cs
  @@ -85,6 +85,8 @@ namespace AajLogistics.Shipping
   public decimal Calculate(Order order, Carrier carrier)
   {
  +    if (carrier == null) return DefaultRate;
       var rate = carrier.RateCode;
       return _rateEngine.GetRate(rate, order.Weight);
   }
implementation_notes:
  - note: "DefaultRate should be a const or readonly field — verify it exists in the class or add as private const decimal DefaultRate = 0m;"
  - note: "Consider whether null order should also be guarded — check callers"
verification_steps:
  - step: "Run: ShippingCalculatorTests.Calculate_ReturnsDefaultRate_WhenCarrierIsNull — should pass"
  - step: "Submit test order with no carrier in staging — should see $0.00 shipping"
  - step: "Submit test order WITH carrier in staging — should see correct rate (regression check)"
side_effects_checked:
  - check: "Method signature unchanged — no callers affected"
  - check: "DefaultRate return value (0m) verified as acceptable for null carrier business rule"
  - check: "No other code paths affected — guard exits early, remaining code unchanged"
confidence: HIGH
```

---

**Related Skills:**
- `minimal-fix-planner` - Plans the fix approach before this skill generates the implementation
- `bug-fix-documenter` - Documents the fix generated by this skill
- `safe-change-boundary-detector` - Verifies the fix stays within safe change boundaries
- `hotfix-validator` - Validates this fix meets hotfix safety criteria
