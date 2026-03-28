# C# Project Standards for GitHub Copilot

## Project Context
Legacy ASP.NET WebForms application with Telerik UI controls, Redis caching, and MSSQL database.

## Core Principles

### 1. Minimal Changes Philosophy
> "The best code is no code. The second best is boring code that works."

- ✅ Make the smallest change that solves the problem
- ✅ Follow existing patterns, don't create new ones
- ✅ Preserve existing code structure and style
- ❌ Don't refactor code unless explicitly requested
- ❌ Don't add "improvements" outside the scope
- ❌ Don't optimize prematurely

### 2. Safety First
- ✅ Never break public APIs or method signatures
- ✅ Respect WebForms page lifecycle (PreInit → Init → Load → Events → PreRender → Render)
- ✅ Preserve ViewState behavior
- ✅ Never skip null checks for user input or external data
- ❌ Don't change existing control IDs or names
- ❌ Don't modify database schema without explicit approval

### 3. Pattern Reuse
- ✅ Find similar existing code and copy its pattern
- ✅ Use existing libraries and helpers already in the project
- ✅ Match existing naming conventions
- ❌ Don't introduce new libraries for one-off needs
- ❌ Don't create helper methods for single use

---

## C# Coding Standards

### Naming Conventions

**Classes:**
```csharp
// ✅ DO: PascalCase for classes
public class CustomerRepository { }
public class OrderProcessor { }

// ❌ DON'T: camelCase or snake_case
public class customerRepository { }
public class order_processor { }
```

**Methods:**
```csharp
// ✅ DO: PascalCase for public methods
public void ProcessOrder() { }
public Customer GetCustomerById(int id) { }

// ✅ DO: PascalCase for private methods
private void ValidateInput() { }
private bool IsValidOrder() { }
```

**Variables and Fields:**
```csharp
// ✅ DO: camelCase for local variables
var customerName = "John";
int orderCount = 10;

// ✅ DO: PascalCase for public properties
public string CustomerName { get; set; }
public int OrderId { get; set; }

// ✅ DO: _camelCase for private fields (match existing pattern)
private readonly ICustomerRepository _customerRepository;
private string _cachedValue;

// ❌ DON'T: Use Hungarian notation
private string strCustomerName;
private int intOrderId;
```

**Constants:**
```csharp
// ✅ DO: PascalCase or UPPER_CASE (match existing pattern in file)
private const int MaxRetries = 3;
private const string DEFAULT_CACHE_KEY = "customers:all";

// Check existing file to match their style
```

### Code Structure

**Method Length:**
```csharp
// ✅ DO: Keep methods focused and short (< 50 lines ideal)
public Customer GetCustomerById(int customerId)
{
    if (customerId <= 0)
        throw new ArgumentException("Invalid customer ID", nameof(customerId));

    return _repository.GetById(customerId);
}

// ❌ DON'T: Create 200+ line methods (unless you're matching existing code)
```

**Error Handling:**
```csharp
// ✅ DO: Validate inputs at entry points
public void ProcessOrder(Order order)
{
    if (order == null)
        throw new ArgumentNullException(nameof(order));

    if (order.Items == null || order.Items.Count == 0)
        throw new ArgumentException("Order must have items", nameof(order));

    // Process...
}

// ✅ DO: Handle expected errors with try-catch
try
{
    var data = externalService.GetData();
}
catch (TimeoutException ex)
{
    _logger.Error("Service timeout", ex);
    return defaultValue;
}

// ❌ DON'T: Swallow exceptions without logging
try
{
    DoSomething();
}
catch { } // BAD!

// ❌ DON'T: Catch Exception unless at top-level
catch (Exception ex) // Only in Global.asax or top-level handlers
```

**Null Checking:**
```csharp
// ✅ DO: Check for null from external sources
var customer = GetCustomerById(id);
if (customer == null)
{
    return NotFound();
}

// ✅ DO: Use null-conditional operator when appropriate
var addressLine = customer?.Address?.Line1 ?? "No address";

// ❌ DON'T: Assume non-null from user input, database, or external APIs
var name = customer.Name; // Might throw NullReferenceException!
```

