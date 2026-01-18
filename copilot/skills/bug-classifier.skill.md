# Bug Classifier Skill

## Purpose
Categorizes bugs by severity, type, reproducibility, and impact to determine appropriate handling approach.

## Input Requirements
```yaml
bug:
  title: <bug title>
  description: <what went wrong>
  error_message: <if applicable>
  reproduction_steps: <if known>
  affected_users: <count or estimate>
  affected_feature: <component/page>
  environment: <prod|staging|dev>
```

## Processing Steps

1. **Severity Classification**
   - User impact level
   - Data impact
   - Production impact
   - Workaround availability

2. **Type Classification**
   - Functional (feature broken)
   - Performance (slow)
   - Data (incorrect results)
   - UI (display/UX issue)
   - Security (vulnerability)

3. **Reproducibility Assessment**
   - Always reproducible
   - Intermittent
   - Rare/difficult to reproduce
   - Cannot reproduce

4. **Component Identification**
   - Affected pages
   - Affected modules
   - Affected systems

5. **Priority Determination**
   - Urgency (based on severity + environment)
   - Impact × Probability

## Output Format

```yaml
bug_classification:
  
  severity:
    level: <critical|high|medium|low>
    reasoning: <why this severity>
  
  type:
    primary: <functional|performance|data|ui|security>
    secondary: [<other types if applicable>]
  
  reproducibility:
    frequency: <always|intermittent|rare|cannot_reproduce>
    reproduction_difficulty: <easy|moderate|difficult>
    steps_verified: <yes|no|unknown>
  
  impact:
    affected_users: <count or percentage>
    affected_feature: <name>
    data_impacted: <yes|no>
    business_impact: <none|low|medium|high|critical>
    workaround_exists: <yes|no>
  
  environment:
    first_reported: <prod|staging|dev>
    reproducible_in: [<environments>]
  
  priority:
    level: <critical|high|medium|low>
    rationale: <urgency and impact>
  
  escalation:
    should_escalate: <yes|no>
    escalate_to: <hotfix|spike|feature_refinement>
    reason: <if escalating>
  
  related_bugs: [<ticket IDs if similar bugs exist>]
  
  recommendation:
    action: <proceed_to_reproduction|hotfix|spike|defer>
    reason: <brief summary>
```

## Severity Levels

### Critical
**Characteristics:**
- Production system down or severely degraded
- Complete feature failure
- Data corruption or loss
- Security breach
- All users affected
- No workaround

**Examples:**
- Login page returns 500 error
- Orders failing to save
- Database connection failure
- Data being deleted accidentally

**Action:** Immediate investigation and hotfix consideration

### High
**Characteristics:**
- Major functionality broken
- Partial feature failure
- Multiple users significantly impacted
- No workaround
- Customer-facing

**Examples:**
- Search results incorrect for complex queries
- Export button throws exception
- Reports show wrong data
- Payment processing fails

**Action:** Expedited bug fix workflow

### Medium
**Characteristics:**
- Functionality degraded
- Workaround exists
- Specific users or scenarios affected
- Intermittent issues
- Customer inconvenience

**Examples:**
- Page slow for large datasets
- Specific filter combination doesn't work
- Occasional timeout
- UI element misaligned

**Action:** Standard bug fix workflow

### Low
**Characteristics:**
- Cosmetic issues
- Minor inconveniences
- Rarely encountered
- No business impact
- Workaround available

**Examples:**
- Typo in label
- Button slightly misaligned
- Tooltip text unclear
- Help text incomplete

**Action:** Can be batched or deferred

## Bug Type Definitions

### Functional Bug
- Feature doesn't work as intended
- Logic error
- Unexpected behavior

### Performance Bug
- System slow
- Memory leak
- Resource exhaustion
- Query inefficient

### Data Bug
- Wrong data returned
- Data corruption
- Calculation error
- Data loss

### UI Bug
- Display issue
- Layout problem
- Responsiveness issue
- Accessibility issue

### Security Bug
- Vulnerability
- Unauthorized access
- Data exposure
- Injection attack

## Reproducibility Assessment

### Always Reproducible
**Characteristics:**
- Same steps always produce bug
- Consistent behavior
- Easy to verify fix

**Example:** "Click Export → Error every time"

### Intermittent
**Characteristics:**
- Occurs sometimes, not always
- Specific conditions trigger it
- May depend on timing or load

**Example:** "Timeout occurs under heavy load"

### Rare/Difficult
**Characteristics:**
- Occurs very infrequently
- Complex conditions to reproduce
- Hard to verify

**Example:** "Occurs once per week under unknown conditions"

### Cannot Reproduce
**Characteristics:**
- User reported issue
- Cannot recreate in test environment
- May be environment-specific

**Example:** "Slow page - fast in test, slow in production"

## Classification Examples

### Example 1: Critical Functional Bug
```yaml
Input:
  title: "Login returns 500 error"
  description: "Users cannot log in - getting server error"
  error_message: "NullReferenceException in LoginHandler"
  environment: "prod"
  affected_users: "All"

Output:
  severity: critical
  type: functional
  reproducibility: always
  affected_users: "All"
  priority: critical
  escalation: "yes"
  escalate_to: hotfix
  recommendation: "Immediate hotfix required"
```

### Example 2: High Performance Bug
```yaml
Input:
  title: "Customer search slow"
  description: "Search takes 30+ seconds for complex filters"
  affected_feature: "Customer search"
  environment: "prod"
  affected_users: "50"

Output:
  severity: high
  type: performance
  reproducibility: always
  affected_users: "50"
  business_impact: high
  workaround_exists: yes (use simpler filters)
  priority: high
  recommendation: "Expedited bug fix, investigate query performance"
```

### Example 3: Medium Intermittent Bug
```yaml
Input:
  title: "Occasional timeout on order export"
  description: "Export sometimes fails with timeout"
  environment: "prod"
  affected_users: "handful, intermittent"
  reproducibility: "Intermittent, cannot reliably reproduce"

Output:
  severity: medium
  type: functional, performance
  reproducibility: intermittent
  affected_users: "5-10"
  business_impact: medium
  workaround_exists: yes (retry or manual export)
  priority: medium
  escalation: yes
  escalate_to: spike
  reason: "Cannot reproduce reliably - needs investigation"
```

### Example 4: Low Cosmetic Bug
```yaml
Input:
  title: "Button label cut off on mobile"
  description: "Export button text doesn't fully display"
  environment: "prod"
  affected_users: "Mobile users"

Output:
  severity: low
  type: ui
  reproducibility: always
  affected_users: "Mobile users"
  business_impact: low
  workaround_exists: yes (use desktop)
  priority: low
  recommendation: "Fix in next regular release, can defer"
```

## Decision Tree

```
┌─ Production?
│  ├─ No → Continue
│  └─ Yes → Consider HOTFIX
│
├─ Severity = Critical?
│  ├─ Yes → HOTFIX mode
│  └─ No → Continue
│
├─ Can reproduce?
│  ├─ No → SPIKE mode
│  └─ Yes → Continue
│
├─ Affects many users?
│  ├─ Yes + High priority → Expedited
│  └─ No + Low priority → Can defer
│
└─ Assign priority based on impact
```

## Related Skills
- `webforms-lifecycle-analyzer` - For WebForms-related bugs
- `linq-query-tracer` - For data bugs
- `production-impact-assessor` - For severity validation
