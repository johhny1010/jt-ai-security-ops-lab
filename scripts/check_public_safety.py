#!/usr/bin/env python3
"""Conservative repo hygiene scan. Complements, does not replace, secret scanning.

Run before publishing; treats unknown addresses/secret-like values as errors.
"""
from __future__ import annotations
import ipaddress
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = (ipaddress.ip_network("10.250.0.0/16"),
           ipaddress.ip_network("198.51.100.0/24"),
           ipaddress.ip_network("203.0.113.0/24"),
           ipaddress.ip_network("192.0.2.0/24"),
           ipaddress.ip_network("127.0.0.0/8"))
IPV4 = re.compile(r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])")
SENSITIVE_NAMES = re.compile(
    r"^(?:id_(?:rsa|ed25519)|config\.xml|telegram\.env|secrets\.env|latest\.json|"
    r"topology\.json|known_hosts)$", re.I)
SECRETS = re.compile(
    r"(?im)^\s*(?:OPNSENSE_KEY|OPNSENSE_SECRET|TELEGRAM_BOT_TOKEN|"
    r"AWS_SECRET_ACCESS_KEY|GITHUB_TOKEN|GH_TOKEN)\s*[:=]\s*['\"]?[^\s#'\"]{8,}"
)
HIGH_CONFIDENCE = re.compile(
    r"\b(?:ghp_|github_pat_|sk_live_)[A-Za-z0-9_\-]{18,}\b"
)
BLOCKED_SUFFIXES = {".p12", ".pfx", ".pem", ".key", ".crt", ".pcap", ".pcapng", ".docx", ".db", ".sqlite"}
TEXT_SUFFIXES = {".md", ".py", ".json", ".yml", ".yaml", ".toml", ".txt", ".service", ".example", ".gitignore", ".env"}


def main() -> int:
    issues = []
    examined = 0
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        if any(part in {".git", "__pycache__", ".pytest_cache", ".venv", "dist", "build"} for part in path.parts):
            continue
        rel = path.relative_to(ROOT)
        if SENSITIVE_NAMES.match(path.name) or path.suffix.lower() in BLOCKED_SUFFIXES:
            issues.append(f"{rel}: blocked filename/filetype")
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in {"README.md", "LICENSE", ".gitignore", ".env.example"}:
            issues.append(f"{rel}: unreviewed file type (fail closed)")
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except (UnicodeError, OSError):
            issues.append(f"{rel}: unreadable/binary content")
            continue
        examined += 1
        if SECRETS.search(content) or HIGH_CONFIDENCE.search(content):
            issues.append(f"{rel}: credential-looking assignment or token")
        for match in IPV4.finditer(content):
            try:
                ip = ipaddress.ip_address(match.group())
            except ValueError:
                continue
            if not any(ip in network for network in ALLOWED):
                issues.append(f"{rel}: non-documentation/non-synthetic address {ip}")
    if issues:
        print("PUBLIC SAFETY SCAN FAILED")
        for issue in sorted(set(issues)):
            print(" -", issue)
        print("Do not push until each issue is investigated and removed.")
        return 1
    print(f"PUBLIC SAFETY SCAN PASS: {examined} reviewed text files; synthetic/demo IP allowlist only")
    print("Reminder: regex scans cannot guarantee secrets or identifying data are absent. Review all files and git history manually.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
