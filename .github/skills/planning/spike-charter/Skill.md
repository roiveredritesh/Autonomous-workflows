---
name: spike-charter
description: Creates focused, time-boxed research charters to investigate technical unknowns and validate assumptions.
---

## Purpose
Creates a focused, time-boxed research charter to investigate technical unknowns and validate assumptions.

## Input Requirements
```yaml
investigation:
  area: <what to investigate>
  uncertainty: <what we don't know>
  decision_needed: <what decision depends on this>
  current_assumptions: [<what we assume>]
  timeline_available: <hours or days>
```

## Processing Steps

1. **Frame Research Question**
   - Make it specific and answerable
   - Identify success criteria
   - Note out-of-scope items

2. **Create Hypothesis**
   - What do we expect to find?
   - Why do we expect that?
   - What would surprise us?

3. **Define Approach**
   - Investigation steps
   - Proof-of-concept needs
   - Tools/environments needed

4. **Set Time Box**
   - Realistic time estimate
   - Hard stop condition
   - Milestone checkpoints

## Output Format

```yaml
spike_charter:
  
  research_question: <specific, answerable question>
  
  business_context:
    why_needed: <business decision or uncertainty>
    decision_maker: <who needs answer>
    deadline: <when decision needed>
  
  scope:
    in_scope:
      - <what we're investigating>
      - <what we're investigating>
    out_of_scope:
      - <what we're not investigating>
      - <what we're excluding>
  
  hypothesis:
    expected_outcome: <what we think we'll find>
    rationale: <why we think this>
    alternatives_to_test: [<other possibilities>]
  
  success_criteria:
    - criterion: <specific measurable criteria>
    - criterion: <example question answered>
    - criterion: <example proof provided>
  
  investigation_approach:
    step_1: <investigation step>
    step_2: <investigation step>
    step_3: <investigation step>
  
  required_resources:
    environments: [<dev|staging|test>]
    tools: [<needed tools>]
    data: [<data needed>]
    access: [<access needed>]
  
  time_box:
    allocated: <hours or days>
    estimated_breakdown:
      investigation: <X hours>
      documentation: <X hours>
      poc: <X hours if needed>
    hard_stop: <when investigation must finish>
  
  milestones:
    - checkpoint_1: <time and what you should know>
    - checkpoint_2: <time and what you should know>
  
  escalation_criteria:
    - criterion: "Investigation blocked by X"
      action: "Escalate and pivot"
    - criterion: "Major finding requiring larger scope"
      action: "Reframe and extend time box"
  
  expected_output:
    - "Clear answer to research question"
    - "Confidence level (high|medium|low)"
    - "Identified risks if proceeding"
    - "Recommendations for next step"
```

## Example Charters

### Example 1: Technology Feasibility
```yaml
research_question: "Can we add async/await to repository methods without breaking WebForms ViewState?"

business_context:
  why_needed: "Performance concern with database operations"
  decision_maker: "Architecture team"
  deadline: "End of month technical review"

scope:
  in_scope:
    - "WebForms lifecycle compatibility with async"
    - "ViewState serialization with async methods"
    - "Proof-of-concept on one repository"
  out_of_scope:
    - "Full application conversion to async"
    - "Performance optimization"
    - "Async UI improvements"

hypothesis:
  expected_outcome: "Async is compatible with WebForms with specific limitations"
  rationale: "WebForms is synchronous by design, but may support async in repository layer"
  alternatives_to_test:
    - "Async fully incompatible"
    - "Async works but requires architectural changes"

success_criteria:
  - "Can create async repository method without breaking ViewState"
  - "Async database calls complete without deadlock"
  - "PostBack still works correctly with async methods"

investigation_approach:
  step_1: "Review WebForms lifecycle with async"
  step_2: "Create POC async repository method"
  step_3: "Test POC on isolated test page"
  step_4: "Document findings and gotchas"

time_box:
  allocated: "4 hours"
  breakdown:
    investigation: "1 hour"
    poc: "2 hours"
    documentation: "1 hour"
  hard_stop: "COB Friday"

milestones:
  checkpoint_1: "After 1 hour - understand WebForms+async compatibility"
  checkpoint_2: "After 2.5 hours - POC code working or blocked"
  checkpoint_3: "After 4 hours - decision point"
```

## Related Skills
- `requirement-extractor` - Clarifies investigation need
- `spike-findings-recorder` - Documents investigation results
- `webforms-lifecycle-analyzer` - For WebForms investigations
