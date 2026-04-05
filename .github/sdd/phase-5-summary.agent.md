---
name: sdd-phase-5-summary
description: SDD Phase 5 — Final Summary (Step 7). Synthesises all output files into an executive summary with final risk, confidence, delivered items, and next steps.
model: Claude Haiku 4.5 (copilot)
tools: [read, edit, todo]
---

# SDD Phase 5 — Summary Agent

## Covers
- **Step 7:** Final Summary

## Prerequisites
Read all of the following before generating the summary:
1. `output/{title-slug}/00-metadata.yaml`
2. `output/{title-slug}/01-requirement-impact.md`
3. `output/{title-slug}/02-story-refinement.md`
4. `output/{title-slug}/03-code-planning.md`
5. `output/{title-slug}/04-execution.md`
6. `output/{title-slug}/05-verification-testing.md`
7. `output/{title-slug}/06-defects-round-*.md` (all rounds, if any)

If any file from steps 1–6 is missing, note it in the summary as incomplete.

---

## Step 7: Final Summary

### 7.1 Synthesise Results

From all output files, extract:

| Item | Source |
|------|--------|
| Work type and title | 00-metadata.yaml |
| Requirements and AC count | 01 + 02 |
| Risk level (initial vs final) | 01 → 05 |
| Files modified, lines changed | 04-execution.md |
| Test results (final round) | 05-verification-testing.md |
| Defect rounds needed | 06-defects-round-*.md |
| Known issues remaining | 05 / user SKIP decisions |

### 7.2 Compute Final Confidence

| Condition | Confidence |
|---|---|
| All ACs pass, 0 defect rounds | HIGH |
| All ACs pass, 1-2 defect rounds | MEDIUM |
| All ACs pass, 3 defect rounds | MEDIUM |
| Known issues remaining (SKIP) | LOW |

### 7.3 Save Final Summary

Create `output/{title-slug}/07-final-summary.md`:

```markdown
# Final Summary — {title}
**Workflow:** {title-slug}
**Work Type:** {WORK_TYPE}
**Jira:** {ticket or N/A}
**Completed:** {date}

---

## Executive Summary
{2-3 sentence plain language description of what was delivered and how it was verified}

## What Was Delivered
- {specific item 1}
- {specific item 2}

## Acceptance Criteria
| # | Criterion | Result |
|---|-----------|--------|
| AC-01 | {description} | ✅ PASS |
| AC-02 | {description} | ✅ PASS |

## Code Changes
| File | Change | Lines |
|------|--------|-------|
| {file} | {description} | +{N}/-{N} |

## Testing
- Total Scenarios : {N}
- Passed          : {N}
- Failed          : {N}
- Defect Rounds   : {N}
- Known Issues    : {NONE or list}

## Risk Assessment (Final)
- Initial Risk : {level from Step 1}
- Final Risk   : {level after testing}
- Confidence   : {HIGH|MEDIUM|LOW}

## Rollback
{brief rollback procedure reference — point to 03-code-planning.md}

## Next Steps
- {e.g. Deploy to staging}
- {e.g. Notify QA team}
- {e.g. Close Jira ticket}

## Lessons Learned
{Any patterns or recurring issues noted during this workflow}
```

### 7.4 Update Metadata

Update `output/{title-slug}/00-metadata.yaml`:
- Set `completed_at` to current datetime
- Set `status` to `completed`
- Set `current_phase` to `done`
- Set `risk_level` to final risk
- Set `confidence` to final confidence

---

## Completion Display

```
🎉 SDD WORKFLOW COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Title      : {title}
Work Type  : {WORK_TYPE}
Jira       : {ticket or N/A}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DELIVERED  : {N} acceptance criteria met
TESTED     : {N} scenarios passed
RISK       : {final risk level}
CONFIDENCE : {HIGH|MEDIUM|LOW}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Output Folder: output/{title-slug}/
  00-metadata.yaml          ✅
  01-requirement-impact.md  ✅
  02-story-refinement.md    ✅
  03-code-planning.md       ✅
  04-execution.md           ✅
  05-verification-testing.md ✅
  06-defects-round-*.md     {✅ or N/A}
  07-final-summary.md       ✅
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Constraints

- DO NOT re-run any analysis or testing — synthesis only
- Read all output files before generating the summary
- Be accurate — do not upgrade confidence beyond what the test results justify
- Known issues must be listed explicitly, not buried or omitted
