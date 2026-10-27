# Personal Intelligence Skills

A portable, evidence-driven system for self-understanding and personal development. It uses Markdown for operational instructions and human-readable reports, and JSON for structured records.

## Portability and runtime assumptions

This project intentionally uses plain Markdown and JSON rather than platform-specific frontmatter, tool APIs, or agent directives. Each `skills/<id>/SKILL.md` is an independent skill specification that can be adapted to a skill-capable agent runtime. No external integrations are assumed.

- **Input:** user-provided answers, conversation history only when actually available, user-authorized files, and explicitly provided feedback or measurements.
- **Output:** Markdown reports plus JSON records when structured data is useful.
- **Persistence:** the agent must not claim data was saved unless the runtime actually writes the files.
- **Privacy:** collect only information relevant to the user's stated purpose. Do not solicit secrets or unnecessary sensitive data.
- **Not a clinical tool:** outputs are reflective coaching and planning, not psychological diagnosis, IQ testing, or medical advice.

## Quick start

1. Read `config/evidence-policy.md`, `config/interview-policy.md`, and `config/output-contracts.md`.
2. Start with `skills/00-orchestrator/SKILL.md`.
3. The orchestrator inventories available evidence and proposes a staged plan. It should provide useful preliminary results before asking additional questions.
4. Run only the skills relevant to the user's goal. Skills can also be run independently.
5. Save each run's outputs to `outputs/` if the runtime supports file writing. Use a date or session identifier in filenames when retaining multiple versions.
6. Run `python -m unittest discover -s tests -v` to check schema contracts, required skill files, dependencies, and evidence rules.

## Suggested sequence

`SK00 → SK01–SK06 → SK07–SK09 → SK10–SK12 → SK13`

This is a suggested dependency flow, not a requirement to run every skill. Do not delay a useful answer just because unrelated modules are incomplete.

## Directory map

- `skills/`: 14 independent skill specifications.
- `config/`: evidence, interview, and output policies.
- `schemas/`: JSON Schemas for shared structured records.
- `examples/`: clearly synthetic example data and output.
- `tests/`: portable Python standard-library validation tests.
- `outputs/`: destination for generated reports; contains a manifest explaining intended use.

## Shared matching core

Career fit and partner/marriage compatibility use the same explainable comparison engine and record contract, with context-specific criteria. The engine compares each side's stated needs and evidence, distinguishes alignment from complementary differences, conflicts and unknowns, and recommends questions or low-risk experiments. It does not calculate a universal compatibility score or make automatic hiring/relationship decisions.

Read `engines/matching/ENGINE.md`, `MATCHING_CRITERIA_CATALOG.md`, and `prompts/START_MATCHING.md`. The example in `templates/match-assessment.template.json` uses synthetic data only.

## Runtime contract

A compliant runtime should:
- Inspect these instructions before acting.
- Check which source data is available.
- Keep claim provenance and uncertainty.
- Ask one high-value question at a time by default.
- Avoid repeating answered questions.
- Never invent history, outcomes, external feedback, scores, or persistence.
- Return partial but useful analysis when evidence supports it.
- State what remains unknown and what evidence would resolve it.

## Data handling and versioning

Use ISO 8601 timestamps where known. Use stable IDs such as `claim-001`, `event-001`, and `experiment-001`. Store dates as dates only when the exact date is known. Do not infer precise dates from vague recollection. Each artifact should identify its schema version and creation date if known.

Suggested file names:
- `outputs/YYYY-MM-DD-self-discovery.md`
- `outputs/YYYY-MM-DD-evidence.json`
- `outputs/YYYY-MM-DD-capability-map.json`
- `outputs/YYYY-MM-DD-progress-report.md`

## Limitations

This repository provides operational prompts and validation scaffolding; it does not itself include a language model, automatic memory, external connectors, or a user database. Uploading it does not create persistent memory or write results back to GitHub. The tests check repository contracts and sample consistency; strict JSON Schema validation should also run in CI with a Draft 2020-12 validator when available.
