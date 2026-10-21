"""Source-aware inventory analysis that never equates observation with presence.

All data in this public project is synthetic. Production collectors are NOT included.
"""

from __future__ import annotations

import ipaddress
import json
from pathlib import Path
from typing import Any


class EvidenceError(ValueError):
    """Invalid or untrusted fixture."""


def load_fixture(path: str | Path) -> dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("metadata", {}).get("classification") != "SYNTHETIC_DEMONSTRATION_DATA":
        raise EvidenceError("Refusing non-synthetic input in public demonstration")
    return data


def _sort_ip(address: str) -> tuple[int, int]:
    parsed = ipaddress.ip_address(address)
    return parsed.version, int(parsed)


def inventory(data: dict[str, Any]) -> dict[str, Any]:
    """Reconcile observed IPs from ARP/DHCP without inventing device identity.

    Returns distinct addresses, not a count of devices that are online.
    Network gateway interfaces and WAN addresses are tagged, not counted as clients.
    MAC discrepancies are flagged for investigation, not called attacks/conflicts.
    """
    opn = data["opnsense"]
    gateways = set(data["topology"]["gateways"])
    hosts: dict[str, dict[str, Any]] = {}
    for source_name, records in (("arp", opn["arp"]), ("dhcp", opn["dhcp"])):
        for record in records:
            address = str(ipaddress.ip_address(record["ip"]))
            host = hosts.setdefault(address, {
                "ip": address, "hostname": None, "mac_by_source": {},
                "seen_in": [], "classification": "gateway" if address in gateways else "observed_client_ip"
            })
            if source_name not in host["seen_in"]:
                host["seen_in"].append(source_name)
            name = str(record.get("hostname") or "").strip()
            if name and not host["hostname"]:
                host["hostname"] = name
            mac = str(record.get("mac") or "").lower().strip()
            if mac:
                host["mac_by_source"][source_name] = mac
    result = []
    for address in sorted(hosts, key=_sort_ip):
        host = hosts[address]
        host["needs_mac_reconciliation"] = len(set(host["mac_by_source"].values())) > 1
        host["reachability"] = "NOT_TESTED"
        result.append(host)
    return {
        "data_classification": "SYNTHETIC_DEMONSTRATION_DATA",
        "source_timestamp_utc": data["metadata"]["collected_at_utc"],
        "arp_records": len(opn["arp"]),
        "dhcp_lease_records": len(opn["dhcp"]),
        "distinct_observed_ips": len(result),
        "observed_client_ips": sum(h["classification"] == "observed_client_ip" for h in result),
        "verified_online_hosts": None,
        "online_status_note": "No live probe was performed: ARP/DHCP are observations, not liveness tests.",
        "hosts": result,
    }


def summary(data: dict[str, Any]) -> dict[str, Any]:
    observed = inventory(data)
    return {
        "data_classification": "SYNTHETIC_DEMONSTRATION_DATA",
        "source_timestamp_utc": data["metadata"]["collected_at_utc"],
        "interface_records": len(data["opnsense"]["interfaces"]),
        "arp_records": observed["arp_records"],
        "dhcp_lease_records": observed["dhcp_lease_records"],
        "observed_client_ips": observed["observed_client_ips"],
        "gateway_records": len(data["opnsense"]["gateways"]),
        "firewall_statistics": data["opnsense"]["firewall_statistics"],
        "caveat": "Fixture counters are not proof of vulnerability, live presence, or active attack."
    }
