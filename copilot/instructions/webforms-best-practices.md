# ASP.NET WebForms Best Practices

## Page Lifecycle
```csharp
// ✅ Set initial values in Page_Load with IsPostBack check
protected void Page_Load(object sender, EventArgs e)
{
    if (!IsPostBack)
    {
        LoadCustomers(); // Initial load only
    }
}

// ✅ Final modifications in PreRender
protected void Page_PreRender(object sender, EventArgs e)
{
    UpdateControlVisibility();
}

// ❌ Don't set control values after Load event
protected void Button_Click(object sender, EventArgs e)
{
    DropDownList1.SelectedValue = "value"; // Won't work!
}
```

## ViewState Management
```csharp
// ✅ Use ViewState for page-specific state (small data)
private string CurrentFilter
{
    get { return ViewState["CurrentFilter"] as string; }
    set { ViewState["CurrentFilter"] = value; }
}

// ❌ Don't store large objects in ViewState
ViewState["AllCustomers"] = GetAllCustomers(); // BAD - bloats page

// ✅ Use Session or Cache for larger data
Session["AllCustomers"] = GetAllCustomers();
```

## Control IDs
```csharp
// ✅ Keep existing control IDs unchanged
<asp:Button ID="btnSave" runat="server" />

// ❌ Don't rename controls (breaks code-behind)
<asp:Button ID="SaveButton" runat="server" /> // If it was btnSave, keep it
```

## Telerik Controls
```csharp
// ✅ Keep ViewState enabled for Telerik controls
<telerik:RadGrid ID="RadGrid1" runat="server" EnableViewState="true" />

// ✅ Handle NeedDataSource for grids
protected void RadGrid1_NeedDataSource(object sender, GridNeedDataSourceEventArgs e)
{
    RadGrid1.DataSource = GetCustomers();
}

// ❌ Don't disable ViewState on Telerik controls
<telerik:RadGrid EnableViewState="false" /> // Breaks functionality!
```

## Critical Rules
- Never change existing control IDs
- Respect the page lifecycle order
- Keep ViewState enabled for Telerik controls
- Don't store large objects in ViewState
