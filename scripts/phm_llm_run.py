#!/usr/bin/env python3
"""Model-backed Personal Human Map runner for OpenAI-compatible chat APIs.

Requires PHM_API_KEY and PHM_MODEL. PHM_API_BASE_URL defaults to
https://api.openai.com/v1. Never place API keys in files or command arguments.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from phm_run import load_json, run_checks, validate_input, render_markdown
    from phm_map_validate import validate_map, schema_with_local_refs, render_markdown as render_human_map
    from phm_map_validate import validate_map, schema_with_local_refs, render_markdown as render_human_map
except ModuleNotFoundError:
    # Allow unittest to load this file by path from the repository root.
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from phm_run import load_json, run_checks, validate_input, render_markdown

SYSTEM = """You are the Personal Human Map analysis engine. Follow the supplied input and repository contract.
Separate direct evidence, self-report, inference, hypothesis, and unknown. Never invent evidence, test scores,
events, outcomes, or source independence. Do not diagnose. For consequential claims, compare at least two
plausible mechanisms, list distinct predictions and counterevidence, and propose a discriminating test.
Do not count repeated AI summaries as independent corroboration. The default deliverable is a whole-person map, not a narrow issue-only report. Cover personality, cognitive process, motivation/values, capabilities, behavior/execution, environment fit, blind spots, development and longitudinal change; mark domains unknown when evidence is absent. Include construct-level cross-assessment synthesis with exact result references, agreement, disagreement, context moderators, source lineage, alternatives and validation plans. Never average unlike scales or invent absent assessment results. Keep astrology/numerology/horoscope/tarot
in a separate interpretive-only lane and never use them to support empirical claims. Be candid when data is
insufficient. Return Markdown, not JSON, unless the phase explicitly asks for a compact JSON checklist."""


def chat_completion(base_url: str, api_key: str, model: str, messages: list[dict[str, str]], timeout: int = 90) -> str:
    url = base_url.rstrip("/") + "/chat/completions"
    payload = json.dumps({
        "model": model,
        "messages": messages,
        "temperature": 0.2,
    }).encode("utf-8")
    request = urllib.request.Request(
        url, data=payload, method="POST",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")[:2000]
        raise RuntimeError(f"Model API returned HTTP {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Could not reach model API: {exc}") from exc
    try:
        return result["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError("Model API response did not contain choices[0].message.content") from exc


def parse_json_object(raw: str) -> dict[str, Any]:
    """Parse a model response that should contain one JSON object."""
    text = raw.strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()
    try:
        value = json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        if start < 0 or end <= start:
            raise ValueError("model response did not contain a JSON object")
        value = json.loads(text[start:end + 1])
    if not isinstance(value, dict):
        raise ValueError("structured map root must be a JSON object")
    return value


def generate_validated_map(data: dict[str, Any], narrative: str, base_url: str,
                           api_key: str, model: str) -> dict[str, Any]:
    """Ask for a schema-conforming map and retry with concrete validation errors."""
    schema = schema_with_local_refs()
    schema_text = json.dumps(schema, ensure_ascii=False, indent=2)
    packet = json.dumps(data, ensure_ascii=False, indent=2)
    errors: list[str] = []
    raw = ""
    for attempt in range(1, 4):
        repair = ""
        if errors:
            repair = "\nPREVIOUS VALIDATION ERRORS — fix every one without inventing evidence:\n" + \
                     "\n".join(f"- {e}" for e in errors)
        prompt = (
            "Return exactly one JSON object for a complete Personal Human Map. Do not wrap it in Markdown.\n"
            "It must conform to the supplied JSON Schema. Preserve the schema's required fields and enums.\n"
            "Use only evidence in the input packet; use exact evidence IDs as evidence_inventory.source_ref and claim refs.\n"
            "Do not invent personality test results, scores, dates, observations, or independent reviewers.\n"
            "If there are no real assessment results, assessment_findings must be empty or explicitly state that no scored result was supplied; do not infer Big Five/MBTI/DISC/Enneagram types.\n"
            "Cover every required domain; say unknown/insufficient evidence where needed. Keep symbolic systems in interpretive_only lane and never use them to support empirical claims.\n"
            "Cross-assessment synthesis must preserve agreement, disagreement, moderators, alternative explanations, confidence rationale, and validation plan. Do not average unlike scales.\n\n"
            "INPUT EVIDENCE PACKET:\n" + packet +
            "\n\nPROVISIONAL NARRATIVE / RED-TEAM OUTPUT:\n" + narrative +
            "\n\nJSON SCHEMA:\n" + schema_text + repair
        )
        raw = chat_completion(base_url, api_key, model, [
            {"role": "system", "content": SYSTEM + " You are now in strict structured-output mode. Return JSON only."},
            {"role": "user", "content": prompt},
        ])
        try:
            mapped = parse_json_object(raw)
            errors = validate_map(mapped)
        except (ValueError, json.JSONDecodeError) as exc:
            errors = [str(exc)]
        if not errors:
            return {"valid": True, "attempts": attempt, "errors": [], "map": mapped,
                    "raw_response": raw}
    return {"valid": False, "attempts": 3, "errors": errors, "map": None,
            "raw_response": raw}


def run_model_pipeline(data: dict[str, Any], base_url: str, api_key: str, model: str) -> dict[str, Any]:
    evidence_packet = json.dumps(data, ensure_ascii=False, indent=2)
    phases = [
        ("draft", "Create a provisional Personal Human Map from the input. Include evidence-linked claims, unknowns, competing mechanisms, predictions, counterevidence, and mechanism-matched experiments. Clearly label unsupported areas."),
        ("red_team_1", "RED-TEAM ROUND 1. Attack the draft above. Identify unsupported/generic claims, source dependence, missing counterexamples, rival mechanisms, overconfidence, safety/privacy issues, and interventions that do not follow from evidence. Cite exact claims/sections and give concrete revisions. Do not rewrite the whole report yet."),
        ("revision", "Revise the draft using the input and Round 1 critique. Explicitly resolve each critique as accepted, partially accepted, or rejected with reason. Downgrade or remove unsupported claims. Preserve uncertainty and the separation of interpretive systems."),
        ("red_team_2", "RED-TEAM ROUND 2. Review the revised report and Round 1 critique for regressions and unresolved blockers. Do not merely repeat Round 1. Test constraint-versus-choice attribution, source independence, evidence traceability, competing mechanisms, falsifiability, safety, and whether each recommendation targets a supported mechanism. End with RELEASE DECISION: PASS or PROVISIONAL/FAIL and list blocking issues. Do not pass if critical claims are unsupported or if evidence is insufficient."),
        ("user_fit_gate", "Perform final user-fit and release-gate review against the original purpose. Summarize what is supported, what remains unknown, the highest-value next evidence, and whether the report is ready. User agreement is not independent validation. If any critical issue remains, label the whole report PROVISIONAL rather than passing."),
    ]
    outputs: dict[str, str] = {}
    context = "INPUT EVIDENCE PACKET:\n" + evidence_packet
    for name, instruction in phases:
        messages = [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": context + "\n\nPHASE: " + name + "\nTASK: " + instruction +
             ("\nReturn the complete draft report." if name == "draft" else "")},
        ]
        output = chat_completion(base_url, api_key, model, messages)
        outputs[name] = output
        context += f"\n\n--- PHASE OUTPUT: {name} ---\n{output}"
    narrative = outputs["user_fit_gate"]
    structured_map = generate_validated_map(data, narrative, base_url, api_key, model)
    return {
        "pipeline_version": "0.2.0-llm",
        "run_at": datetime.now(timezone.utc).isoformat(),
        "model": model,
        "base_url": base_url,
        "subject_ref": data.get("subject_ref"),
        "purpose": data.get("purpose"),
        "structural_checks": run_checks(data),
        "phases": outputs,
        "structured_map": structured_map,
        "semantic_review_attempted": True,
        "independent_review": False,
        "release_status": "provisional",
        "release_note": "Model-assisted multi-stage review completed; not independent validation. Human review and benchmark evaluation remain required before high-stakes use.",
        "limitations": [
            "Model-generated critique is not independent external review.",
            "API/provider may retain or process submitted data according to its terms; use pseudonymous and consented input.",
            "A model's claim of PASS is not itself proof of correctness; inspect blockers and evidence links.",
            "The structural check status is reported separately from semantic model review.",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--out-dir", type=Path, default=Path("outputs/phm-llm-run"))
    parser.add_argument("--base-url", default=os.environ.get("PHM_API_BASE_URL", "https://api.openai.com/v1"))
    parser.add_argument("--model", default=os.environ.get("PHM_MODEL"))
    args = parser.parse_args(argv)
    api_key = os.environ.get("PHM_API_KEY")
    if not api_key or not args.model:
        parser.error("Set PHM_API_KEY and PHM_MODEL in environment variables; never hardcode secrets.")
    try:
        data = load_json(args.input)
        errors = validate_input(data)
        if errors:
            print("Input validation failed:\n" + "\n".join(f"- {e}" for e in errors), file=sys.stderr)
            return 2
        result = run_model_pipeline(data, args.base_url, api_key, args.model)
        args.out_dir.mkdir(parents=True, exist_ok=True)
        (args.out_dir / "run.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        structured = result["structured_map"]
        if structured["valid"]:
            (args.out_dir / "human-map.json").write_text(
                json.dumps(structured["map"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            report = render_human_map(structured["map"])
            report += "\n\n## Pipeline validation\n- Structured map schema/reference validation: PASS\n- Independent review: no\n- Release status: PROVISIONAL (model-assisted self-critique is not independent validation)\n"
        else:
            report = result["phases"]["user_fit_gate"]
            report += "\n\n## STRUCTURED MAP VALIDATION FAILED\n" + "\n".join(f"- {e}" for e in structured["errors"])
            report += "\nThe output remains provisional; no schema-invalid human-map.json was emitted.\n"
        (args.out_dir / "report.md").write_text(
            "# Personal Human Map — Model-assisted run\n\n"
            f"- Model: {args.model}\n- Run at: {result['run_at']}\n"
            f"- Status: {result['release_status']}\n- Independent review: no\n\n"
            + report + "\n\n## Phase artifacts\n"
            + "\n".join(f"- {name}: {args.out_dir / (name + '.md')}" for name in result["phases"]) + "\n",
            encoding="utf-8")
        for name, output in result["phases"].items():
            (args.out_dir / f"{name}.md").write_text(output + "\n", encoding="utf-8")
        print(json.dumps({"status": result["release_status"], "out_dir": str(args.out_dir),
                          "phases": list(result["phases"]),
                          "structured_map_valid": result["structured_map"]["valid"],
                          "structured_map_attempts": result["structured_map"]["attempts"],
                          "structured_map_errors": result["structured_map"]["errors"]}, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, RuntimeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
