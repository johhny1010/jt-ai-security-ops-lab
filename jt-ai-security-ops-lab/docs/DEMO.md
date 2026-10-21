# Demo Walkthrough

## Prerequisites

Python 3.10+; no external packages required for the default demo. A model is optional.

Run from the repository root:

```bash
export PYTHONPATH=src
python -m cyberlab_demo inventory
python -m cyberlab_demo summary
python -m cyberlab_demo investigate --question "Investigate gateway availability"
python -m cyberlab_demo approval-demo
python -m unittest discover -s tests -v
python scripts/check_public_safety.py
```

For Windows PowerShell:

```powershell
$env:PYTHONPATH="src"
python -m cyberlab_demo inventory
python -m cyberlab_demo investigate
```

## What to observe

**Inventory:** The tool combines ARP and DHCP records but excludes gateway IPs from the *observed client IP* count. It never calls an address 'online' without a live reachability test. One synthetic ARP/DHCP MAC discrepancy is reported as needing reconciliation, not proof of intrusion.

**Network summary:** Uses record counts and explicitly states that blocked-packet counters are not verified attacks or CVEs.

**Offline investigation:** Several allowlisted read tools are executed in sequence, with structured results and explicit limitations. This is deterministic and does not involve Qwen.

**Approval demo:** An operator-requested host alias is **staged only**. The program does not contact a firewall and intentionally does not approve or apply the change. Unit tests exercise expiry, cancellation, replay rejection and operator mismatch.

## Optional local Qwen / Ollama tool selection

If you've already installed Ollama locally and pulled a model supporting tool calls:

```bash
PYTHONPATH=src python -m cyberlab_demo investigate --ollama \
 --model YOUR_LOCAL_MODEL \
 --question "Consult the relevant evidence tools, then explain gateway health limitations."
```

The tool loop uses `POST http://127.0.0.1:11434/api/chat` by default, enforces a read-tool allowlist and rejects non-loopback endpoints. The model receives synthetic data, not real network telemetry. Model answers may still require critical evaluation; the demonstration does not claim hallucination elimination.

## Interview demonstration script (3–5 minutes)

1. Explain the five architectural layers and why the LLM has no privileged credentials.
2. Run `inventory` and show the separation of observed IP addresses and verified-online hosts.
3. Run `investigate` to show multi-tool evidence gathering.
4. Run `approval-demo` and point to approval state, expiration and cancellation tests.
5. Show CI plus the public-safety scan and discuss what was verified in the private deployment versus planned.

## Explicit non-goals

No vulnerability scanner; no CVE assertions; no real-world packet capture; no firewall write capability; no secrets; no public exposure of internal infrastructure. This is an architectural and engineering demonstration, not a replacement for audited operational tools.
