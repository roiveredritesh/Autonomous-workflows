---
name: feature-feasibility-analyzer
description: Evaluates technical and business feasibility of proposed features in legacy ASP.NET WebForms environment.
---

# Feature Feasibility Analyzer

## Quick Example

**Input:** "Add real-time chat to customer portal"
**Output:** LOW feasibility - WebForms incompatible, HIGH risk → Recommend spike
**Time:** 2 minutes

---

## Purpose
Evaluates technical and business feasibility of proposed features in legacy ASP.NET WebForms environment.

## Input

```yaml
feature:
  title: <feature name>
  description: <what user wants>
  requirements: [<functional requirements>]
  constraints: [<limitations>]
  timeline: <if specified>
```

## Output

```yaml
feasibility_assessment:
  rating: HIGH|MEDIUM|LOW

  technical_feasibility:
    compatible: yes|no|with_workaround
    blockers: [<technical issues>]
    enablers: [<what helps>]

  legacy_impact:
    webforms_compatible: yes|no|partial
    telerik_compatible: yes|no|partial
    viewstate_impact: none|low|medium|high

  risk_assessment:
    data_integrity: LOW|MEDIUM|HIGH
    performance: LOW|MEDIUM|HIGH
    regression: LOW|MEDIUM|HIGH
    overall_risk: LOW|MEDIUM|HIGH

  complexity:
    level: LOW|MEDIUM|HIGH
    estimated_files: <count>
    estimated_lines: <count>

  alternatives: [<other approaches>]

  recommendation:
    action: proceed|spike|alternative|defer
    reason: <explanation>

  confidence: HIGH|MEDIUM|LOW
```

## Feasibility Ratings

### HIGH - Proceed
- Compatible with WebForms
- Low risk
- Proven patterns exist
- Clear implementation path

### MEDIUM - Proceed with Caution
- Compatible with workarounds
- Moderate risk
- Some unknowns
- May need spike first

### LOW - Spike or Alternative
- WebForms incompatible
- High risk
- Major unknowns
- Needs investigation

## DO:
✅ Assess WebForms compatibility
✅ Check Telerik limitations
✅ Evaluate ViewState impact
✅ Identify risks early
✅ Suggest alternatives
✅ Recommend spike if uncertain

## DON'T:
❌ Ignore WebForms constraints
❌ Skip legacy impact analysis
❌ Underestimate complexity
❌ Proceed with LOW feasibility
❌ Overlook performance risks
❌ Skip alternative approaches

## Error Conditions

**IF WebForms incompatible:**
```
1. Flag as LOW feasibility
2. Explain incompatibility
3. Suggest alternatives:
   - Workaround approach
   - Alternative technology
   - Phased migration
4. Recommend spike investigation
```

**IF high risk detected:**
```
1. Flag specific risks
2. Recommend mitigation:
   - Spike investigation
   - Proof of concept
   - Phased approach
3. Document risk factors
```

## Assessment Criteria

- **HIGH:** Standard WebForms patterns, low risk, proven approach
- **MEDIUM:** Workarounds needed, moderate risk, some unknowns
- **LOW:** WebForms incompatible, high risk, major unknowns

## Example 1: HIGH Feasibility

**Input:**
```yaml
title: "Add Excel export to customer list"
description: "Users need to export customer data"
requirements: ["Export filtered results", "XLSX format"]
```

**Output:**
```yaml
rating: HIGH

technical_feasibility:
  compatible: yes
  enablers:
    - "EPPlus library already in use"
    - "Standard PostBack pattern"
    - "Existing export examples"

legacy_impact:
  webforms_compatible: yes
  telerik_compatible: yes
  viewstate_impact: none

risk_assessment:
  data_integrity: LOW
  performance: LOW
  regression: LOW
  overall_risk: LOW

complexity:
  level: LOW
  estimated_files: 2
  estimated_lines: 40

recommendation:
  action: proceed
  reason: "Standard pattern, low risk, proven approach"
confidence: HIGH
```

---

**Related Skills:**
- `webforms-lifecycle-analyzer` - Analyzes WebForms compatibility
- `telerik-impact-checker` - Checks Telerik limitations
- `spike-charter` - Creates investigation plan
