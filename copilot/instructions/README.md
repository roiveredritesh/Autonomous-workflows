# Instructions - User Guides and Practical Examples

This folder contains user-facing guides for using the autonomous workflow system with GitHub Copilot.

## File Purpose

### PRACTICAL_GUIDE.md ⭐ **Start Here**
**Quick Start and Common Scenarios**

Content:
- Quick start scenarios (4 execution modes)
- Flag reference card
- Common workflows
- Decision response guide (approve, adjust, spike, reject)
- Real-world examples
- Tips for best results
- Troubleshooting

**Use this when:**
- First time using the system
- Want to see practical examples
- Need quick reference for flags
- Troubleshooting issues

**Reading time:** 15-20 minutes

---

### WORKFLOW_EXECUTION_GUIDE.md
**Comprehensive Execution Guide**

Content:
- All execution modes explained in detail
  - Autonomous (default)
  - Checkpoint after analysis
  - Risk-based pausing
  - Manual step-by-step
- Complete execution flags reference
- Common workflows with detailed examples
- Checkpoint response options
- Automatic stop conditions
- Best practices by scenario
- Execution time expectations

**Use this when:**
- Need comprehensive understanding of execution modes
- Want to master all flag combinations
- Looking for best practices
- Planning complex workflows

**Reading time:** 30-40 minutes

---

### FLAG_USAGE_EXAMPLES.md
**Real-World Scenarios**

Content:
- 8 detailed examples with complete execution flows:
  1. Simple feature (full autonomous)
  2. Feature with review checkpoint
  3. Performance optimization (risk-based pausing)
  4. Bug fix (automatic risk detection)
  5. Production hotfix (manual mode)
  6. Complex feature (multiple checkpoints)
  7. Investigation (spike mode)
  8. Story refinement (unclear requirements)
- Flag combination recommendations
- Best practices by scenario type

**Use this when:**
- Want to see complete execution flows
- Looking for flag combinations for specific scenarios
- Need real-world examples
- Understanding how different flags interact

**Reading time:** 45-60 minutes

---

## Learning Path

### Beginner (15 minutes)
1. Read **PRACTICAL_GUIDE.md** - Quick Start section
2. Try a simple feature with no flags
3. Review the output

### Intermediate (30 minutes)
1. Read **WORKFLOW_EXECUTION_GUIDE.md** - Execution Modes
2. Read **FLAG_USAGE_EXAMPLES.md** - Examples 1-4
3. Try a feature with `approve_before_stage: [6]`
4. Try a feature with `approve_at_risk: medium`

### Advanced (1 hour)
1. Read **WORKFLOW_EXECUTION_GUIDE.md** - Complete guide
2. Read **FLAG_USAGE_EXAMPLES.md** - All examples
3. Try complex feature with multiple checkpoints
4. Try manual mode for a production scenario

---

## Quick Flag Reference

### No Flags (Autonomous)
```
"Add Excel export to customer list"
→ Full autonomous execution
→ Time: 30-60 seconds
→ Checkpoints: 0 (unless risk/safety triggered)
```

### Checkpoint Before Implementation
```
"Add email notifications"
Flags:
  approve_before_stage: [6]
→ Review after analysis
→ Time: 50 seconds + your review
→ Checkpoints: 1
```

### Risk-Based Pausing
```
"Optimize customer search query"
Flags:
  approve_at_risk: medium
→ Auto-pause if risk >= MEDIUM
→ Time: Variable + review if risk detected
→ Checkpoints: 0-1 (depends on risk)
```

### Manual Step-by-Step
```
"Add Excel export to customer list"
Flags:
  manual_mode: true
→ Approve every stage
→ Time: 45-135 seconds + 9 decisions
→ Checkpoints: 9
```

---

## Common Scenarios

### Routine Feature (Low Risk)
**Guide:** PRACTICAL_GUIDE.md - Scenario 1
```
No flags → Autonomous
Time: 30-60 seconds
```

### Complex Feature (Want Review)
**Guide:** WORKFLOW_EXECUTION_GUIDE.md - Workflow 2
```
approve_before_stage: [6]
Time: 50 seconds + review
```

### Performance Work (Uncertain Risk)
**Guide:** FLAG_USAGE_EXAMPLES.md - Example 3
```
approve_at_risk: medium
Time: Variable + review if needed
```

