# Execution Flag Parser

## Purpose
Defines how to parse, validate, and apply execution flags for autonomous workflow control.

---

## Overview

The flag parser extracts execution control parameters from user input and creates a structured configuration that agents use to determine when to pause for human approval.

---

## Flag Types

### 1. approve_before_stage

**Purpose:** Pause execution before specific workflow stages

**Type:** `array[integer]`

**Valid Values:** `[1, 2, 3, 4, 5, 6, 7, 8, 9]`

**Default:** `[]` (no stage-based pauses)

**Examples:**
```yaml
# Pause before implementation planning (stage 6)
approve_before_stage: [6]

# Pause before multiple stages
approve_before_stage: [5, 7]

# Inline format
"Add Excel export [approve_before_stage: 6]"
```

**Behavior:**
- Agent executes stages in batch until reaching flagged stage
- Presents consolidated results at checkpoint
- Waits for user approval before continuing

---

### 2. approve_at_risk

**Purpose:** Pause execution when risk level meets or exceeds threshold

**Type:** `string`

**Valid Values:** `low | medium | high`

**Default:** `null` (no risk-based pausing)

**Examples:**
```yaml
# Pause if risk is medium or higher
approve_at_risk: medium

# Pause only on high risk
approve_at_risk: high

# Pause on any risk (including low)
approve_at_risk: low
```

**Behavior:**
- Agent monitors risk level at each stage
- If risk >= threshold, pause and present risk analysis
- User reviews and decides whether to continue

**Risk Comparison:**
```
Risk Levels (ascending):
  LOW < MEDIUM < HIGH

Examples:
  - approve_at_risk: medium
    → Pauses on MEDIUM and HIGH
    → Does NOT pause on LOW

  - approve_at_risk: high
    → Pauses only on HIGH
    → Does NOT pause on LOW or MEDIUM
```

---

### 3. approve_before_skills

**Purpose:** Pause execution before invoking specific skills

**Type:** `array[string]`

**Valid Values:** Any valid skill name from the skills catalog

**Default:** `[]` (no skill-based pauses)

**Examples:**
```yaml
# Pause before expensive database analysis
approve_before_skills: [linq-query-tracer, sql-execution-analyzer]

# Pause before cache strategy decisions
approve_before_skills: [redis-cache-strategy-analyzer]
```

**Behavior:**
- Agent executes normally until skill is needed
- Before invoking flagged skill, pause and request approval
- Present skill purpose and expected impact
- User approves or suggests alternative

**Common Use Cases:**
- Skills with performance cost
- Skills that make critical decisions
- Skills that modify production data
- Skills requiring human judgment

---

### 4. manual_mode

**Purpose:** Require approval after every stage (full manual control)

**Type:** `boolean`

**Valid Values:** `true | false`

**Default:** `false`

**Examples:**
```yaml
# Enable full manual mode
manual_mode: true

# Inline format
"Add Excel export [manual_mode: true]"
```

**Behavior:**
- Execute one stage at a time
- After each stage, present results and pause
- User must approve to continue to next stage
- Slowest but maximum control

**When to Use:**
- Learning the workflow system
- High-risk changes
- Compliance requirements
- Complex debugging

---

### 5. checkpoint_strategy

**Purpose:** Define automatic checkpoint placement strategy

**Type:** `string`

**Valid Values:** `analysis_only | planning_only | both | none`

**Default:** `none` (agent default checkpoints apply)

**Examples:**
```yaml
# Checkpoint after analysis only
checkpoint_strategy: analysis_only

# Checkpoint after both analysis and planning
checkpoint_strategy: both

# No automatic checkpoints (full autonomous)
checkpoint_strategy: none
```

**Behavior:**
```yaml
analysis_only:
  - Execute stages 1-5 (analysis)
  - CHECKPOINT
  - Execute stages 6-9 (planning)
  - Complete

planning_only:
  - Execute stages 1-9
  - CHECKPOINT before final execution
  - Complete after approval

both:
  - Execute stages 1-5 (analysis)
  - CHECKPOINT 1
  - Execute stages 6-9 (planning)
  - CHECKPOINT 2
  - Complete after approval

none:
  - Execute all stages
  - Auto-stops only (no regular checkpoints)
```

