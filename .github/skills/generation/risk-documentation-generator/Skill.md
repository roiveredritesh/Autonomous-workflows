---
name: risk-documentation-generator
description: risk_statement: "IF Redis becomes unavailable THEN SQL Server receives all cached query traffic (est. 5x normal load) BECAUSE the application has no circuit breaker or graceful degradation"
---

# Risk Documentation Generator

## Quick Example

**Input:** Risk: Redis cache unavailability, probability: LOW, impact: HIGH — all DB queries bypass cache, DB overloaded
**Output:** Risk register entry with risk score 6/25, mitigation: circuit breaker + graceful fallback to DB, monitoring: Redis health check alert
**Time:** 1-2 minutes

---

## Purpose
Generates risk register entries documenting technical and business risks with mitigation strategies and monitoring plans.

## Input

```yaml
input:
  risk_description: <what could go wrong>
  risk_category: PERFORMANCE|SECURITY|DATA_INTEGRITY|AVAILABILITY|COMPLIANCE|TECHNICAL_DEBT
  probability: VERY_LOW|LOW|MEDIUM|HIGH|VERY_HIGH
  impact: VERY_LOW|LOW|MEDIUM|HIGH|VERY_HIGH
  affected_components: [<list of systems or features at risk>]
  mitigation_ideas: <optional — any known mitigations>
  risk_owner: <optional — team or role responsible>
  ticket_id: <optional — related ticket>
```

## Output

```yaml
output:
  risk_entry:
    id: <RISK-{id}>
    title: <concise risk title>
    category: <category>
    probability: <level>
    impact: <level>
    risk_score: <1-25 numeric>
    priority: CRITICAL|HIGH|MEDIUM|LOW
    status: OPEN|MITIGATED|ACCEPTED|CLOSED
    owner: <role or team>
  description:
    risk_statement: "IF {condition} THEN {consequence} BECAUSE {reason}"
    affected_components: [<list>]
    worst_case_scenario: <description>
    early_warning_signs: [<indicators>]
  mitigation_strategies:
    - strategy: AVOID|REDUCE|TRANSFER|ACCEPT
      description: <action>
      implementation: <how to implement>
      effort: LOW|MEDIUM|HIGH
      residual_risk: <remaining risk after mitigation>
  monitoring_plan:
    metrics_to_watch: [<list>]
    alert_thresholds: [<condition: alert level>]
    review_frequency: DAILY|WEEKLY|MONTHLY
  confidence: HIGH|MEDIUM|LOW
```

## DO:
✅ Write the risk statement as: "IF {event} THEN {consequence} BECAUSE {mechanism}"
✅ Calculate risk score as probability_value × impact_value (1-5 scale each)
✅ Include early warning signs — they enable proactive response before risk materializes
✅ Provide at least one REDUCE mitigation — pure ACCEPT risks tend to materialize
✅ Set a monitoring plan with specific metrics, not vague "watch for problems"

## DON'T:
❌ Document risks without mitigations — every risk needs at least ACCEPT with rationale
❌ Use vague impact descriptions — quantify where possible (# users affected, revenue impact)
❌ Assign all risks to "the team" — a specific owner is required for accountability
❌ Accept HIGH or CRITICAL risks without a reduction plan
❌ Forget early warning signs — they're more valuable than the risk description itself

## Error Conditions

**IF probability and impact are both VERY_LOW:**
```
1. Consider whether this risk is worth documenting
2. If documenting, mark as ACCEPTED with rationale
3. Flag: LOW_PRIORITY_RISK — may not require active monitoring
```

**IF no mitigation is feasible:**
```
1. Document as ACCEPTED risk with explicit acknowledgment
2. Require sign-off from appropriate authority
3. Flag: ACCEPTED_RISK — no cost-effective mitigation available
```

## Processing Steps

1. **Risk ID:** Assign RISK-{sequential number} or use ticket ID format.

2. **Risk Score:** Map probability and impact to 1-5 values: VERY_LOW=1, LOW=2, MEDIUM=3, HIGH=4, VERY_HIGH=5. Score = probability_value × impact_value (max 25). Priority: CRITICAL 20-25, HIGH 12-19, MEDIUM 6-11, LOW 1-5.

3. **Risk Statement:** Format: "IF {event occurs} THEN {specific consequence} BECAUSE {mechanism that causes it}".

4. **Worst Case:** Describe the maximum plausible damage if risk materializes with no mitigation in place.

5. **Early Warning Signs:** List observable indicators that the risk is increasing: error rate increasing, memory pressure, external dependency latency rising, deployment frequency increasing.

6. **Mitigation Strategies:** For each strategy type: AVOID (eliminate the risk), REDUCE (lower probability or impact), TRANSFER (insurance, SLA), ACCEPT (consciously accept with rationale). Include implementation steps.

7. **Monitoring Plan:** Specify exact metrics (not just "monitor Redis") and alert thresholds. Set review frequency based on risk score: CRITICAL→daily, HIGH→weekly, MEDIUM/LOW→monthly.

## Example

**Input:**
```yaml
risk_description: "Redis cache server unavailability causes all customer searches to hit DB directly, potentially overloading SQL Server"
risk_category: AVAILABILITY
probability: LOW
impact: HIGH
affected_components: ["Customer search", "Product catalog", "Order history"]
risk_owner: "Infrastructure team"
ticket_id: "PROJ-1240"
```

**Output:**
```yaml
risk_entry:
  id: "RISK-024"
  title: "Redis Unavailability Causes SQL Server Overload"
  category: AVAILABILITY
  probability: LOW
  impact: HIGH
  risk_score: 8
  priority: MEDIUM
  status: OPEN
  owner: "Infrastructure team"
description:
  risk_statement: "IF Redis becomes unavailable THEN SQL Server receives all cached query traffic (est. 5x normal load) BECAUSE the application has no circuit breaker or graceful degradation"
  affected_components: ["Customer search", "Product catalog", "Order history"]
  worst_case_scenario: "Redis downtime during peak hours causes SQL Server connection pool exhaustion, making the application completely unavailable for all users"
  early_warning_signs:
    - "Redis connection timeout errors appearing in application logs"
    - "SQL Server CPU above 70% (baseline 20%)"
    - "Customer search response time >3s (baseline 400ms)"
mitigation_strategies:
  - strategy: REDUCE
    description: "Implement circuit breaker pattern — on Redis failure, temporarily serve from DB with degraded caching"
    implementation: "Use Polly library: CircuitBreakerPolicy for Redis calls. Fallback to direct DB query on open circuit."
    effort: MEDIUM
    residual_risk: "DB load increases during Redis downtime but no total failure"
  - strategy: REDUCE
    description: "Redis Sentinel or Cluster for high availability"
    implementation: "Configure StackExchange.Redis with Sentinel endpoints for automatic failover"
    effort: HIGH
    residual_risk: "LOW — failover typically completes in <30s"
monitoring_plan:
  metrics_to_watch:
    - "Redis connection success rate (target: >99.9%)"
    - "SQL Server CPU utilization (alert: >60%)"
    - "Customer search P95 response time (alert: >2000ms)"
  alert_thresholds:
    - "Redis connection failure rate >1%: WARNING"
    - "Redis connection failure rate >5%: CRITICAL"
  review_frequency: WEEKLY
confidence: HIGH
```

---

**Related Skills:**
- `decision-record-creator` - Creates ADRs for decisions made to mitigate risks
- `rollback-plan-generator` - Generates rollback plans as part of risk mitigation
- `hotfix-incident-documenter` - Documents when a risk materializes into an incident
- `postmortem-planner` - Plans postmortem after a risk materializes
