# WebForms Lifecycle Analyzer

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

## Common Scenarios

### Scenario 1: Adding Database Call

**Input:**
```yaml
change: "Load customer data on page load"
operations: ["Database query for customer"]
```

**Analysis:**
```yaml
recommended_event: "Page_Load"
reason: "ViewState available, before rendering"
pattern: |
  protected void Page_Load(object sender, EventArgs e)
  {
      if (!IsPostBack)
      {
          LoadCustomerData();
      }
  }
warnings:
  - "Only load on initial request (!IsPostBack)"
  - "Consider caching in ViewState or Session"
```

### Scenario 2: Dynamic Control Creation

**Input:**
```yaml
change: "Dynamically add controls based on data"
operations: ["Create TextBox controls in loop"]
```

**Analysis:**
```yaml
recommended_event: "Page_Init or Page_Load"
reason: "Controls must be recreated on postback before ViewState loads"
pattern: |
  protected void Page_Init(object sender, EventArgs e)
  {
      // Recreate controls on EVERY request (postback or not)
      CreateDynamicControls();
  }
critical_note: "Dynamic controls MUST be recreated in same order every time"
```

### Scenario 3: Modifying Control Properties

**Input:**
```yaml
change: "Update GridView columns based on user role"
operations: ["Show/hide columns"]
```

**Analysis:**
```yaml
recommended_event: "Page_PreRender"
reason: "All data loaded, last chance before rendering"
pattern: |
  protected void Page_PreRender(object sender, EventArgs e)
  {
      // Modify control appearance
      gvCustomers.Columns[3].Visible = User.IsInRole("Admin");
  }
```

## Decision Tree for Event Selection

```
Need to set page properties (Theme, MasterPage)?
  → Page_PreInit

Need to initialize controls?
  → Page_Init

Need to handle ViewState?
  → Page_Load or later

Need to respond to user action?
  → Control Event Handler (Button_Click, etc.)

Need to modify before rendering?
  → Page_PreRender

Need to do final cleanup?
  → Page_Unload
```

## ViewState Considerations

### ViewState is Available After Init

**Safe ViewState Operations:**
```csharp
// Page_Load or later
protected void Page_Load(object sender, EventArgs e)
{
    // Read ViewState
    var value = ViewState["MyKey"];
    
    // Write ViewState
    ViewState["MyKey"] = "New Value";
}
```

### ViewState Size Impact

**Warning Signs:**
- Large objects in ViewState
- Lists or collections in ViewState
- Heavy ViewState serialization

**Recommendations:**
```yaml
use_viewstate_when:
  - "Small primitive values"
  - "Page-specific state"
  - "No alternative available"

avoid_viewstate_when:
  - "Large collections"
  - "Sensitive data"
  - "Can use Session or Cache"
```

## Telerik Integration Notes

When using Telerik controls:

```yaml
telerik_lifecycle_notes:
  RadGrid:
    - "NeedDataSource fires in Load/PreRender"
    - "ItemCommand fires during postback event"
    - "Rebind() can trigger full lifecycle"
  
  RadComboBox:
    - "ItemsRequested for load-on-demand"
    - "SelectedIndexChanged fires postback"
  
  general:
    - "Telerik controls may trigger additional postbacks"
    - "Some operations require EnableViewState=true"
```

## Safety Checklist

Before approving change:

- [ ] Correct lifecycle event identified
- [ ] ViewState timing respected
- [ ] IsPostBack check included where needed
- [ ] Dynamic controls recreated in Init (if applicable)
- [ ] No expensive operations in Render
- [ ] Telerik control lifecycle understood
- [ ] No ViewState violations

## Usage Example

```
SKILL: webforms-lifecycle-analyzer

INPUT:
  page: "CustomerDetails.aspx"
  change: "Add dropdown to filter orders, populate from database"
  controls: ["ddlOrderFilter"]
  operations:
    - "Query database for filter options"
    - "Bind to dropdown"
    - "Handle selection change"

OUTPUT:
  lifecycle_analysis:
    recommended_events:
      - event: "Page_Load"
        operation: "Load filter options (!IsPostBack)"
        code: |
          if (!IsPostBack)
          {
              LoadFilterOptions();
          }
      
      - event: "ddlOrderFilter_SelectedIndexChanged"
        operation: "Filter grid based on selection"
        code: |
          protected void ddlOrderFilter_SelectedIndexChanged(...)
          {
              FilterOrders(ddlOrderFilter.SelectedValue);
          }
    
    warnings:
      - "Enable AutoPostBack=true on dropdown"
      - "ViewState will store dropdown selection"
      - "Ensure filter loads before grid binds"
    
    safe_to_proceed: yes
```

## Confidence Levels

**High:** Clear lifecycle placement, no violations detected
**Medium:** Minor timing concerns, requires validation
**Low:** Complex interaction, needs spike or testing
