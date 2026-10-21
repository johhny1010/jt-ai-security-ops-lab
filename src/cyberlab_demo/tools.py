"""Allowlisted, read-only tools operating exclusively on a synthetic fixture."""

from __future__ import annotations

import ipaddress
from typing import Any, Callable
from .evidence import inventory, summary

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": name,
            "description": description + " Uses SYNTHETIC public fixture data only.",
            "parameters": parameters,
        },
    }
    for name, description, parameters in [
        ("get_network_summary", "Get source-scoped network overview and caveats", {"type": "object", "properties": {}, "additionalProperties": False}),
        ("get_device_inventory", "Reconcile observed ARP and DHCP IPs; not liveness", {"type": "object", "properties": {}, "additionalProperties": False}),
        ("get_gateway_status", "Inspect fictional gateway status and sample metrics", {"type": "object", "properties": {}, "additionalProperties": False}),
        ("get_interface_status", "Inspect fictional interface state and VLAN labels", {"type": "object", "properties": {}, "additionalProperties": False}),
        ("get_firewall_statistics", "Inspect synthetic aggregate counters, not raw logs", {"type": "object", "properties": {}, "additionalProperties": False}),
        ("get_linux_health", "Inspect fictional Linux host measurements", {"type": "object", "properties": {}, "additionalProperties": False}),
        ("lookup_ip", "Look up one observed IP; never infer online status", {
            "type": "object", "properties": {"ip": {"type": "string"}},
            "required": ["ip"], "additionalProperties": False
        }),
    ]
]


class ToolRegistry:
    def __init__(self, snapshot: dict[str, Any]):
        if snapshot.get("metadata", {}).get("classification") != "SYNTHETIC_DEMONSTRATION_DATA":
            raise ValueError("Public demo tools accept synthetic fixture data only")
        self.snapshot = snapshot
        self._handlers: dict[str, Callable[[dict[str, Any]], Any]] = {
            "get_network_summary": lambda _: summary(self.snapshot),
            "get_device_inventory": lambda _: inventory(self.snapshot),
            "get_gateway_status": lambda _: {"source": "synthetic", "items": self.snapshot["opnsense"]["gateways"]},
            "get_interface_status": lambda _: {"source": "synthetic", "items": self.snapshot["opnsense"]["interfaces"]},
            "get_firewall_statistics": lambda _: {"source": "synthetic", "statistics": self.snapshot["opnsense"]["firewall_statistics"]},
            "get_linux_health": lambda _: {"source": "synthetic", "items": self.snapshot["remote_linux"]},
            "lookup_ip": self._lookup_ip,
        }

    def names(self) -> set[str]:
        return set(self._handlers)

    def call(self, name: str, arguments: dict[str, Any] | None = None) -> Any:
        if name not in self._handlers:
            raise ValueError(f"Tool not allowlisted: {name}")
        if not isinstance(arguments, dict):
            raise ValueError("Tool arguments must be a JSON object")
        schema = next(t["function"]["parameters"] for t in TOOL_SCHEMAS if t["function"]["name"] == name)
        allowed = set(schema["properties"])
        required = set(schema.get("required", []))
        if set(arguments) - allowed or required - set(arguments):
            raise ValueError("Tool argument schema mismatch")
        if not all(isinstance(v, str) for v in arguments.values()):
            raise ValueError("Unsupported argument type")
        return self._handlers[name](arguments)

    def _lookup_ip(self, arguments: dict[str, Any]) -> dict[str, Any]:
        address = str(ipaddress.ip_address(arguments["ip"]))
        entry = next((h for h in inventory(self.snapshot)["hosts"] if h["ip"] == address), None)
        return {
            "source": "synthetic",
            "ip": address,
            "record": entry,
            "verified_online": None,
            "note": "No active network probe has been made"
        }
