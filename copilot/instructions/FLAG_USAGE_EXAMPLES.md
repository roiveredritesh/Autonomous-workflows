# Flag Usage Examples

## Purpose

Real-world examples of how to use execution flags to control autonomous workflow execution.

---

## Example 1: Simple Feature (Full Autonomous)

### Scenario
Adding a straightforward export button - low risk, well understood

### Input
```
Add Excel export button to customer list page
```

### Flags
```yaml
# No flags - fully autonomous
```

### Execution Flow
```
[t=0s] Orchestrator detects MODE: FEATURE
[t=2s] Executing stages 1-5 (analysis)
  ✓ Stage 1: Validate ticket
  ✓ Stage 2: Expand acceptance criteria
  ✓ Stage 3: Assess feasibility (HIGH) and risk (LOW)
  ✓ Stage 4: Analyze legacy impact (minimal)
  ✓ Stage 5: Data/cache strategy (no caching needed)

[t=25s] Executing stages 6-9 (planning)
  ✓ Stage 6: Create implementation plan
  ✓ Stage 7: Generate test scenarios
  ✓ Stage 8: Prepare documentation
  ✓ Stage 9: Define rollback procedure

[t=45s] Complete - ready for implementation
```

### Output
```yaml
MODE: FEATURE
EXECUTION: Autonomous
DURATION: 45 seconds
CHECKPOINTS: 0

ANALYSIS SUMMARY:
  Requirements: Add export button, .xlsx format, all columns
  Feasibility: HIGH
  Risk: LOW
  Legacy Impact: Add button to existing toolbar, use EPPlus library

IMPLEMENTATION PLAN:
  Files: CustomerList.aspx, CustomerList.aspx.cs, CustomerRepository.cs
  Approach: Server-side export on button click
  Tests: Export with filters, empty results, large datasets

READY FOR: Implementation
```

### When to Use This Pattern
- Routine features
- Low-risk changes
- Well-understood requirements
- Standard patterns

---

## Example 2: Feature with Review Checkpoint

### Scenario
Adding email notifications - want to review analysis before committing to implementation

### Input
```
Add email notification when order status changes to Shipped
Flags:
  approve_before_stage: [6]
```

### Execution Flow
```
[t=0s] Orchestrator detects MODE: FEATURE
[t=2s] Executing stages 1-5 (analysis)
  ✓ Stage 1: Validate ticket
  ✓ Stage 2: Expand acceptance criteria
    - Email sent on status change to Shipped
    - Contains order number, tracking link
    - Failure logged but doesn't block status update
  ✓ Stage 3: Assess feasibility (HIGH) and risk (MEDIUM)
  ✓ Stage 4: Analyze legacy impact
    - Modify OrderRepository.UpdateStatus()
    - Add EmailService integration
  ✓ Stage 5: Data/cache impact
    - No database changes needed
    - Email queue for failed sends

[t=30s] ═══ CHECKPOINT: Analysis Complete ═══

STAGES 1-5 COMPLETED

REQUIREMENTS:
- Email on status change to Shipped only
- Email to customer email on order
- Content: order number, tracking URL, expected delivery
- Email failure logged, doesn't block update

FEASIBILITY: HIGH
RISK: MEDIUM
- Email service dependency
- Need retry logic for failures
- Email content template required

LEGACY IMPACT:
- Modify: OrderRepository.UpdateStatus() [safe change boundary]
- Add: EmailService wrapper
- Add: Email template configuration

DECISION REQUIRED:
Approve implementation planning?

[ ] Approve - Continue to stages 6-9
[ ] Adjust - Modify approach
[ ] Spike - Need investigation
[ ] Reject - Stop workflow
═══════════════════════════════════════════

[WAITING FOR USER]
```

### User Response
```
You: "Approve"
```

### Continued Execution
```
[t=31s] Executing stages 6-9 (planning)
  ✓ Stage 6: Create implementation plan
  ✓ Stage 7: Generate test scenarios
  ✓ Stage 8: Prepare documentation
  ✓ Stage 9: Define rollback procedure

[t=50s] Complete - ready for implementation
```

