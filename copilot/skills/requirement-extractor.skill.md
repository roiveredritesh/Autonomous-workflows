# Requirement Extractor Skill

## Purpose
Identifies and clarifies functional, non-functional, and constraint requirements from ambiguous or incomplete specifications.

## Input Requirements
```yaml
specification:
  original_input: <user statement or story>
  context: <any background information>
  constraints: [<known constraints>]
  related_stories: [<ticket IDs if any>]
```

## Processing Steps

1. **Parse Original Input**
   - Identify core request
   - Note assumptions
   - List missing details

2. **Apply Five Whys Technique**
   - Why is this needed?
   - Why does it matter?
   - Why this approach?
   - Why now?
   - Why these constraints?

3. **Categorize Requirements**
   - Functional (MUST have)
   - Non-functional (HOW it works)
   - Constraints (Technical, business, regulatory)
   - Dependencies (What else it needs)

4. **Identify Gaps**
   - What's unclear?
   - What's missing?
   - What's assumed?
   - What needs investigation?

## Output Format

```yaml
requirement_extraction:
  
  original_request: <original statement>
  
  core_need: <fundamental user need>
  
  functional_requirements:
    must_have:
      - <requirement>
      - <requirement>
    should_have:
      - <requirement>
      - <requirement>
    nice_to_have:
      - <requirement>
  
  non_functional_requirements:
    performance:
      - <requirement>
    usability:
      - <requirement>
    reliability:
      - <requirement>
    security:
      - <requirement>
    scalability:
      - <requirement>
  
  constraints:
    technical:
      - <constraint>
    business:
      - <constraint>
    regulatory:
      - <constraint>
    timeline:
      - <constraint>
  
  dependencies:
    internal: [<stories or systems>]
    external: [<third-party services>]
    data: [<data requirements>]
  
  assumptions:
    - <assumption>
    - <assumption>
  
  questions_requiring_clarification:
    - <question>
    - <question>
  
  recommendation:
    completeness: <complete|mostly_complete|incomplete|very_unclear>
    ready_for_implementation: <yes|no|with_spike>
    next_step: <proceed|clarify|spike|refine>
```

## Five Whys Technique

### Question 1: Why is this needed?
**Purpose:** Understand business driver

**Example:**
- Request: "Add export to Excel"
- Why: "Users manually copy data and paste into spreadsheets"
- Driver: "Automation and time savings"

### Question 2: Why this user/stakeholder?
**Purpose:** Identify who benefits

**Example:**
- Request: "Export feature"
- Who: "Sales team, managers, report generators"
- Impact: "Saves 2-5 hours per week per person"

### Question 3: Why this approach/scope?
**Purpose:** Validate chosen solution

**Example:**
- Request: "Export to Excel"
- Why Excel: "Users already use Excel for reporting"
- Why all columns: "Users need flexibility"
- Why this scope: "Initial MVP, can expand later"

### Question 4: Why now/this priority?
**Purpose:** Understand urgency

**Example:**
- Request: "Quarterly requirement"
- Why now: "Q4 reporting season starts next month"
- Priority: "High - reporting deadline critical"

### Question 5: Why these constraints?
**Purpose:** Validate limitations

**Example:**
- Request: "No 500 row limit"
- Why limit: "Performance concerns"
- Why necessary: "Reports usually <200 rows"
- Why consider: "Rare users with 500+ row exports"

## Requirement Categories

### Functional Requirements (WHAT)
- Features that must work
- Business logic
- User interactions
- Data operations

**Example:**
- "Export customer list to Excel"
- "Include name, email, phone"
- "Respect applied filters"

### Non-Functional Requirements (HOW)
- Performance expectations
- Usability standards
- Reliability goals
- Security requirements

**Example:**
- "Export completes in <5 seconds"
- "File opens immediately in Excel"
- "Works on Chrome, Firefox, Safari"

### Constraints
- Technical limitations
- Business rules
- Regulatory requirements
- Resource limitations

**Example:**
- "Cannot modify database schema"
- "Must comply with GDPR"
- "Available development time: 1 week"

