import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class RepositoryContracts(unittest.TestCase):
    def test_core_docs_exist(self):
        for rel in ["README.md", "PRODUCT_SPEC.md", "ARCHITECTURE.md", "USAGE_GUIDE.md", "CLAUDE.md", "prompts/START_HERE.md"]:
            self.assertTrue((ROOT / rel).is_file(), rel)

    def test_twelve_domain_modules_exist(self):
        domains = list((ROOT / "domains").glob("*/DOMAIN.md"))
        self.assertEqual(len(domains), 12)
        for path in domains:
            self.assertGreater(len(path.read_text(encoding="utf-8")), 500, str(path))

    def test_all_json_files_parse(self):
        files = list(ROOT.rglob("*.json"))
        self.assertGreaterEqual(len(files), 10)
        for path in files:
            with self.subTest(file=str(path.relative_to(ROOT))):
                json.loads(path.read_text(encoding="utf-8"))

    def test_profile_template_matches_required_domain_keys(self):
        profile = json.loads((ROOT / "templates/profile.template.json").read_text(encoding="utf-8"))
        self.assertEqual(profile["schema_version"], "2.0")
        self.assertEqual(set(profile["domains"]), {f"D{i:02d}" for i in range(1, 13)})

    def test_profile_schema_contract(self):
        schema = json.loads((ROOT / "schemas/personal-profile-v2.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(schema["properties"]["schema_version"]["const"], "2.0")
        self.assertEqual(len(schema["properties"]["domains"]["required"]), 12)

    def test_private_data_ignored(self):
        gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
        for item in ["data/profile.json", "data/evidence.json", "outputs/*"]:
            self.assertIn(item, gitignore)

    def test_skills_preserved(self):
        skills = list((ROOT / "skills").glob("*/SKILL.md"))
        self.assertGreaterEqual(len(skills), 14)

if __name__ == "__main__":
    unittest.main()
