---
name: change-log-generator
description: "Added Excel export button to Customer List page — exports filtered results to .xlsx"
---

# Change Log Generator

## Quick Example

**Input:** Feature: Excel export added to Customer List, ticket PROJ-1234, files: CustomerList.aspx, ExportHelper.cs
**Output:** Formatted CHANGELOG.md entry, version bump recommendation (minor), release notes snippet for customer communication
**Time:** 30-60 seconds

---

## Purpose
Generates structured change log entries for features, bug fixes, and improvements following Keep a Changelog format for traceability.

## Input

```yaml
input:
  change_type: FEATURE|FIX|IMPROVEMENT|SECURITY|DEPRECATED|REMOVED|BREAKING
  description: <plain English description of the change>
  affected_components: <list of pages, classes, or modules changed>
  ticket_id: <Jira or tracking system ID>
  version: <optional — current version, e.g. 2.14.0>
  audience: DEVELOPER|USER|BOTH
  breaking_change: true|false
```

## Output

```yaml
output:
  changelog_entry:
    section: Added|Fixed|Changed|Deprecated|Removed|Security|Breaking
    entry: <formatted line for CHANGELOG.md>
    full_entry: <multi-line entry with detail>
  version_bump_recommendation:
    current: <version if provided>
    recommended_next: <bumped version>
    bump_type: MAJOR|MINOR|PATCH
    reason: <why this bump level>
  release_notes_snippet:
    customer_facing: <user-friendly description>
    technical_detail: <developer-facing detail>
  pr_description_line: <one-liner for PR description>
  confidence: HIGH|MEDIUM|LOW
```

## DO:
✅ Write user-facing descriptions in plain English, not technical jargon
✅ Follow Keep a Changelog format: Added/Fixed/Changed/Deprecated/Removed/Security
✅ Include the ticket ID as a reference in the entry
✅ Recommend MAJOR bump for breaking changes, MINOR for features, PATCH for fixes
✅ Separate customer-facing release notes from technical developer notes

## DON'T:
❌ Include implementation details in customer-facing release notes
❌ Use abbreviations or class names in user-facing descriptions
❌ Lump multiple unrelated changes into one entry
❌ Skip the ticket reference — it's essential for traceability
❌ Write vague entries like "Fixed bug" — be specific about what was fixed

## Error Conditions

**IF change type is ambiguous:**
```
1. Default to IMPROVEMENT for refactoring or performance changes
2. Default to FIX for defect corrections
3. Flag: TYPE_INFERRED — verify change_type is correct
```

**IF version is not provided:**
```
1. Omit version from output
2. Note: VERSION_UNKNOWN — provide current version for bump recommendation
```

## Processing Steps

1. **Section Mapping:** Map change_type to Keep a Changelog section: FEATURE→Added, FIX→Fixed, IMPROVEMENT→Changed, SECURITY→Security, DEPRECATED→Deprecated, REMOVED→Removed, BREAKING→Breaking.

2. **Entry Formatting:** Short entry: `- [PROJ-1234] {description}`. Full entry adds: component list and technical detail on following lines.

3. **Version Bump Logic:** FEATURE → minor bump (2.14.0 → 2.15.0). FIX → patch bump (2.14.0 → 2.14.1). BREAKING → major bump (2.14.0 → 3.0.0). IMPROVEMENT → patch or minor depending on scope.

4. **Release Notes:** Customer-facing: avoid class names, use feature/function language. Technical: include affected components and migration notes if needed.

5. **PR Line:** Single line suitable for PR description section: `type: description [TICKET-ID]`.

## Example

**Input:**
```yaml
change_type: FEATURE
description: "Added Excel export button to Customer List page — exports filtered results to .xlsx"
affected_components: ["CustomerList.aspx", "CustomerList.aspx.cs", "ExportHelper.cs"]
ticket_id: "PROJ-1234"
version: "2.14.0"
audience: BOTH
breaking_change: false
```

**Output:**
```yaml
changelog_entry:
  section: Added
  entry: "- [PROJ-1234] Added Excel export to Customer List — exports filtered results to .xlsx (max 10,000 rows)"
  full_entry: |
    ### Added
    - [PROJ-1234] Added Excel export to Customer List
      - Exports currently filtered customer results to .xlsx format
      - Maximum 10,000 rows per export
      - Components: CustomerList.aspx, ExportHelper.cs
version_bump_recommendation:
  current: "2.14.0"
  recommended_next: "2.15.0"
  bump_type: MINOR
  reason: "New feature added — minor version bump per semantic versioning"
release_notes_snippet:
  customer_facing: "You can now export your filtered customer list to Excel directly from the Customer List page using the new Export button."
  technical_detail: "Excel export implemented via EPPlus. Respects current RadGrid filters. ExportHelper.cs generates XLSX via streaming for memory efficiency. Max 10K rows enforced."
pr_description_line: "feat: Add Excel export to Customer List [PROJ-1234]"
confidence: HIGH
```

---

**Related Skills:**
- `decision-record-creator` - Creates ADR for significant decisions made during feature delivery
- `pr-metadata-generator` - Generates full PR title, description, and checklist
- `bug-fix-documenter` - Generates bug fix documentation that includes a changelog entry
- `rollback-plan-generator` - Creates rollback plan referenced in the release notes
