# Simplified Copilot Integration Guide

## Quick Start

This autonomous workflow framework helps GitHub Copilot provide structured analysis and planning for your ASP.NET WebForms project. It's designed to work conversationally within VS Code.

### What This Framework Does

✅ Provides structured workflows for features, bugs, hotfixes, performance, and investigations
✅ Uses specialized skills to analyze WebForms, Telerik, LINQ, caching, and database impacts
✅ Ensures minimal code changes following existing patterns
✅ Generates implementation plans with risk assessments

### What This Framework Does NOT Do

❌ Execute code automatically
❌ Pause mid-execution for approval (Copilot is conversational, not interactive)
❌ Deploy or commit changes
❌ Monitor production systems

---

## How to Use

### 1. Request Analysis

Ask Copilot to analyze your requirement:

```
"Analyze adding Excel export to the customer list page"
```

Copilot will:
1. Validate the requirement
2. Analyze feasibility and WebForms compatibility
3. Check Telerik, LINQ, and cache impacts
4. Assess risk and complexity
5. Present complete analysis

### 2. Request Implementation Plan

If analysis looks good, request the plan:

```
"Create implementation plan for the Excel export"
```

Copilot will:
1. Design minimal code changes
2. Identify exact files and methods to modify
3. Create test scenarios
4. Generate rollback plan

### 3. Review and Adjust

Review the plan, then:
- Request adjustments: "Change to use CSV instead of Excel"
- Get more details: "Show the exact code for ExportToExcel method"
- Proceed with implementation: "Implement the changes"

---

## Workflow Types

### Feature Delivery
**Keywords:** add, create, implement, new
**Use when:** Building new functionality

**Example:**
```
"Add Excel export button to CustomerList.aspx"
```

**Copilot will:**
- Validate requirements
- Analyze WebForms/Telerik impact
- Plan minimal changes (2 files, ~40 lines)
- Create test scenarios
- Generate rollback plan

---

### Bug Fix
**Keywords:** fix, bug, broken, error, wrong results
**Use when:** Something isn't working correctly

**Example:**
```
"Customer search returns wrong results when filter is applied"
```

**Copilot will:**
- Classify severity
- Investigate root cause
- Plan minimal fix (no refactoring)
- Identify regression risks
- Create test scenarios

---

### Hotfix (Production Issues)
**Keywords:** production, critical, urgent, down
**Use when:** Production system is degraded or failing

**Example:**
```
"Orders are failing in production - all users affected"
```

**Copilot will:**
- Assess production impact
- Recommend immediate mitigation
- Evaluate fix strategies (rollback, config, code patch)
- Create deployment and rollback plans

---

### Performance Optimization
**Keywords:** slow, performance, optimize, timeout
**Use when:** Something is too slow

**Example:**
```
"Customer search takes 8 seconds - need to optimize"
```

**Copilot will:**
- Profile current performance
- Analyze LINQ queries and SQL
- Identify bottlenecks
- Recommend caching strategy
- Plan optimizations with measurements

---

### Spike (Investigation)
**Keywords:** investigate, explore, why, research, can we
**Use when:** Need to research or investigate something

**Example:**
```
"Can we cache the product catalog in Redis?"
```

**Copilot will:**
- Frame research question
- Create investigation plan
- Identify what to test
- Document findings
- Recommend next steps

---

### Story Refinement
**Use when:** Requirement is vague or incomplete

**Example:**
```
"Fix the slow page"
```

**Copilot will:**
- Identify missing information
- Extract requirements
- Clarify scope
- Generate acceptance criteria
- Route to appropriate workflow

---

## Skills Reference

Skills are organized by category in `skills/{category}/{skill-name}/Skill.md`

### Analysis Skills
- `story-analyzer` - Examines story state and gaps
- `bug-classifier` - Classifies bugs by severity
- `bug-impact-analyzer` - Assesses bug scope
- `production-impact-assessor` - Evaluates production incidents
- `feature-feasibility-analyzer` - Evaluates technical feasibility
- `performance-profiler` - Establishes performance baselines

