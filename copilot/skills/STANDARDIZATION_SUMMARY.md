# Skills Standardization Summary

## Overview

Skills are being standardized to v2.0.0 format with consistent structure, YAML frontmatter, and best practices applied.

---

## Standard v2.0.0 Format

All standardized skills include:

1. ✅ **YAML Frontmatter** with metadata (skill, version, category, complexity, time, priority)
2. ✅ **Quick Example** at top (show input/output within first 30 lines)
3. ✅ **Clear Purpose** statement
4. ✅ **Structured Input/Output** in YAML format
5. ✅ **DO/DON'T Lists** for clear constraints
6. ✅ **Error Conditions** with explicit handling
7. ✅ **Complete Examples** showing usage
8. ✅ **Related Skills** references
9. ✅ **Target Length** 150-250 lines (complex skills up to 300 max)

---

## Standardization Progress

### Completed (v2.0.0) ✅

| Skill | Before | After | Status |
|-------|--------|-------|--------|
| bug-classifier | 334 lines | 179 lines | ✅ Refactored |
| production-impact-assessor | 152 lines | 157 lines | ✅ Refactored |
| safe-change-boundary-detector | 80 lines | 216 lines | ✅ Enhanced |

**Total:** 3 skills standardized (most critical ones)

---

### Pending Standardization (v1.0.0)

The following 25 skills are scheduled for standardization:

#### High Priority (Core Workflow Skills)
- `jira-story-intake` - Used by feature delivery
- `minimal-diff-planner` - Used by all agents (currently 447 lines - needs major streamlining)
- `feature-feasibility-analyzer` - Used by feature delivery
- `test-scenario-generator` - Used by multiple agents
- `rollback-plan-generator` - Used by all agents

#### Medium Priority (Specialized Analysis)
- `webforms-lifecycle-analyzer` - WebForms validation
- `linq-query-tracer` - Data analysis
- `performance-profiler` - Performance analysis
- `telerik-impact-checker` - Telerik validation
- `sql-impact-analyzer` - Database analysis
- `redis-cache-strategy-analyzer` - Cache analysis
- `cache-invalidation-mapper` - Cache validation
- `webforms-regression-analyzer` - Regression detection
- `telerik-behavior-analyzer` - Telerik analysis

#### Medium Priority (Planning & Generation)
- `hotfix-strategy-planner` - Used by hotfix agent
- `emergency-mitigation-planner` - Used by hotfix agent
- `minimal-fix-planner` - Used by bug-fix agent
- `acceptance-criteria-generator` - Used by refinement agent
- `acceptance-criteria-expander` - Used by feature delivery
- `requirement-extractor` - Used by refinement agent
- `spike-charter` - Used by spike agent
- `spike-findings-recorder` - Used by spike agent

#### Lower Priority (Specialized Detection)
- `edge-case-detector` - Used by refinement agent
- `bug-impact-analyzer` - Used by bug-fix agent
- `story-analyzer` - Used by refinement agent

**Total:** 25 skills pending standardization

---

## Benefits of Standardization

### Faster Parsing
- YAML frontmatter enables quick metadata extraction
- Quick examples show outcome first
- Consistent structure improves scanning

### Better Error Handling
- Explicit error conditions
- Clear IF/THEN scripts
- Documented failure modes

### Easier Maintenance
- Consistent format across all skills
- Clear sections for updates
- Standardized examples

### Improved User Experience
- Quick examples at top (outcome first)
- DO/DON'T lists for clarity
- Action-oriented instructions

---

## Skill Categories

Skills are categorized by function:

- **analysis** (12 skills): Analyzes code, data, patterns, performance
- **planning** (5 skills): Creates strategies and plans
- **validation** (4 skills): Validates safety and correctness
- **generation** (5 skills): Generates docs, tests, criteria
- **detection** (2 skills): Detects issues and patterns

---

## Complexity Levels

- **low** (10 skills): Simple, straightforward (30-90 seconds)
- **medium** (15 skills): Moderate analysis (1-4 minutes)
- **high** (3 skills): Deep analysis, multiple steps (3-10 minutes)

---

## Next Steps

### Incremental Standardization Plan

**Phase 1 (Completed):** ✅
- Create standard template
- Refactor 3 most critical skills
- Document standardization approach

**Phase 2 (Recommended):**
- Standardize high-priority core workflow skills (5 skills)
- Estimated time: 3-4 hours

**Phase 3 (Future):**
- Standardize remaining specialized skills (20 skills)
- Estimated time: 6-8 hours
- Can be done incrementally as needed

---

## Quality Metrics

### Current State (3 skills standardized)
- ✅ YAML frontmatter: 3/28 (11%)
- ✅ Quick examples: 3/28 (11%)
- ✅ DO/DON'T lists: 3/28 (11%)
- ✅ Error conditions: 3/28 (11%)

### Target State (All skills standardized)
- 🎯 YAML frontmatter: 28/28 (100%)
- 🎯 Quick examples: 28/28 (100%)
- 🎯 DO/DON'T lists: 28/28 (100%)
- 🎯 Error conditions: 28/28 (100%)

---

## Usage

**To use standardized skills:**
1. Reference by name in agent files
2. Use template from `SKILL_TEMPLATE.md` for new skills
3. Follow examples in refactored skills

**To standardize a skill:**
1. Read existing skill
2. Apply template from `SKILL_TEMPLATE.md`
3. Add YAML frontmatter with correct metadata
4. Add quick example at top
5. Add DO/DON'T lists
6. Add error conditions
7. Streamline to 150-300 lines
8. Test references in agent files

---

**Status:** Phase 1 complete, 3 critical skills standardized, 25 pending
**Quality:** v2.0.0 standard established and proven
**Ready for:** Incremental Phase 2 standardization
