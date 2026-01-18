# Production Impact Assessor Skill

## Purpose
Evaluates the business and technical impact of production incidents to determine severity and urgency.

## Input Requirements
```yaml
incident:
  description: <brief incident description>
  affected_feature: <feature or module>
  error_message: <if applicable>
  user_reports: [<reported issues>]
  started_at: <timestamp>
  affected_users: <estimate or count>
```

## Processing Steps

1. **Analyze User Impact**
   - Identify affected user count or percentage
   - Determine completeness of feature failure (partial/complete)
   - Check for workarounds available

2. **Assess Data Risk**
   - Is data being corrupted?
   - Is data being lost?
   - Is sensitive data exposed?

3. **Evaluate Business Impact**
   - Revenue impact
   - SLA violations
   - Customer-facing implications

4. **Determine Time Sensitivity**
   - Immediate action required?
   - Can it wait hours?
   - Can it wait until next business day?

## Output Format

```yaml
impact_assessment:
  severity: <critical|high|medium|low>
  scope: <all_users|specific_users|specific_feature|internal>
  data_at_risk: <yes|no|unknown>
  business_impact: <revenue|sla|customer_satisfaction|internal>
  workaround_available: <yes|no>
  time_sensitivity: <immediate|hours|day|can_wait>
  
  estimated_impact:
    affected_users: <count or percentage>
    revenue_impact: <estimated or known>
    duration_so_far: <time since start>
  
  decision:
    action: <immediate_hotfix|expedited_fix|standard_fix|escalate>
    recommendation: <clear action>
```

## Examples

### Example 1: Critical - Production Down
```yaml
Input:
  description: "Login page returns 500 error"
  affected_feature: "Authentication"
  error_message: "NullReferenceException in LoginHandler"
  user_reports: ["Cannot login", "All users affected"]
  affected_users: "All"

Output:
  severity: critical
  scope: all_users
  data_at_risk: no
  business_impact: revenue
  workaround_available: no
  time_sensitivity: immediate
  action: immediate_hotfix
```

### Example 2: High - Significant Feature Broken
```yaml
Input:
  description: "Order export to Excel fails"
  affected_feature: "Order Management"
  error_message: "OutOfMemoryException"
  user_reports: ["Export button throws error"]
  affected_users: "50"

Output:
  severity: high
  scope: specific_feature
  data_at_risk: no
  business_impact: customer_satisfaction
  workaround_available: yes (manual export)
  time_sensitivity: hours
  action: expedited_fix
```

### Example 3: Medium - Partial Impact
```yaml
Input:
  description: "Search results slow for large datasets"
  affected_feature: "Search"
  error_message: null
  user_reports: ["Timeouts on complex filters"]
  affected_users: "10"

Output:
  severity: medium
  scope: specific_users
  data_at_risk: no
  business_impact: customer_satisfaction
  workaround_available: yes (simpler filters)
  time_sensitivity: day
  action: standard_fix
```

## Assessment Criteria

### Critical Severity
- Production system down or severely degraded
- Complete feature failure
- Data corruption or loss occurring
- All users affected
- Revenue-impacting
- No workaround

### High Severity
- Major functionality broken
- Partial feature failure
- Multiple users affected
- No workaround available
- Customer-facing impact

### Medium Severity
- Functionality degraded
- Workaround exists
- Specific scenarios or users affected
- Customer inconvenience

### Low Severity
- Cosmetic or minor issues
- Workaround available
- Rarely encountered
- Internal impact only

## Related Skills
- `emergency-mitigation-planner` - For stabilization
- `production-log-analyzer` - For root cause
- `hotfix-strategy-planner` - For resolution approach
