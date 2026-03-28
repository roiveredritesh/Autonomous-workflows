# Acceptance Criteria Generator Skill

## Purpose
Transforms requirements into specific, testable acceptance criteria in Gherkin format.

## Input Requirements
```yaml
requirements:
  story_title: <title>
  core_requirement: <what must work>
  functional_requirements: [<list>]
  edge_cases: [<known edge cases>]
  constraints: [<constraints>]
```

## Processing Steps

1. **Map to Happy Path**
   - Primary success scenario
   - Normal expected flow
   - Typical user actions

2. **Cover Edge Cases**
   - Boundary conditions
   - Error scenarios
   - Special cases

3. **Format as Gherkin**
   - Given [context]
   - When [action]
   - Then [outcome]

4. **Ensure Testability**
   - Each criterion is verifiable
   - No ambiguous language
   - Clear success/failure

## Output Format

```yaml
acceptance_criteria:
  
  happy_path_criteria:
    - criterion_1:
        given: <precondition>
        when: <action>
        then: <expected outcome>
        and: [<additional outcomes>]
        type: happy_path
    
    - criterion_2:
        given: <precondition>
        when: <action>
        then: <expected outcome>
        type: happy_path
  
  edge_case_criteria:
    - edge_case_1:
        given: <special condition>
        when: <action>
        then: <expected behavior>
        type: edge_case
  
  error_handling_criteria:
    - error_1:
        given: <error condition>
        when: <trigger>
        then: <error handling>
        type: error_condition
  
  criteria_summary:
    total_criteria: <count>
    happy_path: <count>
    edge_cases: <count>
    error_handling: <count>
    coverage_assessment: <comprehensive|good|adequate|incomplete>
  
  testability_check:
    all_criteria_testable: <yes|no>
    specific_enough: <yes|no>
    measurable: <yes|no>
    clear_success: <yes|no>
```

## Gherkin Format Rules

### Given (Precondition)
- Sets up the initial state
- What must be true for test to start
- Example: "Given a customer exists with status 'Active'"

### When (Action)
- The action being tested
- User interaction or system event
- Example: "When user clicks 'Export' button"

### Then (Outcome)
- Expected result
- System behavior after action
- Example: "Then Excel file downloads"

### And (Additional)
- Add more conditions or outcomes
- Use for multiple assertions
- Example: "And file contains customer data"

## Example Criteria

### Example 1: Simple Feature
```yaml
Feature: Export Customer List to Excel

Acceptance Criteria:
  Criterion 1 - Export Button Visible:
    Given: Customer list page is open
    When: User navigates to customer list
    Then: Export button is visible in toolbar
  
  Criterion 2 - Basic Export:
    Given: Customer list page with 10 customers
    When: User clicks Export button
    Then: Excel file downloads
    And: File contains 10 rows of customer data
    And: File contains Name, Email, Status columns
  
  Criterion 3 - Filter Respected:
    Given: Customer list page with filter Applied (Status = 'Active')
    When: User clicks Export button
    Then: Excel file contains only active customers
  
  Criterion 4 - Large Export Warning:
    Given: Customer list has 500+ customers
    When: User attempts to export all
    Then: System shows warning
    And: User can confirm or cancel
  
  Criterion 5 - Error Handling:
    Given: Export in progress
    When: User closes browser
    Then: Browser requests confirmation
    And: File download stops cleanly
```

### Example 2: Feature with Multiple Scenarios
```yaml
Feature: Customer Status Update Notification

Happy Path:
  Criterion 1 - Status Change Detected:
    Given: Order exists with status "Processing"
    When: Status is updated to "Shipped"
    Then: System detects status change
    And: Sends email notification to customer
  
  Criterion 2 - Email Content:
    Given: Order being shipped
    When: Email sends
    Then: Email includes order number
    And: Email includes tracking information
    And: Email includes expected delivery date

Edge Cases:
  Criterion 3 - No Email on File:
    Given: Order with no customer email
    When: Status updated
    Then: Email not sent
    And: Warning logged
  
  Criterion 4 - Multiple Status Changes:
    Given: Order in Processing
    When: Status changed twice in 1 minute
    Then: Only latest status triggers email

Error Handling:
  Criterion 5 - Email Service Down:
    Given: Email service is unavailable
    When: Status update attempted
    Then: Status updates successfully
    And: Email send scheduled for retry
    And: Status change not blocked
```

### Example 3: Data Validation
```yaml
Feature: Add Phone Number Field

Criterion 1 - Phone Field Visible:
  Given: Customer form open
  When: User loads form
  Then: Phone number field visible
  And: Field label is "Phone Number"

Criterion 2 - Valid Phone Input:
  Given: Phone field visible
  When: User enters valid phone "(555) 123-4567"
  Then: Form saves successfully
  And: Phone number stored in database

Criterion 3 - Invalid Phone Format:
  Given: Phone field visible
  When: User enters "abc123"
  Then: Validation error shown
  And: Error message: "Invalid phone format"
  And: Form not submitted

Criterion 4 - Empty Phone Allowed:
  Given: Phone field visible
  When: User leaves phone empty
  Then: Form saves successfully
  And: Phone field marked as optional
```

## Testability Assessment

### Good Criteria Characteristics
- ✅ Specific: "Export includes Name, Email, Status"
- ✅ Measurable: "Page loads in <2 seconds"
- ✅ Testable: Can write automated test
- ✅ Independent: Doesn't depend on other criteria
- ✅ Clear: No ambiguous language

### Bad Criteria Examples
- ❌ Vague: "System works well"
- ❌ Non-measurable: "Page loads quickly"
- ❌ Non-testable: "User is happy"
- ❌ Dependent: "System is fast after optimization"
- ❌ Unclear: "Handles edge cases"

## Coverage Framework

### Happy Path (Main Scenario)
- Normal use case
- Typical user interaction
- Expected flow

### Edge Cases (Boundary Conditions)
- Empty/null values
- Maximum/minimum values
- Concurrent operations
- Special states

### Error Handling
- Validation failures
- Service unavailability
- Network issues
- Permission denials

### Non-Functional
- Performance
- Security
- Accessibility
- Usability

## Related Skills
- `requirement-extractor` - Identifies requirements
- `edge-case-detector` - Finds edge cases
- `story-analyzer` - Analyzes current state
