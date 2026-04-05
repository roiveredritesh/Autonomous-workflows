---
name: sql-impact-analyzer
description: Evaluates how database schema changes impact queries, performance, and existing functionality.
---

## Purpose
Evaluates how database schema changes impact queries, performance, and existing functionality.

## Input Requirements
```yaml
change:
  type: <column_add|column_remove|table_create|table_drop|index>
  description: <what's changing>
  affected_tables: [<tables>]
  affected_queries: [<query names>]
```

## Processing Steps

1. **Identify Affected Queries**
   - Which queries use affected tables?
   - Which queries reference affected columns?

2. **Analyze Impact**
   - Will query still work?
   - Will performance change?
   - Are migrations needed?

3. **Plan Migration**
   - What data movement needed?
   - How to handle existing data?
   - Rollback strategy?

## Output Format

```yaml
sql_impact_analysis:
  
  change_analysis:
    change_type: <type>
    affected_tables: [<tables>]
    affected_columns: [<columns>]
  
  impacted_queries:
    - query: <query name>
      location: <file>
      impact: <will_break|will_change|unaffected>
      reason: <explanation>
    
    - query: <another>
      ...
  
  performance_impact:
    indexes_affected: [<indexes>]
    query_plans_changed: <yes|no>
    performance_estimate: <slower|faster|same>
  
  migration_plan:
    data_migration_needed: <yes|no>
    migration_steps:
      - step: <action>
    
    downtime_required: <minutes|hours>
    rollback_strategy: <strategy>
  
  recommendations:
    approach: <recommended approach>
    alternative_approaches: [<alternatives>]
    testing_needed: [<tests>]
```

## Related Skills
- `linq-query-tracer` - For LINQ impact
- `redis-cache-strategy-analyzer` - For caching impact
