# Autonomous Workflow System

## Overview

This folder contains a complete autonomous workflow system for GitHub Copilot that uses execution flags to control when to pause for human approval.

---

## Quick Start

**Integrating with your project? Start here:**

1. [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) - ⭐ **How to add to your existing `.github/copilot-instructions.md`**
2. [COPILOT_INTEGRATION.md](COPILOT_INTEGRATION.md) - Full autonomous workflow instructions for Copilot

**New to the system? Start here:**

3. [instructions/PRACTICAL_GUIDE.md](instructions/PRACTICAL_GUIDE.md) - Practical examples of how to use the system
4. [instructions/WORKFLOW_EXECUTION_GUIDE.md](instructions/WORKFLOW_EXECUTION_GUIDE.md) - Comprehensive execution guide
5. [instructions/FLAG_USAGE_EXAMPLES.md](instructions/FLAG_USAGE_EXAMPLES.md) - Real-world examples with different flags

**Then explore:**

6. [specs/requirements.md](specs/requirements.md) - Complete system requirements and principles
7. [specs/EXECUTION_CONTROL.md](specs/EXECUTION_CONTROL.md) - Technical specification of execution flow

---

## Documentation Structure

### Core Concepts

**[requirements.md](specs/requirements.md)**
- System architecture and principles
- Execution modes (autonomous vs manual)
- Execution flags specification
- Agent and skill definitions
- Safety rules and constraints
- Implementation status

**Purpose:** Understand the "why" behind the system

**[EXECUTION_RULES.md](specs/EXECUTION_RULES.md)** ⚠️ **Critical**
- Formal enforcement rules
- Non-negotiable safety constraints
- Flag validation and conflicts
- Risk assessment formulas
- Escalation conditions

**Purpose:** Understand the "must" and "must not" rules

---

### Execution Control

**[EXECUTION_CONTROL.md](specs/EXECUTION_CONTROL.md)**
- Execution flow diagrams
- Execution patterns (autonomous, checkpoint, manual)
- Batch execution strategy
- Checkpoint handling
- Error handling
- Performance characteristics

**Purpose:** Technical deep-dive into how execution works

---

**[EXECUTION_RULES.md](specs/EXECUTION_RULES.md)** ⚠️ **Critical Reference**
- 10 categories of enforcement rules
- Flag validation and conflict resolution
- Safety rules (non-negotiable)
- Stage transition requirements
- Mandatory checkpoint triggers
- Risk assessment rules
- Escalation conditions
- Rule enforcement matrix

**Purpose:** Define non-negotiable rules that govern all execution

---

### User Guides

**[PRACTICAL_GUIDE.md](instructions/PRACTICAL_GUIDE.md)** ⭐ **Start Here**
- Quick start scenarios
- Common workflows
- Flag reference card
- Decision response guide
- Troubleshooting
- Real-world examples

**Purpose:** Learn by example - practical usage

---

**[WORKFLOW_EXECUTION_GUIDE.md](instructions/WORKFLOW_EXECUTION_GUIDE.md)**
- Execution modes explained
- Execution flags reference
- Common workflows
- Checkpoint response options
- Automatic stop conditions
- Best practices

**Purpose:** Comprehensive guide to all execution modes and flags

---

**[FLAG_USAGE_EXAMPLES.md](instructions/FLAG_USAGE_EXAMPLES.md)**
- Real-world scenarios with execution flow
- Flag combinations for different situations
- Best practices by scenario type
- Complete example outputs

**Purpose:** See exactly how different flags work in practice

---

### Implementation Details

**[FLAG_PARSER.md](specs/FLAG_PARSER.md)**
- Flag parsing algorithm
- Flag types and validation
- Execution context creation
- Natural language translation
- Error handling
- Testing and validation

**Purpose:** Implementation reference for flag parsing

---

### Agents and Skills

