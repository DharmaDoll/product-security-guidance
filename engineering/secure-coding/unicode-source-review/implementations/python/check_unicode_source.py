#!/usr/bin/env python3
"""Strict UTF-8 Python source review example. Never executes inspected source."""

import argparse
import ast
import io
import os
from pathlib import Path
import sys
import tokenize
import unicodedata


# Deliberately narrow project policy, not a Unicode-wide security profile.
BIDI = {0x061C, 0x200E, 0x200F, *range(0x202A, 0x202F), *range(0x2066, 0x206A)}
INVISIBLE = {
    0x00AD, 0x034F, 0x180E, 0x200B, 0x200C, 0x200D, 0x2060, 0xFEFF,
    *range(0x206A, 0x2070), *range(0xFFF9, 0xFFFC),
    *range(0xE0001, 0xE0080),
}


def label(path):
    # A filename can contain control characters; never print it verbatim.
    return ascii(str(path))


def source_files(paths):
    files = set()
    errors = []
    for selected in paths:
        path = Path(selected)
        if path.is_symlink():
            errors.append(f"ERROR {label(path)} symlink-target")
        elif path.is_file():
            if path.suffix == ".py":
                files.add(path)
            else:
                errors.append(f"ERROR {label(path)} not-python-source")
        elif path.is_dir():
            def walk_error(exc):
                errors.append(f"ERROR {label(exc.filename)} unreadable-directory")

            for root, dirs, names in os.walk(path, followlinks=False, onerror=walk_error):
                for name in dirs[:]:
                    candidate = Path(root) / name
                    if candidate.is_symlink():
                        errors.append(f"ERROR {label(candidate)} symlink-directory")
                        dirs.remove(name)
                for name in names:
                    if not name.endswith(".py"):
                        continue
                    candidate = Path(root) / name
                    if candidate.is_symlink():
                        errors.append(f"ERROR {label(candidate)} symlink-source")
                    else:
                        files.add(candidate)
        else:
            errors.append(f"ERROR {label(path)} missing-input")
    if not files:
        errors.append("ERROR no-python-source")
    return sorted(files), errors


def scan(path):
    findings = []
    errors = []
    try:
        raw = path.read_bytes()
    except OSError:
        return findings, [f"ERROR {label(path)} unreadable-source"]

    try:
        # This implementation accepts only UTF-8, so decode failure is final.
        source = raw.decode("utf-8")
    except UnicodeDecodeError:
        return findings, [f"ERROR {label(path)} invalid-utf8"]
    try:
        declared_encoding, _ = tokenize.detect_encoding(io.BytesIO(raw).readline)
    except (SyntaxError, LookupError):
        return findings, [f"ERROR {label(path)} invalid-encoding-declaration"]
    if declared_encoding not in ("utf-8", "utf-8-sig"):
        return findings, [f"ERROR {label(path)} non-utf8-source"]
    # Decode BOM as U+FEFF so the character policy reports its location.
    # Python line endings are CRLF, CR, and LF; splitlines() also splits at
    # Unicode separators which Python does not treat as source line endings.
    for line_number, line in enumerate(source.replace("\r\n", "\n").replace("\r", "\n").split("\n"), 1):
        for column, char in enumerate(line, 1):
            point = ord(char)
            if point in BIDI or point in INVISIBLE:
                category = "bidi-control" if point in BIDI else "invisible-format"
                findings.append(
                    f"REJECT {label(path)}:{line_number}:{column} U+{point:04X} {category}"
                )

    try:
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, ValueError):
        errors.append(f"ERROR {label(path)} invalid-python-source")
        return findings, errors

    def report_identifier(spelling, line, column):
        points = sorted({ord(char) for char in spelling if not char.isascii()})
        if not points:
            return
        category = (
            "identifier-normalization-change"
            if unicodedata.normalize("NFKC", spelling) != spelling
            else "non-ascii-identifier"
        )
        codes = ",".join(f"U+{point:04X}" for point in points)
        findings.append(f"REJECT {label(path)}:{line}:{column} {codes} {category}")

    try:
        tokens = tokenize.generate_tokens(io.StringIO(source).readline)
        for token in tokens:
            if token.type == tokenize.NAME:
                report_identifier(token.string, token.start[0], token.start[1] + 1)
    except (tokenize.TokenError, IndentationError, SyntaxError, ValueError):
        errors.append(f"ERROR {label(path)} tokenization-failed")

    # Python 3.10 tokenize treats the whole f-string as STRING; names inside
    # replacement fields need a second pass against AST source positions.
    lines = source.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    for node in ast.walk(tree):
        segment = ast.get_source_segment(source, node)
        if segment is None:
            continue
        if isinstance(node, (ast.Name, ast.arg)):
            spelling, prefix = segment, ""
        elif isinstance(node, ast.Attribute):
            prefix, _, spelling = segment.rpartition(".")
            prefix += "."
            spelling = spelling.strip()
        elif isinstance(node, ast.keyword) and node.arg is not None:
            spelling, _, _ = segment.partition("=")
            prefix = ""
            spelling = spelling.strip()
        else:
            continue
        if not spelling.isidentifier():
            continue
        line = node.lineno + prefix.count("\n")
        if "\n" in prefix:
            column = len(prefix.rsplit("\n", 1)[1]) + 1
        else:
            before = lines[node.lineno - 1].encode("utf-8")[:node.col_offset]
            column = len(before.decode("utf-8")) + len(prefix) + 1
        report_identifier(spelling, line, column)
    return findings, errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", help="Python files or directories to review")
    args = parser.parse_args(argv)
    files, errors = source_files(args.paths)
    findings = []
    for path in files:
        found, failed = scan(path)
        findings.extend(found)
        errors.extend(failed)
    for message in sorted(set(findings)) + sorted(set(errors)):
        print(message)
    if errors:
        return 2
    if findings:
        return 1
    print(f"PASS {len(files)} Python source file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
