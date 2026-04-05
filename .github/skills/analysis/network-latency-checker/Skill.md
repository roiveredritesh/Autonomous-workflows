---
name: network-latency-checker
description: Checks network latency between the ASP.NET WebForms app server and external dependencies (SQL Server, Redis, external APIs) to isolate network-level performance issues.
---

# Network Latency Checker

## Quick Example

**Input:** App server connection to SQL Server, Redis, and ShipStation API
**Output:** SQL Server P95=4ms (OK), Redis P95=1ms (OK), ShipStation API P95=1800ms (CRITICAL — external bottleneck)
**Time:** 1-3 minutes

---

## Purpose
Checks network latency between the ASP.NET WebForms app server and external dependencies (SQL Server, Redis, external APIs) to isolate network-level performance issues.

## Input

```yaml
input:
  dependencies:
    - name: <friendly name>
      type: SQL_SERVER|REDIS|HTTP_API|FILE_SHARE|OTHER
      connection_string_or_url: <connection string or URL>
  sample_request_count: <number of pings/requests per dependency, default 20>
  timeout_ms: <max wait per sample, default 5000>
  test_operation: <optional — specific SQL query, Redis PING, HTTP GET path>
```

## Output

```yaml
output:
  results:
    - dependency: <name>
      type: <SQL_SERVER|REDIS|HTTP_API>
      status: HEALTHY|DEGRADED|UNREACHABLE
      latency_ms:
        min: <ms>
        p50: <ms>
        p95: <ms>
        p99: <ms>
        max: <ms>
      packet_loss_percent: <%>
      timeout_count: <count>
      verdict: OK|HIGH|CRITICAL
  summary:
    worst_dependency: <name>
    network_is_bottleneck: true|false
    total_external_overhead_p95_ms: <sum of P95 per dependency>
  recommendations:
    - dependency: <name>
      action: <optimization suggestion>
      priority: critical|high|medium
  confidence: HIGH|MEDIUM|LOW
```

## DO:
✅ Test with realistic payloads — not just PING — to capture serialization overhead
✅ Measure P95 and P99 as they reveal tail latency that causes user-visible slowness
✅ Test during production-like load conditions, not idle
✅ Repeat measurements 20+ times to get statistically meaningful percentiles
✅ Separate network latency from server processing time

## DON'T:
❌ Use PING (ICMP) alone — TCP connection latency is what matters for app dependencies
❌ Test from your dev machine — always test from the app server
❌ Ignore packet loss — even 0.1% packet loss can cause major TCP retransmissions
❌ Accept a single measurement as representative — use percentiles
❌ Conflate DNS resolution time with connection latency

## Error Conditions

**IF dependency is unreachable:**
```
1. Check firewall rules and network security groups
2. Verify connection string hostname/IP is correct
3. Return: UNREACHABLE — <dependency name> — cannot establish TCP connection
```

**IF latency is extremely high (>1000ms P50):**
```
1. Check if dependency is in different datacenter/region
2. Check for DNS resolution issues
3. Return: NETWORK_DEGRADED — possible routing issue or geographic distance
```

**IF test cannot run from app server (no access):**
```
1. Request network team to run latency test
2. Use Application Insights dependency tracking as proxy
3. Return: REMOTE_TEST_REQUIRED — cannot run latency check from app server directly
```

## Processing Steps

1. **Dependency Inventory:** List all external dependencies with their connection info. Categorize as SQL Server, Redis, HTTP API, file share, or other.

2. **Connection Test:** For each dependency: establish TCP connection to host:port. Record connection time. Do not send data yet. Record if connection fails.

3. **Operation Test:** Send a minimal real operation: SQL → `SELECT 1`, Redis → `PING`, HTTP API → `GET /health`. Record round-trip time including serialization.

4. **Percentile Calculation:** After N samples, calculate min, P50, P95, P99, max latency. Calculate packet loss as (timeouts / total samples).

5. **Verdict Assignment:** P95 thresholds: OK <10ms (DB/Redis), OK <200ms (HTTP), HIGH 10-50ms (DB), HIGH 200-1000ms (HTTP), CRITICAL >50ms (DB/Redis), CRITICAL >1000ms (HTTP).

6. **Bottleneck Determination:** Sum P95 latencies across all dependencies. If sum exceeds 20% of observed page load time, flag `network_is_bottleneck: true`.

7. **Recommendations:** For each CRITICAL or HIGH verdict, recommend: connection pooling tuning, geographic co-location, circuit breaker, caching, or timeout adjustment.

## Example

**Input:**
```yaml
dependencies:
  - name: "SQL Server (Primary)"
    type: SQL_SERVER
    connection_string_or_url: "Server=db-prod-01;Database=AajLogistics;..."
  - name: "Redis Cache"
    type: REDIS
    connection_string_or_url: "redis-prod-01:6379"
  - name: "ShipStation API"
    type: HTTP_API
    connection_string_or_url: "https://ssapi.shipstation.com"
sample_request_count: 30
```

**Output:**
```yaml
results:
  - dependency: "SQL Server (Primary)"
    type: SQL_SERVER
    status: HEALTHY
    latency_ms: {min: 1, p50: 2, p95: 4, p99: 8, max: 15}
    packet_loss_percent: 0%
    timeout_count: 0
    verdict: OK
  - dependency: "Redis Cache"
    type: REDIS
    status: HEALTHY
    latency_ms: {min: 0, p50: 1, p95: 1, p99: 2, max: 3}
    packet_loss_percent: 0%
    timeout_count: 0
    verdict: OK
  - dependency: "ShipStation API"
    type: HTTP_API
    status: DEGRADED
    latency_ms: {min: 400, p50: 1200, p95: 1800, p99: 2400, max: 4800}
    packet_loss_percent: 0%
    timeout_count: 2
    verdict: CRITICAL
summary:
  worst_dependency: "ShipStation API"
  network_is_bottleneck: true
  total_external_overhead_p95_ms: 1805
recommendations:
  - dependency: "ShipStation API"
    action: "Cache shipping rate responses in Redis with 15-minute TTL — rates change infrequently"
    priority: critical
  - dependency: "ShipStation API"
    action: "Implement async rate fetching — decouple from page load critical path"
    priority: high
confidence: HIGH
```

---

**Related Skills:**
- `request-profiler` - Profiles the full request lifecycle including network calls
- `performance-profiler` - Establishes baselines that include external dependency time
- `redis-behavior-checker` - Deep analysis of Redis connection health and operations
- `cache-miss-detector` - Identifies opportunities to cache external API responses
