---
name: performance-validation-planner
description: Plans performance validation to verify optimizations achieved their targets including load scenarios, success criteria, monitoring duration, and regression detection.
---

# Performance Validation Planner

## Quick Example

**Input:** Baseline 8200ms, target 400ms, optimization applied: index + LINQ fix + cache
**Output:** Validation plan: 3 load scenarios (typical/peak/stress), 4 metrics to track, success criteria (P95 <500ms), monitoring duration 2 hours post-deploy
**Time:** 2-3 minutes

---

## Purpose
Plans performance validation to verify optimizations achieved their targets including load scenarios, success criteria, monitoring duration, and regression detection.

## Input

```yaml
input:
  baseline_metrics:
    page_load_ms: <before optimization>
    query_time_ms: <before optimization>
    cache_hit_rate_percent: <before optimization>
    error_rate_percent: <before optimization>
  target_metrics:
    page_load_ms: <goal>
    query_time_ms: <goal>
    cache_hit_rate_percent: <goal>
  optimization_applied: <list of optimizations implemented>
  data_volume: <approximate production data size>
  concurrent_user_estimate: <typical and peak>
  acceptable_degradation_percent: <what % regression triggers rollback>
```

## Output

```yaml
output:
  validation_test_plan:
    pre_deploy:
      - test: <description>
        environment: STAGING
        method: <how to run>
        success_criteria: <specific threshold>
    post_deploy:
      - test: <description>
        environment: PRODUCTION
        method: <how to run>
        duration_minutes: <how long to run/observe>
        success_criteria: <specific threshold>
  load_scenarios:
    - scenario: TYPICAL|PEAK|STRESS
      concurrent_users: <count>
      data_volume: <records>
      duration_minutes: <test duration>
      expected_p50_ms: <ms>
      expected_p95_ms: <ms>
      pass_threshold_p95_ms: <maximum acceptable>
  metrics_to_track:
    - metric: <name>
      baseline: <before>
      target: <after optimization>
      acceptable: <minimum acceptable>
      monitoring_source: <where to measure — Application Insights, Redis, SQL Server>
  regression_criteria:
    triggers_rollback:
      - condition: <specific condition>
        severity: CRITICAL|HIGH
  monitoring_schedule:
    post_deploy_immediate_minutes: <first monitoring period>
    post_deploy_extended_hours: <extended monitoring>
    comparison_period: <timeframe to compare>
  confidence: HIGH|MEDIUM|LOW
```

## DO:
✅ Test under PEAK load conditions — not just typical — to verify at scale
✅ Measure P95 and P99, not just P50 — tail latency is user-visible
✅ Include data correctness in validation — verify optimization returns same results
✅ Monitor for at least 30 minutes post-deploy before declaring success
✅ Set specific numeric thresholds — not "should be faster"

## DON'T:
❌ Validate only in staging — production data and traffic patterns differ
❌ Stop monitoring after 5 minutes — issues can appear after cache warm-up
❌ Declare success without checking data correctness
❌ Use a single test run as validation — run multiple to detect variability
❌ Forget to check for regression in adjacent features — optimization can break neighbors

## Error Conditions

**IF staging doesn't have production-scale data:**
```
1. Test with production data subset — at least 10% of production volume
2. Extrapolate results with scaling factor
3. Flag: REDUCED_DATA_VOLUME — results may not fully represent production behavior
```

**IF load testing tools are not available:**
```
1. Use production traffic observation post-deploy as validation
2. Require extended monitoring period (2 hours instead of 30 minutes)
3. Flag: NO_LOAD_TESTING — validation relies on production traffic; risk is higher
```

**IF P95 target is not achievable in staging:**
```
1. Investigate cause — different hardware, different data volume, different configuration
2. Document expected difference between staging and production performance
3. Flag: STAGING_GAP — adjust targets for staging vs production separately
```

## Processing Steps

1. List all metrics affected: page load, query time, cache hit rate, DB CPU, error rate.
2. Design load scenarios: Typical (10% peak), Peak (estimated max), Stress (2× peak).
3. Pre-deploy: run typical load in staging, verify P95 meets target, verify data correctness.
4. Post-deploy: watch error rate first 15 min (any spike = rollback), monitor P50/P95 under real traffic.
5. Regression criteria: flag if any feature degrades >20% AND absolute time >500ms.
6. Reporting: Success = all targets met for 30+ min under typical load with no regressions.

## Example

**Input:**
```yaml
baseline_metrics:
  page_load_ms: 8200
  query_time_ms: 7800
  cache_hit_rate_percent: 0
  error_rate_percent: 0
target_metrics:
  page_load_ms: 400
  query_time_ms: 200
  cache_hit_rate_percent: 70
optimization_applied: ["LINQ WHERE fix", "Index IX_Customers_Status", "Redis cache 5min TTL"]
data_volume: "45,000 customers"
concurrent_user_estimate: "typical: 50, peak: 200"
acceptable_degradation_percent: 20
```

**Output:**
```yaml
validation_test_plan:
  pre_deploy:
    - test: "Customer search response time with 45K records in staging"
      environment: STAGING
      method: "Run CustomerSearch.aspx with Status='Active' filter, measure in MiniProfiler"
      success_criteria: "P95 <500ms for at least 3 consecutive runs"
    - test: "Search results match pre-optimization results"
      environment: STAGING
      method: "Run query-behavior-validator: original LINQ vs optimized LINQ on same dataset"
      success_criteria: "Row count identical, all rows present in both result sets"
  post_deploy:
    - test: "Production error rate monitoring"
      environment: PRODUCTION
      method: "Application Insights: error rate dashboard, 1-minute granularity"
      duration_minutes: 60
      success_criteria: "Error rate remains at pre-optimization baseline (0%)"
    - test: "Cache hit rate after warm-up"
      environment: PRODUCTION
      method: "Redis INFO stats: keyspace_hits / (hits + misses)"
      duration_minutes: 30
      success_criteria: ">70% hit rate after 15-minute warm-up period"
load_scenarios:
  - scenario: TYPICAL
    concurrent_users: 50
    data_volume: "45,000 customers"
    expected_p95_ms: 350
    pass_threshold_p95_ms: 500
  - scenario: PEAK
    concurrent_users: 200
    data_volume: "45,000 customers"
    expected_p95_ms: 600
    pass_threshold_p95_ms: 1000
metrics_to_track:
  - {metric: "Customer search P95 page load", baseline: "8200ms", target: "<400ms", acceptable: "<1000ms", monitoring_source: "Application Insights"}
  - {metric: "CustomerRepository.GetByFilter query time", baseline: "7800ms", target: "<200ms", acceptable: "<500ms", monitoring_source: "SQL Server Profiler"}
  - {metric: "Redis cache hit rate", baseline: "0%", target: ">70%", acceptable: ">50%", monitoring_source: "Redis INFO stats"}
  - {metric: "Application error rate", baseline: "0%", target: "0%", acceptable: "<0.1%", monitoring_source: "Application Insights"}
regression_criteria:
  triggers_rollback:
    - {condition: "Error rate >1% for >2 consecutive minutes", severity: CRITICAL}
    - {condition: "Data correctness check fails (result count differs)", severity: CRITICAL}
confidence: HIGH
```

---

**Related Skills:**
- `performance-implementation-planner` - Creates the implementation plan that validation will test
- `optimization-strategy-planner` - Provides the strategy and expected improvements for targets
- `performance-regression-checker` - Checks that validation finds no regressions
- `query-behavior-validator` - Validates that optimized queries return identical results
