# Security Policy and Public Repository Publishing Checklist

## This repository is safe by design

No production telemetry, shell history, firewall backups, hostnames, private endpoint URLs, public WAN IPs, user identity records, API credentials, SSH material, certificates, private keys, bot token, systemd credential files, database snapshots, screenshots or captured packets should be committed.

All included IPs and MACs are fictional. Private example ranges use only `10.250.0.0/16`, WAN examples are RFC 5737 documentation addresses, and MAC addresses are locally administered placeholders (`02:00:...`).

## Before publishing actual private lab content

1. **Never upload whole `/opt/ai-security`, `/etc`, `.ssh`, OPNsense XML backups, container volumes, or the original internal project report.**
2. Export **only hand-reviewed, new sanitized examples**; do not copy credentials and assume `.gitignore` will protect them.
3. Replace all real hostnames, networks, gateways, MAC addresses, interface IDs, account names, cloud IDs, logs and user identifiers with synthetic identifiers. Remove metadata and screenshots with browser URLs or topology.
4. Strip even public CA certificates: internal PKI subjects and fingerprints can reveal private infrastructure details.
5. Review `git diff --cached` and `git ls-files`; run `python scripts/check_public_safety.py` and an independent secret scanner such as GitHub secret scanning or `gitleaks` before every push.
6. Make the first repository private and inspect it in GitHub's web UI before switching visibility to public. Check the entire commit history, not just the latest files.
7. Use a dedicated GitHub authentication method; never embed PATs or passwords in remote URLs or shell command history.
8. If a secret was ever committed, **rotate it** and rewrite history as needed; deleting the file in a later commit does not undo exposure.

## Threat model

| Trust boundary | Threat | Control |
|---|---|---|
| User message → model | Prompt injection or ambiguous instructions | Model output cannot authorize writes |
| Logs/DHCP labels → model | Malicious text masquerading as instructions | Treat all telemetry as untrusted data |
| Model → read tools | Tool names/parameters invented by model | Allowlist, parameter schema, loop limit |
| Model/chat → privileged broker | Unapproved network changes | Separate authenticated policy enforcement, independent human approval |
| Collector → network devices | Credential disclosure or TLS interception | Least privilege, verified CA, protected secrets |
| Repository → public | Accidental network/secret exposure | Synthetic fixtures, safety scan, history review |

**Important:** `admin_sim.py` is an **in-memory education simulation**. Its simple `actor` string is not authenticated identity, and it must not be adapted to production as-is.

## Reporting security concerns

Do not open a public GitHub issue containing passwords, internal addresses, exploit details or production logs. Contact the repository owner privately through an appropriate secure channel.