### Dependencies
- Other stories required
- Third-party services
- Data prerequisites
- Integration points

**Example:**
- "Requires customer filtering feature (PROJ-2100)"
- "Uses EPPlus library"
- "Needs database read access"

## Examples

### Example 1: Vague Request
```yaml
Input:
  original_input: "We need better reporting"

Processing:
  Why 1: "Users spend time manually gathering data"
  Why 2: "Sales team needs timely insights"
  Why 3: "Current reports don't answer their questions"
  Why 4: "New product line launched, need new metrics"
  Why 5: "Timeline: Need by end of quarter"

Output:
  core_need: "Enable sales team to generate sales metrics by region and product"
  
  functional_requirements:
    must_have:
      - "Report showing total sales by region"
      - "Report showing sales by product category"
      - "Filter by date range"
      - "Filter by sales rep"
  
  non_functional:
    performance: "Report generates in <2 seconds"
    usability: "No SQL knowledge required"
  
  constraints:
    business: "Must include new product line"
    timeline: "Complete by end of Q4"
  
  questions:
    - "Which specific metrics are needed?"
    - "What date ranges matter?"
    - "Who needs access?"
    - "Export format requirements?"
```

### Example 2: Incomplete Story
```yaml
Input:
  original_input: "Add email notifications for order status changes"

Processing:
  What is unclear:
    - Which status changes trigger email?
    - Who receives email?
    - What information in email?
    - What if email fails?
    - Email preferences?
    - Bulk operations?
  
Output:
  core_need: "Keep customers informed of order progress"
  
  functional_requirements:
    must_have:
      - "Send email when order status changes"
      - "Email contains order summary"
      - "Respect customer email preferences"
    should_have:
      - "Include tracking link"
      - "Include estimated delivery"
    
  constraints:
    technical: "Email service may be down"
    business: "Cannot break order processing if email fails"
  
  assumptions:
    - "Email preferences exist (or need to be created)"
    - "All orders have customer email"
    - "Email service available"
  
  questions:
    - "Which status changes trigger notification?"
    - "Include other order data or just summary?"
    - "Notification preferences?"
    - "Email handling on failure?"
```

### Example 3: Complex Feature
```yaml
Input:
  original_input: "Implement customer portal for self-service"

Output:
  core_need: "Reduce support tickets by enabling customers to self-serve"
  
  functional_requirements:
    must_have:
      - "View order history"
      - "Download invoices"
      - "View tracking information"
      - "Submit support tickets"
    should_have:
      - "Update profile information"
      - "Manage communication preferences"
  
  non_functional:
    performance: "Page load <2 seconds"
    security: "HTTPS only, password requirements"
    availability: "99.5% uptime"
    usability: "Mobile responsive, no training needed"
  
  constraints:
    technical: "Legacy WebForms application"
    regulatory: "PCI DSS for payment data"
    business: "Phase 1 launch in 6 weeks"
  
  dependencies:
    internal: ["Authentication service", "Order system", "Payment system"]
    external: ["Email service", "Shipping provider API"]
  
  questions:
    - "Authentication: Same login as internal? New login?"
    - "Payment: Allow new charges or view-only?"
    - "Support tickets: Via portal or escalate to staff?"
```

## Requirement Template

```
Functional Requirement: [What the system does]
- Trigger: [What causes this?]
- Actors: [Who/what is involved?]
- Preconditions: [What must be true first?]
- Steps: [Sequence of actions]
- Outcome: [What happens?]
- Postconditions: [What's true after?]
- Exceptions: [What if something goes wrong?]

Example:
- Trigger: User clicks "Export" button
- Preconditions: User has view permission, data available
- Steps: 
  1. System validates export request
  2. System gathers filtered data
  3. System formats data as Excel
  4. System sends to user
- Outcome: Excel file downloads
- Exceptions: 
  - No data: Show "No records to export"
  - Permission denied: Show "Access denied"
```

## Related Skills
- `acceptance-criteria-generator` - Converts requirements to testable criteria
- `edge-case-detector` - Identifies edge cases from requirements
- `spike-charter` - Plans investigation for unclear requirements
