# PURPOSE

This prompt defines the REQUIREMENTS for an AI-assisted delivery architecture
that uses a COMBINATION of AGENTS and SKILLS to safely deliver changes in a
LEGACY ASP.NET WebForms application.

This file does NOT execute work.
This file defines RULES, EXPECTATIONS, and CONSTRAINTS that all workflows,
agents, and skills MUST follow.

---

# CORE PRINCIPLES

1. Capability is decoupled from orchestration
2. Skills are reusable and independently invocable
3. Agents orchestrate; skills execute
4. Legacy safety overrides optimization
5. Decisions are more important than code
6. Documentation is part of delivery, not an afterthought
7. **Autonomous execution by default, human control by choice**
8. **Fast feedback through batch execution with smart checkpoints**

---

# EXECUTION MODEL

## Autonomous Hybrid Architecture

The system operates in **AUTONOMOUS MODE by default** with optional human intervention gates.

### Default Behavior: Autonomous Batch Execution

```yaml
execution_mode: autonomous
behavior: 
  - Execute all analysis stages in batch
  - Invoke all necessary skills automatically
  - Return consolidated results in single response
  - Pause only at predefined checkpoints or risk triggers
```

### Human Intervention Control

Human approval can be injected at any point using **execution flags**:

```yaml
execution_flags:
  approve_before_stage: [<stage_numbers>]  # Pause before specific stages
  approve_at_risk: <high|medium|low>       # Pause if risk meets threshold
  approve_before_skills: [<skill_names>]   # Pause before specific skills
  manual_mode: <boolean>                    # Require approval at every stage
```

### Automatic Stop Conditions (Non-Negotiable)

The system MUST pause for human decision when:

```yaml
automatic_stops:
  - risk_level: HIGH
  - confidence: LOW
  - safety_violation: detected
  - unknown_behavior: encountered
  - public_api_change: required
  - conflicting_requirements: detected
```

### Checkpoint Strategy

**Smart Checkpoints** occur at decision commitment points:

```yaml
checkpoint_types:
  analysis_complete:
    after_stages: [1, 2, 3, 4, 5]
    question: "Analysis complete. Approve implementation planning?"
    
  planning_complete:
    after_stages: [6, 7, 8, 9]
    question: "Plan ready. Approve for execution?"
    
  risk_detected:
    trigger: risk_level >= medium
    question: "Risk detected. Review and approve?"
    
  safety_concern:
    trigger: safety_rule_violation
    question: "Safety concern requires decision."
```

---

# DEFINITIONS

## AGENT

An agent is responsible for:

- Deciding WHAT needs to be done
- Deciding WHEN it should happen
- Deciding WHICH skills to invoke
- Deciding WHETHER to stop or continue
- **Executing stages in batch by default**
- **Pausing only when flags require or risks demand it**

Agents MUST NOT:

- Contain deep domain logic
- Re-implement skill behavior
- Produce unstructured output
- **Pause unnecessarily for low-risk decisions**
- **Request approval for routine skill invocations**

### Agent Execution Contract

Every agent MUST declare:

```yaml
execution_configuration:
  default_mode: autonomous | manual
  batch_execute_stages: [<stage_list>]
  auto_stop_conditions: [<conditions>]
  checkpoint_after: [<stage_numbers>]
  respect_flags: true
```

---

## SKILL

A skill is:

- Atomic
- Stateless
- Reusable
- Deterministic
- **Executable without approval (unless flagged)**

Skills:

- Perform ONE well-defined capability
- Can be executed independently
- Accept explicit input
- Produce structured output
- **Execute immediately when invoked (no approval needed by default)**

Skills MUST NOT:

- Decide workflow order
- Make product or release decisions
- Assume execution context
- **Request human approval (that's the agent's job)**

---

# SYSTEM CONTEXT (FIXED)

- Application Type: ASP.NET WebForms (Legacy)
- UI Framework: Telerik
- Cache Layer: Redis
- Database: MSSQL
- Version Control: Git-based
- Delivery Model: Incremental, rollback-safe
- **Execution Model: Autonomous with optional gates**

All agents and skills MUST assume this context unless explicitly overridden.

---

# REQUIRED MODES OF OPERATION

The system MUST support the following MODES:

- FEATURE delivery
- BUG FIX delivery
- STORY REFINEMENT
- RESEARCH / SPIKE
- DATA & PERFORMANCE OPTIMIZATION
- HOTFIX (production-safe)

The selected MODE MUST be explicitly stated at the beginning of execution.

**Each mode supports both autonomous and manual execution via flags.**

---

# MANDATORY DELIVERY STAGES

No workflow may skip these stages unless explicitly justified:

1. Intake / Triage
2. Requirement Clarity (or explicit uncertainty)
3. Feasibility & Risk Assessment
4. System & Legacy Impact Analysis
5. Data & Cache Impact (if applicable)
6. Implementation (minimal diff)
7. Regression & QA Planning
8. Documentation
9. Release & Rollback Readiness

**Stages 1-5 execute in batch (analysis) by default.**
**Checkpoint after stage 5 before implementation planning.**
**Stages 6-9 execute in batch (planning) after approval.**

---

# SKILL INVOCATION REQUIREMENTS

Whenever a skill is used, the following structure is REQUIRED:

SKILL: <skill.name>

INPUT:

- Context
- Constraints
- Assumptions

OUTPUT:

- Structured result
- Risks
- Confidence level

Skills MUST NOT produce free-form or narrative-only output.

**Skills execute immediately without approval unless:**

- Execution flags require approval for this specific skill
- Agent determines human decision needed based on risk

---

# REQUIRED SKILL CATEGORIES

The architecture MUST support skills in the following categories:

## Product & Jira

- Story refinement
- Acceptance criteria expansion
- Bug classification
- Spike definition

## Legacy System Analysis

- WebForms lifecycle analysis
- Telerik control impact
- Safe-change boundary detection

## Data & Performance

- LINQ-to-SQL tracing
- Query optimization
- Stored procedure decisioning
- Index analysis

## Cache

- Redis key strategy analysis
- Invalidation mapping
- Stampede risk detection

## Quality & Release

- WebForms regression analysis
- Test scenario generation
- PR metadata generation
- Rollback planning

## Documentation

- Change logs
- Decision records
- Risk documentation

**All skills execute autonomously unless execution flags override.**

---

# AGENT RESPONSIBILITY REQUIREMENTS

Agents MUST:

- Declare intent before acting
- State assumptions explicitly
- Stop execution when uncertainty is high
- Escalate unknowns to SPIKE mode
- **Execute stages in batch when risk is acceptable**
- **Respect execution flags when provided**
- **Present consolidated results at checkpoints**

Agents MUST NOT:

- Write production code directly
- Optimize prematurely
- Hide uncertainty
- Skip documentation steps
- **Pause for approval on routine operations**
- **Ignore automatic stop conditions**

---

# EXECUTION FLAG SYNTAX

## Flag Declaration

Users control execution flow with optional flags:

```yaml
# Full autonomous (default if no flags)
<no flags provided>

# Stop before specific stages
flags:
  approve_before_stage: [6]  # Stop before implementation planning

# Stop at risk threshold
flags:
  approve_at_risk: medium  # Stop if risk is medium or higher

# Stop before specific skills
flags:
  approve_before_skills: [linq-query-tracer, redis-cache-strategy-analyzer]

# Full manual control
flags:
  manual_mode: true  # Approve every stage
```

## Flag Examples

**Example 1: Fully Autonomous (Default)**

```
User: "Add Excel export to customer list"
[No flags = full batch execution]

Output: Complete analysis and plan in one response
```

**Example 2: Checkpoint Before Implementation**

```
User: "Add Excel export to customer list"
Flags:
  approve_before_stage: [6]

Output: 
  - Stages 1-5 complete (analysis)
  - CHECKPOINT: "Approve implementation planning?"
  [WAITING]
User: "Approved"
Output:
  - Stages 6-9 complete (planning)
```

**Example 3: Stop on Medium Risk**

```
User: "Optimize customer search performance"
Flags:
  approve_at_risk: medium

Output:
  - Analysis reveals MEDIUM risk
  - CHECKPOINT: "Risk: MEDIUM. Review before continuing?"
```

**Example 4: Manual Step-by-Step**

```
User: "Add Excel export to customer list"
Flags:
  manual_mode: true

Output:
  - Stage 1 complete
  - CHECKPOINT: "Continue to stage 2?"
[Repeat for each stage]
```

---

# LEGACY SAFETY RULES (NON-NEGOTIABLE)

- Public APIs must not change without justification
- WebForms lifecycle must be respected
- Telerik contracts must not be broken
- Redis invalidation must be explicit
- SQL behavior must be observable
- Rollback must always be possible

If any rule is violated, the workflow MUST stop and report.

**These rules trigger automatic stops regardless of execution flags.**

---

# DECISION TRACEABILITY

Every significant decision MUST be traceable to:

- A requirement
- A spike finding
- A documented constraint

Undocumented decisions are considered defects.

**In autonomous mode, decisions are documented in batch output.**
**In manual mode, decisions are presented at each checkpoint.**

---

# COMPLETION CRITERIA

A workflow is considered COMPLETE only when:

- Requirements are explicit
- Risks are understood
- Skills were reused appropriately
- Changes are minimal and safe
- Documentation exists
- Rollback steps are defined

**Completion is independent of execution mode (autonomous vs manual).**

---

# FAILURE MODES (EXPECTED)

The system MUST gracefully handle:

- Incomplete requirements
- Conflicting acceptance criteria
- Unknown legacy behavior
- Performance uncertainty

In these cases, the system MUST:

- Switch to REFINEMENT or SPIKE mode
- Clearly communicate blockers
- Avoid speculative implementation
- **Automatically pause for human decision**

---

# ORCHESTRATOR BEHAVIOR

## Primary Responsibilities

The orchestrator is the **entry point** and must:

1. **Detect MODE** from user input
2. **Parse execution flags** (if provided)
3. **Load target agent** with flag configuration
4. **Execute or delegate** based on mode
5. **Monitor for stop conditions**
6. **Present results** at checkpoints

## Orchestrator Execution Logic

```yaml
orchestrator_flow:
  1_parse_input:
    - Extract request
    - Extract flags (if any)
    - Set default: autonomous mode
  
  2_detect_mode:
    - Analyze request
    - Determine MODE (FEATURE, BUG, etc.)
    - Confidence level
  
  3_configure_execution:
    - Apply flags to agent
    - Set checkpoint strategy
    - Configure stop conditions
  
  4_delegate:
    - Load target agent
    - Pass flags and configuration
    - Execute or coordinate execution
  
  5_monitor:
    - Watch for stop conditions
    - Check risk levels
    - Enforce safety rules
  
  6_checkpoint_handling:
    - Present consolidated results
    - Request approval if needed
    - Continue or stop based on response
```

## Orchestrator Output Format

```yaml
orchestrator_output:
  mode: <detected mode>
  confidence: <high|medium|low>
  execution_mode: <autonomous|manual|hybrid>
  flags_applied: [<list>]
  target_agent: <agent name>
  checkpoint_strategy: <description>
  
  [If autonomous mode]
  status: executing_batch
  
  [If checkpoint reached]
  checkpoint:
    stage_complete: <stages>
    results: <consolidated output>
    decision_required: <yes|no>
    options: [<approve|reject|adjust>]
```

---

# AGENT EXECUTION PATTERNS

## Pattern 1: Full Autonomous (Default)

```yaml
user_input: "Add Excel export to customer list"
flags: none

agent_behavior:
  - Execute stages 1-5 (analysis)
  - Invoke all necessary skills automatically
  - Execute stages 6-9 (planning)
  - Return complete plan
  
response_time: 30-60 seconds
approval_points: 0 (unless risk detected)
```

## Pattern 2: Checkpoint at Implementation

```yaml
user_input: "Add Excel export to customer list"
flags:
  approve_before_stage: [6]

agent_behavior:
  - Execute stages 1-5 (analysis)
  - CHECKPOINT: Present analysis
  - [WAIT for approval]
  - Execute stages 6-9 (planning)
  - Return complete plan
  
approval_points: 1
```

## Pattern 3: Risk-Based Pausing

```yaml
user_input: "Optimize database query performance"
flags:
  approve_at_risk: medium

agent_behavior:
  - Execute stages 1-3
  - Stage 4 detects MEDIUM risk
  - CHECKPOINT: Present risk analysis
  - [WAIT for approval]
  - Continue stages 5-9
  
approval_points: 1 (triggered by risk)
```

## Pattern 4: Manual Control

```yaml
user_input: "Add Excel export to customer list"
flags:
  manual_mode: true

agent_behavior:
  - Execute stage 1
  - CHECKPOINT
  - Execute stage 2
  - CHECKPOINT
  - [Repeat for each stage]
  
approval_points: 9 (one per stage)
```

---

# SKILL EXECUTION IN AUTONOMOUS MODE

## Skill Invocation Rules

```yaml
default_behavior: immediate_execution

skill_invocation:
  1_agent_determines_need:
    - Agent identifies required skill
    - Checks execution flags
    
  2_execute_immediately_if:
    - No skill-specific flag blocking it
    - Risk is acceptable
    - Skill is available
    
  3_batch_with_others:
    - Multiple skills can execute in sequence
    - Results compiled
    - Presented together at checkpoint
    
  4_flag_override:
    - If skill is flagged for approval
    - Pause before executing
    - Present skill invocation for approval
```

## Skill Output Consolidation

In autonomous mode, skill outputs are **consolidated** into agent response:

