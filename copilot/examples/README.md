# Workflow Examples

Complete, detailed examples of autonomous workflow executions.

## Purpose

These examples show complete workflow executions from start to finish, demonstrating:
- How agents process different types of requests
- What skill invocations look like
- How checkpoints are presented
- What the final output contains
- How different execution modes work

## Examples

### Feature Delivery
**File:** `feature-example.md`
**Scenario:** Add Excel export to customer list
**Shows:** Complete 9-stage FEATURE workflow with autonomous execution

### Bug Fix
**File:** `bug-fix-example.md`
**Scenario:** Customer search returns wrong results
**Shows:** Complete 8-stage BUG workflow with root cause analysis

### Hotfix
**File:** `hotfix-example.md`
**Scenario:** Production orders failing 100%
**Shows:** Complete 8-phase HOTFIX workflow with manual mode

### Performance
**File:** `performance-example.md`
**Scenario:** Customer search slow (8+ seconds)
**Shows:** Complete 7-stage PERFORMANCE workflow with optimization

### Spike
**File:** `spike-example.md`
**Scenario:** Can we cache product catalog in Redis?
**Shows:** Complete 4-stage SPIKE workflow with investigation

### Story Refinement
**File:** `story-refinement-example.md`
**Scenario:** "Fix the slow page"
**Shows:** Complete 6-stage REFINEMENT workflow transforming vague request

## How to Use

1. **Learning:** Read examples to understand workflow execution
2. **Reference:** Use as templates for similar scenarios
3. **Comparison:** Compare your outputs against these examples
4. **Training:** Use to train team on autonomous workflow system

## Example Format

Each example includes:
- **Input:** Original user request
- **Mode Detection:** How orchestrator chose the mode
- **Stage-by-Stage:** Complete execution with skill invocations
- **Checkpoints:** How checkpoints are presented (if any)
- **Final Output:** Complete deliverable
- **Metadata:** Execution time, risk, confidence
- **Variations:** How different flags would change execution

---

**See also:**
- Main docs: `copilot/COPILOT_INTEGRATION.md`
- Templates: `copilot/TEMPLATES.md`
- Agents: `copilot/agents/`