---

## Flag Parsing Algorithm

### Step 1: Detect Flag Syntax

```yaml
input_patterns:

  # Pattern 1: Inline brackets
  regex: '\[([^\]]+)\]'
  example: "Add Excel export [approve_before_stage: 6]"

  # Pattern 2: YAML block after request
  marker: "Flags:" or "flags:"
  example: |
    Add Excel export
    Flags:
      approve_before_stage: [6]
      approve_at_risk: medium

  # Pattern 3: Natural language
  keywords:
    - "pause before"
    - "stop before"
    - "approve before"
    - "manual mode"
  example: "Add Excel export, but pause before implementation"
  translation: "approve_before_stage: [6]"
```

### Step 2: Extract Flag Values

```python
def extract_flags(user_input):
    """
    Extract execution flags from user input

    Returns: dict with flag keys and values
    """
    flags = {
        'approve_before_stage': [],
        'approve_at_risk': None,
        'approve_before_skills': [],
        'manual_mode': False,
        'checkpoint_strategy': None
    }

    # Check for inline brackets
    inline_match = re.search(r'\[([^\]]+)\]', user_input)
    if inline_match:
        flags.update(parse_inline_flags(inline_match.group(1)))

    # Check for YAML block
    if 'flags:' in user_input.lower():
        yaml_section = extract_yaml_section(user_input)
        flags.update(parse_yaml_flags(yaml_section))

    # Check for natural language
    flags.update(parse_natural_language(user_input))

    return flags
```

### Step 3: Validate Flag Values

```python
def validate_flags(flags):
    """
    Validate flag values and apply constraints

    Raises: ValueError if invalid
    """
    # Validate approve_before_stage
    if flags['approve_before_stage']:
        for stage in flags['approve_before_stage']:
            if not isinstance(stage, int) or stage < 1 or stage > 9:
                raise ValueError(f"Invalid stage number: {stage}")

    # Validate approve_at_risk
    if flags['approve_at_risk']:
        valid_risks = ['low', 'medium', 'high']
        if flags['approve_at_risk'].lower() not in valid_risks:
            raise ValueError(f"Invalid risk level: {flags['approve_at_risk']}")

    # Validate approve_before_skills
    if flags['approve_before_skills']:
        available_skills = get_available_skills()
        for skill in flags['approve_before_skills']:
            if skill not in available_skills:
                raise ValueError(f"Unknown skill: {skill}")

    # Validate checkpoint_strategy
    if flags['checkpoint_strategy']:
        valid_strategies = ['analysis_only', 'planning_only', 'both', 'none']
        if flags['checkpoint_strategy'] not in valid_strategies:
            raise ValueError(f"Invalid strategy: {flags['checkpoint_strategy']}")

    return True
```

### Step 4: Apply Defaults

```python
def apply_defaults(flags):
    """
    Apply default values for missing flags
    """
    defaults = {
        'approve_before_stage': [],
        'approve_at_risk': None,
        'approve_before_skills': [],
        'manual_mode': False,
        'checkpoint_strategy': None
    }

    for key, default_value in defaults.items():
        if key not in flags or flags[key] is None:
            flags[key] = default_value

    return flags
```

---

## Execution Context Creation

### Context Structure

```yaml
execution_context:
  # Original user request
  request: <cleaned request text>

  # Detected workflow mode
  mode: <FEATURE|BUG|SPIKE|HOTFIX|PERFORMANCE|REFINEMENT>

  # Execution flags
  flags:
    approve_before_stage: [<stages>]
    approve_at_risk: <threshold>
    approve_before_skills: [<skills>]
    manual_mode: <boolean>
    checkpoint_strategy: <strategy>

  # Derived execution mode
  execution_mode: <autonomous|manual|hybrid>

  # Agent configuration
  agent:
    name: <agent_name>
    default_checkpoints: [<stages>]
    auto_stop_conditions: [<conditions>]

  # Runtime state
  current_stage: 0
  completed_stages: []
  pending_checkpoints: []
  risk_level: <LOW|MEDIUM|HIGH>
```

