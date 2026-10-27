import json
import unittest
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except ImportError:
    Draft202012Validator = None

ROOT = Path(__file__).resolve().parents[1]

@unittest.skipIf(Draft202012Validator is None, "Install jsonschema to run full Draft 2020-12 validation")
class Draft202012Validation(unittest.TestCase):
    def load_json(self, rel):
        return json.loads((ROOT / rel).read_text(encoding="utf-8"))

    def test_every_schema_is_valid_draft_2020_12(self):
        for path in (ROOT / "schemas").glob("*.schema.json"):
            with self.subTest(schema=path.name):
                Draft202012Validator.check_schema(json.loads(path.read_text(encoding="utf-8")))

    def test_matching_example_validates(self):
        schema = self.load_json("schemas/match-assessment.schema.json")
        sample = self.load_json("templates/match-assessment.template.json")
        Draft202012Validator(schema).validate(sample)

    def test_shareable_profile_example_validates_and_requires_consent(self):
        schema = self.load_json("schemas/shareable-profile.schema.json")
        sample = self.load_json("templates/shareable-profile.template.json")
        Draft202012Validator(schema).validate(sample)
        invalid = json.loads(json.dumps(sample))
        invalid["consent"]["owner_approved"] = False
        with self.assertRaises(Exception):
            Draft202012Validator(schema).validate(invalid)

    def test_mutual_review_example_requires_all_participants_opted_in(self):
        schema = self.load_json("schemas/mutual-review.schema.json")
        sample = self.load_json("templates/mutual-review.template.json")
        Draft202012Validator(schema).validate(sample)
        invalid = json.loads(json.dumps(sample))
        invalid["participants"][1]["participated_voluntarily"] = False
        with self.assertRaises(Exception):
            Draft202012Validator(schema).validate(invalid)

if __name__ == "__main__":
    unittest.main()