---

## ASP.NET WebForms Specific

### Page Lifecycle
```csharp
// ✅ DO: Set control properties in the correct event
protected void Page_Load(object sender, EventArgs e)
{
    if (!IsPostBack)
    {
        // Initial page load - bind data
        LoadCustomers();
    }
}

protected void Page_PreRender(object sender, EventArgs e)
{
    // Last chance to modify controls before rendering
    UpdateControlVisibility();
}

// ❌ DON'T: Set control values after their Load event
protected void Button_Click(object sender, EventArgs e)
{
    // This is during control events, after Load
    DropDownList1.SelectedValue = "value"; // Won't work as expected!
}
```

### ViewState
```csharp
// ✅ DO: Use ViewState for page-specific state
private string CurrentFilter
{
    get { return ViewState["CurrentFilter"] as string; }
    set { ViewState["CurrentFilter"] = value; }
}

// ❌ DON'T: Store large objects in ViewState (> 1KB)
ViewState["AllCustomers"] = GetAllCustomers(); // BAD - bloats page size

// ✅ DO: Use Session or Cache for larger data
Session["AllCustomers"] = GetAllCustomers();
```

### Control References
```csharp
// ✅ DO: Keep existing control IDs unchanged
<asp:Button ID="btnSave" runat="server" OnClick="btnSave_Click" />

// ❌ DON'T: Rename controls (breaks code-behind references)
<asp:Button ID="SaveButton" runat="server" /> // If it was btnSave, keep it btnSave
```

---

## Telerik Controls

### Binding Patterns
```csharp
// ✅ DO: Follow existing Telerik binding pattern in the file
protected void Page_Load(object sender, EventArgs e)
{
    if (!IsPostBack)
    {
        RadGrid1.DataSource = GetCustomers();
        RadGrid1.DataBind();
    }
}

// ✅ DO: Handle Telerik events
protected void RadGrid1_NeedDataSource(object sender, GridNeedDataSourceEventArgs e)
{
    RadGrid1.DataSource = GetCustomers();
}

// ❌ DON'T: Mix server and AJAX binding patterns
```

### ViewState Requirements
```csharp
// ✅ DO: Keep ViewState enabled for Telerik controls
<telerik:RadGrid ID="RadGrid1" runat="server" EnableViewState="true">

// ❌ DON'T: Disable ViewState on Telerik controls (breaks functionality)
<telerik:RadGrid ID="RadGrid1" runat="server" EnableViewState="false"> // BAD!
```

---

## Data Access (LINQ & EF)

### LINQ Queries
```csharp
// ✅ DO: Filter and sort in the database (before .ToList())
var customers = context.Customers
    .Where(c => c.Status == "Active")
    .OrderBy(c => c.Name)
    .Take(50)
    .ToList();

// ❌ DON'T: Filter after .ToList() (loads all data into memory)
var customers = context.Customers
    .ToList()
    .Where(c => c.Status == "Active") // BAD - filters in memory
    .OrderBy(c => c.Name)
    .Take(50)
    .ToList();

// ✅ DO: Project only needed columns
var customerNames = context.Customers
    .Select(c => new { c.Id, c.Name })
    .ToList();

// ❌ DON'T: Select entire entities when you only need a few fields
var customers = context.Customers.ToList(); // Then only use .Name
```

### N+1 Query Problem
```csharp
// ✅ DO: Use Include() for related data
var orders = context.Orders
    .Include(o => o.Customer)
    .Include(o => o.Items)
    .ToList();

// ❌ DON'T: Lazy load in loops
var orders = context.Orders.ToList();
foreach (var order in orders)
{
    var customer = order.Customer; // N+1: Queries database for each order!
}
```

### Async/Await
```csharp
// ✅ DO: Use async for database operations (if existing code uses it)
public async Task<List<Customer>> GetCustomersAsync()
{
    return await context.Customers
        .Where(c => c.Status == "Active")
        .ToListAsync();
}

// ❌ DON'T: Mix sync and async in WebForms (check existing pattern first)
// WebForms has limited async support - match existing code style
```

