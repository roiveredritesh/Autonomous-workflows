---
name: spike-findings-recorder
description: Systematically documents spike investigation findings, confidence levels, and actionable recommendations.
---

## Purpose
Systematically documents spike investigation findings, confidence levels, and actionable recommendations.

## Input Requirements
```yaml
spike_summary:
  question: <research question>
  time_allocated: <hours>
  time_spent: <hours>
  investigation_steps: [<what was investigated>]
  findings: [<discoveries>]
  evidence: [<supporting data>]
```

## Processing Steps

1. **Organize Findings**
   - What did we learn?
   - What was confirmed?
   - What was disproven?
   - What remains unknown?

2. **Assess Confidence**
   - High: Question fully answered with evidence
   - Medium: Partially answered, some unknowns
   - Low: Inconclusive, need more investigation

3. **Identify Risks**
   - New risks discovered
   - Risks that can be mitigated
   - Risks that remain

4. **Create Recommendations**
   - Immediate next steps
   - Future considerations
   - Decision point

## Output Format

```yaml
spike_findings_report:
  
  investigation_summary:
    question: <research question>
    time_allocated: <hours>
    time_spent: <hours>
    status: <complete|incomplete|blocked>
  
  what_we_learned:
    discoveries:
      - <discovery 1>
      - <discovery 2>
    confirmed_assumptions: [<what was right>]
    disproven_assumptions: [<what was wrong>]
    unknowns_remaining: [<still don't know>]
  
  evidence:
    - evidence: <finding>
      type: <measurement|test|code_review|documentation>
      confidence: <high|medium|low>
    - evidence: <finding>
      type: <type>
      confidence: <confidence>
  
  risk_assessment:
    new_risks_identified:
      - risk: <description>
        probability: <high|medium|low>
        impact: <high|medium|low>
        mitigation: <how to handle>
    
    risks_we_can_mitigate: [<list>]
    
    risks_requiring_acceptance: [<list>]
  
  confidence_level:
    overall: <high|medium|low>
    rationale: <why this confidence level>
    gaps: [<what would increase confidence>]
  
  recommendations:
    immediate_next_steps:
      - <action>
      - <action>
    
    future_considerations:
      - <consideration>
      - <consideration>
    
    decision_point:
      recommended_action: <proceed|pivot|needs_more_investigation|escalate>
      reasoning: <summary>
      alternative_actions:
        - option: <option>
          when_to_choose: <when applicable>
  
  artifacts_created:
    - <poc_code if applicable>
    - <test_results if applicable>
    - <documentation>
  
  lessons_learned:
    - <lesson>
    - <lesson>
  
  follow_up_actions:
    - action: <follow-up needed>
      owner: <who should do it>
      timing: <when>
```

## Examples

### Example 1: Investigation Complete - Proceed
```yaml
investigation_summary:
  question: "Can we add async/await to repository methods?"
  time_allocated: "4 hours"
  time_spent: "3.5 hours"
  status: complete

discoveries:
  - "Async is compatible with WebForms repository methods"
  - "ViewState works correctly with async"
  - "PostBack still functions normally"
  - "One gotcha: Exception handling differs slightly"

evidence:
  - evidence: "Created async GetCustomers() method on test page"
    type: test
    confidence: high
  - evidence: "Tested PostBack and state restoration"
    type: test
    confidence: high
  - evidence: "ViewState serialization still works"
    type: test
    confidence: high

confidence_level:
  overall: high
  rationale: "Created POC, tested multiple scenarios, all positive"
  gaps:
    - "Load testing under high concurrency not done"
    - "Performance impact not quantified"

risks_identified:
  - risk: "Potential deadlock if synchronous methods call async"
    probability: medium
    impact: high
    mitigation: "Document async-only repositories"

recommendation:
  action: proceed
  reasoning: "Async is viable, benefits outweigh risks"
  next_steps:
    - "Spike on performance impact"
    - "Create async repository pattern"
    - "Convert one repository as proof"
```

## Related Skills
- `spike-charter` - Defines investigation scope
- `requirement-extractor` - Clarifies investigation need
- `feature-feasibility-analyzer` - Uses spike findings for feasibility
