# Redis Cache Strategy Analyzer

## Purpose
Analyzes caching requirements and designs safe, effective Redis caching strategies for legacy ASP.NET WebForms application.

## Input

```yaml
data_to_cache: <description of data>
access_pattern: <how often accessed>
data_volume: <size estimate>
update_frequency: <how often changes>
consistency_requirement: <strict|eventual|best_effort>
```

## Analysis Process

### 1. Assess Cache Suitability

**Good Candidates for Caching:**
- ✅ Read-heavy data (read:write > 10:1)
- ✅ Expensive to compute/query
- ✅ Shared across users
- ✅ Relatively stable data
- ✅ Tolerate some staleness

**Poor Candidates:**
- ❌ Write-heavy data
- ❌ User-specific sensitive data
- ❌ Must be real-time
- ❌ Frequently changing
- ❌ Simple to query

### 2. Design Key Strategy

**Key Pattern Design:**

**Pattern: Entity Type + Identifier**
```
Format: {entity}:{id}
Example: customer:12345
Example: product:SKU-789
```

**Pattern: List/Collection**
```
Format: {entity}:list:{criteria}
Example: customers:list:active
Example: products:list:category:electronics
```

**Pattern: Computed/Aggregated**
```
Format: {computation}:{params}
Example: sales:total:2024-01
Example: inventory:count:warehouse:east
```

**Pattern: User-Specific**
```
Format: user:{userId}:{resource}
Example: user:456:cart
Example: user:456:preferences
```

### 3. Determine TTL Strategy

**TTL Guidelines:**

```yaml
static_reference_data:
  ttl: 24 hours
  example: "Product categories, states list"
  
semi_static_data:
  ttl: 1-4 hours
  example: "Product catalog, customer list"
  
frequently_updated:
  ttl: 5-30 minutes
  example: "Inventory levels, order status"
  
computed_results:
  ttl: based on computation cost
  example: "Complex reports, aggregations"
  
user_session_data:
  ttl: session duration + 1 hour
  example: "Shopping cart, user preferences"
```

### 4. Design Invalidation Strategy

**Invalidation Patterns:**

**Pattern 1: Direct Invalidation**
```csharp
// When entity changes, delete its cache
public void UpdateCustomer(int id, Customer data)
{
    _repository.Update(id, data);
    _cache.Remove($"customer:{id}");
}
```

**Pattern 2: Wildcard Invalidation**
```csharp
// Invalidate multiple related keys
public void UpdateProduct(int id, Product data)
{
    _repository.Update(id, data);
    _cache.Remove($"product:{id}");
    _cache.RemovePattern("products:list:*"); // All product lists
}
```

**Pattern 3: Tag-Based Invalidation**
```csharp
// Tag cache entries for bulk invalidation
_cache.Set("customer:123", data, tags: ["customers", "active-customers"]);
// Later: invalidate all with tag
_cache.InvalidateTag("customers");
```

**Pattern 4: Time-Based (Passive)**
```csharp
// Let TTL handle invalidation
_cache.Set("report:monthly", data, ttl: TimeSpan.FromHours(24));
// No explicit invalidation needed
```

### 5. Detect Cache Stampede Risk

**Stampede Scenario:**
```
1. Cache entry expires
2. Multiple requests see cache miss simultaneously
3. All requests query database
4. Database overwhelmed
```

**Detection:**
```yaml
high_risk:
  - High traffic endpoint
  - Expensive query (>1 second)
  - Large TTL with synchronized expiry
  
medium_risk:
  - Moderate traffic
  - Moderate query cost
  - Predictable expiry time
  
low_risk:
  - Low traffic
  - Cheap query
  - Staggered expiry
```

**Mitigation Strategies:**

**Strategy 1: Lock-Based Refresh**
```csharp
public async Task<T> GetOrRefresh<T>(string key, Func<Task<T>> factory)
{
    var cached = await _cache.GetAsync<T>(key);
    if (cached != null) return cached;
    
    // Acquire lock
    using (await _lock.AcquireAsync($"lock:{key}"))
    {
        // Double-check after acquiring lock
        cached = await _cache.GetAsync<T>(key);
        if (cached != null) return cached;
        
        // Only one request computes
        var data = await factory();
        await _cache.SetAsync(key, data, ttl);
        return data;
    }
}
```

