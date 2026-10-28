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

## Personal Human Map executable scaffold

The PHM branch now includes a deterministic pipeline scaffold:

```bash
python scripts/phm_run.py templates/phm-run.template.json --out-dir outputs/phm-run
python -m unittest discover -s tests -v
```

It emits JSON and Markdown artifacts, checks claim/evidence references and source lineage, flags missing counterevidence or competing mechanisms, and prevents symbolic sources from supporting empirical claims. The included template is synthetic. Read [docs/PHM_RUNTIME.md](docs/PHM_RUNTIME.md) before using it.

**Important:** this is a structural pipeline, not yet an LLM-backed autonomous workflow. It does not generate semantic analysis or perform independent red-team reviews. Its output labels those limitations explicitly; a clean structural result is not a semantic release pass.

## Whole-person map and cross-assessment synthesis

The human-map contract now requires construct-level cross-assessment synthesis, a complete multi-domain map, and an explicit version/change log for longitudinal updates. See [cross-assessment synthesis guide](docs/CROSS_ASSESSMENT_SYNTHESIS.md), [cross-assessment schema](schemas/cross-assessment-synthesis.schema.json), and the explicitly synthetic [whole-person template](templates/phm-human-map.template.json). The synthesis records agreement and disagreement separately, tracks source lineage and context moderators, and proposes tests for competing explanations. It does not average incompatible scores or invent absent personality-test results.

## Personal Human Map executable pipeline

Two execution modes are available:

- **Structural checks (no API):** `python scripts/phm_run.py templates/phm-run.template.json --out-dir outputs/phm-run`
- **Model-assisted five-phase review + structured-map pipeline:** set `PHM_API_KEY`, `PHM_MODEL`, and optionally `PHM_API_BASE_URL`, then run `python scripts/phm_llm_run.py templates/phm-run.template.json --out-dir outputs/phm-llm-run`.

The model-assisted runner calls an OpenAI-compatible Chat Completions API for draft → red-team round 1 → revision → red-team round 2 → user-fit/release gate, then requests a schema-conforming structured map and validates it. A valid map is written as `human-map.json` and rendered to Markdown; invalid output is retried up to three times and fails closed. The renderer includes all whole-person domains and longitudinal change history. The included template is synthetic. See [docs/PHM_RUNTIME.md](docs/PHM_RUNTIME.md) for the input contract, configuration, privacy notes, and release limitations.

**Important:** model-generated review is not independent review. The pipeline remains provisional and does not provide a database, automatic memory, validated psychometric scoring, or longitudinal outcome collection. Never hardcode API keys or submit unnecessary sensitive data.

## Suggested sequence

`SK00 → SK01–SK06 → SK07–SK09 → SK10–SK12 → SK13`

This is a suggested dependency flow, not a requirement to run every skill. Do not delay a useful answer just because unrelated modules are incomplete.

## Directory map

- `skills/`: independent skill specifications.
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

This repository provides operational prompts and validation scaffolding; it does not itself include a language model, automatic memory, external connectors, or a user database. The PHM CLI is a local deterministic validator/artifact generator, not an LLM. Persistence is local to the path selected by the person running it. Tests check repository contracts and sample consistency; semantic quality and longitudinal validity require separate evaluation.
