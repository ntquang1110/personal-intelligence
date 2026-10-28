"""Adversarial quality-gate tests; standard-library only."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PersonalHumanMapRedTeamContracts(unittest.TestCase):
    def test_red_team_prompt_requires_all_six_review_passes(self):
        prompt = (ROOT / "prompts/RED_TEAM_PERSONAL_HUMAN_MAP.md").read_text(encoding="utf-8")
        for phrase in ("Evidence audit", "Mechanism challenge", "Personalization attack",
                       "Contradiction and calibration", "Decision usefulness", "Harm and leakage"):
            self.assertIn(phrase, prompt)
        for field in ("blocking_issues", "unsupported_claims", "generic_claims",
                      "rival_mechanisms", "release_decision"):
            self.assertIn(field, prompt)

    def test_rubric_has_hard_gates_not_just_average(self):
        rubric = (ROOT / "evaluations/personal-human-map/QUALITY_RUBRIC.md").read_text(encoding="utf-8")
        self.assertIn("Any 0 in evidence traceability, calibration, or safety means **fail**", rubric)
        self.assertIn("Do not average away a failed critical dimension", rubric)
        self.assertIn("Second red-team review", rubric)

    def test_adversarial_cases_cover_common_failure_modes(self):
        cases = json.loads((ROOT / "evaluations/personal-human-map/adversarial-cases.json").read_text(encoding="utf-8"))
        ids = {case["id"] for case in cases}
        self.assertGreaterEqual(len(cases), 10)
        for case_id in ("PHM-001", "PHM-002", "PHM-004", "PHM-005", "PHM-007", "PHM-010"):
            self.assertIn(case_id, ids)
        for case in cases:
            self.assertTrue(case["must_do"])
            self.assertTrue(case["must_not"])

    def test_no_case_allows_interpretive_system_to_prove_ability(self):
        cases = json.loads((ROOT / "evaluations/personal-human-map/adversarial-cases.json").read_text(encoding="utf-8"))
        case = next(case for case in cases if case["id"] == "PHM-004")
        joined = " ".join(case["must_not"]).lower()
        self.assertIn("birth data", joined)
        self.assertIn("competence", joined)


if __name__ == "__main__":
    unittest.main()
