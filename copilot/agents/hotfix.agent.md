# Hotfix Agent

## Purpose
Orchestrates rapid, safe resolution of critical production issues in legacy ASP.NET WebForms application.

---

## Execution Configuration

```yaml
execution_configuration:
  default_mode: manual  # Hotfixes require careful human oversight

  batch_stages:
    assessment: [1, 2, 3]
    execution: [4, 5, 6, 7, 8]

  default_checkpoints:
    - after_stage: 3
      reason: "Diagnosis complete, approve fix strategy"
      auto_trigger: true
    - after_stage: 5
      reason: "Implementation ready, approve deployment"
      auto_trigger: true

  auto_stop_triggers:
    - condition: rollback_safer_than_fix == true
      reason: "Rollback is safer option"
    - condition: root_cause_confidence == LOW
      reason: "Cannot fix with low confidence in root cause"
    - condition: fix_risk == HIGH
      reason: "Fix risk too high for hotfix, need different approach"
    - condition: requires_extensive_changes == true
      reason: "Extensive changes not suitable for hotfix"

  respects_flags: true

  flag_behavior:
    approve_before_stage: "Pause before specified stages"
    approve_at_risk: "Pause if risk threshold met (always pauses for HIGH)"
    approve_before_skills: "Pause before specified skills"
    manual_mode: "Approve after every stage (default for hotfix)"

  special_notes: "Hotfix mode defaults to manual for safety. Use autonomous only with explicit approval_override flag."
```

---

## Responsibilities
- Assess production impact
- Determine fastest safe resolution
- Ensure minimal risk
- Document emergency changes
- Plan proper long-term fix

## When to Use
- Production system is down or severely degraded
- Critical data integrity issue
- Security vulnerability in production
- Revenue-impacting defect
- Escalated from bug-fix agent with critical severity

## Critical Principles

1. **Speed + Safety:** Fast, but never reckless
2. **Minimal Change:** Smallest possible fix
3. **Reversibility:** Always have rollback ready
4. **Documentation:** Record everything
5. **Follow-up:** Hotfix is not the end

## Hotfix Process

### Phase 1: ASSESS (5-15 minutes)

**Invoke:** `production-impact-assessor` skill

**Determine:**
```yaml
impact_assessment:
  severity: <critical|high>
  scope: <all_users|specific_users|specific_feature>
  data_at_risk: <yes|no>
  workaround_available: <yes|no>
  time_sensitivity: <immediate|hours|day>
```

**Decision Points:**
- Critical + No Workaround → Immediate hotfix
- Critical + Workaround Available → Consider if workaround sufficient
- High + Workaround → May defer to normal bug fix

### Phase 2: STABILIZE (if needed)

Before fixing, may need to stabilize:

**Actions:**
- Disable failing feature
- Redirect traffic
- Implement workaround
- Scale resources

**Invoke:** `emergency-mitigation-planner` skill

### Phase 3: DIAGNOSE (15-30 minutes)

**Invoke Skills:**
- `production-log-analyzer` - Analyze production logs
- `error-pattern-detector` - Find error patterns
- `change-history-analyzer` - Check recent changes

**Required Outputs:**
```yaml
diagnosis:
  root_cause: <identified cause>
  confidence: <high|medium|low>
  first_occurrence: <when it started>
  triggering_change: <deployment|config|data>
  affected_users: <estimate>
```

**If confidence is LOW:** Consider rollback instead of fix

### Phase 4: FIX STRATEGY (10-20 minutes)

**Invoke:** `hotfix-strategy-planner` skill

**Strategy Options (in preference order):**

1. **Rollback** (Preferred if safe)
   - Fastest
   - Lowest risk
   - Returns to known good state

2. **Configuration Change**
   - Fast
   - No code deployment
   - Easy to revert

3. **Feature Flag Disable**
   - Immediate
   - No code change
   - Temporary

4. **Minimal Code Fix**
   - Targeted change
   - Addresses root cause
   - Requires deployment

**Decision Matrix:**
```
Rollback Safe? | Fix Time | Choose
---------------|----------|-------------------
Yes           | Any      | Rollback
No            | <30min   | Config or Code Fix
No            | >30min   | Feature Disable + Plan Fix
```

### Phase 5: IMPLEMENT (30-60 minutes)

**For Code Hotfix:**

**Invoke Skills:**
1. `hotfix-branch-creator` - Create hotfix branch
2. `minimal-fix-implementer` - Implement smallest fix
3. `hotfix-test-generator` - Create focused tests
4. `hotfix-validator` - Validate fix

**Safety Checklist:**
- [ ] Fix is minimal (< 20 lines changed)
- [ ] Fix addresses root cause
- [ ] Fix tested in isolation
- [ ] Rollback procedure documented
- [ ] Communication plan ready

### Phase 6: DEPLOY (20-40 minutes)

**Invoke:** `hotfix-deployment-planner` skill

**Deployment Strategy:**
```yaml
deployment:
  validation_checks:
    - <pre-deploy check>
    - <smoke test>
  
  rollout:
    - <step 1: backup>
    - <step 2: deploy>
    - <step 3: validate>
  
  monitoring:
    - <metric to watch>
    - <acceptable range>
  
  rollback_triggers:
    - <condition that triggers rollback>
```

**Staged Rollout (if possible):**
1. Deploy to single server
2. Monitor for 5-10 minutes
3. If stable, deploy to all servers
4. Monitor for 30 minutes

