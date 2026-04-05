---
name: webforms-lifecycle-validator
description: Validates that code changes respect ASP.NET WebForms page lifecycle order and constraints, preventing runtime errors and unexpected behavior.
---

# WebForms Lifecycle Validator

## Quick Example

**Input:** Code reads `Request.Form["ddlStatus"]` in `Page_Init`, change: binds RadDropDownList in Page_Load
**Output:** VIOLATION — reading form values in Page_Init is before ViewState restore; control value not yet available. Move to Page_Load or Page_LoadComplete.
**Time:** 2-3 minutes

---

## Purpose
Validates that code changes respect ASP.NET WebForms page lifecycle order and constraints, preventing runtime errors and unexpected behavior.

## Input

```yaml
input:
  code_change: <code being added or modified>
  lifecycle_phase_of_change: <PreInit|Init|InitComplete|PreLoad|Load|Control Events|LoadComplete|PreRender|PreRenderComplete|SaveState|Render>
  viewstate_dependencies: <optional — list of controls or data that depend on ViewState>
  is_postback_specific: <true|false — does the change only execute on postback>
  page_name: <optional — .aspx page name for context>
```

## Output

```yaml
output:
  lifecycle_violations:
    - violation_id: <V1..Vn>
      severity: CRITICAL|HIGH|MEDIUM|LOW
      phase: <where violation occurs>
      description: <what is wrong>
      rule_violated: <specific WebForms lifecycle rule>
      fix: <what to change>
  viewstate_issues:
    - issue: <description>
      control: <control name>
      impact: <data lost or state incorrect>
      fix: <correction>
  postback_issues:
    - issue: <description>
      fix: <correction>
  lifecycle_summary:
    phase_order_correct: true|false
    viewstate_safe: true|false
    postback_handling_correct: true|false
    overall_valid: true|false
  recommendations:
    - recommendation: <description>
      priority: critical|high|medium
  confidence: HIGH|MEDIUM|LOW
```

## DO:
✅ Verify lifecycle phase order: PreInit < Init < Load < Events < PreRender < Render
✅ Check that control data binding happens in Page_Load, not Page_Init
✅ Verify ViewState-dependent reads happen after LoadViewState (in Page_Load or later)
✅ Ensure postback-specific code is wrapped in `if (IsPostBack)` where appropriate
✅ Validate that Telerik controls are initialized before their events are wired

## DON'T:
❌ Read form values or control values in Page_Init — ViewState not yet loaded
❌ Set control values in Page_PreRender that should persist — too late for ViewState
❌ Modify DataSource in a control event without re-binding
❌ Wire event handlers in Page_Load when they should be in Page_Init
❌ Access Master Page controls before Page_Init completes

## Error Conditions

**IF lifecycle phase is ambiguous:**
```
1. Ask: is this code in a method called from Page_Load? Or from an event handler?
2. Trace call chain to determine effective lifecycle phase
3. Flag: PHASE_AMBIGUOUS — provide the calling method for accurate validation
```

**IF code uses async patterns (async void event handlers):**
```
1. Flag: ASYNC_WEBFORMS — async/await in WebForms lifecycle has specific constraints
2. Verify ScriptManager is configured for async postback if using UpdatePanel
3. Return: ASYNC_VALIDATION_REQUIRED — WebForms async patterns need specific review
```

## Processing Steps

1. **Phase Identification:** Determine in which lifecycle phase the code executes. Trace: is it in Page_Load? An event handler? Page_PreRender? If in a helper method, determine the calling context.

2. **Lifecycle Rule Check:** Apply rules: (1) Reading Request.Form — valid in Page_Load+ (after ViewState loaded). (2) Setting control values — valid in Page_Load; in events re-bind if needed. (3) Calling DataBind — valid in Page_Load or control events. (4) Accessing Session/Cache — valid in all phases.

3. **ViewState Dependency Check:** For each control or property accessed: does it depend on ViewState being loaded? ViewState loads between Init and Load. Flag if accessed in PreInit or Init.

4. **Postback Flow Check:** Identify: does the code behave differently on first load vs postback? Verify `if (!IsPostBack)` guards where needed. Check that event handlers only fire on postback (correct).

5. **Telerik-Specific Checks:** RadGrid rebind: must happen in Page_Load or SelectedIndexChanged event, not in Page_PreRender. RadComboBox DataSource: set in Page_Load on first load only. NeedDataSource event: must call `e.IsFromCache` check.

6. **Fix Generation:** For each violation: state the correct phase, provide example code with correct placement, explain why the original phase is wrong.

## Example

**Input:**
```yaml
code_change: |
  protected void Page_Init(object sender, EventArgs e)
  {
      var selectedStatus = ddlStatus.SelectedValue; // reading control value
      if (selectedStatus == "Active") {
          LoadActiveCustomers();
      }
  }
lifecycle_phase_of_change: Init
viewstate_dependencies: ["ddlStatus"]
is_postback_specific: true
```

**Output:**
```yaml
lifecycle_violations:
  - violation_id: V1
    severity: CRITICAL
    phase: Init
    description: "ddlStatus.SelectedValue read in Page_Init — ViewState has NOT been loaded yet. SelectedValue will always be the default (empty or first item) regardless of what was posted."
    rule_violated: "ViewState is loaded between Init and Load. Control state is only valid from Page_Load onwards."
    fix: "Move this code to Page_Load and wrap in if (IsPostBack): protected void Page_Load(object sender, EventArgs e) { if (IsPostBack) { var selectedStatus = ddlStatus.SelectedValue; ... } }"
viewstate_issues:
  - issue: "ddlStatus.SelectedValue in Page_Init returns default — ViewState not loaded"
    control: "ddlStatus"
    impact: "LoadActiveCustomers() always called, regardless of actual selection"
    fix: "Move read to Page_Load after ViewState restore"
postback_issues:
  - issue: "Reading postback control value in non-postback-safe phase"
    fix: "Add if (IsPostBack) guard after moving to Page_Load"
lifecycle_summary:
  phase_order_correct: false
  viewstate_safe: false
  postback_handling_correct: false
  overall_valid: false
recommendations:
  - recommendation: "Move selectedStatus read to Page_Load with IsPostBack guard — this is the correct phase for reading postback control values"
    priority: critical
confidence: HIGH
```

---

**Related Skills:**
- `webforms-lifecycle-analyzer` - Deep analysis of the full WebForms lifecycle for a page
- `telerik-contract-validator` - Validates Telerik-specific lifecycle constraints
- `safe-change-boundary-detector` - Ensures the fix stays within safe change boundaries
- `webforms-regression-analyzer` - Identifies regression risks from lifecycle changes
