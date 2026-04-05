---
name: production-verification-checker
description: Verifies production health after a hotfix deployment by comparing error rates, response times, and critical path metrics against pre-incident baseline.
---

# Production Verification Checker

## Quick Example

**Input:** Hotfix for order submission deployed, monitoring: Application Insights, baseline: 0% error rate, 2s load time
**Output:** STABLE — error rate: 0% (was 100%), load time: 1.8s (baseline 2s), 15 successful orders in 10 minutes. All critical paths verified.
**Time:** 2-3 minutes

---

## Purpose
Verifies production health after a hotfix deployment by comparing error rates, response times, and critical path metrics against pre-incident baseline.

## Input

```yaml
input:
  affected_feature: <what was fixed>
  monitoring_metrics: <list of metrics available — Application Insights, IIS, custom>
  baseline_values:
    error_rate_percent: <normal error rate before incident>
    page_load_p95_ms: <normal P95 page load>
    transactions_per_minute: <normal throughput>
  monitoring_window_minutes: <how long to observe, default 30>
  critical_paths: <list of critical user paths to verify>
```

## Output

```yaml
output:
  overall_status: STABLE|DEGRADED|CRITICAL|INSUFFICIENT_DATA
  status_reason: <why this status was assigned>
  metric_comparison:
    - metric: <name>
      baseline: <value>
      current: <value>
      delta_percent: <%>
      status: NORMAL|IMPROVED|SLIGHTLY_DEGRADED|DEGRADED|CRITICAL
  critical_path_verification:
    - path: <user path>
      status: VERIFIED|FAILED|NOT_VERIFIED
      evidence: <what was observed>
  anomalies_detected:
    - type: <error type or metric anomaly>
      description: <detail>
      severity: CRITICAL|HIGH|MEDIUM|LOW
  recommendations:
    - action: <what to do>
      priority: critical|high|medium
  continue_monitoring: true|false
  monitoring_duration_recommendation_minutes: <how much longer to monitor>
  confidence: HIGH|MEDIUM|LOW
```

## DO:
✅ Compare against the pre-incident baseline, not the incident state (100% errors)
✅ Verify the specific failure scenario is now resolved (submit an order with null carrier)
✅ Check for any NEW errors that weren't present before — hotfix may have introduced issues
✅ Monitor for at least 15 minutes before declaring STABLE
✅ Track business metrics (orders per minute, successful checkouts) not just technical metrics

## DON'T:
❌ Compare against the incident state — that's not the baseline
❌ Declare STABLE after <5 minutes — issues can emerge after cache warmup
❌ Ignore new error types that appear post-hotfix — they may be new regressions
❌ Skip business metric verification — technical metrics can look fine while business is broken
❌ Stop monitoring at 15 minutes for CRITICAL incidents — extend to 60+ minutes

## Error Conditions

**IF monitoring is unavailable:**
```
1. Run manual verification: submit test transactions in production (minimal)
2. Check IIS logs manually for new error entries
3. Flag: MANUAL_VERIFICATION — automated monitoring unavailable; manual verification required
```

**IF baseline values are unknown:**
```
1. Use industry benchmarks: <1% error rate, <3s P95 for web apps
2. Flag: BASELINE_UNKNOWN — verification is relative, not absolute
```

**IF insufficient time has passed:**
```
1. Return: INSUFFICIENT_DATA — only N minutes of post-deploy data available
2. Set continue_monitoring: true with recommendation to check in X more minutes
```

## Processing Steps

1. **Current State Measurement:** Pull current metrics from monitoring: error rate (last 5 min), P50/P95 response time (last 10 min), throughput (last 5 min). Compare to baseline values.

2. **Error Rate Analysis:** Primary indicator. NORMAL = within 10% of baseline. SLIGHTLY_DEGRADED = 10-50% above baseline. DEGRADED = 50-100% above. CRITICAL = >100% above or absolute >5%.

3. **Performance Analysis:** Compare P95 response time. NORMAL = within 20% of baseline. IMPROVED = faster than baseline. SLIGHTLY_DEGRADED = 20-50% slower. DEGRADED = >50% slower.

4. **New Error Detection:** Compare error types in last 15 minutes against pre-incident baseline. Any new exception type that wasn't present before the hotfix = potential regression.

5. **Critical Path Verification:** For each critical_path: verify by reviewing successful transaction logs or running a test transaction. Mark VERIFIED if successful completions observed.

6. **Business Metric Comparison:** Check: orders per minute, successful checkouts, key conversion metric. Should be close to baseline within 10-20%. Large drops indicate a silent failure.

7. **Status Assignment:** STABLE = all metrics normal, no new errors, critical paths verified. DEGRADED = some metrics off baseline but improving, no new errors. CRITICAL = new errors, metrics significantly off. INSUFFICIENT_DATA = <10 minutes of data.

## Example

**Input:**
```yaml
affected_feature: "Order submission — ShippingCalculator fix"
monitoring_metrics: ["Application Insights", "Custom health endpoint"]
baseline_values:
  error_rate_percent: 0
  page_load_p95_ms: 2000
  transactions_per_minute: 35
monitoring_window_minutes: 20
critical_paths:
  - "Customer submits order with carrier"
  - "Customer submits order without carrier (draft)"
  - "Admin views order list"
```

**Output:**
```yaml
overall_status: STABLE
status_reason: "Error rate returned to 0%, response time at baseline, 21 successful orders in 20 minutes (baseline: 35/min, currently 31/min — slightly below baseline but within normal variance)"
metric_comparison:
  - {metric: "Error rate", baseline: "0%", current: "0%", delta_percent: 0, status: NORMAL}
  - {metric: "Page load P95", baseline: "2000ms", current: "1850ms", delta_percent: -7.5, status: IMPROVED}
  - {metric: "Orders per minute", baseline: "35", current: "31", delta_percent: -11.4, status: SLIGHTLY_DEGRADED}
critical_path_verification:
  - {path: "Order with carrier", status: VERIFIED, evidence: "17 successful orders with carrier in logs in last 20 minutes"}
  - {path: "Order without carrier (draft)", status: VERIFIED, evidence: "4 draft orders submitted with DefaultRate ($0.00) — no errors"}
  - {path: "Admin order list", status: VERIFIED, evidence: "No errors in admin page — 3 admin sessions active"}
anomalies_detected:
  - {type: "Orders per minute slightly below baseline", description: "31/min vs 35/min baseline — likely catchup from 32-minute outage window affecting user sessions", severity: LOW}
recommendations:
  - {action: "Continue monitoring for 30 more minutes — orders/min trending up (+3 in last 5 min), expect full recovery", priority: medium}
  - {action: "Notify customer support: outage resolved, affected 312 customers — provide retry guidance", priority: high}
continue_monitoring: true
monitoring_duration_recommendation_minutes: 30
confidence: HIGH
```

---

**Related Skills:**
- `hotfix-validator` - Validates hotfix safety before deployment (this skill validates after)
- `hotfix-deployment-planner` - The deployment plan that this skill monitors completion of
- `request-profiler` - Profiles specific requests if performance anomalies are detected
- `production-log-analyzer` - Analyzes logs if anomalies require deeper investigation
