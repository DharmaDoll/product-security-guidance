"""Behavior checks use temporary, inert source files; none are executed."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).with_name("check_unicode_source.py")


class UnicodeSourceCheckTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def run_check(self, *paths):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *(str(path) for path in paths)],
            text=True, capture_output=True, check=False,
        )

    def source(self, text=None, data=None):
        path = self.root / "example.py"
        path.write_bytes(data if data is not None else text.encode("utf-8"))
        return path

    def test_safe_multilingual_string(self):
        result = self.run_check(self.source('message = "日本語の文章"\n'))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS 1", result.stdout)

    def test_safe_multilingual_fstring(self):
        result = self.run_check(self.source('value = 1\nmessage = f"日本語 {value}"\n'))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_bidi_in_comment(self):
        result = self.run_check(self.source("# note " + chr(0x202E) + " hidden\n"))
        self.assertEqual(result.returncode, 1)
        self.assertIn("U+202E bidi-control", result.stdout)
        self.assertNotIn("hidden", result.stdout)

    def test_invisible_in_string(self):
        result = self.run_check(self.source('message = "a' + chr(0x200B) + 'b"\n'))
        self.assertEqual(result.returncode, 1)
        self.assertIn("U+200B invisible-format", result.stdout)

    def test_confusable_identifier(self):
        result = self.run_check(self.source("p" + chr(0x0430) + "yload = 1\n"))
        self.assertEqual(result.returncode, 1)
        self.assertIn("U+0430 non-ascii-identifier", result.stdout)

    def test_nfkc_changing_identifier(self):
        result = self.run_check(self.source(chr(0xFF56) + "alue = 1\n"))
        self.assertEqual(result.returncode, 1)
        self.assertIn("U+FF56 identifier-normalization-change", result.stdout)

    def test_identifier_inside_fstring_expression(self):
        source = 'message = f"日本語{' + chr(0xFF56) + 'alue}"\n'
        result = self.run_check(self.source(source))
        self.assertEqual(result.returncode, 1)
        self.assertIn("U+FF56 identifier-normalization-change", result.stdout)

    def test_attribute_inside_fstring_expression(self):
        source = 'message = f"{obj.' + chr(0x0430) + '}"\n'
        result = self.run_check(self.source(source))
        self.assertEqual(result.returncode, 1)
        self.assertIn("U+0430 non-ascii-identifier", result.stdout)

    def test_invalid_utf8_and_syntax_are_errors(self):
        bad_bytes = self.run_check(self.source(data=b"value = \xff\n"))
        self.assertEqual(bad_bytes.returncode, 2)
        self.assertIn("invalid-utf8", bad_bytes.stdout)
        bad_syntax = self.run_check(self.source("if True print('x')\n"))
        self.assertEqual(bad_syntax.returncode, 2)
        self.assertIn("invalid-python-source", bad_syntax.stdout)

    def test_unsupported_encoding_is_error(self):
        result = self.run_check(self.source(data=b"# coding: latin-1\nvalue = 1\n"))
        self.assertEqual(result.returncode, 2)
        self.assertIn("non-utf8-source", result.stdout)

    def test_empty_scope_is_error(self):
        result = self.run_check(self.root)
        self.assertEqual(result.returncode, 2)
        self.assertIn("no-python-source", result.stdout)

    def test_symlink_source_is_error(self):
        target = self.source("value = 1\n")
        link = self.root / "alias.py"
        try:
            link.symlink_to(target)
        except OSError:
            self.skipTest("symlinks unavailable")
        result = self.run_check(self.root)
        self.assertEqual(result.returncode, 2)
        self.assertIn("symlink-source", result.stdout)


if __name__ == "__main__":
    unittest.main()
