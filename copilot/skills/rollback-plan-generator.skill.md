# Rollback Plan Generator Skill

## Purpose
Creates detailed rollback procedures to safely revert changes if needed.

## Input Requirements
```yaml
change:
  description: <what's being deployed>
  files_changed: [<files>]
  database_changes: [<schema changes if any>]
  deployment_target: <environment>
  affected_users: <count|percentage>
```

## Processing Steps

1. **Identify Rollback Triggers**
   - What indicates rollback is needed?
   - Who decides to rollback?

2. **Plan Reversion Steps**
   - Code rollback
   - Database rollback
   - Cache clearing
   - Configuration revert

3. **Create Validation Steps**
   - How to verify rollback succeeded?
   - How to confirm system healthy?

4. **Prepare Communications**
   - Who to notify?
   - What to communicate?

## Output Format

```yaml
rollback_plan:
  
  deployment_summary:
    change_description: <what deployed>
    files_modified: <count>
    database_changes: <yes|no>
    affected_components: [<list>]
  
  rollback_triggers:
    - trigger: <what indicates rollback needed>
      metric: <how to detect>
      action: <initiate rollback>
  
  rollback_procedure:
    decision_point: <who decides>
    go_no_go_criteria: [<criteria>]
    
    rollback_steps:
      - step_1: <specific action>
        time_estimate: <minutes>
        owner: <who does this>
      
      - step_2: <action>
        ...
    
    database_rollback:
      - action: <if database changed>
      - backup_location: <where backup is>
      - restore_procedure: <how to restore>
      - data_validation: <how to verify>
    
    cache_clearing:
      - action: <clear if needed>
    
    configuration_revert:
      - action: <revert if changed>
  
  validation_steps:
    - check: <what to verify>
      success_criteria: <definition of success>
      owner: <who verifies>
    
    - check: <another check>
      ...
  
  communication_plan:
    notify_first: <immediate notification>
    message: <what to communicate>
    follow_up: <status updates>
    
    when_rollback_complete:
      message: <completion message>
      notify: <who to notify>
  
  rollback_testing:
    tested: <yes|no>
    when_tested: <when>
    results: <successful|issues_found>
    issues_found: [<if any>]
  
  time_estimates:
    decision_to_start: <minutes>
    rollback_execution: <minutes>
    validation: <minutes>
    total_downtime: <minutes>
  
  success_criteria:
    - <rollback succeeded if...>
    - <system healthy if...>
```

## Related Skills
- `hotfix-deployment-planner` - For hotfix rollback
- `minimal-diff-planner` - Minimizes rollback complexity
