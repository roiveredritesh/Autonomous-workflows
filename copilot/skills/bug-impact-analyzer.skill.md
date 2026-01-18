# Bug Impact Analyzer Skill

## Purpose
Assesses the scope and impact of a bug to understand who is affected and how severely.

## Input Requirements
```yaml
bug:
  description: <bug description>
  affected_feature: <feature>
  reproduction_steps: [<steps>]
  environment: <prod|staging|dev>
  first_reported: <when>
```

## Processing Steps

1. **User Impact Assessment**
   - Who is affected?
   - How many users?
   - What can't they do?

2. **Data Impact Assessment**
   - Is data being corrupted?
   - Is data being lost?
   - Is data integrity at risk?

3. **System Impact Assessment**
   - Performance impact?
   - Availability impact?
   - Cascading failures?

4. **Scope Analysis**
   - Just one feature or multiple?
   - Just one page or multiple?
   - Just one user type or multiple?

## Output Format

```yaml
impact_assessment:
  
  user_impact:
    estimated_affected_users: <count|percentage>
    user_types_affected: [<types>]
    what_they_cannot_do: [<functionality>]
    severity_per_user: <high|medium|low>
  
  data_impact:
    data_at_risk: <none|being_lost|corrupted|exposed>
    scope: <single_record|multiple|all>
    recovery_possible: <yes|no|with_effort>
  
  system_impact:
    performance_affected: <yes|no|degraded>
    availability_affected: <yes|no>
    cascading_failures: <yes|no>
  
  scope_analysis:
    affected_features: [<list>]
    affected_pages: [<list>]
    affected_modules: [<list>]
    scope_estimate: <single_component|multiple|application_wide>
  
  business_impact:
    revenue_impact: <none|minimal|moderate|severe>
    customer_facing: <yes|no>
    workaround_exists: <yes|no>
  
  priority_assessment:
    urgency: <immediate|urgent|soon|defer>
    impact_score: <1-10>
    recommendation: <hotfix|expedited_fix|standard|defer>
```

## Related Skills
- `bug-classifier` - Classifies bug severity
- `production-impact-assessor` - For production assessment