### Execution Mode Determination

```python
def determine_execution_mode(flags):
    """
    Determine overall execution mode from flags
    """
    if flags['manual_mode']:
        return 'manual'

    if (flags['approve_before_stage'] or
        flags['approve_at_risk'] or
        flags['approve_before_skills'] or
        flags['checkpoint_strategy']):
        return 'hybrid'

    return 'autonomous'
```

---

## Flag Priority and Conflicts

### Priority Order (Highest to Lowest)

1. `manual_mode` - Overrides all other flags
2. Auto-stop conditions - Cannot be overridden
3. `approve_at_risk` - Triggers on risk threshold
4. `approve_before_stage` - Explicit stage pauses
5. `approve_before_skills` - Skill-specific pauses
6. `checkpoint_strategy` - General checkpoint placement
7. Agent default checkpoints - Fallback

### Conflict Resolution

```yaml
# If manual_mode is true, ignore other flags
manual_mode: true
approve_before_stage: [6]  # IGNORED
→ Result: Pause after every stage

# If approve_at_risk and approve_before_stage both trigger
approve_at_risk: medium
approve_before_stage: [5]
# Stage 5 detects medium risk
→ Result: Single checkpoint (don't pause twice)

# If checkpoint_strategy conflicts with approve_before_stage
checkpoint_strategy: analysis_only  # Pause after stage 5
approve_before_stage: [6]           # Pause before stage 6
→ Result: Both checkpoints apply (different purposes)
```

---

## Natural Language Translation

### Common Phrases to Flags

```yaml
# Pause before implementation
"pause before implementation"
"stop before coding"
"approve before changes"
→ approve_before_stage: [6]

# Risk-based pausing
"pause on medium risk"
"stop if risky"
"review high-risk changes"
→ approve_at_risk: medium

# Manual mode
"step by step"
"manual control"
"approve each stage"
→ manual_mode: true

# Analysis checkpoint
"review after analysis"
"pause before planning"
→ checkpoint_strategy: analysis_only
```

### Translation Algorithm

```python
def parse_natural_language(text):
    """
    Translate natural language into execution flags
    """
    flags = {}

    text_lower = text.lower()

    # Check for manual mode keywords
    manual_keywords = ['step by step', 'manual mode', 'approve each']
    if any(kw in text_lower for kw in manual_keywords):
        flags['manual_mode'] = True

    # Check for risk keywords
    if 'medium risk' in text_lower or 'risky' in text_lower:
        flags['approve_at_risk'] = 'medium'
    elif 'high risk' in text_lower:
        flags['approve_at_risk'] = 'high'

    # Check for stage keywords
    if 'before implementation' in text_lower or 'before coding' in text_lower:
        flags['approve_before_stage'] = [6]
    elif 'before planning' in text_lower or 'after analysis' in text_lower:
        flags['checkpoint_strategy'] = 'analysis_only'

    return flags
```

---

## Output Format Examples

### Example 1: Full Autonomous

```yaml
input: "Add Excel export to customer list"

parsed_context:
  request: "Add Excel export to customer list"
  mode: FEATURE
  flags:
    approve_before_stage: []
    approve_at_risk: null
    approve_before_skills: []
    manual_mode: false
    checkpoint_strategy: null
  execution_mode: autonomous

behavior:
  - Execute all stages 1-9 in batch
  - Pause only on auto-stop conditions
  - Return complete analysis and plan
```

### Example 2: Checkpoint Before Implementation

```yaml
input: "Add Excel export [approve_before_stage: 6]"

parsed_context:
  request: "Add Excel export"
  mode: FEATURE
  flags:
    approve_before_stage: [6]
    approve_at_risk: null
    approve_before_skills: []
    manual_mode: false
    checkpoint_strategy: null
  execution_mode: hybrid

behavior:
  - Execute stages 1-5 (analysis) in batch
  - CHECKPOINT: Present analysis, request approval
  - Execute stages 6-9 (planning) after approval
  - Return complete plan
```

### Example 3: Risk-Based Pausing

