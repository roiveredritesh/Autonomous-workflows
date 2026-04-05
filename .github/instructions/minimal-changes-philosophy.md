# Minimal Changes Philosophy

> "The best code is no code. The second best is boring code that works."

## Core Principles

### 1. Make the Smallest Change
- ✅ Modify only what's necessary to solve the problem
- ✅ Follow existing patterns - don't create new ones
- ❌ Don't refactor code "while you're in there"
- ❌ Don't add "improvements" outside the scope

### 2. Pattern Reuse
```csharp
// ✅ Find similar existing code and copy its pattern
// If there's already an "Export to PDF" button, copy that pattern for "Export to Excel"

// ❌ Don't create new patterns or abstractions
// If the codebase uses manual SQL, don't introduce a query builder library
```

### 3. No Refactoring Unless Asked
- ✅ Preserve existing code structure and style
- ✅ Match indentation, naming, and formatting
- ❌ Don't rename variables for "clarity"
- ❌ Don't extract methods unless necessary
- ❌ Don't "clean up" surrounding code

### 4. No Premature Optimization
- ✅ Make it work first, optimize only if needed
- ❌ Don't optimize without measurements
- ❌ Don't add caching "just in case"
- ❌ Don't create abstractions for future needs

## Examples

### ✅ Good: Minimal Change
```csharp
// Adding export feature - copy existing PDF export pattern
protected void btnExportExcel_Click(object sender, EventArgs e)
{
    var customers = GetFilteredCustomers(); // Reuse existing method
    ExportToExcel(customers, "Customers.xlsx");
}
```

### ❌ Bad: Over-Engineering
```csharp
// Don't create new abstractions unnecessarily
public interface IExportStrategy { }
public class ExcelExportStrategy : IExportStrategy { }
public class ExportFactory { }
// Just add a simple export method!
```

### ✅ Good: Follow Existing Patterns
```csharp
// File already has 5 methods named like "GetCustomerById"
public Customer GetOrderById(int id) // Follow the pattern
{
    return _repository.GetById(id);
}
```

### ❌ Bad: Introduce New Patterns
```csharp
// Don't change naming conventions mid-file
public async Task<Customer> RetrieveCustomerAsync(int id) // Different pattern!
{
    return await _repository.FindByIdAsync(id);
}
```

## Red Flags (Avoid These)

❌ "While I'm here, let me refactor..."
❌ "This could be more DRY..."
❌ "Let me extract this into a helper..."
❌ "I'll add error handling for all edge cases..."
❌ "This should really use dependency injection..."

## Quick Checklist

Before making any change, ask:
1. ✅ Is this change absolutely necessary?
2. ✅ Am I following existing patterns?
3. ✅ Am I touching only what's needed?
4. ✅ Would someone reviewing this see a focused, clear change?
5. ❌ Am I refactoring or "improving" unrelated code?

**Remember:** Code that works is better than code that's "perfect".
