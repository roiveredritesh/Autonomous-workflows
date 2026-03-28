---
skill: hotfix-strategy-planner
version: 2.0.0
category: planning
complexity: medium
estimated_time: 2-4 minutes
priority: critical
last_updated: 2026-01-18
---

# Hotfix Strategy Planner

## Quick Example

**Input:** Orders failing - deployment 2h ago caused issue
**Output:** ROLLBACK strategy (fastest, safest) - 15min total time
**Time:** 3 minutes

---

## Purpose
Determines the fastest safe way to resolve critical production issues by evaluating rollback, config changes, or minimal code fixes.

## Input

```yaml
hotfix:
  issue: <problem description>
  root_cause: <identified cause>
  confidence: HIGH|MEDIUM|LOW
  time_available: <minutes>
```

## Output

```yaml
hotfix_strategy:
  chosen_strategy: rollback|config|feature_disable|code_patch|data_fix

  reasoning: <why this approach>

  implementation_time: <minutes>
  risk_level: LOW|MEDIUM|HIGH

  steps: [<high-level actions>]
  validation: [<how to verify>]
  rollback_plan: <if strategy fails>

  confidence: HIGH|MEDIUM|LOW
```

## Strategy Options (Priority Order)

### 1. ROLLBACK (Preferred)
- **When:** Recent deployment caused issue
- **Time:** 15-20 minutes
- **Risk:** LOW (known good state)
- **Best for:** Clear deployment trigger

### 2. CONFIGURATION CHANGE
- **When:** Settings can resolve issue
- **Time:** 5-10 minutes
- **Risk:** VERY LOW
- **Best for:** Feature flags, app settings

### 3. FEATURE DISABLE
- **When:** Can disable problematic feature
- **Time:** 5-15 minutes
- **Risk:** LOW
- **Best for:** Temporary mitigation

### 4. CODE PATCH
- **When:** Must fix code, can't rollback
- **Time:** 60-90 minutes
- **Risk:** MEDIUM-HIGH
- **Best for:** Minimal, targeted fix

### 5. DATA FIX
- **When:** Bad data causing failures
- **Time:** 10-30 minutes
- **Risk:** MEDIUM (data integrity)
- **Best for:** Known data issue

## Decision Matrix

```
Rollback  | Root Cause  | Time     | Choose
Available | Confidence  | Pressure |
----------|-------------|----------|------------------
YES       | Any         | Any      | ROLLBACK
NO        | HIGH        | <30min   | CODE PATCH or CONFIG
NO        | MEDIUM/LOW  | Any      | SPIKE + FEATURE DISABLE
NO        | HIGH        | >30min   | FEATURE DISABLE + PLAN FIX
```

## DO:
✅ Prefer rollback when available
✅ Choose fastest safe option
✅ Verify root cause confidence
✅ Plan rollback for chosen strategy
✅ Test in staging if possible
✅ Document decision reasoning

## DON'T:
❌ Choose code patch over rollback
❌ Proceed with LOW root cause confidence
❌ Skip validation planning
❌ Deploy without rollback plan
❌ Make extensive changes
❌ Skip stakeholder communication

## Error Conditions

**IF root cause confidence LOW:**
```
1. STOP - cannot hotfix safely
2. Options:
   - Feature disable (temporary)
   - Spike investigation (understand first)
   - Rollback (if available)
3. Do NOT proceed with code patch
```

**IF no safe strategy:**
```
1. Escalate immediately
2. Implement workaround
3. Scale resources
4. Communicate delays
5. Plan proper investigation
```

## Example 1: Choose Rollback

**Input:**
```yaml
issue: "Orders failing 100%"
root_cause: "Deployment 2 hours ago"
confidence: HIGH
time_available: immediate
```

**Output:**
```yaml
chosen_strategy: rollback

reasoning: "Recent deployment caused issue - rollback is fastest and safest"

implementation_time: 15 minutes
risk_level: LOW

steps:
  - "Create rollback deployment"
  - "Test in staging (5 min)"
  - "Deploy to production"
  - "Monitor for 30 min"

validation:
  - "Orders process successfully"
  - "No errors in logs"
  - "Response times normal"

rollback_plan: "If rollback fails, feature disable order submission"

confidence: HIGH
```

## Example 2: Choose Feature Disable

**Input:**
```yaml
issue: "New feature causing crashes"
root_cause: "Feature interaction unclear"
confidence: MEDIUM
```

**Output:**
```yaml
chosen_strategy: feature_disable

reasoning: "Root cause unclear - disable feature while investigating"

implementation_time: 10 minutes
risk_level: LOW

steps:
  - "Set feature flag to disabled"
  - "Clear application cache"
  - "Verify feature disabled"
  - "Monitor stability"

validation:
  - "No more crashes"
  - "Core functionality works"

rollback_plan: "Re-enable if needed (very low risk)"

confidence: MEDIUM
```

---

**Related Skills:**
- `emergency-mitigation-planner` - For immediate stabilization
- `production-impact-assessor` - For severity assessment
- `rollback-plan-generator` - For detailed rollback planning
