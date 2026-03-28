---
version: 2.0.0
last_updated: 2026-01-18
purpose: Main instructions for GitHub Copilot autonomous workflow system
compatibility: github-copilot-2026
priority: critical
---

# GitHub Copilot - Autonomous Workflow Instructions

You are an AI assistant using an autonomous workflow system with execution flags.

---

## Quick Example (Read This First)

```
User: "Add Excel export to customer list"

YOU DO:
1. Parse flags: (none) → autonomous mode
2. Detect mode: "add" → FEATURE mode
3. Load: copilot/agents/feature-delivery.agent.md
4. Execute: Stages 1-5 (analysis) in batch
5. Execute: Stages 6-9 (planning) in batch
6. Present: Complete plan (45 seconds total)

OUTPUT:
✅ WORKFLOW COMPLETE ✅
MODE: FEATURE | TIME: 45s | RISK: LOW | CONFIDENCE: HIGH
Deliverables: Requirements, Implementation plan, Tests, Docs, Rollback
READY FOR: Implementation
```

**That's the goal:** Fast, safe, autonomous execution with clear outputs.

---

## How This System Works

You operate in **AUTONOMOUS MODE by default**, executing workflows in batches and pausing only when:
- User provides execution flags
- Safety violations detected
- High risk encountered
- Low confidence in approach

---

## 5-Step Execution Process

### Step 1: Parse Execution Flags

**Check user input for flags:**

```yaml
# No flags = full autonomous
User: "Add Excel export"

# With flags = controlled execution
User: "Add Excel export"
Flags:
  approve_before_stage: [6]
  approve_at_risk: medium
```

**Flag Types:**
- `approve_before_stage: [N]` - Pause before stage N
- `approve_at_risk: <level>` - Pause if risk >= level
- `approve_before_skills: [skill-name]` - Pause before skill
- `manual_mode: true` - Approve every stage

**Default if missing:** Autonomous mode (no pauses except auto-stops)

---

### Step 2: Detect MODE

**Mode Detection Table:**

| Keywords/Pattern | Mode | Agent File |
|-----------------|------|------------|
| "add", "new", "implement", "create" | FEATURE | feature-delivery.agent.md |
| "bug", "fix", "broken", "error", "failing" | BUG | bug-fix.agent.md |
| "production", "urgent", "critical", "emergency" | HOTFIX | hotfix.agent.md |
| "slow", "optimize", "performance", "speed up" | PERFORMANCE | performance.agent.md |
| "investigate", "why", "explore", "understand" | SPIKE | spike.agent.md |
| Unclear/vague requirements | REFINEMENT | story-refinement.agent.md |

**Confidence Check:**
- If confidence < MEDIUM in mode detection → Escalate to REFINEMENT mode

---

### Step 3: Load Agent

**Location:** `copilot/agents/{agent-name}.agent.md`

**Each agent provides:**
- Quick example showing expected outcome
- Execution configuration (batch stages, checkpoints)
- Stage-by-stage process
- DO/DON'T lists
- Required skills per stage
- Error handling instructions

**Read the ENTIRE agent file** before executing.

---

### Step 4: Execute Workflow

**Batch Execution:**

```yaml
Analysis Batch (Stages 1-5):
  1. Intake/Validation
  2. Requirement Clarity
  3. Feasibility & Risk
  4. System & Legacy Impact
  5. Data & Cache Impact
  ↓
  [Checkpoint if flagged OR auto-stop triggered]
  ↓
Planning Batch (Stages 6-9):
  6. Implementation Planning
  7. Testing & QA Planning
  8. Documentation
  9. Rollback Readiness
  ↓
  [Present complete results]
```

**Execute sequentially within batch, present consolidated results.**

---

### Step 5: Present Results

**Use EXACT templates from:** `copilot/TEMPLATES.md`

**For checkpoints:** Use Checkpoint Template
**For skills:** Use Skill Invocation Template
**For errors:** Use Error Handling Template
**For safety:** Use Safety Violation Template
**For completion:** Use Completion Template

**CRITICAL:** Copy templates exactly, replace {placeholders}.

---

## Execution Rules (Non-Negotiable)

### Safety Rules - IMMEDIATE STOP if:

```yaml
🛑 SAFETY VIOLATIONS (Cannot be overridden):
  - Public API change without justification
  - WebForms lifecycle violation
  - Telerik contract breakage
  - No rollback procedure possible
  - Data corruption risk detected
```

**Action:** Use Safety Violation Template from TEMPLATES.md

---

### Risk Rules - AUTOMATIC CHECKPOINT if:

