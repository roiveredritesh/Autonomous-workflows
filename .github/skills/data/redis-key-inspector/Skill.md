---
name: redis-key-inspector
description: Inspects specific Redis keys for value, TTL, memory usage, and access patterns to diagnose caching issues in the ASP.NET WebForms application.
---

# Redis Key Inspector

## Quick Example

**Input:** Key `customer:search:active:north`, Redis connection prod
**Output:** Type: string, TTL: 47s remaining, Size: 2.8MB, Last access: 2s ago, Value: JSON array (truncated), Anomaly: value too large for effective caching
**Time:** 30-60 seconds

---

## Purpose
Inspects specific Redis keys for value, TTL, memory usage, and access patterns to diagnose caching issues in the ASP.NET WebForms application.

## Input

```yaml
input:
  key_name_or_pattern: <exact key name or glob pattern>
  redis_connection: <optional — connection string or StackExchange.Redis config>
  show_value_preview: <true|false — show first 200 chars of value, default true>
  max_keys_to_inspect: <limit for pattern queries, default 10>
```

## Output

```yaml
output:
  keys_inspected:
    - key: <exact key name>
      exists: true|false
      type: string|hash|list|set|zset
      ttl_seconds_remaining: <seconds or -1 for no expiry or -2 for missing>
      ttl_status: HEALTHY|EXPIRING_SOON|NO_EXPIRY|MISSING
      size_bytes: <bytes>
      size_human: <KB or MB>
      last_access_seconds_ago: <via OBJECT IDLETIME>
      encoding: <embstr|raw|ziplist|hashtable|etc>
      value_preview: <first 200 chars or field list for hashes>
      anomalies:
        - type: VALUE_TOO_LARGE|NO_TTL|WRONG_TYPE|EXPIRED|LOW_IDLETIME
          description: <detail>
          severity: HIGH|MEDIUM|LOW
  summary:
    total_size_bytes: <sum>
    any_anomalies: true|false
    recommendations:
      - action: <description>
        priority: critical|high|medium
  confidence: HIGH|MEDIUM|LOW
```

## DO:
✅ Use `OBJECT ENCODING` to understand memory layout (ziplist is more compact than hashtable)
✅ Check `OBJECT IDLETIME` to verify the key is actually being accessed
✅ Verify TTL is set — keys without TTL accumulate indefinitely
✅ Compare key size against expected size — large values indicate missing DTO projection
✅ Check if the value type matches what the application expects (string vs hash)

## DON'T:
❌ Dump the full value for large keys — use GETRANGE or HKEYS for inspection
❌ Modify key TTL or value during inspection — read-only analysis only
❌ Inspect thousands of keys in production without SCAN (use SCAN not KEYS)
❌ Delete keys during inspection — document and recommend deletion separately
❌ Expose sensitive PII from key values in the output

## Error Conditions

**IF key does not exist:**
```
1. Check if TTL has expired (key may have recently expired)
2. Check if key name format is correct (casing, separator)
3. Return: KEY_NOT_FOUND — TTL: -2 (expired or never existed)
```

**IF Redis is not accessible:**
```
1. Verify connection string and network connectivity
2. Try redis-cli from app server: redis-cli -h <host> ping
3. Return: REDIS_UNREACHABLE — check Redis server and firewall
```

**IF pattern matches too many keys:**
```
1. Warn: LARGE_RESULT — limiting to max_keys_to_inspect
2. Use SCAN with COUNT to sample safely
3. Report: Only first N keys inspected
```

## Processing Steps

1. **Key Resolution:** If exact key, proceed directly. If pattern, use `SCAN 0 MATCH <pattern> COUNT 100` to safely enumerate. Limit to `max_keys_to_inspect`.

2. **Existence Check:** `EXISTS <key>` → 1 (exists) or 0 (missing). If missing, record `ttl_seconds_remaining: -2`.

3. **Type Check:** `TYPE <key>` → string, hash, list, set, zset. Verify matches expected type from application code.

4. **TTL Check:** `TTL <key>` → remaining seconds, -1 (no expiry), -2 (doesn't exist). Flag no-expiry as anomaly for non-configuration data.

5. **Size Check:** For strings: `STRLEN <key>`. For hashes: `HLEN <key>` (field count) + `DEBUG OBJECT <key>` (serializedlength). For lists: `LLEN <key>`. Flag if > 100KB.

6. **Access Pattern:** `OBJECT IDLETIME <key>` → seconds since last access. High idletime (>TTL/2) suggests key is not being accessed as expected.

7. **Value Preview:** For strings: `GETRANGE <key> 0 199` (first 200 chars). For hashes: `HKEYS <key>`. For lists: `LRANGE <key> 0 4`. Truncate and present safely.

8. **Anomaly Detection:** Flag: size >100KB (too large), no TTL (memory leak risk), idletime > TTL (not being used), wrong type (code/cache mismatch), size 0 (empty value cached).

## Example

**Input:**
```yaml
key_name_or_pattern: "customer:search:active:north"
show_value_preview: true
```

**Output:**
```yaml
keys_inspected:
  - key: "customer:search:active:north"
    exists: true
    type: string
    ttl_seconds_remaining: 47
    ttl_status: EXPIRING_SOON
    size_bytes: 2867200
    size_human: "2.8 MB"
    last_access_seconds_ago: 2
    encoding: raw
    value_preview: '[{"Id":1,"CompanyName":"Aaj Freight Ltd","Status":"Active","Region":"North","Email":"contact@aaj...'
    anomalies:
      - type: VALUE_TOO_LARGE
        description: "2.8MB value — serialized full CustomerEntity list with navigation properties. Expected <50KB for search results."
        severity: HIGH
      - type: EXPIRING_SOON
        description: "47 seconds remaining — stampede risk if 50+ users hit this simultaneously on expiry"
        severity: MEDIUM
summary:
  total_size_bytes: 2867200
  any_anomalies: true
  recommendations:
    - action: "Project to CustomerSearchDto (12 fields) before caching — estimated size reduction from 2.8MB to 45KB"
      priority: high
    - action: "Add TTL jitter: base 300s ± 45s to prevent cache stampede on expiry"
      priority: medium
confidence: HIGH
```

---

**Related Skills:**
- `redis-key-strategy-analyzer` - Analyzes key naming patterns and TTL strategy
- `redis-behavior-checker` - Verifies hit/miss rates and overall Redis health
- `serialization-overhead-checker` - Analyzes why values are larger than expected
- `cache-stampede-detector` - Assesses stampede risk for expiring keys