**[agents/](agents/)** - Specialized workflow agents
- [orchestrator.agent.md](agents/orchestrator.agent.md) - Entry point, flag parsing, mode detection
- [feature-delivery.agent.md](agents/feature-delivery.agent.md) - New feature delivery
- [bug-fix.agent.md](agents/bug-fix.agent.md) - Bug fix workflow
- [hotfix.agent.md](agents/hotfix.agent.md) - Production emergency workflow
- [performance.agent.md](agents/performance.agent.md) - Performance optimization
- [spike.agent.md](agents/spike.agent.md) - Investigation and research
- [story-refinement.agent.md](agents/story-refinement.agent.md) - Requirements clarification

**[skills/](skills/)** - Reusable capabilities
- See [skills/README.md](skills/README.md) for complete catalog

---

## Learning Path

### Level 1: Beginner (15 minutes)

**Goal:** Understand basic autonomous execution

1. Read: [PRACTICAL_GUIDE.md](instructions/PRACTICAL_GUIDE.md) - Quick Start section
2. Try: Simple feature request with no flags
3. Review: Output and understand the workflow

**Example:**
```
You: "Add export button to customer list"
[No flags - fully autonomous]
Result: Complete plan in 45 seconds
```

---

### Level 2: Intermediate (30 minutes)

**Goal:** Use execution flags for control

1. Read: [WORKFLOW_EXECUTION_GUIDE.md](instructions/WORKFLOW_EXECUTION_GUIDE.md) - Execution Modes section
2. Read: [FLAG_USAGE_EXAMPLES.md](instructions/FLAG_USAGE_EXAMPLES.md) - Examples 1-4
3. Try: Feature with checkpoint flag
4. Try: Feature with risk-based pausing

**Example:**
```
You: "Add email notifications"
Flags:
  approve_before_stage: [6]
Result: Checkpoint after analysis, then continue
```

---

### Level 3: Advanced (1 hour)

**Goal:** Master all execution patterns

1. Read: [EXECUTION_CONTROL.md](specs/EXECUTION_CONTROL.md) - Complete specification
2. Read: [FLAG_USAGE_EXAMPLES.md](instructions/FLAG_USAGE_EXAMPLES.md) - All examples
3. Try: Complex feature with multiple checkpoints
4. Try: Manual mode for production hotfix

**Example:**
```
You: "Migrate customer data to new schema"
Flags:
  approve_before_stage: [5, 7]
  approve_at_risk: low
Result: Multiple review points for high-risk work
```

---

### Level 4: Expert (2+ hours)

**Goal:** Understand system architecture and rules

1. Read: [requirements.md](specs/requirements.md) - Complete requirements
2. Read: [EXECUTION_RULES.md](specs/EXECUTION_RULES.md) - **Formal enforcement rules**
3. Read: [FLAG_PARSER.md](specs/FLAG_PARSER.md) - Implementation details
4. Read: All agent specifications in [agents/](agents/)
5. Customize: Create team-specific flag patterns

---

## Common Use Cases

### Use Case 1: Routine Feature

**Documentation:** [PRACTICAL_GUIDE.md](instructions/PRACTICAL_GUIDE.md) - Scenario 1

**Pattern:**
```
No flags → Autonomous execution
Time: 30-60 seconds
Checkpoints: 0
```

---

### Use Case 2: Complex Feature

**Documentation:** [WORKFLOW_EXECUTION_GUIDE.md](instructions/WORKFLOW_EXECUTION_GUIDE.md) - Workflow 2

**Pattern:**
```
approve_before_stage: [6]
Time: 50 seconds + review
Checkpoints: 1 (after analysis)
```

---

### Use Case 3: Performance Optimization

**Documentation:** [FLAG_USAGE_EXAMPLES.md](instructions/FLAG_USAGE_EXAMPLES.md) - Example 3

**Pattern:**
```
approve_at_risk: medium
Time: Variable + review if risk detected
Checkpoints: 0-1 (risk-based)
```

---

### Use Case 4: Production Hotfix

**Documentation:** [FLAG_USAGE_EXAMPLES.md](instructions/FLAG_USAGE_EXAMPLES.md) - Example 5

**Pattern:**
```
manual_mode: true (or auto-detected by hotfix agent)
Time: Variable + 9 decision points
Checkpoints: 9 (every stage)
```

---

### Use Case 5: Investigation

**Documentation:** [agents/spike.agent.md](agents/spike.agent.md)

