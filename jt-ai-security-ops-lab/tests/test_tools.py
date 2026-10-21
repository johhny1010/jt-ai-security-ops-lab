import unittest
from pathlib import Path
from cyberlab_demo.evidence import load_fixture
from cyberlab_demo.tools import ToolRegistry
from cyberlab_demo.agent import _validated_local_ollama_url, offline_investigation

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "synthetic_snapshot.json"


class ToolTests(unittest.TestCase):
    def setUp(self):
        self.registry = ToolRegistry(load_fixture(FIXTURE))

    def test_gateway_read(self):
        self.assertEqual(len(self.registry.call("get_gateway_status", {})["items"]), 2)

    def test_rejects_unknown_tool(self):
        with self.assertRaises(ValueError):
            self.registry.call("run_shell", {"command": "id"})

    def test_rejects_unsupported_parameters(self):
        with self.assertRaises(ValueError):
            self.registry.call("get_gateway_status", {"execute": True})

    def test_lookup_ip(self):
        result = self.registry.call("lookup_ip", {"ip": "10.250.10.25"})
        self.assertEqual(result["record"]["hostname"], "ai-node")
        self.assertIsNone(result["verified_online"])

    def test_no_unknown_ip_invention(self):
        result = self.registry.call("lookup_ip", {"ip": "10.250.10.200"})
        self.assertIsNone(result["record"])

    def test_offline_multiple_tools(self):
        result = offline_investigation("Investigate gateway", self.registry)
        self.assertGreaterEqual(len(result["tool_trace"]), 3)
        self.assertIn("SYNTHETIC", result["source"])

    def test_ollama_local_only(self):
        self.assertEqual(_validated_local_ollama_url("http://127.0.0.1:11434"),
                         "http://127.0.0.1:11434/api/chat")
        for bad in ("https://example.com", "http://198.51.100.10:11434",
                    "http://localhost:11434/api/admin", "file:///tmp/api"):
            with self.subTest(url=bad):
                with self.assertRaises(ValueError):
                    _validated_local_ollama_url(bad)


if __name__ == "__main__":
    unittest.main()
