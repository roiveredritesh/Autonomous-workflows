# LINQ and Entity Framework Best Practices

## Query Efficiency
```csharp
// ✅ Filter and sort in database (before .ToList())
var customers = context.Customers
    .Where(c => c.Status == "Active")
    .OrderBy(c => c.Name)
    .Take(50)
    .ToList();

// ❌ Don't filter after .ToList() (loads all data)
var customers = context.Customers
    .ToList()
    .Where(c => c.Status == "Active") // BAD - filters in memory
    .ToList();
```

## Projection
```csharp
// ✅ Select only needed columns
var customerNames = context.Customers
    .Select(c => new { c.Id, c.Name })
    .ToList();

// ❌ Don't select entire entities when only need few fields
var customers = context.Customers.ToList(); // Then only use .Name
```

## N+1 Query Problem
```csharp
// ✅ Use Include() for related data
var orders = context.Orders
    .Include(o => o.Customer)
    .Include(o => o.Items)
    .ToList();

// ❌ Don't lazy load in loops
var orders = context.Orders.ToList();
foreach (var order in orders)
{
    var customer = order.Customer; // Queries database for each order!
}
```

## Async Operations
```csharp
// ✅ Use async for database operations (if existing code uses it)
public async Task<List<Customer>> GetCustomersAsync()
{
    return await context.Customers
        .Where(c => c.Status == "Active")
        .ToListAsync();
}

// ⚠️ Check existing pattern - WebForms has limited async support
```

## Pagination
```csharp
// ✅ Paginate at database level
public List<Customer> GetCustomers(int page, int pageSize)
{
    return context.Customers
        .OrderBy(c => c.Name)
        .Skip((page - 1) * pageSize)
        .Take(pageSize)
        .ToList();
}

// ❌ Don't load all then paginate
var all = context.Customers.ToList(); // Loads 100,000 records!
return all.Skip(start).Take(count);
```

**Golden Rule:** Do filtering, sorting, and pagination in the database, not in memory.
