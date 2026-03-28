# C# Project Standards for GitHub Copilot

## Project: Legacy ASP.NET WebForms
Technology stack: WebForms, Telerik controls, Entity Framework, Redis caching, SQL Server

## Core Philosophy
**Minimal changes:** Make the smallest change that works. Follow existing patterns. No refactoring unless requested.

## Quick Reference

### Coding Standards
- **Naming:** `copilot/instructions/csharp-naming-conventions.md`
- **WebForms:** `copilot/instructions/webforms-best-practices.md`
- **LINQ & EF:** `copilot/instructions/linq-best-practices.md`
- **Redis Caching:** `copilot/instructions/redis-caching-patterns.md`
- **Error Handling:** `copilot/instructions/error-handling-patterns.md`
- **Minimal Changes:** `copilot/instructions/minimal-changes-philosophy.md`

### Workflow Integration
- **Quick Start:** `copilot/SIMPLIFIED_INTEGRATION.md`
- **Skills Catalog:** `copilot/skills/README.md`
- **Agents:** `copilot/agents/`

## Critical Rules
1. Never break public APIs
2. Respect WebForms lifecycle
3. Keep ViewState enabled for Telerik controls
4. Filter in database, not memory
5. Always validate user input
6. Never swallow exceptions
7. Match existing patterns - don't create new ones

---

**Last Updated:** 2026-03-28
