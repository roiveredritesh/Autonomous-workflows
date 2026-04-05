# Skills Directory

## Overview
28 specialized skills organized by category for autonomous workflow execution with GitHub Copilot.

All skills follow the **v2.0.0 standard** with YAML frontmatter, quick examples, DO/DON'T lists, and error handling.

---

## Folder Structure

```
skills/
├── analysis/        # 6 skills - Analyze existing code and situations
├── planning/        # 5 skills - Create implementation or resolution plans
├── generation/      # 5 skills - Generate artifacts and documentation
├── validation/      # 4 skills - Validate and extract requirements
├── webforms/        # 4 skills - ASP.NET WebForms and Telerik specific
└── data/            # 4 skills - Data access, caching, and performance
```

Each skill: `{category}/{skill-name}/Skill.md`

---

## Skills by Category

### Analysis (6 skills)
Skills that analyze existing code, situations, or requirements:

| Skill | Purpose | Time |
|-------|---------|------|
| **story-analyzer** | Examines current story state and identifies gaps | 30-60s |
| **bug-classifier** | Classifies bugs by severity and type | 30-60s |
| **bug-impact-analyzer** | Assesses bug scope and user impact | 1-2min |
| **production-impact-assessor** | Evaluates production incidents | 30-60s |
| **feature-feasibility-analyzer** | Evaluates technical feasibility | 2-3min |
| **performance-profiler** | Establishes performance baselines | 2-3min |

### Planning (5 skills)
Skills that create implementation or resolution plans:

| Skill | Purpose | Time |
|-------|---------|------|
| **minimal-diff-planner** | Plans minimal focused changes | 3-5min |
| **minimal-fix-planner** | Plans minimal bug fixes | 2-3min |
| **emergency-mitigation-planner** | Develops immediate stabilization | 1-2min |
| **hotfix-strategy-planner** | Determines fastest safe resolution | 2-4min |
| **spike-charter** | Creates focused research investigations | 2-3min |

### Generation (5 skills)
Skills that generate artifacts, criteria, or documentation:

| Skill | Purpose | Time |
|-------|---------|------|
| **acceptance-criteria-generator** | Creates testable acceptance criteria | 1-2min |
| **acceptance-criteria-expander** | Expands criteria with edge cases | 2-3min |
| **test-scenario-generator** | Creates comprehensive test scenarios | 2-3min |
| **rollback-plan-generator** | Creates detailed rollback procedures | 1-2min |
| **spike-findings-recorder** | Documents investigation findings | 1-2min |

### Validation (4 skills)
Skills that validate, check, or extract requirements:

| Skill | Purpose | Time |
|-------|---------|------|
| **requirement-extractor** | Extracts functional/non-functional requirements | 1-2min |
| **edge-case-detector** | Identifies boundary conditions | 2-3min |
| **safe-change-boundary-detector** | Identifies safe modification points | 1-2min |
| **jira-story-intake** | Validates and extracts JIRA ticket info | 30-60s |

### WebForms (4 skills)
Skills specific to ASP.NET WebForms and Telerik:

| Skill | Purpose | Time |
|-------|---------|------|
| **webforms-lifecycle-analyzer** | Analyzes WebForms page lifecycle impact | 1-2min |
| **webforms-regression-analyzer** | Identifies WebForms regression risks | 2-3min |
| **telerik-behavior-analyzer** | Analyzes Telerik control behavior | 1-2min |
| **telerik-impact-checker** | Validates Telerik compatibility | 30-90s |

### Data (4 skills)
Skills related to data access, caching, and performance:

| Skill | Purpose | Time |
|-------|---------|------|
| **linq-query-tracer** | Analyzes LINQ query efficiency | 2-3min |
| **sql-impact-analyzer** | Evaluates database change impacts | 2-3min |
| **redis-cache-strategy-analyzer** | Analyzes Redis caching strategies | 2-3min |
| **cache-invalidation-mapper** | Maps cache invalidation points | 2-3min |

---

## How Skills Are Used

### By Agents
Agents invoke skills as part of their workflow execution:

**Feature Delivery Agent** uses:
- jira-story-intake, acceptance-criteria-expander, feature-feasibility-analyzer
- webforms-lifecycle-analyzer, telerik-impact-checker, safe-change-boundary-detector
- linq-query-tracer, sql-impact-analyzer, redis-cache-strategy-analyzer
- minimal-diff-planner, test-scenario-generator, rollback-plan-generator

**Bug Fix Agent** uses:
- bug-classifier, bug-impact-analyzer, minimal-fix-planner
- webforms-lifecycle-analyzer, webforms-regression-analyzer
- safe-change-boundary-detector, test-scenario-generator

**Hotfix Agent** uses:
- production-impact-assessor, emergency-mitigation-planner
- hotfix-strategy-planner, minimal-fix-planner, rollback-plan-generator

