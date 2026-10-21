"""Offline tests that simulate Ollama tool responses without running a model."""
import io
import json
import unittest
from pathlib import Path
from unittest.mock import patch

from cyberlab_demo.agent import ollama_tool_loop
from cyberlab_demo.evidence import load_fixture
from cyberlab_demo.tools import ToolRegistry

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "synthetic_snapshot.json"


class FakeResponse:
    def __init__(self, data):
        self.stream = io.BytesIO(json.dumps(data).encode())

    def __enter__(self):
        return self.stream

    def __exit__(self, *_):
        self.stream.close()


class AgentLoopTests(unittest.TestCase):
    def setUp(self):
        self.registry = ToolRegistry(load_fixture(FIXTURE))

    @patch("cyberlab_demo.agent.urllib.request.urlopen")
    def test_native_tool_call_then_answer(self, opener):
        opener.side_effect = [
            FakeResponse({"message": {"role": "assistant", "content": "", "tool_calls": [
                {"function": {"name": "get_gateway_status", "arguments": {}}}
            ]}}),
            FakeResponse({"message": {"role": "assistant", "content": "Fixture only; status not live."}}),
        ]
        outcome = ollama_tool_loop("Check gateway", self.registry, "local-test-model")
        self.assertEqual(len(opener.call_args_list), 2)
        self.assertIn("get_gateway_status", outcome["tool_trace"][0])
        self.assertIn("Fixture only", outcome["model_reply"])

    @patch("cyberlab_demo.agent.urllib.request.urlopen")
    def test_unallowlisted_tool_rejected(self, opener):
        opener.side_effect = [
            FakeResponse({"message": {"role": "assistant", "content": "", "tool_calls": [
                {"function": {"name": "delete_firewall_rules", "arguments": {}}}
            ]}}),
            FakeResponse({"message": {"role": "assistant", "content": "No write was made."}}),
        ]
        outcome = ollama_tool_loop("Change firewall", self.registry, "local-test-model")
        self.assertIn("Rejected", outcome["tool_trace"][0])
        self.assertEqual(len(opener.call_args_list), 2)

    def test_invalid_round_limit(self):
        with self.assertRaises(ValueError):
            ollama_tool_loop("Test", self.registry, "local-test-model", max_rounds=99)


if __name__ == "__main__":
    unittest.main()
