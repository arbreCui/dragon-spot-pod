from __future__ import annotations

import unittest

from check_phase_a9b_b2p_solved_lifecycle import (
    B2B_PATH,
    B2C_PATH,
    B2H_PATH,
    check_contract,
)


class B2PContractMutationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.b2b = B2B_PATH.read_text(encoding="utf-8")
        cls.b2c = B2C_PATH.read_text(encoding="utf-8")
        cls.b2h = B2H_PATH.read_text(encoding="utf-8")
        check_contract(cls.b2b, cls.b2c, cls.b2h)

    @staticmethod
    def changed(text: str, old: str, new: str, count: int = 1) -> str:
        if text.count(old) < count:
            raise AssertionError(f"mutation anchor missing: {old!r}")
        return text.replace(old, new, count)

    def rejected(
        self,
        *,
        b2b: str | None = None,
        b2c: str | None = None,
        b2h: str | None = None,
    ) -> None:
        with self.assertRaises(AssertionError):
            check_contract(
                self.b2b if b2b is None else b2b,
                self.b2c if b2c is None else b2c,
                self.b2h if b2h is None else b2h,
            )

    def test_01_change_legacy_abi(self) -> None:
        self.rejected(b2c=self.changed(
            self.b2c,
            "system_name,status)\n    type(c_ptr), intent(in) :: ipflux",
            "system_name,status,ipseed)\n    type(c_ptr), intent(in) :: ipflux,ipseed",
        ))

    def test_02_add_cont_rho_scalar(self) -> None:
        self.rejected(b2c=self.changed(
            self.b2c,
            "ipflux,ipseed_lifecycle, &",
            "ipflux,ipseed_lifecycle,rho64, &",
        ))

    def test_03_remove_present_gate(self) -> None:
        self.rejected(b2c=self.changed(
            self.b2c,
            "publish_solved = present(ipseed_lifecycle)",
            "publish_solved = .true.",
        ))

    def test_04_remove_exact_inventory(self) -> None:
        self.rejected(b2c=self.changed(
            self.b2c,
            "PROJECTED_AUTHORITY_IS_EXACT(lifecycle_authority)",
            ".true.",
        ))

    def test_05_remove_plane_from_inventory(self) -> None:
        self.rejected(b2c=self.changed(
            self.b2c,
            "['RHO         ','PLANE       ','FLUX        ','STATE       ', &",
            "['RHO         ','EXTRA       ','FLUX        ','STATE       ', &",
        ))

    def test_06_remove_seed_flux_validation(self) -> None:
        self.rejected(b2c=self.changed(
            self.b2c,
            "REAL64_FLUX_IS_VALID(lifecycle_authority)",
            ".true.",
        ))

    def test_07_accept_wrong_seed_state(self) -> None:
        self.rejected(b2c=self.changed(
            self.b2c,
            "12,'PROJECTED')) return",
            "12,'SOLVED')) return",
        ))

    def test_08_misread_rho(self) -> None:
        self.rejected(b2c=self.changed(
            self.b2c,
            "call LCMGET(lifecycle_authority,'RHO',lifecycle_rho64)",
            "lifecycle_rho64=1.0_real64",
        ))

    def test_09_misread_plane(self) -> None:
        self.rejected(b2c=self.changed(
            self.b2c,
            "call LCMGET(lifecycle_authority,'PLANE',lifecycle_plane)",
            "lifecycle_plane=1",
        ))

    def test_10_misread_epoch(self) -> None:
        self.rejected(b2c=self.changed(
            self.b2c,
            "call LCMGET(lifecycle_authority,'EPOCH',lifecycle_epoch)",
            "lifecycle_epoch=1",
        ))

    def test_11_remove_rho_finiteness(self) -> None:
        self.rejected(b2c=self.changed(
            self.b2c,
            "if (.not. ieee_is_finite(lifecycle_rho64)) return",
            "continue",
        ))

    def test_12_remove_plane_range(self) -> None:
        self.rejected(b2c=self.changed(
            self.b2c,
            "if (lifecycle_plane < 1 .or. lifecycle_plane > 3) return",
            "continue",
        ))

    def test_13_remove_epoch_guard(self) -> None:
        self.rejected(b2c=self.changed(
            self.b2c,
            "if (lifecycle_epoch < 0 .or. &\n"
            "          lifecycle_epoch == huge(lifecycle_epoch)) return",
            "continue",
        ))

    def test_14_remove_fresh_check(self) -> None:
        self.rejected(b2c=self.changed(
            self.b2c,
            "if (.not. EMPTY_LCM_ROOT(ipflux)) return",
            "continue",
        ))

    def test_15_hardcode_output_rho(self) -> None:
        self.rejected(b2c=self.changed(
            self.b2c,
            "call LCMPUT(authority,'RHO',1,4,lifecycle_rho64)",
            "call LCMPUT(authority,'RHO',1,4,1.0_real64)",
        ))

    def test_16_hardcode_output_plane(self) -> None:
        self.rejected(b2c=self.changed(
            self.b2c,
            "call LCMPUT(authority,'PLANE',1,1,lifecycle_plane)",
            "call LCMPUT(authority,'PLANE',1,1,1)",
        ))

    def test_17_change_solved_state(self) -> None:
        self.rejected(b2c=self.changed(
            self.b2c,
            "authority_state = 'SOLVED'",
            "authority_state = 'PROJECTED'",
        ))

    def test_18_increment_epoch_in_b2c(self) -> None:
        self.rejected(b2c=self.changed(
            self.b2c,
            "call LCMPUT(authority,'EPOCH',1,1,lifecycle_epoch)",
            "call LCMPUT(authority,'EPOCH',1,1,lifecycle_epoch+1)",
        ))

    def test_19_add_return_after_first_write(self) -> None:
        anchor = "authority = LCMDID(ipflux,'SPOT-R64')"
        self.rejected(b2c=self.changed(
            self.b2c, anchor, anchor + "\n    if (.true.) return"
        ))

    def test_20_route_cont_through_legacy(self) -> None:
        self.rejected(b2b=self.changed(
            self.b2b,
            "call SPOR64_B2C_PUBLISH_CONT(ipflux,ipseed, &",
            "call SPOR64_B2C_PUBLISH(ipflux, &",
        ))

    def test_21_misroute_cont_seed(self) -> None:
        self.rejected(b2b=self.changed(
            self.b2b,
            "SPOR64_B2C_PUBLISH_CONT(ipflux,ipseed, &",
            "SPOR64_B2C_PUBLISH_CONT(ipflux,ipsou, &",
        ))

    def test_22_remove_boot_legacy_route(self) -> None:
        self.rejected(b2b=self.changed(
            self.b2b,
            "call SPOR64_B2C_PUBLISH(ipflux,SPOR64_B2B_ACCEPTED_UNPUBLISHED, &",
            "call SPOR64_B2C_PUBLISH_CONT(ipflux,ipseed, &",
        ))

    def test_23_b2h_accepts_projected_seed(self) -> None:
        self.rejected(b2h=self.changed(
            self.b2h,
            "'SOLVED')) return",
            "'PROJECTED')) return",
        ))

    def test_24_b2h_stops_incrementing(self) -> None:
        self.rejected(b2h=self.changed(
            self.b2h,
            "output_epoch = seed_epoch + 1",
            "output_epoch = seed_epoch",
        ))

    def test_25_remove_output_seed_alias_rejection(self) -> None:
        self.rejected(b2c=self.changed(
            self.b2c,
            "if (c_associated(ipflux,ipseed_lifecycle)) return",
            "continue",
        ))

    def test_26_insert_write_before_designated_first_write(self) -> None:
        self.rejected(b2c=self.changed(
            self.b2c,
            "    seen_unknown = .false.",
            "    call LCMPUT(ipflux,'EARLY',1,1,accepted_token)\n"
            "    seen_unknown = .false.",
        ))

    def test_27_mutate_lifecycle_authority(self) -> None:
        anchor = "call LCMGET(lifecycle_authority,'EPOCH',lifecycle_epoch)"
        self.rejected(b2c=self.changed(
            self.b2c,
            anchor,
            anchor + "\n      call LCMPUT(lifecycle_authority,'EPOCH',1,1,"
            "lifecycle_epoch)",
        ))

    def test_28_publish_not_accepted_core_result(self) -> None:
        self.rejected(b2b=self.changed(
            self.b2b,
            "else if (.not. accepted) then",
            "else if (.false.) then",
        ))

    def test_29_change_seed_flux_list_extent(self) -> None:
        self.rejected(b2c=self.changed(
            self.b2c,
            "RECORD_MATCHES(lifecycle_authority,'FLUX',NGRP,10)",
            "RECORD_MATCHES(lifecycle_authority,'FLUX',NGRP-1,10)",
        ))

    def test_30_stop_seed_flux_scan_before_last_group(self) -> None:
        self.rejected(b2c=self.changed(
            self.b2c,
            "    do ig = 1, NGRP\n"
            "      call LCMLEL(ipflux,ig,actual_length,actual_type)",
            "    do ig = 1, NGRP-1\n"
            "      call LCMLEL(ipflux,ig,actual_length,actual_type)",
        ))

    def test_31_remove_seed_flux_element_length_check(self) -> None:
        self.rejected(b2c=self.changed(
            self.b2c,
            "if (actual_length /= NUNKNO .or. actual_type /= 4) return",
            "if (actual_type /= 4) return",
        ))

    def test_32_remove_seed_flux_element_type_check(self) -> None:
        self.rejected(b2c=self.changed(
            self.b2c,
            "if (actual_length /= NUNKNO .or. actual_type /= 4) return",
            "if (actual_length /= NUNKNO) return",
        ))

    def test_33_remove_seed_flux_finiteness_check(self) -> None:
        self.rejected(b2c=self.changed(
            self.b2c,
            "if (.not. all(ieee_is_finite(stage64))) return",
            "if (.false.) return",
        ))

    def test_34_change_legacy_character_abi(self) -> None:
        self.rejected(b2c=self.changed(
            self.b2c,
            "character(len=4), intent(in) :: coptio",
            "character(len=8), intent(in) :: coptio",
        ))

    def test_35_remove_accepted_token_guard(self) -> None:
        self.rejected(b2c=self.changed(
            self.b2c,
            "if (accepted_token /= ACCEPTED_UNPUBLISHED) return",
            "continue",
        ))


if __name__ == "__main__":
    unittest.main()
