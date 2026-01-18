# Quick Reference: Agents & Skills

## Decision Tree: Which Agent/Skill to Use?

### What are you doing?

#### "I need to add a new feature" → FEATURE DELIVERY AGENT
```
1. jira-story-intake (Validate ticket)
2. acceptance-criteria-expander (Clarify requirements)  
3. feature-feasibility-analyzer (Check if possible)
4. webforms-lifecycle-analyzer (WebForms impact?)
5. minimal-diff-planner (Plan changes)
6. test-scenario-generator (Create tests)
7. rollback-plan-generator (Plan rollback)
```

#### "There's a bug" → BUG FIX AGENT
```
1. bug-classifier (How serious?)
2. bug-impact-analyzer (Who's affected?)
3. minimal-fix-planner (How to fix?)
4. webforms-regression-analyzer (What could break?)
5. test-scenario-generator (Test cases?)
6. rollback-plan-generator (How to revert?)
```

#### "Production is down!" → HOTFIX AGENT
```
1. production-impact-assessor (CRITICAL?)
2. emergency-mitigation-planner (How to stabilize?)
3. hotfix-strategy-planner (What's the fix?)
4. rollback-plan-generator (Always needed!)
5. Deploy and monitor
```

#### "We don't know how/if we can do X" → SPIKE AGENT
```
1. spike-charter (Define investigation)
2. Investigate...
3. spike-findings-recorder (Document results)
4. Recommend: Proceed? Pivot? More research?
```

#### "Requirements are unclear" → STORY REFINEMENT AGENT
```
1. story-analyzer (What's missing?)
2. requirement-extractor (What do they need?)
3. acceptance-criteria-generator (Make it testable)
4. edge-case-detector (Don't forget edge cases)
```

#### "It's slow!" → PERFORMANCE AGENT
```
1. performance-profiler (Measure now vs. target)
2. linq-query-tracer (LINQ queries OK?)
3. sql-impact-analyzer (Database issue?)
4. cache-invalidation-mapper (Caching strategy?)
5. Optimize and validate
```

---

## Skills by Category

### 🎯 Requirements & Stories
- story-analyzer: What's unclear?
- requirement-extractor: Extract needs
- acceptance-criteria-generator: Make testable
- edge-case-detector: What could go wrong?

### ⚙️ Feature Planning
- jira-story-intake: Validate ticket
- feature-feasibility-analyzer: Is it possible?
- minimal-diff-planner: Minimal changes
- test-scenario-generator: Test cases

### 🐛 Bug Fixing
- bug-classifier: How serious?
- bug-impact-analyzer: How many affected?
- minimal-fix-planner: Fix strategy
- webforms-regression-analyzer: Regression risk?

### 🔴 Production Issues
- production-impact-assessor: How critical?
- emergency-mitigation-planner: How to stabilize?
- hotfix-strategy-planner: Fix approach
- rollback-plan-generator: How to revert

### 🔬 Research
- spike-charter: Define question
- spike-findings-recorder: Document findings

### 🏛️ Legacy System
- webforms-lifecycle-analyzer: ViewState? Lifecycle?
- telerik-impact-checker: Telerik compatible?
- telerik-behavior-analyzer: How do they work?
- safe-change-boundary-detector: Safe to modify?

### 🚀 Performance
- performance-profiler: Measure performance
- linq-query-tracer: Query optimization
- sql-impact-analyzer: Database impact
- cache-invalidation-mapper: Cache strategy

---

## Quick Skill Reference

