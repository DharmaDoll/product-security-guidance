"""Local HTTP smoke tests for the GitHub indicator watch."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse


spec = importlib.util.spec_from_file_location("indicator_watch", Path(__file__).with_name("watch.py"))
watch = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(watch)


class Handler(BaseHTTPRequestHandler):
    requests = 0
    notifications = []
    incomplete = False
    total = 1
    private_code = False
    webhook_status = 204

    def log_message(self, *_args):
        pass

    def do_GET(self):
        type(self).requests += 1
        query = parse_qs(urlparse(self.path).query).get("q", [""])[0]
        if self.path.startswith("/search/code"):
            item = {"repository": {"id": 7, "private": type(self).private_code}, "path": "config/app.txt", "html_url": "https://github.com/example/public/blob/abc/config/app.txt"}
        elif "is:pr" in query:
            item = {"id": 12, "html_url": "https://github.com/example/public/pull/2"}
        else:
            item = {"id": 11, "html_url": "https://github.com/example/public/issues/1"}
        payload = {"total_count": type(self).total, "incomplete_results": type(self).incomplete, "items": [item]}
        body = json.dumps(payload).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        body = self.rfile.read(int(self.headers["Content-Length"]))
        type(self).notifications.append((json.loads(body), self.headers.get("Idempotency-Key")))
        self.send_response(type(self).webhook_status)
        self.end_headers()


class WatchTests(unittest.TestCase):
    def setUp(self):
        Handler.requests = 0
        Handler.notifications = []
        Handler.incomplete = False
        Handler.total = 1
        Handler.private_code = False
        Handler.webhook_status = 204
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.base = f"http://127.0.0.1:{self.server.server_address[1]}"
        self.temp = tempfile.TemporaryDirectory()
        self.state_path = Path(self.temp.name) / "state.json"
        self.config = [
            {"id": "company-domain", "kind": "domain", "value": "example.invalid"},
            {"id": "security-mailbox", "kind": "email", "value": "security@example.invalid"},
        ]

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)
        self.temp.cleanup()

    def test_review_then_notify_once_and_suppress_duplicate_search_hits(self):
        state = watch.load_state(self.state_path)
        first, partial = watch.scan(self.config, state, "synthetic-token", api_base=self.base, pause=0)
        self.assertEqual(6, Handler.requests)
        self.assertEqual(3, len(first))
        self.assertEqual([], partial)
        self.assertTrue(all(len(item["indicator_ids"]) == 2 for item in first))
        self.assertEqual([], Handler.notifications)
        watch.save_state(self.state_path, state)
        state = watch.load_state(self.state_path)
        ident = first[0]["id"]
        watch.notify(state, ident, self.base + "/webhook")
        self.assertEqual(1, len(Handler.notifications))
        self.assertEqual(ident, Handler.notifications[0][1])
        self.assertNotIn("example.invalid", json.dumps(Handler.notifications[0][0]))
        with self.assertRaises(watch.WatchError):
            watch.notify(state, ident, self.base + "/webhook")
        second, _ = watch.scan(self.config, state, "synthetic-token", api_base=self.base, pause=0)
        self.assertEqual([], second)
        self.assertEqual(1, len(Handler.notifications))

    def test_incomplete_search_does_not_advance_state(self):
        Handler.incomplete = True
        state = watch.load_state(self.state_path)
        with self.assertRaises(watch.WatchError):
            watch.scan(self.config, state, "synthetic-token", api_base=self.base, pause=0)
        self.assertEqual({}, state["findings"])

    def test_private_code_result_is_rejected(self):
        Handler.private_code = True
        state = watch.load_state(self.state_path)
        with self.assertRaises(watch.WatchError):
            watch.scan(self.config[:1], state, "synthetic-token", api_base=self.base, pause=0)
        self.assertEqual({}, state["findings"])

    def test_failed_webhook_does_not_suppress_notification(self):
        Handler.webhook_status = 500
        state = watch.load_state(self.state_path)
        new, _ = watch.scan(self.config[:1], state, "synthetic-token", api_base=self.base, pause=0)
        with self.assertRaises(watch.WatchError):
            watch.notify(state, new[0]["id"], self.base + "/webhook")
        self.assertEqual("pending", state["findings"][new[0]["id"]]["status"])

    def test_result_cap_is_reported_with_observed_candidates(self):
        Handler.total = 101
        state = watch.load_state(self.state_path)
        new, partial = watch.scan(self.config[:1], state, "synthetic-token", api_base=self.base, pause=0)
        self.assertEqual(3, len(new))
        self.assertEqual(3, len(partial))

    def test_bad_indicator_and_corrupt_state_are_rejected(self):
        path = Path(self.temp.name) / "config.json"
        path.write_text('{"indicators":[{"id":"company-domain","kind":"domain","value":"*example.invalid"}]}', encoding="utf-8")
        with self.assertRaises(watch.WatchError):
            watch.load_config(path)
        self.state_path.write_text("{", encoding="utf-8")
        with self.assertRaises(watch.WatchError):
            watch.load_state(self.state_path)


if __name__ == "__main__":
    unittest.main()
