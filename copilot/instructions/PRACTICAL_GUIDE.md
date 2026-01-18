# Autonomous Execution - Practical Guide

## How to Use the System

This guide shows you **exactly how to interact** with the autonomous delivery system.

---

## Quick Start

### Scenario 1: "I just want it done fast and safe"

**Use:** Default autonomous mode (no flags)

```
You: "Add Excel export to customer list"

System: [30-60 seconds later]

========================================
MODE: FEATURE
EXECUTION: Autonomous
TIME: 47 seconds

✅ ANALYSIS COMPLETE (Stages 1-5)

Requirements:
- Export button on customer list page
- Excel format (.xlsx)
- All visible columns included
- Respects current filters
- Max 10,000 rows
- Error handling for timeout

Feasibility: HIGH
Risk: LOW
Complexity: MEDIUM

Legacy Impact:
- CustomerList.aspx: Add toolbar button
- Page_Load: Check !IsPostBack
- No ViewState issues
- No Telerik changes needed

Data/Cache: No cache needed, reuse existing query

✅ PLAN COMPLETE (Stages 6-9)

Implementation:
- 2 files modified
- ~40 lines added
- Uses existing EPPlus library
- Follows InvoiceList export pattern

Tests: 8 scenarios generated
Documentation: Complete
Rollback: Simple file revert

READY FOR: Implementation
========================================

What would you like to do?
[ ] Implement this plan
[ ] Adjust something
[ ] See more details
```

**That's it.** Full analysis and plan in under a minute.

---

### Scenario 2: "I want to review before committing to implementation"

**Use:** Checkpoint flag

```
You: "Add Excel export to customer list"
Flags:
  approve_before_stage: [6]

System: [30 seconds later]

========================================
CHECKPOINT: Analysis Complete

✅ STAGES 1-5 COMPLETED

[All analysis results shown above]

RECOMMENDATION: Proceed with implementation planning
RISK: LOW
CONFIDENCE: HIGH

DECISION REQUIRED:
Analysis looks good. Proceed to create implementation plan?

[ ] Approve - Continue to stages 6-9
[ ] Adjust - Change something
[ ] Spike - Need more investigation
========================================

You: "Approve"

System: [20 seconds later]

========================================
✅ PLANNING COMPLETE (Stages 6-9)

[Implementation plan, tests, docs, rollback]

READY FOR: Implementation
========================================
```

**Total time:** 50 seconds + your review time

---

### Scenario 3: "This seems risky, pause if things look dangerous"

**Use:** Risk threshold flag

```
You: "Optimize the customer search query - it's taking 30 seconds"
Flags:
  approve_at_risk: medium

System: [Analyzing...]

========================================
⚠️ CHECKPOINT: Risk Threshold Reached

STAGES 1-4 COMPLETED:

Root Cause Found:
- N+1 query pattern detected
- Loading all 50,000 customers then filtering
- Missing index on Status column
- Full table scan on every search

RISK: MEDIUM
Factors:
- Large table (50K+ rows)
- High traffic endpoint (100 req/sec)
- Index change required (DDL operation)

MITIGATION:
Option A: Add index (LOW risk implementation)
  - CREATE INDEX on Customers.Status
  - 30-second deployment
  - 95% performance improvement

Option B: Rewrite query (MEDIUM risk)
  - Change LINQ to stored proc
  - Larger code change
  - 98% performance improvement

RECOMMENDATION: Option A (index)

DECISION REQUIRED:
Risk is MEDIUM. Review and approve to continue?

[ ] Approve Option A
[ ] Approve Option B  
[ ] Need more analysis (SPIKE)
========================================
```

**System stopped automatically** because risk hit your threshold.

---

### Scenario 4: "I want full control over every step"

**Use:** Manual mode flag

```
You: "Add Excel export to customer list"
Flags:
  manual_mode: true

System:
========================================
STAGE 1: Intake Complete

Ticket: PROJ-1234
Summary: Add Excel export to customer list
Status: Ready

Continue to Stage 2 (Requirements)?
========================================

You: "Yes"

System:
========================================
STAGE 2: Requirements Complete

Acceptance Criteria:
[Criteria listed]

Continue to Stage 3 (Feasibility)?
========================================

[Repeat for stages 3-9]
```

