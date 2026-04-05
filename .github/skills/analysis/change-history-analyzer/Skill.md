---
name: change-history-analyzer
description: Analyzes git commit history and deployment logs to identify what changed and when, correlating changes with production issues.
---

# Change History Analyzer

## Quick Example

**Input:** Error first seen 14:23 UTC, git log for last 48 hours, affected file `ShippingCalculator.cs`
**Output:** Deployment at 14:19 UTC introduced commit `a3f92b1` — removed null guard in `ShippingCalculator.Calculate`, HIGH confidence this is the culprit
**Time:** 2-3 minutes

---

## Purpose
Analyzes git commit history and deployment logs to identify what changed and when, correlating changes with production issues.

## Input

```yaml
input:
  git_log: <git log output or path to repo — used to get commit history>
  issue_first_occurrence: <ISO timestamp when the error was first observed>
  affected_files: <optional list of files suspected to be related>
  deployment_timestamps: <optional list of deployment times to check against>
  lookback_hours: <how far back to search, default 72>
```

## Output

```yaml
output:
  change_timeline:
    - timestamp: <ISO>
      type: DEPLOYMENT|COMMIT|CONFIG_CHANGE
      identifier: <commit SHA or deployment ID>
      author: <name or system>
      description: <commit message or deployment notes>
      files_changed: [<list>]
      proximity_to_issue: <minutes before issue onset>
  likely_culprit:
    identifier: <commit SHA or deployment>
    timestamp: <ISO>
    author: <name>
    description: <commit message>
    reason: <why this is suspected>
    confidence: HIGH|MEDIUM|LOW
  correlated_files:
    - file: <path>
      changed_in: <commit SHA>
      change_type: MODIFIED|ADDED|DELETED|RENAMED
      change_summary: <what changed>
  recent_changes_summary:
    commits_in_window: <count>
    deployments_in_window: <count>
    files_touched: <count>
  confidence: HIGH|MEDIUM|LOW
```

## DO:
✅ Focus on changes within 2 hours before the issue first occurred
✅ Prioritize changes to files in the affected component's namespace
✅ Flag hotfix or rollback commits as especially relevant
✅ Note changes to shared utilities, base classes, or configuration files
✅ Record the exact commit SHA and author for accountability

## DON'T:
❌ Assume the most recent commit is always the culprit — check proximity to issue onset
❌ Ignore infrastructure/config changes — they can cause code-level symptoms
❌ Overlook dependency version bumps in NuGet packages or Web.config
❌ Skip merge commits — they may introduce conflicting changes
❌ Report the full git log — summarize and focus on the relevant window

## Error Conditions

**IF git repository is not accessible:**
```
1. Request manual git log export: `git log --oneline --stat --since="72 hours ago"`
2. Return error: GIT_ACCESS_FAILED — provide manual log for analysis
```

**IF no changes found in the lookback window:**
```
1. Extend lookback to 7 days
2. Check for infrastructure changes outside git (IIS config, SQL Server jobs)
3. Return: NO_RECENT_CHANGES — issue may be data-driven rather than code-driven
```

**IF affected files are not provided:**
```
1. Derive affected files from error stack trace (from production-log-analyzer output)
2. Search git log for any files matching component name from error
```

## Processing Steps

1. **Git Log Extraction:** Run or parse `git log --since=<lookback> --stat --format="%H|%ai|%an|%s"` to get structured commit data including changed files.

2. **Deployment Correlation:** Map deployment timestamps against commit history. Identify which commits were included in each deployment. Note the deployment immediately before the issue onset.

3. **Time Window Focus:** Calculate time delta between each change and `issue_first_occurrence`. Sort changes by proximity (ascending delta). Flag changes within 30 minutes as HIGH proximity.

4. **File Intersection:** If `affected_files` provided, filter commits to those touching matching files. Score each commit by: (1) proximity to issue, (2) whether it touches affected files, (3) whether it was a deployment trigger.

5. **Change Summary:** For each candidate commit, extract the diff summary — files modified, lines added/removed, nature of change (logic vs formatting vs config).

6. **Culprit Scoring:** Score candidates: proximity (40%), affected file overlap (40%), change nature (20%). Pick highest scorer as `likely_culprit`. Set confidence based on score spread.

## Example

**Input:**
```yaml
issue_first_occurrence: "2026-04-05T14:23:00Z"
affected_files: ["ShippingCalculator.cs", "CarrierRepository.cs"]
lookback_hours: 24
deployment_timestamps: ["2026-04-05T14:19:00Z", "2026-04-04T09:00:00Z"]
```

**Output:**
```yaml
change_timeline:
  - timestamp: "2026-04-05T14:19:00Z"
    type: DEPLOYMENT
    identifier: "deploy-2026-04-05-v2.14.1"
    author: "CI/CD Pipeline"
    description: "Release v2.14.1 — Shipping rate refactor"
    files_changed: ["ShippingCalculator.cs", "RateEngine.cs"]
    proximity_to_issue: 4
  - timestamp: "2026-04-05T13:45:00Z"
    type: COMMIT
    identifier: "a3f92b1"
    author: "Ahmed Khan"
    description: "Refactor: simplify carrier selection logic"
    files_changed: ["ShippingCalculator.cs"]
    proximity_to_issue: 38
likely_culprit:
  identifier: "a3f92b1"
  timestamp: "2026-04-05T13:45:00Z"
  author: "Ahmed Khan"
  description: "Refactor: simplify carrier selection logic"
  reason: "Touches ShippingCalculator.cs — the file in the error stack. Deployed 4 minutes before issue onset."
  confidence: HIGH
correlated_files:
  - file: "ShippingCalculator.cs"
    changed_in: "a3f92b1"
    change_type: MODIFIED
    change_summary: "Removed null guard on Carrier before property access"
recent_changes_summary:
  commits_in_window: 7
  deployments_in_window: 1
  files_touched: 12
confidence: HIGH
```

---

**Related Skills:**
- `production-log-analyzer` - Provides the error timestamp and component to correlate against
- `error-pattern-detector` - Identifies error onset time used as correlation anchor
- `minimal-fix-planner` - Uses change summary to understand what needs reverting or patching
- `hotfix-strategy-planner` - Determines whether rollback is safe based on change scope
