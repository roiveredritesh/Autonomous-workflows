---
name: acceptance-criteria-expander
description: Transforms basic or incomplete acceptance criteria into comprehensive, testable specifications.
---

## Purpose
Transforms basic or incomplete acceptance criteria into comprehensive, testable specifications.

## Input
```yaml
story_summary: <brief description>
current_criteria: [<existing criteria if any>]
context: <additional context>
assumptions: [<any assumptions>]
```

## Process

**1. Analyze:** Evaluate if existing criteria are specific, testable, cover happy path, edge cases, and errors.
**2. Format:** Apply Given-When-Then for each criterion.
**3. Cover:** Happy path, alternative paths (different roles/states), edge cases (empty/max/concurrent), error conditions (invalid input, permission denied, timeout).
**4. Validate:** Each criterion must be specific, measurable, and testable (can verify pass/fail).

## Output

```yaml
expanded_criteria:
  happy_path:
    - given: <context>
      when: <action>
      then: <outcome>
      and: <additional outcome>
  
  alternative_paths:
    - given: <alternative context>
      when: <action>
      then: <outcome>
  
  edge_cases:
    - scenario: <description>
      given: <context>
      when: <action>
      then: <outcome>
  
  error_conditions:
    - error: <type>
      given: <context>
      when: <action>
      then: <error handling>
  
  validation_rules:
    - field: <field name>
      rule: <validation rule>
      message: <error message>

confidence: <high|medium|low>
missing_information: [<gaps if any>]
questions_for_clarification: [<if needed>]
```

## Examples

### Example 1: Basic Story

**Input:**
```yaml
story: "Add export to Excel for customer list"
current_criteria:
  - "User can export customer list"
```

**Output:**
```yaml
expanded_criteria:
  happy_path:
    - given: "User is on customer list page with results displayed"
      when: "User clicks 'Export to Excel' button"
      then: "Excel file (.xlsx) downloads to user's computer"
      and: "File contains all visible columns from the list"
      and: "File respects current sort order"
  
  alternative_paths:
    - given: "User has applied filters to customer list"
      when: "User clicks 'Export to Excel'"
      then: "Excel file contains only filtered results"
    
    - given: "User has selected specific customers (checkboxes)"
      when: "User clicks 'Export to Excel'"
      then: "Excel file contains only selected customers"
  
  edge_cases:
    - scenario: "Empty result set"
      given: "Customer list has no results (filter returns nothing)"
      when: "User clicks 'Export to Excel'"
      then: "User sees message 'No data to export'"
      and: "No file is downloaded"
    
    - scenario: "Large result set"
      given: "Customer list has 50,000 results"
      when: "User clicks 'Export to Excel'"
      then: "User sees warning 'Export limited to 10,000 rows'"
      and: "Excel file contains first 10,000 rows"
      and: "User can export next batch if needed"
    
    - scenario: "Export timeout"
      given: "Export takes longer than 30 seconds"
      when: "Processing times out"
      then: "User sees error message 'Export failed - please narrow your search'"
  
  error_conditions:
    - error: "No permission"
      given: "User doesn't have export permission"
      when: "User clicks 'Export to Excel'"
      then: "Export button is disabled or shows permission error"
    
    - error: "Server error"
      given: "Server encounters error during export"
      when: "Export fails"
      then: "User sees 'Export failed - please try again'"
      and: "Error is logged for troubleshooting"
  
  validation_rules:
    - field: "result_count"
      rule: "max 10,000 rows per export"
      message: "Export limited to 10,000 rows"

confidence: high
```

### Example 2: Complex Feature

**Input:**
```yaml
story: "Send email when order status changes"
current_criteria:
  - "Email sent on status change"
```

**Output:**
```yaml
expanded_criteria:
  happy_path:
    - given: "Order exists with status 'Processing' and valid customer email"
      when: "Status is changed to 'Shipped'"
      then: "Email sent to customer email address"
      and: "Email contains order number, tracking link, expected delivery date"
      and: "Email send is logged in audit trail"
  
  alternative_paths:
    - given: "Order status changes from 'Pending' to 'Processing'"
      when: "Status changes"
      then: "Confirmation email sent with order details"
    
    - given: "Order status changes to 'Cancelled'"
      when: "Status changes"
      then: "Cancellation email sent explaining next steps"
  
  edge_cases:
    - scenario: "No email on order"
      given: "Order has no email address"
      when: "Status changes to 'Shipped'"
      then: "Status updates normally"
      and: "Warning logged that email not sent"
    
    - scenario: "Invalid email"
      given: "Order has malformed email address"
      when: "Status changes"
      then: "Status updates normally; email validation error logged"
  
  error_conditions:
    - error: "Email service unavailable"
      given: "Email service is down"
      when: "Status change triggers email"
      then: "Status updates successfully"
      and: "Email queued for retry (3 attempts)"
      and: "Failure logged after 3 attempts"
    
    - error: "Email send fails"
      given: "Email send returns error"
      when: "Send attempt fails"
      then: "Error logged with order ID and email address"
      and: "Status update not rolled back"
  
  validation_rules:
    - field: "email_address"
      rule: "valid email format"
      message: "Invalid email format"
    
    - field: "status_change"
      rule: "only specific statuses trigger email"
      message: "Status change does not trigger notification"

confidence: high
```

## Related Skills
- `requirement-extractor` - Identifies requirements
- `acceptance-criteria-generator` - Creates specific criteria
- `edge-case-detector` - Identifies missing scenarios
