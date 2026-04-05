---
name: production-impact-assessor
description: Evaluates business and technical impact of production incidents to determine severity and required response urgency.
---

# Production Impact Assessor

## Quick Example

**Input:** "Login returns 500 error - all users affected"
**Output:** Severity: CRITICAL, Scope: ALL_USERS, Action: IMMEDIATE_HOTFIX
**Time:** 30 seconds

---

## Purpose
Evaluates business and technical impact of production incidents to determine severity and required response urgency.

## Input

```yaml
incident:
  description: <what's happening>
  affected_feature: <feature/module>
  affected_users: <all|many|few|specific>
  data_at_risk: <yes|no|unknown>
  workaround_available: <yes|no>
  started_at: <timestamp>
```

## Output

```yaml
impact_assessment:
  severity: CRITICAL|HIGH|MEDIUM|LOW
  scope: all_users|specific_users|specific_feature
  data_at_risk: yes|no|unknown
  business_impact: revenue|sla|customer_satisfaction|internal
  workaround_available: yes|no
  time_sensitivity: immediate|hours|day

  decision:
    action: immediate_hotfix|expedited_fix|standard_fix
    recommendation: <clear action>

  confidence: HIGH|MEDIUM|LOW
```

## Severity Criteria

### CRITICAL → Immediate Hotfix
- Production system down
- Complete feature failure
- Data corruption occurring
- All users affected
- Revenue-impacting
- No workaround

### HIGH → Expedited Fix
- Major functionality broken
- Multiple users affected
- No workaround
- Customer-facing impact

### MEDIUM → Standard Fix
- Functionality degraded
- Workaround exists
- Specific scenarios/users

### LOW → Can Defer
- Minor issues
- Workaround available
- Internal impact only

## DO:
✅ Assess actual business impact
✅ Consider data corruption risk
✅ Check for available workarounds
✅ Evaluate user count affected
✅ Determine time sensitivity
✅ Recommend clear action

## DON'T:
❌ Downplay severity to avoid hotfix
❌ Ignore data corruption risks
❌ Skip workaround assessment
❌ Underestimate user impact
❌ Delay critical assessments

## Error Conditions

**IF insufficient information:**
```
1. Ask specific questions:
   - How many users affected?
   - Is data at risk?
   - Any workaround available?
   - When did it start?
2. Use conservative assessment
3. Escalate if unclear
```

## Example 1: Critical

**Input:**
```yaml
description: "Login returns 500 error"
affected_feature: Authentication
affected_users: all
data_at_risk: no
workaround_available: no
```

**Output:**
```yaml
severity: CRITICAL
scope: all_users
business_impact: revenue
time_sensitivity: immediate
action: immediate_hotfix
recommendation: "System down, all users locked out - immediate hotfix required"
confidence: HIGH
```

## Example 2: High

**Input:**
```yaml
description: "Order export fails"
affected_feature: Order Management
affected_users: 50
workaround_available: yes (manual export)
```

**Output:**
```yaml
severity: HIGH
scope: specific_feature
business_impact: customer_satisfaction
time_sensitivity: hours
action: expedited_fix
recommendation: "Workaround exists but users impacted - expedited fix needed"
confidence: HIGH
```

---

**Related Skills:**
- `emergency-mitigation-planner` - For incident stabilization
- `hotfix-strategy-planner` - For resolution strategy
- `bug-classifier` - For non-production issues
