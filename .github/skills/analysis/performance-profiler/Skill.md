---
name: performance-profiler
description: Establishes performance baselines and identifies bottlenecks through profiling and measurement.
---

## Purpose
Establishes performance baselines and identifies bottlenecks through profiling and measurement.

## Input Requirements
```yaml
profiling:
  component: <what to profile>
  load_level: <typical|peak|stress>
  measurement_period: <duration>
  metrics_to_capture: [<metrics>]
```

## Processing Steps

1. **Establish Baseline**
   - Measure current performance
   - Record metrics
   - Document conditions

2. **Identify Bottlenecks**
   - Where is time spent?
   - What's slow?
   - What can improve?

3. **Quantify Impact**
   - How much impact?
   - What's the cost?
   - Who's affected?

## Output Format

```yaml
performance_baseline:
  
  measurement_conditions:
    load_level: <typical|peak>
    concurrent_users: <count>
    data_volume: <size>
    measurement_period: <duration>
  
  current_metrics:
    page_load_time: <ms>
    request_time: <ms>
    response_time: <ms>
    error_rate: <percentage>
    throughput: <requests/sec>
  
  percentile_metrics:
    p50: <median>
    p95: <95th percentile>
    p99: <99th percentile>
    max: <maximum observed>
  
  bottlenecks_identified:
    - component: <what's slow>
      time_spent: <ms or %>
      frequency: <how often>
      severity: <critical|high|medium|low>
  
  acceptability_assessment:
    current_acceptable: <yes|no|marginal>
    target_improvement: <percentage|milliseconds>
  
  recommendations:
    optimization_candidates: [<items to optimize>]
    effort_to_improve: <low|medium|high>
    expected_gain: <percentage>
```

## Related Skills
- `linq-query-tracer` - For query profiling
- `request-profiler` - For request profiling
- `optimization-strategy-planner` - For optimization planning
