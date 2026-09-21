from pathlib import Path
import tempfile
import unittest

from check_docs import check


class DocumentChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repository"
        record = self.root / "controls/records/sample"
        record.mkdir(parents=True)
        (record / "control.yaml").write_text("id: PSB-TEST-001\n")

    def test_valid_anchor_and_external_reference(self):
        (self.root / "README.md").write_text("# 日本語 heading\n[x](#日本語-heading) [source](https://example.org/spec)\n")
        self.assertEqual(check(self.root)[0], [])

    def test_missing_target_and_anchor(self):
        (self.root / "README.md").write_text("[x](missing.md) [y](#missing)\n")
        self.assertEqual(len(check(self.root)[0]), 2)

    def test_existing_file_outside_repository_is_rejected(self):
        (self.root.parent / "legacy.md").write_text("# Legacy\n")
        (self.root / "README.md").write_text("[legacy](../legacy.md)\n")
        self.assertIn("escapes repository", check(self.root)[0][0])

    def test_duplicate_control_id_is_rejected(self):
        other = self.root / "controls/records/other"
        other.mkdir()
        (other / "control.yaml").write_text('{\n  "id": "PSB-TEST-001",\n}\n')
        self.assertIn("duplicate control ID", check(self.root)[0][0])
