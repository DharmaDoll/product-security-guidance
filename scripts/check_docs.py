"""Offline Markdown link, boundary and control-ID checks; no adoption claims."""

from pathlib import Path
import re
import sys
import unicodedata
from urllib.parse import unquote, urlsplit

LINK = re.compile(r"\[[^\]\n]*\]\(([^)\s]+)\)")


def anchors(text):
    result = set(re.findall(r'<a\s+(?:id|name)=[\"\']([^\"\']+)', text))
    seen = {}
    for heading in re.findall(r"^#{1,6}\s+(.+)", text, re.M):
        heading = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", heading)
        heading = re.sub(r"<[^>]+>", "", heading).strip().lower()
        slug = "".join(c for c in heading if c in "-_ " or unicodedata.category(c)[0] in "LN").replace(" ", "-")
        n = seen.get(slug, 0)
        seen[slug] = n + 1
        result.add(slug + (f"-{n}" if n else ""))
    return result


def check(root):
    root = root.resolve()
    errors = []
    count = 0
    for file in sorted(root.rglob("*.md")):
        for raw in LINK.findall(file.read_text(encoding="utf-8")):
            parts = urlsplit(raw)
            if parts.scheme in {"https", "http", "mailto"}:
                continue
            if parts.scheme or parts.netloc:
                errors.append(f"{file.relative_to(root)}: unsupported link {raw}")
                continue
            count += 1
            target = (file.parent / unquote(parts.path)).resolve() if parts.path else file
            if not target.is_relative_to(root):
                errors.append(f"{file.relative_to(root)}: link escapes repository: {raw}")
            elif not target.exists():
                errors.append(f"{file.relative_to(root)}: missing target: {raw}")
            elif parts.fragment and target.suffix == ".md" and unquote(parts.fragment) not in anchors(target.read_text(encoding="utf-8")):
                errors.append(f"{file.relative_to(root)}: missing anchor: {raw}")
    ids = set()
    records = sorted((root / "controls/records").rglob("control.yaml"))
    if not records:
        errors.append("No control records found")
    for file in records:
        # Supports both current YAML and JSON-formatted YAML record headers.
        found = re.findall(r'^\s{0,2}[\"\']?id[\"\']?\s*:\s*[\"\']?(PSB-[A-Z]+-\d{3})[\"\']?\s*,?\s*$', file.read_text(), re.M)
        if len(found) != 1 or found[0] in ids:
            errors.append(f"{file.relative_to(root)}: missing or duplicate control ID")
        else:
            ids.add(found[0])
    return errors, count, len(ids)


if __name__ == "__main__":
    errors, count, records = check(Path(__file__).resolve().parents[1])
    for error in errors:
        print(error, file=sys.stderr)
    print(f"{count} local links; {records} unique control IDs; {len(errors)} errors")
    sys.exit(bool(errors))
