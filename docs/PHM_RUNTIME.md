# Personal Human Map runtime

## Two execution modes

### 1. Deterministic structural checks (no API required)

```bash
python scripts/phm_run.py templates/phm-run.template.json --out-dir outputs/phm-run
python -m unittest discover -s tests -v
```

This mode checks input shape, claim-to-evidence references, source lineage, counterevidence, competing mechanisms, and symbolic/empirical lane separation. It writes `report.json` and `report.md`. A `structural_pass` is not a semantic quality pass.

### 2. Model-assisted five-phase pipeline

The model runner calls an OpenAI-compatible Chat Completions API in five sequential phases: draft → red-team round 1 → revision → red-team round 2 → user-fit/release gate. Each phase is written separately so the critique trail is inspectable.

Set credentials in environment variables; never hardcode secrets:

**PowerShell**
```powershell
$env:PHM_API_KEY = "your-api-key"
$env:PHM_MODEL = "your-model-name"
$env:PHM_API_BASE_URL = "https://api.openai.com/v1"
python scripts/phm_llm_run.py templates/phm-run.template.json --out-dir outputs/phm-llm-run
```

**Bash**
```bash
export PHM_API_KEY="your-api-key"
export PHM_MODEL="your-model-name"
export PHM_API_BASE_URL="https://api.openai.com/v1"
python scripts/phm_llm_run.py templates/phm-run.template.json --out-dir outputs/phm-llm-run
```

For another provider, set `PHM_API_BASE_URL` to an endpoint compatible with `/chat/completions`. The provider's model and response format must be compatible with that API contract. The API key is read from the environment and is never written into output files.

## Input contract

Top-level fields:
- `subject_ref`: pseudonymous subject identifier; do not put secrets here.
- `purpose`: decision/question the map should support.
- `evidence[]`: records with stable `id`, `text`, `source_type`; optional `source_ref`, `independence_group`, `observed_at`, and `limitations`.
- `claims[]`: records with stable `claim_id`, `claim`, optional `claim_class`, `status`, `confidence`, `evidence_refs[]`, `counterevidence_refs[]`, and `mechanisms[]`.
- `interpretive_items[]`: optional symbolic interpretations, kept in a separate output lane and never used as empirical support.

The included template is synthetic. Replace it with consented, evidence-backed input before using the pipeline for an actual case. Do not invent data to complete missing fields.

## Outputs and gates

- Deterministic mode: `report.json` and `report.md`.
- Model-assisted mode: `run.json`, final `report.md`, and phase artifacts `draft.md`, `red_team_1.md`, `revision.md`, `red_team_2.md`, `user_fit_gate.md`.
- Structural `fail`: blocker exists, such as an unknown evidence reference or symbolic source supporting an empirical claim.
- Structural `provisional`: no blocker, but warnings remain.
- Structural `structural_pass`: no structural warnings; this does not validate truth or semantic quality.

## Critical limitations

The model runner is an orchestration scaffold, not an independent reviewer. All critique phases use the configured model and can share its blind spots. The result remains provisional and human review is recommended, especially for consequential decisions. Model provider retention/data-processing terms apply; use pseudonymous, consented inputs and avoid unnecessary sensitive data. The pipeline does not provide persistent database storage, automatic memory, validated psychometric scoring, or longitudinal outcome collection. Those remain separate implementation tasks.
