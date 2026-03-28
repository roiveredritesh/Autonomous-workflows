# Edge Case Detector Skill

## Purpose
Identifies edge cases, boundary conditions, and error scenarios that must be handled in acceptance criteria and implementation.

## Input Requirements
```yaml
feature:
  description: <feature description>
  requirements: [<requirements>]
  data_involved: [<types of data>]
  user_roles: [<roles that interact>]
  systems_involved: [<systems>]
```

## Processing Steps

1. **Boundary Analysis**
   - Empty values
   - Null values
   - Maximum values
   - Minimum values

2. **State Analysis**
   - Initial state
   - State transitions
   - Invalid states

3. **Concurrency Analysis**
   - Simultaneous operations
   - Race conditions
   - Timing issues

4. **Permission Analysis**
   - No access
   - Partial access
   - Full access

5. **Data Quality Analysis**
   - Invalid formats
   - Special characters
   - Malformed data

## Output Format

```yaml
edge_case_analysis:
  
  boundary_conditions:
    empty_values:
      - scenario: <empty condition>
        handling: <what should happen>
        risk: <low|medium|high>
    
    null_values:
      - scenario: <null condition>
        handling: <what should happen>
        risk: <low|medium|high>
    
    maximum_values:
      - scenario: <max condition>
        handling: <what should happen>
        risk: <low|medium|high>
    
    minimum_values:
      - scenario: <min condition>
        handling: <what should happen>
        risk: <low|medium|high>
  
  state_edge_cases:
    - edge_case: <specific state scenario>
      description: <what's special about it>
      handling: <required behavior>
      acceptance_criterion: <testable criterion>
  
  concurrency_scenarios:
    - scenario: <concurrent operation>
      risk: <low|medium|high>
      handling: <how to prevent/handle>
      test_approach: <how to test>
  
  permission_scenarios:
    - scenario: <permission case>
      user_type: <user without this permission>
      expected_behavior: <what should happen>
      error_message: <if applicable>
  
  data_quality_edge_cases:
    - case: <invalid data scenario>
      example: <concrete example>
      handling: <validation or error>
      user_message: <what user sees>
  
  error_scenarios:
    - error: <possible error>
      trigger: <what causes it>
      handling: <how to handle>
      user_experience: <what user sees>
  
  edge_cases_summary:
    total_edge_cases_identified: <count>
    critical_edge_cases: [<must handle>]
    important_edge_cases: [<should handle>]
    nice_to_have: [<could handle>]
    acceptance_criteria_added: <count>
```

## Edge Case Categories

### Boundary Conditions

**Empty Values:**
- Empty list/collection
- Empty string
- Empty file
- No data returned

**Null Values:**
- Null object reference
- Missing optional field
- Uninitialized variable

**Maximum Values:**
- Maximum array size
- Maximum string length
- Maximum number value
- Maximum concurrent users

**Minimum Values:**
- Zero items
- Single item (not multiple)
- Minimum acceptable value

### State Edge Cases

**Initial State:**
- First time using feature
- No previous data
- Fresh installation

**State Transitions:**
- Valid transitions
- Invalid transitions
- Partial transitions

**Special States:**
- Deleted but cached
- Archived but active
- Locked or read-only
- In-progress operations

### Concurrency Scenarios

**Simultaneous Operations:**
- Multiple users same data
- Rapid-fire requests
- Overlapping operations
- Race conditions

**Timing Issues:**
- Operation timeout
- Slow network
- Service delays
- Batch operations

### Permission Scenarios

**No Permission:**
- User cannot access
- Error message needed
- Graceful failure

**Partial Permission:**
- Can view, not edit
- Limited subset visible
- Restricted operations

**Permission Changes:**
- Permission revoked mid-operation
- New permission granted
- Role changes

### Data Quality Edge Cases

**Invalid Formats:**
- Wrong data type
- Invalid characters
- Encoding issues
- Special characters

