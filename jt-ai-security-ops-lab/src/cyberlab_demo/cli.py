"""Command-line entry point for a safe, fictional lab demonstration."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from .admin_sim import ApprovalSimulator
from .agent import offline_investigation, ollama_tool_loop
from .evidence import inventory, load_fixture, summary
from .tools import ToolRegistry

DEFAULT_FIXTURE = Path(__file__).resolve().parents[2] / "fixtures" / "synthetic_snapshot.json"


def main() -> None:
    parser = argparse.ArgumentParser(description="Synthetic JT Cyber & AI Lab portfolio demonstration")
    parser.add_argument("mode", choices=["inventory", "summary", "investigate", "approval-demo"])
    parser.add_argument("--fixture", default=str(DEFAULT_FIXTURE))
    parser.add_argument("--question", default="Investigate gateway health and any visible connectivity concerns.")
    parser.add_argument("--ollama", action="store_true", help="Optional local Ollama model using synthetic tools only")
    parser.add_argument("--model", default="qwen3:8b", help="Model installed locally; set as needed")
    parser.add_argument("--base-url", default="http://127.0.0.1:11434")
    args = parser.parse_args()

    data = load_fixture(args.fixture)
    registry = ToolRegistry(data)
    if args.mode == "inventory":
        outcome = inventory(data)
    elif args.mode == "summary":
        outcome = summary(data)
    elif args.mode == "investigate":
        outcome = (ollama_tool_loop(args.question, registry, args.model, args.base_url)
                   if args.ollama else offline_investigation(args.question, registry))
    else:
        sim = ApprovalSimulator()
        proposal = sim.propose_host_alias("DEMO_WEB_NODE", "10.250.10.222")
        outcome = {
            "status": "STAGED_NOT_EXECUTED",
            "simulation_only": True,
            "proposal": {"alias": proposal.name, "address": proposal.address, "expires_at": proposal.expires_at},
            "note": "The demo deliberately stops before approval. No firewall/API write is possible.",
            "audit": sim.audit,
        }
    print(json.dumps(outcome, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
