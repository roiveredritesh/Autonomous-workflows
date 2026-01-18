# JIRA Story Intake Skill

## Purpose
Validates and extracts essential information from JIRA tickets to establish a clear baseline for feature delivery.

## Input Requirements
```yaml
intake:
  jira_ticket_id: <PROJ-1234>  # Can be null if creating new
  story_summary: <title>
  description: <detailed description>
  acceptance_criteria: [<existing criteria if any>]
  created_by: <requester name>
```

## Processing Steps

1. **Ticket Validation**
   - Does ticket exist in JIRA?
   - If not, can it be created?
   - Is ticket in development workflow?

2. **Extract Essential Information**
   - User story summary
   - Business context
   - Existing acceptance criteria
   - Any constraints or dependencies

3. **Identify Missing Information**
   - Is acceptance criteria complete?
   - Is business context clear?
   - Are dependencies documented?

4. **Document Baseline**
   - Establish starting point
   - Record original request
   - Note any gaps for refinement

## Output Format

```yaml
intake_result:
  status: <valid|needs_clarification|created|not_found>
  
  ticket_info:
    jira_id: <PROJ-1234>
    title: <story title>
    url: <JIRA URL>
    created_date: <date>
    created_by: <user>
    status: <Open|In Progress|Ready>
  
  business_context:
    summary: <business problem being solved>
    value: <business value delivered>
    priority: <critical|high|medium|low>
    stakeholder: <who requested this>
  
  current_acceptance_criteria:
    exists: <yes|no>
    criteria: [<list if exists>]
    completeness: <complete|partial|missing>
  
  dependencies:
    internal: [<list of dependent stories>]
    external: [<list of external dependencies>]
  
  gaps_identified: [<items needing clarification>]
  
  next_steps:
    - "Expand acceptance criteria"
    - "Clarify dependencies"
    - "Estimate effort"
  
  recommendation:
    action: <proceed_to_requirement_clarity|request_clarification|create_ticket>
    reason: <brief explanation>
```

## Examples

### Example 1: Valid Ticket with Good Information
```yaml
Input:
  jira_ticket_id: "CUST-2451"
  story_summary: "Add export to Excel for customer list"

Output:
  status: valid
  ticket_info:
    jira_id: "CUST-2451"
    title: "Add export to Excel for customer list"
    priority: "high"
    created_by: "Business Analyst"
  
  business_context:
    summary: "Sales team needs to export customer data for external reporting"
    value: "Saves 2 hours per week in manual export"
    priority: "high"
  
  current_acceptance_criteria:
    exists: yes
    criteria:
      - "Export button visible on customer list page"
      - "Export includes name, email, city, state"
      - "File format: .xlsx"
      - "Respects applied filters"
    completeness: "partial"
  
  gaps_identified:
    - "Maximum rows not specified"
    - "Error handling for large exports not defined"
    - "Performance expectations missing"
  
  recommendation:
    action: "proceed_to_requirement_clarity"
    reason: "Valid ticket with core requirements, gaps can be clarified in next stage"
```

### Example 2: Ticket Needs Clarification
```yaml
Input:
  jira_ticket_id: "CUST-2478"
  story_summary: "Improve performance"

Output:
  status: needs_clarification
  ticket_info:
    jira_id: "CUST-2478"
    title: "Improve performance"
    priority: "medium"
  
  business_context:
    summary: "System is slow in some areas"
    value: "Better user experience"
  
  current_acceptance_criteria:
    exists: no
    completeness: missing
  
  gaps_identified:
    - "Which specific pages/features are slow?"
    - "What is current performance baseline?"
    - "What is target performance?"
    - "Which users are affected?"
    - "Business impact of slow performance?"
  
  recommendation:
    action: "request_clarification"
    reason: "Story is too vague - needs specific problem definition"
    clarification_needed:
      - "Identify specific slow functionality"
      - "Provide performance metrics"
      - "Specify target performance"
```

### Example 3: Create New Ticket
```yaml
Input:
  jira_ticket_id: null
  story_summary: "Add customer segment field to profiles"

Output:
  status: created
  ticket_info:
    jira_id: "CUST-2512"
    title: "Add customer segment field to profiles"
    url: "https://jira.company.com/browse/CUST-2512"
  
  business_context:
    summary: "Support customer segmentation for targeted marketing"
    value: "Enable data-driven marketing campaigns"
    priority: "high"
  
  current_acceptance_criteria:
    exists: no
    completeness: missing
  
  gaps_identified:
    - "All acceptance criteria need to be generated"
    - "Segment options/values not defined"
    - "Reporting requirements unclear"
  
  recommendation:
    action: "proceed_to_requirement_clarity"
    reason: "New ticket created, ready for detailed requirement definition"
```

## Validation Checklist

- [ ] JIRA ticket exists or can be created
- [ ] Ticket has clear title and summary
- [ ] Business context is documented
- [ ] Priority is assigned
- [ ] Acceptance criteria exist (or will be created)
- [ ] Dependencies are identified
- [ ] Stakeholder is identifiable

## Information to Extract

### Required
- Story title/summary
- Business context (why we're doing this)
- Business value/benefit
- Priority level

### Strongly Recommended
- Acceptance criteria (or placeholder)
- Known dependencies
- Affected systems/pages
- Constraints (technical, regulatory, etc.)

### Optional but Helpful
- Original requester
- Target timeline
- Related tickets
- Mockups or examples

## JIRA Ticket Template

For new tickets, ensure they contain:

```
Summary: Clear, action-oriented title

Description:
As a [user role]
I want to [capability]
So that [business value]

Acceptance Criteria:
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

Business Value:
[Why this matters]

Priority: [High|Medium|Low]

Dependencies:
[Other stories or systems]
```

## Related Skills
- `acceptance-criteria-expander` - Expands criteria
- `requirement-extractor` - Extracts requirements
- `spike-charter` - Creates investigation ticket
