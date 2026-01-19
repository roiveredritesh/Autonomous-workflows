# Skills Inventory & Reference

## 🎯 Standardization Status (NEW!)

Skills are being upgraded to **v2.0.0 standard** with YAML frontmatter, quick examples, DO/DON'T lists, and error handling.

**Progress:** 3/28 skills standardized (11%)
- ✅ `bug-classifier` - v2.0.0 (334→179 lines)
- ✅ `production-impact-assessor` - v2.0.0 (152→157 lines)
- ✅ `safe-change-boundary-detector` - v2.0.0 (80→216 lines)

**See:** `STANDARDIZATION_SUMMARY.md` for details and `SKILL_TEMPLATE.md` for standard format.

**Remaining:** 25 skills scheduled for incremental standardization.

---

## Complete Skills List (28 Skills)

### Story & Requirements Skills (6)
1. **story-analyzer** - Analyzes current story state, identifies gaps and assumptions
2. **requirement-extractor** - Extracts functional, non-functional, and constraint requirements
3. **acceptance-criteria-generator** - Creates testable acceptance criteria in Gherkin format
4. **acceptance-criteria-expander** - Expands criteria to include edge cases and error handling
5. **edge-case-detector** - Identifies boundary conditions and error scenarios
6. **test-scenario-generator** - Creates comprehensive test scenarios and test cases

### Feature Delivery Skills (4)
7. **jira-story-intake** - Validates and extracts information from JIRA tickets
8. **feature-feasibility-analyzer** - Evaluates technical and business feasibility
9. **minimal-diff-planner** - Plans minimal, focused changes avoiding unnecessary refactoring
10. **webforms-lifecycle-analyzer** - Analyzes WebForms lifecycle and ViewState impact

### Bug Fix Skills (5)
11. **bug-classifier** - Categorizes bugs by severity, type, and reproducibility
12. **bug-impact-analyzer** - Assesses scope and user impact of bugs
13. **minimal-fix-planner** - Plans minimal, targeted bug fixes
14. **safe-change-boundary-detector** - Identifies safe modification points in code
15. **webforms-regression-analyzer** - Identifies regression risks from changes

### Spike/Investigation Skills (2)
16. **spike-charter** - Creates focused, time-boxed research investigations
17. **spike-findings-recorder** - Documents investigation findings and recommendations

### Production & Hotfix Skills (5)
18. **production-impact-assessor** - Evaluates business and technical impact of incidents
19. **emergency-mitigation-planner** - Develops immediate stabilization strategies
20. **hotfix-strategy-planner** - Determines fastest safe resolution approach
21. **hotfix-deployment-planner** - Plans hotfix deployment and validation
22. **rollback-plan-generator** - Creates detailed rollback procedures

### WebForms & Telerik Skills (3)
23. **telerik-impact-checker** - Validates compatibility with Telerik controls
24. **telerik-behavior-analyzer** - Analyzes Telerik control behavior in scenarios
25. **webforms-regression-analyzer** - Identifies WebForms regression risks

### Data & Performance Skills (4)
26. **linq-query-tracer** - Analyzes LINQ query efficiency and optimization
27. **sql-impact-analyzer** - Evaluates database schema change impacts
28. **performance-profiler** - Establishes baselines and identifies bottlenecks
29. **cache-invalidation-mapper** - Maps cache invalidation points
30. **redis-cache-strategy-analyzer** - (Pre-existing) Analyzes Redis caching strategies

## Skill Organization by Agent Usage

### Orchestrator Agent
- *(Entry point, uses specialized agents)*

### Feature Delivery Agent
Uses: jira-story-intake, acceptance-criteria-expander, feature-feasibility-analyzer, 
webforms-lifecycle-analyzer, telerik-impact-checker, safe-change-boundary-detector,
linq-query-tracer, sql-impact-analyzer, redis-cache-strategy-analyzer,
cache-invalidation-mapper, minimal-diff-planner, webforms-regression-analyzer,
test-scenario-generator, rollback-plan-generator

### Bug Fix Agent
Uses: bug-classifier, webforms-lifecycle-analyzer, linq-query-tracer, 
telerik-behavior-analyzer, redis-behavior-checker, bug-impact-analyzer,
minimal-fix-planner, safe-change-boundary-detector, webforms-lifecycle-validator,
telerik-contract-validator, webforms-regression-analyzer, test-scenario-generator,
rollback-plan-generator

### Hotfix Agent
Uses: production-impact-assessor, emergency-mitigation-planner, production-log-analyzer,
error-pattern-detector, change-history-analyzer, hotfix-strategy-planner,
hotfix-branch-creator, minimal-fix-implementer, hotfix-test-generator, hotfix-validator,
hotfix-deployment-planner, production-verification-checker, hotfix-incident-documenter,
postmortem-planner

