# Minimal Diff Planner

## Purpose
Plans the smallest possible code change to implement a requirement while maintaining legacy system safety.

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
affected_components: [<list of components>]
current_patterns: [<existing code patterns to follow>]
constraints: [<limitations>]
```

## Planning Process

### 1. Identify Existing Patterns

**Find similar implementations:**
- How was this done before?
- What pattern was used?
- Which files were involved?

**Examples:**
```yaml
pattern: "Adding button to page"
existing: "Print button on Invoice page"
files: 
  - Page.aspx (markup)
  - Page.aspx.cs (code-behind)
lines: ~15
```

### 2. Determine Necessary Files

**Only change files that MUST change:**

**✅ Necessary Changes:**
- Page with new UI element
- Code-behind for logic
- Repository if data access changes
- Config if settings needed

**❌ Unnecessary Changes:**
- Helper utilities (unless truly needed)
- Base classes
- Other pages
- Unrelated code

### 3. Calculate Line Impact

**Estimate lines changed per file:**

```yaml
file: CustomerList.aspx
  added: 8 lines (button markup)
  modified: 0
  deleted: 0

file: CustomerList.aspx.cs
  added: 25 lines (export method)
  modified: 0
  deleted: 0

total_impact: 33 lines across 2 files
```

### 4. Avoid Temptation

**Common "while we're here" temptations:**

❌ **Refactoring** - "This method should be broken up"  
✅ **Resist** - Not in scope

❌ **Cleanup** - "Let's fix this spacing"  
✅ **Resist** - Not in scope

❌ **Optimization** - "This could be more efficient"  
✅ **Resist** - Not unless required

❌ **Modernization** - "We should use async here"  
✅ **Resist** - Not in scope

### 5. Reuse Existing Code

**Prefer:**
- Copy-paste existing patterns
- Call existing methods
- Use existing helpers
- Follow established conventions

**Avoid:**
- Creating new base classes
- New design patterns
- New utilities
- Breaking conventions

## Output

```yaml
minimal_diff_plan:
  files_to_modify:
    - file: <path>
      reason: <why this file>
      estimated_lines: <count>
      changes:
        - type: <add|modify|delete>
          location: <where in file>
          description: <what changes>
  
  pattern_to_follow:
    reference_implementation: <where to copy from>
    pattern_name: <name of pattern>
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
    blast_radius: <small|medium|large>
    rollback_complexity: <simple|moderate|complex>
    testing_scope: <minimal|moderate|extensive>

confidence: <high|medium|low>
```

## Examples

### Example 1: Add Export Button

**Requirement:** Add Excel export to Customer List page

**Plan:**
```yaml
minimal_diff_plan:
  files_to_modify:
    - file: CustomerList.aspx
      reason: "Add export button to toolbar"
      estimated_lines: 8
      changes:
        - type: add
          location: "After search button in toolbar"
          description: |
            <asp:Button ID="btnExport" runat="server" 
                Text="Export to Excel" OnClick="btnExport_Click" />
    
    - file: CustomerList.aspx.cs
      reason: "Implement export logic"
      estimated_lines: 32
      changes:
        - type: add
          location: "After existing button handlers"
          description: |
            protected void btnExport_Click(object sender, EventArgs e)
            {
                // Get current grid data
                var customers = GetFilteredCustomers();
                
                // Create Excel using EPPlus (existing library)
                var excel = CreateExcelFromCustomers(customers);
                
                // Download
                Response.Clear();
                Response.ContentType = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet";
                Response.AddHeader("content-disposition", "attachment; filename=Customers.xlsx");
                Response.BinaryWrite(excel.GetAsByteArray());
                Response.End();
            }
  
  pattern_to_follow:
    reference_implementation: "InvoiceList.aspx - Print button"
    pattern_name: "Toolbar button with PostBack"
    justification: "Established pattern for page actions"
  
  avoided_changes:
    - file: CustomerRepository.cs
      reason_avoided: "No data access changes needed - reuse existing GetFilteredCustomers()"
    - file: ExcelHelper.cs
      reason_avoided: "No generic helper needed - inline code is simpler"
  
  refactoring_resisted:
    - temptation: "Extract Excel creation to separate service"
      why_resisted: "Not in scope, adds complexity, single use case"
    - temptation: "Make export async/await"
      why_resisted: "Not in scope, current sync pattern works"
  
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

