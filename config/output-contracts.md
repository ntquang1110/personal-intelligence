# Shared Output Contracts

## Human-readable report

Each report should use this structure where relevant:

1. Purpose and scope
2. Evidence available and missing
3. Findings grouped by claim class
4. Supporting evidence and counterevidence
5. Confidence and limitations
6. Implications
7. Recommended next actions
8. Questions or validation steps
9. Handoff to downstream skills

Omit irrelevant headings rather than filling them with boilerplate.

## Structured records

Use schemas in `schemas/`. Every structured artifact should include:
- `schema_version`
- `created_at` if known; otherwise omit or use `null` only where schema allows it
- stable IDs
- provenance
- explicit unknowns

Do not include raw sensitive information unless necessary and authorized. Prefer summaries and source references.

## Handoff contract

A skill handoff should provide:
- `artifact_id`
- `artifact_type`
- `summary`
- `claims` with evidence class and confidence
- `limitations`
- `open_questions`
- `recommended_next_skills`

Downstream skills must preserve claim class and uncertainty. They may challenge upstream claims but must not silently upgrade a hypothesis to a validated conclusion.

## Output quality bar

A report is useful if the user can tell:
- what is known;
- why it is believed;
- what is uncertain;
- what decision or action it changes;
- how progress will be measured.