---

## Redis Caching

### Key Naming
```csharp
// ✅ DO: Use consistent key patterns
private const string CACHE_KEY_PREFIX = "customers";
var cacheKey = $"{CACHE_KEY_PREFIX}:{customerId}";
var listKey = $"{CACHE_KEY_PREFIX}:list:active";

// Pattern: {entity}:{id} or {entity}:list:{filter}
```

### Cache Operations
```csharp
// ✅ DO: Handle cache misses gracefully
public Customer GetCustomer(int customerId)
{
    var cacheKey = $"customers:{customerId}";
    var cached = _redis.Get<Customer>(cacheKey);

    if (cached != null)
        return cached;

    var customer = _repository.GetById(customerId);
    if (customer != null)
    {
        _redis.Set(cacheKey, customer, TimeSpan.FromMinutes(10));
    }

    return customer;
}

// ✅ DO: Invalidate cache on updates
public void UpdateCustomer(Customer customer)
{
    _repository.Update(customer);

    var cacheKey = $"customers:{customer.Id}";
    _redis.Remove(cacheKey);

    // Also invalidate list caches that might include this customer
    _redis.Remove("customers:list:active");
}
```

---

## Database (SQL Server)

### Stored Procedures
```csharp
// ✅ DO: Use parameterized queries or stored procedures
var customers = context.Database.SqlQuery<Customer>(
    "EXEC GetCustomersByStatus @Status",
    new SqlParameter("@Status", "Active")
).ToList();

// ❌ DON'T: Use string concatenation (SQL injection risk)
var sql = $"SELECT * FROM Customers WHERE Status = '{status}'"; // DANGEROUS!
```

### Transactions
```csharp
// ✅ DO: Use transactions for multi-step operations
using (var transaction = context.Database.BeginTransaction())
{
    try
    {
        context.Orders.Add(order);
        context.SaveChanges();

        UpdateInventory(order.Items);
        context.SaveChanges();

        transaction.Commit();
    }
    catch
    {
        transaction.Rollback();
        throw;
    }
}
```

---

## Performance Patterns

### Pagination
```csharp
// ✅ DO: Paginate at database level
public List<Customer> GetCustomers(int page, int pageSize)
{
    return context.Customers
        .OrderBy(c => c.Name)
        .Skip((page - 1) * pageSize)
        .Take(pageSize)
        .ToList();
}

// ❌ DON'T: Load all data then paginate
var allCustomers = context.Customers.ToList(); // Loads 100,000 records!
return allCustomers.Skip(start).Take(count);
```

### Lazy Loading
```csharp
// ✅ DO: Disable lazy loading if not needed
context.Configuration.LazyLoadingEnabled = false;

// ✅ DO: Use explicit Include() instead
var orders = context.Orders.Include(o => o.Customer).ToList();
```

---

## Testing

### Unit Test Structure
```csharp
// ✅ DO: Follow Arrange-Act-Assert pattern
[Test]
public void GetCustomerById_ValidId_ReturnsCustomer()
{
    // Arrange
    var repository = new Mock<ICustomerRepository>();
    repository.Setup(r => r.GetById(1)).Returns(new Customer { Id = 1, Name = "John" });
    var service = new CustomerService(repository.Object);

    // Act
    var result = service.GetCustomerById(1);

    // Assert
    Assert.IsNotNull(result);
    Assert.AreEqual("John", result.Name);
}

// ✅ DO: Test edge cases
[Test]
public void GetCustomerById_InvalidId_ReturnsNull()
{
    // Test with 0, negative numbers, non-existent IDs
}
```

---

## Common Pitfalls to Avoid

### 1. ViewState Bloat
```csharp
// ❌ DON'T: Store collections in ViewState
ViewState["Customers"] = customers; // Increases page size

// ✅ DO: Store just IDs or use Cache/Session
ViewState["CustomerIds"] = customers.Select(c => c.Id).ToArray();
```

