#!/usr/bin/env python3
"""Small standard-library secret pattern scanner for local Git hooks."""

from __future__ import annotations

import argparse
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys


MAX_FILE_BYTES = 5 * 1024 * 1024
ZERO_OID = re.compile(r"^0+$")

BLOCKED_NAMES = {
    ".ds_store",
    ".netrc",
    "credentials.json",
    "id_dsa",
    "id_ecdsa",
    "id_ed25519",
    "id_rsa",
    "thumbs.db",
}
BLOCKED_SUFFIXES = {
    ".7z", ".bin", ".class", ".db", ".dll", ".dylib", ".exe", ".gz",
    ".jar", ".jks", ".key", ".keystore", ".mdb", ".msi", ".p12",
    ".pem", ".pfx", ".pyc", ".pyo", ".rar", ".so", ".sqlite",
    ".sqlite3", ".tar", ".war", ".zip",
}
ALLOWED_ENV_ENDINGS = (".example", ".sample", ".template")

SECRET_RULES = {
    "private-key": rb"-----BEGIN(?: [A-Z0-9]+)? PRIVATE KEY-----",
    "github-token": rb"\bgh[pousr]_[A-Za-z0-9]{36,}\b",
    "github-fine-grained-pat": rb"\bgithub_pat_[A-Za-z0-9_]{82}\b",
    "aws-access-key": rb"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b",
    "aws-secret-access-key": (
        rb"(?im)^\s*(?:aws_)?secret_access_key\s*[:=]\s*['\"]?"
        rb"[A-Za-z0-9/+=]{40}(?=$|[\s'\"])"
    ),
    "google-api-key": rb"\bAIza[0-9A-Za-z_-]{35}\b",
    "jwt": (
        rb"\beyJ[A-Za-z0-9_-]{5,}\.[A-Za-z0-9_-]{5,}\."
        rb"[A-Za-z0-9_-]{5,}\b"
    ),
    "bearer-token": rb"(?i)\bbearer\s+[A-Za-z0-9._~+/=-]{16,}",
    "slack-webhook": (
        rb"https://hooks\.slack\.com/services/[A-Za-z0-9]{8,}/"
        rb"[A-Za-z0-9]{8,}/[A-Za-z0-9]{16,}"
    ),
    "npmrc-auth-token": (
        rb"(?im)^\s*//[^\s=]+/:_(?:authToken|auth|password)\s*=\s*"
        rb"['\"]?[A-Za-z0-9+/=_-]{20,}"
    ),
    "pypi-api-token": rb"\bpypi-[A-Za-z0-9_-]{85,}\b",
    "credential-assignment": (
        rb"(?im)^\s*(?:api[_-]?key|client[_-]?secret|password|token|"
        rb"access[_-]?token|refresh[_-]?token|auth[_-]?token|"
        rb"private[_-]?token|webhook[_-]?secret|signing[_-]?secret)"
        rb"\s*[:=]\s*['\"]?[A-Za-z0-9/+_.-]{12,}"
    ),
}
COMPILED_RULES = {
    name: re.compile(pattern) for name, pattern in SECRET_RULES.items()
}


class ScanError(RuntimeError):
    """The scanner could not produce a result."""


def git(*arguments: str) -> bytes:
    """Run Git and return stdout, or stop when the input cannot be inspected."""
    try:
        result = subprocess.run(
            ["git", *arguments],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise ScanError(f"cannot execute git: {error}") from error
    if result.returncode != 0:
        raise ScanError(f"git {' '.join(arguments)} failed")
    return result.stdout


def blocked_path(path: str) -> bool:
    """Return True for file types this text-only example does not inspect."""
    name = PurePosixPath(path).name.lower()
    if name == ".env" or name.startswith(".env."):
        return not name.endswith(ALLOWED_ENV_ENDINGS)
    return name in BLOCKED_NAMES or PurePosixPath(name).suffix in BLOCKED_SUFFIXES


def scan(label: str, content: bytes) -> list[tuple[str, str]]:
    """Return rule names and locations without returning matched values."""
    if len(content) > MAX_FILE_BYTES:
        return [("file-too-large", label)]
    if b"\0" in content:
        return [("binary-file", label)]

    findings: list[tuple[str, str]] = []
    if blocked_path(label):
        findings.append(("sensitive-filename", label))
    for name, pattern in COMPILED_RULES.items():
        if pattern.search(content):
            findings.append((name, label))
    return findings


def decode_paths(raw: bytes) -> list[str]:
    return [
        item.decode("utf-8", errors="surrogateescape")
        for item in raw.split(b"\0")
        if item
    ]


def scan_staged() -> list[tuple[str, str]]:
    findings: list[tuple[str, str]] = []
    paths = decode_paths(
        git("diff", "--cached", "--name-only", "-z", "--diff-filter=ACMR")
    )
    for path in paths:
        findings.extend(scan(path, git("show", f":{path}")))
    return findings


def scan_commit(commit: str) -> list[tuple[str, str]]:
    short = commit[:12]
    findings = scan(
        f"{short}:commit-message",
        git("show", "-s", "--format=%B", commit),
    )
    paths = decode_paths(
        git(
            "diff-tree", "--root", "--no-commit-id", "--name-only",
            "--diff-filter=ACMR", "-r", "-z", commit,
        )
    )
    for path in paths:
        for rule, _label in scan(path, git("show", f"{commit}:{path}")):
            findings.append((rule, f"{short}:{path}"))
    return findings


def introduced_commits() -> list[str]:
    """Read pre-push stdin and return commits introduced by the updates."""
    commits: list[str] = []
    for number, line in enumerate(sys.stdin, start=1):
        fields = line.split()
        if len(fields) != 4:
            raise ScanError(f"invalid pre-push input at line {number}")
        _local_ref, local_oid, _remote_ref, remote_oid = fields
        if ZERO_OID.fullmatch(local_oid):
            continue
        if ZERO_OID.fullmatch(remote_oid):
            revision = ("rev-list", local_oid)
        else:
            revision = ("rev-list", f"{remote_oid}..{local_oid}")
        commits.extend(git(*revision).decode("ascii").splitlines())
    return list(dict.fromkeys(commits))


def scan_history() -> list[tuple[str, str]]:
    findings: list[tuple[str, str]] = []
    for commit in introduced_commits():
        findings.extend(scan_commit(commit))
    return findings


def report(findings: list[tuple[str, str]]) -> int:
    for rule, label in findings:
        print(f"BLOCK {rule} {json.dumps(label, ensure_ascii=True)}")
    if findings:
        print(f"REJECTED {len(findings)} finding(s); matched values suppressed")
        return 1
    print("ACCEPTED no sensitive-data findings")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--staged", action="store_true")
    mode.add_argument("--pre-push", action="store_true")
    mode.add_argument("--file", type=Path)
    parser.add_argument("--label")
    args = parser.parse_args()

    try:
        if args.staged:
            findings = scan_staged()
        elif args.pre_push:
            findings = scan_history()
        else:
            if args.file is None or not args.label:
                raise ScanError("--file requires --label")
            findings = scan(args.label, args.file.read_bytes())
    except (OSError, UnicodeError, ScanError) as error:
        print(f"ERROR {error}", file=sys.stderr)
        return 2
    return report(findings)


if __name__ == "__main__":
    raise SystemExit(main())