### Final Output
```yaml
MODE: FEATURE
EXECUTION: Hybrid (checkpoint after analysis)
DURATION: 50 seconds + user decision time
CHECKPOINTS: 1

IMPLEMENTATION PLAN:
  Phase 1: Add EmailService wrapper
  Phase 2: Integrate in OrderRepository
  Phase 3: Add email template
  Phase 4: Add retry logic

TESTS:
  - Email sent on Shipped status change
  - Email not sent on other status changes
  - Failed email logged, update completes
  - Email contains correct data

ROLLBACK:
  - Feature flag to disable email sending
  - Remove EmailService.Send() call
  - Monitor email queue for failures

READY FOR: Implementation
```

### When to Use This Pattern
- Medium-complexity features
- External service integration
- Want to review before committing
- Changes to critical paths

---

## Example 3: Performance Optimization (Risk-Based Pausing)

### Scenario
Optimizing slow query - pause if risky

### Input
```
Optimize customer search page - currently takes 8+ seconds
Flags:
  approve_at_risk: medium
```

### Execution Flow
```
[t=0s] Orchestrator detects MODE: PERFORMANCE
[t=2s] Executing stages 1-4
  ✓ Stage 1: Baseline performance
    Current: 8.2 seconds average
    Target: <3 seconds
  ✓ Stage 2: Identify bottlenecks
    Primary: Database query (7.8s of 8.2s)
  ✓ Stage 3: Root cause analysis
    Issue: Loading all 50K customers, filtering in memory
    Query: SELECT * FROM Customers; then .Where(Status == 'Active')

[t=15s] Stage 4: Risk assessment
  RISK: MEDIUM
  - Large table (50K rows)
  - Missing index on Status column
  - High-traffic page

[t=16s] ═══ CHECKPOINT: Risk Threshold Reached ═══

STAGES 1-4 COMPLETED

RISK: MEDIUM

ROOT CAUSE:
Query loads all 50K customers into memory, then filters
Missing index on Status column causes table scan
Current query: SELECT * FROM Customers WHERE Status = @status
Execution plan: Table Scan (Cost: 98%)

PERFORMANCE:
Current: 8.2 seconds (p95: 12.4s)
Bottleneck: Database query (7.8s)
Memory: 150MB for full customer list

OPTIMIZATION OPTIONS:

Option 1: Add Index + Pagination (RECOMMENDED)
  Risk: LOW
  Impact: 95% improvement (8.2s → 400ms)
  Changes:
    - Add index on Status column
    - Implement pagination (50 rows/page)
    - Update query to filter in database
  Confidence: HIGH

Option 2: Add Caching
  Risk: MEDIUM
  Impact: 90% improvement (first load still slow)
  Changes:
    - Cache active customers in Redis
    - 5-minute TTL
    - Complex invalidation on customer updates
  Confidence: MEDIUM

Option 3: Rewrite Query to Stored Procedure
  Risk: MEDIUM
  Impact: 85% improvement
  Changes:
    - Create stored procedure
    - More testing required
    - Harder to maintain
  Confidence: MEDIUM

DECISION REQUIRED:
Risk is MEDIUM. Review and approve approach?

[ ] Approve - Proceed with Option 1 (recommended)
[ ] Adjust - Choose different option
[ ] Spike - Need more investigation
[ ] Reject - Stop optimization
═══════════════════════════════════════════════

[WAITING FOR USER]
```

### User Response (Scenario A: Approve)
```
You: "Approve"
```

### Continued Execution
```
[t=17s] Executing stages 5-7
  ✓ Stage 5: Safety verification
    - Query behavior validated
    - Index addition safe
    - Pagination maintains correctness
  ✓ Stage 6: Implementation plan
    - Add index: CREATE INDEX IX_Customer_Status
    - Update repository: Add pagination
    - Update UI: Pager control
  ✓ Stage 7: Validation plan
    - Load test with 50K records
    - Verify pagination correctness
    - Monitor database load

[t=40s] Complete - ready for implementation
```

### User Response (Scenario B: Adjust)
```
You: "Adjust: Use Option 2 (caching) but with 10-minute TTL"
```

### Continued Execution
```
[t=17s] Executing stages 5-7 with adjusted parameters
  ✓ Stage 5: Safety verification (caching approach)
  ✓ Stage 6: Implementation plan (caching with 10-min TTL)
  ✓ Stage 7: Validation plan (cache hit rate monitoring)

[t=45s] Complete - ready for implementation
```

