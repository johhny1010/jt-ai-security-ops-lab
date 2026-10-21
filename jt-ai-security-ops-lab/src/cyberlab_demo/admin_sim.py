"""In-memory change-approval demo. NO privileged API, NO persistent writes.

NOT a production authorization system. Used solely to illustrate the lifecycle.
"""

from __future__ import annotations

import hmac
import ipaddress
import re
import secrets
import time
from dataclasses import dataclass


@dataclass
class PendingChange:
    operation: str
    name: str
    address: str
    approval_code: str
    approver: str
    expires_at: float


class ApprovalSimulator:
    def __init__(self, approver: str = "authorized-demo-operator", now: callable = time.time):
        self.approver = approver
        self.now = now
        self.pending: PendingChange | None = None
        self.aliases: dict[str, str] = {}
        self.audit: list[dict[str, str]] = []

    def propose_host_alias(self, name: str, address: str, ttl_seconds: int = 600) -> PendingChange:
        if not re.fullmatch(r"DEMO_[A-Z0-9_]{1,40}", name):
            raise ValueError("Demo alias must start with DEMO_ and use uppercase characters")
        parsed = ipaddress.ip_address(address)
        if parsed not in ipaddress.ip_network("10.250.0.0/16"):
            raise ValueError("Public demo only accepts fictional 10.250.0.0/16 addresses")
        if ttl_seconds < 1 or ttl_seconds > 600:
            raise ValueError("Approval lifetime out of bounds")
        if name in self.aliases:
            raise ValueError("Alias already exists")
        self.pending = PendingChange(
            "create_demo_alias", name, str(parsed),
            secrets.token_hex(6).upper(), self.approver, self.now() + ttl_seconds
        )
        self.audit.append({"event": "proposed", "operation": "create_demo_alias", "name": name})
        return self.pending

    def cancel(self) -> None:
        if self.pending:
            self.audit.append({"event": "cancelled", "name": self.pending.name})
        self.pending = None

    def approve(self, actor: str, code: str) -> dict[str, str]:
        pending = self.pending
        if pending is None:
            raise PermissionError("No pending change")
        if self.now() > pending.expires_at:
            self.pending = None
            self.audit.append({"event": "expired", "name": pending.name})
            raise PermissionError("Approval expired")
        if actor != pending.approver or not hmac.compare_digest(code, pending.approval_code):
            self.audit.append({"event": "denied", "name": pending.name})
            raise PermissionError("Invalid approval")
        # Consume the approval before attempting the simulated write.
        self.pending = None
        self.aliases[pending.name] = pending.address
        verified = self.aliases.get(pending.name) == pending.address
        self.audit.append({"event": "verified" if verified else "verification_failed", "name": pending.name})
        return {
            "simulation_only": "true",
            "operation": pending.operation,
            "alias": pending.name,
            "address": pending.address,
            "readback_verified": str(verified).lower(),
        }