**Pattern:**
```
No flags → Spike agent handles investigation
Time: Variable (time-boxed)
Checkpoints: 1 (at end with findings)
```

---

### Use Case 6: Unclear Requirements

**Documentation:** [agents/story-refinement.agent.md](agents/story-refinement.agent.md)

**Pattern:**
```
No flags → Refinement agent clarifies
Time: 20-40 seconds
Checkpoints: 1 (present refined story)
```

---

## Execution Flags Quick Reference

### approve_before_stage

**Pause before specific stages**

```yaml
approve_before_stage: [6]  # Pause before implementation
approve_before_stage: [5, 7]  # Multiple checkpoints
```

**Stages:**
1. Intake & Validation
2. Requirement Clarity
3. Feasibility & Risk
4. System & Legacy Impact
5. Data & Cache Impact
6. Implementation Planning ← Common checkpoint
7. Regression & QA Planning
8. Documentation
9. Release & Rollback Readiness

---

### approve_at_risk

**Pause when risk meets threshold**

```yaml
approve_at_risk: low     # Pause on any risk
approve_at_risk: medium  # Pause on medium or high
approve_at_risk: high    # Pause only on high risk
```

---

### approve_before_skills

**Pause before specific skills**

```yaml
approve_before_skills: [linq-query-tracer]
approve_before_skills: [redis-cache-strategy-analyzer, cache-invalidation-mapper]
```

---

### manual_mode

**Approve every stage**

```yaml
manual_mode: true
```

Overrides all other flags.

---

### checkpoint_strategy

**Automatic checkpoint placement**

```yaml
checkpoint_strategy: analysis_only  # After stage 5
checkpoint_strategy: planning_only  # Before final execution
checkpoint_strategy: both           # After analysis and planning
checkpoint_strategy: none          # No automatic checkpoints
```

---

## Agent Reference

| Agent | Mode | Default Execution | Purpose |
|-------|------|------------------|---------|
| [Orchestrator](agents/orchestrator.agent.md) | N/A | Autonomous | Entry point, flag parsing, delegation |
| [Feature Delivery](agents/feature-delivery.agent.md) | FEATURE | Autonomous | New feature development |
| [Bug Fix](agents/bug-fix.agent.md) | BUG FIX | Autonomous | Defect resolution |
| [Hotfix](agents/hotfix.agent.md) | HOTFIX | **Manual** | Production emergencies |
| [Performance](agents/performance.agent.md) | PERFORMANCE | Autonomous | Performance optimization |
| [Spike](agents/spike.agent.md) | SPIKE | Autonomous | Time-boxed investigation |
| [Story Refinement](agents/story-refinement.agent.md) | REFINEMENT | Autonomous | Requirements clarification |

---

## Skills Reference

**See:** [skills/README.md](skills/README.md) for complete catalog

**Categories:**
- Product & Jira (story intake, criteria generation, bug classification)
- Legacy System Analysis (WebForms, Telerik, safe boundaries)
- Data & Performance (LINQ tracing, SQL analysis, query optimization)
- Cache (Redis strategy, invalidation mapping, stampede detection)
- Quality & Release (regression analysis, test generation, rollback planning)
- Documentation (change logs, decision records, risk documentation)

---

## Best Practices

### Default to Autonomous

```
Good: "Add export button"
Why: Let the system handle routine work
```

### Add Flags for Complex Work

```
Good: "Add payment integration [approve_before_stage: 6]"
Why: Review before committing to implementation
```

### Use Risk Flags for Uncertain Work

```
Good: "Optimize query [approve_at_risk: medium]"
Why: System pauses if complexity is higher than expected
```

### Use Manual Mode for Production

```
Good: "Fix production bug [manual_mode: true]"
Why: Production changes need careful oversight
```

### Don't Over-Control Routine Work

```
Bad: "Add button [manual_mode: true]"
Why: Simple features don't need 9 approval points
```

---

## Automatic Safeguards

**These always trigger checkpoints, regardless of flags:**

- **Safety Violations**
  - Public API change without justification
  - WebForms lifecycle violation
  - Telerik contract breakage
  - Missing rollback procedure

