import sqlite3
import unittest

from access import AccessDenied, InvoiceService, Principal


class AccessTests(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(":memory:")
        self.addCleanup(self.db.close)
        self.db.execute(
            "CREATE TABLE invoices (id TEXT PRIMARY KEY, tenant_id TEXT NOT NULL, "
            "owner_id TEXT NOT NULL, description TEXT NOT NULL)"
        )
        self.db.executemany("INSERT INTO invoices VALUES (?, ?, ?, ?)", [
            ("a", "t1", "alice", "original-a"),
            ("b", "t1", "bob", "original-b"),
            ("c", "t2", "alice", "original-c"),
        ])
        self.db.commit()
        self.service = InvoiceService(self.db)
        self.alice = Principal("alice", "t1", frozenset({"invoice:read", "invoice:update"}))

    def test_owner_read_and_update(self):
        self.assertEqual(self.service.read(self.alice, "a")["description"], "original-a")
        self.service.update(self.alice, "a", {"description": "changed"})
        self.assertEqual(self.service.read(self.alice, "a")["description"], "changed")

    def test_other_owner_other_tenant_unknown_and_injection_denied(self):
        for target in ("b", "c", "missing", "a' OR 1=1 --"):
            with self.subTest(target=target):
                before = self.db.execute("SELECT * FROM invoices ORDER BY id").fetchall()
                with self.assertRaises(AccessDenied):
                    self.service.read(self.alice, target)
                with self.assertRaises(AccessDenied):
                    self.service.update(self.alice, target, {"description": "bad"})
                self.assertEqual(before, self.db.execute("SELECT * FROM invoices ORDER BY id").fetchall())

    def test_missing_context_and_scopes_denied(self):
        for principal in (None, Principal("", "t1", self.alice.scopes),
                          Principal("alice", "", self.alice.scopes),
                          Principal("alice", "t1", frozenset())):
            with self.subTest(principal=principal):
                with self.assertRaises(AccessDenied):
                    self.service.read(principal, "a")
                with self.assertRaises(AccessDenied):
                    self.service.update(principal, "a", {"description": "bad"})

    def test_read_permission_does_not_grant_update(self):
        principal = Principal("alice", "t1", frozenset({"invoice:read"}))
        self.service.read(principal, "a")
        with self.assertRaises(AccessDenied):
            self.service.update(principal, "a", {"description": "bad"})
        self.assertEqual(self.service.read(principal, "a")["description"], "original-a")

    def test_owner_tenant_and_unbounded_changes_rejected(self):
        for changes in ({"description": "bad", "owner_id": "alice"},
                        {"tenant_id": "t1"}, {}, {"description": 1},
                        {"description": "x" * 201}):
            with self.assertRaises(ValueError):
                self.service.update(self.alice, "a", changes)
        self.assertEqual(self.service.read(self.alice, "a")["description"], "original-a")

    def test_current_ownership_is_checked_at_write(self):
        self.service.read(self.alice, "a")
        self.db.execute("UPDATE invoices SET owner_id = 'bob' WHERE id = 'a'")
        self.db.commit()
        with self.assertRaises(AccessDenied):
            self.service.update(self.alice, "a", {"description": "bad"})
        self.assertEqual(self.db.execute("SELECT description FROM invoices WHERE id='a'").fetchone()[0], "original-a")

    def test_database_failure_is_not_success_or_access_denial(self):
        self.db.execute("DROP TABLE invoices")
        with self.assertRaises(sqlite3.OperationalError):
            self.service.read(self.alice, "a")
        with self.assertRaises(sqlite3.OperationalError):
            self.service.update(self.alice, "a", {"description": "bad"})


if __name__ == "__main__":
    unittest.main()
