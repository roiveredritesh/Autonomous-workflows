---
version: 1.0.0
last_updated: 2026-03-07
purpose: Keep Copilot workflow outputs concise and responsive
---

# Token Budget Policy

## Goals
- Keep default responses short and action-oriented.
- Preserve deterministic structure while minimizing context bloat.
- Move non-essential detail to optional appendix sections.

## Default Output Budgets

### Analysis Batch (Stages 1-5)
- Summary: max 12 lines
- Risks table: max 6 rows
- Dependencies/blockers: max 5 bullets

### Planning Batch (Stages 6-9)
- Implementation plan: max 10 bullets
- Test plan: max 10 bullets
- Rollback plan: max 6 bullets

### Checkpoint Output
- Consolidated results: max 20 lines
- Decision block: required (exact template)
- Structured payload: required

### Completion Output
- Summary: max 8 lines
- Next steps: max 5 items
- Structured payload: required

## Expansion Rule

If user asks for details, include:
- `APPENDIX: Detailed Analysis` (unbounded as requested)
- Keep primary decision section within budgets.

## Hard Limits

- Never omit safety-critical information to satisfy budget.
- Never omit mandatory template sections.
- If budget is exceeded due to safety/error context, mark:
  `BUDGET_EXCEPTION: safety_critical_context`
