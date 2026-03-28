# Redis Caching Patterns

## Key Naming Conventions
```csharp
// ✅ Use consistent key patterns
private const string CACHE_KEY_PREFIX = "customers";

// Pattern: {entity}:{id}
var cacheKey = $"{CACHE_KEY_PREFIX}:{customerId}";
// Example: "customers:12345"

// Pattern: {entity}:list:{filter}
var listKey = $"{CACHE_KEY_PREFIX}:list:active";
// Example: "customers:list:active"
```

## Cache-Aside Pattern
```csharp
// ✅ Check cache, fallback to database
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
```

## Cache Invalidation
```csharp
// ✅ Invalidate on updates
public void UpdateCustomer(Customer customer)
{
    _repository.Update(customer);

    // Invalidate single item cache
    var cacheKey = $"customers:{customer.Id}";
    _redis.Remove(cacheKey);

    // Invalidate list caches that include this customer
    _redis.Remove("customers:list:active");
    _redis.Remove("customers:list:all");
}
```

## Expiration Strategy
```csharp
// ✅ Set appropriate TTL based on data volatility
_redis.Set(key, value, TimeSpan.FromMinutes(5));  // Frequently changing
_redis.Set(key, value, TimeSpan.FromHours(1));    // Moderately stable
_redis.Set(key, value, TimeSpan.FromDays(1));     // Very stable
```

## What to Cache
**Good candidates:**
- ✅ Read-heavy data (read:write > 10:1)
- ✅ Expensive to compute/query
- ✅ Shared across users
- ✅ Relatively stable

**Bad candidates:**
- ❌ Write-heavy data
- ❌ User-specific sensitive data
- ❌ Must be real-time
- ❌ Frequently changing

**Critical Rule:** Always invalidate cache when underlying data changes.