### Planning Skills
- `minimal-diff-planner` - Plans minimal code changes
- `minimal-fix-planner` - Plans minimal bug fixes
- `emergency-mitigation-planner` - Plans incident mitigation
- `hotfix-strategy-planner` - Determines fix strategy
- `spike-charter` - Creates research investigations

### Generation Skills
- `acceptance-criteria-generator` - Creates testable criteria
- `acceptance-criteria-expander` - Expands with edge cases
- `test-scenario-generator` - Creates test scenarios
- `rollback-plan-generator` - Creates rollback procedures
- `spike-findings-recorder` - Documents investigation findings

### Validation Skills
- `requirement-extractor` - Extracts requirements
- `edge-case-detector` - Identifies boundary conditions
- `safe-change-boundary-detector` - Identifies safe modification points
- `jira-story-intake` - Validates tickets

### WebForms Skills
- `webforms-lifecycle-analyzer` - Analyzes page lifecycle impact
- `webforms-regression-analyzer` - Identifies regression risks
- `telerik-behavior-analyzer` - Analyzes Telerik control behavior
- `telerik-impact-checker` - Validates Telerik compatibility

### Data Skills
- `linq-query-tracer` - Analyzes LINQ efficiency
- `sql-impact-analyzer` - Evaluates database changes
- `redis-cache-strategy-analyzer` - Analyzes caching strategies
- `cache-invalidation-mapper` - Maps cache invalidation

---

## Coding Standards

See `copilot-instructions.md` for complete C# coding standards including:
- Naming conventions (PascalCase classes, camelCase variables)
- WebForms lifecycle patterns
- Telerik control guidelines
- LINQ query best practices
- Redis caching patterns
- Error handling
- Performance guidelines

**Key principle:** Minimal changes, follow existing patterns, no refactoring.

---

## Example Conversation

**You:**
```
Add Excel export to the customer list page
```

**Copilot:**
```
I'll analyze adding Excel export functionality to the customer list.

STAGE 1: INTAKE
✓ Requirement: Add Excel export to CustomerList.aspx
✓ Feature type: Data export
✓ Scope: CustomerList page only

STAGE 2-3: ANALYSIS
✓ Feasibility: HIGH - EPPlus library already in project
✓ WebForms compatible: Yes - server-side button event
✓ Telerik: No Telerik control changes needed
✓ Data: Reuse existing customer query
✓ Cache: No cache strategy needed for export
✓ Risk: LOW

📋 ANALYSIS COMPLETE

Ready to proceed with implementation plan?
```

**You:**
```
Yes, create the implementation plan
```

**Copilot:**
```
IMPLEMENTATION PLAN

Files to modify: 2
Lines changed: ~40
Pattern: Follow existing "Export to PDF" pattern

FILE 1: CustomerList.aspx
+ Add export button to toolbar (line 45)
  <asp:Button ID="btnExportExcel" runat="server"
      Text="Export to Excel" OnClick="btnExportExcel_Click" />

FILE 2: CustomerList.aspx.cs
+ Add button click handler (after btnExportPdf_Click)
  protected void btnExportExcel_Click(object sender, EventArgs e)
  {
      var customers = GetFilteredCustomers();
      ExportToExcel(customers, "Customers.xlsx");
  }

+ Add export method (follows ExportToPdf pattern)
  private void ExportToExcel(List<Customer> customers, string filename)
  {
      using (var package = new ExcelPackage())
      {
          var worksheet = package.Workbook.Worksheets.Add("Customers");

          // Headers (row 1)
          worksheet.Cells[1, 1].Value = "Customer ID";
          worksheet.Cells[1, 2].Value = "Name";
          worksheet.Cells[1, 3].Value = "Email";
          worksheet.Cells[1, 4].Value = "Status";

          // Data (rows 2+)
          for (int i = 0; i < customers.Count; i++)
          {
              worksheet.Cells[i + 2, 1].Value = customers[i].Id;
              worksheet.Cells[i + 2, 2].Value = customers[i].Name;
              worksheet.Cells[i + 2, 3].Value = customers[i].Email;
              worksheet.Cells[i + 2, 4].Value = customers[i].Status;
          }

          // Download
          Response.Clear();
          Response.ContentType = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet";
          Response.AddHeader("content-disposition", $"attachment; filename={filename}");
          Response.BinaryWrite(package.GetAsByteArray());
          Response.End();
      }
  }

TEST SCENARIOS:
1. Export with active filters (verify only filtered results exported)
2. Export all customers (verify all fields included)
3. Export empty result set (verify headers-only file or friendly message)
4. Export large dataset (10,000 rows - verify memory usage)

ROLLBACK PLAN:
- Simple file revert (2 files modified)
- No database changes
- No cache changes
- Rollback time: < 5 minutes

RISK: LOW
CONFIDENCE: HIGH
READY FOR IMPLEMENTATION
```

