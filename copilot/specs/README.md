# Specifications - Formal Rules and Architecture

This folder contains the formal specifications that define how the autonomous workflow system operates.

## File Purpose

### requirements.md
**System Architecture and Principles**
- Core principles (autonomous by default, human control by choice)
- Execution model (autonomous hybrid architecture)
- Execution flags specification
- Agent and skill definitions
- Mandatory delivery stages
- Safety rules (non-negotiable)
- Decision traceability requirements
- Completion criteria

**Use this for:** Understanding the "why" behind system design

---

### EXECUTION_RULES.md ⚠️ **Critical**
**Formal Enforcement Rules**

10 categories of rules that MUST be enforced:

1. **Flag Validation Rules**
   - Type validation
   - Conflict detection
   - Default application

2. **Execution Rules**
   - Batch execution requirements
   - Checkpoint presentation format
   - Sequential stage execution

3. **Safety Rules (Non-Negotiable)**
   - Public API change → STOP
   - WebForms lifecycle violation → STOP
   - Telerik contract break → STOP
   - Missing rollback → STOP
   - Data corruption risk → STOP
   - HIGH risk → CHECKPOINT
   - LOW confidence → ESCALATE

4. **Stage Transition Rules**
   - Completion criteria
   - Skip prevention
   - Checkpoint enforcement

5. **Checkpoint Rules**
   - Mandatory triggers
   - Response handling
   - Timeout behavior

6. **Agent Selection Rules**
   - Mode detection priority
   - Mode-agent mapping
   - Escalation triggers

7. **Skill Invocation Rules**
   - Input validation
   - Output validation
   - Approval gates

8. **Risk Assessment Rules**
   - Risk level calculation
   - Risk-based checkpoints
   - Mitigation documentation

9. **Conflict Resolution Rules**
   - Flag priority order
   - Checkpoint deduplication
   - Impossible configuration rejection

10. **Escalation Rules**
    - Automatic mode escalation
    - User-requested escalation
    - Escalation documentation

**Use this for:** Understanding what MUST and MUST NOT happen

---

### EXECUTION_CONTROL.md
**Technical Execution Specification**
- Execution flow diagrams
- Execution patterns (autonomous, checkpoint, manual, risk-based)
- Batch execution strategy
- Checkpoint communication patterns
- Skill execution in batch
- Error handling
- Performance characteristics

**Use this for:** Technical implementation details

---

### FLAG_PARSER.md
**Flag Parsing Implementation**
- Flag types and validation
- Parsing algorithm (inline, YAML, natural language)
- Execution context creation
- Natural language translation
- Error handling
- Testing scenarios

**Use this for:** Implementing flag parser logic

---

## Quick Reference

### Safety Rules (Always Apply)
```yaml
IMMEDIATE_STOP:
  - Public API change without justification
  - WebForms lifecycle violation
  - Telerik contract breakage
  - Missing rollback procedure
  - Data corruption risk

AUTOMATIC_CHECKPOINT:
  - Risk level: HIGH
  - Confidence: LOW
  - Production environment (HOTFIX mode)
```

### Flag Priority Order
```yaml
1. manual_mode (highest - overrides all)
2. safety_violations (cannot override)
3. high_risk_auto_stop (cannot disable)
4. approve_at_risk
5. approve_before_stage
6. approve_before_skills
7. checkpoint_strategy
8. agent_defaults (lowest)
```

### Risk Calculation
```yaml
RISK_FACTORS:
  - technical_complexity (LOW/MEDIUM/HIGH)
  - impact_scope (LOW/MEDIUM/HIGH)
  - reversibility (LOW/MEDIUM/HIGH)
  - production_risk (LOW/MEDIUM/HIGH)
  - data_risk (LOW/MEDIUM/HIGH)

FORMULA:
  IF ANY = HIGH → RISK = HIGH
  ELIF MOST = MEDIUM → RISK = MEDIUM
  ELIF ALL = LOW → RISK = LOW
  ELSE → RISK = MEDIUM (conservative)
```

### Mode Detection Priority
```yaml
1. Explicit mode stated by user (HIGH confidence)
2. Keyword detection (MEDIUM-HIGH confidence)
3. Pattern analysis (MEDIUM confidence)
4. If confidence < MEDIUM → Escalate to REFINEMENT
```

### Escalation Conditions
```yaml
TO_HOTFIX:
  - severity = CRITICAL
  - environment = production
  - current_mode = BUG

TO_SPIKE:
  - confidence = LOW
  - technical_approach = unknown
  - root_cause = unknown

TO_REFINEMENT:
  - requirements = unclear
  - conflicting_requirements = true
  - scope = ambiguous

TO_FEATURE:
  - current_mode = BUG
  - scope > simple_fix
```

## For Implementers

When implementing the autonomous workflow system:

1. **Read requirements.md** first to understand architecture
2. **Study EXECUTION_RULES.md** to know what must be enforced
3. **Reference EXECUTION_CONTROL.md** for implementation patterns
4. **Use FLAG_PARSER.md** for flag parsing logic

## For Users

Users don't need to read these specs directly. Instead, refer to:
- `copilot/instructions/PRACTICAL_GUIDE.md` - Practical usage
- `copilot/instructions/WORKFLOW_EXECUTION_GUIDE.md` - Comprehensive guide
- `copilot/instructions/FLAG_USAGE_EXAMPLES.md` - Real-world examples

## Enforcement Responsibility

```yaml
Orchestrator:
  - Flag validation
  - Agent selection
  - Mode detection
  - Conflict resolution
  - Escalation

All Agents:
  - Safety rules
  - Risk assessment
  - Stage transitions
  - Checkpoints
  - Execution rules

Skills:
  - Input validation
  - Output validation

System:
  - Timeout handling
  - Response processing
  - Deduplication
```

## Non-Negotiable Constraints

These rules CANNOT be overridden:

✋ **Safety violations** - Immediate stop, no exceptions
✋ **HIGH risk** - Mandatory checkpoint
✋ **LOW confidence** - Must escalate to SPIKE/REFINEMENT
✋ **Production hotfixes** - Manual mode enforced
✋ **Missing rollback** - Cannot proceed

---

**The specs in this folder define the "must" and "must not" rules that make the autonomous workflow system safe, predictable, and controllable.**