**You approve each stage.** Slow but maximum control.

---

## Flag Reference Card

Keep this handy:

### No Flags (Default)
```
Request: "Add feature X"
Result: Complete plan in 30-60 seconds
When: You trust the system, low-risk work
```

### Checkpoint Before Implementation
```
Request: "Add feature X"
Flags:
  approve_before_stage: [6]

Result: Review after analysis, approve planning
When: Want to verify approach before committing
```

### Risk-Based Checkpoints
```
Request: "Optimize X"
Flags:
  approve_at_risk: medium

Result: Stops if risk is medium or higher
When: Uncertain about complexity/risk
```

### Skill-Specific Gates
```
Request: "Add caching for X"
Flags:
  approve_before_skills: [redis-cache-strategy-analyzer]

Result: Review before making cache decisions
When: Cache strategy is critical to review
```

### Manual Mode
```
Request: "Add feature X"
Flags:
  manual_mode: true

Result: Approve each of 9 stages individually
When: Learning, training, or very high stakes
```

### Combined Flags
```
Request: "Optimize X"
Flags:
  approve_at_risk: medium
  approve_before_stage: [6, 9]

Result: Multiple checkpoints based on conditions
When: High-stakes work needing multiple reviews
```

---

## Common Workflows

### New Feature (Low Risk)

```
You: "Add print button to invoice page"

System: [35 seconds]
✅ Complete plan
Risk: LOW
Confidence: HIGH
Ready: Yes

You: "Implement"
```

**Total time:** 35 seconds

---

### New Feature (Want Review)

```
You: "Add payment integration with Stripe"
Flags:
  approve_before_stage: [6]

System: [40 seconds]
⏸️ CHECKPOINT
Analysis complete, looks HIGH complexity

You: [Review] "Approved"

System: [30 seconds]
✅ Complete plan

You: "Implement"
```

**Total time:** 70 seconds + review

---

### Bug Fix (Unclear)

```
You: "Customer search returns wrong results sometimes"

System: [20 seconds]
⚠️ LOW CONFIDENCE
Need more information for root cause

SWITCHING TO: Refinement Mode

Questions:
1. Which specific searches fail?
2. What results are wrong?
3. How often ("sometimes")?

You: [Provide details]

System: [Refinement complete]
Now switching to Bug Fix mode

System: [30 seconds]
✅ Root cause: LINQ filter applied after ToList()
Fix: Move Where() before ToList()
```

**System automatically escalated** to get clarity.

---

### Performance Issue (Risky)

```
You: "Order processing is slow, need optimization"
Flags:
  approve_at_risk: medium

System: [45 seconds]
⚠️ MEDIUM RISK DETECTED

Found: Database deadlocks under load
Requires: Transaction isolation changes
Impact: All order operations

CHECKPOINT: Review required

You: "Let's spike this first"

System: Switching to SPIKE mode
Time box: 4 hours
Question: Can we safely change isolation level?
```

**Smart escalation** to investigation.

---

### Production Emergency

```
You: "Orders failing to submit - 100% failure rate"
[No flags needed - HOTFIX mode auto-detects]

System: [15 seconds]
MODE: HOTFIX (auto-detected)
Urgency: CRITICAL

Recent Change Detected:
- Deployment 2 hours ago
- New validation code

RECOMMENDATION: ROLLBACK
- Safest option
- Fastest resolution
- Returns to known good

⏸️ CHECKPOINT (automatic for HOTFIX)
Approve rollback?

You: "Approved"

System:
Rollback procedure:
1. Revert deployment
2. Restart app pool
3. Verify orders working

Time: ~5 minutes
```

**Automatic checkpoint for safety** even in HOTFIX.

---

## Decision Response Guide

At checkpoints, you can respond with:

### Approve
```
"Approve"
"Yes"
"Continue"
"Proceed"
"Go ahead"
```
→ System continues execution

### Adjust
```
"Adjust: Use 1-hour TTL instead of 4-hour"
"Change: Skip caching, use direct query"
"Modify: Add validation before export"
```
→ System adjusts approach, re-runs affected stages