**Constraint Violations:**
- Duplicate values
- Value out of range
- Required field missing
- Referential integrity

## Examples

### Example 1: Export Feature Edge Cases
```yaml
Feature: Export Customer List to Excel

Edge Cases Identified:

Boundary Conditions:
  - empty_result_set:
      scenario: "No customers match filter"
      handling: "Show message 'No records to export'"
      risk: medium
  
  - single_customer:
      scenario: "Filter results in 1 customer"
      handling: "Export works, file has 1 row"
      risk: low
  
  - large_export:
      scenario: "Export 10,000+ customers"
      handling: "Show warning, limit to 10,000 or paginate"
      risk: high

Concurrency:
  - multiple_exports:
      scenario: "Same user exports twice rapidly"
      handling: "Queue requests or prevent double-click"
      risk: medium

Data Quality:
  - special_characters:
      scenario: "Customer name has quotes, commas"
      handling: "Excel escaping handles automatically"
      risk: low
  
  - long_text:
      scenario: "Notes field exceeds Excel cell limit"
      handling: "Truncate with warning"
      risk: medium

Error Scenarios:
  - export_timeout:
      scenario: "Large export takes >30 seconds"
      handling: "Show timeout, suggest filtering"
      error_message: "Export timed out, try narrower filter"
      risk: high
```

### Example 2: Customer Status Update Edge Cases
```yaml
Feature: Update Customer Status

Edge Cases:

State Edge Cases:
  - status_transition_invalid:
      current: "Archived"
      requested: "Active"
      handling: "Prevent transition, show error"
      message: "Cannot reactivate archived customer"
  
  - concurrent_status_change:
      scenario: "Two users change status simultaneously"
      handling: "Last write wins / or show conflict"
      risk: high

Permission Scenarios:
  - user_lacks_permission:
      scenario: "User tries to change status without permission"
      handling: "Show 'Access Denied' error"
      risk: low
  
  - permission_revoked_during_edit:
      scenario: "Permission revoked while form open"
      handling: "Block save, show permission error"
      risk: medium

Data Quality:
  - customer_deleted:
      scenario: "Customer deleted by another user"
      handling: "Show 'Record not found' error"
      risk: medium
```

### Example 3: Form Input Edge Cases
```yaml
Feature: Add Phone Number Field

Edge Cases:

Boundary Conditions:
  - empty_phone:
      scenario: "User leaves phone empty"
      handling: "Allow save (optional field)"
      criterion: "Form saves with empty phone"
  
  - phone_too_long:
      scenario: "User enters 50-character phone"
      handling: "Validate, show error"
      criterion: "Form rejects phone > 20 chars"

Data Quality:
  - invalid_format:
      scenarios:
        - "abc123"
        - "1 2 3 4 5"
        - "+1-555-1234"
      handling: "Validate format, show error"
      message: "Enter phone as (555) 123-4567"
  
  - special_characters:
      scenario: "Phone with symbols: ()- +"
      handling: "Allow standard phone format symbols"
      criterion: "Accepts (555) 123-4567 format"

Permission Scenarios:
  - customer_view_only:
      scenario: "User viewing (not editing) customer"
      handling: "Phone field disabled/read-only"
      criterion: "Phone field not editable in view mode"
```

## Detection Techniques

### Ask the Five Whys
- What if it's empty?
- What if there's no data?
- What if multiple users do this?
- What if the system is slow?
- What if something goes wrong?

### Boundary Analysis
- Empty, null, zero
- Maximum, minimum
- One, many, too many
- Valid, invalid, malformed

### State Analysis
- What states can object be in?
- What transitions are valid?
- What if transition fails?
- What if in unexpected state?

### User Perspective
- What could user do wrong?
- What if user is in hurry?
- What if user has no permission?
- What if user works offline?

## Related Skills
- `acceptance-criteria-generator` - Converts to criteria
- `requirement-extractor` - Identifies requirements
- `test-scenario-generator` - Creates test cases
