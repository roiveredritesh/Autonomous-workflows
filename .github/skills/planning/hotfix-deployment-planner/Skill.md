---
name: hotfix-deployment-planner
description: Plans the deployment sequence for a hotfix including staged rollout, health monitoring, and rollback triggers to ensure safe production deployment.
---

# Hotfix Deployment Planner

## Quick Example

**Input:** Null guard hotfix for ShippingCalculator, 3 IIS servers, rollback: redeploy previous package
**Output:** 5-step deployment plan with staged rollout (1 server → monitor 5min → all servers), monitoring criteria, rollback triggers, estimated 20-minute total deployment
**Time:** 2-3 minutes

---

## Purpose
Plans the deployment sequence for a hotfix including staged rollout, health monitoring, and rollback triggers to ensure safe production deployment.

## Input

```yaml
input:
  hotfix_description: <what the hotfix does>
  affected_servers: <count or list of production servers>
  deployment_method: IIS_RECYCLE|APP_POOL_RESTART|XCOPY|CI_CD_PIPELINE|AZURE_DEPLOYMENT
  rollback_procedure: <how to rollback — redeploy previous, git revert, IIS rollback>
  monitoring_available: [<what monitoring is in place — Application Insights, IIS logs, custom>]
  health_check_url: <URL to verify application health after deploy>
  peak_traffic_times: <when to avoid deployment>
```

## Output

```yaml
output:
  deployment_plan:
    pre_deployment:
      - step: <action>
        responsible: OPS|DEV|BOTH
        estimated_time_minutes: <n>
    staged_rollout:
      - phase: <1..n>
        servers: <count or names>
        action: <what to deploy>
        monitoring_period_minutes: <n>
        success_criteria: [<what must be true to proceed>]
        abort_criteria: [<what triggers rollback>]
    post_deployment:
      - step: <action>
        responsible: OPS|DEV|BOTH
        estimated_time_minutes: <n>
  rollback_plan:
    trigger_conditions: [<what causes rollback>]
    rollback_steps: [<exact steps>]
    estimated_rollback_time_minutes: <n>
    rollback_validation: [<how to verify rollback succeeded>]
  monitoring_plan:
    metrics: [<what to watch>]
    duration_minutes: <how long to monitor after full deploy>
    alert_thresholds: [<condition: action>]
  communication_plan:
    pre_deploy_notification: <who and how to notify>
    status_updates: [<frequency and recipients>]
    resolution_notification: <who gets the "all clear">
  total_estimated_time_minutes: <sum>
  confidence: HIGH|MEDIUM|LOW
```

## DO:
✅ Always deploy to one server first and monitor before rolling to all servers
✅ Define explicit abort criteria — don't leave go/no-go to judgment under pressure
✅ Verify health check URL returns 200 after each server deployment
✅ Keep rollback procedure simple enough to execute under stress
✅ Notify stakeholders before, during, and after — no surprises

## DON'T:
❌ Deploy to all servers simultaneously — staged rollout limits blast radius
❌ Skip the pre-deployment health check — verify baseline before changing anything
❌ Monitor for less than 5 minutes per phase — issues may take time to manifest
❌ Deploy during peak traffic hours — wait for off-peak even for critical hotfixes
❌ Leave rollback procedure vague — it must be executable in <5 minutes

## Error Conditions

**IF no staging environment exists:**
```
1. Treat first production server as staging with minimal traffic
2. Flag: NO_STAGING — first server acts as canary; extra monitoring required
3. Reduce phase 1 server count to 1 and extend monitoring to 15 minutes
```

**IF CI/CD pipeline is unavailable:**
```
1. Plan manual deployment steps
2. Flag: MANUAL_DEPLOY — extra care required; use deployment checklist
3. Two-person verification recommended for all manual steps
```

**IF rollback procedure is unknown:**
```
1. STOP — do not plan deployment without rollback
2. Return: ROLLBACK_REQUIRED — define rollback before proceeding with deployment
```

## Processing Steps

1. **Pre-Deployment Phase:** List all tasks before first server deploy: backup current deployment package, verify rollback procedure is tested, notify stakeholders, drain or reduce traffic if possible, verify health check baseline (all servers healthy).

2. **Staged Rollout Design:** Phase 1: 1 server (or 1/3 of total). Monitor for 5-10 minutes. Success criteria: error rate = 0, response time normal, health check passing. Phase 2: remaining servers. Monitor 10-15 minutes.

