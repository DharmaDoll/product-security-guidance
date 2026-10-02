"""Observe local GNU timeout behavior, without models, credentials or network."""

from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import unittest


WORKER = """
from pathlib import Path
import signal
import sys
import time

if sys.argv[2] == 'ignore':
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
marker = Path(sys.argv[1])
end = time.monotonic() + 6
while time.monotonic() < end:
    with marker.open('ab') as stream:
        stream.write(b'.')
    time.sleep(0.05)
"""

PARENT = """
import signal
import subprocess
import sys
import time

child = subprocess.Popen([sys.executable, sys.argv[1], sys.argv[2], 'term'])
def stop(signum, frame):
    # Keep the parent alive to reap the child; the group signal must stop the child.
    pass
signal.signal(signal.SIGTERM, stop)
while child.poll() is None:
    time.sleep(0.01)
"""


class TimeoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if sys.platform != "linux":
            raise RuntimeError("This smoke test targets Linux")
        cls.timeout = shutil.which("timeout")
        if not cls.timeout:
            raise RuntimeError("GNU coreutils 9.7 timeout is required")
        version = subprocess.run(
            [cls.timeout, "--version"], check=True, capture_output=True, text=True
        ).stdout.splitlines()[0]
        if version != "timeout (GNU coreutils) 9.7":
            raise RuntimeError("This smoke test targets GNU coreutils 9.7")

    def run_command(self, *command):
        return subprocess.run(
            [self.timeout, "--signal=TERM", "--kill-after=1s", "1s", *command],
            capture_output=True,
            timeout=8,
        )

    def assert_stopped(self, marker):
        self.assertTrue(marker.exists(), "worker must have actually started")
        size = marker.stat().st_size
        self.assertGreater(size, 0)
        time.sleep(0.2)
        self.assertEqual(size, marker.stat().st_size, "work continued after timeout")

    def test_normal_command_exits_zero(self):
        result = self.run_command(sys.executable, "-c", "pass")
        self.assertEqual(0, result.returncode)

    def test_command_failure_is_preserved(self):
        result = self.run_command(sys.executable, "-c", "raise SystemExit(7)")
        self.assertEqual(7, result.returncode)

    def test_deadline_stops_actual_work(self):
        with tempfile.TemporaryDirectory() as directory:
            marker = Path(directory) / "heartbeat"
            result = self.run_command(sys.executable, "-c", WORKER, str(marker), "term")
            self.assertEqual(124, result.returncode)
            self.assert_stopped(marker)

    def test_ignored_term_is_followed_by_kill(self):
        with tempfile.TemporaryDirectory() as directory:
            marker = Path(directory) / "heartbeat"
            result = self.run_command(sys.executable, "-c", WORKER, str(marker), "ignore")
            # Python reports direct signal termination as -9; shells expose 137.
            status = result.returncode if result.returncode >= 0 else 128 - result.returncode
            self.assertEqual(137, status)
            self.assert_stopped(marker)

    def test_same_process_group_child_stops(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            worker = root / "worker.py"
            worker.write_text(WORKER)
            marker = root / "heartbeat"
            result = self.run_command(sys.executable, "-c", PARENT, str(worker), str(marker))
            self.assertEqual(124, result.returncode)
            self.assert_stopped(marker)

    def test_missing_command_is_launch_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_command(str(Path(directory) / "missing-command"))
            self.assertEqual(127, result.returncode)


if __name__ == "__main__":
    unittest.main()
