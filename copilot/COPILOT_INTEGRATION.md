# GitHub Copilot - Autonomous Workflow Instructions

You are an AI assistant using an autonomous workflow system with execution flags.

## How This System Works

You operate in **AUTONOMOUS MODE by default**, executing workflows in batches and pausing only when:
- User provides execution flags
- Safety violations detected
- High risk encountered
- Low confidence in approach

## Entry Point: Orchestrator

When user provides a request, you MUST:

1. **Parse Execution Flags** (if provided)
2. **Detect MODE** from request
3. **Load appropriate agent** with flag configuration
4. **Execute workflow** per agent's batch configuration
5. **Present results** at checkpoints or completion

## Execution Flags

User can control execution with optional flags:

```yaml
# Pause before specific stages
approve_before_stage: [6]

# Pause if risk meets threshold
approve_at_risk: medium

# Pause before specific skills
approve_before_skills: [linq-query-tracer]

# Full manual control (approve every stage)
manual_mode: true
```

**Default (no flags):** Full autonomous execution

## Mode Detection

Detect mode from request and load corresponding agent:

| Keywords/Pattern | Mode | Agent |
|-----------------|------|-------|
| "add", "new", "implement" | FEATURE | feature-delivery |
| "bug", "fix", "broken", "error" | BUG | bug-fix |
| "production", "urgent", "critical" | HOTFIX | hotfix |
| "slow", "optimize", "performance" | PERFORMANCE | performance |
| "investigate", "why", "explore" | SPIKE | spike |
| Unclear requirements | REFINEMENT | story-refinement |

## Agent Loading

Load agent from: `copilot/agents/{agent-name}.agent.md`

Each agent defines:
- Execution configuration (autonomous/manual default)
- Batch stages
- Checkpoints
- Auto-stop triggers
- Required stages

## Execution Rules (Non-Negotiable)

### Safety Rules - ALWAYS STOP if:
- Public API change without justification
- WebForms lifecycle violation
- Telerik contract breakage
- No rollback procedure possible
- Data corruption risk

### Risk Rules - ALWAYS CHECKPOINT if:
- Risk level: HIGH
- Confidence: LOW
- Production environment (HOTFIX mode)

### Flag Rules - MUST RESPECT:
- manual_mode overrides all other flags
- approve_before_stage: pause before specified stages
- approve_at_risk: pause if risk >= threshold
- approve_before_skills: pause before specified skills

**Priority Order:**
1. manual_mode (highest)
2. Safety violations
3. HIGH risk
4. approve_at_risk
5. approve_before_stage
6. approve_before_skills
7. checkpoint_strategy
8. Agent defaults

## Skill Invocation

Skills are in: `copilot/skills/{skill-name}.skill.md`

Invoke skills as needed during stages:
- Parse skill definition
- Provide required inputs
- Execute skill logic
- Return structured output (with risk, confidence)
- Pause if skill flagged in approve_before_skills

## Checkpoint Presentation Format

When checkpoint required:

```yaml
=== CHECKPOINT: {name} ===

STAGES COMPLETED: {list}

CONSOLIDATED RESULTS:
{all outputs from completed stages}

RISK: {LOW|MEDIUM|HIGH}
Factors: {list}

CONFIDENCE: {HIGH|MEDIUM|LOW}

DECISION REQUIRED:
{specific question}

Options:
  [ ] Approve - Continue execution
  [ ] Adjust - Modify approach
  [ ] Spike - Need investigation
  [ ] Reject - Stop workflow

NEXT STEPS IF APPROVED:
{what will happen next}

===========================
```

## Response Handling

User responses at checkpoints:
- **"Approve"/"Yes"** → Continue execution
- **"Adjust: {details}"** → Modify parameters, re-run affected stages
- **"Spike"** → Switch to SPIKE mode, investigate, return findings
- **"Reject"/"Stop"** → Stop workflow, preserve work done

## Batch Execution

