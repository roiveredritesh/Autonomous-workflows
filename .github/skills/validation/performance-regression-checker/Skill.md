---
name: performance-regression-checker
description: Checks that a code change hasn't introduced performance regressions by comparing post-change metrics against baseline with configurable tolerance thresholds.
---

# Performance Regression Checker

## Quick Example

**Input:** Baseline P95: 2000ms, post-change P95: 3200ms, acceptable degradation: 20%, threshold: 2400ms
**Output:** REGRESSION DETECTED — P95 is 60% slower than baseline (3200ms vs 2000ms). Exceeds 20% threshold. Recommend rollback or investigation.
**Time:** 2-3 minutes

---

## Purpose
Checks that a code change hasn't introduced performance regressions by comparing post-change metrics against baseline with configurable tolerance thresholds.

## Input

```yaml
input:
  baseline_metrics:
    p50_ms: <median before change>
    p95_ms: <95th percentile before change>
    p99_ms: <99th percentile before change>
    error_rate_percent: <baseline error rate>
    throughput_rps: <requests per second baseline>
  post_change_metrics:
    p50_ms: <median after change>
    p95_ms: <95th percentile after change>
    p99_ms: <99th percentile after change>
    error_rate_percent: <post-change error rate>
    throughput_rps: <requests per second post-change>
  acceptable_degradation_percent: <maximum % worse that is acceptable, default 20>
  measurement_duration_minutes: <how long metrics were collected>
  feature_area: <what was changed>
```

## Output

```yaml
output:
  regression_detected: true|false
  overall_verdict: REGRESSION|NO_REGRESSION|IMPROVEMENT|MARGINAL
  metrics_analysis:
    - metric: <name>
      baseline: <value>
      post_change: <value>
      delta_percent: <%>
      is_regression: true|false
      severity: CRITICAL|HIGH|MEDIUM|LOW|NONE
      acceptable_threshold: <threshold used>
  regression_summary:
    worst_metric: <metric with highest delta>
    worst_delta_percent: <%>
    regressions_count: <count>
    improvements_count: <count>
  root_cause_hypotheses:
    - hypothesis: <possible cause>
      evidence: <supporting data>
      probability: HIGH|MEDIUM|LOW
  recommendation: ROLLBACK|INVESTIGATE|ACCEPT|MONITOR
  recommendation_reason: <explanation>
  confidence: HIGH|MEDIUM|LOW
```

## DO:
✅ Compare against the same time period (same day/hour of previous week if traffic varies)
✅ Use P95 and P99 as primary regression indicators — they capture tail latency
✅ Check throughput alongside latency — regression may appear as dropped throughput
✅ Use statistical significance — don't flag natural variance as regression
✅ Separate regression cause from symptom — identify which component degraded

## DON'T:
❌ Use P50 (median) alone — it hides tail latency regressions
❌ Compare peak-hour metrics against off-peak metrics — traffic patterns affect results
❌ Accept all regressions below threshold without investigation — understand the cause
❌ Flag measurements taken during first 5 minutes post-deploy — cache warm-up affects results
❌ Ignore throughput — a faster P95 with 50% lower throughput indicates a problem

## Error Conditions

**IF baseline metrics are not available:**
```
1. Cannot perform regression check without baseline
2. Request: collect 30+ minutes of baseline before deploying
3. Return: BASELINE_REQUIRED — regression check requires pre-change measurements
```

**IF measurement duration is under 10 minutes:**
```
1. Results may not be statistically significant
2. Flag: INSUFFICIENT_DURATION — collect at least 10 minutes of data for each
3. Report with LOW confidence
```

**IF traffic volume differs significantly between baseline and post-change:**
```
1. Normalize metrics by traffic volume
2. Flag: TRAFFIC_MISMATCH — metric comparison may be affected by different load levels
```

## Processing Steps

1. **Threshold Calculation:** For each metric, acceptable threshold = baseline × (1 + acceptable_degradation/100). Example: baseline P95 2000ms, 20% tolerance → threshold 2400ms.

