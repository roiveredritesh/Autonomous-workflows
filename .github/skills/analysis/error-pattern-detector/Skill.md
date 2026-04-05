---
name: error-pattern-detector
description: Detects recurring error patterns across log entries to identify systemic issues affecting multiple components in the ASP.NET WebForms application.
---

# Error Pattern Detector

## Quick Example

**Input:** 500 log entries from last 24 hours across OrderService, ShippingModule
**Output:** 4 recurring patterns found — P1 (SqlTimeout) appears in all 3 modules, P2 (NullRef) isolated to OrderService, systemic DB issue identified
**Time:** 2-4 minutes

---

## Purpose
Detects recurring error patterns across log entries to identify systemic issues affecting multiple components in the ASP.NET WebForms application.

## Input

```yaml
input:
  log_entries: <raw log text, array of log lines, or path to structured log>
  error_messages: <optional list of specific error messages to focus on>
  stack_traces: <optional list of stack trace strings>
  component_scope: <optional list of assemblies or namespaces to include>
  min_frequency: <optional — minimum occurrences to qualify as a pattern, default 3>
```

## Output

```yaml
output:
  patterns_found:
    - pattern_id: <P1..Pn>
      name: <short human-readable name>
      exception_type: <exception class>
      frequency: <total occurrences>
      affected_components: [<list>]
      is_systemic: <true|false — spans multiple components>
      common_root_cause: <hypothesis>
      representative_stack: <condensed stack trace>
  systemic_issues:
    - issue: <description>
      pattern_ids: [<P1, P3>]
      shared_cause: <common infrastructure or code path>
  per_pattern_summary:
    - pattern_id: P1
      trend: INCREASING|STABLE|DECREASING
      first_seen: <timestamp>
      last_seen: <timestamp>
  confidence: HIGH|MEDIUM|LOW
```

## DO:
✅ Fingerprint errors by exception type + normalized message + top stack frames
✅ Flag patterns appearing in 3+ components as systemic issues
✅ Detect trend direction (increasing/stable/decreasing) using temporal binning
✅ Normalize variable parts of error messages (IDs, timestamps, paths) before comparing
✅ Group related patterns that share a common infrastructure component (DB, Redis, external API)

## DON'T:
❌ Treat every unique message as a unique pattern — normalize variable parts first
❌ Report patterns below minimum frequency threshold — noise adds confusion
❌ Ignore cross-component patterns — they indicate systemic issues, not isolated bugs
❌ Skip trend analysis — a decreasing pattern may not need immediate action
❌ Conflate different exception types with identical messages

## Error Conditions

**IF fewer than min_frequency occurrences of any pattern:**
```
1. Lower min_frequency to 1 for single-entry analysis
2. Return warning: LOW_SAMPLE_COUNT — patterns may not be statistically significant
```

**IF stack traces are missing or truncated:**
```
1. Fingerprint by exception type + message only
2. Flag output: STACK_INCOMPLETE — pattern grouping may be less accurate
```

**IF log entries span multiple applications:**
```
1. Partition by application name/identifier before pattern detection
2. Analyze intra-app patterns first, then cross-app patterns
```

## Processing Steps

1. **Normalization:** Strip variable parts from error messages (GUIDs, row IDs, timestamps, file paths). Normalize whitespace and casing. Extract exception type from message prefix.

2. **Fingerprinting:** Create a fingerprint per entry: `{exception_type}::{normalized_message_hash}::{top_3_stack_frames}`. Group entries by fingerprint into clusters.

3. **Frequency Filter:** Discard clusters below `min_frequency`. Rank remaining patterns by frequency descending.

4. **Component Mapping:** For each pattern cluster, record all distinct components (classes, pages, namespaces) that appear in stack traces. Mark as `is_systemic = true` if 2+ components share the pattern.

5. **Temporal Analysis:** Bin occurrences by hour. Determine trend: count in last quarter vs first quarter of time range. Label INCREASING, STABLE, or DECREASING.

6. **Root Cause Hypothesis:** For systemic patterns, identify shared infrastructure (e.g., same DB connection, same Redis node, same external API). For isolated patterns, point to likely component-level defect.

7. **Output Assembly:** Produce structured output with patterns, systemic issues, and per-pattern summary. Set confidence based on sample size and trace completeness.

## Example

**Input:**
```yaml
log_entries: "<500 log lines from OrderService and ShippingModule>"
min_frequency: 5
component_scope: ["AajLogistics.Orders", "AajLogistics.Shipping"]
```

**Output:**
```yaml
patterns_found:
  - pattern_id: P1
    name: "DB Connection Timeout"
    exception_type: SqlException
    frequency: 143
    affected_components: [OrderRepository, ShippingRepository, CarrierRepository]
    is_systemic: true
    common_root_cause: "SQL Server connection pool exhaustion or lock contention affecting all repositories"
    representative_stack: "SqlCommand.ExecuteReader > Repository.Query > Page_Load"
  - pattern_id: P2
    name: "Order Null Reference"
    exception_type: NullReferenceException
    frequency: 58
    affected_components: [OrderProcessor]
    is_systemic: false
    common_root_cause: "OrderProcessor receives null Order object — guard clause missing"
    representative_stack: "OrderProcessor.Submit > OrderValidator.Validate"
systemic_issues:
  - issue: "SQL Server connection issues affecting all data access layers"
    pattern_ids: [P1]
    shared_cause: "All three repositories use same connection string and pool"
per_pattern_summary:
  - pattern_id: P1
    trend: INCREASING
    first_seen: "2026-04-05T08:00Z"
    last_seen: "2026-04-05T14:00Z"
  - pattern_id: P2
    trend: STABLE
    first_seen: "2026-04-05T09:15Z"
    last_seen: "2026-04-05T13:45Z"
confidence: HIGH
```

---

**Related Skills:**
- `production-log-analyzer` - Analyzes a single log file for error patterns and root causes
- `bug-classifier` - Classifies detected patterns into bug types with severity
- `change-history-analyzer` - Correlates patterns with recent code or deployment changes
- `production-impact-assessor` - Quantifies business impact of systemic error patterns