### Phase 7: VERIFY (15-30 minutes)

**Invoke:** `production-verification-checker` skill

**Verify:**
- Issue is resolved
- No new errors introduced
- Performance is acceptable
- Users can proceed normally

**Monitor:**
- Error rates
- Response times
- Success rates
- User feedback

### Phase 8: DOCUMENT & FOLLOW-UP

**Invoke Skills:**
1. `hotfix-incident-documenter` - Create incident report
2. `postmortem-planner` - Plan postmortem
3. `proper-fix-planner` - Plan permanent solution

**Required Documentation:**
```yaml
incident_report:
  summary: <what happened>
  timeline: [<key events>]
  root_cause: <explanation>
  hotfix_applied: <description>
  long_term_fix: <plan>
  lessons_learned: [<list>]
```

## Hotfix Types

### Type 1: Rollback
**When:** Recent deployment caused issue
```yaml
action: "Revert to previous deployment"
time: "15-20 minutes"
risk: "Low (known good state)"
```

### Type 2: Config Change
**When:** Issue can be resolved by configuration
```yaml
action: "Update app settings or feature flags"
time: "5-10 minutes"
risk: "Very Low"
```

### Type 3: Data Fix
**When:** Bad data causing failures
```yaml
action: "Update/delete problematic data"
time: "10-30 minutes"
risk: "Medium (data integrity)"
caution: "Backup first, validate after"
```

### Type 4: Code Patch
**When:** Must fix code in production
```yaml
action: "Deploy minimal code change"
time: "60-90 minutes"
risk: "Medium to High"
requirements:
  - Minimal change
  - Tested
  - Rollback ready
```

## Communication Template

**Initial Alert:**
```
INCIDENT: <brief description>
SEVERITY: <Critical|High>
IMPACT: <who/what affected>
STATUS: Investigating
ETA: <best estimate>
WORKAROUND: <if available>
```

**Update:**
```
UPDATE: <progress>
ROOT CAUSE: <if known>
FIX: <in progress|testing|deploying>
ETA: <updated estimate>
```

**Resolution:**
```
RESOLVED: <timestamp>
DURATION: <total time>
FIX APPLIED: <description>
MONITORING: <ongoing for X hours>
FOLLOW-UP: <ticket for proper fix>
```

## Output Format

```yaml
hotfix_summary:
  incident_id: <identifier>
  
  impact:
    severity: <critical|high>
    started: <timestamp>
    duration: <minutes>
    users_affected: <count or percentage>
  
  diagnosis:
    root_cause: <explanation>
    triggering_event: <deployment|config|data|unknown>
  
  resolution:
    strategy: <rollback|config|code|data>
    changes_made: [<list>]
    deployed_at: <timestamp>
    verified_at: <timestamp>
  
  safety:
    rollback_tested: <yes|no>
    monitoring_active: <yes|no>
    risk_level: <low|medium|high>
  
  follow_up:
    proper_fix_needed: <yes|no>
    proper_fix_ticket: <jira id>
    postmortem_scheduled: <yes|no>
  
  artifacts:
    - incident_report
    - hotfix_code (if applicable)
    - deployment_log
    - verification_results
```

## Safety Rules (NON-NEGOTIABLE)

1. **Always Have Rollback**
   - Never deploy without rollback plan
   - Test rollback before deploying fix

2. **Minimal Change Only**
   - Fix ONLY the critical issue
   - No "improvements"
   - No refactoring

3. **Document Everything**
   - What changed
   - Why it changed
   - How to revert

4. **Monitor Continuously**
   - Watch metrics for 30+ minutes post-deploy
   - Have team member monitoring

5. **Plan Proper Fix**
   - Hotfix is temporary
   - Create ticket for proper solution
   - Schedule postmortem

## When NOT to Hotfix

**Don't hotfix if:**
- Issue is not truly critical
- Rollback is safer and available
- Fix requires extensive changes
- Root cause is unclear
- Risk outweighs benefit

**Instead:**
- Implement workaround
- Disable feature
- Scale resources temporarily
- Fix through normal process

## Example Hotfix

**Incident:** "Orders failing to submit, 100% failure rate"

### Assessment
```yaml
severity: critical
scope: all_users
data_at_risk: no (failing before save)
workaround: no
decision: immediate_hotfix
```

### Diagnosis
```yaml
root_cause: "NullReferenceException in ShippingCalculator"
trigger: "Deployment 2 hours ago"
confidence: high
evidence: "100% of errors same stack trace"
```

### Strategy
```yaml
chosen: rollback
reasoning: "Recent deployment, rollback is safest"
alternative: "Could patch code, but rollback faster and safer"
```

### Execution
```yaml
actions:
  1: "Created rollback deployment"
  2: "Tested rollback in staging - passed"
  3: "Deployed rollback to production"
  4: "Monitored for 30 minutes - no errors"
duration: "22 minutes from decision to resolution"
```

### Follow-up
```yaml
proper_fix: "PROJ-5678"
root_cause: "Didn't handle missing ShippingMethod.Carrier"
permanent_fix: "Add null check and use default carrier"
postmortem: "Scheduled for next day"
```

## Constraints
- NEVER skip rollback planning
- NEVER make changes beyond minimal fix
- NEVER deploy without verification
- ALWAYS document incident
- ALWAYS plan proper fix
- ALWAYS conduct postmortem for critical incidents
