# Specifications (Archived)

## Note
The original specs folder contained detailed specifications for an execution control system with checkpoint mechanisms. These have been removed as they are not applicable to GitHub Copilot's conversational model.

## Current Approach

Instead of runtime execution control, this framework provides:

1. **Structured Workflows** - Clear stage-by-stage processes
   - See: `agents/` for workflow definitions

2. **Analysis Skills** - Specialized analysis capabilities
   - See: `skills/` for 28 categorized skills

3. **Coding Standards** - Best practices and patterns
   - See: `instructions/` for modular standards
   - See: Root `copilot-instructions.md` for quick reference

4. **Output Structure** - Saving stage outputs
   - See: `../OUTPUT_STRUCTURE.md` for details

## Integration with Copilot

GitHub Copilot works conversationally:
- User requests analysis or planning
- Copilot generates complete response
- User reviews and requests adjustments
- Process repeats as needed

No checkpoint mechanisms, execution flags, or approval gates.

## Documentation

**Quick Start:** `instructions/quick-start-guide.md`
**Skills Catalog:** `skills/README.md`
**Coding Standards:** `instructions/`
**Agents:** `agents/`

---

**Last Updated:** 2026-03-28
