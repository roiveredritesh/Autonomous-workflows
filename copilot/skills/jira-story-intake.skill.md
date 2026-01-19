---
skill: jira-story-intake
version: 2.0.0
category: validation
complexity: low
estimated_time: 30-60 seconds
priority: high
last_updated: 2026-01-18
---

# JIRA Story Intake

## Quick Example

**Input:** Ticket CUST-2451 "Add Excel export to customer list"
**Output:** Valid ticket, partial criteria, 3 gaps identified → Proceed to requirements
**Time:** 40 seconds

---

## Purpose
Validates and extracts essential information from JIRA tickets to establish a clear baseline for feature delivery.

## Input

```yaml
intake:
  jira_ticket_id: <PROJ-1234 or null>
  story_summary: <title>
  description: <details>
  acceptance_criteria: [<if any>]
```

## Output

```yaml
intake_result:
  status: valid|needs_clarification|created|not_found

  ticket_info:
    jira_id: <PROJ-1234>
    title: <story title>
    priority: critical|high|medium|low

  business_context:
    summary: <problem being solved>
    value: <business benefit>
    stakeholder: <who requested>

  current_acceptance_criteria:
    exists: yes|no
    criteria: [<list>]
    completeness: complete|partial|missing

  gaps_identified: [<clarifications needed>]

  recommendation:
    action: proceed|request_clarification|create_ticket
    reason: <explanation>

  confidence: HIGH|MEDIUM|LOW
```

## DO:
✅ Validate ticket exists or can be created
✅ Extract business context and value
✅ Document existing acceptance criteria
✅ Identify gaps requiring clarification
✅ Capture dependencies
✅ Establish clear baseline

## DON'T:
❌ Proceed with invalid or missing tickets
❌ Skip gap identification
❌ Assume missing information
❌ Ignore business context
❌ Overlook dependencies

## Error Conditions

**IF ticket not found:**
```
1. Check if ticket ID valid
2. Attempt to create new ticket
3. If creation fails:
   - Return status: not_found
   - Request valid ticket or creation permission
```

**IF critical information missing:**
```
1. Flag as needs_clarification
2. List specific gaps:
   - Missing business context
   - No acceptance criteria
   - Unclear problem definition
3. Recommend: request_clarification
4. Provide template for stakeholder
```

## Status Values

### valid
- Ticket exists
- Has core information
- Can proceed (gaps addressable)

### needs_clarification
- Too vague or incomplete
- Missing critical context
- Requires stakeholder input

### created
- New ticket created successfully
- Needs requirements definition

### not_found
- Ticket doesn't exist
- Cannot create ticket
- Invalid ticket ID

## Example 1: Valid Ticket

**Input:**
```yaml
jira_ticket_id: "CUST-2451"
story_summary: "Add Excel export to customer list"
```

**Output:**
```yaml
status: valid
ticket_info:
  jira_id: "CUST-2451"
  title: "Add Excel export to customer list"
  priority: high

business_context:
  summary: "Sales team needs customer data for external reporting"
  value: "Saves 2 hours/week in manual export"
  stakeholder: "Business Analyst"

current_acceptance_criteria:
  exists: yes
  criteria:
    - "Export button on customer list page"
    - "Export includes name, email, city, state"
    - "File format: .xlsx"
    - "Respects applied filters"
  completeness: partial

gaps_identified:
  - "Maximum rows not specified"
  - "Error handling for large exports not defined"
  - "Performance expectations missing"

recommendation:
  action: proceed
  reason: "Valid ticket with core requirements, gaps addressable"
confidence: HIGH
```

## Example 2: Needs Clarification

**Input:**
```yaml
jira_ticket_id: "CUST-2478"
story_summary: "Improve performance"
```

**Output:**
```yaml
status: needs_clarification
ticket_info:
  jira_id: "CUST-2478"
  title: "Improve performance"
  priority: medium

gaps_identified:
  - "Which specific pages/features are slow?"
  - "What is current performance baseline?"
  - "What is target performance?"
  - "Which users affected?"
  - "Business impact?"

recommendation:
  action: request_clarification
  reason: "Too vague - needs specific problem definition"
confidence: LOW
```

## Validation Checklist

Before proceeding:
- [ ] Ticket exists or created
- [ ] Clear title and summary
- [ ] Business context documented
- [ ] Priority assigned
- [ ] Acceptance criteria exist or planned
- [ ] Dependencies identified
- [ ] Stakeholder identifiable

---

**Related Skills:**
- `acceptance-criteria-expander` - Expands criteria
- `requirement-extractor` - Extracts detailed requirements
- `story-analyzer` - Analyzes story completeness
