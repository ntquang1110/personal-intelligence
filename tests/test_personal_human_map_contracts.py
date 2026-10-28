"""Static contract tests for Personal Human Map assets; standard-library only."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PersonalHumanMapContracts(unittest.TestCase):
    def load_json(self, relative):
        return json.loads((ROOT / relative).read_text(encoding="utf-8"))

    def test_human_map_schema_has_separate_interpretive_appendix(self):
        schema = self.load_json("schemas/human-map.schema.json")
        self.assertIn("interpretive_appendix", schema["properties"])
        policy = schema["properties"]["separation_policy"]["properties"]
        self.assertEqual(policy["empirical_claims_exclude_interpretive_evidence"]["const"], True)
        self.assertEqual(policy["interpretive_appendix_non_predictive"]["const"], True)

    def test_claim_schema_requires_counterevidence_alternatives_and_validation(self):
        schema = self.load_json("schemas/claim-evidence.schema.json")
        required = schema["required"]
        for field in ("evidence_refs", "counterevidence_refs", "alternatives", "confidence", "validation"):
            self.assertIn(field, required)

    def test_assessment_schema_distinguishes_empirical_and_interpretive_lanes(self):
        schema = self.load_json("schemas/assessment-result.schema.json")
        self.assertEqual(
            schema["properties"]["lane"]["enum"],
            ["empirical", "interpretive_only", "user_meaning"],
        )
        self.assertIn("symbolic_interpretation", schema["properties"]["source_type"]["enum"])

    def test_prompt_forbids_birth_systems_from_supporting_empirical_claims(self):
        prompt = (ROOT / "prompts/START_PERSONAL_HUMAN_MAP.md").read_text(encoding="utf-8")
        self.assertIn("must not:", prompt)
        self.assertIn("support or raise confidence in empirical claims", prompt)
        self.assertIn("trigger/context", prompt)

    def test_workflow_requires_mechanism_and_longitudinal_validation(self):
        workflow = (ROOT / "workflows/personal-human-map.md").read_text(encoding="utf-8")
        self.assertIn("Mechanism extraction", workflow)
        self.assertIn("Validation loop", workflow)
        self.assertIn("counterevidence", workflow)

    def test_docs_distinguish_interest_skill_and_demonstrated_capability(self):
        docs = (ROOT / "docs/PERSONAL_HUMAN_MAP.md").read_text(encoding="utf-8")
        for phrase in ("interest:", "knowledge:", "skill:", "demonstrated capability:", "potential:"):
            self.assertIn(phrase, docs)

    def test_no_unsupported_numeric_confidence_in_contract(self):
        docs = (ROOT / "docs/PERSONAL_HUMAN_MAP.md").read_text(encoding="utf-8")
        self.assertIn("Do not calculate a numerical personality score", docs)
        self.assertIn("low, moderate, high", docs)


if __name__ == "__main__":
    unittest.main()
