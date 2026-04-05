---
name: hotfix-incident-documenter
description: Generates incident report and post-incident documentation for production hotfixes, providing audit trail and enabling systematic improvement.
---

# Hotfix Incident Documenter

## Quick Example

**Input:** Incident: 100% order failures 14:19-14:51 UTC, root cause: null Carrier, hotfix: null guard added, 312 affected orders
**Output:** Incident report, timeline document, executive summary (non-technical), lessons learned, proper fix ticket details
**Time:** 2-3 minutes

---

## Purpose
Generates incident report and post-incident documentation for production hotfixes, providing audit trail and enabling systematic improvement.

## Input

```yaml
input:
  incident_title: <short descriptive title>
  incident_timeline:
    - timestamp: <ISO>
      event: <what happened>
  root_cause: <technical root cause>
  impact:
    users_affected: <count or percentage>
    duration_minutes: <how long the incident lasted>
    features_affected: [<list>]
    data_affected: true|false
  hotfix_applied:
    description: <what was changed>
    files_changed: [<list>]
    deployed_by: <name or role>
    deployment_time: <ISO>
  severity: CRITICAL|HIGH
  ticket_id: <incident ticket ID>
```

## Output

```yaml
output:
  incident_report:
    title: <formatted title>
    severity: <level>
    incident_id: <INC-{id}>
    duration_minutes: <count>
    users_affected: <count>
    status: RESOLVED
    executive_summary: <2-3 sentence non-technical summary>
    timeline: [<formatted timeline>]
    root_cause: <technical explanation>
    hotfix_summary: <what was done>
    immediate_actions: [<what was done during incident>]
    follow_up_actions: [<what needs to happen next>]
  lessons_learned:
    what_went_well: [<list>]
    what_went_poorly: [<list>]
    action_items:
      - action: <specific improvement>
        owner: <role>
        deadline: <ISO date>
  proper_fix_ticket:
    title: <title for permanent fix ticket>
    description: <what needs to be done properly>
    priority: HIGH|MEDIUM
    estimated_effort: <story points or days>
  confidence: HIGH|MEDIUM|LOW
```

## DO:
✅ Write the executive summary in non-technical language — it's for management
✅ Include exact timestamps in the timeline — audit trail requires precision
✅ Separate immediate actions (during incident) from follow-up actions (after)
✅ Be honest in lessons learned — avoid blame, focus on systemic improvements
✅ Create a proper fix ticket — the hotfix is temporary, proper fix is required

## DON'T:
❌ Omit the executive summary — non-technical stakeholders need it
❌ Write lessons learned as blame — focus on process and system improvements
❌ Forget to quantify impact — "some users affected" is not acceptable
❌ Skip the proper fix ticket — hotfixes are band-aids, not permanent solutions
❌ Delay documentation — memory fades; document within 2 hours of resolution

## Error Conditions

**IF timeline is incomplete:**
```
1. Reconstruct from available data: logs, deployment records, Slack/Teams messages
2. Flag: TIMELINE_RECONSTRUCTED — some timestamps may be approximate
```

**IF user impact cannot be quantified:**
```
1. Estimate from: error rate × session count during incident window
2. Flag: IMPACT_ESTIMATED — actual user count may differ
```

## Processing Steps

1. Generate incident ID: `INC-{YYYYMMDD}-{sequential}`.
2. Write executive summary (2-3 non-technical sentences): what failed, who was affected, how it was resolved.
3. Format timeline: `{timestamp} — {event}` grouped by phase (Detection, Diagnosis, Fix, Verification).
4. Document root cause: what was wrong, why it was deployed, what triggered it.
5. Lessons learned: what went well, what went poorly — factual, no blame; create action items for each gap.
6. Create proper fix ticket: hotfix is temporary — plan permanent fix with full test coverage.

## Example

