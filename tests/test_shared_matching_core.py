import json
import unittest
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class SharedMatchingCoreContracts(unittest.TestCase):
    def test_core_artifacts_exist(self):
        for rel in [
            "engines/matching/ENGINE.md",
            "MATCHING_CRITERIA_CATALOG.md",
            "prompts/START_MATCHING.md",
            "schemas/match-assessment.schema.json",
            "templates/match-assessment.template.json",
        ]:
            self.assertTrue((ROOT / rel).is_file(), rel)

    def test_all_json_files_parse(self):
        for path in ROOT.rglob("*.json"):
            with self.subTest(path=str(path.relative_to(ROOT))):
                json.loads(path.read_text(encoding="utf-8"))

    def test_assessment_template_matches_schema_contract(self):
        schema = json.loads((ROOT / "schemas/match-assessment.schema.json").read_text(encoding="utf-8"))
        sample = json.loads((ROOT / "templates/match-assessment.template.json").read_text(encoding="utf-8"))
        self.assertEqual(schema["properties"]["schema_version"]["const"], sample["schema_version"])
        for key in schema["required"]:
            self.assertIn(key, sample, key)
        self.assertTrue(sample["human_decision_required"])
        self.assertEqual(len(sample["participants"]), 2)
        self.assertTrue(all(p["opted_in"] is True for p in sample["participants"]))
        self.assertTrue(all(c["importance_by_participant"] for c in sample["criteria"]))
        datetime.fromisoformat(sample["created_at"].replace("Z", "+00:00"))

    def test_criterion_statuses_cover_non_binary_fit(self):
        schema = json.loads((ROOT / "schemas/match-assessment.schema.json").read_text(encoding="utf-8"))
        statuses = schema["properties"]["criteria"]["items"]["properties"]["status"]["enum"]
        self.assertEqual(set(statuses), {"aligned", "complementary", "unresolved", "conflicting", "not_applicable"})

    def test_no_opaque_score_in_shared_engine(self):
        engine = (ROOT / "engines/matching/ENGINE.md").read_text(encoding="utf-8").lower()
        self.assertIn("never generate a single opaque compatibility score", engine)
        self.assertIn("compare symmetrically", engine)
        self.assertIn("human decision required", engine)

    def test_job_and_partner_contexts_share_the_same_contract(self):
        schema = json.loads((ROOT / "schemas/match-assessment.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(schema["properties"]["context"]["enum"], ["job", "partner", "marriage", "other"])
        catalog = (ROOT / "MATCHING_CRITERIA_CATALOG.md").read_text(encoding="utf-8").lower()
        self.assertIn("career-specific criteria", catalog)
        self.assertIn("partner / marriage-specific criteria", catalog)

if __name__ == "__main__":
    unittest.main()