### 2. Memory Leaks
```csharp
// ✅ DO: Dispose of IDisposable objects
using (var context = new MyDbContext())
{
    // Use context
}

// ❌ DON'T: Leave connections open
var context = new MyDbContext();
// ... use it ... but never dispose
```

### 3. Blocking Async
```csharp
// ❌ DON'T: Block on async methods (causes deadlocks)
var result = GetCustomersAsync().Result; // BAD!
var result2 = GetCustomersAsync().Wait(); // BAD!

// ✅ DO: Use await or make method synchronous
var result = await GetCustomersAsync();
```

---

## Comments and Documentation

### When to Comment
```csharp
// ✅ DO: Comment WHY, not WHAT
// Using ToList() here to avoid deferred execution across web request boundary
var customers = query.ToList();

// ❌ DON'T: State the obvious
// Get customer by ID
var customer = GetCustomerById(id);

// ✅ DO: Document workarounds
// HACK: Telerik RadGrid requires ViewState for paging
// See: https://docs.telerik.com/devtools/aspnet-ajax/controls/grid/...
EnableViewState = true;

// ✅ DO: Document complex business logic
// Calculate discount: 10% for orders > $1000, 5% for > $500
// Discount cannot exceed 20% total per policy DOC-2451
```

### XML Documentation
```csharp
// ✅ DO: Document public APIs
/// <summary>
/// Retrieves customer by ID with cached result.
/// </summary>
/// <param name="customerId">The customer ID</param>
/// <returns>Customer object or null if not found</returns>
/// <exception cref="ArgumentException">Thrown when customerId is invalid</exception>
public Customer GetCustomerById(int customerId)
{
    // Implementation
}
```

---

## File Organization

### Project Structure
```
/App_Code           - Reusable classes
/Controls           - User controls (.ascx)
/Pages             - ASPX pages
/Services          - Business logic
/Repositories      - Data access
/Models            - Data models
/Helpers           - Utility classes
```

### Namespace Conventions
```csharp
// ✅ DO: Match folder structure
namespace YourProject.Services
{
    public class CustomerService { }
}

namespace YourProject.Repositories
{
    public class CustomerRepository { }
}
```

---

## Quick Reference Card

**When adding new code:**
1. Find similar existing code - copy its pattern
2. Use same naming conventions as surrounding code
3. Match existing indentation and formatting
4. Follow same error handling approach
5. Use same libraries (don't add new ones)
6. Test with same data patterns

**Red flags to avoid:**
- ❌ Refactoring existing code "while you're in there"
- ❌ Changing method signatures without checking all callers
- ❌ Disabling ViewState on Telerik controls
- ❌ Loading all data then filtering in memory
- ❌ String concatenation for SQL queries
- ❌ Swallowing exceptions
- ❌ Storing large objects in ViewState

**Always check:**
- ✅ Does this change break existing functionality?
- ✅ Is this the minimal change needed?
- ✅ Does this follow existing patterns?
- ✅ Have I handled null cases?
- ✅ Have I tested edge cases?

---

## Integration with Autonomous Workflow

When using this standards document with the autonomous workflow framework:

**For skills reference:**
- Analysis skills: `skills/analysis/{skill-name}/Skill.md`
- Planning skills: `skills/planning/{skill-name}/Skill.md`
- Validation skills: `skills/validation/{skill-name}/Skill.md`
- WebForms skills: `skills/webforms/{skill-name}/Skill.md`
- Data skills: `skills/data/{skill-name}/Skill.md`

**For workflow execution:**
- Always use `minimal-diff-planner` for implementation planning
- Use `safe-change-boundary-detector` to validate changes won't break existing code
- Use `webforms-lifecycle-analyzer` for any WebForms changes
- Use `linq-query-tracer` for data access changes

---

**Related Documents:**
- `copilot/skills/` - All skills organized by category
- `copilot/agents/` - Workflow agents
- `copilot/TEMPLATES.md` - Output templates
- `copilot/APPROVAL_MECHANISM_ASSESSMENT.md` - Execution model

**Last Updated:** 2026-03-28
