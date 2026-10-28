"""Tests for structured map schema, referential integrity, and Markdown rendering."""
import copy
import json
import unittest
from pathlib import Path

from scripts.phm_map_validate import load_json, render_markdown, validate_map

ROOT = Path(__file__).resolve().parents[1]


class PHMMapValidationTests(unittest.TestCase):
    def setUp(self):
        self.data = load_json(ROOT / "templates" / "phm-human-map.template.json")

    def test_synthetic_template_passes_schema_and_reference_validation(self):
        self.assertEqual(validate_map(self.data), [])

    def test_unknown_claim_evidence_reference_is_rejected(self):
        data = copy.deepcopy(self.data)
        data["claims"][0]["evidence_refs"].append("missing-source")
        self.assertTrue(any("unknown evidence" in x for x in validate_map(data)))

    def test_interpretive_source_cannot_support_empirical_claim(self):
        data = copy.deepcopy(self.data)
        data["evidence_inventory"].append({
            "source_ref": "symbolic-source", "source_type": "interpretive_system",
            "date_range": None, "context": "synthetic", "consent_status": "not_applicable",
            "limitations": ["Interpretive only."]
        })
        data["claims"][0]["evidence_refs"].append("symbolic-source")
        self.assertTrue(any("cannot support an empirical claim" in x for x in validate_map(data)))

    def test_schema_rejects_missing_whole_person_domain(self):
        data = copy.deepcopy(self.data)
        del data["domains"]["personality"]
        self.assertTrue(any("personality" in x for x in validate_map(data)))

    def test_renderer_includes_domains_synthesis_and_unknowns(self):
        report = render_markdown(self.data)
        for phrase in ("## Whole-person domains", "### Personality", "### Stress and recovery (non-clinical)",
                       "### Strengths and costs by context", "### Contradictions and unresolved tensions",
                       "## Cross-assessment synthesis", "## Unknowns and validation plan",
                       "## Next actions", "## Longitudinal change log"):
            if phrase == "PROVISIONAL":
                continue
            self.assertIn(phrase, report)
        self.assertIn("insufficient_evidence", report.lower())


if __name__ == "__main__":
    unittest.main()
