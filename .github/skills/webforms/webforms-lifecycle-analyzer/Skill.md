---
name: webforms-lifecycle-analyzer
description: Analyzes ASP.NET WebForms page lifecycle impact and ensures compliance with lifecycle requirements.
---

## Purpose
Analyzes ASP.NET WebForms page lifecycle impact and ensures compliance with lifecycle requirements.

## ASP.NET WebForms Page Lifecycle

### Standard Lifecycle Events (in order)

1. **PreInit** - Theme, master page set
2. **Init** - Initialize controls, read ViewState
3. **InitComplete** - ViewState tracking begins
4. **PreLoad** - Before Load
5. **Load** - Load ViewState and ControlState
6. **Control Events** - Button clicks, etc.
7. **LoadComplete** - After all controls loaded
8. **PreRender** - Last chance to modify controls
9. **PreRenderComplete** - All controls ready
10. **SaveStateComplete** - ViewState saved
11. **Render** - Generate HTML
12. **Unload** - Cleanup

## Analysis Process

### 1. Identify Current Implementation

**Examine:**
- Which lifecycle events are currently used?
- What operations happen in each event?
- Is ViewState enabled?
- Are there custom controls?

### 2. Analyze Proposed Change

**Check:**
- What lifecycle events will be affected?
- Where should new code execute?
- Will ViewState be modified?
- Are there timing dependencies?

### 3. Detect Lifecycle Violations

**Common Violations:**

**❌ Setting Controls in Wrong Event**
```csharp
// WRONG: Setting control in Page_Load after postback
protected void Page_Load(object sender, EventArgs e)
{
    if (IsPostBack)
        txtName.Text = "New Value"; // ViewState already loaded!
}
```

**✅ Correct Approach**
```csharp
// CORRECT: Set before or check timing
protected void Page_PreInit(object sender, EventArgs e)
{
    // Set before ViewState loads
}
```

**❌ ViewState Access Before Init**
```csharp
// WRONG: ViewState not available yet
protected void Page_PreInit(object sender, EventArgs e)
{
    var value = ViewState["Key"]; // ViewState not loaded!
}
```

**✅ Correct Approach**
```csharp
// CORRECT: Access after Init
protected void Page_Load(object sender, EventArgs e)
{
    var value = ViewState["Key"];
}
```

**❌ Expensive Operations in Render**
```csharp
// WRONG: Database call during rendering
protected override void Render(HtmlTextWriter writer)
{
    var data = Database.Query(); // Too late!
    base.Render(writer);
}
```

**✅ Correct Approach**
```csharp
// CORRECT: Load data in PreRender
protected void Page_PreRender(object sender, EventArgs e)
{
    var data = Database.Query();
    ViewBag.Data = data;
}
```

## Input

```yaml
page_name: <aspx page>
proposed_change: <description of change>
affected_controls: [<list of controls>]
operations: [<operations to perform>]
```

## Output

```yaml
lifecycle_analysis:
  current_implementation:
    events_used: [<list of lifecycle events>]
    viewstate_usage: <enabled|disabled>
    custom_controls: [<list if any>]
  
  impact_assessment:
    affected_events: [<lifecycle events impacted>]
    recommended_event: <where to place new code>
    timing_concerns: [<issues if any>]
  
  violations_detected:
    - violation: <description>
      severity: <high|medium|low>
      location: <file and line>
      fix: <how to correct>
  
  recommendations:
    - event: <lifecycle event>
      operation: <what to do>
      reason: <why this event>
  
  safe_to_proceed: <yes|no|with_changes>
  risks: [<identified risks>]

confidence: <high|medium|low>
```

## DO
✅ Place database calls in `Page_Load` with `!IsPostBack` guard
✅ Recreate dynamic controls in `Page_Init` on every request
✅ Modify control properties in `Page_PreRender`
✅ Set Theme/MasterPage in `Page_PreInit`
✅ Check ViewState availability — only after Init

## DON'T
❌ Access ViewState in `Page_PreInit` (not loaded yet)
❌ Make database calls in `Render` (too late)
❌ Skip `!IsPostBack` guard for initial data loads
❌ Forget to recreate dynamic controls on postback
❌ Ignore Telerik control lifecycle (NeedDataSource, ItemCommand)

## Error Conditions

**IF lifecycle violation detected:**
- Flag as high severity
- Explain which event was wrong and why
- Provide corrected event placement

**IF Telerik controls involved:**
- Check `NeedDataSource`/`ItemCommand` event timing
- Warn: `Rebind()` triggers full lifecycle — use sparingly

## Related Skills
- `webforms-viewstate-analyzer` - ViewState impact analysis
- `telerik-impact-checker` - Telerik control lifecycle
- `safe-change-boundary-detector` - Safe modification points
