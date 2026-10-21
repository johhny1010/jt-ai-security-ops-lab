import unittest
from cyberlab_demo.admin_sim import ApprovalSimulator


class ApprovalTests(unittest.TestCase):
    def setUp(self):
        self.clock = [1000.0]
        self.sim = ApprovalSimulator(now=lambda: self.clock[0])

    def test_staging_does_not_mutate(self):
        self.sim.propose_host_alias("DEMO_ENDPOINT", "10.250.10.25")
        self.assertEqual(self.sim.aliases, {})

    def test_explicit_approval_and_readback(self):
        pending = self.sim.propose_host_alias("DEMO_ENDPOINT", "10.250.10.25")
        result = self.sim.approve("authorized-demo-operator", pending.approval_code)
        self.assertEqual(result["readback_verified"], "true")
        self.assertEqual(self.sim.aliases["DEMO_ENDPOINT"], "10.250.10.25")

    def test_replay_denied(self):
        pending = self.sim.propose_host_alias("DEMO_ENDPOINT", "10.250.10.25")
        self.sim.approve("authorized-demo-operator", pending.approval_code)
        with self.assertRaises(PermissionError):
            self.sim.approve("authorized-demo-operator", pending.approval_code)

    def test_other_actor_denied(self):
        pending = self.sim.propose_host_alias("DEMO_ENDPOINT", "10.250.10.25")
        with self.assertRaises(PermissionError):
            self.sim.approve("unknown-actor", pending.approval_code)
        self.assertEqual(self.sim.aliases, {})

    def test_expiration_denied(self):
        pending = self.sim.propose_host_alias("DEMO_ENDPOINT", "10.250.10.25", ttl_seconds=2)
        self.clock[0] += 3
        with self.assertRaises(PermissionError):
            self.sim.approve("authorized-demo-operator", pending.approval_code)
        self.assertEqual(self.sim.aliases, {})

    def test_cancel_denies_approval(self):
        pending = self.sim.propose_host_alias("DEMO_ENDPOINT", "10.250.10.25")
        self.sim.cancel()
        with self.assertRaises(PermissionError):
            self.sim.approve("authorized-demo-operator", pending.approval_code)

    def test_reject_outside_demo_range(self):
        with self.assertRaises(ValueError):
            self.sim.propose_host_alias("DEMO_BAD", "203.0.113.55")


if __name__ == "__main__":
    unittest.main()
