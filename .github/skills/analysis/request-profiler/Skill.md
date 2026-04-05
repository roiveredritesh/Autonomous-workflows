---
name: request-profiler
description: Profiles individual HTTP request lifecycle to identify slow components in ASP.NET WebForms pages by breaking down time per lifecycle phase.
---

# Request Profiler

## Quick Example

**Input:** `CustomerSearch.aspx` with filter parameters, slow on POST, ~8 seconds
**Output:** Page_Load: 120ms, DB query: 7400ms, ViewState deserialization: 380ms, Render: 100ms — DB query is bottleneck (90% of time)
**Time:** 2-4 minutes

---

## Purpose
Profiles individual HTTP request lifecycle to identify slow components in ASP.NET WebForms pages by breaking down time per lifecycle phase.

## Input

```yaml
input:
  page_url: <relative or absolute URL of the WebForms page>
  request_parameters: <POST/GET parameters or form values>
  request_method: GET|POST
  lifecycle_stage_suspected: <optional — PreInit|Init|Load|Events|PreRender|Render>
  baseline_time_ms: <total observed request time in ms>
  profiling_tool: <optional — MiniProfiler|Application Insights|IIS ETW|manual>
```

## Output

```yaml
output:
  total_time_ms: <observed total>
  lifecycle_breakdown:
    pre_init_ms: <ms>
    init_ms: <ms>
    load_state_ms: <ms>          # ViewState deserialization
    process_postback_ms: <ms>    # Event handlers
    load_ms: <ms>                # Page_Load
    render_ms: <ms>
    unaccounted_ms: <ms>         # Difference from total
  bottleneck:
    phase: <lifecycle phase name>
    component: <class or method name>
    time_ms: <ms>
    percentage_of_total: <%>
    severity: CRITICAL|HIGH|MEDIUM|LOW
  secondary_bottlenecks:
    - phase: <name>
      component: <name>
      time_ms: <ms>
  db_calls:
    count: <number of SQL queries>
    total_time_ms: <combined>
    slowest_query_ms: <ms>
    slowest_query_preview: <truncated SQL>
  cache_hits:
    redis_hits: <count>
    redis_misses: <count>
    hit_rate_percent: <%>
  recommendations:
    - action: <what to optimize>
      expected_saving_ms: <estimate>
      priority: critical|high|medium
  confidence: HIGH|MEDIUM|LOW
```

## DO:
✅ Break down time by all six WebForms lifecycle phases — not just Page_Load
✅ Count and time each SQL query made during the request
✅ Measure ViewState size and deserialization time separately
✅ Record Redis cache hit/miss ratio during the request
✅ Report bottleneck as percentage of total — not just absolute ms

## DON'T:
❌ Profile only happy-path GET requests when the issue is on POST (postback)
❌ Ignore ViewState overhead — it's a common culprit in Telerik-heavy pages
❌ Conflate DB time with network latency — measure each separately
❌ Skip secondary bottlenecks — total optimization requires addressing all significant ones
❌ Report without a baseline — always compare against a reference measurement

## Error Conditions

**IF profiling tool is not available:**
```
1. Instrument manually using Stopwatch around suspected phases
2. Add Application_BeginRequest / Application_EndRequest timing to Global.asax
3. Return: MANUAL_PROFILING_REQUIRED — attach Stopwatch timing results for analysis
```

**IF total time cannot be reproduced:**
```
1. Check if issue is load-dependent (only slow under concurrent users)
2. Recommend profiling under realistic load with JMeter or similar
3. Return: INTERMITTENT_PERFORMANCE — profiling requires load simulation
```

**IF lifecycle phase times don't add up to total:**
```
1. Report unaccounted_ms as a separate line item
2. Flag possible async operations or HTTP modules not captured in trace
```

## Processing Steps

1. **Request Setup:** Identify page URL, method (GET vs POST), and parameters. Determine if it's a postback (affects which lifecycle phases run event handlers).

2. **Lifecycle Instrumentation:** Using MiniProfiler, Application Insights, or manual Stopwatch: instrument PreInit, Init, LoadViewState, ProcessPostBackData, Load, Events (postback), PreRender, Render phases.

3. **DB Call Tracing:** Intercept all SQL commands during the request (via EF profiler or SqlCommand wrapper). Record count, timing, and first 200 chars of each query.

4. **Cache Operation Tracing:** Record all Redis GET/SET operations. Calculate hit rate.

5. **ViewState Measurement:** Capture __VIEWSTATE hidden field size after Render. Estimate deserialization time from LoadViewState phase timing.

6. **Bottleneck Identification:** Rank phases by time consumed. Mark top phase as primary bottleneck if it exceeds 50% of total. Compute severity based on absolute ms (CRITICAL >5000, HIGH >2000, MEDIUM >500).

7. **Recommendations:** For each bottleneck, suggest targeted optimization (index, caching, ViewState disable, eager load, pagination).

## Example

**Input:**
```yaml
page_url: "/Customers/CustomerSearch.aspx"
request_parameters: {txtFilter: "Active", ddlRegion: "North"}
request_method: POST
baseline_time_ms: 8200
profiling_tool: MiniProfiler
```

**Output:**
```yaml
total_time_ms: 8200
lifecycle_breakdown:
  pre_init_ms: 12
  init_ms: 45
  load_state_ms: 380
  process_postback_ms: 7450
  load_ms: 120
  render_ms: 185
  unaccounted_ms: 8
bottleneck:
  phase: process_postback_ms
  component: "CustomerRepository.GetByFilter()"
  time_ms: 7400
  percentage_of_total: 90%
  severity: CRITICAL
secondary_bottlenecks:
  - phase: load_state_ms
    component: "RadGrid ViewState"
    time_ms: 380
db_calls:
  count: 3
  total_time_ms: 7400
  slowest_query_ms: 7380
  slowest_query_preview: "SELECT * FROM Customers WHERE 1=1 -- (no index on Status)"
cache_hits:
  redis_hits: 0
  redis_misses: 2
  hit_rate_percent: 0%
recommendations:
  - action: "Push WHERE filter into SQL — currently filtering 4500 rows in memory"
    expected_saving_ms: 7000
    priority: critical
  - action: "Add index on Customers.Status and Region columns"
    expected_saving_ms: 500
    priority: high
  - action: "Disable ViewState on non-postback Telerik columns"
    expected_saving_ms: 200
    priority: medium
confidence: HIGH
```

---

**Related Skills:**
- `performance-profiler` - Establishes overall performance baselines across multiple requests
- `network-latency-checker` - Isolates network vs processing time in the request lifecycle
- `webforms-lifecycle-analyzer` - Deep analysis of WebForms lifecycle phase interactions
- `sql-execution-analyzer` - Detailed analysis of the SQL queries identified as bottlenecks