### When to Use This Pattern
- Performance optimizations
- Database changes
- Unknown performance impact
- High-traffic pages

---

## Example 4: Bug Fix (Automatic Risk Detection)

### Scenario
Fixing a bug, unsure of complexity

### Input
```
Fix: Customer search returns wrong results when filter applied
Flags:
  approve_at_risk: medium
```

### Execution Flow
```
[t=0s] Orchestrator detects MODE: BUG FIX
[t=2s] Executing stages 1-3
  ✓ Stage 1: Bug classification
    Severity: HIGH
    Type: Functional
    Reproducible: Always
  ✓ Stage 2: Root cause
    Issue: LINQ Where clause applied after ToList()
    Location: CustomerRepository.cs line 145
  ✓ Stage 3: Impact analysis
    User impact: All filtered searches incorrect
    Data impact: None (read-only)
    Scope: Customer search page only

[t=12s] Risk assessment: LOW
[No checkpoint triggered - risk below threshold]

[t=13s] Executing stages 4-8
  ✓ Stage 4: Fix strategy
    Approach: Move .Where() before .ToList()
    Files: CustomerRepository.cs
    Lines changed: ~2
  ✓ Stage 5: Safety verification
    Public API: No changes
    Lifecycle: Not affected
  ✓ Stage 6: Regression prevention
    Test: All filter combinations
    Verify: Related search functionality
  ✓ Stage 7: Documentation
    Root cause documented
    Prevention: Code review checklist updated
  ✓ Stage 8: Rollback
    Simple revert of change

[t=28s] Complete - ready for fix implementation
```

### Output
```yaml
MODE: BUG FIX
EXECUTION: Autonomous (risk stayed LOW)
DURATION: 28 seconds
CHECKPOINTS: 0

ROOT CAUSE:
LINQ Where clause applied after ToList() in CustomerRepository.cs:145
Original: customers.ToList().Where(c => c.Status == filter.Status)
Problem: Filter applied in memory after loading all customers

FIX:
Move .Where() before .ToList()
Fixed: customers.Where(c => c.Status == filter.Status).ToList()

RISK: LOW
IMPACT: 2 lines changed
TESTING: Verify all filter combinations

READY FOR: Fix implementation
```

### When to Use This Pattern
- Bug fixes with uncertain complexity
- Want to auto-pause if risky
- Standard bug triage

---

## Example 5: Production Hotfix (Manual Mode)

### Scenario
Critical production issue - need full control

### Input
```
URGENT: Order submission failing in production, 100% failure rate
Flags:
  manual_mode: true
```