**Performance Agent** uses:
- performance-profiler, linq-query-tracer, sql-impact-analyzer
- redis-cache-strategy-analyzer, cache-invalidation-mapper

**Spike Agent** uses:
- spike-charter, spike-findings-recorder
- webforms-lifecycle-analyzer, telerik-behavior-analyzer
- linq-query-tracer, sql-impact-analyzer

**Story Refinement Agent** uses:
- story-analyzer, requirement-extractor
- acceptance-criteria-generator, edge-case-detector

### Direct Invocation
You can request specific skills:
```
"Use linq-query-tracer to analyze the customer search query"
"Use feature-feasibility-analyzer to evaluate adding real-time updates"
"Use minimal-diff-planner to plan the Excel export implementation"
```

---

## Skill Standard (v2.0.0)

Every skill includes:

```yaml
---
skill: skill-name
version: 2.0.0
category: analysis|planning|generation|validation
complexity: low|medium|high
estimated_time: 30-90s | 1-4min | 3-10min
priority: critical|high|medium|low
last_updated: YYYY-MM-DD
---
```

**Quick Example** (first 30 lines)
- Input example
- Output example
- Typical execution time

**Structure:**
- Purpose (what it does)
- Input format (YAML)
- Output format (YAML)
- DO list (best practices)
- DON'T list (anti-patterns)
- Error conditions (IF/THEN handling)
- Complete examples
- Related skills

**See:** `SKILL_TEMPLATE.md` for the standard format

---

## Skill Cross-References

### Requirement Extraction Pipeline
```
story-analyzer
  → requirement-extractor
    → acceptance-criteria-generator
      → edge-case-detector
        → test-scenario-generator
```

### Feature Delivery Pipeline
```
jira-story-intake
  → feature-feasibility-analyzer
    → webforms-lifecycle-analyzer & telerik-impact-checker
      → minimal-diff-planner
        → test-scenario-generator
          → rollback-plan-generator
```

### Bug Fix Pipeline
```
bug-classifier
  → bug-impact-analyzer
    → minimal-fix-planner
      → safe-change-boundary-detector
        → webforms-regression-analyzer
          → test-scenario-generator
```

### Performance Optimization Pipeline
```
performance-profiler
  → linq-query-tracer & sql-impact-analyzer
    → redis-cache-strategy-analyzer
      → cache-invalidation-mapper
        → minimal-diff-planner
```

### Hotfix Pipeline
```
production-impact-assessor
  → emergency-mitigation-planner
    → hotfix-strategy-planner
      → minimal-fix-planner
        → rollback-plan-generator
```

---

## Usage Guidelines

### For Feature Delivery
1. Start with `jira-story-intake` to validate ticket
2. Use `feature-feasibility-analyzer` to assess approach
3. Check with `webforms-lifecycle-analyzer` and `telerik-impact-checker`
4. Plan changes with `minimal-diff-planner`
5. Create tests with `test-scenario-generator`
6. Always generate `rollback-plan-generator`

### For Bug Fixes
1. Start with `bug-classifier` to categorize
2. Use `bug-impact-analyzer` to understand scope
3. Plan fix with `minimal-fix-planner`
4. Verify safety with `safe-change-boundary-detector`
5. Plan regression tests with `webforms-regression-analyzer`

### For Production Issues
1. Start with `production-impact-assessor`
2. Use `emergency-mitigation-planner` for immediate relief
3. Use `hotfix-strategy-planner` for approach
4. Always use `rollback-plan-generator` for safety

### For Performance Issues
1. Start with `performance-profiler` to baseline
2. Trace with `linq-query-tracer` and `sql-impact-analyzer`
3. Design caching with `redis-cache-strategy-analyzer`
4. Map invalidation with `cache-invalidation-mapper`

---

## Maintenance Notes

- **Skills are self-contained** but reference related skills
- **Each skill has specific input/output contracts**
- **All skills support YAML formatting** for consistency
- **Skills designed to chain together** in typical workflows
- **Ready for automation/tool integration**

---

## Success Metrics

This skill set enables:
- ✅ Structured workflow for all delivery modes
- ✅ Comprehensive risk management
- ✅ Legacy system safety (WebForms-specific)
- ✅ Time-boxed investigations (spikes)
- ✅ Rapid incident response (hotfixes)
- ✅ Quality assurance through comprehensive testing
- ✅ Proper change tracking and rollback capability

---

## Related Documentation

- **Agents:** `../agents/` - Workflow orchestration
- **Integration:** `../instructions/quick-start-guide.md` - How to use with Copilot
- **Standards:** `../copilot-instructions.md` - C# coding standards
- **Templates:** `../instructions/output-templates.md` - Output formatting

**Last Updated:** 2026-03-28
