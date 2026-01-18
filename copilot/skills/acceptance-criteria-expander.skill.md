# Acceptance Criteria Expander

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

### 1. Analyze Current Criteria

Evaluate what exists:
- Are criteria specific and testable?
- Do they cover happy path?
- Are edge cases included?
- Are error conditions specified?

### 2. Apply Given-When-Then Pattern

Format each criterion:
```gherkin
Given [precondition/context]
When [action/event]
Then [expected outcome]
And [additional outcome if needed]
```

### 3. Cover All Scenarios

Ensure coverage of:

**Happy Path**
- Primary use case
- Expected user flow
- Standard data

**Alternative Paths**
- Valid variations
- Different user types
- Different data states

**Edge Cases**
- Boundary conditions (empty, max, min)
- Special characters
- Concurrent operations
- Missing data

**Error Conditions**
- Invalid input
- Permission denied
- System unavailable
- Timeout scenarios

### 4. Make Criteria Testable

Each criterion must be:
- **Specific:** No ambiguous terms
- **Measurable:** Observable outcome
- **Achievable:** Technically possible
- **Relevant:** Supports story goal
- **Testable:** Can verify pass/fail

### 5. Add Validation Rules

Include:
- Required fields
- Data formats
- Value ranges
- Business rules

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
      and: "No email attempt made"
    
    - scenario: "Invalid email"
      given: "Order has malformed email address"
      when: "Status changes"
      then: "Status updates normally"
      and: "Email validation error logged"
      and: "Admin notified of bad email"
    
    - scenario: "Multiple rapid status changes"
      given: "Order status changes 3 times in 1 minute"
      when: "Processing status changes"
      then: "Only final status email sent"
      and: "No duplicate emails sent"
    
    - scenario: "Bulk status update"
      given: "100 orders updated to 'Shipped' via bulk operation"
      when: "Bulk update processes"
      then: "Emails queued and sent asynchronously"
      and: "System doesn't timeout"
  
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
missing_information:
  - "Which specific status transitions trigger emails?"
  - "Should admin users receive notification copies?"
```

## Quality Checklist

Before returning output, verify:

- [ ] Each criterion is testable
- [ ] Happy path is covered
- [ ] At least 3 edge cases identified
- [ ] Error handling is specified
- [ ] No ambiguous terms (e.g., "better", "improved")
- [ ] Specific measurements where applicable
- [ ] User perspective is maintained
- [ ] Technical constraints considered

## Common Pitfalls to Avoid

❌ **Vague:** "System should perform well"
✅ **Specific:** "Page loads in under 3 seconds for 95% of requests"

❌ **Untestable:** "User interface should be intuitive"
✅ **Testable:** "User can complete checkout in 3 clicks without help"

❌ **Missing edge case:** Only happy path
✅ **Complete:** Happy path + alternatives + edge cases + errors

❌ **Assuming context:** "When they click save"
✅ **Explicit context:** "Given user has filled required fields, when they click save"

## Confidence Levels

**High:** All scenarios covered, no missing information
**Medium:** Core scenarios covered, some edge cases may need clarification
**Low:** Significant gaps or uncertainties remain

## Usage

```
SKILL: acceptance-criteria-expander

INPUT:
  story: "Allow users to save search filters"
  current_criteria: ["User can save filters"]
  context: "Customer search page has 8 different filter options"

OUTPUT:
  [Comprehensive criteria following pattern above]
```
