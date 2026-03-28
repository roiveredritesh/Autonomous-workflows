# Skill Standardization Template

## Standard Skill Format (v2.0.0)

All skills should follow this structure:

```markdown
---
skill: {skill-name}
version: 2.0.0
category: {analysis|planning|validation|generation|detection}
complexity: {low|medium|high}
estimated_time: {seconds|minutes}
priority: {critical|high|medium|low}
last_updated: 2026-01-18
---

# {Skill Name}

## Quick Example

**Input:** {Brief input description}
**Output:** {Brief output description}
**Time:** {Typical execution time}

---

## Purpose
{Single sentence describing what this skill does}

## Input

```yaml
input:
  required_field: <description>
  optional_field: <description>
```

## Output

```yaml
output:
  result_field: <description>
  confidence: HIGH|MEDIUM|LOW
```

## DO:
✅ {What to do}
✅ {What to do}
✅ {What to do}

## DON'T:
❌ {What not to do}
❌ {What not to do}
❌ {What not to do}

## Error Conditions

**IF {condition}:**
```
1. {Action}
2. Return error: {error message}
```

## Processing Steps

1. **Step 1:** {Description}
2. **Step 2:** {Description}
3. **Step 3:** {Description}

## Example

**Input:**
```yaml
{example input}
```

**Output:**
```yaml
{example output}
```

---

**Related Skills:**
- `{skill-name}` - {description}
- `{skill-name}` - {description}
```

## Target Metrics

- **Length:** 150-250 lines (complex skills up to 300 lines max)
- **Quick example:** Within first 30 lines
- **Clear sections:** Easy to scan
- **Actionable:** Focus on what to do

## Categories

- **analysis**: Analyzes code, data, or patterns
- **planning**: Creates plans or strategies
- **validation**: Validates safety, correctness
- **generation**: Generates outputs (docs, tests, code)
- **detection**: Detects issues, patterns, risks

## Complexity Levels

- **low**: Simple, straightforward task (30-60 seconds)
- **medium**: Moderate analysis required (1-3 minutes)
- **high**: Deep analysis, multiple steps (3-10 minutes)

---

**All skills MUST:**
1. Have YAML frontmatter
2. Show quick example at top
3. Have clear input/output formats
4. Include DO/DON'T lists
5. Document error conditions
6. Reference related skills
7. Be 150-300 lines maximum
