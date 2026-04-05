# Output Structure for Agent Execution

## Purpose
Save complete outputs from each workflow stage to enable:
- Progress tracking
- Review of analysis and decisions
- Audit trail
- Resuming interrupted work
- Learning from past executions

## Folder Structure

```
output/
└── {workflow-title-slug}/
    ├── 00-metadata.yaml
    ├── 01-refining.md
    ├── 02-analysis.md
    ├── 03-planning.md
    ├── 04-execution.md
    └── 05-review-summary.md
```

### Title Slug Format
Convert workflow title to filesystem-safe slug:
- "Add Excel export to CustomerList" → `add-excel-export-to-customerlist-2026-03-28-143022`
- Include timestamp to avoid conflicts
- Lowercase, hyphens only, no special characters

## Stage Files

### 00-metadata.yaml
```yaml
workflow_id: add-excel-export-to-customerlist-2026-03-28-143022
title: Add Excel export to CustomerList
agent: feature-delivery
mode: FEATURE
started_at: 2026-03-28T14:30:22Z
completed_at: 2026-03-28T14:32:15Z
risk_level: LOW
confidence: HIGH
status: completed
```

### 01-refining.md
**When:** Story Refinement Agent active
**Contains:**
- Original user request (verbatim)
- Identified gaps and ambiguities
- Clarifying questions asked
- Clarifications received
- Refined requirements

### 02-analysis.md
**When:** Analysis stages (1-5 for features, 1-3 for bugs, etc.)
**Contains:**
- Requirement validation
- Feasibility assessment
- WebForms/Telerik compatibility
- LINQ/SQL impact
- Cache strategy analysis
- Risk assessment
- Affected components

### 03-planning.md
**When:** Planning stages (6-9 for features, 4-8 for bugs, etc.)
**Contains:**
- Implementation approach (minimal diff plan)
- Files to modify with specific changes
- Test scenarios
- Rollback procedures
- Deployment considerations

### 04-execution.md
**When:** Implementation phase
**Contains:**
- Code changes made
- Files modified
- Commands executed
- Build/test results
- Issues encountered and resolutions

### 05-review-summary.md
**When:** Workflow completion
**Contains:**
- Executive summary
- What was delivered
- Risk assessment (final)
- Confidence level (final)
- Testing performed
- Next steps
- Lessons learned

## Agent Integration

### Saving Outputs
Each agent should save output after completing each major phase:

```yaml
# In agent execution:
1. Create output folder: output/{title-slug}/
2. Save metadata: 00-metadata.yaml
3. After refining (if needed): Save 01-refining.md
4. After analysis stages: Save 02-analysis.md
5. After planning stages: Save 03-planning.md
6. After execution: Save 04-execution.md
7. At completion: Save 05-review-summary.md
```

### File Naming
Stage files are numbered to maintain order:
- `01-` through `05-` prefix ensures correct sorting
- Descriptive name indicates content
- `.md` format for readability
- `.yaml` for metadata (machine-readable)

## Example: Feature Delivery Workflow

**User Request:** "Add Excel export to customer list"

**Creates:**
```
output/add-excel-export-to-customerlist-2026-03-28-143022/
├── 00-metadata.yaml
├── 02-analysis.md         (Stages 1-5: intake, requirements, feasibility, legacy, data)
├── 03-planning.md         (Stages 6-9: implementation, testing, docs, rollback)
└── 05-review-summary.md   (Final summary)
```

**Note:** No `01-refining.md` because requirements were clear.
**Note:** No `04-execution.md` because Copilot doesn't auto-execute code.

## Example: Bug Fix Workflow

**User Request:** "Customer search returns wrong results"

**Creates:**
```
output/fix-customer-search-wrong-results-2026-03-28-150000/
├── 00-metadata.yaml
├── 02-analysis.md         (Triage, root cause, impact)
├── 03-planning.md         (Minimal fix, safety, regression, rollback)
├── 04-execution.md        (Code changes, testing)
└── 05-review-summary.md   (Summary and verification)
```

## Example: Spike Investigation

**User Request:** "Can we cache product catalog in Redis?"

**Creates:**
```
output/spike-cache-product-catalog-redis-2026-03-28-160000/
├── 00-metadata.yaml
├── 02-analysis.md         (Research plan, investigation steps)
└── 05-review-summary.md   (Findings, recommendations, confidence)
```

---

## SDD Workflow Output Structure

Used by the Spec-Driven Development agents (`sdd-master` + `sdd/phase-*.agent.md`).

### Folder Structure

```
output/
└── {work-type}-{title-slug}-{YYYYMMDD}/
    ├── 00-metadata.yaml
    ├── 01-requirement-impact.md
    ├── 02-story-refinement.md
    ├── 03-code-planning.md
    ├── 04-execution.md
    ├── 05-verification-testing.md
    ├── 06-defects-round-1.md       ← only if defects found
    ├── 06-defects-round-2.md       ← only if multiple rounds needed
    ├── 06-defects-round-3.md       ← max 3 rounds
    └── 07-final-summary.md
```