- **High Risk**
  - Risk level: HIGH
  - Data corruption possible
  - Performance degradation likely

- **Low Confidence**
  - Confidence: LOW
  - Unknown behavior
  - Contradictory requirements

- **Conflicts**
  - Conflicting requirements detected
  - Incompatible constraints

---

## Troubleshooting Guide

### Problem: Too Many Checkpoints

**Cause:** Risk threshold too low or too many stage flags

**Solution:**
```yaml
# Raise risk threshold
approve_at_risk: high  # instead of: low

# Or remove unnecessary stage flags
approve_before_stage: [6]  # instead of: [1,2,3,4,5,6,7,8,9]
```

---

### Problem: Not Enough Control

**Cause:** Using default autonomous mode

**Solution:**
```yaml
# Add checkpoint flag
approve_before_stage: [6]

# Or risk-based pausing
approve_at_risk: medium
```

---

### Problem: System Stopped Unexpectedly

**Cause:** Automatic stop condition triggered

**Solution:**
1. Read the stop reason
2. Address the safety/risk issue
3. Adjust approach or spike investigation
4. Resume workflow

---

### Problem: Unclear Requirements

**Cause:** Vague or incomplete request

**Solution:**
- System automatically escalates to refinement
- Answer clarifying questions
- System continues with refined story

---

## File Organization

```
copilot/
├── README.md (this file - main navigation)
├── INTEGRATION_GUIDE.md (how to add to your existing copilot-instructions.md)
├── COPILOT_INTEGRATION.md (full autonomous workflow instructions)
├── instructions/ (user-facing guides)
│   ├── README.md (instructions index)
│   ├── PRACTICAL_GUIDE.md (practical usage guide)
│   ├── WORKFLOW_EXECUTION_GUIDE.md (comprehensive guide)
│   └── FLAG_USAGE_EXAMPLES.md (real-world examples)
├── specs/ (formal specifications)
│   ├── README.md (specs index)
│   ├── requirements.md (system requirements)
│   ├── EXECUTION_RULES.md (enforcement rules - critical)
│   ├── EXECUTION_CONTROL.md (execution specification)
│   └── FLAG_PARSER.md (implementation details)
├── agents/
│   ├── orchestrator.agent.md
│   ├── feature-delivery.agent.md
│   ├── bug-fix.agent.md
│   ├── hotfix.agent.md
│   ├── performance.agent.md
│   ├── spike.agent.md
│   └── story-refinement.agent.md
└── skills/
    ├── README.md
    └── [30+ skill definitions]
```

---

## Summary

### Key Documents

1. **[PRACTICAL_GUIDE.md](instructions/PRACTICAL_GUIDE.md)** - Start here for practical usage
2. **[WORKFLOW_EXECUTION_GUIDE.md](instructions/WORKFLOW_EXECUTION_GUIDE.md)** - Comprehensive execution guide
3. **[FLAG_USAGE_EXAMPLES.md](instructions/FLAG_USAGE_EXAMPLES.md)** - Real-world examples
4. **[requirements.md](specs/requirements.md)** - System architecture and requirements
5. **[EXECUTION_RULES.md](specs/EXECUTION_RULES.md)** - **Formal enforcement rules (critical)**
6. **[EXECUTION_CONTROL.md](specs/EXECUTION_CONTROL.md)** - Technical specification
7. **[FLAG_PARSER.md](specs/FLAG_PARSER.md)** - Implementation reference

### Key Concepts

- **Autonomous by default** - Fast execution for routine work
- **Flags enable control** - Add checkpoints where needed
- **Risk-aware** - Automatic stops for safety violations
- **Flexible** - From fully autonomous to step-by-step
- **Safe** - Non-negotiable safety rules enforced

### Key Benefits

✅ **Speed** - Complete plans in 30-90 seconds
✅ **Control** - Pause at any point with flags
✅ **Safety** - Automatic stops for high-risk situations
✅ **Intelligence** - Smart escalation when uncertain
✅ **Flexibility** - Adapts to your needs

**The system adapts to your needs: fast when safe, careful when necessary.**
