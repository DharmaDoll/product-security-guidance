#!/usr/bin/env python3
"""Small GitHub public-source watch: collect candidates, review, then notify."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener


API_BASE = "https://api.github.com"
API_VERSION = "2026-03-10"
SCHEMA = "github-indicator-watch/v1"
ID_RE = re.compile(r"^[a-z][a-z0-9-]{1,39}$")
DOMAIN_RE = re.compile(r"^[a-z0-9-]+(?:\.[a-z0-9-]+)+$")
EMAIL_RE = re.compile(r"^[a-z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-z0-9-]+(?:\.[a-z0-9-]+)+$")
SURFACES = (("code", "search/code"), ("issue", "search/issues"), ("pr", "search/issues"))


class WatchError(Exception):
    pass


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, message, headers, new_url):
        return None


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_config(path: Path) -> list[dict[str, str]]:
    try:
        config = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise WatchError("設定ファイルを読めません") from exc
    if not isinstance(config, dict) or set(config) != {"indicators"}:
        raise WatchError("設定は indicators のみを含めてください")
    entries = config["indicators"]
    if not isinstance(entries, list) or not 1 <= len(entries) <= 5:
        raise WatchError("指標は1〜5件に絞ってください")
    ids: set[str] = set()
    values: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != {"id", "kind", "value"}:
            raise WatchError("指標には id, kind, value が必要です")
        ident, kind, value = entry["id"], entry["kind"], entry["value"]
        if not isinstance(ident, str) or not ID_RE.fullmatch(ident):
            raise WatchError("指標IDの形式が不正です")
        if not isinstance(value, str) or value != value.lower() or len(value) > 253:
            raise WatchError("指標値は小文字で指定してください")
        if kind == "domain":
            valid = bool(DOMAIN_RE.fullmatch(value)) and all(
                label and not label.startswith("-") and not label.endswith("-") and len(label) <= 63
                for label in value.split(".")
            )
        elif kind == "email":
            valid = bool(EMAIL_RE.fullmatch(value))
        else:
            valid = False
        if not valid or ident in ids or value in values:
            raise WatchError("指標の値・種別・重複を確認してください")
        ids.add(ident)
        values.add(value)
    return entries


def load_state(path: Path) -> dict:
    if not path.exists():
        return {"schema": SCHEMA, "findings": {}}
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise WatchError("状態ファイルを読めません。空の状態から再開しないでください") from exc
    if not isinstance(state, dict) or state.get("schema") != SCHEMA or not isinstance(state.get("findings"), dict):
        raise WatchError("状態ファイルの形式が不正です")
    for ident, finding in state["findings"].items():
        if not isinstance(finding, dict) or ident != finding.get("id") or finding.get("status") not in {"pending", "notified"} or not isinstance(finding.get("indicator_ids"), list):
            raise WatchError("状態ファイルに不正な候補があります")
    return state


def save_state(path: Path, state: dict) -> None:
    temporary = None
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        descriptor, name = tempfile.mkstemp(prefix=".watch-", dir=path.parent)
        temporary = Path(name)
        os.fchmod(descriptor, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(state, stream, ensure_ascii=False, indent=2, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except OSError as exc:
        raise WatchError("状態ファイルを保存できません") from exc
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def request_json(url: str, token: str, *, payload: dict | None = None, webhook_token: str = "") -> dict:
    headers = {"Accept": "application/json" if payload is not None else "application/vnd.github+json", "User-Agent": "github-indicator-watch/1"}
    if payload is None:
        headers["Authorization"] = f"Bearer {token}"
        headers["X-GitHub-Api-Version"] = API_VERSION
        data = None
    else:
        headers["Content-Type"] = "application/json"
        headers["Idempotency-Key"] = payload["id"]
        if webhook_token:
            headers["Authorization"] = f"Bearer {webhook_token}"
        data = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    try:
        with build_opener(NoRedirect).open(Request(url, data=data, headers=headers), timeout=12) as response:
            raw = response.read(2 * 1024 * 1024 + 1)
            if len(raw) > 2 * 1024 * 1024:
                raise WatchError("応答が大きすぎます")
            if payload is not None:
                return {}
            result = json.loads(raw)
            if not isinstance(result, dict):
                raise WatchError("GitHub応答の形式が不正です")
            return result
    except HTTPError as exc:
        raise WatchError(f"HTTP {exc.code}。認証・検索制限・通知先を確認してください") from exc
    except (URLError, TimeoutError, UnicodeError, json.JSONDecodeError) as exc:
        raise WatchError("通信または応答の解析に失敗しました") from exc


def query_for(value: str, surface: str) -> str:
    term = f'"{value}"'
    if surface == "code":
        return f"{term} in:file"
    return f"{term} is:{surface} is:public in:title,body"


def candidate(item: dict, surface: str, indicator_id: str) -> dict | None:
    if not isinstance(item, dict):
        raise WatchError("GitHub候補の形式が不正です")
    if surface == "code":
        repository = item.get("repository")
        if not isinstance(repository, dict) or repository.get("private") is not False:
            raise WatchError("公開専用の検索でない結果を受け取りました。専用の認証情報を確認してください")
        repository_id, path = repository.get("id"), item.get("path")
        if not isinstance(repository_id, int) or isinstance(repository_id, bool) or repository_id <= 0 or not isinstance(path, str) or not path:
            raise WatchError("GitHub code候補の識別情報が不正です")
        resource = f"{repository_id}:{path}"
    else:
        resource_id = item.get("id")
        if not isinstance(resource_id, int) or isinstance(resource_id, bool) or resource_id <= 0:
            raise WatchError("GitHub Issue/PR候補の識別情報が不正です")
        resource = str(resource_id)
    url = item.get("html_url")
    if not isinstance(url, str):
        raise WatchError("GitHub候補のURLがありません")
    parsed = urlparse(url)
    if (parsed.scheme != "https" or parsed.netloc != "github.com" or parsed.username or parsed.password
            or parsed.query or parsed.fragment or not parsed.path.startswith("/") or len(url) > 2048
            or any(ord(character) < 32 or ord(character) == 127 for character in url)):
        raise WatchError("GitHub候補のURLが不正です")
    ident = hashlib.sha256(f"{surface}\0{resource}".encode()).hexdigest()[:24]
    return {"id": ident, "indicator_ids": [indicator_id], "surface": surface, "url": url}


def scan(config: list[dict[str, str]], state: dict, token: str, *, api_base: str = API_BASE, pause: float = 1.0) -> tuple[list[dict], list[str]]:
    found: dict[str, dict] = {}
    partial: list[str] = []
    for entry in config:
        for surface, endpoint in SURFACES:
            url = f"{api_base}/{endpoint}?" + urlencode({"q": query_for(entry["value"], surface), "per_page": 100})
            result = request_json(url, token)
            if result.get("incomplete_results") is not False or not isinstance(result.get("items"), list):
                raise WatchError("検索結果が不完全または不正です。状態は更新しません")
            total = result.get("total_count")
            if not isinstance(total, int) or isinstance(total, bool) or total < len(result["items"]):
                raise WatchError("検索件数が不正です。状態は更新しません")
            if total > len(result["items"]):
                partial.append(f"{entry['id']}/{surface}: {len(result['items'])}/{total}件のみ取得")
            for item in result["items"]:
                record = candidate(item, surface, entry["id"])
                if record is not None:
                    previous = found.get(record["id"])
                    if previous is None:
                        found[record["id"]] = record
                    else:
                        previous["indicator_ids"] = sorted(set(previous["indicator_ids"] + record["indicator_ids"]))
            if pause:
                time.sleep(pause)
    timestamp = now_iso()
    new = []
    for ident, record in found.items():
        existing = state["findings"].get(ident)
        if existing is None:
            state["findings"][ident] = {**record, "status": "pending", "first_seen": timestamp, "last_seen": timestamp}
            new.append(record)
        else:
            existing["last_seen"] = timestamp
            existing["indicator_ids"] = sorted(set(existing["indicator_ids"] + record["indicator_ids"]))
            existing["url"] = record["url"]
    return new, partial


def notify(state: dict, ident: str, webhook_url: str, webhook_token: str = "") -> None:
    finding = state["findings"].get(ident)
    if finding is None or finding["status"] != "pending":
        raise WatchError("未通知の候補IDを指定してください")
    parsed = urlparse(webhook_url)
    local = parsed.hostname in {"127.0.0.1", "localhost"}
    if parsed.scheme != "https" and not (local and parsed.scheme == "http"):
        raise WatchError("通知先にはHTTPS URLを指定してください")
    if parsed.username or parsed.password or not parsed.hostname:
        raise WatchError("通知先URLが不正です")
    request_json(webhook_url, "", payload={"id": ident, "source": "github-public-search", "indicator_ids": finding["indicator_ids"], "surface": finding["surface"], "url": finding["url"]}, webhook_token=webhook_token)
    finding["status"] = "notified"
    finding["notified_at"] = now_iso()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    scan_parser = sub.add_parser("scan", help="公開候補を収集する")
    scan_parser.add_argument("--config", type=Path, required=True)
    scan_parser.add_argument("--state", type=Path, required=True)
    list_parser = sub.add_parser("list", help="人が確認する候補を表示する")
    list_parser.add_argument("--state", type=Path, required=True)
    notify_parser = sub.add_parser("notify", help="精査済みの候補だけ通知する")
    notify_parser.add_argument("--state", type=Path, required=True)
    notify_parser.add_argument("--id", required=True)
    notify_parser.add_argument("--webhook-url", required=True)
    args = parser.parse_args()
    try:
        state = load_state(args.state)
        if args.command == "scan":
            token = os.environ.get("GITHUB_TOKEN", "")
            if not token:
                raise WatchError("GITHUB_TOKEN が必要です")
            new, partial = scan(load_config(args.config), state, token)
            save_state(args.state, state)
            for finding in new:
                print(f"NEW {finding['id']} {','.join(finding['indicator_ids'])} {finding['surface']} {finding['url']}")
            for warning in partial:
                print(f"PARTIAL {warning}", file=sys.stderr)
            print(f"候補追加={len(new)} 未通知={sum(f['status'] == 'pending' for f in state['findings'].values())}")
            return 2 if partial else 0
        if args.command == "list":
            for finding in state["findings"].values():
                if finding["status"] == "pending":
                    print(f"{finding['id']} {','.join(finding['indicator_ids'])} {finding['surface']} {finding['url']}")
            return 0
        notify(state, args.id, args.webhook_url, os.environ.get("WEBHOOK_TOKEN", ""))
        save_state(args.state, state)
        print(f"NOTIFIED {args.id}")
        return 0
    except WatchError as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
