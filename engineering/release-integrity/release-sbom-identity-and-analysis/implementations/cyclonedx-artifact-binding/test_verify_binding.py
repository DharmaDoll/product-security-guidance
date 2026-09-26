from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


BASE = Path(__file__).resolve().parent
VERIFY = BASE / "verify_binding.py"
EXAMPLE_ARTIFACT = BASE / "examples" / "release.txt"
EXAMPLE_SBOM = BASE / "examples" / "bom.cdx.json"


class BindingCliTests(unittest.TestCase):
    def run_verify(self, artifact: Path, sbom: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(VERIFY), "--artifact", str(artifact), "--sbom", str(sbom)],
            check=False,
            capture_output=True,
            text=True,
        )

    def write_sbom(self, directory: Path, document: dict) -> Path:
        target = directory / "bom.cdx.json"
        target.write_text(json.dumps(document), encoding="utf-8")
        return target

    def test_exact_artifact_binding_passes(self) -> None:
        result = self.run_verify(EXAMPLE_ARTIFACT, EXAMPLE_SBOM)
        self.assertEqual(result.returncode, 0, result.stderr)
        receipt = json.loads(result.stdout)
        self.assertEqual(receipt["status"], "PASS")
        self.assertEqual(
            receipt["artifact_sha256"], hashlib.sha256(EXAMPLE_ARTIFACT.read_bytes()).hexdigest()
        )
        self.assertEqual(receipt["composition"], "incomplete")

    def test_changed_artifact_is_rejected_without_echoing_content(self) -> None:
        with tempfile.TemporaryDirectory() as raw_directory:
            directory = Path(raw_directory)
            artifact = directory / "release.txt"
            canary = "private-canary-must-not-be-printed"
            artifact.write_text(canary, encoding="utf-8")
            result = self.run_verify(artifact, EXAMPLE_SBOM)
        self.assertEqual(result.returncode, 1)
        self.assertIn("artifact SHA-256 does not match", result.stderr)
        self.assertNotIn(canary, result.stderr)

    def test_pre_build_observation_is_not_release_authority(self) -> None:
        document = json.loads(EXAMPLE_SBOM.read_text(encoding="utf-8"))
        document["metadata"]["lifecycles"] = [{"phase": "pre-build"}]
        with tempfile.TemporaryDirectory() as raw_directory:
            sbom = self.write_sbom(Path(raw_directory), document)
            result = self.run_verify(EXAMPLE_ARTIFACT, sbom)
        self.assertEqual(result.returncode, 1)
        self.assertIn("build or post-build", result.stderr)

    def test_dangling_dependency_is_rejected(self) -> None:
        document = json.loads(EXAMPLE_SBOM.read_text(encoding="utf-8"))
        document["dependencies"][0]["dependsOn"] = ["missing-component"]
        with tempfile.TemporaryDirectory() as raw_directory:
            sbom = self.write_sbom(Path(raw_directory), document)
            result = self.run_verify(EXAMPLE_ARTIFACT, sbom)
        self.assertEqual(result.returncode, 1)
        self.assertIn("unresolved target", result.stderr)

    def test_non_string_dependency_is_rejected_without_traceback(self) -> None:
        document = json.loads(EXAMPLE_SBOM.read_text(encoding="utf-8"))
        document["dependencies"][0]["dependsOn"] = [{"bom-ref": "missing-component"}]
        with tempfile.TemporaryDirectory() as raw_directory:
            sbom = self.write_sbom(Path(raw_directory), document)
            result = self.run_verify(EXAMPLE_ARTIFACT, sbom)
        self.assertEqual(result.returncode, 1)
        self.assertIn("dependsOn must contain strings", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

        document = json.loads(EXAMPLE_SBOM.read_text(encoding="utf-8"))
        document["compositions"][0]["aggregate"] = {"unexpected": "object"}
        with tempfile.TemporaryDirectory() as raw_directory:
            sbom = self.write_sbom(Path(raw_directory), document)
            result = self.run_verify(EXAMPLE_ARTIFACT, sbom)
        self.assertEqual(result.returncode, 1)
        self.assertIn("aggregate is unsupported", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_dangling_composition_assembly_is_rejected(self) -> None:
        document = json.loads(EXAMPLE_SBOM.read_text(encoding="utf-8"))
        document["compositions"][0]["assemblies"].append("missing-component")
        with tempfile.TemporaryDirectory() as raw_directory:
            sbom = self.write_sbom(Path(raw_directory), document)
            result = self.run_verify(EXAMPLE_ARTIFACT, sbom)
        self.assertEqual(result.returncode, 1)
        self.assertIn("assemblies contains an unresolved target", result.stderr)

    def test_unknown_composition_is_reported_without_becoming_complete(self) -> None:
        document = copy.deepcopy(json.loads(EXAMPLE_SBOM.read_text(encoding="utf-8")))
        document["compositions"][0]["aggregate"] = "unknown"
        with tempfile.TemporaryDirectory() as raw_directory:
            sbom = self.write_sbom(Path(raw_directory), document)
            result = self.run_verify(EXAMPLE_ARTIFACT, sbom)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["composition"], "unknown")

    def test_malformed_json_is_error_not_pass(self) -> None:
        with tempfile.TemporaryDirectory() as raw_directory:
            sbom = Path(raw_directory) / "bom.cdx.json"
            sbom.write_text('{"bomFormat":', encoding="utf-8")
            result = self.run_verify(EXAMPLE_ARTIFACT, sbom)
        self.assertEqual(result.returncode, 2)
        self.assertIn("ERROR SBOM is not parseable JSON", result.stderr)

    def test_duplicate_json_key_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw_directory:
            sbom = Path(raw_directory) / "bom.cdx.json"
            raw = EXAMPLE_SBOM.read_text(encoding="utf-8")
            duplicate = raw.replace(
                '"specVersion": "1.7",',
                '"specVersion": "1.7", "specVersion": "1.6",',
            )
            sbom.write_text(duplicate, encoding="utf-8")
            result = self.run_verify(EXAMPLE_ARTIFACT, sbom)
        self.assertEqual(result.returncode, 1)
        self.assertIn("duplicate JSON key: specVersion", result.stderr)


if __name__ == "__main__":
    unittest.main()
