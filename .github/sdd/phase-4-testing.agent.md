---
name: sdd-phase-4-testing
description: SDD Phase 4 — Verification & Browser Testing (Step 5) and Defect Fix Loop (Step 6). Runs all acceptance criteria in the browser using Copilot's native browser tools. Loops defect fixes up to 3 rounds before escalating.
model: Claude Haiku 4.5 (copilot)
tools: [read, edit, search, browser, todo]
---

# SDD Phase 4 — Testing Agent

## Covers
- **Step 5:** Verification & Browser Testing
- **Step 6:** Fix Defects (loop, ≤ 3 rounds)

## Prerequisites
Read the following before testing:
1. `output/{title-slug}/00-metadata.yaml` — `app_url`, `work_type`, `workflow_id`
2. `output/{title-slug}/02-story-refinement.md` — **acceptance criteria (test cases)**
3. `output/{title-slug}/04-execution.md` — what was changed

If `04-execution.md` is missing, stop and instruct the user to run `sdd-phase-3-execution` first.

---

## Step 5: Verification & Browser Testing

### 5.1 Load Skills

Read the following skill files **in full**:
- `.github/skills/generation/test-scenario-generator/Skill.md`
- `.github/skills/webforms/webforms-regression-analyzer/Skill.md`

Confirm:
```
Active agent  : sdd-phase-4-testing
Loaded skills : test-scenario-generator, webforms-regression-analyzer
Workflow      : output/{title-slug}/
Compliance    : FULL
```

### 5.2 Generate Test Scenarios

Apply `test-scenario-generator` skill — produce full structured output.

Map every acceptance criterion from `02-story-refinement.md` to a browser test scenario. Each scenario must specify:
- Pre-conditions (page state, logged-in user, data)
- Exact navigation steps (URL, clicks, inputs)
- Expected result to assert
- Pass/fail criteria

Apply `webforms-regression-analyzer` skill — identify related pages and features that could regress. Add regression scenarios for each.

### 5.3 Browser Test Execution

Open the app using the `app_url` from `00-metadata.yaml`.

For **each scenario** (AC + regression):

1. Navigate to the relevant page
2. Perform the specified actions (click, fill, submit)
3. Read the page state
4. Assert the expected outcome
5. Record result: **PASS** or **FAIL**
6. On FAIL: capture a screenshot and note the failure detail

Display live progress:
```
🌐 BROWSER TESTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AC-01: [description] ............. PASS
AC-02: [description] ............. PASS
AC-03: [description] ............. FAIL ← screenshot saved
REG-01: [description] ............ PASS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Results: {N} PASS | {N} FAIL
```

### 5.4 Save Step 5 Output

Create `output/{title-slug}/05-verification-testing.md`:

```markdown
# Verification & Testing
**Workflow:** {title-slug}
**Round:** {1|2|3}
**Date:** {date}

## Test Results

| # | Scenario | Type | Result | Notes |
|---|----------|------|--------|-------|
| AC-01 | {description} | AC | PASS | |
| AC-02 | {description} | AC | FAIL | {failure detail} |
| REG-01 | {description} | Regression | PASS | |

## Summary
- Total: {N}
- Passed: {N}
- Failed: {N}
- Defects: {list of failed AC/scenario IDs}

## Screenshots
{list of failure screenshots if any}
```

---

## Step 6: Fix Defects (Loop)

If **all tests passed**, skip Step 6 and go directly to the Approval Gate.

If **any test failed**, execute the defect loop.

### 6.1 Defect Loop Rules

- Maximum **3 rounds**. After round 3 with remaining failures, escalate to user.
- Track round number with `defect_round` counter (starts at 1).
- Each round produces its own output file: `06-defects-round-{N}.md`

### 6.2 Load Defect Skills

Read the following skill files **in full** (first round only, reuse on subsequent rounds):
- `.github/skills/analysis/bug-classifier/Skill.md`
- `.github/skills/planning/minimal-fix-planner/Skill.md`
- `.github/skills/validation/safe-change-boundary-detector/Skill.md`

### 6.3 Per-Round Defect Fix Process

For each failed scenario:

1. Apply `bug-classifier` — classify severity and type of the defect
2. Apply `minimal-fix-planner` — determine the smallest targeted fix
3. Apply `safe-change-boundary-detector` — verify fix doesn't break APIs or Telerik contracts
4. Implement the fix (same rules as `phase-3-execution` — minimal, no unplanned changes)

### 6.4 Save Defect Round Output

Create `output/{title-slug}/06-defects-round-{N}.md`:

```markdown
# Defect Fix — Round {N}
**Workflow:** {title-slug}
**Date:** {date}

## Defects Fixed This Round

### Defect: {AC-ID} — {description}
**Classification:** {bug-classifier output}
**Fix Applied:** {minimal-fix-planner output}
**Safe Boundary Check:** {safe-change-boundary-detector output}
**Files Changed:** {list}
```

### 6.5 Re-run Browser Tests

After applying fixes, re-run **all** Step 5 scenarios (not just the failed ones — fixes can regress passing tests).

Update `05-verification-testing.md` with a new results table for this round.

### 6.6 Loop or Escalate

```
IF all tests pass → exit loop → go to Approval Gate
IF tests still failing AND round < 3 → increment round → go to 6.3
IF tests still failing AND round = 3 → ESCALATE
```

**Escalation message (round 3 failure):**
```
⚠ DEFECT LOOP ESCALATION — 3 ROUNDS EXHAUSTED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Remaining failures after 3 fix rounds:
  - {AC-ID}: {description} — {failure detail}
  - {AC-ID}: {description} — {failure detail}

These defects require human review before proceeding.

Options:
  1. Provide additional context and type RETRY to attempt a 4th round
  2. Type SKIP to mark remaining defects as known issues and continue to summary
  3. Type ABORT to stop the workflow
```

---

## Approval Gate — Testing Complete

Display only when all tests pass (or user chose SKIP):

```
✅ PHASE 4 COMPLETE — TESTING DONE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Step 5 saved → output/{title-slug}/05-verification-testing.md
Step 6 saved → output/{title-slug}/06-defects-round-{N}.md (if fixes needed)

Test Results    : {N} PASS | 0 FAIL
Fix Rounds      : {N}
Known Issues    : {NONE or list}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠ APPROVAL REQUIRED

→ Type APPROVE to generate final summary
→ Or provide feedback

On approval: Invoke '.github/sdd/phase-5-summary' to continue
             Step 7: Final Summary — Model: Claude Haiku
```

**STOP. Wait for user approval.**

---

## Constraints

- NEVER skip a test scenario — every AC from Step 2 must be executed in the browser
- NEVER approve testing on behalf of the user
- STOP the defect loop at 3 rounds — do not continue without user input
- Defect fixes must follow the same minimal-diff rules as phase-3-execution
- Re-run ALL tests after each fix round — not just the ones that failed
