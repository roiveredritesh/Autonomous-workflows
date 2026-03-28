---
skill: bug-classifier
version: 2.0.0
category: analysis
complexity: low
estimated_time: 30-60 seconds
priority: high
last_updated: 2026-01-18
---

# Bug Classifier

## Quick Example

**Input:** "Customer search returns wrong results"
**Output:** Severity: HIGH, Type: FUNCTIONAL, Reproducible: YES → BUG workflow
**Time:** 45 seconds

---

## Purpose
Classifies bug reports by severity, type, and reproducibility to determine appropriate response workflow (HOTFIX, BUG, or SPIKE).

## Input

```yaml
bug_report:
  description: <what's broken>
  environment: <production|staging|dev>
  affected_users: <all|many|few|one>
  error_message: <if any>
  reproduction_steps: <if known>
```

## Output

```yaml
classification:
  severity: CRITICAL|HIGH|MEDIUM|LOW
  type: FUNCTIONAL|PERFORMANCE|DATA|UI|SECURITY
  reproducible: YES|NO|INTERMITTENT
  affected_users: ALL|MANY|FEW|ONE

  decision:
    workflow: HOTFIX|BUG|SPIKE
    urgency: IMMEDIATE|HOURS|DAYS|NORMAL
    reason: <explanation>

  confidence: HIGH|MEDIUM|LOW
```

## Severity Levels

### CRITICAL → HOTFIX (if production)
- System down or severely degraded
- Complete feature failure
- Data corruption
- All users affected
- No workaround

### HIGH → Expedited BUG
- Major functionality broken
- Multiple users affected
- No workaround
- Customer-facing issue

### MEDIUM → Standard BUG
- Functionality degraded
- Workaround exists
- Specific scenarios
- Intermittent issues

### LOW → Can defer
- Cosmetic issues
- Minor inconveniences
- Rarely encountered

## DO:
✅ Classify based on actual impact
✅ Escalate CRITICAL + Production to HOTFIX immediately
✅ Route non-reproducible bugs to SPIKE
✅ Consider environment (production critical)
✅ Ask clarifying questions if unclear
✅ Document classification reasoning

## DON'T:
❌ Downgrade severity based on fix difficulty
❌ Skip impact assessment
❌ Assume frequency without evidence
❌ Ignore production environment context
❌ Proceed with insufficient information

## Error Conditions

**IF insufficient information:**
```
1. Stop classification
2. Return: NEEDS_CLARIFICATION
3. Request:
   - Specific affected functionality
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment where bug occurs
```

**IF cannot reproduce:**
```
1. Classify as reproducible: NO
2. Recommend: SPIKE workflow
3. Reason: Investigation needed before fix
```

## Decision Matrix

```
Severity  | Environment | Reproducible | → Workflow
----------|-------------|--------------|------------
CRITICAL  | Production  | YES/NO       | → HOTFIX
HIGH      | Production  | YES          | → BUG (expedited)
HIGH      | Production  | NO           | → SPIKE
MEDIUM/LOW| Production  | YES          | → BUG
MEDIUM/LOW| Production  | NO           | → SPIKE
ANY       | Dev/Staging | YES          | → BUG
ANY       | Dev/Staging | NO           | → SPIKE
```

## Example 1: Critical Production

**Input:**
```yaml
description: "Orders failing 100%"
environment: production
affected_users: all
error_message: "NullReferenceException in ShippingCalculator"
```

**Output:**
```yaml
severity: CRITICAL
type: FUNCTIONAL
reproducible: YES
affected_users: ALL
decision:
  workflow: HOTFIX
  urgency: IMMEDIATE
  reason: "Complete feature failure affecting all users"
confidence: HIGH
```

## Example 2: Intermittent Issue

**Input:**
```yaml
description: "Search sometimes times out"
environment: production
affected_users: few
reproduction_steps: "Unknown - happens randomly"
```

**Output:**
```yaml
severity: MEDIUM
type: PERFORMANCE
reproducible: INTERMITTENT
affected_users: FEW
decision:
  workflow: SPIKE
  urgency: DAYS
  reason: "Cannot reproduce - needs investigation"
confidence: MEDIUM
```

---

**Related Skills:**
- `bug-impact-analyzer` - Analyzes bug impact depth
- `production-impact-assessor` - Assesses production severity
- `minimal-fix-planner` - Plans minimal bug fix
