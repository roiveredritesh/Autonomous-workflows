# Error Handling Patterns

## Input Validation
```csharp
// ✅ Validate inputs at entry points
public void ProcessOrder(Order order)
{
    if (order == null)
        throw new ArgumentNullException(nameof(order));

    if (order.Items == null || order.Items.Count == 0)
        throw new ArgumentException("Order must have items", nameof(order));

    // Process...
}
```

## Null Checking
```csharp
// ✅ Check for null from external sources
var customer = GetCustomerById(id);
if (customer == null)
{
    return NotFound();
}

// ✅ Use null-conditional operator
var addressLine = customer?.Address?.Line1 ?? "No address";

// ❌ Don't assume non-null from user input or database
var name = customer.Name; // Might throw NullReferenceException!
```

## Try-Catch Usage
```csharp
// ✅ Handle expected errors
try
{
    var data = externalService.GetData();
}
catch (TimeoutException ex)
{
    _logger.Error("Service timeout", ex);
    return defaultValue;
}

// ❌ Don't swallow exceptions
try
{
    DoSomething();
}
catch { } // BAD - silently fails

// ❌ Don't catch Exception unless at top-level
catch (Exception ex) // Only in Global.asax or top-level handlers
```

## SQL Injection Prevention
```csharp
// ✅ Use parameterized queries
var customers = context.Database.SqlQuery<Customer>(
    "EXEC GetCustomersByStatus @Status",
    new SqlParameter("@Status", "Active")
).ToList();

// ❌ Never use string concatenation for SQL
var sql = $"SELECT * FROM Customers WHERE Status = '{status}'"; // DANGEROUS!
```

## Transaction Handling
```csharp
// ✅ Use transactions for multi-step operations
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

## Resource Cleanup
```csharp
// ✅ Always dispose IDisposable objects
using (var context = new MyDbContext())
{
    // Use context
} // Automatically disposed

// ❌ Don't leave connections open
var context = new MyDbContext();
// ... use it ... but never dispose - MEMORY LEAK!
```

**Golden Rules:**
- Always validate user input
- Always check for null from external sources
- Never swallow exceptions
- Always use parameterized queries
- Always dispose resources
