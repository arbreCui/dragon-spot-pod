#!/usr/bin/env python3
"""Targeted mutation tests for the B2u static host contract."""

from __future__ import annotations

import json
import unittest

import check_phase_a9b_b2u_same_call_asm_host as contract


class B2UStaticContractMutationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.host = contract.HOST.read_text(encoding="utf-8")
        cls.adapter = contract.ADAPTER.read_text(encoding="utf-8")
        cls.kdr = contract.KDRDRV.read_text(encoding="utf-8")
        cls.dramod = contract.DRAMOD.read_text(encoding="utf-8")
        cls.readme = contract.README.read_text(encoding="utf-8")
        cls.manifest = contract.MANIFEST.read_text(encoding="utf-8")

    def changed(self, text: str, old: str, new: str) -> str:
        self.assertEqual(text.count(old), 1, f"mutation needle differs: {old}")
        return text.replace(old, new, 1)

    def rejected(self, function, text: str) -> None:
        with self.assertRaises(contract.GateError):
            function(text)

    def test_00_baseline(self) -> None:
        contract.check_all()

    # Host mutations: exact media, plane order, common symbols and custody.
    def test_01_host_output_must_be_returned(self) -> None:
        changed = self.changed(
            self.host,
            "PARAMETER RETURNED PROJECTED TRACK_f ::",
            "PARAMETER ASSEMBLED PROJECTED TRACK_f ::",
        )
        self.rejected(contract.check_host, changed)

    def test_02_host_track_must_be_sequential_binary(self) -> None:
        changed = self.changed(
            self.host, "::: SEQ_BINARY TRACK_f", "::: LINKED_LIST TRACK_f"
        )
        self.rejected(contract.check_host, changed)

    def test_03_host_private_inventory_is_exact(self) -> None:
        changed = self.changed(
            self.host,
            "LINKED_LIST MICROLIB2 MACRO0 TRACK SYSTEM1 SYSTEM2 SYSTEM3 ;",
            "LINKED_LIST MICROLIB2 MACRO0 TRACK SYSTEM1 SYSTEM2 SYSTEM3 SOLVED ;",
        )
        self.rejected(contract.check_host, changed)

    def test_04_host_module_allowlist_is_exact(self) -> None:
        changed = self.changed(
            self.host,
            "MODULE RECOVER: ASM: SPOR64T: DELETE: END: ;",
            "MODULE RECOVER: ASM: FLU: SPOR64T: DELETE: END: ;",
        )
        self.rejected(contract.check_host, changed)

    def test_05_host_plane1_library_index_is_owned(self) -> None:
        changed = self.changed(
            self.host,
            "MICROLIB2 := RECOVER: PROJECTED :: ITEM 1 ;",
            "MICROLIB2 := RECOVER: PROJECTED :: ITEM 2 ;",
        )
        self.rejected(contract.check_host, changed)

    def test_06_host_plane2_track_index_is_owned(self) -> None:
        changed = self.changed(
            self.host,
            "TRACK := RECOVER: PROJECTED :: ITEM 2 ;",
            "TRACK := RECOVER: PROJECTED :: ITEM 1 ;",
        )
        self.rejected(contract.check_host, changed)

    def test_07_host_plane3_lk1d_index_is_exact(self) -> None:
        changed = self.changed(
            self.host, "EDIT 0 ARM LK1D 3 ;", "EDIT 0 ARM LK1D 2 ;"
        )
        self.rejected(contract.check_host, changed)

    def test_08_host_asm_uses_common_track_symbol(self) -> None:
        changed = self.changed(
            self.host,
            "SYSTEM1 := ASM: MACRO0 TRACK TRACK_f PROJECTED",
            "SYSTEM1 := ASM: MACRO0 TRACK OTHER_f PROJECTED",
        )
        self.rejected(contract.check_host, changed)

    def test_09_host_asm_uses_common_projected_symbol(self) -> None:
        changed = self.changed(
            self.host,
            "SYSTEM2 := ASM: MACRO0 TRACK TRACK_f PROJECTED",
            "SYSTEM2 := ASM: MACRO0 TRACK TRACK_f OTHER",
        )
        self.rejected(contract.check_host, changed)

    def test_10_host_bridge_system_order_is_exact(self) -> None:
        changed = self.changed(
            self.host,
            "RETURNED := SPOR64T: PROJECTED SYSTEM1 SYSTEM2 SYSTEM3 TRACK_f :: ;",
            "RETURNED := SPOR64T: PROJECTED SYSTEM1 SYSTEM3 SYSTEM2 TRACK_f :: ;",
        )
        self.rejected(contract.check_host, changed)

    def test_11_host_bridge_uses_same_track_symbol(self) -> None:
        changed = self.changed(
            self.host,
            "SYSTEM1 SYSTEM2 SYSTEM3 TRACK_f :: ;",
            "SYSTEM1 SYSTEM2 SYSTEM3 OTHER_f :: ;",
        )
        self.rejected(contract.check_host, changed)

    def test_12_host_cannot_delete_system_before_bridge(self) -> None:
        bridge = (
            "RETURNED := SPOR64T: PROJECTED SYSTEM1 SYSTEM2 SYSTEM3 TRACK_f :: ;"
        )
        changed = self.changed(
            self.host, bridge, "SYSTEM1 := DELETE: SYSTEM1 ;\n" + bridge
        )
        self.rejected(contract.check_host, changed)

    def test_13_host_bridge_call_must_be_unique(self) -> None:
        bridge = (
            "RETURNED := SPOR64T: PROJECTED SYSTEM1 SYSTEM2 SYSTEM3 TRACK_f :: ;"
        )
        changed = self.changed(self.host, bridge, bridge + "\n" + bridge)
        self.rejected(contract.check_host, changed)

    def test_14_host_loop_is_forbidden(self) -> None:
        self.rejected(
            contract.check_host,
            self.host + "\nWHILE 0 1 < DO\nENDWHILE ;\n",
        )

    def test_15_host_relaxation_is_forbidden(self) -> None:
        self.rejected(
            contract.check_host,
            self.host + "\nREAL relaxation := 0.5 ;\n",
        )

    # Adapter mutations: exact six-entry ABI and direct B2t forwarding.
    def test_16_adapter_nentry_is_exact(self) -> None:
        changed = self.changed(self.adapter, "if (nentry /= 6)", "if (nentry /= 5)")
        self.rejected(contract.check_adapter, changed)

    def test_17_adapter_output_name_is_exact(self) -> None:
        changed = self.changed(
            self.adapter, "hentry(1) /= 'RETURNED'", "hentry(1) /= 'ASSEMBLED'"
        )
        self.rejected(contract.check_adapter, changed)

    def test_18_adapter_system_names_are_exact(self) -> None:
        changed = self.changed(
            self.adapter, "hentry(4) /= 'SYSTEM2'", "hentry(4) /= 'SYSTEM1'"
        )
        self.rejected(contract.check_adapter, changed)

    def test_19_adapter_track_name_is_exact(self) -> None:
        changed = self.changed(
            self.adapter, "hentry(6) /= 'TRACK_f'", "hentry(6) /= 'OTHER_f'"
        )
        self.rejected(contract.check_adapter, changed)

    def test_20_adapter_lcm_entry_kinds_are_exact(self) -> None:
        changed = self.changed(
            self.adapter, "any(ientry(1:5) /= 1)", "any(ientry(1:4) /= 1)"
        )
        self.rejected(contract.check_adapter, changed)

    def test_21_adapter_track_entry_kind_is_binary(self) -> None:
        changed = self.changed(
            self.adapter, "ientry(6) /= 3", "ientry(6) /= 4"
        )
        self.rejected(contract.check_adapter, changed)

    def test_22_adapter_output_access_is_create(self) -> None:
        changed = self.changed(
            self.adapter, "jentry(1) /= 0", "jentry(1) /= 1"
        )
        self.rejected(contract.check_adapter, changed)

    def test_23_adapter_inputs_are_read_only(self) -> None:
        changed = self.changed(
            self.adapter, "any(jentry(2:6) /= 2)", "any(jentry(2:6) /= 1)"
        )
        self.rejected(contract.check_adapter, changed)

    def test_24_adapter_option_list_is_exact_empty(self) -> None:
        changed = self.changed(self.adapter, "text4 /= ';'", "text4 /= 'ON  '")
        self.rejected(contract.check_adapter, changed)

    def test_25_adapter_reads_option_list_once(self) -> None:
        call = "call REDGET(indic,nitma,flott,text4,dflott)"
        changed = self.changed(self.adapter, call, call + "\n  " + call)
        self.rejected(contract.check_adapter, changed)

    def test_26_adapter_system_pointer_slice_is_exact(self) -> None:
        changed = self.changed(
            self.adapter, "systems = kentry(3:5)", "systems = kentry(2:4)"
        )
        self.rejected(contract.check_adapter, changed)

    def test_27_adapter_forwards_dispatch_track_pointer(self) -> None:
        changed = self.changed(
            self.adapter,
            "systems,kentry(6), &",
            "systems,kentry(5), &",
        )
        self.rejected(contract.check_adapter, changed)

    def test_28_adapter_explicitly_enables_b2t(self) -> None:
        changed = self.changed(
            self.adapter, "cutoff_by_plane,.true.)", "cutoff_by_plane,.false.)"
        )
        self.rejected(contract.check_adapter, changed)

    def test_29_adapter_accepts_only_returned_status(self) -> None:
        changed = self.changed(
            self.adapter,
            "status /= SPOR64_B2T_RETURNED",
            "status == SPOR64_B2T_RETURNED",
        )
        self.rejected(contract.check_adapter, changed)

    def test_30_adapter_cannot_aggregate_cutoffs(self) -> None:
        changed = self.changed(
            self.adapter,
            "end subroutine SPOR64T",
            "status = sum(cutoff_by_plane)\nend subroutine SPOR64T",
        )
        self.rejected(contract.check_adapter, changed)

    def test_31_adapter_cannot_bypass_b2t(self) -> None:
        changed = self.changed(
            self.adapter,
            "systems = kentry(3:5)",
            "systems = kentry(3:5)\n  call SPOR64_B2K_COMMIT_SYSTEM_ARCHIVE()",
        )
        self.rejected(contract.check_adapter, changed)

    # Dispatcher and sequential-file dispatch lifetime.
    def test_32_kdr_selector_is_exact(self) -> None:
        changed = self.changed(
            self.kdr, "HMODUL.EQ.'SPOR64T:'", "HMODUL.EQ.'SPOR64U:'"
        )
        self.rejected(contract.check_kdr, changed)

    def test_33_kdr_callee_is_exact(self) -> None:
        changed = self.changed(
            self.kdr,
            "CALL SPOR64T(NENTRY,HENTRY,IENTRY,JENTRY,KENTRY)",
            "CALL SPOR64K(NENTRY,HENTRY,IENTRY,JENTRY,KENTRY)",
        )
        self.rejected(contract.check_kdr, changed)

    def test_34_kdr_route_is_unique(self) -> None:
        route = (
            "      ELSE IF(HMODUL.EQ.'SPOR64T:') THEN\n"
            "         CALL SPOR64T(NENTRY,HENTRY,IENTRY,JENTRY,KENTRY)"
        )
        changed = self.changed(self.kdr, route, route + "\n" + route)
        self.rejected(contract.check_kdr, changed)

    def test_35_dramod_must_open_file_per_dispatch(self) -> None:
        changed = self.changed(
            self.dramod,
            "my_file_array(i)%my_file=>FILOPN(hparam,jentry(i),ientry(i)-1,0)",
            "my_file_array(i)%my_file=>C_NULL_PTR",
        )
        self.rejected(contract.check_dramod, changed)

    def test_36_dramod_must_close_file_after_dispatch(self) -> None:
        changed = self.changed(
            self.dramod,
            "ier=FILCLS(my_file_array(i)%my_file,1)",
            "ier=0",
        )
        self.rejected(contract.check_dramod, changed)

    def test_37_shipped_selection_is_rejected(self) -> None:
        with self.assertRaises(contract.GateError):
            contract.check_deployment({
                "data/shipped.x2m": (
                    "PROCEDURE SpotStepR64 ;\n"
                    "RETURNED := SpotStepR64 PROJECTED TRACK_f :: ;\n"
                )
            })

    # Metadata mutations prevent claim drift even when code is unchanged.
    def test_38_manifest_cross_dispatch_pointer_overclaim_is_rejected(self) -> None:
        changed = self.changed(
            self.manifest,
            '"same_live_pointer_across_asm1_asm2_asm3_and_spor64t": false',
            '"same_live_pointer_across_asm1_asm2_asm3_and_spor64t": true',
        )
        with self.assertRaises(contract.GateError):
            contract.check_manifest(json.loads(changed))

    def test_39_readme_runtime_overclaim_is_rejected(self) -> None:
        changed = self.changed(
            self.readme,
            "RUNTIME ASM / TRANSPORT / MAP   = NOT EXECUTED",
            "RUNTIME ASM / TRANSPORT / MAP   = EXECUTED",
        )
        self.rejected(contract.check_readme, changed)


if __name__ == "__main__":
    unittest.main()