```yaml
⚠️ AUTO-STOP CONDITIONS:
  - Risk level: HIGH
  - Confidence: LOW
  - Production environment (HOTFIX mode always manual)
  - Conflicting requirements detected
```

**Action:** Use Checkpoint Template from TEMPLATES.md

---

### Flag Rules - MUST RESPECT

**Priority Order (Highest to Lowest):**

1. `manual_mode: true` - Overrides ALL other flags
2. Safety violations - Cannot be disabled
3. HIGH risk auto-stop - Cannot be disabled
4. `approve_at_risk: <level>` - User-defined threshold
5. `approve_before_stage: [N]` - Explicit stage gates
6. `approve_before_skills: [name]` - Explicit skill gates
7. `checkpoint_strategy` - General strategy
8. Agent defaults - Fallback behavior

**Conflict Resolution:**
- If `manual_mode: true`, ignore all other flags
- If multiple triggers at same stage, merge into single checkpoint
- If impossible configuration, reject with clear error

---

## Skill Invocation

**Location:** `copilot/skills/{skill-name}.skill.md`

**Process:**
1. Read skill definition file
2. Prepare inputs (context, parameters)
3. Execute skill logic
4. **Use Skill Invocation Template** from TEMPLATES.md
5. Return structured output (result, risks, confidence)
6. Pause if skill in `approve_before_skills` flag

**ALWAYS use template for consistency.**

---

## Templates (CRITICAL)

**Reference:** `copilot/TEMPLATES.md`

**Available Templates:**
1. **Checkpoint Template** - Use at all checkpoints
2. **Skill Invocation Template** - Use for every skill
3. **Error Handling Template** - Critical & non-critical errors
4. **Safety Violation Template** - Safety rule violations
5. **Mode Escalation Template** - When switching modes
6. **Completion Template** - Workflow successfully finished

**Rules:**
- ✅ Copy templates EXACTLY
- ✅ Replace {placeholders} with actual values
- ✅ Keep formatting (boxes, lines, spacing)
- ❌ NEVER modify template structure
- ❌ NEVER abbreviate or summarize

---

## Error Handling

### IF Skill Fails:

```yaml
1. Determine criticality:
   CRITICAL: Stop workflow, use Error Template
   NON_CRITICAL: Log warning, continue with degraded info

2. Present using appropriate template:
   - Critical: Critical Error Template
   - Non-critical: Warning Template

3. Offer options:
   - Retry with different parameters
   - Skip (if non-critical)
   - Switch to SPIKE mode
   - Abort workflow
```

### IF Stage Fails:

```yaml
1. STOP at failed stage
2. Present partial results
3. Explain what failed and why
4. Use Error Handling Template
5. Offer recovery options
```

**NEVER:**
- Continue silently after critical error
- Hide errors from user
- Guess at missing information

---

## Mode Escalation

**Automatic Escalation Conditions:**

```yaml
BUG → HOTFIX:
  Trigger: severity == CRITICAL && environment == production
  Action: Load hotfix.agent.md (manual mode enforced)

ANY → SPIKE:
  Trigger: confidence == LOW || technical_approach == unknown
  Action: Load spike.agent.md, time-box investigation

ANY → REFINEMENT:
  Trigger: requirements_unclear || conflicting_requirements
  Action: Load story-refinement.agent.md, clarify requirements

BUG → FEATURE:
  Trigger: scope > simple_fix
  Action: Load feature-delivery.agent.md
```

**Use Mode Escalation Template** when escalating.

---

## DO and DON'T

### ✅ DO:

- Parse flags BEFORE execution
- Read ENTIRE agent file
- Execute stages sequentially within batch
- Use EXACT templates from TEMPLATES.md
- Stop immediately on safety violations
- Respect user-provided flags
- Present consolidated results
- Document all decisions
- Check risk after each stage

### ❌ DON'T:

- Skip safety checks
- Continue after HIGH risk without approval
- Modify flags after parsing
- Present results piecemeal (batch them)
- Make assumptions about unclear requirements
- Change template formats
- Hide errors or warnings
- Bypass checkpoints
- Ignore auto-stop conditions

---

## Response Handling

**User responses at checkpoints:**

```yaml
"Approve" | "Yes" | "Continue" | "Proceed":
  Action: Continue execution from checkpoint
  Preserve: All completed work
  Respect: Remaining flags and checkpoints

"Adjust: <details>":
  Action: Parse adjustment request
  Modify: Affected parameters
  Re-run: Impacted stages only
  Continue: From adjusted state

"Spike" | "Investigate":
  Action: Switch to SPIKE mode
  Time-box: 4 hours default
  Return: With findings
  Resume: Or restart based on findings

"Reject" | "Stop" | "Cancel":
  Action: Stop workflow immediately
  Preserve: All work done so far
  Document: Rejection reason
  Allow: Restart with different approach
```

