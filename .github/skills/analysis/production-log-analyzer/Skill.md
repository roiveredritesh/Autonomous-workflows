---
name: production-log-analyzer
description: Analyzes production error logs to identify patterns, frequency, and root causes of failures in ASP.NET WebForms applications.
---

# Production Log Analyzer

## Quick Example

**Input:** IIS/App logs for `ShippingCalculator` errors over last 2 hours
**Output:** 3 distinct error patterns, NullReferenceException at line 142 most frequent (87%), first occurrence 14:23 UTC
**Time:** 3-5 minutes

---

## Purpose
Analyzes production error logs to identify patterns, frequency, and root causes of failures in ASP.NET WebForms applications.

## Input

```yaml
input:
  log_file_path: <path to IIS log, Event Log, or App Insights export>
  error_message: <specific error string or exception type to search for>
  time_range: <ISO 8601 interval, e.g. "2026-04-05T12:00/2026-04-05T14:00">
  component_filter: <optional — class name, page, or module to narrow scope>
  max_entries: <optional — cap analysis at N log lines, default 10000>
```

## Output

```yaml
output:
  summary:
    total_errors: <count>
    unique_patterns: <count>
    time_range_analyzed: <start to end>
    affected_components: [<list of classes/pages>]
  patterns:
    - pattern_id: <P1..Pn>
      exception_type: <NullReferenceException|SqlException|etc>
      message_template: <deduped message>
      frequency: <count>
      percentage: <% of total>
      first_occurrence: <ISO timestamp>
      last_occurrence: <ISO timestamp>
      stack_trace_signature: <top 3 frames>
      affected_component: <class.method>
  root_cause_hypothesis:
    most_likely: <description>
    confidence: HIGH|MEDIUM|LOW
    supporting_evidence: [<log line refs>]
  recommendations:
    - action: <what to investigate or fix>
      priority: critical|high|medium
  confidence: HIGH|MEDIUM|LOW
```

## DO:
✅ Deduplicate stack traces by signature to find true unique patterns
✅ Sort patterns by frequency descending — highest impact first
✅ Record first and last occurrence timestamps to detect onset and duration
✅ Cross-reference error timestamps against deployment/config change history
✅ Flag patterns that began after a recent deployment

## DON'T:
❌ Treat each log line as a unique pattern — aggregate by exception type + stack signature
❌ Ignore low-frequency errors — a rare pattern may indicate data corruption
❌ Skip the time range filter — unbounded analysis wastes time and misses focus
❌ Confuse warning-level entries with errors — filter by severity
❌ Report raw log dumps — always summarize into structured patterns

## Error Conditions

**IF log file not found or inaccessible:**
```
1. Check path and permissions
2. Return error: LOG_ACCESS_FAILED: Cannot read <path> — verify IIS log path or export manually
```

**IF no errors found in time range:**
```
1. Widen time range by 2x
2. If still empty: Return NO_ERRORS_IN_RANGE — issue may have resolved or wrong time range provided
```

**IF log format is unrecognized:**
```
1. Attempt W3C, Common Log Format, and JSON structured log parsing
2. If all fail: Return UNKNOWN_LOG_FORMAT — provide sample lines for manual inspection
```

## Processing Steps

1. **Parse & Filter:** Load log file, parse entries by timestamp into the specified time range. Filter by severity (ERROR, CRITICAL, FATAL). Apply component filter if provided.

2. **Deduplication:** Extract exception type + top 3 stack frames as a fingerprint. Group entries by fingerprint to create pattern clusters. Count frequency per cluster.

3. **Pattern Analysis:** For each cluster, record: exception type, deduped message, frequency, percentage of total, first/last occurrence, affected component (from stack frame), and a representative stack trace.

4. **Temporal Analysis:** Plot error frequency over time. Flag sharp spikes that align with deployment times (check against git log or deployment records).

5. **Root Cause Hypothesis:** Identify the highest-frequency pattern. Cross-reference with recent code changes in `change-history-analyzer`. Form a root cause hypothesis with confidence level based on evidence strength.

6. **Recommendations:** Prioritize patterns by `frequency × severity`. Output actionable recommendations for each top pattern.

## Example

**Input:**
```yaml
log_file_path: "C:\\inetpub\\logs\\LogFiles\\W3SVC1\\u_ex260405.log"
error_message: "NullReferenceException"
time_range: "2026-04-05T12:00/2026-04-05T14:00"
component_filter: "ShippingCalculator"
```

**Output:**
```yaml
summary:
  total_errors: 312
  unique_patterns: 3
  time_range_analyzed: "2026-04-05T12:00 to 14:00"
  affected_components: [ShippingCalculator, OrderProcessor]
patterns:
  - pattern_id: P1
    exception_type: NullReferenceException
    message_template: "Object reference not set to an instance of an object."
    frequency: 271
    percentage: 87%
    first_occurrence: "2026-04-05T12:23:14Z"
    last_occurrence: "2026-04-05T13:58:41Z"
    stack_trace_signature: "ShippingCalculator.Calculate > OrderProcessor.Submit > Page_Load"
    affected_component: "ShippingCalculator.Calculate"
  - pattern_id: P2
    exception_type: SqlException
    message_template: "Timeout expired. The timeout period elapsed..."
    frequency: 41
    percentage: 13%
    first_occurrence: "2026-04-05T12:31:00Z"
    last_occurrence: "2026-04-05T13:45:22Z"
    stack_trace_signature: "CarrierRepository.GetRates > SqlCommand.ExecuteReader"
    affected_component: "CarrierRepository.GetRates"
root_cause_hypothesis:
  most_likely: "ShippingCalculator.Calculate receives null Carrier — likely missing null guard after recent refactor"
  confidence: HIGH
  supporting_evidence: ["P1 started at 12:23 — 4 min after deployment at 12:19", "All P1 traces share same null dereference line"]
recommendations:
  - action: "Add null check for Carrier in ShippingCalculator.Calculate before accessing properties"
    priority: critical
  - action: "Investigate CarrierRepository SQL timeout — possible missing index or lock contention"
    priority: high
confidence: HIGH
```

---

**Related Skills:**
- `error-pattern-detector` - Groups errors by recurring pattern across multiple log files
- `change-history-analyzer` - Correlates errors with recent deployments and commits
- `production-impact-assessor` - Quantifies user and business impact of detected errors
- `bug-classifier` - Classifies identified bugs by type and severity