**Input:**
```yaml
incident_title: "100% Order Submission Failures — ShippingCalculator NullReferenceException"
incident_timeline:
  - {timestamp: "2026-04-05T14:19:00Z", event: "Deployment of v2.14.1 completed"}
  - {timestamp: "2026-04-05T14:23:00Z", event: "First NullReferenceException errors in production logs"}
  - {timestamp: "2026-04-05T14:26:00Z", event: "Customer support escalation — orders failing"}
  - {timestamp: "2026-04-05T14:35:00Z", event: "Engineering paged — incident declared CRITICAL"}
  - {timestamp: "2026-04-05T14:45:00Z", event: "Root cause identified — null Carrier null guard missing"}
  - {timestamp: "2026-04-05T14:51:00Z", event: "Hotfix deployed — error rate returns to 0%"}
root_cause: "ShippingCalculator.Calculate() removed null guard for Carrier during refactor in commit a3f92b1. Orders with null Carrier (draft orders) triggered NullReferenceException."
impact:
  users_affected: 312
  duration_minutes: 32
  features_affected: ["Order submission", "Checkout"]
  data_affected: false
hotfix_applied:
  description: "Added null guard: if (carrier == null) return DefaultRate;"
  files_changed: ["ShippingCalculator.cs"]
  deployed_by: "Ahmed Khan"
  deployment_time: "2026-04-05T14:51:00Z"
severity: CRITICAL
ticket_id: "INC-4521"
```

**Output:**
```yaml
incident_report:
  title: "INC-20260405-001: Order Submission Unavailable — ShippingCalculator Failure"
  severity: CRITICAL
  incident_id: "INC-20260405-001"
  duration_minutes: 32
  users_affected: 312
  status: RESOLVED
  executive_summary: "On April 5, 2026, the order submission feature was completely unavailable for 32 minutes due to a software defect introduced in the v2.14.1 release. Approximately 312 customers were unable to complete orders during this period. The defect was identified and fixed within 32 minutes of onset, and no customer data was lost."
  timeline:
    - "14:19 UTC — v2.14.1 deployed to production"
    - "14:23 UTC — First errors detected in production logs"
    - "14:26 UTC — Customer support escalation received"
    - "14:35 UTC — Engineering paged, CRITICAL incident declared"
    - "14:45 UTC — Root cause identified"
    - "14:51 UTC — Hotfix deployed, error rate 0%, incident resolved"
  root_cause: "ShippingCalculator.Calculate() attempted to access carrier.RateCode without a null check. A null guard that previously existed was accidentally removed during a refactor in commit a3f92b1. Draft orders with no carrier assigned triggered the NullReferenceException on every call."
  hotfix_summary: "Added two-line null guard: 'if (carrier == null) return DefaultRate;' before carrier property access."
  immediate_actions:
    - "Declared CRITICAL incident at 14:35"
    - "Identified affected deployment at 14:39"
    - "Developed and tested hotfix at 14:45-14:50"
    - "Deployed hotfix at 14:51"
  follow_up_actions:
    - "Reschedule/retry affected orders (312 orders to process)"
    - "Conduct postmortem within 48 hours"
    - "Add unit test for null carrier scenario"
lessons_learned:
  what_went_well:
    - "Root cause identified quickly (22 minutes) using production logs"
    - "Hotfix was minimal (2 lines) and low risk"
    - "Team responded promptly once paged"
  what_went_poorly:
    - "9-minute gap between first error (14:23) and customer support escalation (14:26) — monitoring alert not triggered"
    - "Null guard removed in code review without detection"
    - "No unit test for null carrier scenario existed"
  action_items:
    - action: "Configure PagerDuty alert for error rate >5% sustained >2 minutes"
      owner: "Infrastructure team"
      deadline: "2026-04-12"
    - action: "Add unit test: ShippingCalculator_Calculate_WhenCarrierNull"
      owner: "Developer (PROJ-4521 assignee)"
      deadline: "2026-04-07"
    - action: "Add null guard review item to code review checklist"
      owner: "Team Lead"
      deadline: "2026-04-10"
proper_fix_ticket:
  title: "PROPER FIX: Add comprehensive null guards and unit tests to ShippingCalculator [follows INC-20260405-001]"
  description: "The hotfix addressed the immediate symptom. Proper fix: add null guards for all navigation properties in ShippingCalculator and add full unit test coverage for null input scenarios."
  priority: HIGH
  estimated_effort: "1 day"
confidence: HIGH
```

---

**Related Skills:**
- `postmortem-planner` - Plans the postmortem meeting using this incident document as input
- `root-cause-recorder` - Records root cause in structured format for pattern tracking
- `proper-fix-planner` - Plans the permanent fix referenced in the follow-up actions
- `bug-fix-documenter` - Generates the technical bug fix documentation
