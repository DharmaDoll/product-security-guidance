#!/usr/bin/env python3
"""Check direct workflow uses references without network access or code execution."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR PyYAML 6.0.3 is required", file=sys.stderr)
    raise SystemExit(2)


GIT_REF = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_./-]+)?@[0-9a-fA-F]{40}")
DOCKER_REF = re.compile(r"docker://[^@\s]+@sha256:[0-9a-fA-F]{64}")
LOCAL_WORKFLOW = re.compile(r"(?:\./|\$/)\.github/workflows/[^/@\s]+\.ya?ml")
ALLOWED_TAGS = {"tag:yaml.org,2002:" + name for name in ("str", "map", "seq")}


def validate_tree(node, active=None, done=None):
    """Reject ambiguous keys, unsupported tags/merges and cyclic aliases."""
    active = set() if active is None else active
    done = set() if done is None else done
    identity = id(node)
    if identity in active:
        raise ValueError("cyclic YAML alias")
    if identity in done:
        return
    if node.tag not in ALLOWED_TAGS:
        raise ValueError("unsupported YAML tag")
    active.add(identity)
    if isinstance(node, yaml.MappingNode):
        keys = set()
        for key, value in node.value:
            if not isinstance(key, yaml.ScalarNode) or key.tag != "tag:yaml.org,2002:str":
                raise ValueError("mapping key must be a string")
            if key.value == "<<":
                raise ValueError("YAML merge keys are not supported")
            if key.value in keys:
                raise ValueError("duplicate YAML key")
            keys.add(key.value)
            validate_tree(value, active, done)
    elif isinstance(node, yaml.SequenceNode):
        for item in node.value:
            validate_tree(item, active, done)
    active.remove(identity)
    done.add(identity)


def mapping(node, context):
    if not isinstance(node, yaml.MappingNode):
        raise ValueError(context + " must be a mapping")
    return {key.value: value for key, value in node.value}


def references(path):
    # Compose a node tree; do not construct Python objects or infer scalar types.
    tree = yaml.compose(path.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
    if tree is None:
        raise ValueError("empty YAML input")
    validate_tree(tree)
    workflow = mapping(tree, "workflow")
    jobs = mapping(workflow.get("jobs"), "jobs")
    if not jobs:
        raise ValueError("jobs must not be empty")
    found = []
    for job_node in jobs.values():
        job = mapping(job_node, "job")
        if "uses" in job:
            if "steps" in job:
                raise ValueError("job cannot have both uses and steps")
            found.append((job["uses"], True))
            continue
        steps = job.get("steps")
        if not isinstance(steps, yaml.SequenceNode) or not steps.value:
            raise ValueError("ordinary job must have non-empty steps")
        for step_node in steps.value:
            step = mapping(step_node, "step")
            if ("uses" in step) == ("run" in step):
                raise ValueError("step must have exactly one of uses or run")
            if "uses" in step:
                found.append((step["uses"], False))
    return found


def classify(node, reusable):
    if not isinstance(node, yaml.ScalarNode) or node.tag != "tag:yaml.org,2002:str":
        raise ValueError("uses must be a string")
    value = node.value
    if "${{" in value:
        return "REJECT", "computed reference"
    if reusable and LOCAL_WORKFLOW.fullmatch(value):
        return "LOCAL", "same-repository workflow; checkout trust is separate"
    if not reusable and value.startswith("./") and len(value) > 2 and not re.search(r"[@\s]", value):
        return "LOCAL", "same-repository action; checkout trust is separate"
    if not reusable and DOCKER_REF.fullmatch(value):
        return "PINNED", "container digest syntax"
    if GIT_REF.fullmatch(value):
        target = value.rsplit("@", 1)[0]
        if not reusable or re.fullmatch(r"[^/]+/[^/]+/\.github/workflows/[^/]+\.ya?ml", target):
            return "PINNED", "full commit SHA syntax"
    return "REJECT", "expected a full commit SHA or applicable container digest"


def discover(paths):
    found = []
    for raw in paths:
        path = Path(raw)
        if path.is_symlink():
            raise ValueError("symlink input is not supported")
        if path.is_dir():
            candidates = sorted(p for p in path.iterdir() if p.suffix in {".yml", ".yaml"})
        else:
            candidates = [path]
        if not candidates:
            raise ValueError("no workflow YAML files found")
        for candidate in candidates:
            if candidate.is_symlink() or not candidate.is_file() or candidate.suffix not in {".yml", ".yaml"}:
                raise ValueError("missing, unreadable or unsupported workflow input")
            found.append(candidate)
    return list(dict.fromkeys(found))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", help="Workflow files or directories (immediate YAML children).")
    args = parser.parse_args()
    if yaml.__version__ != "6.0.3":
        print("ERROR use the pinned PyYAML 6.0.3 environment", file=sys.stderr)
        return 2
    pinned = local = rejected = 0
    try:
        files = discover(args.paths)
        for path in files:
            for node, reusable in references(path):
                result, reason = classify(node, reusable)
                print(f"{result} {path}:{node.start_mark.line + 1} {reason}")
                pinned += result == "PINNED"
                local += result == "LOCAL"
                rejected += result == "REJECT"
    except (OSError, UnicodeError, ValueError, yaml.YAMLError, RecursionError) as error:
        # Parser exceptions may contain source text: do not print their raw contents.
        reason = str(error) if isinstance(error, ValueError) else type(error).__name__
        print(f"ERROR workflow inspection incomplete: {reason}", file=sys.stderr)
        return 2
    print(f"CHECKED files={len(files)} pinned={pinned} local={local} rejected={rejected}")
    return 1 if rejected else 0


if __name__ == "__main__":
    raise SystemExit(main())
