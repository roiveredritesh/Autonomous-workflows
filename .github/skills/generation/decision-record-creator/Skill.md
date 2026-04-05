---
name: decision-record-creator
description: Creates Architecture Decision Records (ADRs) documenting technical choices and their rationale for future reference and team alignment.
---

# Decision Record Creator

## Quick Example

**Input:** Decision to use Redis for customer search result caching, options considered: Redis vs In-Memory vs SQL Server output cache, chose Redis for distributed deployment support
**Output:** Formatted ADR document with context, options table, decision, consequences, and review date
**Time:** 1-2 minutes

---

## Purpose
Creates Architecture Decision Records (ADRs) documenting technical choices and their rationale for future reference and team alignment.

## Input

```yaml
input:
  decision_title: <short title for the decision>
  context: <what problem or situation prompted this decision>
  options_considered:
    - name: <option name>
      pros: [<list>]
      cons: [<list>]
  chosen_option: <which option was selected>
  rationale: <why this option was chosen over the others>
  consequences:
    positive: [<expected positive outcomes>]
    negative: [<trade-offs or downsides>]
    risks: [<risks to monitor>]
  decision_makers: [<names or roles>]
  ticket_id: <optional — related ticket>
  review_date: <when to revisit this decision>
```

## Output

```yaml
output:
  adr_document:
    id: <ADR-{sequence}>
    title: <formatted title>
    status: ACCEPTED|PROPOSED|DEPRECATED|SUPERSEDED
    date: <ISO date>
    decision_makers: [<list>]
  formatted_adr: |
    # ADR-{id}: {title}
    
    **Status:** ACCEPTED  
    **Date:** {date}  
    **Deciders:** {names}
    
    ## Context
    {context}
    
    ## Options Considered
    | Option | Pros | Cons |
    ...
    
    ## Decision
    {chosen_option} — {rationale}
    
    ## Consequences
    ...
  trade_off_summary:
    accepted_tradeoffs: [<list>]
    monitoring_needed: [<list>]
  confidence: HIGH|MEDIUM|LOW
```

## DO:
✅ Write context in present tense describing the situation at decision time
✅ Include all options seriously considered — rejected options provide context
✅ Be explicit about trade-offs accepted — future readers need to know
✅ Set a review date — decisions made today may be wrong in 6 months
✅ Reference related tickets and other ADRs that this decision depends on

## DON'T:
❌ Document decisions that are obvious or have no real alternatives
❌ Write ADRs for implementation details — reserve for architectural decisions
❌ Leave consequences section vague — list specific expected outcomes
❌ Skip rejected options — they're often as valuable as the chosen option
❌ Make ADRs longer than 2 pages — conciseness increases usage

## Error Conditions

**IF only one option was considered:**
```
1. Document as decision anyway — note that alternatives were not evaluated
2. Flag: SINGLE_OPTION — recommend revisiting with alternatives before finalizing
```

**IF rationale is unclear:**
```
1. Document with PROPOSED status
2. Note: RATIONALE_PENDING — decision needs team review before ACCEPTED
```

## Processing Steps

1. **ADR ID:** Assign sequential ID based on existing ADRs in repository (ADR-001, ADR-002, etc.). If no existing ADRs, start at ADR-001.

2. **Context Writing:** Describe the situation that forced a decision. Include: current system state, the problem being solved, constraints (legacy WebForms, Redis available, SQL Server, Telerik).

3. **Options Table:** Format as markdown table with columns: Option, Description, Pros, Cons. Include at least 2 options (chosen + at least one alternative).

4. **Decision Statement:** One clear sentence: "We will use {chosen_option} because {rationale}." Avoid hedge words like "we might" or "we could".

5. **Consequences:** List concrete outcomes: what becomes easier, what becomes harder, what new risks are introduced. Be honest about trade-offs.

6. **Review Date:** Set based on decision type: technology choice → 12 months, performance optimization → 6 months, security decision → 3 months.

7. **Formatted ADR:** Assemble into standard ADR markdown format ready to commit to `/docs/adr/` or equivalent.

## Example

**Input:**
```yaml
decision_title: "Use Redis for Distributed Customer Search Result Caching"
context: "Customer search is slow (8s). We need to cache results. The app runs on 3 web servers. We need a cache that all servers share."
options_considered:
  - name: "In-Memory Cache (HttpRuntime.Cache)"
    pros: ["No infrastructure cost", "Sub-millisecond access"]
    cons: ["Per-server — 3 servers = 3 separate caches", "Cache warms independently per server"]
  - name: "Redis Distributed Cache"
    pros: ["Shared across all servers", "TTL management", "Already licensed"]
    cons: ["Network latency (~2ms)", "Infrastructure dependency"]
  - name: "SQL Server Output Cache"
    pros: ["No new infrastructure"]
    cons: ["High DB load", "Slow reads — defeats purpose"]
chosen_option: "Redis Distributed Cache"
rationale: "Only Redis provides shared cache across all 3 web servers. In-memory is per-server and causes inconsistent results. Redis is already available."
consequences:
  positive: ["Consistent search results across all servers", "Reduced DB load"]
  negative: ["2ms Redis latency overhead per cache hit"]
  risks: ["Redis unavailability falls back to DB (must handle gracefully)"]
review_date: "2027-04-05"
```

**Output:**
```yaml
adr_document:
  id: "ADR-007"
  title: "Use Redis for Distributed Customer Search Result Caching"
  status: ACCEPTED
  date: "2026-04-05"
  decision_makers: [Team]
formatted_adr: |
  # ADR-007: Use Redis for Distributed Customer Search Result Caching
  
  **Status:** ACCEPTED  
  **Date:** 2026-04-05  
  **Review Date:** 2027-04-05
  
  ## Context
  Customer search takes 8 seconds due to unindexed SQL query on 45,000 rows. We need to cache results to reduce DB load. The application runs on 3 web servers and requires a shared cache to prevent inconsistent results between servers.
  
  ## Options Considered
  | Option | Pros | Cons |
  |--------|------|------|
  | In-Memory Cache | No infrastructure cost, sub-ms access | Per-server — inconsistent results across 3 servers |
  | Redis Distributed Cache | Shared across servers, TTL management, already licensed | 2ms network overhead |
  | SQL Server Output Cache | No new infrastructure | Adds DB load, slow — defeats the purpose |
  
  ## Decision
  We will use Redis Distributed Cache because it is the only option providing shared state across all 3 web servers, preventing inconsistent search results.
  
  ## Consequences
  **Positive:** Consistent results across servers; reduced DB query load by ~70%.  
  **Negative:** 2ms Redis latency overhead on cache hits.  
  **Risks:** Redis unavailability must fall back gracefully to DB queries.
trade_off_summary:
  accepted_tradeoffs: ["2ms latency overhead accepted for consistency and DB protection"]
  monitoring_needed: ["Redis availability monitoring", "Cache hit rate monitoring"]
confidence: HIGH
```

---

**Related Skills:**
- `change-log-generator` - Generates the changelog entry for the feature this ADR supports
- `risk-documentation-generator` - Generates risk register entries for risks identified in ADR
- `pr-metadata-generator` - References relevant ADRs in PR descriptions
- `spike-findings-recorder` - Spike output often leads to an ADR for the chosen approach
