---
skill: minimal-diff-planner
version: 2.0.0
category: planning
complexity: high
estimated_time: 3-5 minutes
priority: critical
last_updated: 2026-01-18
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

### When to Change a File

**Change if:**
- ✅ Directly implements requirement
- ✅ No way to avoid it
- ✅ Follows existing pattern

**Don't change if:**
- ❌ Can accomplish goal without it
- ❌ Would require refactoring
- ❌ Breaks existing pattern

### When to Add New Code

**Add if:**
- ✅ No existing code does this
- ✅ Copying existing pattern
- ✅ Simpler than reusing

**Don't add if:**
- ❌ Existing code can be reused
- ❌ Would duplicate logic
- ❌ Requires new patterns

### When to Refactor

**NEVER refactor unless:**
- Code is truly broken (not just "not ideal")
- Requirement cannot be met without it
- Risk is understood and acceptable
- Documented as explicit decision

## Common Temptations to Resist

❌ **"While we're here..."** - NO
❌ **"This should be cleaned up"** - NO
❌ **"This could be more efficient"** - Only if required
❌ **"We should use async here"** - Not in scope
❌ **"Let's extract this to a service"** - No new abstractions

## Red Flags

### High Line Count
- **Warning:** >100 lines changed
- **Questions:** Is this really minimal? Can we break into smaller changes? Are we refactoring?

### Many Files
- **Warning:** >5 files changed
- **Questions:** Do all need changes? Touching too much? Should be multiple changes?

### New Patterns
- **Warning:** Introducing new pattern
- **Questions:** Why not existing pattern? Is new pattern justified? What's the risk?

### Breaking Changes
- **Warning:** Public API or contract changes
- **Questions:** Can we avoid this? What's alternative? Documented and approved?

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

## Example 2: Fix Bug

**Input:**
```yaml
requirement: "Fix NullReferenceException when customer has no email"
affected_components: ["CustomerNotificationService.cs"]
```

**Output:**
```yaml
files_to_modify:
  - file: CustomerNotificationService.cs
    reason: "Add null check before email send"
    lines: 5
    changes: ["Add if check", "Add log statement", "Add return"]

pattern_to_follow:
  reference: "OrderNotificationService.cs - email null check"
  pattern_name: "Defensive null check with logging"
  justification: "Established pattern for missing email"

avoided_changes:
  - file: CustomerRepository.cs
    reason_avoided: "Data layer fine - UI validation exists, edge case"

  - file: EmailService.cs
    reason_avoided: "Service expects valid emails - caller validates"

refactoring_resisted:
  - temptation: "Create EmailValidator class"
    why_resisted: "Overkill for single check"

  - temptation: "Add email validation to Customer entity"
    why_resisted: "Not in scope, risky change"

total_impact:
  files: 1
  lines_added: 5
  lines_modified: 0
  lines_deleted: 0
  total: 5

risk_assessment:
  blast_radius: tiny
  rollback_complexity: trivial
  testing_scope: minimal

confidence: HIGH
```

## Quality Checks

Before returning plan:
- [ ] Cannot reduce file count further
- [ ] Cannot reduce line count further
- [ ] Following existing patterns
- [ ] No refactoring included
- [ ] No "improvements" included
- [ ] Rollback is simple
- [ ] Risk is minimal
- [ ] Testing scope is clear

---

**Related Skills:**
- `safe-change-boundary-detector` - Validates safe change points
- `webforms-lifecycle-analyzer` - Checks lifecycle compliance
- `rollback-plan-generator` - Plans simple rollback
