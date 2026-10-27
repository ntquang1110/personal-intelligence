import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class SharingSafetyContracts(unittest.TestCase):
    def test_shareable_profile_requires_explicit_approval(self):
        schema = json.loads((ROOT / "schemas/shareable-profile.schema.json").read_text(encoding="utf-8"))
        consent = schema["properties"]["consent"]["properties"]
        self.assertIs(consent["owner_approved"]["const"], True)
        claim = schema["properties"]["claims"]["items"]["properties"]
        self.assertIs(claim["approved_for_sharing"]["const"], True)
        self.assertIn("purpose_relevance", claim)

    def test_mutual_review_requires_both_parties_opted_in(self):
        schema = json.loads((ROOT / "schemas/mutual-review.schema.json").read_text(encoding="utf-8"))
        participant = schema["properties"]["participants"]["items"]["properties"]
        self.assertIs(participant["participated_voluntarily"]["const"], True)
        self.assertIs(participant["approved_shared_profile"]["const"], True)
        self.assertIn("human_decision_required", schema["required"])
        self.assertIs(schema["properties"]["human_decision_required"]["const"], True)

    def test_new_matching_schema_rejects_unknown_fields_by_contract(self):
        schema = json.loads((ROOT / "schemas/match-assessment.schema.json").read_text(encoding="utf-8"))
        self.assertIs(schema["additionalProperties"], False)
        self.assertIs(schema["properties"]["human_decision_required"]["const"], True)
        self.assertIs(schema["properties"]["participants"]["items"]["additionalProperties"], False)

if __name__ == "__main__":
    unittest.main()
