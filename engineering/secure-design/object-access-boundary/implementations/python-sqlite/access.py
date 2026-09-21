"""Owner-scoped invoice operations; not an authentication implementation."""

import sqlite3
from dataclasses import dataclass


class AccessDenied(Exception):
    """Same public result for missing and inaccessible objects."""


@dataclass(frozen=True)
class Principal:
    # Only the trusted authentication layer may construct this context.
    user_id: str
    tenant_id: str
    scopes: frozenset[str]


class InvoiceService:
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    def _authorize(self, principal: Principal | None, operation: str):
        if (
            not isinstance(principal, Principal)
            or not principal.user_id
            or not principal.tenant_id
            or operation not in principal.scopes
        ):
            raise AccessDenied()

    def read(self, principal: Principal | None, invoice_id: str):
        self._authorize(principal, "invoice:read")
        row = self.connection.execute(
            "SELECT id, description FROM invoices "
            "WHERE id = ? AND tenant_id = ? AND owner_id = ?",
            (invoice_id, principal.tenant_id, principal.user_id),
        ).fetchone()
        if row is None:
            raise AccessDenied()
        return {"id": row[0], "description": row[1]}

    def update(self, principal: Principal | None, invoice_id: str, changes: dict):
        self._authorize(principal, "invoice:update")
        if (
            not isinstance(changes, dict)
            or set(changes) != {"description"}
            or not isinstance(changes["description"], str)
            or len(changes["description"]) > 200
        ):
            raise ValueError("only a bounded description can be updated")
        with self.connection:
            cursor = self.connection.execute(
                "UPDATE invoices SET description = ? "
                "WHERE id = ? AND tenant_id = ? AND owner_id = ?",
                (changes["description"], invoice_id, principal.tenant_id, principal.user_id),
            )
            if cursor.rowcount != 1:
                raise AccessDenied()