**skill-name** | **Input** | **Output** | **Time**
---|---|---|---
story-analyzer | Current story | Gaps & assumptions | 5 min
requirement-extractor | Unclear req | Clear requirements | 10 min
acceptance-criteria-generator | Requirements | Testable criteria | 10 min
edge-case-detector | Criteria | Edge cases covered | 15 min
test-scenario-generator | Criteria + edge cases | Test scenarios | 20 min
jira-story-intake | Ticket ID or link | Validated ticket info | 5 min
feature-feasibility-analyzer | Feature description | Feasibility assessment | 15 min
minimal-diff-planner | Feature scope | Minimal change plan | 10 min
bug-classifier | Bug report | Severity & type | 5 min
bug-impact-analyzer | Bug details | User/data impact | 10 min
minimal-fix-planner | Root cause | Fix strategy | 10 min
webforms-lifecycle-analyzer | Change scope | Lifecycle impact | 10 min
webforms-regression-analyzer | Code change | Regression risks | 10 min
production-impact-assessor | Incident | Severity assessment | 5 min
emergency-mitigation-planner | Problem | Stabilization plan | 10 min
hotfix-strategy-planner | Root cause | Resolution approach | 10 min
rollback-plan-generator | Change details | Detailed rollback | 15 min
spike-charter | Research question | Investigation plan | 10 min
spike-findings-recorder | Investigation results | Findings report | 15 min
performance-profiler | Component | Baseline metrics | 30 min
linq-query-tracer | LINQ code | Optimization analysis | 10 min
sql-impact-analyzer | SQL change | Impact assessment | 15 min
cache-invalidation-mapper | Data changes | Invalidation points | 15 min
safe-change-boundary-detector | Code location | Safe zones identified | 10 min
telerik-impact-checker | Change scope | Telerik compatibility | 10 min
telerik-behavior-analyzer | Behavior question | Behavior analysis | 10 min

---

## Typical Workflows

### Feature from Request to Ready (45 min)
1. ✅ jira-story-intake (5 min)
2. ✅ acceptance-criteria-expander (5 min)
3. ✅ feature-feasibility-analyzer (10 min)
4. ✅ minimal-diff-planner (10 min)
5. ✅ test-scenario-generator (10 min)
6. ✅ rollback-plan-generator (5 min)

### Bug from Report to Ready (40 min)
1. ✅ bug-classifier (5 min)
2. ✅ bug-impact-analyzer (10 min)
3. ✅ minimal-fix-planner (10 min)
4. ✅ webforms-regression-analyzer (10 min)
5. ✅ test-scenario-generator (5 min)

### Production Incident to Resolved (25 min)
1. ✅ production-impact-assessor (5 min)
2. ✅ hotfix-strategy-planner (10 min)
3. ✅ rollback-plan-generator (5 min)
4. ✅ Deploy & Validate (5 min)

### Unclear Story to Refined (40 min)
1. ✅ story-analyzer (10 min)
2. ✅ requirement-extractor (10 min)
3. ✅ acceptance-criteria-generator (10 min)
4. ✅ edge-case-detector (10 min)

---

## Error Handling

**Problem** | **Use This Skill** | **Action**
---|---|---
"I don't know if it's possible" | spike-charter | Do a time-boxed investigation
"Requirements are vague" | story-analyzer | Analyze what's unclear
"It might break something" | webforms-regression-analyzer | Check regression risk
"What if it fails?" | rollback-plan-generator | Always have rollback ready
"Production is on fire" | production-impact-assessor | Assess criticality immediately
"Is the fix minimal?" | minimal-fix-planner | Plan surgical fix
"Do we understand the root cause?" | bug-classifier | Classify first
"How will users be affected?" | bug-impact-analyzer | Assess impact
"Will cache be consistent?" | cache-invalidation-mapper | Map invalidation points

---

## Key Principles

✅ **Always use rollback-plan-generator** for any production change
✅ **Always start with classifier** for bugs
✅ **Always check feasibility** before committing
✅ **Always analyze regression** before deploying
✅ **Always test edge cases** before ship
✅ **Always validate WebForms compatibility** for legacy code
✅ **Always time-box investigations** with spike-charter
✅ **Always plan for failure** in production

---

## Files Location

All skills are in: `d:\RAG\.github\skills\`

- README.md - Complete inventory
- STATUS_REPORT.md - Readiness status
- IMPLEMENTATION_SUMMARY.md - What was implemented
- *.skill.md - Individual skill definitions

---

## Need Help?

**"What skill should I use?"** → Read the decision tree above
**"How do I use a skill?"** → Open the .skill.md file
**"What skills exist?"** → See README.md
**"What's ready to use?"** → See STATUS_REPORT.md

---

**Version**: 1.0
**Last Updated**: Jan 17, 2026
**Status**: ✅ Production Ready