**Strategy 2: Probabilistic Early Refresh**
```csharp
public async Task<T> GetWithEarlyRefresh<T>(string key, Func<Task<T>> factory, TimeSpan ttl)
{
    var (data, remainingTtl) = await _cache.GetWithTtl<T>(key);
    
    if (data != null)
    {
        // Probabilistically refresh before expiry
        var refreshProbability = 1.0 - (remainingTtl.TotalSeconds / ttl.TotalSeconds);
        if (Random.NextDouble() < refreshProbability * 0.1)
        {
            // Async refresh (don't wait)
            _ = Task.Run(async () =>
            {
                var fresh = await factory();
                await _cache.SetAsync(key, fresh, ttl);
            });
        }
        return data;
    }
    
    // Cache miss - standard load
    data = await factory();
    await _cache.SetAsync(key, data, ttl);
    return data;
}
```

**Strategy 3: Staggered Expiration**
```csharp
public void SetWithStagger(string key, object data, TimeSpan baseTtl)
{
    // Add random jitter to prevent synchronized expiry
    var jitter = TimeSpan.FromSeconds(Random.Next(0, 300)); // 0-5 min
    var actualTtl = baseTtl + jitter;
    _cache.Set(key, data, actualTtl);
}
```

## Output

```yaml
cache_strategy:
  cache_suitability:
    recommended: <yes|no|conditional>
    reason: <explanation>
    conditions: [<if conditional>]
  
  key_design:
    pattern: <key pattern template>
    examples: [<sample keys>]
    collision_risk: <none|low|medium>
  
  ttl_strategy:
    base_ttl: <duration>
    ttl_type: <fixed|sliding|adaptive>
    reasoning: <why this TTL>
  
  invalidation:
    strategy: <direct|pattern|tag|time>
    trigger_points: [<when to invalidate>]
    code_example: <implementation>
  
  stampede_assessment:
    risk_level: <high|medium|low>
    traffic_estimate: <requests/sec>
    query_cost: <ms>
    mitigation_needed: <yes|no>
    mitigation_strategy: <if needed>
  
  implementation:
    cache_aside: <code example>
    read_through: <code example if applicable>
    write_through: <code example if applicable>
  
  monitoring:
    metrics_to_track: [<list>]
    alert_thresholds: [<conditions>]

confidence: <high|medium|low>
risks: [<identified risks>]
```

## Common Patterns

### Pattern 1: Product Catalog Cache

**Input:**
```yaml
data: "Product catalog (50K products)"
access: "High read, low write"
volume: "~150MB"
update_frequency: "Daily batch + occasional updates"
```

**Output:**
```yaml
strategy:
  key_pattern: "product:{productId}"
  list_pattern: "products:list:{category}:{page}"
  ttl: "4 hours with stagger"
  
invalidation:
  on_update: |
    _cache.Remove($"product:{id}");
    _cache.RemovePattern("products:list:*");
  on_batch: |
    _cache.RemovePattern("product:*");
  
stampede_mitigation:
  needed: yes
  reason: "High traffic, expensive full catalog query"
  approach: "Lock-based refresh for full catalog"
```

### Pattern 2: User Session Data

**Input:**
```yaml
data: "Shopping cart"
access: "User-specific, frequent"
volume: "Small (< 1KB per user)"
update_frequency: "Every add/remove"
```

**Output:**
```yaml
strategy:
  key_pattern: "user:{userId}:cart"
  ttl: "Session duration + 1 hour"
  
invalidation:
  on_add: "Update cache entry"
  on_remove: "Update cache entry"
  on_checkout: "Remove cache entry"
  
stampede: "No risk (user-specific)"
```

### Pattern 3: Computed Report

**Input:**
```yaml
data: "Sales summary report"
access: "Moderate, multiple users"
volume: "Medium (~5MB)"
update_frequency: "Data changes constantly, report daily"
```

