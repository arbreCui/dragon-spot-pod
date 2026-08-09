from __future__ import annotations

import unittest
from pathlib import Path

from check_phase_a9b_b2w_returned_close import (
    ContractError,
    HERE,
    DEFAULT_HARNESS,
    DEFAULT_POSTERIOR,
    DEFAULT_RUNNER,
    DEFAULT_SOURCE,
    check_contract,
)


class B2WContractMutations(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = DEFAULT_SOURCE.read_text()
        cls.harness = DEFAULT_HARNESS.read_text()
        cls.posterior = DEFAULT_POSTERIOR.read_text()
        cls.runner = DEFAULT_RUNNER.read_text()

    def check(self, source=None, harness=None, posterior=None, runner=None):
        check_contract(
            self.source if source is None else source,
            self.harness if harness is None else harness,
            self.posterior if posterior is None else posterior,
            self.runner if runner is None else runner,
        )

    def rejects(self, **kwargs):
        with self.assertRaises(ContractError):
            self.check(**kwargs)

    def test_baseline(self):
        self.check()

    def test_public_abi_mutation(self):
        self.rejects(source=self.source.replace("SPOR64_B2W_CLOSE(ipaxout,", "SPOR64_B2W_CLOSE(ipbad,"))

    def test_status_mutation(self):
        self.rejects(source=self.source.replace("SPOR64_B2W_CLOSED = 2", "SPOR64_B2W_CLOSED = 3"))

    def test_reciprocal_mutation(self):
        self.rejects(source=self.source.replace("1.0_real64/real(keff32,real64)", "rho64", 1))

    def test_feedback_inventory_mutation(self):
        self.rejects(source=self.source.replace("names(9)", "names(8)", 1))

    def test_child_inventory_mutation(self):
        self.rejects(source=self.source.replace("names(16)", "names(15)", 1))

    def test_plane_forbidden_mutation(self):
        self.rejects(source=self.source.replace("ABSENT_RECORD(authority,'PLANE')", "ABSENT_RECORD(authority,'OTHER')"))

    def test_leakage_promotion_mutation(self):
        self.rejects(source=self.source.replace("real(child_leakage32(ig,ip),real64)", "axial_leakage64(ig)"))

    def test_l1_propagation_mutation(self):
        needle = "call LCMPUT(iparchiveout,'SPOT-ITER-K',1,4,iter_keff64)"
        replacement = needle + "\n    call LCMPUT(iparchiveout,'SPOT-L1-ERR',1,2,l1_error32)"
        self.rejects(source=self.source.replace(needle, replacement))

    def test_l1_identity_mutation(self):
        self.rejects(source=self.source.replace(
            "maxval(abs(child_leakage32-system_leakage32))",
            "maxval(abs(child_leakage32))",
        ))

    def test_system_validator_mutation(self):
        self.rejects(source=self.source.replace(
            "RETURNED_SYSTEM_IS_VALID(input_system(ip),ip,",
            "RETURNED_CHILD_IS_VALID(input_system(ip),",
        ))

    def test_system_schema_mutation(self):
        self.rejects(source=self.source.replace(
            "logical function RETURNED_SYSTEM_ROOT_IS_EXACT",
            "logical function RETURNED_SYSTEM_ROOT_IS_LOOSE",
        ))

    def test_missing_negative_marker(self):
        self.rejects(harness=self.harness.replace("BAD-Q-MIRROR", "BAD-Q-OTHER"))

    def test_posterior_b2w_dependency(self):
        self.rejects(posterior=self.posterior.replace("use GANLIB", "use GANLIB\n  use SPOR64_B2W"))

    def test_posterior_spoleak_call(self):
        self.rejects(posterior=self.posterior.replace("implicit none", "implicit none\n  call SPOLEAK"))

    def test_runner_strictness_mutation(self):
        self.rejects(runner=self.runner.replace("-Werror", "-Wno-error"))

    def test_runner_cleanup_mutation(self):
        self.rejects(runner=self.runner.replace("rm -rf", "keep"))


if __name__ == "__main__":
    unittest.main()
