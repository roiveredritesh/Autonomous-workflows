# Spike Findings Recorder Skill

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

### Example 2: Investigation Blocked - Escalate
```yaml
investigation_summary:
  question: "Can we integrate with new payment provider?"
  time_allocated: "6 hours"
  time_spent: "4 hours"
  status: blocked

discoveries:
  - "Payment provider API requires OAuth 2.0"
  - "Documentation unclear on WebForms integration"
  - "No C# samples available"

evidence:
  - evidence: "Reviewed 10 integration guides, all for ASP.NET Core"
    type: documentation
    confidence: medium
  - evidence: "Provider support says 'WebForms should work' but unconfirmed"
    type: communication
    confidence: low

blockers:
  - "No working example for WebForms"
  - "API requires HTTPS redirect handling complex in WebForms"
  - "Provider support slow to respond"

recommendation:
  action: escalate
  reasoning: "Cannot complete investigation in available time"
  escalation:
    - "Request provider technical resources"
    - "Consider direct integration or abstraction layer"
    - "May require POC with provider support"
  
  follow_up:
    - action: "Contact payment provider for WebForms guidance"
      timing: "Next business day"
    - action: "Plan larger spike if proceeding"
      timing: "Based on provider response"
```

### Example 3: Investigation Inconclusive - More Research Needed
```yaml
investigation_summary:
  question: "Why does search timeout on large result sets?"
  time_allocated: "4 hours"
  time_spent: "4 hours"
  status: incomplete

discoveries:
  - "Timeout occurs with 50K+ results"
  - "Timeout in data formatting, not query"
  - "Different root causes for different queries"

evidence:
  - evidence: "Query completes in 1 second, formatting takes 15 seconds"
    type: measurement
    confidence: high
  - evidence: "Simple queries format quickly, complex format slowly"
    type: measurement
    confidence: medium

unknowns_remaining:
  - "Exact formatting bottleneck (serialization? rendering?)"
  - "Why complex vs simple queries differ so much"
  - "Whether pagination would help"

confidence_level:
  overall: medium
  rationale: "Found issue location but not root cause"
  gaps:
    - "Need profiler data on formatting"
    - "Need to test with pagination"

recommendation:
  action: needs_more_investigation
  reasoning: "Found area of concern but need deeper analysis"
  next_spike:
    - "Profile formatting code with large dataset"
    - "Test pagination approach"
    - "Measure impact of each formatting step"
  
  estimated_effort: "6-8 hours for deeper analysis"
```

## Confidence Assessment

### High Confidence
- Question fully answered
- Evidence is clear and reproducible
- POC successful if needed
- No significant unknowns
- **Decision:** Can make decisions based on findings

### Medium Confidence
- Question partially answered
- Some evidence, some gaps
- Manageable unknowns
- POC partially successful
- **Decision:** Can proceed with caution, plan mitigations

### Low Confidence
- Question not well answered
- Evidence incomplete
- Significant unknowns remain
- POC failed or blocked
- **Decision:** Need more investigation or spike

## Risk Documentation

For each risk identified:

```yaml
risk:
  description: <clear description>
  probability: <high|medium|low>
    reasoning: <why this probability>
  
  impact: <high|medium|low>
    reasoning: <why this impact>
  
  mitigation: <how to reduce risk>
  
  acceptance: <if we must proceed despite risk>
```

## Recommendation Framework

```
Confidence | Risks | Recommendation
-----------|-------|------------------
High       | Low   | Proceed immediately
High       | High  | Proceed with mitigations
Medium     | Low   | Proceed with caution
Medium     | High  | Mitigate first, then proceed
Low        | Any   | More investigation needed
```

## Related Skills
- `spike-charter` - Defines investigation scope
- `requirement-extractor` - Clarifies investigation need
- `feature-feasibility-analyzer` - Uses spike findings for feasibility assessment