### Execution Flow
```
[t=0s] Orchestrator detects MODE: HOTFIX
       Note: Hotfix agent defaults to manual mode for safety

[t=2s] Executing stage 1 (assessment)
  ✓ Production impact assessed
    Severity: CRITICAL
    Scope: All users
    Data at risk: No
    Workaround: None

[t=5s] ═══ STAGE 1 COMPLETE ═══
ASSESSMENT:
Severity: CRITICAL
Impact: 100% order submission failure
Started: 2 hours ago (coincides with deployment)
Users affected: All
Workaround: None available

Continue to stage 2 (Diagnosis)?
═══════════════════════════════

You: "Yes"

[t=6s] Executing stage 2 (diagnosis)
  ✓ Analyzed production logs
  ✓ Detected error pattern
    Error: NullReferenceException in ShippingCalculator
    Trigger: Deployment 2 hours ago
    Confidence: HIGH

[t=10s] ═══ STAGE 2 COMPLETE ═══
DIAGNOSIS:
Root cause: NullReferenceException in ShippingCalculator
Stack trace: ShippingCalculator.Calculate() line 87
Trigger: Deployment v2.4.1 (2 hours ago)
First occurrence: 2:00 PM (matches deployment)
Pattern: 100% of order submissions failing with same error

Continue to stage 3 (Fix Strategy)?
═════════════════════════════════════

You: "Yes"

[t=11s] Executing stage 3 (fix strategy)
  ✓ Evaluated strategy options

[t=15s] ═══ STAGE 3 COMPLETE ═══
FIX STRATEGY:

Option 1: ROLLBACK (RECOMMENDED)
  Time: 15-20 minutes
  Risk: LOW (return to known good state)
  Reasoning: Recent deployment, rollback is safest

Option 2: Code Patch
  Time: 60-90 minutes
  Risk: MEDIUM
  Fix: Add null check for ShippingMethod.Carrier
  Reasoning: Addresses root cause but takes longer

RECOMMENDATION: Rollback to v2.4.0

Approve rollback strategy?
═══════════════════════════

You: "Approve - proceed with rollback"

[t=16s] Executing stage 4 (implementation)
  ✓ Created rollback deployment
  ✓ Tested rollback in staging
  ✓ Rollback validated - no errors

[t=22s] ═══ STAGE 4 COMPLETE ═══
ROLLBACK PREPARED:
- Deployment package: v2.4.0
- Staging test: PASSED
- Validation: 20 test orders successful
- Risk: LOW

Approve deployment to production?
═══════════════════════════════════

You: "Approve"

[t=23s] Executing stage 5 (deployment)
  ✓ Deployed to production
  ✓ Smoke tests passed
  ✓ Monitoring active

[t=28s] ═══ STAGE 5 COMPLETE ═══
DEPLOYED: v2.4.0 (rollback)
Status: Orders submitting successfully
Error rate: 0% (down from 100%)

Continue monitoring for 30 minutes?
═══════════════════════════════════

You: "Yes"

[t=29s] Executing stage 6 (verification)
  [Monitoring for 30 minutes]

[t=59s] ═══ STAGE 6 COMPLETE ═══
VERIFICATION:
- 30 minutes elapsed
- 147 orders submitted successfully
- Error rate: 0%
- Performance: Normal
- User reports: Issue resolved

Continue to documentation (stage 7)?
════════════════════════════════════

You: "Yes"

[... continues through stages 7-8 ...]

[t=75s] Complete - incident resolved
```

### Final Output
```yaml
MODE: HOTFIX
EXECUTION: Manual (full control)
DURATION: 75 seconds + user decision time (9 checkpoints)
INCIDENT DURATION: ~22 minutes from decision to resolution

RESOLUTION:
Strategy: Rollback to v2.4.0
Deployment time: 6 minutes
Verification: 30 minutes
Total downtime: ~2 hours (from issue start)

FOLLOW-UP:
Proper fix: PROJ-5678 created
Root cause: Missing null check for ShippingMethod.Carrier
Permanent fix: Add null check and use default carrier
Postmortem: Scheduled for next day

LESSONS LEARNED:
- Deployment lacked smoke tests for shipping calculation
- Need automated test for all order submission paths
```

### When to Use This Pattern
- Production emergencies
- Critical hotfixes
- Maximum oversight required
- Compliance/audit requirements

---

## Example 6: Complex Feature (Multiple Checkpoints)

### Scenario
Data migration - high risk, multiple review points needed

### Input
```
Migrate customer address data to new normalized schema
Flags:
  approve_before_stage: [5, 7]
  approve_at_risk: low
```

### Execution Flow
```
[t=0s] Orchestrator detects MODE: FEATURE
[t=2s] Executing stages 1-4
  ✓ Stage 1: Validate requirements
  ✓ Stage 2: Expand acceptance criteria
  ✓ Stage 3: Assess feasibility (MEDIUM) and risk (HIGH)
  ✓ Stage 4: Analyze legacy impact (extensive)

[t=20s] Stage 5: Data impact analysis
  RISK: HIGH (data migration)

[t=21s] ═══ CHECKPOINT 1: Risk Detected ═══
RISK: HIGH

DATA MIGRATION COMPLEXITY:
- 50,000 customer records
- Denormalized address schema → Normalized
- Production data at risk
- Requires careful rollback strategy

[WAITING FOR USER]

You: "Spike - need migration proof of concept"

[Copilot switches to SPIKE mode]
[Returns after spike with findings]

You: "Resume with updated approach"

[t=25s] Executing stage 5 (revised)
  ✓ Updated data migration strategy
  ✓ Phased migration approach
  ✓ Validation checkpoints

[t=30s] ═══ CHECKPOINT 2: Stage 5 Complete ═══
(Flag: approve_before_stage: [5])

DATA MIGRATION STRATEGY:
Phase 1: Add new normalized tables (no data migration)
Phase 2: Dual-write to both schemas
Phase 3: Backfill historical data in batches
Phase 4: Validate data consistency
Phase 5: Switch reads to new schema
Phase 6: Remove old schema

Approve planning stages?

You: "Approve"

[t=31s] Executing stage 6
  ✓ Implementation plan created

[t=40s] Executing stage 7
  ✓ Test scenarios generated

[t=45s] ═══ CHECKPOINT 3: Stage 7 Complete ═══
(Flag: approve_before_stage: [7])

TESTING STRATEGY:
- Validation queries for data consistency
- Rollback test for each phase
- Performance testing for dual-write
- Load testing for backfill

Approve documentation and rollback planning?

You: "Approve"

[t=46s] Executing stages 8-9
  ✓ Documentation prepared
  ✓ Rollback procedures defined

[t=60s] Complete - ready for phased implementation
```