### Spike Agent
Uses: spike-charter, webforms-lifecycle-analyzer, telerik-behavior-analyzer,
safe-change-boundary-detector, linq-query-tracer, sql-execution-analyzer,
cache-performance-checker, data-model-explorer, stored-procedure-analyzer,
redis-key-inspector, api-contract-analyzer, dependency-mapper, spike-findings-recorder

### Story Refinement Agent
Uses: story-analyzer, requirement-extractor, acceptance-criteria-generator,
edge-case-detector

### Performance Agent
Uses: performance-profiler, request-profiler, sql-execution-analyzer,
cache-miss-detector, network-latency-checker, linq-query-tracer,
sql-execution-plan-analyzer, missing-index-detector, n-plus-one-detector,
redis-key-strategy-analyzer, cache-stampede-detector, cache-invalidation-analyzer,
webforms-viewstate-analyzer, serialization-overhead-checker, loop-optimization-scanner,
optimization-strategy-planner, safe-change-boundary-detector, query-behavior-validator,
cache-correctness-validator, performance-regression-checker,
performance-implementation-planner, performance-validation-planner

## Skills Still Needing Implementation

The following skills are referenced in agents but not yet implemented:
- production-log-analyzer
- error-pattern-detector
- change-history-analyzer
- hotfix-branch-creator
- minimal-fix-implementer
- hotfix-test-generator
- hotfix-validator
- hotfix-incident-documenter
- postmortem-planner
- data-model-explorer
- stored-procedure-analyzer
- redis-key-inspector
- api-contract-analyzer
- dependency-mapper
- request-profiler
- sql-execution-analyzer
- cache-miss-detector
- network-latency-checker
- sql-execution-plan-analyzer
- missing-index-detector
- n-plus-one-detector
- redis-behavior-checker
- webforms-lifecycle-validator
- telerik-contract-validator
- webforms-viewstate-analyzer
- serialization-overhead-checker
- loop-optimization-scanner
- optimization-strategy-planner
- query-behavior-validator
- cache-correctness-validator
- performance-regression-checker
- performance-implementation-planner
- performance-validation-planner
- hotfix-deployment-planner
- production-verification-checker
- change-log-generator
- decision-record-creator
- risk-documentation-generator
- pr-metadata-generator

## Recommended Implementation Order

### Phase 1 (Critical for MVP)
- ✅ All 28 primary skills created
- These enable basic workflow through all agents

### Phase 2 (High Value)
Priority skills to implement next:
1. hotfix-deployment-planner (needed for hotfix execution)
2. hotfix-branch-creator & hotfix-validator (for code hotfixes)
3. request-profiler (for performance diagnosis)
4. sql-execution-analyzer (for query optimization)
5. optimization-strategy-planner (for performance optimization)

### Phase 3 (Supporting Skills)
After Phase 2, implement remaining skills based on frequency of use and priority.

## Skill Cross-References

Skills are organized to work together. Key relationships:

```
Requirement Extraction Pipeline:
  story-analyzer → requirement-extractor → acceptance-criteria-generator 
  → edge-case-detector → test-scenario-generator

Feasibility Pipeline:
  jira-story-intake → feature-feasibility-analyzer → spike-charter (if needed)

Bug Fix Pipeline:
  bug-classifier → bug-impact-analyzer → minimal-fix-planner 
  → safe-change-boundary-detector → webforms-regression-analyzer

Performance Diagnosis Pipeline:
  performance-profiler → linq-query-tracer → sql-impact-analyzer 
  → optimization-strategy-planner

Hotfix Pipeline:
  production-impact-assessor → emergency-mitigation-planner 
  → hotfix-strategy-planner → hotfix-deployment-planner → rollback-plan-generator
```

## Usage Guidelines

### For Feature Delivery
1. Start with `jira-story-intake` to validate ticket
2. Use `feature-feasibility-analyzer` to assess approach
3. Use `webforms-lifecycle-analyzer` to check compatibility
4. Plan changes with `minimal-diff-planner`
5. Create tests with `test-scenario-generator`

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
5. Document with incident-related skills

## Maintenance Notes

- Skills are self-contained but reference related skills
- Each skill has specific input/output contracts
- All skills support Gherkin/YAML formatting for consistency
- Skills designed to chain together in typical workflows
- Ready for automation/tool integration

## Success Metrics

This skill set enables:
- ✅ Structured workflow for all delivery modes
- ✅ Comprehensive risk management
- ✅ Legacy system safety (WebForms-specific)
- ✅ Time-boxed investigations (spikes)
- ✅ Rapid incident response (hotfixes)
- ✅ Quality assurance through comprehensive testing
- ✅ Proper change tracking and rollback capability