**Output:**
```yaml
strategy:
  key_pattern: "report:sales:daily:{date}"
  ttl: "24 hours"
  
invalidation:
  strategy: "Time-based only"
  reasoning: "Daily granularity acceptable, expensive to compute"
  
stampede_mitigation:
  needed: yes
  approach: "Lock-based, compute once daily"
```

## Redis Best Practices

### Memory Management
```yaml
eviction_policy: "allkeys-lru" # Recommended for cache
max_memory: "2GB" # Set appropriate limit
monitor: "memory_usage, eviction_rate"
```

### Serialization
```yaml
format: "JSON" # Human-readable, flexible
alternative: "MessagePack" # Smaller, faster
avoid: "BinaryFormatter" # Security risk
```

### Connection Handling
```yaml
pattern: "Connection multiplexing"
library: "StackExchange.Redis"
pooling: "Single connection, managed by library"
```

## Anti-Patterns to Avoid

### ❌ Anti-Pattern 1: Cache Everything
```csharp
// BAD: Caching user-specific, frequently changing data
_cache.Set($"user:{userId}:notifications", notifications, TimeSpan.FromHours(1));
// Notifications change constantly, cache is always stale
```

### ❌ Anti-Pattern 2: No Invalidation Strategy
```csharp
// BAD: Set and forget
_cache.Set("customers", allCustomers, TimeSpan.FromDays(30));
// 30 days of stale data!
```

### ❌ Anti-Pattern 3: Synchronized Expiry
```csharp
// BAD: All entries expire at same time
foreach (var product in products)
{
    _cache.Set($"product:{product.Id}", product, TimeSpan.FromHours(1));
}
// Stampede when all 50K products expire together
```

## Usage Example

```
SKILL: redis-key-strategy-analyzer

INPUT:
  data_to_cache: "Customer list for dropdown (5000 customers)"
  access_pattern: "Every page load, 100 req/sec"
  data_volume: "~2MB serialized"
  update_frequency: "New customers weekly, updates daily"
  consistency_requirement: "eventual (5-10 min staleness OK)"

OUTPUT:
  cache_strategy:
    cache_suitability:
      recommended: yes
      reason: "High read:write ratio, shared data, tolerate staleness"
    
    key_design:
      pattern: "customers:list:active"
      examples: 
        - "customers:list:active"
        - "customers:list:inactive"
    
    ttl_strategy:
      base_ttl: "10 minutes"
      ttl_type: "fixed with stagger"
      reasoning: "Balance freshness vs database load"
      code: |
        var jitter = TimeSpan.FromSeconds(Random.Next(0, 120));
        _cache.Set(key, data, TimeSpan.FromMinutes(10) + jitter);
    
    invalidation:
      strategy: "direct + time-based"
      trigger_points:
        - "Customer created: Remove customers:list:*"
        - "Customer status changed: Remove customers:list:*"
        - "Otherwise: Let TTL handle"
      code: |
        public void UpdateCustomer(Customer c)
        {
            _repo.Update(c);
            _cache.RemovePattern("customers:list:*");
        }
    
    stampede_assessment:
      risk_level: high
      traffic_estimate: "100 req/sec"
      query_cost: "200ms (5000 rows)"
      mitigation_needed: yes
      mitigation_strategy: "lock-based refresh"
      code: |
        public async Task<List<Customer>> GetActiveCustomers()
        {
            var key = "customers:list:active";
            
            var cached = await _cache.GetAsync<List<Customer>>(key);
            if (cached != null) return cached;
            
            using (await _lock.AcquireAsync($"lock:{key}"))
            {
                cached = await _cache.GetAsync<List<Customer>>(key);
                if (cached != null) return cached;
                
                var customers = await _repo.GetActive();
                await _cache.SetAsync(key, customers, TimeSpan.FromMinutes(10));
                return customers;
            }
        }
    
    monitoring:
      metrics:
        - "cache_hit_rate (target: >90%)"
        - "cache_miss_duration (alert if >500ms)"
        - "eviction_rate (alert if >10/sec)"

  confidence: high
```

## Confidence Levels

**High:** Clear caching benefit, standard pattern
**Medium:** Benefits exist but complexity concerns
**Low:** Unclear benefit or high risk
