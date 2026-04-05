# Integration Guide

## How to Add Autonomous Workflow System to Your Existing Copilot Instructions

You have three options for integrating the autonomous workflow system with your existing `.github/copilot-instructions.md`:

---

## Option 1: Simple Reference (Recommended)

Add this section to your existing `.github/copilot-instructions.md`:

```markdown
## Autonomous Workflow System

When the user requests workflow automation (features, bugs, performance, etc.), use the autonomous workflow system:

**Entry Point:** Load `agents/orchestrator.agent.md`

**Quick Reference:**
- Parse execution flags (if provided)
- Detect MODE: FEATURE, BUG, HOTFIX, PERFORMANCE, SPIKE, or REFINEMENT
- Load appropriate agent from `agents/`
- Execute per agent configuration
- Respect safety rules in `specs/README.md (archived)`

**Modes:**
- `FEATURE` → `feature-delivery.agent.md`
- `BUG` → `bug-fix.agent.md`
- `HOTFIX` → `hotfix.agent.md` (production emergencies)
- `PERFORMANCE` → `performance.agent.md`
- `SPIKE` → `spike.agent.md` (investigations)
- `REFINEMENT` → `story-refinement.agent.md` (unclear requirements)

**Execution Flags:**
```yaml
approve_before_stage: [6]     # Pause before stage 6
approve_at_risk: medium        # Pause if risk >= medium
manual_mode: true              # Approve every stage
```

**Non-Negotiable Rules:**
- Safety violations → IMMEDIATE STOP
- HIGH risk → AUTOMATIC CHECKPOINT
- LOW confidence → ESCALATE to SPIKE/REFINEMENT

For full details, see: `instructions/integration-overview.md`
```

---

## Option 2: Inline Instructions

If you want full instructions in your main file, copy the entire content from `instructions/integration-overview.md` and paste it as a section in your `.github/copilot-instructions.md`.

**Pros:** Everything in one file
**Cons:** Makes your instructions file longer

---

## Option 3: Conditional Loading

Add trigger keywords to your existing instructions:

```markdown
## Workflow Detection

If the user's request matches these patterns, activate the autonomous workflow system:

**Trigger Keywords:**
- "add", "new", "implement", "create" → FEATURE mode
- "bug", "fix", "broken", "error" → BUG mode
- "production", "urgent", "critical", "emergency" → HOTFIX mode
- "slow", "optimize", "performance" → PERFORMANCE mode
- "investigate", "why", "explore" → SPIKE mode
- Unclear requirements → REFINEMENT mode

**When triggered:**
1. Load `agents/orchestrator.agent.md`
2. Follow orchestrator instructions
3. Load appropriate specialized agent
4. Execute workflow per agent configuration

For detailed workflow execution, refer to: `instructions/integration-overview.md`
```

---

## File Structure After Integration

```
your-project/
├── .github/
│   ├── copilot-instructions.md (your existing instructions + workflow reference)
│   ├── instructions/ (including integration-overview.md)
│   ├── specs/ (formal rules, mostly archived)
│   ├── agents/ (workflow definitions)
│   └── skills/ (capabilities)
└── [your other files]
```

---

## Recommended Approach

**For most projects:** Use **Option 1** (Simple Reference)

Add a concise section to your existing `.github/copilot-instructions.md` that:
- Explains when to use the workflow system
- Shows how to detect mode
- References the full instructions in `instructions/integration-overview.md`

This keeps your main instructions clean while making the workflow system available when needed.

---

## Example Integration

Here's what your existing `.github/copilot-instructions.md` might look like with the workflow system integrated:

```markdown
# Your Project - Copilot Instructions

[Your existing instructions here...]

## Project-Specific Guidelines
[Your existing guidelines...]

## Coding Standards
[Your existing standards...]

---

## Autonomous Workflow System

For feature development, bug fixes, and workflow automation, use the autonomous workflow system.

### When to Use
- User requests a new feature
- User reports a bug
- User requests performance optimization
- User wants to investigate something
- Requirements are unclear

### Quick Start
1. Detect mode from user request (FEATURE, BUG, HOTFIX, etc.)
2. Load orchestrator: `agents/orchestrator.agent.md`
3. Parse execution flags (if provided)
4. Load appropriate agent
5. Execute workflow

### Execution Modes
- **Autonomous (default):** Execute all stages in batch
- **With checkpoints:** Pause at user-specified stages
- **Risk-based:** Auto-pause when risk detected
- **Manual:** Approve every stage

### Safety Rules (Non-Negotiable)
- Safety violations → STOP immediately
- HIGH risk → Checkpoint required
- LOW confidence → Escalate to investigation

**Full Documentation:** `instructions/integration-overview.md`
**Formal Rules:** `specs/README.md (archived)`
**User Guides:** `instructions/`

---

[Rest of your existing instructions...]
```

---

## Summary

✅ **Best Practice:** Add a concise reference section to your existing instructions
✅ **Keep:** Full workflow details in `instructions/integration-overview.md`
✅ **Maintain:** Your existing project-specific instructions
✅ **Activate:** Workflow system only when needed

This modular approach lets you:
- Keep your main instructions focused on your project
- Use workflow system when appropriate
- Maintain both systems independently
- Scale as needed