```yaml
input: |
  Optimize customer search query
  Flags:
    approve_at_risk: medium

parsed_context:
  request: "Optimize customer search query"
  mode: PERFORMANCE
  flags:
    approve_before_stage: []
    approve_at_risk: medium
    approve_before_skills: []
    manual_mode: false
    checkpoint_strategy: null
  execution_mode: hybrid

behavior:
  - Execute stages 1-3 normally
  - Stage 4 detects MEDIUM risk
  - CHECKPOINT: Present risk analysis, request approval
  - Continue stages 5-7 after approval
```

### Example 4: Full Manual Mode

```yaml
input: "Add Excel export [manual_mode: true]"

parsed_context:
  request: "Add Excel export"
  mode: FEATURE
  flags:
    approve_before_stage: []
    approve_at_risk: null
    approve_before_skills: []
    manual_mode: true
    checkpoint_strategy: null
  execution_mode: manual

behavior:
  - Execute stage 1, pause
  - Execute stage 2, pause
  - Execute stage 3, pause
  - ... (repeat for all 9 stages)
```

---

## Integration with Agents

### Agent Receives Execution Context

```yaml
agent_invocation:
  agent: feature-delivery
  context:
    request: <cleaned request>
    flags: <parsed flags>
    execution_mode: <mode>

agent_behavior:
  # Load agent configuration
  config = load_agent_config('feature-delivery')

  # Merge flags with agent defaults
  checkpoints = merge_checkpoints(config.default_checkpoints, flags)
  stops = merge_stops(config.auto_stops, flags)

  # Execute with configuration
  if execution_mode == 'autonomous':
    execute_batch(all_stages, stops)
  elif execution_mode == 'manual':
    execute_step_by_step(all_stages)
  else:  # hybrid
    execute_batch_with_checkpoints(all_stages, checkpoints, stops)
```

---

## Error Handling

### Invalid Flag Values

```yaml
error_handling:
  invalid_stage:
    input: "approve_before_stage: [10]"
    error: "Invalid stage number: 10. Valid range: 1-9"
    action: Request correction from user

  invalid_risk:
    input: "approve_at_risk: critical"
    error: "Invalid risk level: critical. Valid: low, medium, high"
    action: Request correction from user

  invalid_skill:
    input: "approve_before_skills: [unknown-skill]"
    error: "Unknown skill: unknown-skill"
    action: Show available skills, request correction
```

### Conflicting Flags

```yaml
conflict_handling:
  manual_with_other_flags:
    input:
      manual_mode: true
      approve_before_stage: [6]
    warning: "manual_mode overrides approve_before_stage"
    resolution: Use manual_mode, ignore other flags

  checkpoint_strategy_with_stages:
    input:
      checkpoint_strategy: analysis_only
      approve_before_stage: [6]
    warning: "Both will apply, may result in multiple pauses"
    resolution: Keep both, inform user
```

---

## Testing and Validation

### Test Cases

```yaml
test_suite:

  test_no_flags:
    input: "Add Excel export"
    expected:
      flags:
        approve_before_stage: []
        manual_mode: false
      execution_mode: autonomous

  test_inline_flag:
    input: "Add Excel export [approve_before_stage: 6]"
    expected:
      flags:
        approve_before_stage: [6]
      execution_mode: hybrid

  test_yaml_flags:
    input: |
      Add Excel export
      Flags:
        approve_before_stage: [6]
        approve_at_risk: medium
    expected:
      flags:
        approve_before_stage: [6]
        approve_at_risk: medium
      execution_mode: hybrid

  test_manual_mode:
    input: "Add Excel export [manual_mode: true]"
    expected:
      flags:
        manual_mode: true
      execution_mode: manual

  test_natural_language:
    input: "Add Excel export, but pause before implementation"
    expected:
      flags:
        approve_before_stage: [6]
      execution_mode: hybrid
```

---

## Summary

This flag parser enables flexible execution control:

- **Autonomous by default** - No flags means full batch execution
- **Flexible control** - Multiple flag types for different needs
- **Multiple formats** - Inline, YAML, or natural language
- **Validation** - Catches errors before execution
- **Conflict resolution** - Clear priority rules
- **Agent integration** - Seamless handoff to specialized agents

**The parser transforms user intent into precise execution control.**
