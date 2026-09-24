from __future__ import annotations

import contextlib
import io
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import scan_sensitive as scanner


def inert_samples() -> dict[str, bytes]:
    return {
        "private-key": ("-----BEGIN " + "PRIVATE KEY-----").encode(),
        "github-token": ("gh" + "p_" + "A" * 36).encode(),
        "github-fine-grained-pat": ("github_" + "pat_" + "A" * 82).encode(),
        "aws-access-key": ("AK" + "IA" + "A" * 16).encode(),
        "aws-secret-access-key": ("aws_secret_access_key=" + "A" * 40).encode(),
        "google-api-key": ("AI" + "za" + "A" * 35).encode(),
        "jwt": ("ey" + "JAAAAA.BBBBB.CCCCC").encode(),
        "bearer-token": ("Bearer " + "b" * 16).encode(),
        "slack-webhook": (
            "https://hooks.slack.com/" + "services/AAAAAAAA/BBBBBBBB/" + "C" * 16
        ).encode(),
        "npmrc-auth-token": (
            "//registry.example.invalid/:_authToken=" + "n" * 20
        ).encode(),
        "pypi-api-token": ("pypi" + "-" + "P" * 85).encode(),
        "credential-assignment": ("api_" + "key=" + "g" * 12).encode(),
    }


class PatternTests(unittest.TestCase):
    def test_each_declared_rule_has_a_detected_inert_sample(self) -> None:
        samples = inert_samples()
        self.assertEqual(set(samples), set(scanner.SECRET_RULES))
        for rule, value in samples.items():
            with self.subTest(rule=rule):
                self.assertIn((rule, "example.txt"), scanner.scan("example.txt", value))

    def test_safe_near_misses_and_environment_template(self) -> None:
        self.assertEqual(scanner.scan("example.txt", b"api_key=short"), [])
        self.assertEqual(scanner.scan(".env.example", b"NAME=value"), [])
        self.assertEqual(
            scanner.scan(".env", b"NAME=value"),
            [("sensitive-filename", ".env")],
        )

    def test_binary_and_large_file_are_rejected(self) -> None:
        self.assertEqual(
            scanner.scan("example.txt", b"safe\0data"),
            [("binary-file", "example.txt")],
        )
        self.assertEqual(
            scanner.scan("example.txt", b"A" * (scanner.MAX_FILE_BYTES + 1)),
            [("file-too-large", "example.txt")],
        )

    def test_report_does_not_print_matched_value(self) -> None:
        value = inert_samples()["credential-assignment"]
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            status = scanner.report(scanner.scan("example.txt", value))
        self.assertEqual(status, 1)
        self.assertIn("BLOCK credential-assignment", output.getvalue())
        self.assertNotIn(value.decode(), output.getvalue())


class GitModeTests(unittest.TestCase):
    def git(self, repository: Path, *arguments: str) -> str:
        result = subprocess.run(
            ["git", "-C", str(repository), *arguments],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout.strip()

    def run_scanner(
        self, repository: Path, *arguments: str, input_text: str | None = None
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(Path(scanner.__file__)), *arguments],
            cwd=repository,
            input=input_text,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    def repository(self, root: Path) -> Path:
        repository = root / "repository"
        self.git(root, "init", "-q", str(repository))
        self.git(repository, "config", "user.name", "Pattern Scanner Test")
        self.git(repository, "config", "user.email", "test@example.invalid")
        return repository

    def test_staged_mode_reads_index_instead_of_worktree(self) -> None:
        with tempfile.TemporaryDirectory() as raw_root:
            repository = self.repository(Path(raw_root))
            source = repository / "example.txt"
            source.write_text("safe staged content\n")
            self.git(repository, "add", "example.txt")
            source.write_bytes(inert_samples()["credential-assignment"])

            clean = self.run_scanner(repository, "--staged")
            self.assertEqual(clean.returncode, 0, clean.stderr)

            self.git(repository, "add", "example.txt")
            blocked = self.run_scanner(repository, "--staged")
            self.assertEqual(blocked.returncode, 1, blocked.stderr)

    def test_pre_push_finds_value_removed_from_latest_tree(self) -> None:
        with tempfile.TemporaryDirectory() as raw_root:
            repository = self.repository(Path(raw_root))
            source = repository / "example.txt"
            source.write_text("safe baseline\n")
            self.git(repository, "add", "example.txt")
            self.git(repository, "commit", "-q", "-m", "baseline")
            baseline = self.git(repository, "rev-parse", "HEAD")

            value = inert_samples()["github-token"]
            source.write_bytes(value)
            self.git(repository, "add", "example.txt")
            self.git(repository, "commit", "-q", "-m", "add inert canary")
            source.write_text("removed from latest tree\n")
            self.git(repository, "add", "example.txt")
            self.git(repository, "commit", "-q", "-m", "remove inert canary")
            head = self.git(repository, "rev-parse", "HEAD")

            hook_input = f"refs/heads/main {head} refs/heads/main {baseline}\n"
            blocked = self.run_scanner(
                repository, "--pre-push", input_text=hook_input
            )
            self.assertEqual(blocked.returncode, 1, blocked.stderr)
            self.assertIn("BLOCK github-token", blocked.stdout)
            self.assertNotIn(value.decode(), blocked.stdout + blocked.stderr)

    def test_git_invokes_hooks_and_rejects_inert_canary(self) -> None:
        with tempfile.TemporaryDirectory() as raw_root:
            repository = self.repository(Path(raw_root))
            hooks = Path(scanner.__file__).parent / "hooks"
            self.git(repository, "config", "core.hooksPath", str(hooks))

            source = repository / "example.txt"
            source.write_text("safe content\n")
            self.git(repository, "add", "example.txt")
            self.git(repository, "commit", "-q", "-m", "safe commit")

            value = inert_samples()["credential-assignment"]
            source.write_bytes(value)
            self.git(repository, "add", "example.txt")
            blocked = subprocess.run(
                ["git", "-C", str(repository), "commit", "-q", "-m", "blocked commit"],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertNotEqual(blocked.returncode, 0)
            output = blocked.stdout + blocked.stderr
            self.assertIn("BLOCK credential-assignment", output)
            self.assertNotIn(value.decode(), output)
            self.assertEqual(self.git(repository, "rev-list", "--count", "HEAD"), "1")


if __name__ == "__main__":
    unittest.main()
