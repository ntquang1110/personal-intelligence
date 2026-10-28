#!/usr/bin/env python3
"""Validate and render a structured Personal Human Map JSON artifact."""
from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator
except ImportError:
    Draft202012Validator = None  # type: ignore[assignment]

ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot read valid JSON from {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError("Map root must be a JSON object.")
    return value


def schema_with_local_refs() -> dict[str, Any]:
    schema = load_json(ROOT / "schemas" / "human-map.schema.json")
    synthesis = load_json(ROOT / "schemas" / "cross-assessment-synthesis.schema.json")
    schema = copy.deepcopy(schema)
    schema["properties"]["assessment_synthesis"] = synthesis
    return schema


def validate_map(data: dict[str, Any]) -> list[str]:
    if Draft202012Validator is None:
        return ["Install jsonschema to validate map schema: python -m pip install jsonschema"]
    schema = schema_with_local_refs()
    Draft202012Validator.check_schema(schema)
    errors = [
        f"schema at {'/'.join(str(p) for p in err.absolute_path) or '<root>'}: {err.message}"
        for err in Draft202012Validator(schema).iter_errors(data)
    ]

    inventory = data.get("evidence_inventory", [])
    evidence_by_ref = {
        item.get("source_ref"): item
        for item in inventory if isinstance(item, dict) and isinstance(item.get("source_ref"), str)
    }
    claim_ids = {
        item.get("claim_id")
        for item in data.get("claims", []) if isinstance(item, dict)
    }
    for claim in data.get("claims", []):
        if not isinstance(claim, dict):
            continue
        cid = claim.get("claim_id", "<unknown>")
        for field in ("evidence_refs", "counterevidence_refs"):
            for ref in claim.get(field, []) if isinstance(claim.get(field, []), list) else []:
                if ref not in evidence_by_ref:
                    errors.append(f"claim {cid}: {field} references unknown evidence {ref!r}")
                elif field == "evidence_refs" and claim.get("claim_class") != "unknown" and evidence_by_ref[ref].get("source_type") == "interpretive_system":
                    errors.append(f"claim {cid}: symbolic/interpretive evidence {ref!r} cannot support an empirical claim")

    synthesis = data.get("assessment_synthesis", {})
    for construct in synthesis.get("constructs", []) if isinstance(synthesis, dict) else []:
        if not isinstance(construct, dict):
            continue
        for ref in construct.get("behavioral_evidence_refs", []):
            if ref not in evidence_by_ref:
                errors.append(f"construct {construct.get('construct_id', '<unknown>')}: unknown behavioral evidence {ref!r}")
        for finding in construct.get("assessment_findings", []):
            if not isinstance(finding, dict):
                continue
            aid = finding.get("assessment_id")
            if aid and aid not in evidence_by_ref:
                errors.append(f"construct {construct.get('construct_id', '<unknown>')}: assessment_id {aid!r} missing from evidence inventory")
            result_ref = finding.get("result_ref")
            if result_ref and result_ref not in evidence_by_ref:
                errors.append(f"construct {construct.get('construct_id', '<unknown>')}: result_ref {result_ref!r} missing from evidence inventory")
            if result_ref in evidence_by_ref and finding.get("lane") == "empirical" and evidence_by_ref[result_ref].get("source_type") == "interpretive_system":
                errors.append(f"construct {construct.get('construct_id', '<unknown>')}: interpretive source {result_ref!r} cannot support empirical assessment findings")

    for entry in data.get("change_log", []):
        if not isinstance(entry, dict):
            continue
        for cid in entry.get("changed_claim_ids", []):
            if cid not in claim_ids:
                errors.append(f"change log version {entry.get('version')}: references unknown claim {cid!r}")
        for ref in entry.get("triggering_evidence_refs", []):
            if ref not in evidence_by_ref:
                errors.append(f"change log version {entry.get('version')}: references unknown evidence {ref!r}")

    for action in data.get("next_actions", []):
        if not isinstance(action, dict):
            continue
        for cid in action.get("linked_claim_ids", []):
            if cid not in claim_ids:
                errors.append(f"next action references unknown claim {cid!r}")
    return errors


def render_markdown(data: dict[str, Any]) -> str:
    lines = [
        "# Personal Human Map",
        "",
        f"- Map ID: {data.get('map_id', 'unknown')}",
        f"- Subject reference: {data.get('subject_ref', 'unknown')}",
        f"- Purpose: {data.get('purpose', 'not stated')}",
        f"- Created: {data.get('created_at') or 'not recorded'}",
        f"- Updated: {data.get('updated_at') or 'not recorded'}",
        "",
        "> Interpret claims according to their evidence class and confidence. A structurally valid map is not a psychological diagnosis or proof that every claim is true.",
        "",
        "## Evidence inventory",
    ]
    for item in data.get("evidence_inventory", []):
        lines.append(f"- **{item.get('source_ref', 'unknown')}** ({item.get('source_type', 'unknown')}): {item.get('context') or 'context not recorded'}")
        for limitation in item.get("limitations", []):
            lines.append(f"  - Limitation: {limitation}")
    lines.extend(["", "## Whole-person domains"])
    domain_labels = {
        "context": "Context", "personality": "Personality", "cognition": "Cognitive process",
        "motivation": "Motivation and values", "capabilities": "Capabilities",
        "behavior": "Behavior and execution", "environment_fit": "Environment and collaboration fit",
        "blind_spots": "Blind spots", "development": "Development direction",
        "stress_recovery": "Stress and recovery (non-clinical)",
        "strengths_and_costs": "Strengths and costs by context",
        "contradictions": "Contradictions and unresolved tensions",
    }
    for key, label in domain_labels.items():
        lines.extend(["", f"### {label}"])
        values = data.get("domains", {}).get(key, [])
        lines.extend([f"- {value}" for value in values] if values else ["- Unknown / insufficient evidence."])
    lines.extend(["", "## Evidence-linked claims"])
    for claim in data.get("claims", []):
        lines.extend([
            "",
            f"### {claim.get('claim_id', 'claim')} — {claim.get('status', 'unclassified')}",
            claim.get("claim", ""),
            f"- Domain: {claim.get('domain', 'unspecified')}",
            f"- Class: {claim.get('claim_class', 'unspecified')}; confidence: {claim.get('confidence', 'not assessed')}",
            f"- Evidence: {', '.join(claim.get('evidence_refs', [])) or 'none'}",
            f"- Counterevidence: {', '.join(claim.get('counterevidence_refs', [])) or 'none recorded'}",
        ])
        if claim.get("mechanism"):
            lines.append(f"- Proposed mechanism: {claim['mechanism']}")
        for alternative in claim.get("alternatives", []):
            lines.append(f"- Alternative: {alternative}")
        for condition in claim.get("scope_conditions", []):
            lines.append(f"- Scope: {condition}")
    lines.extend(["", "## Cross-assessment synthesis"])
    synthesis = data.get("assessment_synthesis", {})
    for construct in synthesis.get("constructs", []):
        lines.extend([
            "",
            f"### {construct.get('construct', 'Unspecified construct')}",
            f"- Definition: {construct.get('working_definition', 'not defined')}",
            f"- Agreement: {'; '.join(construct.get('agreement', [])) or 'none established'}",
            f"- Disagreement: {'; '.join(construct.get('disagreement', [])) or 'none recorded'}",
            f"- Context moderators: {'; '.join(construct.get('context_moderators', [])) or 'not assessed'}",
            f"- Confidence: {construct.get('confidence', {}).get('level', 'not assessed')} — {construct.get('confidence', {}).get('rationale', '')}",
        ])
        for finding in construct.get("assessment_findings", []):
            lines.append(f"- Assessment {finding.get('instrument', finding.get('assessment_id'))}: {finding.get('finding')} [lane: {finding.get('lane')}]")
        for alternative in construct.get("alternatives", []):
            lines.append(f"- Rival explanation: {alternative.get('explanation')}; distinguish by: {alternative.get('distinguishing_observation')}")
        for plan in construct.get("validation_plan", []):
            lines.append(f"- Validation: {plan}")
    lines.extend(["", "## Unknowns and validation plan"])
    for item in data.get("unknowns", []):
        lines.append(f"- **Unknown:** {item.get('question')} Why it matters: {item.get('why_it_matters')} How to resolve: {item.get('how_to_resolve')}")
    lines.extend(["", "## Next actions"])
    for item in data.get("next_actions", []):
        lines.append(f"- [ ] {item.get('action')} — Success measure: {item.get('measure_of_success')} (claims: {', '.join(item.get('linked_claim_ids', [])) or 'none'})")
    synthesis_limits = synthesis.get("global_limitations", [])
    if synthesis_limits:
        lines.extend(["", "## Synthesis limitations", *[f"- {x}" for x in synthesis_limits]])
    if data.get("interpretive_appendix"):
        lines.extend(["", "## Interpretive-only appendix", "This section is separate from empirical findings."])
        lines.extend(f"- {x}" for x in data["interpretive_appendix"].get("interpretation", []))
    lines.extend(["", "## Longitudinal change log"])
    history = data.get("change_log", [])
    if history:
        for entry in history:
            lines.append(f"- Version {entry.get('version')}: {entry.get('summary')} (changed at: {entry.get('changed_at') or 'not recorded'}; claims: {', '.join(entry.get('changed_claim_ids', [])) or 'none listed'}; triggering evidence: {', '.join(entry.get('triggering_evidence_refs', [])) or 'none listed'})")
    else:
        lines.append("- No previous version recorded; this is the baseline map.")
    lines.extend(["", "## Release status", f"- Map version: {data.get('map_version', 'not recorded')}", f"- Synthesis review status: {synthesis.get('review_status', 'not recorded')}", "- Schema/reference checks passed. This does not certify psychometric validity or independent review.", ""])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("map_json", type=Path)
    parser.add_argument("--out", type=Path, help="Markdown output path; defaults beside input as report.md")
    args = parser.parse_args(argv)
    try:
        data = load_json(args.map_json)
        errors = validate_map(data)
        if errors:
            print("Map validation failed:\n" + "\n".join(f"- {e}" for e in errors), file=sys.stderr)
            return 2
        output = args.out or args.map_json.parent / "report.md"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(render_markdown(data), encoding="utf-8")
        print(json.dumps({"validation": "passed", "markdown": str(output), "map_id": data.get("map_id")}, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
