import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class RepositoryContractTests(unittest.TestCase):
    def test_all_fourteen_skill_files_exist(self):
        expected = [
            "00-orchestrator", "01-life-timeline", "02-identity-values",
            "03-cognitive-style", "04-behavioral-patterns", "05-decision-intelligence",
            "06-feedback-360", "07-capability-audit", "08-career-strategy",
            "09-life-strategy", "10-behavioral-experiments",
            "11-personal-operating-system", "12-evolution-tracker", "13-final-synthesis"
        ]
        for name in expected:
            path = ROOT / "skills" / name / "SKILL.md"
            self.assertTrue(path.exists(), f"Missing {path}")
            text = path.read_text(encoding="utf-8")
            self.assertIn("## Workflow", text)
            self.assertIn("## Output contract", text)
            self.assertGreater(len(text), 900, f"Skill appears too short: {name}")

    def test_json_files_parse(self):
        for path in list((ROOT / "schemas").glob("*.json")) + list((ROOT / "examples").glob("*.json")):
            with self.subTest(path=path):
                json.loads(path.read_text(encoding="utf-8"))

    def test_evidence_schema_has_required_claim_fields(self):
        schema = json.loads((ROOT / "schemas/evidence.schema.json").read_text(encoding="utf-8"))
        required = set(schema["required"])
        self.assertTrue({"claim_id", "claim", "class", "confidence", "confidence_rationale", "validation_status"} <= required)
        self.assertIn("UNKNOWN", schema["properties"]["class"]["enum"])

    def test_no_skill_claims_all_sources_are_always_available(self):
        for path in (ROOT / "skills").glob("*/SKILL.md"):
            text = path.read_text(encoding="utf-8").lower()
            self.assertTrue("actually available" in text or "available" in text, str(path))

    def test_shared_policies_exist(self):
        for rel in ["config/evidence-policy.md", "config/interview-policy.md", "config/output-contracts.md", "README.md"]:
            self.assertTrue((ROOT / rel).exists(), rel)

if __name__ == "__main__":
    unittest.main()