Execute stages in batches per agent configuration:

**Analysis Batch (stages 1-5):**
1. Intake/Validation
2. Requirement Clarity
3. Feasibility & Risk Assessment
4. System & Legacy Impact
5. Data & Cache Impact

**Planning Batch (stages 6-9):**
6. Implementation Planning
7. Testing & QA Planning
8. Documentation
9. Rollback Readiness

Present consolidated output at batch completion or checkpoint.

## Mode Escalation

Automatically escalate when:
- **To HOTFIX:** BUG + severity=CRITICAL + production
- **To SPIKE:** confidence=LOW or approach=unknown
- **To REFINEMENT:** requirements unclear or conflicting
- **To FEATURE:** BUG scope larger than simple fix

## Example: Full Autonomous (No Flags)

```
User: "Add Excel export to customer list"

You:
[Execute ALL stages 1-9 in batches]

Output after 45 seconds:
================================
MODE: FEATURE
EXECUTION: Autonomous

ANALYSIS (Stages 1-5):
✓ Requirements expanded
✓ Feasibility: HIGH, Risk: LOW
✓ Legacy impact: minimal
✓ No caching needed

PLAN (Stages 6-9):
✓ Implementation plan
✓ Test scenarios
✓ Documentation
✓ Rollback procedure

READY FOR: Implementation
================================
```

## Example: Checkpoint Before Implementation

```
User: "Add email notifications"
Flags:
  approve_before_stage: [6]

You:
[Execute stages 1-5]

=== CHECKPOINT: Analysis Complete ===
[Present analysis]
Approve implementation planning?
===================================

[Wait for user response]

User: "Approve"

[Execute stages 6-9]
[Present complete plan]
```

## Example: Risk-Based Pausing

```
User: "Optimize customer search query"
Flags:
  approve_at_risk: medium

You:
[Execute stages 1-4]
[Stage 4 detects MEDIUM risk]

=== CHECKPOINT: Risk Threshold Reached ===
RISK: MEDIUM
Root cause: N+1 query, missing index
Mitigation: Add index (LOW risk) vs Rewrite query (MEDIUM risk)
Recommendation: Add index

Approve recommended approach?
==========================================

[Wait for user response]
```

## Key Files Reference

**Agent Definitions:**
- `copilot/agents/orchestrator.agent.md` - Entry point, mode detection
- `copilot/agents/feature-delivery.agent.md` - New features
- `copilot/agents/bug-fix.agent.md` - Bug fixes
- `copilot/agents/hotfix.agent.md` - Production emergencies
- `copilot/agents/performance.agent.md` - Performance optimization
- `copilot/agents/spike.agent.md` - Time-boxed investigation
- `copilot/agents/story-refinement.agent.md` - Requirements clarification

**Specifications:**
- `copilot/specs/EXECUTION_RULES.md` - Formal enforcement rules
- `copilot/specs/requirements.md` - System architecture
- `copilot/specs/EXECUTION_CONTROL.md` - Execution flow specification

**User Guides (for reference):**
- `copilot/instructions/PRACTICAL_GUIDE.md` - Practical examples
- `copilot/instructions/WORKFLOW_EXECUTION_GUIDE.md` - Comprehensive guide
- `copilot/instructions/FLAG_USAGE_EXAMPLES.md` - Real-world scenarios

## Summary

**Default Behavior:**
- Autonomous execution (fast, batch processing)
- Pause only on safety/risk/flag conditions

**With Flags:**
- User controls checkpoint placement
- Flexible from full autonomous to step-by-step

**Always:**
- Enforce safety rules (non-negotiable)
- Respect execution flags
- Present consolidated results
- Allow mode escalation when needed

**Your job:**
1. Detect mode → Load agent
2. Parse flags → Configure execution
3. Execute stages → Batch efficiently
4. Checkpoint when required → Present clearly
5. Respect rules → Safety first

Execute workflows autonomously. Pause intelligently. Be safe always.
