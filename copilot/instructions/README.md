# Instructions Directory

## Overview
Modular coding standards and best practices for working with this ASP.NET WebForms project using GitHub Copilot.

## Available Instructions

### Core Standards
- **[csharp-naming-conventions.md](csharp-naming-conventions.md)** - Classes, methods, variables, properties, constants
- **[minimal-changes-philosophy.md](minimal-changes-philosophy.md)** - Core principle: make the smallest change that works
- **[error-handling-patterns.md](error-handling-patterns.md)** - Validation, null checking, exceptions, transactions

### Technology-Specific
- **[webforms-best-practices.md](webforms-best-practices.md)** - Page lifecycle, ViewState, Telerik controls
- **[linq-best-practices.md](linq-best-practices.md)** - Query efficiency, projections, N+1 problems, pagination
- **[redis-caching-patterns.md](redis-caching-patterns.md)** - Key naming, cache-aside pattern, invalidation, TTL

## How to Use

### With GitHub Copilot
Reference specific guides when requesting code:

```
"Add customer export following minimal-changes-philosophy
and webforms-best-practices"
```

```
"Optimize this query following linq-best-practices"
```

```
"Add caching following redis-caching-patterns"
```

### As a Developer
- Start with **minimal-changes-philosophy.md** - understand the core approach
- Check **csharp-naming-conventions.md** for naming rules
- Reference technology-specific guides as needed

## Quick Reference

**Before writing code:**
1. What's the minimal change needed?
2. Is there existing code I can copy?
3. Am I following the project's naming conventions?
4. Have I handled errors appropriately?

**For WebForms:**
- Respect page lifecycle
- Keep ViewState enabled for Telerik controls
- Never change control IDs

**For Data Access:**
- Filter in database, not memory
- Use Include() for related data
- Paginate at database level

**For Caching:**
- Use consistent key patterns
- Invalidate on updates
- Set appropriate TTL

## Main Reference

See root-level **copilot-instructions.md** for quick reference to all standards.

---

**Last Updated:** 2026-03-28
