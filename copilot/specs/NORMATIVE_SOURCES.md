---
version: 1.0.0
last_updated: 2026-03-07
purpose: Define authoritative (normative) vs informative documents
---

# Normative vs Informative Sources

## Normative (runtime behavior authority)

1. `copilot/COPILOT_INTEGRATION.md`
2. `copilot/TEMPLATES.md`
3. `copilot/specs/EXECUTION_RULES.md`

If conflicts exist, resolve in this order:
1) Safety rules in `EXECUTION_RULES.md`
2) Runtime flow in `COPILOT_INTEGRATION.md`
3) Output format in `TEMPLATES.md`

## Informative (guidance/training only)

- `copilot/README.md`
- `copilot/instructions/*.md`
- `copilot/examples/*`
- `copilot/BEST_PRACTICES_AUDIT.md`
- `copilot/COPILOT_ONLY_IMPROVEMENT_REVIEW.md`

These files must not redefine flags/safety behavior in conflicting ways.

## Maintenance Rules

- Any behavior change MUST be updated in normative docs first.
- Informative docs SHOULD link to normative docs instead of duplicating rules.
- Validation checks should fail if normative references are missing or broken.
