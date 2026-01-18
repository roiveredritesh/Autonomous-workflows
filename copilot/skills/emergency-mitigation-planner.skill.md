# Emergency Mitigation Planner Skill

## Purpose
Develops immediate stabilization strategies to reduce impact of critical production issues while root cause is being investigated.

## Input Requirements
```yaml
incident:
  severity: <critical|high>
  affected_feature: <feature name>
  user_count_affected: <number>
  data_at_risk: <yes|no>
  revenue_impact: <high|medium|low>
  description: <incident details>
```

## Processing Steps

1. **Identify Mitigation Options**
   - Feature disabling
   - Traffic redirection
   - Workaround enablement
   - Capacity scaling
   - Graceful degradation

2. **Evaluate Each Option**
   - Speed of implementation
   - Effectiveness
   - Risk level
   - User impact

3. **Prioritize Options**
   - Fastest high-impact first
   - Lowest-risk first
   - Combined approach if needed

4. **Create Implementation Plan**
   - Specific steps
   - Rollback procedure
   - Communication strategy

## Output Format

```yaml
mitigation_strategy:
  immediate_actions:
    - action: <specific action>
      implementation_time: <minutes>
      expected_relief: <percentage or users>
      risk: <low|medium|high>
  
  primary_mitigation:
    option: <feature_disable|traffic_redirect|workaround|scale|degrade>
    approach: <detailed approach>
    implementation_steps: [<step-by-step>]
    expected_impact: <improvement>
    time_to_implement: <minutes>
    rollback_steps: [<revert steps>]
  
  alternative_mitigations: [<other options if primary fails>]
  
  communication:
    customer_message: <what to tell users>
    eta_for_resolution: <estimated time>
    status_update_frequency: <how often>
  
  next_steps:
    - "Implement primary mitigation"
    - "Investigate root cause in parallel"
    - "Plan proper fix"
```

## Mitigation Types

### Feature Disabling
**When:** Feature is causing the issue but not essential
```yaml
approach: "Disable feature via feature flag or code"
implementation_time: "2-5 minutes"
example: "Disable faulty report export feature"
pros:
  - "Very fast"
  - "Easy to rollback"
cons:
  - "Users lose access to feature"
  - "May not work if feature is core"
```

### Traffic Redirection
**When:** One server/service is failing
```yaml
approach: "Redirect traffic away from failing component"
implementation_time: "5-15 minutes"
example: "Route requests to backup database instance"
pros:
  - "Immediate relief"
  - "Maintains service"
cons:
  - "Requires infrastructure setup"
  - "May overload alternate system"
```

### Graceful Degradation
**When:** Can provide reduced functionality
```yaml
approach: "Serve reduced/cached data instead of live"
implementation_time: "5-10 minutes"
example: "Show cached customer list instead of querying DB"
pros:
  - "Maintains service"
  - "Better than nothing"
cons:
  - "Data may be stale"
  - "User experience degraded"
```

### Capacity Scaling
**When:** System is overloaded
```yaml
approach: "Add resources or adjust limits"
implementation_time: "10-20 minutes"
example: "Increase server memory limit or add servers"
pros:
  - "May buy time for fix"
cons:
  - "Temporary solution"
  - "Costly"
```

### Workaround Communication
**When:** No technical mitigation available
```yaml
approach: "Communicate workaround to users"
implementation_time: "immediate"
example: "Tell users to clear browser cache and retry"
pros:
  - "No system changes"
  - "Low risk"
cons:
  - "Requires user action"
  - "May not solve for all"
```

## Mitigation Decision Matrix

```
Impact | Reversible | Implementation Time | Option
--------|-----------|---------------------|--------------
High   | Yes       | <5 min               | Feature disable
High   | Yes       | 5-15 min             | Traffic redirect
High   | Partial   | 5-10 min             | Degradation
Medium | Yes       | <10 min              | Workaround
Medium | No        | <30 min              | Fix properly
Low    | -         | -                    | Let run, fix later
```

## Example Mitigations

### Scenario 1: Order Processing Failing
```yaml
Issue: "Orders failing to save due to database connection pool exhaustion"

Options Evaluated:
  1. Feature disable: Not viable (core feature)
  2. Scale: Add DB connections immediately
  3. Degrade: Show cached order list (not viable for new orders)
  4. Redirect: Redirect to backup database

Primary Mitigation:
  action: "Scale database connection pool from 50 to 200"
  time: "3 minutes"
  impact: "Handles 4x more concurrent users"
  risk: "Low - just increasing limits"
  
Alternative:
  action: "Redirect to read-only mode"
  time: "5 minutes"
  message: "New orders temporarily disabled, existing orders can be viewed"
```

### Scenario 2: Search Timeout Loop
```yaml
Issue: "Search functionality causing cascading timeouts"

Primary Mitigation:
  action: "Disable search feature via feature flag"
  time: "2 minutes"
  impact: "Eliminates timeouts, users lose search"
  risk: "Low - quick rollback"
  message: "Search temporarily unavailable, use navigation instead"
  
Alternative:
  action: "Limit search to indexed fields only"
  time: "10 minutes"
  impact: "Faster searches, less comprehensive"
```

## Communication Template

**Initial Mitigation Alert:**
```
INCIDENT: [Brief description]
IMPACT: [What users can/cannot do]
MITIGATION ACTIVE: [What we're doing]
ETA: [When it should be resolved]
WORKAROUND: [What users can do]
```

**Resolution Update:**
```
UPDATE: [Progress]
MITIGATION: [Still active/escalating/resolving]
ROOT CAUSE: [If found]
ETA: [Updated estimate]
```

## Safety Rules
- NEVER apply mitigation without understanding trade-offs
- ALWAYS have rollback plan
- ALWAYS communicate status to users
- ALWAYS continue investigating root cause
- NEVER apply mitigation that corrupts data
- ALWAYS test mitigation in staging if possible

## Related Skills
- `production-impact-assessor` - Determines urgency
- `hotfix-strategy-planner` - Determines fix approach
- `production-verification-checker` - Validates mitigation worked
