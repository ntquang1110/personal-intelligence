"""Contract tests for evidence-led workload mechanism analysis."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class WorkloadModelContracts(unittest.TestCase):
    def test_start_prompt_separates_capacity_constraints_and_choice(self):
        prompt = (ROOT / "prompts/START_PERSONAL_HUMAN_MAP.md").read_text(encoding="utf-8").lower()
        for phrase in ("available capacity", "external constraints", "discretionary goals",
                       "context-switching", "decision uncertainty", "counterevidence"):
            self.assertIn(phrase, prompt)

    def test_workflow_requires_constraint_classification_and_two_reviews(self):
        workflow = (ROOT / "workflows/personal-human-map.md").read_text(encoding="utf-8").lower()
        for phrase in ("externally required", "negotiable", "discretionary", "blocked/waiting",
                       "adversarial review round 1", "adversarial review round 2",
                       "who controls the constraint"):
            self.assertIn(phrase, workflow)

    def test_case_record_does_not_promote_self_report_to_verified_fact(self):
        case = (ROOT / "evaluations/personal-human-map/INTERVIEW_WORKLOAD_CASE.md").read_text(encoding="utf-8").lower()
        for phrase in ("self-report", "not yet support", "competing mechanisms", "weakening evidence"):
            self.assertIn(phrase, case)

    def test_adversarial_benchmarks_include_constraint_choice_and_capacity(self):
        cases = json.loads((ROOT / "evaluations/personal-human-map/adversarial-cases.json").read_text(encoding="utf-8"))
        ids = {case["id"] for case in cases}
        for case_id in ("PHM-011", "PHM-012", "PHM-013"):
            self.assertIn(case_id, ids)
        for case in cases:
            self.assertTrue(case["must_do"])
            self.assertTrue(case["must_not"])


if __name__ == "__main__":
    unittest.main()
