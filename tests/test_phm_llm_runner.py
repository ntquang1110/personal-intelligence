"""Tests for model-backed PHM phase orchestration without making network calls."""
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

    def test_pipeline_runs_all_five_phases_and_never_claims_independence(self):
        calls = []

        def fake_chat(base_url, api_key, model, messages, timeout=90):
            calls.append(messages[-1]["content"])
            return f"mock output {len(calls)}"

        with patch.object(runner, "chat_completion", side_effect=fake_chat):
            result = runner.run_model_pipeline(self.sample(), "https://example.invalid/v1", "test-key", "test-model")
        self.assertEqual(list(result["phases"]), ["draft", "red_team_1", "revision", "red_team_2", "user_fit_gate"])
        self.assertEqual(len(calls), 5)
        self.assertTrue(result["semantic_review_attempted"])
        self.assertFalse(result["independent_review"])
        self.assertEqual(result["release_status"], "provisional")

    def test_phase_context_includes_prior_outputs(self):
        seen = []

        def fake_chat(base_url, api_key, model, messages, timeout=90):
            seen.append(messages[-1]["content"])
            return "prior-phase-result"

        with patch.object(runner, "chat_completion", side_effect=fake_chat):
            runner.run_model_pipeline(self.sample(), "https://example.invalid/v1", "test-key", "test-model")
        self.assertIn("prior-phase-result", seen[1])
        self.assertIn("RED-TEAM ROUND 1", seen[1])
        self.assertIn("Round 1 critique", seen[2])


if __name__ == "__main__":
    unittest.main()
