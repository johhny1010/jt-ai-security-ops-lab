# Engineering Roadmap

## Milestone 1 — Public portfolio reproducibility (included)

Synthetic data, transparent architecture and limitations, typed read tools, local optional tool-calling loop, tests and safety scan.

## Milestone 2 — Improved investigation quality

- Evidence freshness and per-source provenance for every model-visible fact.
- Better identity joins across ARP, DHCP, DNS, authenticated host telemetry and switches.
- Structured hypothesis/evidence/counterevidence output for deep investigations.
- Explicit confidence discipline and scenario-based regression suite.

## Milestone 3 — Production-grade authorized change execution

- Dedicated read-only and write-capable service identities.
- Broker-side operator authentication independent of the model and Telegram text.
- Config diff, API operation allowlist, scope limits, impact assessment and lockout-safe rollback.
- One-time, short-lived approvals bound to actor, target, parameters and configuration revision.
- Post-write readback, signed/auditable events and secure secret rotation.
- Real firewall-rule changes only after unit, integration and manual acceptance testing.

## Milestone 4 — Wider infrastructure coverage

Authenticated, minimum-privilege integrations with hypervisor, DNS, storage and managed switch. Avoid broad root credentials and unsupported 'health' claims.

## Milestone 5 — Incident response / security operations

Well-scoped detections backed by specific event evidence, correlation rules, false-positive review, alert deduplication, operator escalation and incident timeline retention. Vulnerability findings only after a verified scanner/source is integrated.

## Success criteria

The agent answers simple questions precisely, investigates complex issues by selecting tools, reports what is uncertain, refuses unauthorized mutations, and proves the outcome of any approved change using independent evidence.
