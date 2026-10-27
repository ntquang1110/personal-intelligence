# Architecture

## Principle: one profile, many lenses
The canonical local file `data/profile.json` is the working model. Domain modules and engines update it through evidence-backed changes rather than creating unrelated conclusions.

## Layers
1. Conversation interface.
2. Orchestrator chooses workflow based on goal, evidence gaps, and stage.
3. Evidence store records claims, sources, dates, confidence, and contradictions.
4. Twelve domain modules collect and interpret information.
5. Analysis engines synthesize patterns, bottlenecks, career options, life strategy, and actions.
6. Output layer generates human-readable reports and JSON exports.
7. Feedback loop updates conclusions after experiments and new evidence.

## Data flow
`Conversation/documents → evidence items → domain summaries → integrated profile → diagnostic hypotheses → options/trade-offs → action plan → progress review → profile update`

## Local data
Copy templates into `data/profile.json`, `data/evidence.json`, `data/decisions.json`, and `data/experiments.json`. Keep populated files private; commit templates and schemas only.

## Modules
- `skills/`: portable workflow instructions.
- `domains/`: 12 discovery and analysis guides.
- `engines/`: evidence, diagnostic, strategy, prioritization, feedback.
- `schemas/`: contracts for structured records.
- `templates/`: empty starter records.
- `prompts/`: reusable entry points and reviews.
- `tests/`: repository integrity checks.

Markdown and JSON keep the system portable across model vendors. No API key or specific vendor is required.
