---
name: dependency-mapper
description: Maps dependencies between components, services, and external systems to understand impact radius before making changes.
---

# Dependency Mapper

## Quick Example

**Input:** `CustomerRepository` class
**Output:** Direct deps: DbContext, RedisCache, ILogger. Transitive: SQL Server, Redis node. Callers: 7 pages, 3 services. Circular: none. External: SQL Server, Redis
**Time:** 3-5 minutes

---

## Purpose
Maps dependencies between components, services, and external systems to understand impact radius before making changes.

## Input

```yaml
input:
  component_name: <class name, file path, or module name>
  direction: INBOUND|OUTBOUND|BOTH
  depth: <how many levels of transitive deps to trace, default 2>
  include_external: <true|false — include SQL Server, Redis, APIs, default true>
  scope: <optional — limit to namespace or project>
```

## Output

```yaml
output:
  component: <name>
  direct_dependencies:
    - name: <class or service name>
      type: CLASS|INTERFACE|EXTERNAL_DB|EXTERNAL_API|REDIS|FILE
      coupling: TIGHT|LOOSE
      usage: <how it is used — injected, instantiated, called statically>
  transitive_dependencies:
    - name: <name>
      via: <direct dependency that pulls this in>
      depth: <1|2|3>
  inbound_callers:
    - name: <class or page>
      type: ASPX_PAGE|CODE_BEHIND|SERVICE|REPOSITORY|TEST
      call_count_estimate: <per request or per day>
  circular_dependencies:
    - cycle: [<A>, <B>, <C>, <A>]
      severity: HIGH|MEDIUM
  external_systems:
    - system: <SQL Server|Redis|ShipStation API|etc>
      via_component: <which class makes the call>
      operation: READ|WRITE|READ_WRITE
  change_impact:
    safe_to_change: true|false
    must_notify: [<callers that need coordinating>]
    risk_level: HIGH|MEDIUM|LOW
  confidence: HIGH|MEDIUM|LOW
```

## DO:
✅ Map both inbound (who calls this) and outbound (what this calls) dependencies
✅ Distinguish between interface dependencies (loose) and concrete class dependencies (tight)
✅ Identify which ASPX pages are entry points that depend on this component
✅ Flag static method calls — they create hidden tight coupling
✅ Check for WebForms-specific coupling: event handlers, DataSource bindings, ObjectDataSource

## DON'T:
❌ Limit analysis to direct dependencies only — transitive deps matter for impact assessment
❌ Ignore infrastructure dependencies (SQL Server, Redis) — they affect change risk
❌ Miss ASP.NET-specific bindings in .aspx markup (DataSourceID, ObjectDataSource TypeName)
❌ Forget Global.asax and HttpModules — they depend on many components
❌ Underestimate the cost of circular dependencies in legacy WebForms code

## Error Conditions

**IF component not found in codebase:**
```
1. Check for namespace prefix or alternate casing
2. Search for partial match in class names
3. Return: COMPONENT_NOT_FOUND — verify class name and namespace
```

**IF codebase is too large for full transitive scan:**
```
1. Limit depth to 2 levels
2. Report: DEPTH_LIMITED — full transitive graph requires deeper scan
```

**IF circular dependency detected:**
```
1. Record all members of the cycle
2. Flag as HIGH severity — circular deps prevent safe unit testing and refactoring
3. Suggest breaking cycle via interface extraction
```

## Processing Steps

1. **Component Location:** Find the class/file in the codebase. Identify its namespace, base classes, and implemented interfaces.

2. **Outbound Mapping (What it depends on):** Scan constructor parameters (DI), field declarations, method calls. Identify: injected interfaces, concrete instantiations (`new X()`), static calls, `HttpContext` / `Session` / `Cache` usage.

3. **Inbound Mapping (Who depends on it):** Search codebase for: class name in constructors, ObjectDataSource TypeName in .aspx, DI registrations, `Page.FindControl` usage, event handler wiring.

4. **Transitive Expansion:** For each direct dependency, recurse to find their dependencies up to specified depth. Note the path (via chain).

5. **External System Identification:** Within dependency tree, identify connections to: SQL Server (SqlConnection, DbContext), Redis (StackExchange.Redis), external APIs (HttpClient, WebRequest), file system.

6. **Circular Dependency Detection:** Build directed graph of all dependencies. Run DFS cycle detection. Report any cycles found.

7. **Change Impact Assessment:** Count inbound callers. Assess coupling type. If 3+ pages depend directly on this component, mark change_impact.risk_level as HIGH. If interface-based, MEDIUM. If well-isolated, LOW.

## Example

**Input:**
```yaml
component_name: "CustomerRepository"
direction: BOTH
depth: 2
include_external: true
```

**Output:**
```yaml
component: "CustomerRepository"
direct_dependencies:
  - name: "AajLogisticsDbContext"
    type: CLASS
    coupling: TIGHT
    usage: "Injected via constructor — used for all DB queries"
  - name: "IRedisCache"
    type: INTERFACE
    coupling: LOOSE
    usage: "Injected — used for customer search result caching"
  - name: "ILogger"
    type: INTERFACE
    coupling: LOOSE
    usage: "Injected — used for error logging"
transitive_dependencies:
  - name: "SQL Server"
    via: "AajLogisticsDbContext"
    depth: 2
  - name: "Redis"
    via: "IRedisCache → RedisCache"
    depth: 2
inbound_callers:
  - name: "CustomerSearch.aspx.cs"
    type: ASPX_PAGE
    call_count_estimate: "~50 per minute"
  - name: "CustomerDetailService"
    type: SERVICE
    call_count_estimate: "~20 per minute"
  - name: "OrderProcessor"
    type: SERVICE
    call_count_estimate: "~30 per minute"
circular_dependencies: []
external_systems:
  - system: "SQL Server"
    via_component: "AajLogisticsDbContext"
    operation: READ_WRITE
  - system: "Redis"
    via_component: "RedisCache"
    operation: READ_WRITE
change_impact:
  safe_to_change: true
  must_notify: ["CustomerSearch.aspx.cs", "CustomerDetailService", "OrderProcessor"]
  risk_level: MEDIUM
confidence: HIGH
```

---

**Related Skills:**
- `safe-change-boundary-detector` - Uses dependency map to determine safe change boundaries
- `api-contract-analyzer` - Validates public API contracts within identified dependency chain
- `bug-impact-analyzer` - Uses dependency map to assess blast radius of a bug
- `sql-impact-analyzer` - Maps dependencies on specific SQL tables and stored procedures
