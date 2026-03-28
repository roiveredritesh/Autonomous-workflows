# Skills Reorganization Plan

## Overview
Reorganizing 28 skills from flat structure to categorized folder structure for better organization and discoverability.

## Proposed Structure

### Category 1: Analysis (6 skills)
Skills that analyze existing code, situations, or requirements:

| Current File | New Location | Purpose |
|--------------|-------------|---------|
| story-analyzer.skill.md | analysis/story-analyzer/Skill.md | Examines current story state |
| bug-classifier.skill.md | analysis/bug-classifier/Skill.md | Classifies bugs by severity |
| bug-impact-analyzer.skill.md | analysis/bug-impact-analyzer/Skill.md | Assesses bug scope and impact |
| production-impact-assessor.skill.md | analysis/production-impact-assessor/Skill.md | Evaluates production incidents |
| feature-feasibility-analyzer.skill.md | analysis/feature-feasibility-analyzer/Skill.md | Evaluates technical feasibility |
| performance-profiler.skill.md | analysis/performance-profiler/Skill.md | Establishes baselines and bottlenecks |

### Category 2: Planning (5 skills)
Skills that create implementation or resolution plans:

| Current File | New Location | Purpose |
|--------------|-------------|---------|
| minimal-diff-planner.skill.md | planning/minimal-diff-planner/Skill.md | Plans minimal focused changes |
| minimal-fix-planner.skill.md | planning/minimal-fix-planner/Skill.md | Plans minimal bug fixes |
| emergency-mitigation-planner.skill.md | planning/emergency-mitigation-planner/Skill.md | Develops immediate stabilization |
| hotfix-strategy-planner.skill.md | planning/hotfix-strategy-planner/Skill.md | Determines fastest safe resolution |
| spike-charter.skill.md | planning/spike-charter/Skill.md | Creates focused research investigations |

### Category 3: Generation (5 skills)
Skills that generate artifacts, criteria, or documentation:

| Current File | New Location | Purpose |
|--------------|-------------|---------|
| acceptance-criteria-generator.skill.md | generation/acceptance-criteria-generator/Skill.md | Creates testable acceptance criteria |
| acceptance-criteria-expander.skill.md | generation/acceptance-criteria-expander/Skill.md | Expands criteria with edge cases |
| test-scenario-generator.skill.md | generation/test-scenario-generator/Skill.md | Creates comprehensive test scenarios |
| rollback-plan-generator.skill.md | generation/rollback-plan-generator/Skill.md | Creates detailed rollback procedures |
| spike-findings-recorder.skill.md | generation/spike-findings-recorder/Skill.md | Documents investigation findings |

### Category 4: Validation (4 skills)
Skills that validate, check, or extract requirements:

| Current File | New Location | Purpose |
|--------------|-------------|---------|
| requirement-extractor.skill.md | validation/requirement-extractor/Skill.md | Extracts functional/non-functional requirements |
| edge-case-detector.skill.md | validation/edge-case-detector/Skill.md | Identifies boundary conditions |
| safe-change-boundary-detector.skill.md | validation/safe-change-boundary-detector/Skill.md | Identifies safe modification points |
| jira-story-intake.skill.md | validation/jira-story-intake/Skill.md | Validates and extracts JIRA ticket info |

### Category 5: WebForms (4 skills)
Skills specific to ASP.NET WebForms and Telerik:

| Current File | New Location | Purpose |
|--------------|-------------|---------|
| webforms-lifecycle-analyzer.skill.md | webforms/webforms-lifecycle-analyzer/Skill.md | Analyzes WebForms lifecycle impact |
| webforms-regression-analyzer.skill.md | webforms/webforms-regression-analyzer/Skill.md | Identifies WebForms regression risks |
| telerik-behavior-analyzer.skill.md | webforms/telerik-behavior-analyzer/Skill.md | Analyzes Telerik control behavior |
| telerik-impact-checker.skill.md | webforms/telerik-impact-checker/Skill.md | Validates Telerik compatibility |

### Category 6: Data (4 skills)
Skills related to data access, caching, and performance:

| Current File | New Location | Purpose |
|--------------|-------------|---------|
| linq-query-tracer.skill.md | data/linq-query-tracer/Skill.md | Analyzes LINQ query efficiency |
| sql-impact-analyzer.skill.md | data/sql-impact-analyzer/Skill.md | Evaluates database change impacts |
| redis-cache-strategy-analyzer.skill.md | data/redis-cache-strategy-analyzer/Skill.md | Analyzes Redis caching strategies |
| cache-invalidation-mapper.skill.md | data/cache-invalidation-mapper/Skill.md | Maps cache invalidation points |

## Folder Structure

```
skills/
├── analysis/
│   ├── story-analyzer/
│   │   └── Skill.md
│   ├── bug-classifier/
│   │   └── Skill.md
│   ├── bug-impact-analyzer/
│   │   └── Skill.md
│   ├── production-impact-assessor/
│   │   └── Skill.md
│   ├── feature-feasibility-analyzer/
│   │   └── Skill.md
│   └── performance-profiler/
│       └── Skill.md
├── planning/
│   ├── minimal-diff-planner/
│   │   └── Skill.md
│   ├── minimal-fix-planner/
│   │   └── Skill.md
│   ├── emergency-mitigation-planner/
│   │   └── Skill.md
│   ├── hotfix-strategy-planner/
│   │   └── Skill.md
│   └── spike-charter/
│       └── Skill.md
├── generation/
│   ├── acceptance-criteria-generator/
│   │   └── Skill.md
│   ├── acceptance-criteria-expander/
│   │   └── Skill.md
│   ├── test-scenario-generator/
│   │   └── Skill.md
│   ├── rollback-plan-generator/
│   │   └── Skill.md
│   └── spike-findings-recorder/
│       └── Skill.md
├── validation/
│   ├── requirement-extractor/
│   │   └── Skill.md
│   ├── edge-case-detector/
│   │   └── Skill.md
│   ├── safe-change-boundary-detector/
│   │   └── Skill.md
│   └── jira-story-intake/
│       └── Skill.md
├── webforms/
│   ├── webforms-lifecycle-analyzer/
│   │   └── Skill.md
│   ├── webforms-regression-analyzer/
│   │   └── Skill.md
│   ├── telerik-behavior-analyzer/
│   │   └── Skill.md
│   └── telerik-impact-checker/
│       └── Skill.md
└── data/
    ├── linq-query-tracer/
    │   └── Skill.md
    ├── sql-impact-analyzer/
    │   └── Skill.md
    ├── redis-cache-strategy-analyzer/
    │   └── Skill.md
    └── cache-invalidation-mapper/
        └── Skill.md
```

## Agent Reference Updates Required

All 7 agents will need to update skill references from:
- `skills/skill-name.skill.md`
TO:
- `skills/{category}/{skill-name}/Skill.md`

## Implementation Steps

1. ✅ Create reorganization plan document
2. Create new folder structure (6 categories × skill folders)
3. Copy skill files to new locations with Skill.md naming
4. Update all 7 agent files with new skill paths
5. Remove old flat skill files
6. Update README.md to reflect new structure
7. Test agent references

## Benefits

- **Better Organization**: Skills grouped by function
- **Easier Discovery**: Category folders make it clear what type of skill to use
- **Scalability**: Easy to add new skills to appropriate categories
- **Clarity**: Following user's example pattern (`/skills/data/linq-optimizer/Skill.md`)
