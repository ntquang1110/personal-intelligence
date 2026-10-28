"""Contract tests for whole-person map coverage and assessment synthesis."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CrossAssessmentContracts(unittest.TestCase):
    def load(self, path):
        return json.loads((ROOT / path).read_text(encoding="utf-8"))

    def test_synthesis_schema_preserves_agreement_disagreement_and_alternatives(self):
        schema = self.load("schemas/cross-assessment-synthesis.schema.json")
        construct = schema["properties"]["constructs"]["items"]
        required = construct["required"]
        for field in ("assessment_findings", "behavioral_evidence_refs", "agreement",
                      "disagreement", "context_moderators", "alternatives", "confidence",
                      "validation_plan"):
            self.assertIn(field, required)

    def test_whole_person_template_covers_domains_and_separate_symbolic_lane(self):
        data = self.load("templates/phm-human-map.template.json")
        for domain in ("context", "personality", "cognition", "motivation", "capabilities",
                       "behavior", "environment_fit", "blind_spots", "development"):
            self.assertIn(domain, data["domains"])
        self.assertIn("assessment_synthesis", data)
        self.assertTrue(data["separation_policy"]["empirical_claims_exclude_interpretive_evidence"])
        self.assertIsNone(data["interpretive_appendix"])
        self.assertIn("synthetic", data["purpose"].lower())

    def test_instruments_are_not_averaged_or_used_as_ability_labels(self):
        docs = (ROOT / "docs/CROSS_ASSESSMENT_SYNTHESIS.md").read_text(encoding="utf-8").lower()
        for phrase in ("do not average unlike scales", "mbti", "big five", "disc", "enneagram",
                       "astrology/numerology", "longitudinal"):
            self.assertIn(phrase, docs)

    def test_prompt_requires_complete_map_and_construct_level_synthesis(self):
        prompt = (ROOT / "prompts/START_PERSONAL_HUMAN_MAP.md").read_text(encoding="utf-8").lower()
        for phrase in ("construct-by-construct", "agreement", "disagreement",
                       "personality", "cognitive process", "motivation/values",
                       "environment/collaboration fit", "longitudinal change log"):
            self.assertIn(phrase, prompt)


if __name__ == "__main__":
    unittest.main()