confidence: high
```

### Example 2: Fix Bug

**Requirement:** Fix NullReferenceException when customer has no email

**Plan:**
```yaml
minimal_diff_plan:
  files_to_modify:
    - file: CustomerNotificationService.cs
      reason: "Add null check before email send"
      estimated_lines: 3
      changes:
        - type: add
          location: "Line 45, before email send"
          description: |
            if (string.IsNullOrEmpty(customer.Email))
            {
                _logger.Warning($"Customer {customer.Id} has no email");
                return;
            }
  
  pattern_to_follow:
    reference_implementation: "OrderNotificationService.cs - email null check"
    pattern_name: "Defensive null check with logging"
    justification: "Established pattern for missing email handling"
  
  avoided_changes:
    - file: CustomerRepository.cs
      reason_avoided: "Data layer is fine - UI validation exists, this is edge case"
    - file: EmailService.cs
      reason_avoided: "Service should accept valid emails - caller responsible for validation"
  
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

confidence: high
```

### Example 3: Performance Fix

**Requirement:** Fix slow customer search (N+1 query)

**Plan:**
```yaml
minimal_diff_plan:
  files_to_modify:
    - file: CustomerRepository.cs
      reason: "Add Include for eager loading"
      estimated_lines: 2
      changes:
        - type: modify
          location: "GetActiveCustomers method, line 67"
          description: |
            OLD:
            return _context.Customers
                .Where(c => c.Status == "Active")
                .ToList();
            
            NEW:
            return _context.Customers
                .Include(c => c.Orders)
                .Where(c => c.Status == "Active")
                .ToList();
  
  pattern_to_follow:
    reference_implementation: "OrderRepository.cs - Include pattern"
    pattern_name: "Eager loading with Include"
    justification: "Standard EF pattern for related data"
  
  avoided_changes:
    - file: CustomerList.aspx.cs
      reason_avoided: "Display logic unchanged"
    - file: Customer.cs
      reason_avoided: "Entity unchanged"
  
  refactoring_resisted:
    - temptation: "Switch to stored procedure"
      why_resisted: "Bigger change, LINQ Include sufficient"
    - temptation: "Add caching layer"
      why_resisted: "Not in scope, Include fixes the N+1"
    - temptation: "Rewrite query in fluent syntax"
      why_resisted: "Works as-is with Include"
  
  total_impact:
    files: 1
    lines_added: 1
    lines_modified: 1
    lines_deleted: 0
    total: 2
  
  risk_assessment:
    blast_radius: tiny
    rollback_complexity: trivial
    testing_scope: minimal

confidence: high
```

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

**Add new code if:**
- ✅ No existing code does this
- ✅ Copying existing pattern
- ✅ Simpler than reusing

**Don't add if:**
- ❌ Existing code can be reused
- ❌ Would duplicate logic
- ❌ Requires new patterns

### When to Refactor

**Never refactor unless:**
- Code is truly broken (not just "not ideal")
- Requirement cannot be met without it
- Risk is understood and acceptable
- Documented as explicit decision

## Red Flags

### High Line Count
```yaml
warning: "Over 100 lines changed"
questions:
  - "Is this really minimal?"
  - "Can we break into smaller changes?"
  - "Are we refactoring?"
```

### Many Files
```yaml
warning: "More than 5 files changed"
questions:
  - "Do all these files need changes?"
  - "Are we touching too much?"
  - "Should this be multiple changes?"
```

### New Patterns
```yaml
warning: "Introducing new pattern"
questions:
  - "Why not use existing pattern?"
  - "Is new pattern justified?"
  - "What's the risk?"
```

### Breaking Changes
```yaml
warning: "Public API or contract changes"
questions:
  - "Can we avoid this?"
  - "What's the alternative?"
  - "Is this documented and approved?"
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

## Usage

```
SKILL: minimal-diff-planner

INPUT:
  requirement: "Add search filter for customer status"
  affected_components: ["CustomerList.aspx"]
  current_patterns: ["Existing filters use dropdown in toolbar"]
  constraints: ["Must maintain existing filter behavior"]

OUTPUT:
  minimal_diff_plan:
    files_to_modify: [2 files, 35 lines total]
    pattern_to_follow: "Copy City filter dropdown pattern"
    refactoring_resisted: ["Don't extract filter logic to service"]
    blast_radius: small
```

## Confidence Levels

**High:** Clear minimal path, existing pattern, low risk  
**Medium:** Some alternatives possible, moderate complexity  
**Low:** Multiple approaches, unclear minimal path
