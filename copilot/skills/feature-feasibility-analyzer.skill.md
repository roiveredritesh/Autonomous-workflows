# Feature Feasibility Analyzer Skill

## Purpose
Evaluates technical and business feasibility of proposed features in legacy ASP.NET WebForms environment.

## Input Requirements
```yaml
feature:
  title: <feature name>
  description: <what user wants>
  requirements: [<functional requirements>]
  constraints: [<technical or business constraints>]
  timeline: <requested timeline if any>
  affected_systems: [<systems involved>]
```

## Processing Steps

1. **Technical Feasibility Assessment**
   - Can it be done with current technology stack?
   - WebForms compatibility issues?
   - Third-party library availability?
   - Performance implications?

2. **Legacy System Impact**
   - ViewState implications
   - Page lifecycle conflicts
   - Telerik control limitations
   - Database schema changes needed?

3. **Risk Evaluation**
   - Data integrity risks
   - Performance risks
   - Regression risks
   - Deployment risks

4. **Complexity Estimation**
   - Lines of code to change
   - Modules to modify
   - Testing effort
   - Refactoring needed?

5. **Alternative Approaches**
   - Identify workarounds
   - Consider phased approach
   - Evaluate different technical paths

## Output Format

```yaml
feasibility_assessment:
  
  technical_feasibility:
    rating: <high|medium|low>
    reasoning: <explanation>
    blockers: [<technical blockers if any>]
    opportunities: [<enablers>]
  
  legacy_system_impact:
    webforms_compatible: <yes|no|with_workaround>
    viewstate_impact: <none|minor|significant|blocker>
    lifecycle_issues: [<list if any>]
    telerik_concerns: [<list if any>]
  
  risk_assessment:
    overall_risk: <low|medium|high|critical>
    risks:
      - risk: <description>
        probability: <high|medium|low>
        impact: <high|medium|low>
        mitigation: <how to mitigate>
  
  complexity_estimation:
    estimated_lines_changed: <range>
    modules_to_modify: [<list>]
    refactoring_required: <yes|no|maybe>
    effort_hours: <estimate>
    testing_effort: <low|medium|high>
  
  alternatives_considered:
    - option: <alternative approach>
      pros: [<advantages>]
      cons: [<disadvantages>]
      recommendation: <why chosen or not>
  
  recommendation:
    decision: <proceed|proceed_with_mitigations|pivot|spike_first|not_feasible>
    reasoning: <summary>
    required_mitigations: [<list if decision is proceed_with_mitigations>]
    preconditions: [<what needs to be true>]
```

## Assessment Examples

### Example 1: Low Risk - Straightforward Feature
```yaml
Feature: "Add export to Excel button on customer list"

Output:
  technical_feasibility: high
  webforms_compatible: yes
  viewstate_impact: none
  overall_risk: low
  estimated_lines: "50-100"
  modules: ["CustomerList.aspx", "CustomerRepository"]
  effort: "4-8 hours"
  recommendation: "Proceed - straightforward feature"
```

### Example 2: Medium Risk - Database Changes
```yaml
Feature: "Add customer segment field for marketing targeting"

Output:
  technical_feasibility: medium
  webforms_compatible: yes
  viewstate_impact: minor
  overall_risk: medium
  risks:
    - risk: "Existing reports must be updated"
      probability: high
      impact: medium
      mitigation: "Include in scope, plan carefully"
    - risk: "Data migration for existing customers"
      probability: high
      impact: medium
      mitigation: "Script migration, test thoroughly"
  estimated_lines: "200-400"
  modules: ["CustomerForm.aspx", "CustomerRepository", "ReportPages"]
  effort: "20-30 hours"
  recommendation: "Proceed with careful planning"
```

### Example 3: High Risk - Architectural Change
```yaml
Feature: "Add real-time notifications via SignalR"

Output:
  technical_feasibility: low
  webforms_compatible: no (with_workaround)
  viewstate_impact: significant
  lifecycle_issues:
    - "SignalR incompatible with PostBack model"
    - "Stateful connections vs stateless pages"
  overall_risk: high
  blockers:
    - "Requires architectural changes"
    - "May need partial UI rewrite"
    - "Testing complexity increases significantly"
  recommendation: "Spike first - unknown compatibility issues"
```

### Example 4: Not Feasible
```yaml
Feature: "Switch from synchronous to fully async operations"

Output:
  technical_feasibility: low
  webforms_compatible: no
  lifecycle_issues:
    - "WebForms designed for synchronous model"
    - "ViewState serialization complex with async"
    - "Exception handling differs"
  overall_risk: critical
  blockers:
    - "Would require complete page rewrite"
    - "Risk of regression in all pages using async"
    - "No gradual migration path"
  recommendation: "Not feasible - consider as future architecture initiative, not feature"
  alternatives:
    - "Async database calls only (spike first)"
    - "WebForms to ASPX.NET Core migration (long-term)"
```

## Risk Categories

### Technical Risks
- Third-party library incompatibility
- Performance degradation
- Scalability concerns
- Security vulnerabilities

### Legacy System Risks
- WebForms incompatibility
- ViewState bloat
- Page lifecycle violations
- State management issues

### Data Risks
- Schema migration complexity
- Data consistency issues
- Backward compatibility breaks
- Rollback complexity

### Integration Risks
- External service dependencies
- API compatibility
- Cache invalidation
- Concurrent update issues

## Feasibility Levels

### High Feasibility
- Clear technical path
- Minimal legacy system impact
- Low risk
- Can start immediately
- **Decision:** Proceed

### Medium Feasibility
- Some technical challenges
- Moderate legacy impact
- Medium risk
- Needs careful planning
- **Decision:** Proceed with mitigations

### Low Feasibility
- Significant technical challenges
- High legacy impact
- High risk
- Requires investigation
- **Decision:** Spike first

### Not Feasible
- Blocking issues
- Architectural misalignment
- Critical risks
- **Decision:** Reject or major refactor

## Estimation Framework

| Aspect | Low | Medium | High | Very High |
|--------|-----|--------|------|-----------|
| Lines Changed | <50 | 50-200 | 200-500 | >500 |
| Modules | 1 | 2-3 | 4-6 | 6+ |
| Effort Hours | 4-8 | 12-20 | 24-40 | 40+ |
| Risk Level | Low | Medium | High | Critical |
| Recommendation | Proceed | Plan | Spike | Don't |

## Related Skills
- `acceptance-criteria-expander` - Clarifies requirements
- `spike-charter` - Plans investigation
- `webforms-lifecycle-analyzer` - Checks page lifecycle impact
- `minimal-diff-planner` - Plans minimal implementation
