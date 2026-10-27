import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class MatchingContracts(unittest.TestCase):
    def test_matching_and_privacy_docs_exist(self):
        for rel in [
            "MATCHING_AND_MUTUAL_REVIEW.md",
            "PRIVACY_AND_CONSENT.md",
            "REVIEW_GAPS_AND_ROADMAP.md",
            "prompts/JOB_FIT_REVIEW.md",
            "prompts/PARTNER_COMPATIBILITY_REVIEW.md",
            "prompts/CREATE_SHAREABLE_PROFILE.md",
        ]:
            self.assertTrue((ROOT / rel).is_file(), rel)

    def test_new_schemas_parse_and_have_versions(self):
        expected = {
            "schemas/shareable-profile.schema.json": "2.1",
            "schemas/mutual-review.schema.json": "2.1",
        }
        for rel, version in expected.items():
            with self.subTest(file=rel):
                schema = json.loads((ROOT / rel).read_text(encoding="utf-8"))
                self.assertEqual(schema["properties"]["schema_version"]["const"], version)

    def test_mutual_review_requires_human_decision(self):
        schema = json.loads((ROOT / "schemas/mutual-review.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(schema["properties"]["human_decision_required"]["const"], True)
        self.assertIn("participated_voluntarily", schema["properties"]["participants"]["items"]["required"])

    def test_job_fit_guardrails_are_explicit(self):
        prompt = (ROOT / "prompts/JOB_FIT_REVIEW.md").read_text(encoding="utf-8").lower()
        self.assertIn("do not infer or score protected or sensitive traits", prompt)
        self.assertIn("do not recommend an automatic hire/reject decision", prompt)

    def test_partner_review_is_mutual_and_opt_in(self):
        prompt = (ROOT / "prompts/PARTNER_COMPATIBILITY_REVIEW.md").read_text(encoding="utf-8").lower()
        self.assertIn("voluntarily chooses to participate", prompt)
        self.assertIn("do not secretly analyze", prompt)
        self.assertIn("universal spouse score", prompt)

if __name__ == "__main__":
    unittest.main()
