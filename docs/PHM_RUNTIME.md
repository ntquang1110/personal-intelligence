# Personal Human Map runtime scaffold

## What this delivers

`scripts/phm_run.py` is the first executable PHM pipeline step. It accepts a JSON evidence/claims packet, validates basic input shape, checks claim-to-evidence references, warns when multiple records share one source lineage, flags missing counterevidence and competing mechanisms, enforces the empirical/interpretive boundary, and writes `report.json` plus `report.md`.

It uses only the Python standard library. It does not call a model or external service.

## Run it

From the repository root:

```bash
python scripts/phm_run.py templates/phm-run.template.json --out-dir outputs/phm-run
python -m unittest discover -s tests -v
```

The template is synthetic and must not be mistaken for a real person's profile. Replace it with consented, evidence-backed input before using the pipeline for an actual case.

## Input contract

Top-level fields:
- `subject_ref`: pseudonymous subject identifier; do not put secrets here.
- `purpose`: decision/question the map should support.
- `evidence[]`: records with stable `id`, `text`, `source_type`; optional `source_ref`, `independence_group`, `observed_at`, and `limitations`.
- `claims[]`: records with stable `claim_id`, `claim`, optional `claim_class`, `status`, `confidence`, `evidence_refs[]`, `counterevidence_refs[]`, and `mechanisms[]`.
- `interpretive_items[]`: optional symbolic interpretations, kept in a separate output lane and never used as empirical support.

Each mechanism should include its description, predicted observations, weakening/counterevidence, and a discriminating test. Do not invent data to complete missing fields.

## Release statuses

- `fail`: structural blocker exists, such as an unknown evidence reference or symbolic source supporting an empirical claim.
- `provisional`: no structural blocker, but warnings remain.
- `structural_pass`: no structural warnings were found. This is **not** a semantic quality pass or evidence of independent review.

## Critical limitation

The two review entries in output are explicit gates, not claims that red-team reviews were performed. Semantic critique still requires an LLM or human reviewer and must be recorded separately. The next implementation step is a model adapter/orchestrator that runs draft → red-team 1 → revision → red-team 2 → release rubric, stores each artifact/version, and only then marks semantic review complete.
