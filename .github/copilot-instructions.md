# GitHub Copilot Instructions for ASP.NET WebForms Project

## Project Context
Legacy ASP.NET WebForms application with Telerik UI, Entity Framework, Redis caching, SQL Server.

## Core Philosophy
**Minimal changes:** Make the smallest change that works. Follow existing patterns. No refactoring unless requested.

---

## Quick Reference Guides

### Coding Standards
- **[Naming Conventions](instructions/csharp-naming-conventions.md)** - Classes, methods, variables, properties
- **[Minimal Changes Philosophy](instructions/minimal-changes-philosophy.md)** - Core principle (read this first!)
- **[Error Handling](instructions/error-handling-patterns.md)** - Validation, null checks, exceptions
- **[WebForms Best Practices](instructions/webforms-best-practices.md)** - Lifecycle, ViewState, Telerik
- **[LINQ Best Practices](instructions/linq-best-practices.md)** - Query efficiency, N+1 problems
- **[Redis Caching](instructions/redis-caching-patterns.md)** - Key naming, invalidation patterns

### Integration & Workflow
- **[Quick Start Guide](instructions/quick-start-guide.md)** - Get started in 5 minutes
- **[Integration Overview](instructions/integration-overview.md)** - Complete framework overview
- **[Output Templates](instructions/output-templates.md)** - Standard output formats

### Advanced
- **[Best Practices Audit](instructions/best-practices-audit.md)** - Comprehensive audit checklist
- **[Integration Quickstart](instructions/integration-quickstart.md)** - Detailed integration steps

---

## Autonomous Workflow Framework

### Skills Catalog
**Location:** `skills/` - 28 specialized analysis skills organized by category

**Categories:**
- `analysis/` - 6 skills for code/situation analysis
- `planning/` - 5 skills for implementation planning
- `generation/` - 5 skills for generating artifacts
- `validation/` - 4 skills for requirement validation
- `webforms/` - 4 skills for WebForms/Telerik specific
- `data/` - 4 skills for data access and caching

**See:** [skills/README.md](skills/README.md) for complete catalog

### Workflow Agents
**Location:** `agents/` - 7 workflow orchestrators

- `feature-delivery` - New feature implementation
- `bug-fix` - Defect resolution
- `hotfix` - Production emergencies
- `performance` - Optimization work
- `spike` - Technical investigations
- `story-refinement` - Requirement clarification
- `orchestrator` - Workflow routing

**See:** [agents/](agents/) folder for agent definitions

---

## Critical Rules

1. **Never break public APIs** - Existing method signatures are contracts
2. **Respect WebForms lifecycle** - PreInit → Init → Load → Events → PreRender → Render
3. **Keep ViewState enabled for Telerik** - Required for control functionality
4. **Filter in database, not memory** - Use `.Where()` before `.ToList()`
5. **Always validate user input** - Never trust external data
6. **Never swallow exceptions** - Always log or handle properly
7. **Match existing patterns** - Don't create new abstractions

---

## How to Use This Framework

### For Simple Code Requests:
```
"Add Excel export button following webforms-best-practices
and minimal-changes-philosophy"
```
→ Copilot applies coding standards directly

### For Complex Analysis:
```
"Use feature-delivery agent to analyze adding real-time notifications"
```
→ Copilot follows workflow structure with skills

### For Specific Skills:
```
"Use linq-query-tracer to analyze the customer search query"
```
→ Copilot applies that specific skill

---

## Output Structure

Workflow outputs are saved to `/output/{title}/` with:
- `00-metadata.yaml` - Workflow metadata
- `02-analysis.md` - Analysis phase outputs
- `03-planning.md` - Implementation planning
- `05-review-summary.md` - Final summary

**See:** [OUTPUT_STRUCTURE.md](OUTPUT_STRUCTURE.md) for details

---

## Getting Started

1. **Read:** [Minimal Changes Philosophy](instructions/minimal-changes-philosophy.md)
2. **Review:** [Quick Start Guide](instructions/quick-start-guide.md)
3. **Reference:** [Skills Catalog](skills/README.md) as needed
4. **Apply:** Coding standards from [instructions/](instructions/)

---

## File Structure
```
.github/
├── copilot-instructions.md     ← You are here
├── agents/                      ← Workflow orchestrators
├── skills/                      ← Analysis capabilities
├── instructions/                ← Coding standards & guides
├── OUTPUT_STRUCTURE.md          ← Output format spec
└── README.md                    ← Framework overview
```

---

**Framework Version:** 2.0.0
**Last Updated:** 2026-03-28
**Optimized for:** GitHub Copilot in VS Code
