# Framework Cleanup Plan

## Issue 1: Agents Still Reference Stages/Checkpoints
**Problem:** Agents reference "Stage 1-9", "CHECKPOINT", "Batch Execution"
**Solution:** Reframe as deliverables, not execution stages

**Change:**
- "Stage 1: Intake" → "Output: Requirement validation"
- "Stage 2: Requirements" → "Output: Acceptance criteria"
- Remove "CHECKPOINT" references
- Remove "Batch Execution" language
- Focus on what Copilot delivers, not how it executes

## Issue 2: Move to .github Folder
**Current Structure:**
```
/copilot-instructions.md
/copilot/
  ├── agents/
  ├── skills/
  ├── instructions/
  └── ...
```

**New Structure:**
```
/.github/
  └── copilot/
      ├── copilot-instructions.md (main entry point)
      ├── agents/
      ├── skills/
      ├── instructions/
      └── ...
```

**Benefits:**
- Standard GitHub convention (.github for tooling)
- Separates framework from project code
- User downloads framework in expected location
- Clean root directory

## Issue 3: Make VS Code Copilot Ready
**Actions:**
- Remove all checkpoint/approval references from agents
- Simplify agent language to focus on outputs
- Clear, actionable instructions
- Ready to use out of the box

## Issue 4: Move Large Docs to Instructions
**Files to split:**
- COPILOT_INTEGRATION.md → instructions/copilot-integration-guide.md
- SIMPLIFIED_INTEGRATION.md → Already good, move to instructions/
- BEST_PRACTICES_AUDIT.md → instructions/best-practices.md
- TEMPLATES.md → instructions/templates.md

**Update copilot-instructions.md to reference all**

---

## Implementation Order

1. ✅ Create .github/copilot structure
2. ✅ Move all framework files to .github/copilot
3. ✅ Simplify agents (remove stages/checkpoints)
4. ✅ Move large docs to instructions folder
5. ✅ Update copilot-instructions.md with all references
6. ✅ Commit and push

---

Let's execute this plan!