2. **Delta Calculation:** delta_percent = (post_change - baseline) / baseline × 100. Positive = regression (slower), Negative = improvement.

3. **Severity Classification:** P95 delta severity: >50% = CRITICAL, 20-50% = HIGH, 10-20% = MEDIUM, 5-10% = LOW, <5% = NONE. Error rate any increase = HIGH. Throughput drop >20% = HIGH.

4. **Regression Detection:** regression_detected = any metric exceeds its threshold. Count regressions and improvements separately.

5. **Root Cause Hypothesis:** Based on which metrics regressed: only latency regressed (new code path, added computation, lock contention), throughput dropped (threading issue, saturation), error rate increased (bug introduced, timeout configured too short).

6. **Verdict Assignment:** REGRESSION: any metric >threshold. IMPROVEMENT: all metrics better than baseline. MARGINAL: all within 10% either direction. NO_REGRESSION: all within threshold but no clear improvement.

7. **Recommendation:** ROLLBACK: CRITICAL severity regression. INVESTIGATE: HIGH severity without clear cause. ACCEPT: within threshold, cause understood. MONITOR: MARGINAL, needs more data.

## Example

**Input:**
```yaml
baseline_metrics:
  p50_ms: 800
  p95_ms: 2000
  p99_ms: 3500
  error_rate_percent: 0.1
  throughput_rps: 45
post_change_metrics:
  p50_ms: 850
  p95_ms: 3200
  p99_ms: 5800
  error_rate_percent: 0.1
  throughput_rps: 42
acceptable_degradation_percent: 20
measurement_duration_minutes: 30
feature_area: "Customer search caching layer"
```

**Output:**
```yaml
regression_detected: true
overall_verdict: REGRESSION
metrics_analysis:
  - {metric: "P50 response time", baseline: "800ms", post_change: "850ms", delta_percent: 6.3, is_regression: false, severity: LOW, acceptable_threshold: "960ms"}
  - {metric: "P95 response time", baseline: "2000ms", post_change: "3200ms", delta_percent: 60.0, is_regression: true, severity: CRITICAL, acceptable_threshold: "2400ms"}
  - {metric: "P99 response time", baseline: "3500ms", post_change: "5800ms", delta_percent: 65.7, is_regression: true, severity: CRITICAL, acceptable_threshold: "4200ms"}
  - {metric: "Error rate", baseline: "0.1%", post_change: "0.1%", delta_percent: 0, is_regression: false, severity: NONE, acceptable_threshold: "0.12%"}
  - {metric: "Throughput", baseline: "45 rps", post_change: "42 rps", delta_percent: -6.7, is_regression: false, severity: LOW, acceptable_threshold: "36 rps"}
regression_summary:
  worst_metric: "P99 response time"
  worst_delta_percent: 65.7%
  regressions_count: 2
  improvements_count: 0
root_cause_hypotheses:
  - hypothesis: "New Redis cache serialization overhead at P95/P99 — median (P50) barely affected but tail latency (P95/P99) shows large jump indicating serialization timeout or large payload for occasional large queries"
    evidence: "P50 only 6% slower but P95 60% slower — suggests new slow path affects minority of requests"
    probability: HIGH
  - hypothesis: "Cache lock contention on cold start — thundering herd on first requests after deploy"
    evidence: "30-minute window includes cold cache period"
    probability: MEDIUM
recommendation: INVESTIGATE
recommendation_reason: "CRITICAL P95/P99 regression detected. P50 healthy suggests issue affects specific request types, not all requests. Investigate cache serialization overhead for large datasets before deciding rollback vs fix."
confidence: HIGH
```

---

**Related Skills:**
- `performance-validation-planner` - Plans the validation approach that feeds metrics into this checker
- `request-profiler` - Profiles specific requests to identify regression source
- `serialization-overhead-checker` - Investigates serialization as a regression cause
- `cache-performance-checker` - Evaluates whether cache introduced the regression