### Output
```yaml
MODE: FEATURE
EXECUTION: Hybrid (3 checkpoints)
DURATION: 60 seconds + 3 × decision time + spike time
CHECKPOINTS: 3 (risk + 2 stage flags)

IMPLEMENTATION PLAN:
Phased approach over 2 weeks:
  Week 1: Add new schema, dual-write
  Week 2: Backfill, validate, switch reads

RISK MITIGATION:
- Spike validated approach
- Phased rollout
- Rollback at each phase
- Continuous validation

READY FOR: Implementation (Phase 1)
```

### When to Use This Pattern
- Data migrations
- High-risk changes
- Multi-phase implementations
- Need multiple review points

---

## Example 7: Investigation (Spike Mode)

### Scenario
Unknown legacy behavior needs investigation

### Input
```
Investigate: Why does OrderRepository cache expire at random times?
```

### Execution Flow
```
[t=0s] Orchestrator detects MODE: SPIKE
[t=2s] Executing stage 1 (spike definition)
  ✓ Research question: Why random cache expiration?
  ✓ Success criteria: Understand expiration pattern
  ✓ Time box: 4 hours
  ✓ Out of scope: Fixing the issue (investigation only)

[t=5s] Executing stages 2-3 (investigation)
  ✓ Hypothesis: Time-based TTL with clock skew
  ✓ Investigation steps defined
  ✓ Skills invoked:
    - redis-key-inspector
    - cache-behavior-analyzer
    - code-archaeology

[t=2.5 hours] Investigation findings:
  ✓ Analyzed cache keys
  ✓ Reviewed expiration logs
  ✓ Traced code history
  ✓ Found root cause

[t=2.5 hours] Executing stage 4 (findings)
  ✓ Documented discoveries
  ✓ Assessed confidence (HIGH)
  ✓ Formulated recommendations

[t=2.5 hours] ═══ SPIKE COMPLETE ═══

RESEARCH QUESTION:
Why does OrderRepository cache expire at random times?

TIME SPENT: 2.5 hours (within 4-hour time box)

FINDINGS:
Root cause: Cache TTL calculated using DateTime.Now
Issue: Multiple servers with clock skew (up to 30 seconds)
Result: Cache expires at different times on different servers

Evidence:
- Server timestamps vary by 15-30 seconds
- Cache keys use absolute expiration
- Logs show staggered expiration times matching clock skew

CONFIDENCE: HIGH

RECOMMENDATIONS:
1. Use DateTimeOffset.UtcNow instead of DateTime.Now
2. Add clock synchronization monitoring
3. Consider sliding expiration instead of absolute

NEXT STEPS:
- Create ticket for proper fix
- Estimate: Low complexity, low risk
- Can implement in next sprint

═════════════════════════════════════

Ready to create fix ticket?

You: "Yes - create feature ticket for fix"

[Orchestrator creates feature ticket with spike findings]
```

### When to Use This Pattern
- Unknown legacy behavior
- Technical feasibility questions
- Performance investigations
- Root cause analysis

---

## Example 8: Story Refinement (Unclear Requirements)

### Scenario
Vague feature request needs clarification

### Input
```
We need better customer reporting
```

