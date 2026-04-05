---
name: story-analyzer
description: Examines current story state to identify gaps, assumptions, and missing information that need clarification
---

## Purpose
Examines current story state to identify gaps, assumptions, and missing information that need clarification.

## Input Requirements
```yaml
story:
  title: <story title>
  description: <current description>
  acceptance_criteria: [<existing criteria if any>]
  history: [<previous interactions>]
```

## Processing Steps

1. **Analyze What Exists**
   - Review current description
   - Note existing acceptance criteria
   - Identify what's clear

2. **Identify Unclear Aspects**
   - What assumptions are implicit?
   - What terminology is vague?
   - What details are missing?

3. **List Missing Information**
   - Acceptance criteria gaps
   - Business context gaps
   - Technical context gaps
   - Scope gaps

4. **Document Current State**
   - What we have
   - What's unclear
   - What's missing

## Output Format

```yaml
story_analysis:
  
  current_state:
    title: <story title>
    description_clarity: <clear|mostly_clear|vague|very_vague>
    acceptance_criteria_completeness: <complete|mostly_complete|incomplete|missing>
    scope_clarity: <clear|mostly_clear|unclear>
  
  what_exists:
    clearly_defined:
      - <item>
      - <item>
    
    adequately_described:
      - <item>
      - <item>
  
  what_is_unclear:
    unclear_aspects:
      - aspect: <what's unclear>
        current_state: <what we have>
        needed: <what's needed>
      
      - aspect: <another unclear thing>
        ...
    
    vague_terminology:
      - term: <vague word>
        examples: <where it's used>
        clarification_needed: <what does it mean>
    
    implicit_assumptions:
      - assumption: <what we're assuming>
        rationale: <why assumed>
        needs_validation: <yes|no>
  
  what_is_missing:
    critical_gaps:
      - <missing information>
      - <missing information>
    
    important_gaps:
      - <missing information>
      - <missing information>
    
    optional_but_helpful:
      - <information>
      - <information>
  
  completeness_assessment:
    percentage_complete: <estimate>
    readiness: <ready|mostly_ready|needs_refinement|not_ready>
    effort_to_complete: <low|medium|high>
    blocking_issues: [<list if any>]
  
  recommendations:
    next_steps:
      1: <clarification needed>
      2: <clarification needed>
    
    suggested_questions:
      - <question to ask>
      - <question to ask>
    
    action: <proceed_with_current|refine_first|spike|request_clarification>
```

## Examples

### Example 1: Well-Defined Story
```yaml
Input:
  title: "Add export to Excel button on customer list"
  description: "Sales team needs to export customer data for reporting"
  acceptance_criteria:
    - "Export button visible"
    - "Exports selected columns"
    - "File format: .xlsx"

Output:
  what_exists:
    clearly_defined:
      - "Core feature (export to Excel)"
      - "User role (sales team)"
      - "Business context (for reporting)"
      - "File format requirement"
      - "Button visibility"
  
  what_is_unclear:
    unclear_aspects:
      - aspect: "Selected columns"
        current_state: "Mentioned but not specified which"
        needed: "List specific columns to include"
      
      - aspect: "Number of rows"
        current_state: "Not mentioned"
        needed: "Maximum rows, pagination?"
  
  what_is_missing:
    critical_gaps:
      - "Which columns to include"
    
    important_gaps:
      - "Error handling for large exports"
      - "Performance requirements"
  
  completeness_assessment:
    percentage_complete: 75
    readiness: mostly_ready
    effort_to_complete: low
  
  recommended_action: "Refine with clarification on columns and limits"
```

## Related Skills
- `requirement-extractor` - Clarifies investigation need
- `spike-findings-recorder` - Documents investigation results
- `webforms-lifecycle-analyzer` - For WebForms investigations
    - assumption: "Email field is optional"
      current_state: "Not stated, but implied"
      needs_validation: yes
    
    - assumption: "Email must be unique"
      current_state: "Not stated"
      needs_validation: yes
    
    - assumption: "Email format validation needed"
      current_state: "Standard practice, not explicit"
      needs_validation: yes
    
    - assumption: "Verification email sent"
      current_state: "Not mentioned, but possible expectation"
      needs_validation: yes
  
  questions_to_ask:
    - "Is email required or optional?"
    - "Must email be unique across all customers?"
    - "Should we send verification email?"
    - "What if customer has multiple emails?"
    - "Can customer change email after creation?"
  
  recommended_action: "Validate assumptions before refining acceptance criteria"
```

## Related Skills
- `requirement-extractor` - Extracts detailed requirements
- `acceptance-criteria-generator` - Creates specific criteria
- `edge-case-detector` - Identifies missing scenarios
