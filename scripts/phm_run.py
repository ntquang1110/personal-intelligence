#!/usr/bin/env python3
"""Deterministic Personal Human Map pipeline scaffold.

This tool validates evidence/claim provenance and emits a reviewable run artifact.
It does NOT call an LLM, infer personality, or claim that semantic red-team review
has occurred. Human/LLM analysis must be supplied in the input claims and review
notes; automated checks here are structural guardrails only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

VERSION = "0.1.0"
INTERPRETIVE_TYPES = {"astrology", "numerology", "horoscope", "tarot", "symbolic"}
EMPIRICAL_CLAIM_CLASSES = {"observation", "inference", "hypothesis", "validated"}


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot read valid JSON from {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError("Input root must be a JSON object.")
    return value


def validate_input(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(data.get("subject_ref"), str) or not data["subject_ref"].strip():
        errors.append("subject_ref must be a non-empty string")
    if not isinstance(data.get("purpose"), str) or not data["purpose"].strip():
        errors.append("purpose must be a non-empty string")
    if not isinstance(data.get("evidence", []), list):
        errors.append("evidence must be an array")
    if not isinstance(data.get("claims", []), list):
        errors.append("claims must be an array")
    assessment_results = data.get("assessment_results", [])
    if not isinstance(assessment_results, list):
        errors.append("assessment_results must be an array")
        assessment_results = []
    valid_lanes = {"empirical", "interpretive_only", "user_meaning"}
    valid_source_types = {"self_report", "performance_task", "observer_feedback", "work_sample", "longitudinal_outcome", "symbolic_interpretation"}
    valid_interpretations = {"scored_per_manual", "qualitative_summary", "unscored", "interpretive_only"}
    seen_assessments: set[str] = set()
    for i, result in enumerate(assessment_results):
        if not isinstance(result, dict):
            errors.append(f"assessment_results[{i}] must be an object")
            continue
        aid = result.get("assessment_id")
        if not isinstance(aid, str) or not aid.strip():
            errors.append(f"assessment_results[{i}].assessment_id must be a non-empty string")
        elif aid in seen_assessments:
            errors.append(f"duplicate assessment_id: {aid}")
        else:
            seen_assessments.add(aid)
        if result.get("lane") not in valid_lanes:
            errors.append(f"assessment_results[{i}].lane is invalid")
        instrument = result.get("instrument")
        if not isinstance(instrument, dict) or not all(isinstance(instrument.get(k), str) and instrument[k].strip() for k in ("name", "purpose")) or "version" not in instrument:
            errors.append(f"assessment_results[{i}].instrument must include name, version, and purpose")
        if result.get("source_type") not in valid_source_types:
            errors.append(f"assessment_results[{i}].source_type is invalid")
        if not isinstance(result.get("results"), list):
            errors.append(f"assessment_results[{i}].results must be an array")
        else:
            for j, finding in enumerate(result["results"]):
                if not isinstance(finding, dict) or not isinstance(finding.get("construct"), str) or not finding.get("construct", "").strip():
                    errors.append(f"assessment_results[{i}].results[{j}].construct is required")
                    continue
                if "value" not in finding:
                    errors.append(f"assessment_results[{i}].results[{j}].value is required (use null if unknown)")
                if finding.get("interpretation_status") not in valid_interpretations:
                    errors.append(f"assessment_results[{i}].results[{j}].interpretation_status is invalid")
        if not isinstance(result.get("limitations"), list):
            errors.append(f"assessment_results[{i}].limitations must be an array")
    seen_evidence: set[str] = set()
    for i, item in enumerate(data.get("evidence", [])):
        if not isinstance(item, dict):
            errors.append(f"evidence[{i}] must be an object")
            continue
        eid = item.get("id")
        if not isinstance(eid, str) or not eid.strip():
            errors.append(f"evidence[{i}].id must be a non-empty string")
        elif eid in seen_evidence:
            errors.append(f"duplicate evidence id: {eid}")
        else:
            seen_evidence.add(eid)
        if not isinstance(item.get("text"), str) or not item["text"].strip():
            errors.append(f"evidence[{i}].text must be a non-empty string")
        if not isinstance(item.get("source_type"), str):
            errors.append(f"evidence[{i}].source_type is required")
    seen_claims: set[str] = set()
    for i, claim in enumerate(data.get("claims", [])):
        if not isinstance(claim, dict):
            errors.append(f"claims[{i}] must be an object")
            continue
        cid = claim.get("claim_id")
        if not isinstance(cid, str) or not cid.strip():
            errors.append(f"claims[{i}].claim_id must be a non-empty string")
        elif cid in seen_claims:
            errors.append(f"duplicate claim id: {cid}")
        else:
            seen_claims.add(cid)
        if not isinstance(claim.get("claim"), str) or not claim["claim"].strip():
            errors.append(f"claims[{i}].claim must be a non-empty string")
        if claim.get("claim_class", "hypothesis") not in EMPIRICAL_CLAIM_CLASSES | {"unknown"}:
            errors.append(f"claims[{i}].claim_class is invalid")
    return errors


def run_checks(data: dict[str, Any]) -> dict[str, Any]:
    evidence = data.get("evidence", [])
    claims = data.get("claims", [])
    evidence_by_id = {e.get("id"): e for e in evidence if isinstance(e, dict) and e.get("id")}
    evidence_ids = set(evidence_by_id)
    independence_groups: dict[str, list[str]] = defaultdict(list)
    for e in evidence:
        if not isinstance(e, dict):
            continue
        group = e.get("independence_group") or e.get("source_ref") or e.get("id", "unknown")
        independence_groups[str(group)].append(str(e.get("id", "unknown")))

    issues: list[dict[str, str]] = []
    claim_results: list[dict[str, Any]] = []
    for claim in claims:
        if not isinstance(claim, dict):
            continue
        cid = str(claim.get("claim_id", "unknown"))
        refs = claim.get("evidence_refs", [])
        counter_refs = claim.get("counterevidence_refs", [])
        refs = refs if isinstance(refs, list) else []
        counter_refs = counter_refs if isinstance(counter_refs, list) else []
        missing_refs = [str(r) for r in refs + counter_refs if r not in evidence_ids]
        if missing_refs:
            issues.append({"severity": "blocker", "claim_id": cid,
                           "issue": "unknown evidence references: " + ", ".join(missing_refs)})
        if not refs and claim.get("claim_class", "hypothesis") not in {"unknown"}:
            issues.append({"severity": "blocker", "claim_id": cid,
                           "issue": "empirical claim has no evidence_refs"})
        groups = sorted({str(evidence_by_id[r].get("independence_group") or
                              evidence_by_id[r].get("source_ref") or r)
                         for r in refs if r in evidence_by_id})
        if len(groups) < len([r for r in refs if r in evidence_by_id]) and len(refs) > 1:
            issues.append({"severity": "warning", "claim_id": cid,
                           "issue": "multiple evidence items share a source lineage; do not count them as independent corroboration"})
        if not counter_refs:
            issues.append({"severity": "warning", "claim_id": cid,
                           "issue": "no counterevidence linked; second red-team review should seek disconfirmation"})
        mechanisms = claim.get("mechanisms", [])
        if not isinstance(mechanisms, list):
            mechanisms = []
        if claim.get("status") not in {"unknown", "retired", "contradicted"} and len(mechanisms) < 2:
            issues.append({"severity": "warning", "claim_id": cid,
                           "issue": "fewer than two competing mechanisms; add alternatives or explain why not applicable"})
        for item in refs:
            ev = evidence_by_id.get(item)
            if ev and str(ev.get("source_type", "")).lower() in INTERPRETIVE_TYPES:
                issues.append({"severity": "blocker", "claim_id": cid,
                               "issue": f"interpretive source {item} cannot support an empirical claim"})
        claim_results.append({
            "claim_id": cid,
            "claim": claim.get("claim", ""),
            "status": claim.get("status", "hypothesis"),
            "claim_class": claim.get("claim_class", "hypothesis"),
            "confidence": claim.get("confidence", "not_assessed"),
            "evidence_refs": refs,
            "counterevidence_refs": counter_refs,
            "mechanism_count": len(mechanisms),
            "source_independence_groups": groups,
            "missing_evidence_refs": missing_refs,
        })

    interpretive_items = data.get("interpretive_items", [])
    if not isinstance(interpretive_items, list):
        interpretive_items = []
        issues.append({"severity": "warning", "claim_id": "run", "issue": "interpretive_items must be an array"})
    # A symbolic lane is report-only and deliberately not read as empirical evidence.
    reviews = [
        {
            "round": 1,
            "focus": "evidence traceability, generic claims, rival mechanisms, missing counterexamples, source dependence",
            "result": "automated structural checks only; semantic red-team review NOT run",
            "open_issues": sum(1 for x in issues if x["severity"] in {"blocker", "warning"}),
        },
        {
            "round": 2,
            "focus": "regressions, constraint-versus-choice attribution, intervention fit, falsifiability, lane separation",
            "result": "automated release-gate recheck only; independent second review NOT run",
            "open_issues": sum(1 for x in issues if x["severity"] in {"blocker", "warning"}),
        },
    ]
    blockers = [x for x in issues if x["severity"] == "blocker"]
    warnings = [x for x in issues if x["severity"] == "warning"]
    status = "fail" if blockers else ("provisional" if warnings else "structural_pass")
    return {
        "pipeline_version": VERSION,
        "run_at": datetime.now(timezone.utc).isoformat(),
        "subject_ref": data.get("subject_ref"),
        "purpose": data.get("purpose"),
        "input_evidence_count": len(evidence),
        "input_claim_count": len(claims),
        "independence_groups": {k: v for k, v in independence_groups.items()},
        "claims": claim_results,
        "interpretive_items_separate_lane": interpretive_items,
        "issues": issues,
        "reviews": reviews,
        "release_status": status,
        "release_note": (
            "FAIL: resolve blockers before use." if blockers else
            "PROVISIONAL: warnings remain; semantic review and longitudinal validation are not established."
            if warnings else
            "STRUCTURAL PASS ONLY: this is not evidence of semantic quality or independent review."
        ),
        "limitations": [
            "This pipeline does not call a language model.",
            "The two review records are structural guardrails, not completed semantic red-team reviews.",
            "A clean structural result does not validate the truth of claims or prove assessment validity.",
            "Input claims and evidence remain user/runtime-supplied; no memory or external sources are fetched.",
        ],
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# Personal Human Map — Pipeline Run",
        "",
        f"- Pipeline: {result['pipeline_version']}",
        f"- Run at: {result['run_at']}",
        f"- Subject ref: {result.get('subject_ref')}",
        f"- Purpose: {result.get('purpose')}",
        f"- Release status: **{result['release_status']}**",
        "",
        "## Summary",
        f"- Evidence items: {result['input_evidence_count']}",
        f"- Claims: {result['input_claim_count']}",
        f"- Issues: {len(result['issues'])}",
        "",
        "## Claims",
    ]
    if not result["claims"]:
        lines.append("No claims supplied.")
    for c in result["claims"]:
        lines += [
            f"### {c['claim_id']} — {c['claim']}",
            f"- Status/class/confidence: {c['status']} / {c['claim_class']} / {c['confidence']}",
            f"- Evidence refs: {', '.join(c['evidence_refs']) or 'none'}",
            f"- Counterevidence refs: {', '.join(c['counterevidence_refs']) or 'none'}",
            f"- Competing mechanisms supplied: {c['mechanism_count']}",
            f"- Independent source groups: {', '.join(c['source_independence_groups']) or 'none'}",
            "",
        ]
    lines += ["## Issues"]
    if not result["issues"]:
        lines.append("No structural issues found.")
    for issue in result["issues"]:
        lines.append(f"- **{issue['severity'].upper()}** [{issue['claim_id']}]: {issue['issue']}")
    lines += [
        "",
        "## Two review gates",
        "- Round 1: " + result["reviews"][0]["result"],
        "- Round 2: " + result["reviews"][1]["result"],
        "",
        "## Release note",
        result["release_note"],
        "",
        "## Limitations",
    ]
    lines.extend(f"- {item}" for item in result["limitations"])
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Input evidence/claims JSON")
    parser.add_argument("--out-dir", type=Path, default=Path("outputs/phm-run"),
                        help="Directory for report.json and report.md")
    args = parser.parse_args(argv)
    try:
        data = load_json(args.input)
        errors = validate_input(data)
        if errors:
            print("Input validation failed:", file=sys.stderr)
            for error in errors:
                print(f"- {error}", file=sys.stderr)
            return 2
        result = run_checks(data)
        args.out_dir.mkdir(parents=True, exist_ok=True)
        (args.out_dir / "report.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (args.out_dir / "report.md").write_text(render_markdown(result), encoding="utf-8")
        print(json.dumps({
            "release_status": result["release_status"],
            "issues": len(result["issues"]),
            "json_report": str(args.out_dir / "report.json"),
            "markdown_report": str(args.out_dir / "report.md"),
        }, ensure_ascii=False, indent=2))
        return 1 if result["release_status"] == "fail" else 0
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