### SDD File Descriptions

| File | Phase Agent | Step | Contains |
|------|-------------|------|----------|
| `00-metadata.yaml` | `sdd-master` | 0 | work_type, title, app_url, jira_ticket, started_at, status |
| `01-requirement-impact.md` | `sdd/phase-1-analysis` | 1 | Skill outputs: story-analyzer, requirement-extractor, feasibility/bug-classifier, sql/webforms/telerik impact, risk assessment, Q&A with user |
| `02-story-refinement.md` | `sdd/phase-1-analysis` | 2 | Given/When/Then acceptance criteria, edge cases, scope boundary (IN/OUT), definition of done |
| `03-code-planning.md` | `sdd/phase-2-planning` | 3 | File-by-file change plan, line estimates, safe change boundaries, rollback procedure |
| `04-execution.md` | `sdd/phase-3-execution` | 4 | Files modified, lines added/removed, deviations from plan |
| `05-verification-testing.md` | `sdd/phase-4-testing` | 5 | Test scenario results (PASS/FAIL per AC), regression results, screenshots of failures |
| `06-defects-round-N.md` | `sdd/phase-4-testing` | 6 | Defects classified, minimal fix applied, safe boundary check — one file per loop round |
| `07-final-summary.md` | `sdd/phase-5-summary` | 7 | Executive summary, delivered ACs, final risk/confidence, next steps, lessons learned |

### SDD Metadata Schema

```yaml
workflow_id: feature-add-print-button-20260404
title: Add print button to DailyReportList
work_type: FEATURE              # FEATURE | BUG | PERFORMANCE | HOTFIX
jira_ticket: PROJ-1234          # or null
app_url: https://localhost:44300
agent: sdd-master
phases:
  - phase-1-analysis
  - phase-2-planning
  - phase-3-execution
  - phase-4-testing
  - phase-5-summary
started_at: 2026-04-04T10:00:00Z
completed_at: 2026-04-04T11:30:00Z
current_phase: done
status: completed               # in-progress | completed | escalated | aborted
risk_level: LOW                 # LOW | MEDIUM | HIGH | CRITICAL
confidence: HIGH                # HIGH | MEDIUM | LOW
```

### SDD Example: Feature Delivery

**User:** `"Add print button to DailyReportList"`

```
output/feature-add-print-button-20260404/
├── 00-metadata.yaml             (work_type: FEATURE, app_url saved)
├── 01-requirement-impact.md     (feasibility HIGH, 2 files affected, risk LOW)
├── 02-story-refinement.md       (7 ACs in Given/When/Then, 4 edge cases)
├── 03-code-planning.md          (DailyReportList.aspx + .aspx.cs, ~35 lines, rollback: git revert)
├── 04-execution.md              (+28/-0 lines, no deviations)
├── 05-verification-testing.md   (7/7 PASS, 2 regression scenarios PASS)
└── 07-final-summary.md          (risk: LOW, confidence: HIGH, 0 defect rounds)
```

### SDD Example: Bug Fix With Defect Loop

**User:** `"Search filter returns wrong results"`

```
output/bug-search-filter-wrong-results-20260404/
├── 00-metadata.yaml
├── 01-requirement-impact.md     (bug-classifier: HIGH severity, LINQ filter-in-memory)
├── 02-story-refinement.md       (4 ACs, 3 edge cases)
├── 03-code-planning.md          (1 file, 2 lines changed)
├── 04-execution.md              (+2/-2 lines)
├── 05-verification-testing.md   (3/4 PASS, AC-03 FAIL — round 1)
├── 06-defects-round-1.md        (AC-03 fix: null check added)
├── 05-verification-testing.md   (4/4 PASS — round 2 retest)
└── 07-final-summary.md          (risk: LOW, confidence: MEDIUM, 1 defect round)
```

---

## Benefits

1. **Audit Trail:** Full record of decisions and reasoning
2. **Resumability:** Can review and continue interrupted work
3. **Learning:** Review past workflows to improve
4. **Collaboration:** Share analysis with team members
5. **Documentation:** Auto-generated project documentation
6. **Debugging:** Understand why decisions were made

## Implementation Notes

- Create output folder if it doesn't exist
- Use UTF-8 encoding for all files
- Include timestamps in metadata
- Keep markdown files readable (not machine-generated bloat)
- Save incrementally (after each stage completes)
- Don't save sensitive data (credentials, PII)

## .gitignore Recommendation

```gitignore
# Output folders contain execution logs - don't commit
/output/

# Optional: Keep only review summaries
/output/*/*.md
!/output/*/05-review-summary.md
```

This allows sharing final summaries while keeping detailed execution logs local.

---

**Related:** See `agents/` for agent implementation details
