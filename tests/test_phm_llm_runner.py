"""Tests for model-backed PHM orchestration without network calls."""
import copy
import importlib.util
import json
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("phm_llm_run", ROOT / "scripts" / "phm_llm_run.py")
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


class PHMLLMRunnerTests(unittest.TestCase):
    def sample(self):
        return json.loads((ROOT / "templates" / "phm-run.template.json").read_text(encoding="utf-8"))

    def valid_map_for_sample(self):
        data = json.loads((ROOT / "templates" / "phm-human-map.template.json").read_text(encoding="utf-8"))
        data["subject_ref"] = "subject-example"
        data["purpose"] = "Synthetic example for validating structured map output."
        data["evidence_inventory"] = data["evidence_inventory"][:2]
        data["evidence_inventory"][0]["source_ref"] = "ev-001"
        data["evidence_inventory"][0]["source_type"] = "interview"
        data["evidence_inventory"][0]["context"] = "Synthetic interview evidence."
        data["evidence_inventory"][1]["source_ref"] = "ev-002"
        data["evidence_inventory"][1]["source_type"] = "behavioral_episode"
        data["evidence_inventory"][1]["context"] = "Synthetic behavioral episode."
        data["claims"][0]["evidence_refs"] = ["ev-001", "ev-002"]
        data["claims"][1]["evidence_refs"] = ["ev-001"]
        data["assessment_synthesis"]["constructs"][0]["assessment_findings"] = []
        data["assessment_synthesis"]["constructs"][0]["behavioral_evidence_refs"] = ["ev-001", "ev-002"]
        data["assessment_synthesis"]["global_limitations"] = [
            "Synthetic example only; no real assessment scores or user profile."
        ]
        return data

    def test_pipeline_runs_five_review_phases_and_validates_structured_map(self):
        calls = []
        valid_map = self.valid_map_for_sample()

        def fake_chat(base_url, api_key, model, messages, timeout=90):
            prompt = messages[-1]["content"]
            calls.append(prompt)
            if "JSON SCHEMA:" in prompt:
                return json.dumps(valid_map)
            return f"mock output {len(calls)}"

        with patch.object(runner, "chat_completion", side_effect=fake_chat):
            result = runner.run_model_pipeline(self.sample(), "https://example.invalid/v1", "test-key", "test-model")
        self.assertEqual(list(result["phases"]), ["draft", "red_team_1", "revision", "red_team_2", "user_fit_gate"])
        self.assertEqual(len(calls), 6)
        self.assertTrue(result["semantic_review_attempted"])
        self.assertFalse(result["independent_review"])
        self.assertEqual(result["release_status"], "provisional")
        self.assertTrue(result["structured_map"]["valid"])
        self.assertEqual(result["structured_map"]["attempts"], 1)

    def test_invalid_structured_output_retries_three_times_then_fails_closed(self):
        calls = []

        def fake_chat(base_url, api_key, model, messages, timeout=90):
            calls.append(messages[-1]["content"])
            return "not JSON"

        with patch.object(runner, "chat_completion", side_effect=fake_chat):
            result = runner.run_model_pipeline(self.sample(), "https://example.invalid/v1", "test-key", "test-model")
        self.assertEqual(len(calls), 8)
        self.assertFalse(result["structured_map"]["valid"])
        self.assertEqual(result["structured_map"]["attempts"], 3)
        self.assertTrue(result["structured_map"]["errors"])

    def test_generated_map_cannot_introduce_evidence_not_in_input(self):
        sample = self.sample()
        invalid_map = self.valid_map_for_sample()
        invalid_map["evidence_inventory"][0]["source_ref"] = "invented-evidence-id"

        with patch.object(runner, "chat_completion", return_value=json.dumps(invalid_map)):
            result = runner.generate_validated_map(
                sample, "mock narrative", "https://example.invalid/v1", "test-key", "test-model"
            )
        self.assertFalse(result["valid"])
        self.assertEqual(result["attempts"], 3)
        self.assertTrue(any("not present in the input evidence packet" in e for e in result["errors"]))

    def test_phase_context_includes_prior_outputs(self):
        seen = []
        valid_map = self.valid_map_for_sample()

        def fake_chat(base_url, api_key, model, messages, timeout=90):
            prompt = messages[-1]["content"]
            seen.append(prompt)
            if "JSON SCHEMA:" in prompt:
                return json.dumps(valid_map)
            return "prior-phase-result"

        with patch.object(runner, "chat_completion", side_effect=fake_chat):
            runner.run_model_pipeline(self.sample(), "https://example.invalid/v1", "test-key", "test-model")
        self.assertIn("prior-phase-result", seen[1])
        self.assertIn("RED-TEAM ROUND 1", seen[1])
        self.assertIn("Round 1 critique", seen[2])


if __name__ == "__main__":
    unittest.main()
