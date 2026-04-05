---
name: acceptance-criteria-generator
description: Transforms requirements into specific, testable acceptance criteria in Gherkin format.
---

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

- **Given** → initial state/precondition
- **When** → action being tested
- **Then** → expected outcome
- **And** → additional conditions or assertions

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
    Given: Customer list with 10 customers
    When: User clicks Export button
    Then: Excel file downloads with 10 rows, Name/Email/Status columns
  
  Criterion 3 - Filter Respected:
    Given: Filter Applied (Status = 'Active')
    When: User clicks Export
    Then: File contains only active customers
  
  Criterion 4 - Error Handling:
    Given: Export in progress
    When: Server timeout
    Then: Error message shown; no partial file downloaded
```

## Related Skills
- `requirement-extractor` - Identifies requirements
- `edge-case-detector` - Finds edge cases
- `story-analyzer` - Analyzes current state
