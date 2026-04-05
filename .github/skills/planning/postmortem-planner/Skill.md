---
name: postmortem-planner
description: Plans postmortem meetings and action items after production incidents to drive systematic improvement and prevent recurrence.
---

# Postmortem Planner

## Quick Example

**Input:** CRITICAL incident INC-20260405-001, 32-minute outage, 312 users affected, root cause: null guard removed in refactor
**Output:** Postmortem agenda (60 min), discussion topics, 5 action items with owners and deadlines, follow-up schedule
**Time:** 2-3 minutes

---

## Purpose
Plans postmortem meetings and action items after production incidents to drive systematic improvement and prevent recurrence.

## Input

```yaml
input:
  incident_summary: <reference to hotfix-incident-documenter output or brief summary>
  root_cause: <technical root cause>
  incident_severity: CRITICAL|HIGH
  affected_teams: [<list of teams involved>]
  time_to_detect_minutes: <how long until incident was noticed>
  time_to_resolve_minutes: <total incident duration>
  contributing_factors: [<list of factors that enabled the incident>]
  scheduled_date: <when the postmortem will be held>
```

## Output

```yaml
output:
  postmortem_meeting:
    title: <formatted meeting title>
    scheduled: <ISO datetime>
    duration_minutes: <recommended duration>
    facilitator_role: <who should lead>
    attendees: [<required roles>]
  agenda:
    - time_minutes: <allocated>
      topic: <agenda item>
      objective: <what to achieve in this slot>
      owner: <who leads this section>
  discussion_topics:
    - topic: <question or discussion point>
      category: DETECTION|RESPONSE|ROOT_CAUSE|PREVENTION|PROCESS
      priority: HIGH|MEDIUM|LOW
  action_items:
    - action: <specific, measurable action>
      category: MONITORING|TESTING|PROCESS|INFRASTRUCTURE|DOCUMENTATION
      owner: <role>
      deadline: <ISO date>
      success_criteria: <how to know it's complete>
  follow_up:
    next_review_date: <ISO date>
    metrics_to_track: [<what to measure to verify improvement>]
  blameless_reminder: <statement reinforcing blameless culture>
  confidence: HIGH|MEDIUM|LOW
```

## DO:
✅ Enforce blameless culture — focus on systems and processes, not individuals
✅ Limit postmortem to 60-90 minutes — longer meetings lose focus and energy
✅ Assign specific owners to each action item — unowned items don't get done
✅ Set concrete deadlines — "soon" or "next sprint" is not a deadline
✅ Schedule a follow-up review to verify action items are completed

## DON'T:
❌ Assign blame or name individuals as root causes
❌ Skip action items — postmortem without actions is just a retrospective
❌ Create more than 5-7 action items — too many means none get done
❌ Invite unnecessary attendees — keep to affected teams only
❌ Hold postmortem more than 48 hours after resolution — details fade

## Error Conditions

**IF incident was minor (LOW severity):**
```
1. Recommend async postmortem (written document) instead of meeting
2. Reduce to 3 action items maximum
3. Flag: LIGHTWEIGHT_POSTMORTEM — formal meeting may not be proportional
```

**IF team is unavailable within 48 hours:**
```
1. Hold a 15-minute preliminary discussion to capture immediate memories
2. Schedule full postmortem within 1 week
3. Distribute incident document for async comment before meeting
```

## Processing Steps

1. **Meeting Setup:** Title: "Postmortem: {incident title} — {date}". Duration: 60 min for CRITICAL, 45 min for HIGH. Facilitator: engineering manager or senior dev not involved in the incident. Attendees: incident responders, team leads of affected systems, QA lead.

2. **Agenda Design:** Fixed structure: (1) Timeline review 15min, (2) Impact review 5min, (3) Root cause deep dive 20min, (4) What went well 10min, (5) What went poorly 10min, (6) Action items 15min, (7) Wrap up 5min.

3. **Discussion Topics:** Generate 5-7 questions covering: detection (how was it found, how can we find it faster), response (was the escalation path correct), root cause (how did this happen), prevention (what would have prevented this), process (what process gaps exist).

4. **Action Item Generation:** For each contributing factor: create one action item. Each action: specific verb + measurable outcome + owner role + deadline. Maximum 7 action items total.

5. **Success Criteria:** For each action item: define a testable condition. "Add unit test" → "Unit test exists in repo and passes in CI". "Add monitoring alert" → "Alert fires in test environment for simulated failure".

