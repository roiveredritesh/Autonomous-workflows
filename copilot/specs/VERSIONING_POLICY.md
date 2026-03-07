---
version: 1.0.0
last_updated: 2026-03-07
purpose: Versioning, compatibility, and deprecation policy for Copilot workflow docs
---

# Versioning and Deprecation Policy

## Compatibility

- Supported target: `github-copilot-2026`
- Backward compatibility: minor/patch releases should keep existing flags/templates valid.

## Versioning Model

Use semantic versioning for normative docs:
- MAJOR: breaking behavior or template structure changes
- MINOR: new backward-compatible capabilities
- PATCH: clarifications/typos/non-behavioral changes

## Change Classification

A change is behavior-impacting if it modifies any of:
- flag semantics
- safety/risk stop conditions
- mode detection precedence
- required output fields/templates

Behavior-impacting changes MUST:
1. Update version in affected normative file(s)
2. Add changelog entry in commit/PR description
3. Note migration guidance for deprecated fields

## Deprecation Rules

- Minimum deprecation window: 1 minor release.
- Deprecated flags/templates must emit explicit warning text:
  `DEPRECATION_WARNING: <field> will be removed in <version>`
- Remove deprecated behavior only in a MAJOR release.
