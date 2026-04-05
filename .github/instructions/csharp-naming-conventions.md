# C# Naming Conventions

## Classes and Interfaces
```csharp
// ✅ PascalCase for classes
public class CustomerRepository { }
public interface ICustomerService { }

// ❌ Don't use camelCase or snake_case
public class customerRepository { }
```

## Methods
```csharp
// ✅ PascalCase for all methods (public and private)
public void ProcessOrder() { }
private void ValidateInput() { }
```

## Variables and Parameters
```csharp
// ✅ camelCase for local variables and parameters
var customerName = "John";
int orderCount = 10;
```

## Properties
```csharp
// ✅ PascalCase for properties
public string CustomerName { get; set; }
public int OrderId { get; set; }
```

## Fields
```csharp
// ✅ _camelCase for private fields (match existing pattern)
private readonly ICustomerRepository _customerRepository;
private string _cachedValue;

// ❌ Don't use Hungarian notation
private string strCustomerName; // BAD
```

## Constants
```csharp
// ✅ PascalCase or UPPER_CASE (match existing file pattern)
private const int MaxRetries = 3;
private const string DEFAULT_CACHE_KEY = "customers:all";
```

**Rule:** Always match the naming convention used in the file you're editing.
