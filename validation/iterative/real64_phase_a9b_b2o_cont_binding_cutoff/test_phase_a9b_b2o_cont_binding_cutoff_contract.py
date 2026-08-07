from __future__ import annotations

import unittest

from check_phase_a9b_b2o_cont_binding_cutoff import (
    A8_PATH,
    A9_PATH,
    B2B_PATH,
    B2O_PATH,
    FLU_PATH,
    check_contract,
)


class B2OContractMutationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.b2b = B2B_PATH.read_text(encoding="utf-8")
        cls.flu = FLU_PATH.read_text(encoding="utf-8")
        cls.a8 = A8_PATH.read_text(encoding="utf-8")
        cls.a9 = A9_PATH.read_text(encoding="utf-8")
        cls.b2o = B2O_PATH.read_text(encoding="utf-8")
        check_contract(cls.b2b, cls.flu, cls.a8, cls.a9, cls.b2o)

    def rejected(
        self,
        *,
        b2b: str | None = None,
        flu: str | None = None,
        a8: str | None = None,
        a9: str | None = None,
        b2o: str | None = None,
    ) -> None:
        with self.assertRaises(AssertionError):
            check_contract(
                self.b2b if b2b is None else b2b,
                self.flu if flu is None else flu,
                self.a8 if a8 is None else a8,
                self.a9 if a9 is None else a9,
                self.b2o if b2o is None else b2o,
            )

    @staticmethod
    def changed(text: str, old: str, new: str, count: int = 1) -> str:
        if text.count(old) < count:
            raise AssertionError(f"mutation anchor missing: {old!r}")
        return text.replace(old, new, count)

    def test_01_remove_joint_admission(self) -> None:
        text = self.changed(
            self.b2b,
            "if (.not. CONT_LIFECYCLE_IS_BOUND(ipseed,ipsou,ipsys, &\n"
            "          seed_leak1d32,leak1d_input32)) return",
            "continue",
        )
        self.rejected(b2b=text)

    def test_02_seed_state_mutation(self) -> None:
        self.rejected(b2b=self.changed(self.b2b, "'PROJECTED')) return", "'SOLVED')) return"))

    def test_03_source_state_mutation(self) -> None:
        self.rejected(b2b=self.changed(self.b2b, "'FROZEN-QFIS')) return", "'PROJECTED')) return"))

    def test_04_system_state_mutation(self) -> None:
        self.rejected(b2b=self.changed(self.b2b, "'ASSEMBLED')) return", "'PROJECTED')) return"))

    def test_05_epoch_mutation(self) -> None:
        self.rejected(b2b=self.changed(self.b2b, "CONT_EPOCH = 1", "CONT_EPOCH = 2"))

    def test_06_remove_source_rho_bits(self) -> None:
        old = "transfer(source_rho64,0_int64)) return"
        self.rejected(b2b=self.changed(self.b2b, old, "transfer(seed_rho64,0_int64)) return"))

    def test_07_remove_system_rho_bits(self) -> None:
        old = "transfer(system_rho64,0_int64)) return"
        self.rejected(b2b=self.changed(self.b2b, old, "transfer(seed_rho64,0_int64)) return"))

    def test_08_remove_plane_range(self) -> None:
        old = "if (source_plane < 1 .or. source_plane > NPLANE) return"
        self.rejected(b2b=self.changed(self.b2b, old, "continue"))

    def test_09_remove_plane_equality(self) -> None:
        old = "if (system_plane /= source_plane) return"
        self.rejected(b2b=self.changed(self.b2b, old, "continue"))

    def test_10_remove_leakage_bits(self) -> None:
        old = "if (.not. SAME_REAL32_BITS(seed_leakage,system_leakage)) return"
        self.rejected(b2b=self.changed(self.b2b, old, "continue"))

    def test_11_weaken_source_inventory(self) -> None:
        self.rejected(b2b=self.changed(self.b2b, "'QFISS       '", "'EXTRA       '"))

    def test_12_add_b2b_write(self) -> None:
        anchor = "CONT_LIFECYCLE_IS_BOUND = .false."
        text = self.changed(
            self.b2b,
            anchor,
            anchor + "\n    call LCMPUT(ipseed,'BAD',1,1,1)",
        )
        self.rejected(b2b=text)

    def test_13_remove_flu_observer(self) -> None:
        self.rejected(flu=self.changed(
            self.flu,
            "        WRITE(IOUT,5990) IR64MD,IB2STAT,CUTOFF64\n",
            "",
        ))

    def test_14_move_observer_inside_success(self) -> None:
        old = (
            "        WRITE(IOUT,5990) IR64MD,IB2STAT,CUTOFF64\n"
            "        IF(IB2STAT.EQ.SPOR64_B2C_HOST_COMMITTED) THEN"
        )
        new = (
            "        IF(IB2STAT.EQ.SPOR64_B2C_HOST_COMMITTED) THEN\n"
            "          WRITE(IOUT,5990) IR64MD,IB2STAT,CUTOFF64"
        )
        self.rejected(flu=self.changed(self.flu, old, new))

    def test_15_narrow_flu_counter(self) -> None:
        self.rejected(flu=self.changed(
            self.flu,
            "      INTEGER(INT64) CUTOFF64",
            "      INTEGER CUTOFF64",
        ))

    def test_16_make_counter_decide_output(self) -> None:
        old = "        WRITE(IOUT,5990) IR64MD,IB2STAT,CUTOFF64"
        new = "        IF(CUTOFF64.GT.0) WRITE(IOUT,5990) IR64MD,IB2STAT,CUTOFF64"
        self.rejected(flu=self.changed(self.flu, old, new))

    def test_17_write_counter_to_lcm(self) -> None:
        anchor = "        WRITE(IOUT,5990) IR64MD,IB2STAT,CUTOFF64"
        text = self.changed(
            self.flu,
            anchor,
            anchor + "\n        CALL LCMPUT(IPFLUX,'CUTOFF',1,1,CUTOFF64)",
        )
        self.rejected(flu=text)

    def test_18_change_inherited_cutoff(self) -> None:
        self.rejected(a8=self.changed(
            self.a8,
            "1.0e-7_real32",
            "2.0e-7_real32",
        ))

    def test_19_remove_counterfactual_site(self) -> None:
        self.rejected(a8=self.changed(
            self.a8,
            "guard_live .neqv. guard_zero",
            "guard_live .eqv. guard_zero",
        ))

    def test_20_remove_a9_aggregation(self) -> None:
        self.rejected(a9=self.changed(
            self.a9,
            "cutoff_visit64 = cutoff_visit64 + cutoff_delta64",
            "cutoff_visit64 = 0_int64",
        ))

    def test_21_remove_seed_plane_equality(self) -> None:
        self.rejected(b2b=self.changed(
            self.b2b,
            "if (seed_plane /= source_plane) return",
            "continue",
        ))

    def test_22_narrow_flu_format(self) -> None:
        self.rejected(flu=self.changed(self.flu, "I20)", "I5)"))

    def test_23_miswire_source_finite_check(self) -> None:
        self.rejected(b2b=self.changed(
            self.b2b,
            "ieee_is_finite(source_rho64)",
            "ieee_is_finite(seed_rho64)",
        ))

    def test_24_remove_same_index_system_selection(self) -> None:
        self.rejected(b2o=self.changed(
            self.b2o,
            "input_system = LCMGIL(systems,nplane)",
            "input_system = LCMGIL(systems,1)",
        ))

    def test_25_remove_same_index_seed_selection(self) -> None:
        self.rejected(b2o=self.changed(
            self.b2o,
            "input_seed = LCMGIL(fluxes,nplane)",
            "input_seed = LCMGIL(fluxes,1)",
        ))


if __name__ == "__main__":
    unittest.main()