6. **Follow-up Schedule:** For CRITICAL: review action items in 1 week, progress check in 2 weeks, final review in 1 month. Track in incident ticket.

7. **Blameless Reminder:** Include explicit statement in agenda: "We are investigating systems and processes, not assigning blame. All team members acted in good faith with the information available."

## Example

**Input:**
```yaml
incident_summary: "INC-20260405-001: 100% order submission failures for 32 minutes, 312 users affected"
root_cause: "Null guard removed during refactor in commit a3f92b1, deployed in v2.14.1"
incident_severity: CRITICAL
affected_teams: ["Engineering", "QA", "Operations"]
time_to_detect_minutes: 4
time_to_resolve_minutes: 32
contributing_factors:
  - "No unit test for null carrier scenario"
  - "Monitoring alert not configured for error rate spike"
  - "Code reviewer did not detect null guard removal"
scheduled_date: "2026-04-07T10:00:00"
```

**Output:**
```yaml
postmortem_meeting:
  title: "Postmortem: INC-20260405-001 — Order Submission Outage (2026-04-05)"
  scheduled: "2026-04-07T10:00:00"
  duration_minutes: 60
  facilitator_role: "Engineering Manager (or Senior Dev not involved in incident)"
  attendees: ["Incident lead", "Developer (a3f92b1 author)", "Team Lead", "QA Lead", "Ops on-call"]
agenda:
  - {time_minutes: 5, topic: "Blameless culture reminder + ground rules", objective: "Set psychological safety for honest discussion", owner: "Facilitator"}
  - {time_minutes: 15, topic: "Timeline walkthrough", objective: "Shared understanding of what happened and when", owner: "Incident lead"}
  - {time_minutes: 5, topic: "Impact review", objective: "Quantify user and business impact", owner: "Facilitator"}
  - {time_minutes: 20, topic: "Root cause deep dive", objective: "Understand why this happened at all levels (code, process, system)", owner: "Team"}
  - {time_minutes: 5, topic: "What went well", objective: "Identify and reinforce effective practices", owner: "Facilitator"}
  - {time_minutes: 5, topic: "What went poorly", objective: "Identify systemic gaps without blame", owner: "Facilitator"}
  - {time_minutes: 5, topic: "Action items", objective: "Agree on specific, owned, time-bound improvements", owner: "Facilitator"}
discussion_topics:
  - {topic: "Why did the monitoring alert not fire for 4 minutes after first errors?", category: DETECTION, priority: HIGH}
  - {topic: "What would make code review catch null guard removals automatically?", category: PREVENTION, priority: HIGH}
  - {topic: "Why was there no unit test for the null carrier scenario?", category: TESTING, priority: HIGH}
  - {topic: "How can we make the rollback process faster (target <15min)?", category: RESPONSE, priority: MEDIUM}
action_items:
  - action: "Configure Application Insights alert: error rate >2% for >2 minutes → PagerDuty CRITICAL"
    category: MONITORING
    owner: "Operations team"
    deadline: "2026-04-12"
    success_criteria: "Alert fires in staging when error rate is simulated at 5%"
  - action: "Add unit test suite for ShippingCalculator covering all null input combinations"
    category: TESTING
    owner: "Developer (PROJ-4521 assignee)"
    deadline: "2026-04-07"
    success_criteria: "Tests exist and pass in CI pipeline"
  - action: "Add 'null guards on navigation properties' to code review checklist"
    category: PROCESS
    owner: "Team Lead"
    deadline: "2026-04-10"
    success_criteria: "Checklist updated and team notified"
follow_up:
  next_review_date: "2026-04-14"
  metrics_to_track: ["Time-to-detect future incidents (target: <2min)", "Unit test coverage for ShippingCalculator", "Code review checklist usage rate"]
blameless_reminder: "This postmortem investigates our systems, processes, and tooling — not individual performance. All team members made reasonable decisions with the information available. Our goal is to build better systems."
confidence: HIGH
```

---

**Related Skills:**
- `hotfix-incident-documenter` - Generates the incident document used as postmortem input
- `proper-fix-planner` - Plans the permanent fix that is an action item from postmortem
- `root-cause-recorder` - Records root cause in structured format for pattern tracking
- `risk-documentation-generator` - Documents risks identified during postmortem discussion
