# How to Present This Project to Employers

## Professional project summary (portfolio / resume)

**AI Security Operations & Network Automation — Independent Engineering Project**

Designed and iteratively developed a self-hosted AI security-operations lab using Python, local Ollama/Qwen inference, OPNsense REST APIs, Linux monitoring, scheduled telemetry and a Telegram interface. Validated six firewall read-data sources, CA-verified API communication and native structured LLM tool requests; implemented evidence-aware inventory handling, an isolated administrative broker design and approval-controlled change staging. Produced a sanitized, testable open-source demonstration emphasizing safe automation, source integrity and security boundaries.

## Interview talking points

**Problem:** A local AI chatbot can narrate arbitrary logs and confidently report false conclusions unless backed by explicit evidence and constrained tools.

**Approach:** Separated infrastructure collection, evidence validation, conversational planning and privileged change execution. Used deterministic calculations where exact answers are needed and the LLM where interpretation is appropriate.

**Representative debug story:** A management API was initially unavailable due to an expired and hostname-mismatched certificate. Replaced it through private PKI and verified it using the CA rather than bypassing TLS validation.

**Representative automation story:** A direct `sudo` approach failed inside a systemd-hardened Telegram service (`NoNewPrivileges=yes`). Preserved the restriction and moved privileged operations to a separate broker.

**Maturity statement:** Several read-only integrations and command-stage flows were tested; broad autonomous administrator writes were a planned next phase, not falsely claimed as completed.

## Skills a reviewer can see in the repository

- Python standard-library API and JSON processing
- Allowlisted LLM tool invocation and bounded multi-step loops
- Security automation and operator-approved change-control modeling
- Source provenance, measured facts versus inference, and input validation
- Network concepts: segmented topologies, ARP, DHCP, gateways and packet-filter telemetry
- systemd service hardening and operational troubleshooting
- Unit testing, GitHub Actions and safe publication discipline

## What not to claim

- “PhD-level AI that never hallucinates.”
- “Autonomous firewall changes verified in production” without completed evidence.
- “29 online hosts” from ARP/DHCP alone.
- “All vulnerabilities eliminated” when no scanner has established findings.
- “Production-ready policy engine” based on a simulator.

Honest engineering tradeoffs are a stronger interview signal than exaggerated features.
