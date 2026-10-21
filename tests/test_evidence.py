import unittest
import tempfile
from pathlib import Path

from cyberlab_demo.evidence import EvidenceError, inventory, load_fixture, summary

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "synthetic_snapshot.json"


class EvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = load_fixture(FIXTURE)

    def test_fixture_marked_synthetic(self):
        self.assertEqual(self.data["metadata"]["classification"], "SYNTHETIC_DEMONSTRATION_DATA")

    def test_counts_based_on_records(self):
        result = inventory(self.data)
        self.assertEqual(result["arp_records"], 9)
        self.assertEqual(result["dhcp_lease_records"], 5)
        self.assertEqual(result["distinct_observed_ips"], 10)

    def test_gateway_excluded_from_clients(self):
        result = inventory(self.data)
        self.assertEqual(result["observed_client_ips"], 8)
        self.assertEqual(len([h for h in result["hosts"] if h["classification"] == "gateway"]), 2)

    def test_lease_is_not_online_proof(self):
        result = inventory(self.data)
        self.assertIsNone(result["verified_online_hosts"])
        self.assertTrue(all(h["reachability"] == "NOT_TESTED" for h in result["hosts"]))

    def test_mac_difference_requires_corrob(self):
        result = inventory(self.data)
        host = next(h for h in result["hosts"] if h["ip"] == "10.250.10.30")
        self.assertTrue(host["needs_mac_reconciliation"])
        self.assertNotIn("rogue", str(host).lower())

    def test_repeated_mac_not_automatically_conflict(self):
        result = inventory(self.data)
        host = next(h for h in result["hosts"] if h["ip"] == "10.250.10.31")
        self.assertFalse(host["needs_mac_reconciliation"])

    def test_rejects_non_synthetic_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "untrusted.json"
            path.write_text('{"metadata": {"classification": "LIVE"}}')
            with self.assertRaises(EvidenceError):
                load_fixture(path)

    def test_summary_is_explicitly_synthetic(self):
        value = summary(self.data)
        self.assertIn("SYNTHETIC", value["data_classification"])
        self.assertEqual(value["interface_records"], 4)


if __name__ == "__main__":
    unittest.main()