3. **Success/Abort Criteria:** Per phase, define specific numeric thresholds: abort if error rate >1%, response time >2x baseline, health check fails, any CRITICAL log entries appear.

4. **Post-Deployment Phase:** Tasks after all servers deployed: update monitoring dashboards, send resolution notification, tag git release, update incident ticket status.

5. **Rollback Plan:** Trigger conditions (same as abort criteria). Steps: specific commands or pipeline triggers to roll back. Estimated time. Validation: same health criteria as deployment success.

6. **Monitoring Plan:** Metrics to watch: error rate (Application Insights or IIS logs), response time (P50/P95), health check status, key business metric (orders processed per minute).

7. **Communication Plan:** Pre-deploy: ops + dev lead. During: status every 10 minutes to incident channel. Post: all-clear to stakeholders + customer support if user-facing impact.

## Example

**Input:**
```yaml
hotfix_description: "Add null guard for Carrier in ShippingCalculator — fixes 100% order submission failures"
affected_servers: 3
deployment_method: CI_CD_PIPELINE
rollback_procedure: "Trigger 'Deploy v2.14.1' pipeline in CI/CD — redeploys previous package"
monitoring_available: ["Application Insights", "IIS logs", "Custom health endpoint"]
health_check_url: "https://app.aajlogistics.com/health"
peak_traffic_times: "09:00-17:00 local time"
```

**Output:**
```yaml
deployment_plan:
  pre_deployment:
    - {step: "Verify all 3 servers healthy at /health endpoint", responsible: OPS, estimated_time_minutes: 2}
    - {step: "Confirm rollback pipeline 'Deploy v2.14.1' is tested and ready", responsible: DEV, estimated_time_minutes: 3}
    - {step: "Notify: #incident-channel — hotfix deployment starting", responsible: DEV, estimated_time_minutes: 1}
  staged_rollout:
    - phase: 1
      servers: "1 of 3 (server-prod-01)"
      action: "Trigger CI/CD hotfix pipeline for server-prod-01"
      monitoring_period_minutes: 7
      success_criteria:
        - "Error rate = 0% (was 100% before hotfix)"
        - "Health check returns 200"
        - "Orders can be submitted (S1 smoke test)"
      abort_criteria:
        - "Any NullReferenceException in logs"
        - "Error rate >1%"
        - "Health check returns non-200"
    - phase: 2
      servers: "Remaining 2 (server-prod-02, server-prod-03)"
      action: "Trigger CI/CD hotfix pipeline for remaining servers"
      monitoring_period_minutes: 15
      success_criteria:
        - "Error rate = 0% across all servers"
        - "Order submission rate returns to pre-incident baseline"
      abort_criteria:
        - "Error rate >0.5% for >2 minutes"
  post_deployment:
    - {step: "Send all-clear notification to stakeholders", responsible: DEV, estimated_time_minutes: 2}
    - {step: "Update incident ticket to RESOLVED", responsible: DEV, estimated_time_minutes: 1}
    - {step: "Tag release v2.14.2 in git", responsible: DEV, estimated_time_minutes: 2}
rollback_plan:
  trigger_conditions:
    - "Phase 1 abort criteria met"
    - "Phase 2 error rate >0.5% sustained >2 minutes"
    - "Manual decision by incident commander"
  rollback_steps:
    - "Trigger CI/CD pipeline: Deploy v2.14.1 to all servers"
    - "Verify health checks return 200 on all servers"
    - "Verify error rate returns to 0 (incident started at 14:23)"
  estimated_rollback_time_minutes: 8
  rollback_validation: ["All 3 servers at /health return 200", "Error rate in Application Insights = 0%"]
monitoring_plan:
  metrics: ["Error rate (Application Insights)", "Orders per minute (business metric)", "P95 response time"]
  duration_minutes: 30
  alert_thresholds:
    - "Error rate >1%: ABORT rollback immediately"
    - "Orders/min <50% of baseline for >5min: INVESTIGATE"
communication_plan:
  pre_deploy_notification: "#incident-channel, #ops, on-call pager"
  status_updates: ["Every 10 minutes to #incident-channel during rollout"]
  resolution_notification: "#incident-channel, customer-support, management-distro"
total_estimated_time_minutes: 33
confidence: HIGH
```

---

**Related Skills:**
- `hotfix-branch-creator` - Plans the git branch strategy that feeds into deployment
- `production-verification-checker` - Verifies production health after deployment completes
- `hotfix-validator` - Validates the hotfix is safe to deploy
- `rollback-plan-generator` - Generates detailed rollback documentation