```yaml
consolidated_output:
  stage_1_intake:
    skill: jira-story-intake
    result: <structured output>
  
  stage_2_requirements:
    skill: acceptance-criteria-expander
    result: <structured output>
  
  stage_4_legacy_impact:
    skills:
      - webforms-lifecycle-analyzer: <output>
      - telerik-impact-checker: <output>
      - safe-change-boundary-detector: <output>
  
  final_assessment:
    risk: LOW
    confidence: HIGH
    ready_for: implementation
```

---

# CHECKPOINT COMMUNICATION PATTERN

## Checkpoint Format

```yaml
=== CHECKPOINT: <checkpoint_name> ===

STAGES COMPLETED: <list>

CONSOLIDATED RESULTS:
<all relevant outputs>

RISK ASSESSMENT:
  Level: <LOW|MEDIUM|HIGH>
  Factors: [<list>]

CONFIDENCE: <HIGH|MEDIUM|LOW>

DECISION REQUIRED:
  Question: <specific question>
  Options:
    [ ] Approve - Continue to next phase
    [ ] Adjust - Modify approach
    [ ] Spike - Need more investigation
    [ ] Reject - Stop workflow

NEXT STEPS IF APPROVED:
<what will happen next>

================================
```

## Response Handling

User responses at checkpoints:

```yaml
approve: 
  - Continue execution
  - Apply next batch of stages
  - Respect remaining flags

adjust:
  - Present configuration options
  - Allow parameter changes
  - Re-run affected stages

spike:
  - Switch to SPIKE mode
  - Time-box investigation
  - Return to original workflow after

reject:
  - Stop workflow
  - Document reason
  - Preserve analysis done so far
```

---

# PHILOSOPHY STATEMENT

In legacy systems:

- Speed comes from clarity
- Safety comes from constraints
- Quality comes from boring solutions

Agents exist to reduce cognitive load.
Skills exist to preserve expertise.

**Autonomous execution exists to maximize throughput.**
**Human checkpoints exist to maintain control.**
**Flags exist to balance speed with safety.**

---

# IMPLEMENTATION STATUS

## Created Components

### Agents (7 total - ALL CREATED)

✅ orchestrator.md
✅ feature-delivery.md
✅ bug-fix.md
✅ spike.md
✅ story-refinement.md
✅ performance.md
✅ hotfix.md

### Skills (5 core + 25 planned)

✅ acceptance-criteria-expander.md
✅ webforms-lifecycle-analyzer.md
✅ linq-query-tracer.md
✅ redis-cache-strategy-analyzer.md
✅ minimal-diff-planner.md

📋 **High Priority Skills to Create:**

- webforms-regression-analyzer.md
- test-scenario-generator.md
- rollback-plan-generator.md
- telerik-impact-checker.md
- safe-change-boundary-detector.md
- n-plus-one-detector.md
- cache-invalidation-mapper.md

### Documentation (ALL CREATED)

✅ README.md
✅ QUICK_REFERENCE.md
✅ AGENT_SKILL_INDEX.md
✅ GETTING_STARTED.md

---

# NEXT STEPS FOR EXECUTION MODEL

## Required Updates to Existing Agents

Each agent needs execution configuration added:

```yaml
# Add to each agent.md file
execution_configuration:
  default_mode: autonomous
  batch_execute_stages: [<stage_list>]
  checkpoint_after: [<stage_numbers>]
  auto_stop_conditions:
    - risk_level: HIGH
    - confidence: LOW
    - safety_violation: true
  respect_flags: true
```

## Required Flag Parser

Create utility for parsing execution flags:

```python
# execution_flag_parser.py
def parse_flags(user_input):
    """Extract execution flags from user input"""
    flags = {
        'mode': 'autonomous',  # default
        'approve_before_stage': [],
        'approve_at_risk': None,
        'approve_before_skills': [],
        'manual_mode': False
    }
    # Parse logic here
    return flags
```

## Integration Pattern

```yaml
How it works together:
  
  1. User provides input (with optional flags)
  2. Orchestrator parses flags
  3. Orchestrator loads target agent with flag config
  4. Agent executes batch stages
  5. Agent pauses at flagged checkpoints or auto-stops
  6. Agent presents consolidated results
  7. User approves or adjusts
  8. Agent continues
  9. Complete output returned
```

---

# SUMMARY

This architecture provides:

✅ **Autonomous by default** - Fast execution without unnecessary pauses
✅ **Human control available** - Flags enable intervention anywhere
✅ **Smart checkpoints** - Stop at decision points, not busy work
✅ **Risk-aware** - Automatic stops for safety violations
✅ **Batch execution** - Multiple stages/skills execute together
✅ **Consolidated output** - All results presented together
✅ **Flexible control** - From full autonomous to step-by-step manual
✅ **Safety preserved** - All legacy rules still enforced

**The best of both worlds: Speed when safe, control when needed.**