### Production Emergency (Maximum Control)
**Guide:** FLAG_USAGE_EXAMPLES.md - Example 5
```
manual_mode: true (or auto-detected)
Time: Variable + 9 decisions
```

---

## Execution Flags

### approve_before_stage
Pause before specific stages (1-9)
```yaml
approve_before_stage: [6]  # Pause before implementation
approve_before_stage: [5, 7]  # Multiple checkpoints
```

**Common checkpoints:**
- Stage 5: After data/cache impact analysis
- Stage 6: Before implementation planning ← Most common
- Stage 7: Before testing planning

### approve_at_risk
Pause when risk meets threshold
```yaml
approve_at_risk: low     # Pause on any risk
approve_at_risk: medium  # Pause on MEDIUM or HIGH risk
approve_at_risk: high    # Pause only on HIGH risk
```

**When to use:**
- `low`: Learning mode, want to see all risk assessments
- `medium`: Standard for uncertain work
- `high`: Only pause on critical risks

### approve_before_skills
Pause before specific skills
```yaml
approve_before_skills: [linq-query-tracer]
approve_before_skills: [redis-cache-strategy-analyzer, cache-invalidation-mapper]
```

**Common skills to gate:**
- `linq-query-tracer` - Database query analysis
- `sql-execution-analyzer` - SQL performance
- `redis-cache-strategy-analyzer` - Caching decisions

### manual_mode
Approve every stage (overrides all other flags)
```yaml
manual_mode: true
```

**When to use:**
- Production hotfixes
- Learning the workflow
- Compliance requirements
- Maximum oversight needed

### checkpoint_strategy
Automatic checkpoint placement
```yaml
checkpoint_strategy: analysis_only  # After stage 5
checkpoint_strategy: planning_only  # Before execution
checkpoint_strategy: both  # After analysis and planning
checkpoint_strategy: none  # No automatic checkpoints
```

---

## Checkpoint Responses

At checkpoints, you can respond:

### Approve
```
"Approve" | "Yes" | "Continue" | "Proceed"
→ Continue execution
```

### Adjust
```
"Adjust: Use 10-minute TTL instead"
"Change: Skip caching, use direct query"
→ Modify approach, re-run affected stages
```

### Spike
```
"Spike" | "Investigate" | "Need more info"
→ Switch to SPIKE mode, investigate, return findings
```

### Reject
```
"Reject" | "Stop" | "Different approach"
→ Stop workflow, preserve work done
```

---

## Best Practices

### ✅ Do This

**For routine work:**
- Use default (no flags)
- Trust autonomous execution
- Review output before implementing

**For learning:**
- Use `approve_before_stage: [6]`
- See analysis, then approve planning
- Builds confidence in system

**For high-risk work:**
- Use `approve_at_risk: medium`
- System pauses when risk detected
- You review and decide

**For unclear requests:**
- Just ask naturally
- System escalates to refinement
- Get clarity, then proceed

### ❌ Don't Do This

**Don't micro-manage:**
```
# Bad
Flags:
  approve_before_stage: [1,2,3,4,5,6,7,8,9]

# Just use manual_mode instead
```

**Don't over-control routine work:**
```
# Bad for simple features
"Add button [manual_mode: true]"

# Better
"Add button" (no flags)
```

**Don't skip safety:**
- Safety rules are non-negotiable
- If system stops for safety, address it
- Don't try to bypass safety checks

---

## Troubleshooting

### "Too many checkpoints"
**Cause:** Risk threshold too low
**Fix:** `approve_at_risk: medium` instead of `low`

### "Not enough control"
**Cause:** Using default autonomous
**Fix:** Add `approve_before_stage: [6]` or `approve_at_risk: medium`

### "System stopped unexpectedly"
**Cause:** Auto-stop condition (safety/risk/confidence)
**Fix:** Read stop reason, address issue, adjust approach

### "System asking too many questions"
**Cause:** Requirements unclear
**Fix:** Answer questions (refinement mode helps clarify)

---

## For More Details

**Formal specifications:** See `copilot/specs/`
- requirements.md - Architecture
- EXECUTION_RULES.md - Formal rules
- EXECUTION_CONTROL.md - Technical spec
- FLAG_PARSER.md - Implementation

**Main navigation:** See `copilot/README.md`

---

**These guides help you use the autonomous workflow system effectively. Start with PRACTICAL_GUIDE.md and build up to more advanced usage.**
