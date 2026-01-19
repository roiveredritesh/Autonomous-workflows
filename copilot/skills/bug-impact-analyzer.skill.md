---
skill: bug-impact-analyzer
version: 2.0.0
category: analysis
complexity: low
estimated_time: 1-2 minutes
priority: high
last_updated: 2026-01-18
---

# Bug Impact Analyzer

## Quick Example

**Input:** Customer search returns wrong results
**Output:** 200 users affected, data integrity safe, business impact HIGH → Expedite
**Time:** 90 seconds

---

## Purpose
Assesses scope and impact of bugs on users, data, and business operations to prioritize response.

## Input

```yaml
bug:
  description: <bug description>
  affected_feature: <feature/page>
  environment: production|staging|dev
```

## Output

```yaml
impact_assessment:
  user_impact:
    affected_users: <count or %>
    severity_per_user: HIGH|MEDIUM|LOW
    workaround_available: yes|no

  data_impact:
    data_at_risk: none|corrupted|lost|exposed
    recovery_possible: yes|no|with_effort

  business_impact:
    revenue_impact: none|minimal|moderate|severe
    customer_facing: yes|no

  scope:
    affected_features: [<list>]
    scope_estimate: single|multiple|wide

  urgency: IMMEDIATE|URGENT|SOON|DEFER
  recommendation: hotfix|expedited|standard|defer

  confidence: HIGH|MEDIUM|LOW
```

## DO:
✅ Assess actual user count
✅ Check data corruption/loss
✅ Evaluate business impact
✅ Identify workarounds
✅ Determine urgency

## DON'T:
❌ Underestimate user impact
❌ Ignore data integrity
❌ Overlook revenue impact
❌ Skip workaround check

---

**Related Skills:**
- `bug-classifier` - Categorizes bug
- `production-impact-assessor` - Production severity
- `minimal-fix-planner` - Plans fix
