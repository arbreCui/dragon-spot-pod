from __future__ import annotations

import copy
import re
import unittest

import check_phase_a9b_b2c_publication as gate


def replace_once(text: str, pattern: str, replacement: str) -> str:
    changed, count = re.subn(pattern, replacement, text, count=1, flags=re.I | re.S)
    if count != 1:
        raise AssertionError(f"mutation pattern count {count}: {pattern}")
    return changed


class RepositoryBaseline(unittest.TestCase):
    def test_repository_contract(self) -> None:
        gate.check_repository()


class PublisherMutations(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = gate.B2C.read_text()

    def reject(self, pattern: str, replacement: str) -> None:
        mutant = replace_once(self.source, pattern, replacement)
        with self.assertRaises(gate.ContractError):
            gate.check_publisher_text(mutant)


PUBLISHER_MUTATIONS = [
    ("status5", r"SPOR64_B2C_PREFLIGHT_FAILED\s*=\s*5", "SPOR64_B2C_PREFLIGHT_FAILED = 9"),
    ("status6", r"SPOR64_B2C_CHILD_PUBLISHED\s*=\s*6", "SPOR64_B2C_CHILD_PUBLISHED = 9"),
    ("status7", r"SPOR64_B2C_DRIVER_COMMITTED\s*=\s*7", "SPOR64_B2C_DRIVER_COMMITTED = 9"),
    ("status8", r"SPOR64_B2C_HOST_COMMITTED\s*=\s*8", "SPOR64_B2C_HOST_COMMITTED = 9"),
    ("token", r"ACCEPTED_UNPUBLISHED\s*=\s*4", "ACCEPTED_UNPUBLISHED = 3"),
    ("initial_status", r"status\s*=\s*SPOR64_B2C_PREFLIGHT_FAILED", "status = SPOR64_B2C_HOST_COMMITTED"),
    ("accepted_guard", r"accepted_token\s*/=\s*ACCEPTED_UNPUBLISHED", "accepted_token == ACCEPTED_UNPUBLISHED"),
    ("finite_flux", r"ieee_is_finite\(terminal_flux64\)", "ieee_is_finite(terminal_source64)"),
    ("finite_source", r"ieee_is_finite\(terminal_source64\)", "ieee_is_finite(terminal_flux64)"),
    ("range_flux", r"abs\(terminal_flux64\)\s*>\s*REAL32_MAX64", "abs(terminal_flux64) > 2.0_real64*REAL32_MAX64"),
    ("range_source", r"abs\(terminal_source64\)\s*>\s*REAL32_MAX64", "abs(terminal_source64) > 2.0_real64*REAL32_MAX64"),
    ("collision_spot", r"ABSENT_RECORD\(ipflux,'SPOT-R64'\)", "ABSENT_RECORD(ipflux,'SPOT-X64')"),
    ("collision_sour", r"ABSENT_RECORD\(ipflux,'SOUR'\)", "ABSENT_RECORD(ipflux,'SOURX')"),
    ("collision_aflux", r"ABSENT_RECORD\(ipflux,'AFLUX'\)", "ABSENT_RECORD(ipflux,'AFLUXX')"),
    ("collision_dflux", r"ABSENT_RECORD\(ipflux,'DFLUX'\)", "ABSENT_RECORD(ipflux,'DFLUXX')"),
    ("collision_adflux", r"ABSENT_RECORD\(ipflux,'ADFLUX'\)", "ABSENT_RECORD(ipflux,'ADFLUXX')"),
    ("legacy_schema", r"RECORD_MATCHES\(ipflux,'FLUX',NGRP,10\)", "RECORD_MATCHES(ipflux,'FLUX',NGRP,2)"),
    ("state_preflight", r"RECORD_MATCHES\(ipflux,'STATE-VECTOR',NSTATE,1\)", "RECORD_MATCHES(ipflux,'STATE-VECTOR',NSTATE,2)"),
    ("eps_preflight", r"RECORD_MATCHES\(ipflux,'EPS-CONVERGE',5,2\)", "RECORD_MATCHES(ipflux,'EPS-CONVERGE',4,2)"),
    ("key_preflight", r"ABSENT_OR_MATCHES\(ipflux,'KEYFLX',NREG,1\)", "ABSENT_OR_MATCHES(ipflux,'KEYFLX',NREG,2)"),
    ("option_preflight", r"ABSENT_OR_MATCHES\(ipflux,'OPTION',1,3\)", "ABSENT_OR_MATCHES(ipflux,'OPTION',2,3)"),
    ("link_macro_preflight", r"ABSENT_OR_MATCHES\(ipflux,'LINK.MACRO',3,3\)", "ABSENT_OR_MATCHES(ipflux,'LINK.MACRO',4,3)"),
    ("link_track_preflight", r"ABSENT_OR_MATCHES\(ipflux,'LINK.TRACK',3,3\)", "ABSENT_OR_MATCHES(ipflux,'LINK.TRACK',4,3)"),
    ("link_system_preflight", r"ABSENT_OR_MATCHES\(ipflux,'LINK.SYSTEM',3,3\)", "ABSENT_OR_MATCHES(ipflux,'LINK.SYSTEM',4,3)"),
    ("leak_preflight", r"ABSENT_OR_MATCHES\(ipflux,'SPOT-LEAK1D',NGRP,2\)", "ABSENT_OR_MATCHES(ipflux,'SPOT-LEAK1D',NGRP,4)"),
    ("legacy_element", r"itylcm\s*/=\s*2", "itylcm /= 4"),
    ("allocation", r"allocate\(flux_stage32", "allocate(source_stage32"),
    ("authority_name", r"LCMDID\(ipflux,'SPOT-R64'\)", "LCMDID(ipflux,'SPOT-X64')"),
    ("authority_flux_type", r"LCMPDL\(authority_flux,ig,NUNKNO,4", "LCMPDL(authority_flux,ig,NUNKNO,2"),
    ("authority_source_type", r"LCMPDL\(authority_source,ig,NUNKNO,4", "LCMPDL(authority_source,ig,NUNKNO,2"),
    ("flux_conversion", r"flux_stage32\s*=\s*real\(terminal_flux64,real32\)", "flux_stage32 = real(terminal_source64,real32)"),
    ("source_conversion", r"source_stage32\s*=\s*real\(terminal_source64,real32\)", "source_stage32 = real(terminal_flux64,real32)"),
    ("legacy_flux_type", r"LCMPDL\(legacy_flux,ig,NUNKNO,2", "LCMPDL(legacy_flux,ig,NUNKNO,4"),
    ("legacy_source_name", r"LCMLID\(ipflux,'SOUR',NGRP\)", "LCMLID(ipflux,'SOURCE',NGRP)"),
    ("state_record", r"'STATE-VECTOR'", "'STATE-VECTOX'"),
    ("eps_record", r"'EPS-CONVERGE'", "'EPS-CONVERGX'"),
    ("key_record", r"'KEYFLX'", "'KEYFLY'"),
    ("option_record", r"'OPTION'", "'OPTIOX'"),
    ("macro_link", r"'LINK.MACRO'", "'LINK.MACRX'"),
    ("track_link", r"'LINK.TRACK'", "'LINK.TRACX'"),
    ("system_link", r"'LINK.SYSTEM'", "'LINK.SYSTEX'"),
    ("leak_record", r"'SPOT-LEAK1D'", "'SPOT-LEAK1X'"),
    ("final_status", r"status\s*=\s*SPOR64_B2C_HOST_COMMITTED", "status = SPOR64_B2C_DRIVER_COMMITTED"),
    ("fallback", r"deallocate\(flux_stage32,source_stage32\)", "call FLUDRV\n    deallocate(flux_stage32,source_stage32)"),
]


def make_publisher_test(pattern: str, replacement: str):
    def test(self: PublisherMutations) -> None:
        self.reject(pattern, replacement)

    return test


for mutation_name, mutation_pattern, mutation_replacement in PUBLISHER_MUTATIONS:
    setattr(
        PublisherMutations,
        f"test_mutation_{mutation_name}",
        make_publisher_test(mutation_pattern, mutation_replacement),
    )


class IntegrationMutations(unittest.TestCase):
    def test_b2b_call_removed(self) -> None:
        text = replace_once(gate.B2B.read_text(), r"call\s+SPOR64_B2C_PUBLISH", "call B2C_REMOVED")
        with self.assertRaises(gate.ContractError):
            gate.check_b2b_text(text)

    def test_b2b_token_changed(self) -> None:
        text = replace_once(
            gate.B2B.read_text(),
            r"SPOR64_B2C_PUBLISH\(ipflux,SPOR64_B2B_ACCEPTED_UNPUBLISHED",
            "SPOR64_B2C_PUBLISH(ipflux,SPOR64_B2B_NOT_ACCEPTED",
        )
        with self.assertRaises(gate.ContractError):
            gate.check_b2b_text(text)

    def test_flu_success_status_changed(self) -> None:
        text = replace_once(
            gate.FLU.read_text(),
            r"IB2STAT\.EQ\.SPOR64_B2C_HOST_COMMITTED",
            "IB2STAT.EQ.SPOR64_B2C_DRIVER_COMMITTED",
        )
        with self.assertRaises(gate.ContractError):
            gate.check_flu_text(text)

    def test_flu_return_removed(self) -> None:
        text = replace_once(
            gate.FLU.read_text(), r"DEALLOCATE\(IMERG\)\s*RETURN", "DEALLOCATE(IMERG)\n      CONTINUE"
        )
        with self.assertRaises(gate.ContractError):
            gate.check_flu_text(text)

    def test_dependency_removed(self) -> None:
        deps = gate.DEPS.read_text().replace("FLU.o: SPOR64_B2B.o SPOR64_B2C.o", "FLU.o: SPOR64_B2B.o", 1)
        with self.assertRaises(gate.ContractError):
            gate.check_build_text(gate.MAKEFILE.read_text(), deps)

    def test_target_dependency_added(self) -> None:
        make = gate.MAKEFILE.read_text().replace(
            "spot-real64-phase-a9b-b2c-publication :",
            "spot-real64-phase-a9b-b2c-publication : all",
            1,
        )
        with self.assertRaises(gate.ContractError):
            gate.check_build_text(make, gate.DEPS.read_text())


class SourceHardeningMutations(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.b2c = gate.B2C.read_text()
        cls.b2b = gate.B2B.read_text()
        cls.flu = gate.FLU.read_text()

    def test_b2c_cannot_delete_lcm_record(self) -> None:
        text = replace_once(
            self.b2c,
            r"(\n\s*authority\s*=\s*LCMDID)",
            r"\n    call LCMDEL(ipflux,'FLUX')\1",
        )
        with self.assertRaises(gate.ContractError):
            gate.check_publisher_text(text)

    def test_b2c_column_one_call_is_not_a_comment(self) -> None:
        text = replace_once(
            self.b2c,
            r"(\n\s*authority\s*=\s*LCMDID)",
            r"\ncall LCMDEL(ipflux,'FLUX')\1",
        )
        with self.assertRaises(gate.ContractError):
            gate.check_publisher_text(text)

    def test_b2c_unreviewed_wrapper_call_is_rejected(self) -> None:
        text = replace_once(
            self.b2c,
            r"(\n\s*authority\s*=\s*LCMDID)",
            r"\n    call ROGUE_MUTATE(ipflux)\1",
        )
        with self.assertRaises(gate.ContractError):
            gate.check_publisher_text(text)

    def test_b2c_free_form_continued_call_is_rejected(self) -> None:
        text = replace_once(
            self.b2c,
            r"(\n\s*authority\s*=\s*LCMDID)",
            r"\n    ca&\n&ll ROGUE_MUTATE(ipflux)\1",
        )
        with self.assertRaises(gate.ContractError):
            gate.check_publisher_text(text)

    def test_b2c_function_style_wrapper_is_rejected(self) -> None:
        text = replace_once(
            self.b2c,
            r"(\n\s*authority\s*=\s*LCMDID)",
            r"\n    if (ROGUE_MUTATE(ipflux)) return\1",
        )
        with self.assertRaises(gate.ContractError):
            gate.check_publisher_text(text)

    def test_b2c_cannot_create_unreviewed_lcm_list(self) -> None:
        text = replace_once(
            self.b2c,
            r"(\n\s*authority\s*=\s*LCMDID)",
            r"\n    authority = LCMDIL(ipflux,1)\1",
        )
        with self.assertRaises(gate.ContractError):
            gate.check_publisher_text(text)

    def test_b2c_cannot_alias_lcmdel(self) -> None:
        text = replace_once(
            self.b2c,
            r"use\s+GANLIB",
            "use GANLIB, BAD_DELETE => LCMDEL",
        )
        text = replace_once(
            text,
            r"(\n\s*authority\s*=\s*LCMDID)",
            r"\n    call BAD_DELETE(ipflux,'FLUX')\1",
        )
        with self.assertRaises(gate.ContractError):
            gate.check_publisher_text(text)

    def test_b2b_cannot_delete_lcm_record(self) -> None:
        text = replace_once(
            self.b2b,
            r"(\n\s*admission_complete\s*=\s*\.true\.)",
            r"\n    call LCMDEL(ipflux,'FLUX')\1",
        )
        with self.assertRaises(gate.ContractError):
            gate.check_b2b_text(text)

    def test_b2b_column_one_call_is_not_a_comment(self) -> None:
        text = replace_once(
            self.b2b,
            r"(\n\s*admission_complete\s*=\s*\.true\.)",
            r"\ncall LCMDEL(ipflux,'FLUX')\1",
        )
        with self.assertRaises(gate.ContractError):
            gate.check_b2b_text(text)

    def test_b2b_unreviewed_wrapper_call_is_rejected(self) -> None:
        text = replace_once(
            self.b2b,
            r"(\n\s*admission_complete\s*=\s*\.true\.)",
            r"\n    call ROGUE_MUTATE(ipflux)\1",
        )
        with self.assertRaises(gate.ContractError):
            gate.check_b2b_text(text)

    def test_b2b_free_form_continued_call_is_rejected(self) -> None:
        text = replace_once(
            self.b2b,
            r"(\n\s*admission_complete\s*=\s*\.true\.)",
            r"\n    ca&\n&ll ROGUE_MUTATE(ipflux)\1",
        )
        with self.assertRaises(gate.ContractError):
            gate.check_b2b_text(text)

    def test_b2b_function_style_wrapper_is_rejected(self) -> None:
        text = replace_once(
            self.b2b,
            r"(\n\s*admission_complete\s*=\s*\.true\.)",
            r"\n    if (ROGUE_MUTATE(ipflux)) return\1",
        )
        with self.assertRaises(gate.ContractError):
            gate.check_b2b_text(text)

    def test_b2b_cannot_create_unreviewed_lcm_list(self) -> None:
        text = replace_once(
            self.b2b,
            r"(\n\s*admission_complete\s*=\s*\.true\.)",
            r"\n    jpflux = LCMDIL(ipflux,1)\1",
        )
        with self.assertRaises(gate.ContractError):
            gate.check_b2b_text(text)

    def test_b2b_cannot_alias_lcmdel(self) -> None:
        text = replace_once(
            self.b2b,
            r"use\s+GANLIB",
            "use GANLIB, BAD_DELETE => LCMDEL",
        )
        text = replace_once(
            text,
            r"(\n\s*admission_complete\s*=\s*\.true\.)",
            r"\n    call BAD_DELETE(ipflux,'FLUX')\1",
        )
        with self.assertRaises(gate.ContractError):
            gate.check_b2b_text(text)

    def test_b2b_early_schema_guard_cannot_be_removed(self) -> None:
        text = replace_once(
            self.b2b,
            r"if\s*\(\.not\.\s*ABSENT_OR_MATCHES\(ipflux,'KEYFLX',NREG,1\)\)\s*return",
            "continue",
        )
        with self.assertRaises(gate.ContractError):
            gate.check_b2b_text(text)

    def test_flu_selected_branch_cannot_delete_lcm_record(self) -> None:
        text = replace_once(
            self.flu,
            r"(\n\s*DEALLOCATE\(IMERG\)\s*\n\s*RETURN)",
            r"\n        CALL LCMDEL(IPFLUX,'FLUX')\1",
        )
        with self.assertRaises(gate.ContractError):
            gate.check_flu_text(text)

    def test_flu_selected_branch_wrapper_call_is_rejected(self) -> None:
        text = replace_once(
            self.flu,
            r"(\n\s*DEALLOCATE\(IMERG\)\s*\n\s*RETURN)",
            r"\n        CALL ROGUE_MUTATE(IPFLUX)\1",
        )
        with self.assertRaises(gate.ContractError):
            gate.check_flu_text(text)

    def test_flu_fixed_form_continued_wrapper_call_is_rejected(self) -> None:
        text = replace_once(
            self.flu,
            r"(\n\s*DEALLOCATE\(IMERG\)\s*\n\s*RETURN)",
            r"\n      CA\n     1LL ROGUE_MUTATE(IPFLUX)\1",
        )
        with self.assertRaises(gate.ContractError):
            gate.check_flu_text(text)

    def test_flu_fixed_form_continued_lcm_write_is_rejected(self) -> None:
        text = replace_once(
            self.flu,
            r"(\n\s*DEALLOCATE\(IMERG\)\s*\n\s*RETURN)",
            r"\n      CA\n     1LL LCMP\n     2UT(IPFLUX,'ROGUE',1,1,IMERG)\1",
        )
        with self.assertRaises(gate.ContractError):
            gate.check_flu_text(text)

    def test_flu_function_style_wrapper_is_rejected(self) -> None:
        text = replace_once(
            self.flu,
            r"(\n\s*DEALLOCATE\(IMERG\)\s*\n\s*RETURN)",
            r"\n      IF(ROGUE_MUTATE(IPFLUX).NE.0) CONTINUE\1",
        )
        with self.assertRaises(gate.ContractError):
            gate.check_flu_text(text)

    def test_flu_prebranch_wrapper_call_is_rejected(self) -> None:
        text = replace_once(
            self.flu,
            r"(\n\s*IF\(LR64\)\s*THEN)",
            r"\n      CALL ROGUE_MUTATE(IPFLUX)\1",
        )
        with self.assertRaises(gate.ContractError):
            gate.check_flu_text(text)

    def test_flu_prebranch_lcm_list_creation_is_rejected(self) -> None:
        text = replace_once(
            self.flu,
            r"(\n\s*IF\(LR64\)\s*THEN)",
            r"\n      IPFLUP=LCMDIL(IPFLUX,1)\1",
        )
        with self.assertRaises(gate.ContractError):
            gate.check_flu_text(text)

    def test_flu_selector_cannot_be_cleared_before_branch(self) -> None:
        text = replace_once(
            self.flu,
            r"(\n\s*IF\(LR64\)\s*THEN)",
            r"\n      LR64=.FALSE.\1",
        )
        with self.assertRaises(gate.ContractError):
            gate.check_flu_text(text)

    def test_flu_selected_route_cannot_jump_to_legacy(self) -> None:
        text = replace_once(
            self.flu,
            r"(\n\s*IF\(LR64\)\s*THEN)",
            r"\n      GO TO 9123\1",
        )
        text = replace_once(
            text,
            r"(\n\s*ENDIF\s*\n\*----\n\*  COMMIT PARSER-INDEPENDENT)",
            r"\n 9123 CONTINUE\1",
        )
        with self.assertRaises(gate.ContractError):
            gate.check_flu_text(text)

    def test_flu_fixed_form_statement_label_cannot_move(self) -> None:
        text = self.flu.replace("   10 CONTINUE", "      CONTINUE", 1)
        text = text.replace("      ISTATE(:NSTATE)=0", "   10 ISTATE(:NSTATE)=0", 1)
        self.assertNotEqual(text, self.flu)
        with self.assertRaises(gate.ContractError):
            gate.check_flu_text(text)

    def test_flu_lcmdel_use_alias_is_rejected(self) -> None:
        text = replace_once(
            self.flu,
            r"USE\s+GANLIB",
            "USE GANLIB, ONLY: LCMDEL_ALIAS => LCMDEL",
        )
        text = replace_once(
            text,
            r"(\n\s*DEALLOCATE\(IMERG\)\s*\n\s*RETURN)",
            r"\n        CALL LCMDEL_ALIAS(IPFLUX,'FLUX')\1",
        )
        with self.assertRaises(gate.ContractError):
            gate.check_flu_text(text)

    def test_flu_lcmdel_procedure_alias_is_rejected(self) -> None:
        text = replace_once(
            self.flu,
            r"(INTEGER\(INT64\)\s+CUTOFF64)",
            r"\1\n      PROCEDURE(LCMDEL), POINTER :: BADDEL => LCMDEL",
        )
        text = replace_once(
            text,
            r"(\n\s*DEALLOCATE\(IMERG\)\s*\n\s*RETURN)",
            r"\n        CALL BADDEL(IPFLUX,'FLUX')\1",
        )
        with self.assertRaises(gate.ContractError):
            gate.check_flu_text(text)

    def test_flu_selected_branch_cannot_create_lcm_list(self) -> None:
        text = replace_once(
            self.flu,
            r"(\n\s*DEALLOCATE\(IMERG\)\s*\n\s*RETURN)",
            r"\n        IPFLUP=LCMDIL(IPFLUX,1)\1",
        )
        with self.assertRaises(gate.ContractError):
            gate.check_flu_text(text)

    def test_publisher_use_rename_is_rejected(self) -> None:
        text = replace_once(
            self.b2b,
            r"use\s+SPOR64_B2C\s*,\s*only\s*:\s*SPOR64_B2C_PUBLISH",
            "use SPOR64_B2C, only : BAD_PUBLISH => SPOR64_B2C_PUBLISH",
        )
        text = replace_once(text, r"call\s+SPOR64_B2C_PUBLISH", "call BAD_PUBLISH")
        with self.assertRaises(gate.ContractError):
            gate.check_global_publisher_callsites({"SPOR64_B2B.f90": text})

    def test_publisher_procedure_alias_is_rejected(self) -> None:
        text = replace_once(
            self.b2b,
            r"(implicit\s+none)",
            r"\1\n  procedure(SPOR64_B2C_PUBLISH), pointer :: BAD_PUBLISH => SPOR64_B2C_PUBLISH",
        )
        with self.assertRaises(gate.ContractError):
            gate.check_global_publisher_callsites({"SPOR64_B2B.f90": text})

    def test_column_one_publisher_call_in_other_free_source_is_rejected(self) -> None:
        path = gate.ROOT / "src/SPOR64_A9.f90"
        text = "call SPOR64_B2C_PUBLISH()\n" + path.read_text()
        with self.assertRaises(gate.ContractError):
            gate.check_global_publisher_callsites({"SPOR64_A9.f90": text})

    def test_continued_publisher_name_in_other_free_source_is_rejected(self) -> None:
        path = gate.ROOT / "src/SPOR64_A9.f90"
        text = "call SPOR64_B2C_&\n&PUBLISH()\n" + path.read_text()
        with self.assertRaises(gate.ContractError):
            gate.check_global_publisher_callsites({"SPOR64_A9.f90": text})

    def test_publisher_call_cannot_arrive_through_include(self) -> None:
        path = gate.ROOT / "src/SPOR64_A9.f90"
        text = "include 'rogue_publisher.inc'\n" + path.read_text()
        with self.assertRaises(gate.ContractError):
            gate.check_global_publisher_callsites({"SPOR64_A9.f90": text})

    def test_blank_spelled_fixed_form_include_is_rejected(self) -> None:
        text = "      I N C L U D E 'rogue_publisher.inc'\n" + gate.FLU.read_text()
        with self.assertRaises(gate.ContractError):
            gate.check_global_publisher_callsites({"FLU.f": text})

    def test_publisher_call_cannot_arrive_through_cpp_token_paste(self) -> None:
        path = gate.ROOT / "src/SPOR64_A9.f90"
        text = (
            "#define CAT(a,b) a ## b\n"
            "call CAT(SPOR64_B2C_,PUBLISH)()\n"
            + path.read_text()
        )
        with self.assertRaises(gate.ContractError):
            gate.check_global_publisher_callsites({"SPOR64_A9.f90": text})

    def test_blank_spelled_fixed_form_publisher_call_is_rejected(self) -> None:
        text = replace_once(
            self.flu,
            r"(\n\s*IF\(LR64\)\s*THEN)",
            r"\n      C A L L SPOR64_B2C_PUBL ISH()\1",
        )
        with self.assertRaises(gate.ContractError):
            gate.check_global_publisher_callsites({"FLU.f": text})


class HelperHardeningMutations(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.b2c = gate.B2C.read_text()
        cls.b2b = gate.B2B.read_text()

    def reject_b2c(self, pattern: str, replacement: str) -> None:
        text = replace_once(self.b2c, pattern, replacement)
        with self.assertRaises(gate.ContractError):
            gate.check_publisher_text(text)

    def reject_b2b(self, pattern: str, replacement: str) -> None:
        text = replace_once(self.b2b, pattern, replacement)
        with self.assertRaises(gate.ContractError):
            gate.check_b2b_text(text)

    def test_required_guard_cannot_be_replaced_by_string_decoy(self) -> None:
        text = replace_once(
            self.b2c,
            r"(integer\s*::\s*state_vector\(NSTATE\))",
            r'\1\n    character(len=*), parameter :: fake_guard = '
            r'"IF(.NOT.ABSENT_RECORD(IPFLUX,\'SPOT-R64\'))RETURN"',
        )
        text = replace_once(
            text,
            r"if\s*\(\.not\.\s*ABSENT_RECORD\(ipflux,'SPOT-R64'\)\)\s*return",
            "continue",
        )
        with self.assertRaises(gate.ContractError):
            gate.check_publisher_text(text)

    def test_b2c_record_schema_conjunction_is_frozen(self) -> None:
        self.reject_b2c(
            r"actual_length\s*==\s*expected_length\s*\.and\.",
            "actual_length == expected_length .or.",
        )

    def test_b2c_absence_conjunction_is_frozen(self) -> None:
        self.reject_b2c(
            r"actual_length\s*==\s*0\s*\.and\.\s*actual_type\s*==\s*99",
            "actual_length == 0 .or. actual_type == 99",
        )

    def test_b2c_absent_or_matches_default_is_frozen(self) -> None:
        self.reject_b2c(
            r"ABSENT_OR_MATCHES\s*=\s*\.false\.",
            "ABSENT_OR_MATCHES = .true.",
        )

    def test_b2b_lcm_entry_kind_is_frozen(self) -> None:
        self.reject_b2b(
            r"LCM_ENTRY_KIND\s*=\s*kind_value\s*==\s*1\s*\.or\.\s*kind_value\s*==\s*2",
            "LCM_ENTRY_KIND = .true.",
        )

    def test_b2b_record_schema_conjunction_is_frozen(self) -> None:
        self.reject_b2b(
            r"actual_length\s*==\s*expected_length\s*\.and\.",
            "actual_length == expected_length .or.",
        )

    def test_b2b_absence_conjunction_is_frozen(self) -> None:
        self.reject_b2b(
            r"actual_length\s*==\s*0\s*\.and\.\s*actual_type\s*==\s*99",
            "actual_length == 0 .or. actual_type == 99",
        )

    def test_b2b_absent_or_matches_default_is_frozen(self) -> None:
        self.reject_b2b(
            r"ABSENT_OR_MATCHES\s*=\s*\.false\.",
            "ABSENT_OR_MATCHES = .true.",
        )

    def test_b2b_character_record_comparison_is_frozen(self) -> None:
        self.reject_b2b(
            r"value\(1:character_count\)\s*==\s*expected_value",
            "value(1:character_count) /= expected_value",
        )


class RunnerHardeningMutations(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.runner = gate.RUNNER.read_text()

    def rejected_semantics(self, text: str) -> None:
        with self.assertRaises(gate.ContractError):
            gate.check_runner(text, verify_hash=False)

    def test_runner_hash_drift_is_rejected(self) -> None:
        with self.assertRaises(gate.ContractError):
            gate.check_runner(self.runner + "\n# drift\n")

    def test_runner_fc_reassignment_is_rejected(self) -> None:
        self.rejected_semantics(self.runner + "\nFC=/tmp/fake\n")

    def test_runner_export_fc_reassignment_is_rejected(self) -> None:
        self.rejected_semantics(self.runner + "\nexport FC=/tmp/fake\n")

    def test_runner_env_compiler_dispatch_is_rejected(self) -> None:
        text = replace_once(self.runner, r'"\$FC"\s+-O0', 'env "$FC" -O0')
        self.rejected_semantics(text)

    def test_runner_direct_compiler_is_rejected(self) -> None:
        self.rejected_semantics(
            self.runner + "\n/opt/homebrew/bin/gfortran rogue.f90 -o rogue\n"
        )

    def test_runner_extra_artifact_execution_is_rejected(self) -> None:
        self.rejected_semantics(self.runner + '\n"$BUILD_DIR/rogue"\n')

    def test_runner_command_substitution_execution_is_rejected(self) -> None:
        self.rejected_semantics(self.runner + '\nprobe=$("$BUILD_DIR/rogue")\n')

    def test_runner_pipe_execution_is_rejected(self) -> None:
        self.rejected_semantics(self.runner + '\nprintf x | "$BUILD_DIR/rogue"\n')

    def test_runner_secondary_shell_is_rejected(self) -> None:
        self.rejected_semantics(self.runner + '\nsh -c "$BUILD_DIR/rogue"\n')

    def test_runner_quoted_dragon_is_rejected(self) -> None:
        self.rejected_semantics(self.runner + '\n"$ROOT/bin/Darwin_arm64/Dragon"\n')

    def test_runner_dot_source_is_rejected(self) -> None:
        self.rejected_semantics(self.runner + '\n. "$BUILD_DIR/rogue"\n')

    def test_runner_backtick_substitution_is_rejected(self) -> None:
        self.rejected_semantics(self.runner + '\nprobe=`"$BUILD_DIR/rogue"`\n')

    def test_runner_single_line_function_is_rejected(self) -> None:
        self.rejected_semantics(
            self.runner + '\nrogue() { "$BUILD_DIR/rogue"; }\n'
        )

    def test_runner_variable_indirect_dragon_is_rejected(self) -> None:
        self.rejected_semantics(
            self.runner + '\nSOLVER="$ROOT/bin/Darwin_arm64/Dragon"\n"$SOLVER"\n'
        )

    def test_runner_root_other_solver_is_rejected(self) -> None:
        self.rejected_semantics(self.runner + '\n"$ROOT/bin/OtherSolver"\n')

    def test_runner_function_internal_dragon_is_rejected(self) -> None:
        self.rejected_semantics(
            self.runner + '\nrogue() { "$ROOT/bin/Darwin_arm64/Dragon"; }\n'
        )

    def test_runner_thirteenth_state_scenario_is_rejected(self) -> None:
        text = replace_once(
            self.runner,
            r"over-negative\s+boundary\s+normal\n",
            "over-negative boundary normal normal\n",
        )
        self.rejected_semantics(text)

    def test_runner_sixth_publisher_scenario_is_rejected(self) -> None:
        text = replace_once(
            self.runner,
            r"for\s+scenario\s+in\s+valid\s+wrong-token\s+existing-spot\s+nan\s+range\n",
            "for scenario in valid wrong-token existing-spot nan range valid\n",
        )
        self.rejected_semantics(text)

    def test_runner_quote_spliced_dynamic_path_is_rejected(self) -> None:
        self.rejected_semantics(self.runner + '\n"$SYN_DIR""/rogue"\n')

    def test_runner_quoted_dot_source_is_rejected(self) -> None:
        self.rejected_semantics(self.runner + "\n'.' \"$BUILD_DIR/rogue\"\n")

    def test_runner_keyword_function_is_rejected(self) -> None:
        self.rejected_semantics(
            self.runner + '\nfunction rogue { "$SYN_DIR/rogue"; }; rogue\n'
        )

    def test_runner_assignment_prefixed_execution_is_rejected(self) -> None:
        self.rejected_semantics(
            self.runner + '\nX=1 "$ROOT/bin/Darwin_arm64/Dragon"\n'
        )

    def test_runner_positional_parameter_execution_is_rejected(self) -> None:
        self.rejected_semantics(
            self.runner + '\nset -- "$ROOT/bin/Darwin_arm64/Dragon"\n"$@"\n'
        )

    def test_runner_semicolon_dot_source_is_rejected(self) -> None:
        self.rejected_semantics(self.runner + '\n:; . "$BUILD_DIR/rogue"\n')

    def test_runner_hidden_extra_execution_is_rejected(self) -> None:
        text = replace_once(
            self.runner,
            r"then\n(\s*)echo \"SPOR64 PHASE-A9b-B2c FAILURE: state-machine",
            r'then\n\1  "$SYN_DIR/b2c_state_machine" normal\n\1echo "SPOR64 PHASE-A9b-B2c FAILURE: state-machine',
        )
        self.rejected_semantics(text)

    def test_runner_split_command_name_is_rejected(self) -> None:
        self.rejected_semantics(
            self.runner + '\ncom""mand "$ROOT/bin/Darwin_arm64/Dragon"\n'
        )

    def test_runner_secondary_shell_option_variant_is_rejected(self) -> None:
        self.rejected_semantics(
            self.runner + '\nsh -ec \"$ROOT/bin/Darwin_arm64/Dragon\"\n'
        )

    def test_runner_embedded_interpreter_execution_is_rejected(self) -> None:
        self.rejected_semantics(
            self.runner
            + "\npython3 -c 'import os; os.system(\"$ROOT/bin/Darwin_arm64/Dragon\")'\n"
        )


class LiteralHardeningMutations(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.b2c = gate.B2C.read_text()
        cls.b2b = gate.B2B.read_text()

    def reject_b2c(self, pattern: str, replacement: str) -> None:
        text = replace_once(self.b2c, pattern, replacement)
        with self.assertRaises(gate.ContractError):
            gate.check_publisher_text(text)

    def reject_b2b(self, pattern: str, replacement: str) -> None:
        text = replace_once(self.b2b, pattern, replacement)
        with self.assertRaises(gate.ContractError):
            gate.check_b2b_text(text)

    def test_spot_epoch_embedded_space_is_rejected(self) -> None:
        self.reject_b2c(
            r"ABSENT_RECORD\(ipflux,'SPOT-R64'\)",
            "ABSENT_RECORD(ipflux,'SPOT -R64')",
        )

    def test_spot_epoch_lowercase_is_rejected(self) -> None:
        self.reject_b2c(
            r"ABSENT_RECORD\(ipflux,'SPOT-R64'\)",
            "ABSENT_RECORD(ipflux,'spot-r64')",
        )

    def test_sour_epoch_embedded_spaces_are_rejected(self) -> None:
        self.reject_b2c(
            r"ABSENT_RECORD\(ipflux,'SOUR'\)",
            "ABSENT_RECORD(ipflux,'S O U R')",
        )

    def test_sour_epoch_lowercase_is_rejected(self) -> None:
        self.reject_b2c(
            r"ABSENT_RECORD\(ipflux,'SOUR'\)",
            "ABSENT_RECORD(ipflux,'sour')",
        )

    def test_b2c_option_embedded_space_is_rejected(self) -> None:
        self.reject_b2c(r"coptio\s*/=\s*'B0  '", "coptio /= 'B 0 '")

    def test_b2c_option_lowercase_is_rejected(self) -> None:
        self.reject_b2c(r"coptio\s*/=\s*'B0  '", "coptio /= 'b0  '")

    def test_macro_name_embedded_spaces_are_rejected(self) -> None:
        self.reject_b2c(
            r"macro_name\s*/=\s*'MACRO0'", "macro_name /= 'M A C R O 0'"
        )

    def test_macro_name_lowercase_is_rejected(self) -> None:
        self.reject_b2c(
            r"macro_name\s*/=\s*'MACRO0'", "macro_name /= 'macro0'"
        )

    def test_b2b_option_embedded_space_is_rejected(self) -> None:
        self.reject_b2b(r"coptio\s*/=\s*'B0  '", "coptio /= 'B 0 '")

    def test_b2b_option_lowercase_is_rejected(self) -> None:
        self.reject_b2b(r"coptio\s*/=\s*'B0  '", "coptio /= 'b0  '")


class ManifestHardeningMutations(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = gate.json.loads(gate.MANIFEST.read_text())

    def rejected(self, path: tuple[str, ...], value: object) -> None:
        data = copy.deepcopy(self.manifest)
        cursor = data
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = value
        with self.assertRaises(gate.ContractError):
            gate.check_manifest(data)

    def test_completion_marker_claim(self) -> None:
        self.rejected(("publication_contract", "completion_marker"), True)

    def test_collision_policy_drift(self) -> None:
        self.rejected(("publication_contract", "collision_policy"), "status 5")

    def test_epoch_policy_cannot_omit_adjoint_lists(self) -> None:
        self.rejected(
            ("publication_contract", "epoch_policy"),
            "single epoch; SPOT-R64 and root SOUR must be absent",
        )

    def test_ordered_owner_refinement_drift(self) -> None:
        self.rejected(("ordered_owner_refinement", "a9b_implementation"), "three routines")

    def test_runtime_provenance_claim(self) -> None:
        self.rejected(("status", "runtime_provenance_validated"), True)

    def test_actual_transport_claim(self) -> None:
        self.rejected(("status", "actual_transport_response_validated"), True)

    def test_solver_execution_authorization_claim(self) -> None:
        self.rejected(("status", "production_solver_execution_authorized"), True)

    def test_relaxation_claim(self) -> None:
        self.rejected(("status", "relaxation_parameters_added"), True)

    def test_empirical_parameter_claim(self) -> None:
        self.rejected(("status", "empirical_parameters_added"), True)

    def test_tracking_read_claim(self) -> None:
        self.rejected(("status", "validation_tracking_stream_reads"), 1)

    def test_transport_solve_claim(self) -> None:
        self.rejected(("status", "validation_transport_solves"), 1)

    def test_dragon_run_claim(self) -> None:
        self.rejected(("status", "dragon_runs"), 1)

    def test_radial_convergence_claim(self) -> None:
        self.rejected(("status", "radial_convergence"), "CONVERGED")

    def test_mutation_count_drift(self) -> None:
        self.rejected(("validation_evidence", "mutation_tests"), 999)

    def test_real_link_archive_inventory_drift(self) -> None:
        data = copy.deepcopy(self.manifest)
        data["production_publisher_link_archives"] = [
            "Ganlib/lib/Darwin_arm64/libGanlib.a"
        ]
        with self.assertRaises(gate.ContractError):
            gate.check_manifest(data)


class ReceiptHardeningMutations(unittest.TestCase):
    @staticmethod
    def receipt_lines() -> list[str]:
        return ["0" * 64 + "  " + path for path in gate.EXPECTED_RECEIPT_PATHS]

    def rejected(self, lines: list[str]) -> None:
        with self.assertRaises(gate.ContractError):
            gate.check_receipt("\n".join(lines) + "\n", verify_digests=False)

    def test_receipt_reordering_is_rejected(self) -> None:
        lines = self.receipt_lines()
        lines[0], lines[1] = lines[1], lines[0]
        self.rejected(lines)

    def test_receipt_missing_path_is_rejected(self) -> None:
        self.rejected(self.receipt_lines()[:-1])

    def test_receipt_extra_path_is_rejected(self) -> None:
        self.rejected(self.receipt_lines() + ["0" * 64 + "  rogue"])


if __name__ == "__main__":
    unittest.main()
