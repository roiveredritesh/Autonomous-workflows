---
skill: feature-feasibility-analyzer
version: 2.0.0
category: analysis
complexity: medium
estimated_time: 2-3 minutes
priority: high
last_updated: 2026-01-18
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

### Technical Feasibility
- **HIGH:** Standard WebForms patterns
- **MEDIUM:** Requires custom solution
- **LOW:** Incompatible with WebForms

### Legacy Compatibility
- **YES:** Works with ViewState/lifecycle
- **PARTIAL:** Workarounds needed
- **NO:** Violates WebForms constraints

### Risk Level
- **LOW:** Minimal changes, proven patterns
- **MEDIUM:** Moderate changes, some unknowns
- **HIGH:** Extensive changes, major unknowns

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

## Example 2: LOW Feasibility

**Input:**
```yaml
title: "Add real-time chat to customer portal"
description: "Live chat between customers and support"
requirements: ["Real-time messaging", "Presence indicators"]
```

**Output:**
```yaml
rating: LOW

technical_feasibility:
  compatible: no
  blockers:
    - "WebForms request/response model incompatible with real-time"
    - "SignalR difficult to integrate with WebForms lifecycle"
    - "ViewState conflicts with persistent connections"

legacy_impact:
  webforms_compatible: no
  viewstate_impact: high

risk_assessment:
  overall_risk: HIGH

alternatives:
  - "Use polling instead of real-time (workaround)"
  - "Separate SPA page for chat (partial modernization)"
  - "Third-party chat widget (external integration)"
  - "Defer until platform migration"

recommendation:
  action: spike
  reason: "WebForms incompatible - investigate alternatives"
confidence: HIGH
```

## Example 3: MEDIUM Feasibility

**Input:**
```yaml
title: "Add async data loading to improve performance"
description: "Make page load faster with async calls"
```

**Output:**
```yaml
rating: MEDIUM

technical_feasibility:
  compatible: with_workaround
  blockers:
    - "WebForms Page async patterns complex"
    - "ViewState handling with async tricky"
  enablers:
    - "Can use AJAX for partial updates"
    - "Telerik AJAX controls available"

legacy_impact:
  webforms_compatible: partial
  viewstate_impact: medium

risk_assessment:
  regression: MEDIUM
  overall_risk: MEDIUM

complexity:
  level: MEDIUM

alternatives:
  - "Use Telerik AJAX for partial updates (proven)"
  - "Full async Page (complex, risky)"
  - "Client-side loading with API (modern)"

recommendation:
  action: spike
  reason: "Multiple approaches - spike to validate best path"
confidence: MEDIUM
```

---

**Related Skills:**
- `webforms-lifecycle-analyzer` - Analyzes WebForms compatibility
- `telerik-impact-checker` - Checks Telerik limitations
- `spike-charter` - Creates investigation plan
