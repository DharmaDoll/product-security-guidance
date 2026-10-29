"""Observe Git mirror recovery in disposable repositories, with no network."""

import os
from pathlib import Path
import subprocess
import tempfile
import unittest


class MirrorRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="git-recovery-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "source"
        self.backup = self.root / "backup.git"
        self.restored = self.root / "restored.git"
        self.env = os.environ.copy()
        # Ignore inherited Git repository and config overrides. No user hooks,
        # signing, credentials, or maintenance are needed by this offline test.
        for key in list(self.env):
            if key.startswith("GIT_"):
                del self.env[key]
        self.env.update({
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_TERMINAL_PROMPT": "0",
            "GIT_ALLOW_PROTOCOL": "file",
            "LC_ALL": "C",
        })
        self.git("init", "--template=", "--initial-branch=main", str(self.source))
        self.at(self.source, "config", "user.name", "Recovery example")
        self.at(self.source, "config", "user.email", "recovery@example.invalid")
        (self.source / "product.txt").write_text("released product\n")
        self.at(self.source, "add", "product.txt")
        self.at(self.source, "commit", "-m", "Released version")
        self.at(self.source, "branch", "release/1.x")
        self.at(self.source, "tag", "-a", "v1.0.0", "-m", "Release")
        (self.source / "product.txt").write_text("next development version\n")
        self.at(self.source, "commit", "-am", "Next version")

    def git(self, *args, check=True):
        return subprocess.run(
            ["git", *args], cwd=self.root, env=self.env,
            text=True, capture_output=True, check=check, timeout=30,
        )

    def at(self, repository, *args, check=True):
        return self.git("-C", str(repository), *args, check=check)

    def expected_refs(self, repository):
        output = self.git(
            "ls-remote", "--refs", "--", str(repository),
            "refs/heads/*", "refs/tags/*",
        ).stdout
        self.assertTrue(output.strip(), "Empty collection is not a backup")
        return sorted(output.splitlines())

    def actual_refs(self, repository):
        return sorted(self.at(
            repository, "for-each-ref",
            "--format=%(objectname)%09%(refname)", "refs/heads", "refs/tags",
        ).stdout.splitlines())

    def mirror(self, source, destination, check=True):
        result = self.git(
            "clone", "--mirror", "--origin", "origin", "--no-local", "--no-hardlinks",
            "--reject-shallow", "--template=", "--",
            str(source), str(destination), check=check,
        )
        if result.returncode == 0:
            self.at(destination, "config", "--remove-section", "remote.origin")
        return result

    def backup_source(self):
        expected = self.expected_refs(self.source)
        self.mirror(self.source, self.backup)
        self.at(self.backup, "fsck", "--full")
        self.assertEqual(expected, self.actual_refs(self.backup))
        return expected

    def test_source_unavailable_restore_preserves_refs_and_release_content(self):
        expected = self.backup_source()
        # Rename the disposable source instead of deleting a user's repository.
        self.source.rename(self.root / "unavailable-source")
        self.assertFalse(self.source.exists())
        self.assertFalse((self.backup / "objects/info/alternates").exists())
        self.mirror(self.backup, self.restored)
        self.at(self.restored, "fsck", "--full")
        self.assertEqual(expected, self.actual_refs(self.restored))
        self.assertEqual(
            "released product\n",
            self.at(self.restored, "show", "refs/tags/v1.0.0:product.txt").stdout,
        )
        self.assertEqual("", self.at(self.restored, "remote").stdout)
        self.assertEqual("true", self.at(
            self.restored, "rev-parse", "--is-bare-repository",
        ).stdout.strip())

    def test_missing_tag_is_incomplete_even_when_fsck_succeeds(self):
        expected = self.backup_source()
        self.mirror(self.backup, self.restored)
        self.at(self.restored, "update-ref", "-d", "refs/tags/v1.0.0")
        self.at(self.restored, "fsck", "--full")
        self.assertNotEqual(expected, self.actual_refs(self.restored))

    def test_same_tag_name_at_different_object_is_incomplete(self):
        expected = self.backup_source()
        self.mirror(self.backup, self.restored)
        new_object = self.at(self.restored, "rev-parse", "refs/heads/main").stdout.strip()
        self.at(self.restored, "update-ref", "refs/tags/v1.0.0", new_object)
        self.at(self.restored, "fsck", "--full")
        actual = self.actual_refs(self.restored)
        self.assertEqual(len(expected), len(actual))
        self.assertNotEqual(expected, actual)

    def test_corrupt_backup_objects_fail_integrity_check(self):
        self.backup_source()
        packs = list((self.backup / "objects/pack").glob("*.pack"))
        self.assertTrue(packs, "Git transport must have produced a pack")
        packs[0].chmod(0o600)
        packs[0].write_bytes(b"corrupt disposable test pack")
        result = self.at(self.backup, "fsck", "--full", check=False)
        self.assertNotEqual(0, result.returncode)

    def test_existing_restore_repository_is_not_overwritten(self):
        self.backup_source()
        self.git("init", "--bare", "--template=", str(self.restored))
        marker = self.restored / "existing-marker"
        marker.write_text("keep existing repository\n")
        result = self.mirror(self.backup, self.restored, check=False)
        self.assertNotEqual(0, result.returncode)
        self.assertEqual("keep existing repository\n", marker.read_text())

    def test_shallow_source_is_rejected(self):
        shallow = self.root / "shallow"
        self.git("clone", "--depth=1", "--template=", self.source.as_uri(), str(shallow))
        self.assertEqual("true", self.at(
            shallow, "rev-parse", "--is-shallow-repository",
        ).stdout.strip())
        result = self.mirror(shallow, self.backup, check=False)
        self.assertNotEqual(0, result.returncode)

    def test_ref_change_during_collection_is_not_accepted(self):
        expected = self.expected_refs(self.source)
        self.at(self.source, "tag", "v2.0.0")
        self.mirror(self.source, self.backup)
        self.at(self.backup, "fsck", "--full")
        self.assertNotEqual(expected, self.actual_refs(self.backup))


if __name__ == "__main__":
    unittest.main()
