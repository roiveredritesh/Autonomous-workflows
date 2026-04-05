---
name: requirement-extractor
description: Identifies and clarifies functional, non-functional, and constraint requirements from ambiguous or incomplete specifications.
---

## Quick Example

**Input:** "Add Excel export to customer list page"
**Output:** must_have: [Export button, xlsx format, respect filters, max 10K rows]; questions: [columns to include? error handling?]

---

## Purpose
Identifies and clarifies functional, non-functional, and constraint requirements from ambiguous or incomplete specifications.

## Input Requirements
```yaml
specification:
  original_input: <user statement or story>
  context: <any background information>
  constraints: [<known constraints>]
  related_stories: [<ticket IDs if any>]
```

## Processing Steps

1. **Parse Original Input**
   - Identify core request
   - Note assumptions
   - List missing details

2. **Apply Five Whys Technique**
   - Why is this needed?
   - Why does it matter?
   - Why this approach?
   - Why now?
   - Why these constraints?

3. **Categorize Requirements**
   - Functional (MUST have)
   - Non-functional (HOW it works)
   - Constraints (Technical, business, regulatory)
   - Dependencies (What else it needs)

4. **Identify Gaps**
   - What's unclear?
   - What's missing?
   - What's assumed?
   - What needs investigation?

## Output Format

```yaml
requirement_extraction:
  
  original_request: <original statement>
  
  core_need: <fundamental user need>
  
  functional_requirements:
    must_have:
      - <requirement>
      - <requirement>
    should_have:
      - <requirement>
      - <requirement>
    nice_to_have:
      - <requirement>
  
  non_functional_requirements:
    performance:
      - <requirement>
    usability:
      - <requirement>
    reliability:
      - <requirement>
    security:
      - <requirement>
    scalability:
      - <requirement>
  
  constraints:
    technical:
      - <constraint>
    business:
      - <constraint>
    regulatory:
      - <constraint>
    timeline:
      - <constraint>
  
  dependencies:
    internal: [<stories or systems>]
    external: [<third-party services>]
    data: [<data requirements>]
  
  assumptions:
    - <assumption>
    - <assumption>
  
  questions_requiring_clarification:
    - <question>
    - <question>
  
  recommendation:
    completeness: <complete|mostly_complete|incomplete|very_unclear>
    ready_for_implementation: <yes|no|with_spike>
    next_step: <proceed|clarify|spike|refine>
```

## Related Skills
- `acceptance-criteria-generator` - Converts requirements to testable criteria
- `edge-case-detector` - Identifies edge cases from requirements
- `spike-charter` - Plans investigation for unclear requirements