### Execution Flow
```
[t=0s] Orchestrator detects MODE: REFINEMENT
       (Low confidence in requirements)

[t=2s] Executing refinement stages 1-6
  ✓ Stage 1: Analyze current state
    - 3 existing customer reports
    - All export to PDF only
    - Generated on-demand

  ✓ Stage 2: Extract requirements
    Questions for stakeholder:
    - What's wrong with current reports?
    - Who uses them?
    - What decisions need better data?
    - Specific improvements needed?

  ✓ Stage 3: Generate acceptance criteria
    (Based on typical patterns)

  ✓ Stage 4: Identify edge cases

  ✓ Stage 5: Define scope

  ✓ Stage 6: Complete metadata

[t=20s] ═══ REFINEMENT COMPLETE ═══

ORIGINAL: "We need better customer reporting"

REFINED STORY:
"Add Excel export to existing Customer Sales Report"

REQUIREMENTS:
Functional:
- Export button on Customer Sales Report page
- Excel format (.xlsx)
- All visible columns included
- Respect current filter/sort
- Maximum 10,000 rows

Non-functional:
- Export completes within 10 seconds
- No impact on page performance
- Works in all supported browsers

ACCEPTANCE CRITERIA:
Given: Customer Sales Report is displayed
When: User clicks "Export to Excel" button
Then: Excel file downloads with filtered data
And: File contains all visible columns
And: Filename includes date (CustomerSales_2024-01-15.xlsx)

EDGE CASES:
- Empty result set → Export with headers only
- >10K rows → Show warning, export first 10K
- Export fails → Show error, allow retry
- Special characters in data → Properly escaped

SCOPE:
In scope:
  - Excel export only
  - Customer Sales Report only
  - Use existing EPPlus library

Out of scope:
  - PDF format (future consideration)
  - Other reports (separate stories)
  - Scheduled/automatic exports

METADATA:
Complexity: Medium
Risk: Low
Dependencies: EPPlus library (already in use)
Affected components: CustomerSalesReport.aspx

READY FOR IMPLEMENTATION: Yes

═══════════════════════════════════

Accept refinement? Start feature workflow?

You: "Yes - proceed with feature implementation"

[Orchestrator switches to FEATURE mode with refined story]
```

### When to Use This Pattern
- Vague requirements
- Unclear scope
- Missing acceptance criteria
- Need stakeholder clarification

---

## Flag Combinations Summary

### Conservative (Maximum Control)

```yaml
# Good for: High-risk changes, production work
Flags:
  manual_mode: true
```

---

### Balanced (Review at Key Points)

```yaml
# Good for: Medium-risk features, external integrations
Flags:
  approve_before_stage: [6]
  approve_at_risk: medium
```

---

### Risk-Aware (Auto-pause on Issues)

```yaml
# Good for: Unknown complexity, performance work
Flags:
  approve_at_risk: medium
  approve_before_skills: [linq-query-tracer, sql-execution-analyzer]
```

---

### Analysis Review (Check Before Commitment)

```yaml
# Good for: Want to see analysis before implementation
Flags:
  approve_before_stage: [6]
# or
Flags:
  checkpoint_strategy: analysis_only
```

---

### Aggressive (Trust the Process)

```yaml
# Good for: Low-risk routine work, well-understood patterns
# No flags - fully autonomous
```

---

## Best Practices by Scenario

### New Feature (Standard)
```yaml
Default: No flags (autonomous)
Add flags if: External integration, database changes
```

### New Feature (Complex)
```yaml
Recommended:
  approve_before_stage: [6]
  approve_at_risk: medium
```

### Bug Fix (Standard)
```yaml
Recommended:
  approve_at_risk: medium
```

### Bug Fix (Production)
```yaml
Recommended:
  manual_mode: true
```

### Performance Work
```yaml
Recommended:
  approve_at_risk: low
  approve_before_stage: [6]
```

### Data Migration
```yaml
Recommended:
  approve_before_stage: [5, 7]
  approve_at_risk: low
```

### Investigation
```yaml
Default: No flags (spike agent handles)
```

### Unclear Requirements
```yaml
Default: No flags (refinement agent handles)
```

---

## Summary

These examples demonstrate:

1. **Start simple** - No flags for routine work
2. **Add control as needed** - Flags for complex/risky work
3. **Risk-aware** - System auto-pauses on safety issues
4. **Flexible** - Adjust at checkpoints
5. **Mode-aware** - Different agents have different defaults

**Choose flags based on risk, complexity, and need for control.**
