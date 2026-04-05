---
name: minimal-diff-planner
description: Plans the smallest possible code change to implement requirements while maintaining legacy system safety and avoiding refactoring.
---

# Minimal Diff Planner

## Quick Example

**Input:** Add Excel export to customer list
**Output:** 2 files, 40 lines total, follows Print button pattern → LOW risk
**Time:** 4 minutes

---

## Purpose
Plans the smallest possible code change to implement requirements while maintaining legacy system safety and avoiding refactoring.

## Philosophy

> "The best code is no code. The second best is boring code that works."

**Minimal diff means:**
- Fewest files changed
- Fewest lines changed
- Maximum pattern reuse
- Zero refactoring
- No "improvements"

## Input

```yaml
requirement: <what needs to be done>
affected_components: [<components>]
current_patterns: [<existing patterns to follow>]
constraints: [<limitations>]
```

## Output

```yaml
minimal_diff_plan:
  files_to_modify:
    - file: <path>
      reason: <why>
      lines: <estimate>
      changes: [<add|modify|delete>]

  pattern_to_follow:
    reference: <where to copy from>
    pattern_name: <name>
    justification: <why this pattern>

  avoided_changes:
    - file: <path>
      reason_avoided: <why not changing>

  refactoring_resisted:
    - temptation: <what we could do>
      why_resisted: <why we won't>

  total_impact:
    files: <count>
    lines_added: <count>
    lines_modified: <count>
    lines_deleted: <count>
    total: <sum>

  risk_assessment:
    blast_radius: tiny|small|medium|large
    rollback_complexity: trivial|simple|moderate|complex
    testing_scope: minimal|moderate|extensive

  confidence: HIGH|MEDIUM|LOW
```

## DO:
✅ Find and follow existing patterns
✅ Minimize files changed
✅ Minimize lines changed
✅ Reuse existing code/methods
✅ Follow established conventions
✅ Resist refactoring temptation
✅ Resist "improvement" temptation

## DON'T:
❌ Refactor existing code
❌ Create new patterns
❌ Add "improvements"
❌ Optimize unnecessarily
❌ Create new base classes
❌ Break existing conventions
❌ Change more than necessary

## Decision Rules

**Change a file if:** directly implements requirement, no way to avoid it, follows existing pattern.
**Don't change if:** can accomplish goal without it, would require refactoring, breaks existing pattern.
**Add new code if:** no existing code does this, copying existing pattern.
**Don't add if:** existing code can be reused, would duplicate logic.
**Never refactor unless:** code is truly broken AND requirement cannot be met without it.

## Common Temptations to Resist

❌ **"While we're here..."** - NO
❌ **"This should be cleaned up"** - NO
❌ **"This could be more efficient"** - Only if required
❌ **"We should use async here"** - Not in scope
❌ **"Let's extract this to a service"** - No new abstractions

## Red Flags

- **>100 lines changed:** Verify still minimal — not refactoring?
- **>5 files changed:** All necessary? Should be multiple changes?
- **New patterns:** Why not existing? Risk understood?

## Example 1: Add Export Button

**Input:**
```yaml
requirement: "Add Excel export to Customer List page"
affected_components: ["CustomerList.aspx"]
current_patterns: ["Print button on Invoice page"]
```

**Output:**
```yaml
files_to_modify:
  - file: CustomerList.aspx
    reason: "Add export button to toolbar"
    lines: 8
    changes: ["Add button markup"]

  - file: CustomerList.aspx.cs
    reason: "Implement export logic"
    lines: 32
    changes: ["Add button click handler", "Add Excel generation"]

pattern_to_follow:
  reference: "InvoiceList.aspx - Print button"
  pattern_name: "Toolbar button with PostBack"
  justification: "Established pattern for page actions"

avoided_changes:
  - file: CustomerRepository.cs
    reason_avoided: "Reuse existing GetFilteredCustomers()"

  - file: ExcelHelper.cs
    reason_avoided: "Inline code simpler than new helper"

refactoring_resisted:
  - temptation: "Extract Excel creation to separate service"
    why_resisted: "Not in scope, adds complexity, single use case"

  - temptation: "Make export async/await"
    why_resisted: "Current sync pattern works, not in scope"

total_impact:
  files: 2
  lines_added: 40
  lines_modified: 0
  lines_deleted: 0
  total: 40

risk_assessment:
  blast_radius: small
  rollback_complexity: simple
  testing_scope: minimal

confidence: HIGH
```

---

**Related Skills:**
- `safe-change-boundary-detector` - Validates safe change points
- `webforms-lifecycle-analyzer` - Checks lifecycle compliance
- `rollback-plan-generator` - Plans simple rollback
