# Test Scenario Generator Skill

## Purpose
Creates comprehensive test scenarios and test cases based on acceptance criteria and edge cases.

## Input Requirements
```yaml
feature:
  description: <feature>
  acceptance_criteria: [<criteria>]
  edge_cases: [<edge cases>]
  user_roles: [<roles>]
  systems: [<involved systems>]
```

## Processing Steps

1. **Map Criteria to Test Scenarios**
   - One or more scenarios per criterion
   - Include all paths through feature

2. **Create Test Cases**
   - Preconditions
   - Steps
   - Expected results
   - Post-conditions

3. **Plan Test Types**
   - Manual tests
   - Automated tests
   - Integration tests
   - Load tests if needed

4. **Identify Test Data**
   - What data needed
   - Valid vs invalid data
   - Boundary values

## Output Format

```yaml
test_scenarios:
  
  test_scenario_list:
    - scenario_id: "TS-001"
      scenario_name: <test scenario name>
      criterion_covered: <acceptance criterion>
      
      preconditions:
        - <precondition>
        - <precondition>
      
      test_steps:
        - step_1: <action>
        - step_2: <action>
        - step_3: <action>
      
      expected_results:
        - <expected result>
        - <expected result>
      
      test_type: <manual|automated|both>
      automation_feasibility: <easy|moderate|difficult>
      test_data_needed:
        - <data type>
        - <data type>
      
      priority: <critical|high|medium|low>
    
    - scenario_id: "TS-002"
      ...
  
  test_data_matrix:
    valid_data:
      - <example>
      - <example>
    
    invalid_data:
      - <example>
      - <example>
    
    boundary_values:
      - <example>
      - <example>
  
  regression_test_scenarios: [<scenarios to prevent regression>]
  
  test_coverage:
    total_scenarios: <count>
    happy_path: <count>
    edge_case: <count>
    error_handling: <count>
    coverage_percentage: <estimate>
  
  manual_vs_automated:
    recommended_manual: [<scenarios>]
    recommended_automated: [<scenarios>]
    recommended_both: [<scenarios>]
  
  test_execution_plan:
    phase_1: [<scenarios to test first>]
    phase_2: [<scenarios>]
    phase_3: [<scenarios>]
```

## Examples

### Example 1: Export Feature Test Scenarios
```yaml
Test Scenario 1: Basic Export
  Criterion: "Export button visible and functional"
  
  Preconditions:
    - Customer list page open
    - At least 5 customers in system
  
  Test Steps:
    1. Navigate to Customer List page
    2. Click Export button
    3. Wait for download
  
  Expected Results:
    - Export button visible and clickable
    - Excel file downloads
    - File named correctly (CustomerExport_[date].xlsx)
    - File opens in Excel without errors
  
  Test Type: Manual (UI interaction)
  
Test Scenario 2: Export with Filters
  Criterion: "Export respects applied filters"
  
  Preconditions:
    - Customer list with 100+ customers
    - Status filter: Active
  
  Test Steps:
    1. Apply Status = 'Active' filter
    2. Verify 30 customers shown
    3. Click Export
    4. Open downloaded file
    5. Count rows
  
  Expected Results:
    - Export contains exactly 30 customers
    - All customers have Status = Active
  
  Test Type: Automated (data verification)

Test Scenario 3: Large Export Warning
  Criterion: "Warn user when exporting >10,000 rows"
  
  Preconditions:
    - System has 15,000 customers
  
  Test Steps:
    1. Go to Customer List (no filters)
    2. Click Export
    3. Observe warning
  
  Expected Results:
    - Warning shown: "This export contains 15,000 records"
    - User can confirm or cancel
    - If confirm, export proceeds
    - If cancel, no export
  
  Test Type: Manual + Automated
  
Test Scenario 4: Export with No Results
  Criterion: "Handle empty result set gracefully"
  
  Preconditions:
    - Filter applied: Status = 'Deleted'
    - No deleted customers exist
  
  Test Steps:
    1. Apply filter
    2. Verify 'No results' message
    3. Try to export
  
  Expected Results:
    - Message shown: "No records to export"
    - Export button disabled or greyed
    - No file downloads
  
  Test Type: Manual
```

### Example 2: Form Validation Test Scenarios
```yaml
Test Scenario 1: Valid Form Submission
  Preconditions:
    - Customer form open
    - All required fields visible
  
  Test Steps:
    1. Fill Name: "John Smith"
    2. Fill Email: "john@example.com"
    3. Fill Phone: "(555) 123-4567"
    4. Click Save
  
  Expected Results:
    - Form submits successfully
    - Customer record created
    - Confirmation message shown
  
  Test Type: Automated

Test Scenario 2: Invalid Email Format
  Test Steps:
    1. Fill Name: "John Smith"
    2. Fill Email: "not-an-email"
    3. Click Save
  
  Expected Results:
    - Form not submitted
    - Error message: "Invalid email format"
    - Email field highlighted
    - Other data preserved
  
  Test Type: Automated

Test Scenario 3: Duplicate Email
  Preconditions:
    - Customer exists with john@example.com
  
  Test Steps:
    1. Create new customer with same email
    2. Click Save
  
  Expected Results:
    - Form not submitted
    - Error message: "Email already exists"
    - Data preserved for retry
  
  Test Type: Automated

Test Scenario 4: Optional Phone Field
  Test Steps:
    1. Fill Name, Email
    2. Leave Phone empty
    3. Click Save
  
  Expected Results:
    - Form submits
    - Customer saved with empty phone
    - No error message
  
  Test Type: Automated
```

## Test Data Template

```yaml
valid_test_data:
  email:
    - "user@example.com"
    - "first.last@company.co.uk"
    - "user+tag@example.com"

invalid_test_data:
  email:
    - "not-an-email"
    - "user@"
    - "@example.com"
    - "user space@example.com"

boundary_values:
  customer_count:
    - 0 (empty list)
    - 1 (single item)
    - 9,999 (just below limit)
    - 10,000 (at limit)
    - 10,001 (just over limit)
```

## Test Type Definitions

**Manual Tests:**
- UI interactions
- User experience
- Visual verification
- Complex workflows

**Automated Tests:**
- Data validation
- Calculations
- Database operations
- Performance thresholds

**Integration Tests:**
- Multiple components
- System interactions
- External service calls

**Load Tests:**
- Performance under load
- Concurrent operations
- Resource limits

## Coverage Goals

- Happy path: 100%
- Edge cases: 80%+
- Error handling: 80%+
- Overall: 90%+ criterion coverage

## Related Skills
- `acceptance-criteria-expander` - Defines criteria to test
- `edge-case-detector` - Identifies edge cases to test
- `webforms-regression-analyzer` - For regression testing
