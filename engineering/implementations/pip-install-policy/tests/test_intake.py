"""Observe pip candidate selection using locally generated harmless packages."""
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import unittest
import zipfile


class WheelOnlyIntake(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        version = subprocess.run(
            [sys.executable, '-m', 'pip', '--version'],
            check=True, capture_output=True, text=True,
        )
        print(version.stdout.strip())

    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory(prefix='pip-intake-')
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        self.marker = self.root / 'backend-started'
        self.report = self.root / 'report.json'
        self.requirements = self.root / 'requirements.txt'
        self.policy = (Path(__file__).parents[1] / 'secure/requirements-policy.txt').read_text()

    def wheel(self):
        path = self.root / 'intake_demo-1.0-py3-none-any.whl'
        with zipfile.ZipFile(path, 'w') as wheel:
            prefix = 'intake_demo-1.0.dist-info/'
            wheel.writestr(prefix + 'METADATA', 'Metadata-Version: 2.1\nName: intake-demo\nVersion: 1.0\n')
            wheel.writestr(prefix + 'WHEEL', 'Wheel-Version: 1.0\nGenerator: fixture\nRoot-Is-Purelib: true\nTag: py3-none-any\n')
            wheel.writestr(prefix + 'RECORD', '')
        return path

    def sdist(self):
        path = self.root / 'intake_demo-1.0.tar.gz'
        files = {
            'pyproject.toml': '[build-system]\nrequires = []\nbuild-backend = "backend"\nbackend-path = ["."]\n',
            'backend.py': (
                'from pathlib import Path\n'
                f'Path({str(self.marker)!r}).write_text("benign fixture invoked")\n'
                'raise RuntimeError("benign backend stops here")\n'
            ),
            'PKG-INFO': 'Metadata-Version: 2.1\nName: intake-demo\nVersion: 1.0\n',
        }
        with tarfile.open(path, 'w:gz') as archive:
            for name, content in files.items():
                data = content.encode()
                entry = tarfile.TarInfo('intake_demo-1.0/' + name)
                entry.size = len(data)
                archive.addfile(entry, io.BytesIO(data))
        return path

    def run_pip(self, artifact, *, guarded=True, incorrect_hash=False):
        digest = '0' * 64 if incorrect_hash else hashlib.sha256(artifact.read_bytes()).hexdigest()
        text = self.policy + f'\nintake-demo==1.0 --hash=sha256:{digest}\n'
        if not guarded:
            text = 'intake-demo==1.0\n'
        self.requirements.write_text(text)
        return subprocess.run(
            [sys.executable, '-m', 'pip', '--isolated', 'install',
             '--dry-run', '--ignore-installed', '--no-deps', '--no-index',
             '--no-cache-dir', '--disable-pip-version-check', '--no-build-isolation',
             '--find-links', str(self.root), '--report', str(self.report),
             '-r', str(self.requirements)],
            cwd=self.root, capture_output=True, text=True, timeout=30,
        )

    def test_wheel_is_selected(self):
        result = self.run_pip(self.wheel())
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        installs = json.loads(self.report.read_text())['install']
        self.assertEqual(len(installs), 1)
        self.assertTrue(installs[0]['download_info']['url'].endswith('.whl'))
        self.assertFalse(self.marker.exists())

    def test_source_only_candidate_is_rejected_before_backend(self):
        result = self.run_pip(self.sdist())
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('No matching distribution found', result.stderr)
        self.assertFalse(self.marker.exists())

    def test_fixture_backend_runs_without_policy(self):
        result = self.run_pip(self.sdist(), guarded=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(self.marker.exists(), result.stdout + result.stderr)
        self.assertIn('benign backend stops here', result.stderr)

    def test_hash_mismatch_is_rejected(self):
        result = self.run_pip(self.wheel(), incorrect_hash=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('DO NOT MATCH THE HASHES', result.stderr)


if __name__ == '__main__':
    unittest.main()
