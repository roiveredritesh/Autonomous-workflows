---
name: pr-metadata-generator
description: Generates pull request metadata including title, description template, labels, reviewer suggestions, and test checklist for consistent and complete PR submissions.
---

# PR Metadata Generator

## Quick Example

**Input:** Bug fix for NullReferenceException in ShippingCalculator, ticket PROJ-4521, risk: LOW, 2 files changed
**Output:** PR title, description with context/change/test checklist, labels: [bugfix, critical, hotfix-candidate], suggested reviewers based on changed files
**Time:** 30-60 seconds

---

## Purpose
Generates pull request metadata including title, description template, labels, reviewer suggestions, and test checklist for consistent and complete PR submissions.

## Input

```yaml
input:
  change_type: FEATURE|BUGFIX|HOTFIX|REFACTOR|PERFORMANCE|DOCUMENTATION
  change_description: <what was changed and why>
  files_changed: <list of files modified>
  ticket_id: <Jira or issue tracker ID>
  risk_level: CRITICAL|HIGH|MEDIUM|LOW
  test_scenarios: <optional — list of test scenarios to include in checklist>
  breaking_change: true|false
  target_branch: <main|develop|release/x.y>
```

## Output

```yaml
output:
  pr_title: <formatted title following convention>
  pr_description: |
    ## Summary
    {change description}
    
    ## Ticket
    {ticket link}
    
    ## Changes
    {file list with descriptions}
    
    ## Test Checklist
    {checkbox list}
    
    ## Risk Assessment
    {risk level and mitigations}
    
    ## Rollback
    {rollback procedure}
  labels: [<list of GitHub/Azure DevOps labels>]
  suggested_reviewers:
    - name: <reviewer role or name>
      reason: <why this reviewer is relevant>
  merge_requirements:
    approvals_needed: <count>
    required_checks: [<CI jobs, code analysis>]
    merge_strategy: SQUASH|MERGE|REBASE
  confidence: HIGH|MEDIUM|LOW
```

## DO:
✅ Follow conventional commit format for PR title: `type(scope): description [TICKET-ID]`
✅ Include a test checklist with specific scenarios, not vague "tested manually"
✅ Set labels that enable filtering and reporting (bugfix, feature, risk-level)
✅ Suggest reviewers based on files changed (code owners or domain experts)
✅ Include rollback procedure — required for all production-bound changes

## DON'T:
❌ Write PR titles like "Fix bug" or "Update code" — be specific
❌ Leave test checklist empty — even for small changes, list what was verified
❌ Skip risk assessment — risk level drives approval requirements
❌ Forget breaking change label — it triggers additional review requirements
❌ Set target branch as main for features (should go to develop or feature branch)

## Error Conditions

**IF ticket ID is not provided:**
```
1. Use change description to generate title
2. Flag: NO_TICKET — add ticket ID before submitting PR
```

**IF files changed list is empty:**
```
1. Request list of changed files
2. Cannot generate reviewer suggestions without file list
3. Return: FILES_REQUIRED — provide changed file list for complete PR metadata
```

## Processing Steps

1. **Title Generation:** Format: `{type}({scope}): {description} [{TICKET-ID}]`. Scope = primary component (shipping, orders, customers). Keep under 72 characters. Examples: `fix(shipping): add null guard for carrier in ShippingCalculator [PROJ-4521]`.

2. **Description Template:** Generate sections: Summary (2-3 sentences), Ticket link, Changes (file by file with one-line description), Test Checklist (specific scenarios), Risk Assessment (level + what was done to mitigate), Rollback (git revert command or specific steps).

3. **Label Selection:** Map change_type → label: BUGFIX→bugfix, FEATURE→enhancement, HOTFIX→hotfix, PERFORMANCE→performance. Add risk labels: CRITICAL→risk-critical, HIGH→risk-high. Add breaking-change if applicable.

4. **Reviewer Suggestions:** Based on files changed: `.aspx` files → WebForms reviewer, `Repository.cs` → data layer reviewer, LINQ queries → performance reviewer. Always suggest: team lead for CRITICAL/HIGH risk.

5. **Merge Requirements:** CRITICAL/HOTFIX → 2 approvals, squash merge, all CI checks pass. HIGH → 2 approvals, merge. MEDIUM/LOW → 1 approval, squash merge.

6. **Test Checklist:** From test_scenarios input or derived from change: for each file changed, add 1-2 verification steps. Include regression: "Verify {related feature} still works".

## Example

**Input:**
```yaml
change_type: BUGFIX
change_description: "Added null guard for Carrier navigation property in ShippingCalculator.Calculate() to fix 100% order submission failures"
files_changed: ["ShippingCalculator.cs", "ShippingCalculatorTests.cs"]
ticket_id: "PROJ-4521"
risk_level: CRITICAL
test_scenarios: ["Order with carrier assigned submits successfully", "Order with no carrier uses default rate", "Bulk order submission does not regress"]
breaking_change: false
target_branch: main
```

**Output:**
```yaml
pr_title: "fix(shipping): add null guard for carrier in ShippingCalculator [PROJ-4521]"
pr_description: |
  ## Summary
  Fixes critical production issue where ShippingCalculator.Calculate() threw NullReferenceException for orders with no carrier assigned. Added null guard returning DefaultRate when carrier is null.
  
  ## Ticket
  [PROJ-4521](https://jira.example.com/browse/PROJ-4521) — CRITICAL: 100% order submission failures
  
  ## Changes
  - `ShippingCalculator.cs` — Added null guard before carrier property access (line 87, +2 lines)
  - `ShippingCalculatorTests.cs` — Added test: Calculate_ReturnsDefaultRate_WhenCarrierIsNull
  
  ## Test Checklist
  - [ ] Order with carrier assigned submits successfully
  - [ ] Order with no carrier uses DefaultRate ($0.00 handling)
  - [ ] Bulk order submission does not regress
  - [ ] Production error rate returns to 0% after deploy
  - [ ] Verified fix in staging with null carrier test order
  
  ## Risk Assessment
  **Level: CRITICAL** — Fixes active production outage  
  **Mitigation:** Minimal 2-line change, unit test added, staged rollout planned
  
  ## Rollback
  `git revert <commit-sha>` then redeploy. Estimated rollback time: 5 minutes.
labels: [bugfix, risk-critical, hotfix]
suggested_reviewers:
  - name: "Senior Developer (shipping domain)"
    reason: "ShippingCalculator.cs change — domain expertise required"
  - name: "Team Lead"
    reason: "CRITICAL risk level requires lead approval"
merge_requirements:
  approvals_needed: 2
  required_checks: ["CI/CD Build", "Unit Tests", "Code Analysis"]
  merge_strategy: SQUASH
confidence: HIGH
```

---

**Related Skills:**
- `change-log-generator` - Generates the changelog entry to reference in the PR description
- `decision-record-creator` - Creates ADRs linked from PR description when architectural decisions are made
- `rollback-plan-generator` - Generates the rollback section included in PR description
- `test-scenario-generator` - Generates test scenarios for the PR checklist