**You:**
```
Implement the changes
```

*Copilot generates the actual code...*

---

## Tips for Best Results

### ✅ DO:
- Be specific about what page/feature you're working with
- Mention if it's production critical
- Provide error messages or symptoms for bugs
- Ask for analysis before implementation
- Request test scenarios
- Review generated code carefully

### ❌ DON'T:
- Ask for broad refactoring ("make it better")
- Expect Copilot to execute code automatically
- Assume Copilot knows your exact project structure (tell it!)
- Skip the analysis phase for complex changes
- Deploy without testing

---

## Folder Structure

```
.github/
├── agents/                    # Workflow orchestration
│   ├── orchestrator.agent.md
│   ├── feature-delivery.agent.md
│   ├── bug-fix.agent.md
│   ├── hotfix.agent.md
│   ├── performance.agent.md
│   ├── spike.agent.md
│   └── story-refinement.agent.md
│
├── skills/                    # Specialized analysis skills
│   ├── analysis/
│   ├── planning/
│   ├── generation/
│   ├── validation/
│   ├── webforms/
│   └── data/
│
├── instructions/
│   ├── quick-start-guide.md   # This file
│   ├── output-templates.md    # Output templates
│   └── integration-overview.md
│
├── specs/                     # Archived formal rules
└── README.md                  # Full documentation

copilot-instructions.md        # C# coding standards (project root)
```

---

## Troubleshooting

**Q: Copilot isn't following the workflow structure**
A: Explicitly reference the agent: "Use the feature-delivery agent workflow to analyze..."

**Q: Analysis is too high-level**
A: Request specific skills: "Use linq-query-tracer to analyze the query performance"

**Q: Plan includes refactoring I didn't ask for**
A: Emphasize minimal changes: "Create minimal fix - no refactoring"

**Q: Need to investigate something first**
A: Switch to spike mode: "Create a spike to investigate [specific question]"

**Q: Copilot stops mid-analysis**
A: Continue: "Continue with the remaining stages" or "Proceed to implementation planning"

---

## Integration with copilot-instructions.md

The `copilot-instructions.md` file contains C# coding standards. Use it alongside this workflow guide:

**For analysis and planning:**
→ Use this guide (quick-start-guide.md)
→ Reference appropriate workflow and skills

**For actual coding:**
→ Use coding standards (copilot-instructions.md)
→ Follow naming conventions, patterns, and safety rules

**Example:**
```
"Analyze adding Excel export [use feature-delivery workflow]
Then implement following the C# standards in copilot-instructions.md"
```

---

## Quick Reference

**Feature:** `"Add [functionality] to [page/component]"`
**Bug:** `"Fix [problem] in [location]"`
**Hotfix:** `"[Problem] in production - [users affected]"`
**Performance:** `"[Component] is slow - [current time] needs [target time]"`
**Spike:** `"Investigate [question/approach]"`
**Refinement:** `"Clarify requirements for [vague request]"`

**See full skills list:** `skills/README.md`
**See coding standards:** `copilot-instructions.md`
**See templates:** `instructions/output-templates.md`

---

**Last Updated:** 2026-03-28
