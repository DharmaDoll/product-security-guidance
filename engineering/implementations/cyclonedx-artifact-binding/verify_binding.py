#!/usr/bin/env python3
"""Verify a bounded CycloneDX 1.7 release-artifact binding contract."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


SERIAL_RE = re.compile(
    r"^urn:uuid:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
)
VERSIONED_PURL_RE = re.compile(r"^pkg:[^@\s]+@[^?\s#]+(?:\?[^#\s]+)?(?:#[^\s]+)?$")
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")
RELEASE_PHASES = {"build", "post-build"}
COMPOSITION_STATES = {
    "complete",
    "incomplete",
    "incomplete_first_party_only",
    "incomplete_first_party_proprietary_only",
    "incomplete_first_party_opensource_only",
    "incomplete_third_party_only",
    "incomplete_third_party_proprietary_only",
    "incomplete_third_party_opensource_only",
    "unknown",
    "not_specified",
}


class Rejected(ValueError):
    """The input was readable but violated the binding contract."""


class InputError(RuntimeError):
    """The input could not be evaluated reliably."""


def require_object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise Rejected(f"{label} must be an object")
    return value


def require_list(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise Rejected(f"{label} must be an array")
    return value


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise Rejected(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise InputError(f"SBOM contains a non-JSON constant: {value}")


def read_sbom(path: Path, max_bytes: int) -> tuple[dict[str, Any], bytes]:
    try:
        size = path.stat().st_size
        if size > max_bytes:
            raise InputError(f"SBOM exceeds the {max_bytes}-byte input limit")
        raw = path.read_bytes()
        if len(raw) > max_bytes:
            raise InputError(f"SBOM exceeds the {max_bytes}-byte input limit")
    except OSError as error:
        raise InputError(f"cannot read SBOM: {error}") from error
    try:
        document = json.loads(raw, object_pairs_hook=unique_object, parse_constant=reject_constant)
    except (json.JSONDecodeError, UnicodeDecodeError, RecursionError) as error:
        raise InputError(f"SBOM is not parseable JSON: {error}") from error
    return require_object(document, "SBOM"), raw


def hash_artifact(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            for block in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(block)
    except OSError as error:
        raise InputError(f"cannot read artifact: {error}") from error
    return digest.hexdigest()


def check_document_identity(sbom: dict[str, Any]) -> tuple[str, int]:
    if sbom.get("bomFormat") != "CycloneDX" or sbom.get("specVersion") != "1.7":
        raise Rejected("only CycloneDX 1.7 JSON is supported")
    serial = sbom.get("serialNumber")
    if not isinstance(serial, str) or not SERIAL_RE.fullmatch(serial):
        raise Rejected("serialNumber must be a lowercase RFC 4122 urn:uuid")
    version = sbom.get("version", 1)
    if not isinstance(version, int) or isinstance(version, bool) or version < 1:
        raise Rejected("version must be a positive integer")
    return serial, version


def check_lifecycle(metadata: dict[str, Any]) -> list[str]:
    phases: list[str] = []
    for index, item in enumerate(require_list(metadata.get("lifecycles"), "metadata.lifecycles")):
        lifecycle = require_object(item, f"metadata.lifecycles[{index}]")
        phase = lifecycle.get("phase")
        if isinstance(phase, str):
            phases.append(phase)
    if not RELEASE_PHASES.intersection(phases):
        raise Rejected("metadata.lifecycles must include build or post-build")
    return phases


def check_component(component: dict[str, Any], label: str) -> tuple[str, str]:
    reference = component.get("bom-ref")
    if not isinstance(reference, str) or not reference:
        raise Rejected(f"{label}.bom-ref must be a non-empty string")
    purl = component.get("purl")
    if not isinstance(purl, str) or not VERSIONED_PURL_RE.fullmatch(purl):
        raise Rejected(f"{label}.purl must identify an exact version")
    return reference, purl


def check_root_hash(root: dict[str, Any], artifact_digest: str) -> None:
    matching_hashes = []
    for index, item in enumerate(require_list(root.get("hashes"), "metadata.component.hashes")):
        hash_record = require_object(item, f"metadata.component.hashes[{index}]")
        if hash_record.get("alg") == "SHA-256":
            content = hash_record.get("content")
            if not isinstance(content, str) or not SHA256_RE.fullmatch(content):
                raise Rejected("metadata.component SHA-256 is malformed")
            matching_hashes.append(content.lower())
    if len(matching_hashes) != 1:
        raise Rejected("metadata.component must contain exactly one SHA-256 hash")
    if matching_hashes[0] != artifact_digest:
        raise Rejected("artifact SHA-256 does not match metadata.component")


def check_references(sbom: dict[str, Any], root: dict[str, Any]) -> tuple[str, int, set[str]]:
    root_ref, _ = check_component(root, "metadata.component")
    references = {root_ref}
    components = require_list(sbom.get("components"), "components")
    for index, item in enumerate(components):
        component = require_object(item, f"components[{index}]")
        reference, _ = check_component(component, f"components[{index}]")
        if reference in references:
            raise Rejected(f"duplicate bom-ref: {reference}")
        references.add(reference)

    dependency_subjects: set[str] = set()
    for index, item in enumerate(require_list(sbom.get("dependencies"), "dependencies")):
        dependency = require_object(item, f"dependencies[{index}]")
        reference = dependency.get("ref")
        if not isinstance(reference, str) or reference not in references:
            raise Rejected(f"dependencies[{index}].ref does not resolve")
        if reference in dependency_subjects:
            raise Rejected(f"duplicate dependency subject: {reference}")
        dependency_subjects.add(reference)
        targets = require_list(dependency.get("dependsOn"), f"dependencies[{index}].dependsOn")
        if any(not isinstance(target, str) for target in targets):
            raise Rejected(f"dependencies[{index}].dependsOn must contain strings")
        if len(targets) != len(set(targets)):
            raise Rejected(f"dependencies[{index}].dependsOn contains duplicates")
        for target in targets:
            if target not in references:
                raise Rejected(f"dependencies[{index}] contains an unresolved target")
    if root_ref not in dependency_subjects:
        raise Rejected("root component has no dependency relationship record")
    return root_ref, len(components), references


def check_composition(sbom: dict[str, Any], root_ref: str, references: set[str]) -> str:
    matching_states: list[str] = []
    for index, item in enumerate(require_list(sbom.get("compositions"), "compositions")):
        composition = require_object(item, f"compositions[{index}]")
        assemblies = require_list(composition.get("assemblies", []), f"compositions[{index}].assemblies")
        for field in ("assemblies", "dependencies"):
            targets = require_list(composition.get(field, []), f"compositions[{index}].{field}")
            if any(not isinstance(target, str) for target in targets):
                raise Rejected(f"compositions[{index}].{field} must contain strings")
            if len(targets) != len(set(targets)):
                raise Rejected(f"compositions[{index}].{field} contains duplicates")
            if any(target not in references for target in targets):
                raise Rejected(f"compositions[{index}].{field} contains an unresolved target")
        if root_ref in assemblies:
            aggregate = composition.get("aggregate")
            if not isinstance(aggregate, str) or aggregate not in COMPOSITION_STATES:
                raise Rejected(f"compositions[{index}].aggregate is unsupported")
            matching_states.append(aggregate)
    if len(matching_states) != 1:
        raise Rejected("exactly one composition must describe the root assembly")
    return matching_states[0]


def verify(artifact: Path, sbom_path: Path, max_sbom_bytes: int) -> dict[str, Any]:
    if max_sbom_bytes < 1:
        raise InputError("max SBOM bytes must be positive")
    artifact_digest = hash_artifact(artifact)
    sbom, raw_sbom = read_sbom(sbom_path, max_sbom_bytes)
    serial, version = check_document_identity(sbom)
    metadata = require_object(sbom.get("metadata"), "metadata")
    phases = check_lifecycle(metadata)
    root = require_object(metadata.get("component"), "metadata.component")
    check_root_hash(root, artifact_digest)
    root_ref, component_count, references = check_references(sbom, root)
    composition = check_composition(sbom, root_ref, references)
    return {
        "status": "PASS",
        "artifact_sha256": artifact_digest,
        "sbom_sha256": hashlib.sha256(raw_sbom).hexdigest(),
        "bom_serial": serial,
        "bom_version": version,
        "root_ref": root_ref,
        "observation_phases": phases,
        "component_count": component_count,
        "composition": composition,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact", type=Path, required=True)
    parser.add_argument("--sbom", type=Path, required=True)
    parser.add_argument("--max-sbom-bytes", type=int, default=10 * 1024 * 1024)
    args = parser.parse_args()
    try:
        result = verify(args.artifact, args.sbom, args.max_sbom_bytes)
    except Rejected as error:
        print(f"REJECT {error}", file=sys.stderr)
        return 1
    except InputError as error:
        print(f"ERROR {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
