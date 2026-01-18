# Hotfix Strategy Planner Skill

## Purpose
Determines the fastest safe way to resolve a critical production issue.

## Input Requirements
```yaml
hotfix:
  issue: <problem description>
  root_cause: <identified cause>
  resolution_options: [<options>]
  time_available: <minutes>
```

## Processing Steps

1. **Evaluate Resolution Options**
   - Rollback
   - Configuration change
   - Feature disable
   - Code patch
   - Data fix

2. **Assess Time/Risk/Safety**
   - How long each option?
   - Risk level?
   - Rollback safe?

3. **Choose Best Option**
   - Fastest safe approach?
   - What's the best trade-off?

4. **Plan Implementation**
   - Detailed steps
   - Validation checks
   - Rollback readiness

## Output Format

```yaml
hotfix_strategy:
  
  issue_summary:
    problem: <description>
    root_cause: <cause>
    severity: <critical|high>
  
  options_evaluated:
    - option: <resolution approach>
      time_to_implement: <minutes>
      risk_level: <low|medium|high>
      rollback_safe: <yes|no>
      data_risk: <none|low|medium|high>
      pros: [<advantages>]
      cons: [<disadvantages>]
    
    - option: <another>
      ...
  
  chosen_strategy:
    option: <which chosen>
    reasoning: <why best>
    time_estimate: <minutes>
    risk_level: <low|medium|high>
  
  implementation_plan:
    step_1: <action>
    step_2: <action>
    step_3: <action>
  
  validation_plan:
    pre_implementation_checks: [<checks>]
    post_implementation_checks: [<checks>]
  
  rollback_plan:
    rollback_ready: <yes|no>
    rollback_steps: [<steps>]
    rollback_time: <minutes>
  
  communication_plan:
    initial_message: <message>
    resolution_message: <message>
```

## Related Skills
- `production-impact-assessor` - Assesses impact
- `emergency-mitigation-planner` - For stabilization
- `hotfix-deployment-planner` - For deployment
