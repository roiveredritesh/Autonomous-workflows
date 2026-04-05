# Autonomous Workflows Framework for GitHub Copilot

## Overview
This framework provides structured workflows, specialized analysis skills, and coding standards for working with GitHub Copilot on an ASP.NET WebForms project.

**Optimized for:** GitHub Copilot in VS Code
**Version:** 2.0.0

---

## Quick Start

1. **Read the main instructions:**
   - Open [`copilot-instructions.md`](copilot-instructions.md)
   - This is your entry point to the entire framework

2. **Review coding standards:**
   - Start with [Minimal Changes Philosophy](instructions/minimal-changes-philosophy.md)
   - Check [Quick Start Guide](instructions/quick-start-guide.md)

3. **Use skills as needed:**
   - Browse [skills catalog](skills/README.md)
   - 28 specialized skills organized by category

4. **Follow agents for complex work:**
   - See [agents/](agents/) for workflow orchestrators
   - 7 agents for different types of work

---

## Folder Structure

```
.github/
├── copilot-instructions.md       ← START HERE
│
├── agents/                        ← Workflow orchestrators
│   ├── feature-delivery.agent.md
│   ├── bug-fix.agent.md
│   ├── hotfix.agent.md
│   ├── performance.agent.md
│   ├── spike.agent.md
│   ├── story-refinement.agent.md
│   └── orchestrator.agent.md
│
├── skills/                        ← Analysis capabilities (28 skills)
│   ├── analysis/                  6 skills
│   ├── planning/                  5 skills
│   ├── generation/                5 skills
│   ├── validation/                4 skills
│   ├── webforms/                  4 skills
│   ├── data/                      4 skills
│   └── README.md                  ← Skills catalog
│
├── instructions/                  ← Coding standards & guides
│   ├── csharp-naming-conventions.md
│   ├── minimal-changes-philosophy.md
│   ├── error-handling-patterns.md
│   ├── webforms-best-practices.md
│   ├── linq-best-practices.md
│   ├── redis-caching-patterns.md
│   ├── quick-start-guide.md
│   ├── integration-overview.md
│   ├── output-templates.md
│   └── best-practices-audit.md
│
├── OUTPUT_STRUCTURE.md            ← Output format specification
└── README.md                      ← This file
```

---

## What's Included

### Workflow Agents (7)
Structured workflows for different types of work:
- **feature-delivery** - New features and enhancements
- **bug-fix** - Defect resolution  
- **hotfix** - Production emergency response
- **performance** - Optimization work
- **spike** - Technical investigations
- **story-refinement** - Requirement clarification
- **orchestrator** - Workflow routing and coordination

### Skills (28 specialized analysis skills)
Organized by category:
- **Analysis** (6) - Code and situation analysis
- **Planning** (5) - Implementation planning
- **Generation** (5) - Artifact generation
- **Validation** (4) - Requirement validation
- **WebForms** (4) - WebForms/Telerik specific
- **Data** (4) - Data access and caching

### Coding Standards
Modular best practices for:
- C# naming conventions
- WebForms page lifecycle
- LINQ query optimization
- Redis caching patterns
- Error handling
- Minimal changes philosophy

---

## How to Use

### Method 1: Direct Coding Standards
For simple code requests:
```
"Add customer export following webforms-best-practices 
and minimal-changes-philosophy"
```

### Method 2: Use Specific Skills
For targeted analysis:
```
"Use linq-query-tracer to analyze this query performance"
```

### Method 3: Follow Workflow Agents
For complex work:
```
"Use feature-delivery agent to analyze adding notifications"
```

---

## Core Principles

1. **Minimal Changes** - Smallest change that works
2. **Follow Patterns** - Reuse existing code patterns
3. **Safety First** - Never break public APIs or lifecycle
4. **No Refactoring** - Unless explicitly requested
5. **Match Standards** - Follow project conventions

---

## Integration with GitHub Copilot

This framework is designed specifically for GitHub Copilot's conversational model:
- No checkpoint mechanisms (Copilot can't pause execution)
- Focus on deliverables, not execution stages
- Clear, actionable instructions
- Modular documentation for easy reference

---

## Getting Help

- **Main instructions:** [copilot-instructions.md](copilot-instructions.md)
- **Quick start:** [instructions/quick-start-guide.md](instructions/quick-start-guide.md)
- **Skills catalog:** [skills/README.md](skills/README.md)
- **Coding standards:** [instructions/](instructions/)

---

## Output Structure

Workflow outputs are saved to `/output/{workflow-title}/`:
- `00-metadata.yaml` - Workflow metadata
- `02-analysis.md` - Analysis outputs
- `03-planning.md` - Implementation planning
- `05-review-summary.md` - Final summary

See [OUTPUT_STRUCTURE.md](OUTPUT_STRUCTURE.md) for details.

---

**Version:** 2.0.0
**Last Updated:** 2026-03-28
**Optimized for:** GitHub Copilot in VS Code