### Spike
```
"Spike"
"Need more investigation"
"Let's test this first"
"Investigate: Can we use async here?"
```
→ System switches to SPIKE mode, time-boxes investigation

### Reject
```
"Reject"
"Stop"
"Different approach needed"
"This won't work"
```
→ System stops, preserves analysis, explains why

---

## Tips for Best Results

### ✅ Do This

**For Low-Risk Work:**
- Use default (no flags)
- Let system run autonomous
- Review output, then implement

**For Learning:**
- Use `approve_before_stage: [6]`
- Review analysis, approve planning
- Builds confidence in system

**For High-Risk:**
- Use `approve_at_risk: medium`
- System stops when risk detected
- You review and decide

**For Unclear Requests:**
- Just ask naturally
- System will escalate to refinement
- Get clarity, then proceed

### ❌ Don't Do This

**Don't micro-manage:**
```
# BAD
Flags:
  approve_before_stage: [1,2,3,4,5,6,7,8,9]
  
# Just use manual_mode: true instead
```

**Don't skip safety:**
```
# BAD (hypothetical - system won't allow)
flags:
  skip_safety_checks: true
  
# Safety checks are NON-NEGOTIABLE
```

**Don't fight the system:**
```
# If system says HIGH risk, don't force it
# Either approve with understanding, or spike it
```

---

## Troubleshooting

### "System stopped for no reason"

**Likely:** Safety violation detected

**Action:**
- Read the violation message
- Understand the issue
- Either adjust approach or justify override

### "Too many checkpoints"

**Likely:** Risk threshold too low

**Action:**
```
# Change from:
approve_at_risk: low

# To:
approve_at_risk: medium
```

### "Not enough checkpoints"

**Likely:** Using default autonomous

**Action:**
```
# Add:
approve_before_stage: [6]  # Before implementation

# Or:
approve_at_risk: medium  # On medium+ risk
```

### "System wants more info"

**Likely:** Requirements unclear

**Action:**
- System escalated to refinement (good!)
- Answer the questions
- System will continue automatically

---

## Real-World Examples

### Example 1: Simple Feature

```
Request: "Add sort by date to orders table"

Time: 32 seconds
Checkpoints: 0 (low risk)
Output: Complete plan

Developer action: Implement
```

### Example 2: Complex Feature

```
Request: "Add multi-currency support"
Flags: {approve_before_stage: [6]}

Time: 85 seconds + review
Checkpoints: 1
Output: 
  - Analysis (HIGH complexity)
  - [Checkpoint - developer reviews]
  - Complete plan

Developer action: Implement in phases
```

### Example 3: Unclear Bug

```
Request: "Fix the dashboard bug"

System: "Which dashboard? What bug?"
Developer: "Sales dashboard, numbers wrong"
System: "Always wrong or sometimes?"
Developer: "Only on Mondays"

Time: 45 seconds total
Checkpoints: 0 (after refinement)
Output: Root cause + minimal fix

Developer action: Implement
```

### Example 4: Performance Issue

```
Request: "Customer search too slow"
Flags: {approve_at_risk: medium}

Analysis: N+1 query, missing index
Risk: MEDIUM (large table, high traffic)
Checkpoint: Required

Developer reviews, approves index addition

Time: 60 seconds + review
Output: Implementation plan

Developer action: Implement with monitoring
```

---

## Next Steps

### Getting Started
1. Start with simple requests, no flags
2. Get comfortable with autonomous mode
3. Try checkpoint flags on medium work
4. Graduate to risk-based flags for complex work

### Building Confidence
- First 5 requests: Review all outputs carefully
- Next 10 requests: Use checkpoint flags
- After that: Trust autonomous for low-risk

### Team Adoption
- Start with one developer
- Share successful outputs
- Standardize flag patterns for your team
- Build team-specific guidelines

---

## Summary

The autonomous hybrid system gives you:

✅ **Speed** - Complete plans in under a minute
✅ **Control** - Flags let you review when needed
✅ **Safety** - Automatic stops for high-risk situations
✅ **Intelligence** - System escalates when uncertain
✅ **Flexibility** - From fully autonomous to fully manual

**Default to autonomous.** Add flags when you need control.

**Trust the system.** It'll stop when it should.

**Review the output.** Then implement with confidence.
