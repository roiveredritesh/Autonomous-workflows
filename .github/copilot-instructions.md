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
**Location:** `agents/` - 8 workflow orchestrators

- `feature-delivery` - New feature implementation
- `bug-fix` - Defect resolution
- `hotfix` - Production emergencies
- `performance` - Optimization work
- `spike` - Technical investigations
- `story-refinement` - Requirement clarification
- `orchestrator` - Workflow routing
- `sdd-master` - **Spec-Driven Development: full 7-step lifecycle** (analysis → planning → coding → browser testing → summary)

**SDD Phase Agents** (invoked in sequence by `sdd-master`):
**Location:** `sdd/` - 5 phase-specific agents with per-phase model assignment

- `sdd/phase-1-analysis` - Steps 1+2: Requirements & Story Refinement [Claude Sonnet]
- `sdd/phase-2-planning` - Step 3: Code Planning [Claude Sonnet]
- `sdd/phase-3-execution` - Step 4: Code Execution [Claude Sonnet]
- `sdd/phase-4-testing` - Steps 5+6: Browser Testing & Defect Fixes [Claude Haiku]
- `sdd/phase-5-summary` - Step 7: Final Summary [Claude Haiku]

**See:** [agents/](agents/) folder for agent definitions

### Auto-Agent Selection (MANDATORY)
Before responding to ANY request involving bugs, features, performance, analysis, or requirement refinement — even if the user does NOT name an agent:

1. Identify the applicable agent from the table below based on request type.
2. Read that agent file from `agents/`.
3. Read every skill listed in the agent's `Skills used by this agent` section.
4. Only then begin analysis, planning, or implementation.

| Request type | Auto-select agent |
|---|---|
| Bug report, error, fix | `bug-fix` |
| New feature, story | `feature-delivery` |
| Production emergency | `hotfix` |
| Slow query, performance | `performance` |
| Uncertainty, investigation | `spike` |
| Requirements, acceptance criteria | `story-refinement` |
| Unclear / multiple types | `orchestrator` |
| `sdd`, `spec-driven`, `full lifecycle`, `end-to-end`, `7-step` | `sdd-master` |

Skipping this step is **non-compliant** regardless of request simplicity or whether the user names an agent.

---

### Mandatory Agent Compliance
When a user explicitly selects, references, or asks to use a custom agent, treat that choice as a required workflow contract.

Required behavior:
1. Read the selected agent file before doing substantive analysis, planning, refinement, or implementation.
2. Read every skill file listed in the agent's `Skills used by this agent` section before continuing.
3. Do not substitute an informal/manual workflow for the agent workflow without stating that explicitly to the user.
4. If any referenced skill file cannot be found or loaded, stop and tell the user which file is missing before proceeding.
5. Structure the work according to the phases and output expectations defined by that agent.
6. **For EVERY skill applied, produce its structured output block in the response** — YAML or formatted section as defined in the skill's Output Format. Do not summarize or paraphrase. Show the actual output.
7. In the response, explicitly confirm active agent name, loaded skill names, and whether execution is fully compliant.

Minimum execution trace example:
```
Active agent: story-refinement
Loaded skills: story-analyzer, requirement-extractor, acceptance-criteria-generator, edge-case-detector
Workflow compliance: FULL
```

Non-compliance rule:
- If the agent file was read but the referenced skills were not loaded, do not claim the agent workflow was followed.
- In that case, explicitly state that only a partial/manual workflow was performed.

---

### Skill Output Requirement (MANDATORY)
Every skill applied MUST produce its structured output inline in the response, exactly as defined in that skill's `SKILL.md` Output Format section. Do not summarize, paraphrase, or omit.

Rules:
- If the skill defines a YAML output block → show that YAML block
- If the skill defines a formatted section → show that section
- If no output format is defined → show a clearly labelled findings section
- A skill with no output block in the response was **read, not applied**

This applies to every skill in every agent workflow, present and future.

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
├── agents/                      ← Workflow orchestrators (including sdd-master)
├── sdd/                         ← SDD phase agents (phase-1 through phase-5)
├── skills/                      ← Analysis capabilities
├── instructions/                ← Coding standards & guides
├── OUTPUT_STRUCTURE.md          ← Output format spec
└── README.md                    ← Framework overview
```

---

**Framework Version:** 2.1.0
**Last Updated:** 2026-04-04
**Optimized for:** GitHub Copilot in VS Code
