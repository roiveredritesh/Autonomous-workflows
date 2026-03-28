---
skill: rollback-plan-generator
version: 2.0.0
category: generation
complexity: low
estimated_time: 1-2 minutes
priority: high
last_updated: 2026-01-18
---

# Rollback Plan Generator

## Quick Example

**Input:** Deploy Excel export (2 files changed, no DB changes)
**Output:** 5-step rollback plan, 10min total time, git revert procedure
**Time:** 90 seconds

---

## Purpose
Creates detailed, tested rollback procedures to safely revert changes if deployment fails.

## Input

```yaml
change:
  description: <what's being deployed>
  files_changed: [<files>]
  database_changes: yes|no
  deployment_target: production|staging|dev
  risk_level: LOW|MEDIUM|HIGH
```

## Output

```yaml
rollback_plan:
  deployment_summary:
    description: <change description>
    files_modified: <count>
    database_changes: yes|no
    risk_level: LOW|MEDIUM|HIGH

  rollback_triggers:
    - trigger: <what indicates need>
      metric: <how to detect>
      action: initiate_rollback

  rollback_procedure:
    decision_maker: <who decides>
    steps:
      - action: <specific step>
        time: <minutes>
        owner: <who executes>

  validation:
    - check: <what to verify>
      success_criteria: <definition>

  communication:
    notify: [<who>]
    message: <template>

  time_estimates:
    total_downtime: <minutes>

  confidence: HIGH|MEDIUM|LOW
```

## Rollback Types

### Code Only (Simplest)
- Git revert to previous commit
- No database changes
- Quick validation
- Time: 5-15 minutes

### Code + Configuration
- Revert code
- Restore config files
- Clear cache if needed
- Time: 10-20 minutes

### Code + Database (Complex)
- Revert code
- Restore database backup
- Validate data integrity
- Time: 20-60 minutes

## DO:
✅ Test rollback procedure before deployment
✅ Document all rollback steps
✅ Include validation criteria
✅ Specify time estimates
✅ Identify rollback triggers
✅ Plan communication

## DON'T:
❌ Deploy without rollback plan
❌ Skip rollback testing
❌ Assume rollback will work
❌ Forget database backup
❌ Omit validation steps
❌ Ignore communication needs

## Error Conditions

**IF database changes involved:**
```
1. REQUIRE database backup
2. Document restore procedure
3. Include data validation steps
4. Test restore in non-prod
5. Add extra time buffer
```

**IF high-risk deployment:**
```
1. Test rollback in staging first
2. Have team standing by
3. Monitor metrics closely
4. Plan staged rollback if possible
5. Double validation steps
```

## Example 1: Simple Code Rollback

**Input:**
```yaml
description: "Add Excel export button"
files_changed: ["CustomerList.aspx", "CustomerList.aspx.cs"]
database_changes: no
risk_level: LOW
```

**Output:**
```yaml
rollback_procedure:
  decision_maker: "Deployment lead"

  steps:
    - action: "Git revert to commit abc123"
      time: "2 minutes"
      owner: "DevOps"

    - action: "Rebuild and deploy previous version"
      time: "5 minutes"
      owner: "DevOps"

    - action: "Clear application cache"
      time: "1 minute"
      owner: "DevOps"

validation:
  - check: "Page loads without errors"
    success_criteria: "200 status, no exceptions"

  - check: "Existing functionality works"
    success_criteria: "Search, filter work as before"

rollback_triggers:
  - trigger: "Page returns 500 error"
    metric: "Error rate > 0%"
    action: "Immediate rollback"

  - trigger: "Export breaks other features"
    metric: "User reports + testing"
    action: "Rollback within 1 hour"

time_estimates:
  total_downtime: "8 minutes"

confidence: HIGH
```

## Example 2: Database Rollback

**Input:**
```yaml
description: "Add CustomerSegment column"
database_changes: yes
risk_level: MEDIUM
```

**Output:**
```yaml
rollback_procedure:
  decision_maker: "Tech lead"

  steps:
    - action: "Stop application"
      time: "1 minute"

    - action: "Restore database backup"
      time: "15 minutes"
      owner: "DBA"

    - action: "Validate data integrity"
      time: "5 minutes"
      owner: "DBA"

    - action: "Git revert code changes"
      time: "3 minutes"
      owner: "DevOps"

    - action: "Deploy previous version"
      time: "5 minutes"
      owner: "DevOps"

    - action: "Start application"
      time: "2 minutes"

validation:
  - check: "Database schema correct"
    success_criteria: "CustomerSegment column removed"

  - check: "Data intact"
    success_criteria: "Record count matches backup"

  - check: "Application functional"
    success_criteria: "All features working"

rollback_triggers:
  - trigger: "Data corruption detected"
    metric: "Data validation fails"
    action: "IMMEDIATE rollback"

  - trigger: "Performance degradation"
    metric: "Query time > 2x baseline"
    action: "Rollback within 30 min"

time_estimates:
  total_downtime: "31 minutes"

confidence: MEDIUM
```

## Validation Checklist

Before deployment:
- [ ] Rollback procedure documented
- [ ] Rollback tested in non-prod
- [ ] Database backup verified (if DB changes)
- [ ] Validation criteria defined
- [ ] Time estimates realistic
- [ ] Communication plan ready
- [ ] Team briefed on rollback

---

**Related Skills:**
- `minimal-diff-planner` - Minimizes rollback complexity
- `hotfix-deployment-planner` - For hotfix rollback planning
- `safe-change-boundary-detector` - Identifies low-risk changes
