---
name: telerik-contract-validator
description: Validates that code changes don't break Telerik control contracts including ViewState requirements, DataSource bindings, event handlers, and control lifecycle expectations.
---

# Telerik Contract Validator

## Quick Example

**Input:** RadGrid DataSource changed from ObjectDataSource to manual binding, NeedDataSource event removed
**Output:** CRITICAL violation — RadGrid requires NeedDataSource event handler or EnableViewState must be false. Missing handler will cause "RadGrid requires either a data source or a NeedDataSource event handler" exception.
**Time:** 2-3 minutes

---

## Purpose
Validates that code changes don't break Telerik control contracts including ViewState requirements, DataSource bindings, event handlers, and control lifecycle expectations.

## Input

```yaml
input:
  telerik_control_name: <RadGrid|RadComboBox|RadEditor|RadAjaxManager|RadDatePicker|etc>
  property_changes: <list of properties being modified>
  event_handler_changes: <list of event handlers being added, removed, or modified>
  databinding_method: OBJECTDATASOURCE|MANUAL|LINQ|NEDDATASOURCE_EVENT
  viewstate_change: <true|false — is EnableViewState being changed>
  code_change: <the code being validated>
```

## Output

```yaml
output:
  contract_violations:
    - violation_id: <C1..Cn>
      severity: CRITICAL|HIGH|MEDIUM|LOW
      control: <control name>
      property_or_event: <what is being changed>
      description: <what contract is violated>
      telerik_requirement: <the Telerik rule being broken>
      fix: <how to fix it>
  event_binding_issues:
    - event: <event name>
      issue: <description>
      consequence: <what happens at runtime>
      fix: <correction>
  viewstate_contract_issues:
    - issue: <description>
      impact: <what breaks if ViewState is disabled incorrectly>
      fix: <correction>
  datasource_issues:
    - issue: <description>
      fix: <correction>
  validation_summary:
    all_contracts_valid: true|false
    critical_violations: <count>
    can_deploy_safely: true|false
  confidence: HIGH|MEDIUM|LOW
```

## DO:
✅ Verify NeedDataSource event handler is present when RadGrid uses server-side paging
✅ Check that RadComboBox DataTextField and DataValueField match the data source schema
✅ Validate that RadAjaxManager/RadAjaxPanel wraps all controls involved in async operations
✅ Verify RadEditor SaveContent() is called before reading editor content in postback
✅ Check that RadGrid columns match the DataSource schema — mismatch causes silent binding failures

## DON'T:
❌ Disable ViewState on RadGrid if server-side paging or selection is used
❌ Remove NeedDataSource event from RadGrid without switching to manual binding mode
❌ Set RadComboBox.DataSource in Page_PreRender — too late for RadAjax callbacks
❌ Wire RadGrid RowCommand without checking RadCommandEventArgs cast
❌ Use ClientIDMode="Static" on Telerik controls — it breaks the naming container

## Error Conditions

**IF Telerik control version is unknown:**
```
1. Check Telerik.Web.UI.dll version in project references
2. Some contracts changed between Telerik versions (pre-2014 vs post-2014)
3. Flag: VERSION_UNKNOWN — validation may miss version-specific requirements
```

**IF code uses RadGrid with mixed DataSource and NeedDataSource:**
```
1. These modes are mutually exclusive
2. Flag: CONFLICTING_BINDING_MODES — choose one binding strategy
```

**IF RadAjaxManager is not present and async is expected:**
```
1. Check for UpdatePanel (Microsoft's async alternative)
2. If neither: async updates won't work
3. Return: ASYNC_NOT_CONFIGURED — add RadAjaxManager or UpdatePanel
```

## Processing Steps

1. **Control Contract Identification:** Based on control type, identify required contracts: RadGrid → NeedDataSource or DataSource + DataBind, EnableViewState for paging. RadComboBox → DataTextField, DataValueField must match source. RadEditor → content read via .Content property post-SaveContent.

2. **Property Change Validation:** For each changed property: check if change violates a contract. Example: setting AllowPaging=true on RadGrid requires either NeedDataSource event or DataSource set in Page_Load.

3. **Event Handler Check:** Identify events being added/removed/modified. For each removal: verify it's not required for the control to function. Required events: RadGrid.NeedDataSource (with server-side paging), RadGrid.ItemCommand, RadComboBox.ItemsRequested (with load-on-demand).

4. **ViewState Analysis:** If ViewState is being disabled: check all controls that depend on ViewState for state retention. RadGrid selection state, RadComboBox selected item, RadDatePicker selected date — all require ViewState.

5. **DataSource Binding Validation:** Verify DataTextField/DataValueField match property names on the data object. Case-sensitive. Check that DataSource is set before DataBind() is called.

6. **RadAjax Validation:** If async updates needed: verify control is in RadAjaxManager AjaxSettings or wrapped in RadAjaxPanel. Missing async config causes full page postback instead of partial.

7. **Fix Generation:** For each violation: provide the exact fix with code example. Include Telerik documentation reference if the rule is non-obvious.

## Example

**Input:**
```yaml
telerik_control_name: RadGrid
property_changes: ["Removed NeedDataSource event handler", "Added DataSource in Page_Load"]
event_handler_changes: ["Removed: RadGrid1_NeedDataSource", "Added: direct DataSource assignment"]
databinding_method: MANUAL
viewstate_change: false
code_change: |
  protected void Page_Load(object sender, EventArgs e)
  {
      RadGrid1.DataSource = GetCustomers();
      RadGrid1.DataBind();
  }
  // Removed: protected void RadGrid1_NeedDataSource(object sender, GridNeedDataSourceEventArgs e) { ... }
```

**Output:**
```yaml
contract_violations:
  - violation_id: C1
    severity: HIGH
    control: RadGrid1
    property_or_event: NeedDataSource
    description: "Switched from NeedDataSource event to manual DataSource+DataBind in Page_Load. This will cause double binding on postbacks — Page_Load fires on every request, rebinding the grid on every postback (including button clicks, pagination, sorting)."
    telerik_requirement: "When using manual DataSource binding, wrap DataBind in if (!IsPostBack) or use NeedDataSource event which RadGrid calls only when it needs fresh data."
    fix: |
      protected void Page_Load(object sender, EventArgs e)
      {
          if (!IsPostBack) // Add this guard
          {
              RadGrid1.DataSource = GetCustomers();
              RadGrid1.DataBind();
          }
      }
event_binding_issues: []
viewstate_contract_issues: []
datasource_issues:
  - issue: "DataBind called on every postback — grid loses selection state and pagination position on every postback"
    fix: "Add if (!IsPostBack) guard or restore NeedDataSource event"
validation_summary:
  all_contracts_valid: false
  critical_violations: 0
  can_deploy_safely: false
recommendations:
  - recommendation: "Add if (!IsPostBack) guard to prevent rebinding on postbacks OR restore NeedDataSource pattern which handles this automatically"
    priority: high
confidence: HIGH
```

---

**Related Skills:**
- `telerik-behavior-analyzer` - Analyzes current Telerik control behavior and configuration
- `webforms-lifecycle-validator` - Validates overall WebForms lifecycle correctness
- `webforms-regression-analyzer` - Identifies regression risks from Telerik control changes
- `telerik-impact-checker` - Checks feature-level impact of Telerik control changes
