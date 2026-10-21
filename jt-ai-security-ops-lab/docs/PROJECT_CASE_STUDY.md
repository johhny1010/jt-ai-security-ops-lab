# Engineering Case Study — From Chatbot to Evidence-Grounded SOC Agent

## 1. Problem and motivation

A home lab with multiple Linux hosts, an OPNsense firewall, segmented networks, local inference services and NVIDIA GPUs can produce large amounts of telemetry. A basic conversational assistant could narrate logs, but it frequently confused historical data with current state, overstated security conclusions and answered quick inventory questions with generic threat reports.

**Engineering goal:** A security-operations interface that accepts plain-language questions; decides which vetted diagnostics to perform; correlates actual results; makes appropriately qualified statements; and prepares operator-controlled infrastructure changes.

This public case study reports milestones seen in an earlier private project session. It **does not assert that the private system remains online or that every planned feature has shipped**.

## 2. System decomposition

Five cooperating concerns were separated:

1. **Infrastructure:** OPNsense routing/firewall; logically segmented lab networks; Linux hosts; storage, DNS and virtual machines; local GPU inference services.
2. **Collection:** Scheduled snapshotting; read-only OPNsense endpoints; constrained Linux collector accounts; GPU/Ollama observations; retained history.
3. **Evidence layer:** Timestamped observations; separate inventory from current state; reconciliation of MAC/IP/lease records; explicit stale-data handling.
4. **Reasoning layer:** Local LLM, SOC rules, natural-language dialogue, tool selection, bounded tool iterations, fact-specific response routing.
5. **Change layer:** Independent privileged service, narrowly supported operations, human confirmation, audit events, and readback verification design.

## 3. Implementation history and observed milestones

| Milestone | Evidence from the engineering session | Interpretation |
|---|---|---|
| Scheduled observer | `systemd` oneshot/timer checks returned success | Periodic collection configured at time of test |
| Linux collectors | Three authenticated remote collectors reported `ok` | Linux read telemetry was functioning in the test |
| OPNsense TLS | Certificate issued by a private CA, matching DNS/IP SAN; `curl --cacert` returned 200 | Transport identity successfully verified from the service account |
| OPNsense read coverage | Six distinct read endpoints returned HTTP 200 | Selected interfaces, ARP, traffic, gateway, statistics, lease data available |
| Data counts | Example observed snapshot: 14 interface records, 26–27 ARP records, 12 DHCP lease records | Snapshot-dependent numbers; *not* unique-live-host counts |
| Qwen tool protocol | Ollama native `tool_calls` returned `get_opnsense_gateway_status` with `{}` | Model can request structured read tool calls |
| Telegram policy/data bridge | Bot service active; policy and observer bridge markers installed | Integration deployed; answer accuracy still required testing |
| Admin broker | Independent broker returned readiness probe; staged alias creation and cancellation observed | Readiness/proposal/cancel proven; **write and verification not proven** |
| Agent v4 | User reported agent test worked | User-reported test; complete end-to-end trace not preserved here |

## 4. Critical engineering incident: expired management TLS

An OPNsense management certificate was found to be long-expired and not valid for the IP address used by collectors. The repair sequence was intentionally cautious: create a lab root CA, issue a new server cert with both a DNS SAN and IP SAN, switch the GUI certificate, distribute **only the public CA certificate**, and validate HTTPS without bypassing verification. The collector then reported authenticated API status `ok`.

The lesson is that connecting automation to a firewall requires proper identity validation, not blanket `verify=False` or `curl -k` in production code.

## 5. Critical engineering incident: hallucinated security conclusions

Earlier responses took genuine counters and made unsupported leaps:

- ARP records were called *online devices* without active reachability evidence.
- A recurring MAC address was interpreted as a conflict without checking raw ARP/DHCP associations.
- Blocked traffic was framed as proof of attack or exposure.
- The AI confused the AI inference server with the virtualization host.
- A quick IP/hostname request expanded into unrelated threat reporting.

**Corrections introduced:** deterministic inventory handling for factual queries; source timestamps; separation of verified, inferred and unknown claims; and an allowlisted observer bridge. The public sample replays the same principles with invented data and tests.

## 6. Critical engineering incident: privilege boundaries

The conversational bot ran with `NoNewPrivileges=yes`, which prevented a direct `sudo` backend from elevating. A manually invoked test succeeded, but the Telegram service reported the backend unavailable. Instead of relaxing the systemd protection, the architecture was changed to a separate administrator broker reached through a restricted local communication path.

**What was shown:** readiness and proposal/cancellation behavior. **What remains:** production-grade identity/authentication enforcement at the broker boundary before high-impact writes. A human-readable `/approve` string inside the chatbot must never be the sole privilege control for routing or WAN changes.

## 7. Tool calling versus mere prompt engineering

A large prompt can guide a model, but cannot independently verify that a device exists or prevent a process from executing a bad command. The relevant engineering improvement was to combine:

- **Typed tools:** explicit names, argument schemas, allowlisted read sources.
- **Guardrails in Python:** rejects unknown tools, invalid arguments and requests to unimplemented operations.
- **Evidence provenance:** tools return source/caveats alongside measurements.
- **Bounded loops:** predictable maximum reasoning rounds and response sizes.
- **Administrative isolation:** model instructions do not constitute execution authorization.

This public demo includes these techniques in a limited, reviewable form.

## 8. Demonstrable outcome and limits

A hiring manager can inspect actual code showing structured data reconciliation, multi-tool orchestration, defensive programming, test-driven scenarios and simulated approvals. The public version does **not** require trusted access to a private network, and it is **not advertised as a deployable firewall administrator**.

## 9. What I would improve in a production implementation

Independent authenticated approval identity; read-only vs privileged API identities; immutable audit events; complete before/after rule diff; verified firewall/NAT edit APIs; lockout-aware rollback; comprehensive regression tests; manual end-to-end tests across VLANs; performance and latency budgets; secrets scanning in CI; monitoring of the monitor; and clear incident-response escalation boundaries.

---

*Authored as a sanitized engineering portfolio case study. Sensitive original documentation, credentials, topology and operational data remain private.*
