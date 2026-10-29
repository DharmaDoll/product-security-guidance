"""Exercise the public CLI on inert workflow text; never execute an Action."""

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parent
SHA = "0123456789abcdef0123456789abcdef01234567"


class WorkflowReferenceTests(unittest.TestCase):
    def invoke(self, *paths):
        return subprocess.run(
            [sys.executable, str(ROOT / "check_refs.py"), *map(str, paths)],
            text=True, capture_output=True, timeout=10,
        )

    def inspect_text(self, text):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "workflow.yml"
            path.write_text(text)
            return self.invoke(path)

    def assert_exit(self, result, expected):
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)

    def test_fixed_action_reusable_and_container(self):
        result = self.invoke(ROOT / "pinned.yml")
        self.assert_exit(result, 0)
        self.assertIn("pinned=3 local=1 rejected=0", result.stdout)

    def test_tag_branch_and_container_tag_rejected(self):
        result = self.invoke(ROOT / "mutable.yml")
        self.assert_exit(result, 1)
        self.assertIn("rejected=3", result.stdout)

    def test_short_missing_and_computed_refs_rejected(self):
        for ref in ("example/action@0123456", "example/action", "${{ inputs.action }}", "./${{ inputs.path }}"):
            with self.subTest(ref=ref):
                result = self.inspect_text(f'jobs: {{test: {{steps: [{{uses: "{ref}"}}]}}}}')
                self.assert_exit(result, 1)

    def test_flow_and_quoted_keys_are_inspected(self):
        result = self.inspect_text("'jobs': {test: {'steps': [{'uses': 'example/action@v1'}]}}")
        self.assert_exit(result, 1)

    def test_folded_scalar_and_shared_alias_are_inspected(self):
        result = self.inspect_text(
            "jobs:\n  test:\n    steps:\n      - &shared\n        uses: >-\n          example/action@v1\n      - *shared\n"
        )
        self.assert_exit(result, 1)
        self.assertIn("rejected=2", result.stdout)

    def test_run_text_is_not_an_action_reference(self):
        result = self.inspect_text("jobs:\n  test:\n    steps:\n      - run: |\n          echo 'uses: example/action@v1'\n")
        self.assert_exit(result, 0)
        self.assertIn("pinned=0 local=0 rejected=0", result.stdout)

    def test_same_repository_workflow_forms(self):
        for ref in ("./.github/workflows/local.yml", "$/.github/workflows/local.yaml"):
            with self.subTest(ref=ref):
                result = self.inspect_text(f"jobs: {{reuse: {{uses: '{ref}'}}}}")
                self.assert_exit(result, 0)
                self.assertIn("local=1", result.stdout)

    def test_missing_empty_directory_and_symlink_are_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assert_exit(self.invoke(root / "missing.yml"), 2)
            self.assert_exit(self.invoke(root), 2)
            alias = root / "alias.yml"
            alias.symlink_to(ROOT / "pinned.yml")
            self.assert_exit(self.invoke(root), 2)

    def test_broken_duplicate_and_nonworkflow_inputs_are_errors(self):
        for text in (
            "jobs: [", "", "name: only-name", "jobs: {}",
            "jobs: {test: {steps: [{uses: example/action@v1, uses: example/action@" + SHA + "}]}}",
            "jobs: {test: {steps: [{uses: {nested: value}}]}}",
            "jobs: {test: {steps: [{uses: example/action@v1, run: echo ok}]}}",
            "jobs: {test: {steps: [{name: only-name}]}}",
        ):
            with self.subTest(text=text):
                self.assert_exit(self.inspect_text(text), 2)

    def test_merge_custom_tag_and_cyclic_alias_are_errors(self):
        for text in (
            "base: &base {steps: [{run: echo ok}]}\njobs: {test: {<<: *base}}",
            "jobs: !custom {test: {steps: [{run: echo ok}]}}",
            "loop: &loop [*loop]\njobs: {test: {steps: [{run: echo ok}]}}",
        ):
            with self.subTest(text=text):
                self.assert_exit(self.inspect_text(text), 2)

    def test_directory_inspects_all_immediate_workflows_without_modifying_them(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in ("pinned.yml", "mutable.yml"):
                (root / name).write_bytes((ROOT / name).read_bytes())
            before = {p.name: p.read_bytes() for p in root.iterdir()}
            result = self.invoke(root)
            self.assert_exit(result, 1)
            self.assertIn("files=2", result.stdout)
            self.assertEqual(before, {p.name: p.read_bytes() for p in root.iterdir()})

    def test_missing_dependency_is_an_error(self):
        result = subprocess.run(
            [sys.executable, "-S", str(ROOT / "check_refs.py"), str(ROOT / "pinned.yml")],
            env={k: v for k, v in os.environ.items() if k != "PYTHONPATH"},
            text=True, capture_output=True, timeout=10,
        )
        self.assert_exit(result, 2)
        self.assertIn("PyYAML", result.stderr)


if __name__ == "__main__":
    unittest.main()
