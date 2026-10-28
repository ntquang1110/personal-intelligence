"""Executable tests for the deterministic PHM pipeline scaffold."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("phm_run", ROOT / "scripts" / "phm_run.py")
phm = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(phm)


class PHMRuntimeTests(unittest.TestCase):
    def sample(self):
        return json.loads((ROOT / "templates" / "phm-run.template.json").read_text(encoding="utf-8"))

    def test_sample_input_validates_and_generates_two_explicit_review_stages(self):
        data = self.sample()
        self.assertEqual(phm.validate_input(data), [])
        result = phm.run_checks(data)
        self.assertEqual(len(result["reviews"]), 2)
        self.assertIn("NOT run", result["reviews"][0]["result"])
        self.assertEqual(result["release_status"], "provisional")

    def test_unknown_evidence_reference_is_blocking(self):
        data = self.sample()
        data["claims"][0]["evidence_refs"] = ["does-not-exist"]
        result = phm.run_checks(data)
        self.assertEqual(result["release_status"], "fail")
        self.assertTrue(any(i["severity"] == "blocker" for i in result["issues"]))

    def test_interpretive_source_cannot_support_empirical_claim(self):
        data = self.sample()
        data["evidence"].append({
            "id": "ev-symbolic", "text": "Synthetic symbolic reading",
            "source_type": "astrology", "source_ref": "symbolic-001"
        })
        data["claims"][0]["evidence_refs"].append("ev-symbolic")
        result = phm.run_checks(data)
        self.assertEqual(result["release_status"], "fail")
        self.assertTrue(any("cannot support an empirical claim" in i["issue"] for i in result["issues"]))

    def test_missing_counterevidence_and_competing_mechanisms_are_flagged(self):
        data = self.sample()
        data["claims"][0]["counterevidence_refs"] = []
        data["claims"][0]["mechanisms"] = []
        result = phm.run_checks(data)
        messages = [i["issue"] for i in result["issues"]]
        self.assertTrue(any("no counterevidence" in m for m in messages))
        self.assertTrue(any("fewer than two competing mechanisms" in m for m in messages))

    def test_cli_writes_json_and_markdown_artifacts(self):
        data = self.sample()
        with tempfile.TemporaryDirectory() as temp:
            input_path = Path(temp) / "input.json"
            output_path = Path(temp) / "output"
            input_path.write_text(json.dumps(data), encoding="utf-8")
            exit_code = phm.main([str(input_path), "--out-dir", str(output_path)])
            self.assertEqual(exit_code, 0)
            self.assertTrue((output_path / "report.json").exists())
            self.assertTrue((output_path / "report.md").exists())


if __name__ == "__main__":
    unittest.main()