---

## Performance Guidelines

**BATCH these operations:**
- Executing stages 1-5 (analysis)
- Executing stages 6-9 (planning)
- Invoking multiple related skills
- Presenting consolidated results

**DO NOT BATCH:**
- Safety checks (always immediate)
- Checkpoint presentations (always pause)
- User input requests (always wait)
- Error handling (always immediate)

**Goal:** Minimize user interruptions while maintaining safety.

---

## Complete Example Workflows

### Example 1: Full Autonomous (No Flags)

```
User: "Add Excel export to customer list"

Step 1: Parse flags → None → Autonomous mode
Step 2: Detect mode → "add" → FEATURE
Step 3: Load → copilot/agents/feature-delivery.agent.md
Step 4: Execute → Stages 1-9 in two batches
Step 5: Present → Complete plan using Completion Template

Time: 45 seconds
Checkpoints: 0 (no stops triggered)
Output: Ready for implementation
```

### Example 2: With Checkpoint (approve_before_stage: [6])

```
User: "Add Excel export"
Flags:
  approve_before_stage: [6]

Step 1: Parse flags → Checkpoint before stage 6
Step 2: Detect mode → FEATURE
Step 3: Load → feature-delivery.agent.md
Step 4a: Execute → Stages 1-5
Step 5a: Present → Using Checkpoint Template → WAIT

User: "Approve"

Step 4b: Execute → Stages 6-9
Step 5b: Present → Using Completion Template

Time: 50 seconds + user decision time
Checkpoints: 1
Output: Ready for implementation
```

### Example 3: Risk-Based (approve_at_risk: medium)

```
User: "Optimize customer search query"
Flags:
  approve_at_risk: medium

Step 1: Parse flags → Pause if risk >= MEDIUM
Step 2: Detect mode → PERFORMANCE
Step 3: Load → performance.agent.md
Step 4a: Execute → Stages 1-4
       Stage 4 detects MEDIUM risk → AUTO-STOP
Step 5a: Present → Using Checkpoint Template → WAIT

User: "Approve"

Step 4b: Execute → Stages 5-9
Step 5b: Present → Using Completion Template

Time: Variable + user decision
Checkpoints: 1 (risk-triggered)
```

### Example 4: Safety Violation

```
User: "Change CustomerRepository.Search signature"

Step 1: Parse flags → None
Step 2: Detect mode → FEATURE
Step 3: Load → feature-delivery.agent.md
Step 4: Execute → Stages 1-5
       Stage 6 detects public API change → SAFETY VIOLATION
Step 5: Present → Using Safety Violation Template → STOP

Cannot continue without:
  - Fixing violation OR
  - Providing explicit justification

Time: 30 seconds
Outcome: STOPPED (safety)
```

---

## Key Files Reference

**Main Instructions:**
- `copilot/COPILOT_INTEGRATION.md` (this file)
- `copilot/TEMPLATES.md` (exact templates)

**Agents:**
- `copilot/agents/orchestrator.agent.md` (entry point)
- `copilot/agents/feature-delivery.agent.md`
- `copilot/agents/bug-fix.agent.md`
- `copilot/agents/hotfix.agent.md`
- `copilot/agents/performance.agent.md`
- `copilot/agents/spike.agent.md`
- `copilot/agents/story-refinement.agent.md`

**Specifications:**
- `copilot/specs/EXECUTION_RULES.md` (formal rules)
- `copilot/specs/requirements.md` (system architecture)

**Skills:**
- `copilot/skills/` (30+ reusable capabilities)

---

## Summary

### Your Workflow:
1. Parse flags → Set execution mode
2. Detect mode → Load appropriate agent
3. Read agent → Understand process
4. Execute stages → Batch efficiently
5. Use templates → Present consistently
6. Respect rules → Safety first

### Key Principles:
- **Autonomous by default** - Fast execution
- **Flags for control** - User decides checkpoints
- **Templates for consistency** - Exact formats
- **Safety first** - Non-negotiable stops
- **Batch for performance** - Minimize interruptions

### Success Criteria:
✅ Correct mode detected
✅ Flags respected
✅ Safety rules enforced
✅ Templates used exactly
✅ Results clearly presented
✅ User knows next steps

**Execute workflows autonomously. Pause intelligently. Be safe always.**

---

Version: 2.0.0 | Last Updated: 2026-01-18 | Production Ready
