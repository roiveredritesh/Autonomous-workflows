---
name: hotfix-branch-creator
description: Plans hotfix branch strategy including branch name, base commit, merge strategy, and deployment path for safe emergency production fixes.
---

# Hotfix Branch Creator

## Quick Example

**Input:** Hotfix for v2.14.1 NullReferenceException, base branch: main, fix description: null guard in ShippingCalculator
**Output:** Branch name `hotfix/PROJ-4521-shipping-null-guard`, base commit SHA, merge plan (hotfix→main→develop), deployment sequence
**Time:** 1-2 minutes

---

## Purpose
Plans hotfix branch strategy including branch name, base commit, merge strategy, and deployment path for safe emergency production fixes.

## Input

```yaml
input:
  affected_version: <version in production with the issue, e.g. "2.14.1">
  base_branch: <branch to create hotfix from, usually "main" or "release/x.y">
  hotfix_description: <short description of what the fix does>
  ticket_id: <incident or bug ticket ID>
  current_branches:
    main: <current SHA on main>
    develop: <current SHA on develop>
    release: <optional — release branch SHA>
  target_environments: [<staging|pre-prod|production>]
```

## Output

```yaml
output:
  branch_strategy:
    hotfix_branch_name: <hotfix/{ticket}-{slug}>
    base_branch: <which branch to cut from>
    base_commit_sha: <SHA to cut from>
    rationale: <why this base>
  merge_plan:
    step_1: <first merge: hotfix → where>
    step_2: <second merge: where → where>
    step_3: <optional third merge>
    merge_strategy: SQUASH|MERGE_COMMIT
    commit_message_template: <suggested commit message>
  deployment_sequence:
    - environment: <env name>
      from_branch: <which branch>
      pre_deploy_check: <what to verify before deploy>
      rollback_branch: <which branch to roll back to>
  tagging_plan:
    tag_name: <v2.14.2>
    tag_message: <message>
    when_to_tag: <before or after production deploy>
  commands:
    create_branch: <exact git commands>
    merge_commands: [<exact git commands>]
    tag_command: <exact git command>
  confidence: HIGH|MEDIUM|LOW
```

## DO:
✅ Cut hotfix branch from the exact commit that is in production (not latest main if they differ)
✅ Plan merges back to BOTH main and develop to prevent regression
✅ Generate exact git commands — no room for interpretation under pressure
✅ Tag the production commit before and after the hotfix for rollback reference
✅ Name branch consistently: `hotfix/{ticket-id}-{slug}` for traceability

## DON'T:
❌ Cut hotfix from develop — it may contain unreleased code
❌ Forget to merge hotfix back to develop — it causes regression in next release
❌ Use feature branch naming conventions for hotfixes — hotfix/ prefix is required
❌ Skip tagging — rollback requires knowing exact commit to revert to
❌ Squash merge to develop — preserve hotfix commit history for audit trail

## Error Conditions

**IF main and production are out of sync:**
```
1. Identify the exact commit that was deployed to production
2. Cut hotfix from that commit, not from main HEAD
3. Flag: VERSION_MISMATCH — production may be behind main; confirm deployment commit
```

**IF develop has conflicts with hotfix:**
```
1. Flag: MERGE_CONFLICT_RISK — hotfix may conflict with work in progress on develop
2. Plan for manual conflict resolution step
3. Assign conflict resolution to most familiar developer
```

## Processing Steps

1. **Base Commit Identification:** If production is on a tagged release (v2.14.1), use that tag's commit. If production is latest main, use current main SHA. Verify: git log -1 --format="%H" on the base branch.

2. **Branch Name Generation:** Format: `hotfix/{ticket-id}-{descriptive-slug}`. Slug: lowercase, hyphens, max 30 chars. Example: `hotfix/PROJ-4521-shipping-null-guard`.

3. **Merge Plan Design:** Standard hotfix flow: (1) hotfix → main (or release branch), (2) main → develop (to include fix in next release). If release branch exists: hotfix → release → main AND release → develop.

4. **Deployment Sequence:** Per environment: staging first (from hotfix branch), validate, then pre-prod (from hotfix or main), validate, then production (from tagged main). Include rollback reference for each.

5. **Tagging Plan:** Before production deploy: tag current production commit as `v{version}` (if not already tagged) for rollback reference. After successful production deploy: tag as `v{version+patch}`.

6. **Command Generation:** Generate exact, copy-paste git commands: `git checkout -b hotfix/PROJ-4521-shipping-null-guard main`, `git checkout main && git merge --no-ff hotfix/PROJ-4521-shipping-null-guard`, etc.

## Example

**Input:**
```yaml
affected_version: "2.14.1"
base_branch: main
hotfix_description: "Add null guard for Carrier in ShippingCalculator.Calculate"
ticket_id: "PROJ-4521"
current_branches:
  main: "a3f92b1"
  develop: "d8e41c2"
target_environments: [staging, production]
```

**Output:**
```yaml
branch_strategy:
  hotfix_branch_name: "hotfix/PROJ-4521-shipping-null-guard"
  base_branch: main
  base_commit_sha: "a3f92b1"
  rationale: "main is at the same commit as v2.14.1 production deployment"
merge_plan:
  step_1: "hotfix/PROJ-4521-shipping-null-guard → main (after staging validation)"
  step_2: "main → develop (to include fix in next release, prevent regression)"
  merge_strategy: MERGE_COMMIT
  commit_message_template: "hotfix: add null guard for Carrier in ShippingCalculator [PROJ-4521]\n\nFixes CRITICAL: NullReferenceException causing 100% order submission failures.\nCarrier can be null for draft orders — return DefaultRate when null.\n\nCo-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
deployment_sequence:
  - environment: staging
    from_branch: "hotfix/PROJ-4521-shipping-null-guard"
    pre_deploy_check: "Run smoke tests S1-S3 from hotfix-test-generator output"
    rollback_branch: "main@a3f92b1"
  - environment: production
    from_branch: main
    pre_deploy_check: "Staging smoke tests all PASS, no new errors in staging logs"
    rollback_branch: "tag v2.14.1"
tagging_plan:
  tag_name: "v2.14.2"
  tag_message: "Hotfix: null guard for Carrier in ShippingCalculator [PROJ-4521]"
  when_to_tag: "After successful production deployment"
commands:
  create_branch: |
    git checkout main
    git pull origin main
    git checkout -b hotfix/PROJ-4521-shipping-null-guard
    # make changes, commit
    git push origin hotfix/PROJ-4521-shipping-null-guard
  merge_commands:
    - "git checkout main && git merge --no-ff hotfix/PROJ-4521-shipping-null-guard -m 'hotfix: null guard for Carrier [PROJ-4521]'"
    - "git push origin main"
    - "git checkout develop && git merge --no-ff main -m 'merge hotfix v2.14.2 to develop'"
    - "git push origin develop"
  tag_command: "git tag -a v2.14.2 -m 'Hotfix: null guard for Carrier [PROJ-4521]' && git push origin v2.14.2"
confidence: HIGH
```

---

**Related Skills:**
- `hotfix-deployment-planner` - Plans the deployment sequence in detail using this branch strategy
- `hotfix-strategy-planner` - Determines whether code hotfix or rollback is the right approach
- `minimal-fix-implementer` - Generates the actual code change for the hotfix branch
- `hotfix-validator` - Validates the branch and change before deployment
