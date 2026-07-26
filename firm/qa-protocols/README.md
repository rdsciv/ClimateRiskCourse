# QA protocols

## Before any number ships

1. **Re-run test:** Can a cold session re-execute the script and match?
2. **Lineage test:** Does each figure point to script path + input table + anchor or judgment note?
3. **Label test:** Are judged figures labeled **judgment**?
4. **Gap test:** Are unknowns listed rather than smoothed?
5. **Scenario test:** Are scenarios presented as alternatives (not additive)?

## Agent QA pass (week 6 skill)

Open a **fresh** Grok session (or subagent) with only:

- the deliverable
- `firm/qa-protocols/`
- output tables

Prompt: “Challenge every material figure. List failures only.”

Do not let the authoring session grade itself without a second pass.
