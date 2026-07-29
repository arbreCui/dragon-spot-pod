#!/usr/bin/env python3
"""Fail-closed checker for the Phase-A5 private population path."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
IMPLEMENTATION = HERE / "SPOR64_A5.f90"
MANIFEST = HERE / "precision_manifest.json"
RUNNER = HERE / "run_phase_a5.sh"
RECEIPT = HERE / "phase_a5_implementation_receipt.sha256"
BASELINE_COMMIT = "d66faf70aab96696261788efe0aa02cf18cd0e17"

# Filled only after the implementation, manifest, and runner have stopped
# changing.  Leaving either digest empty deliberately makes the full checker
# fail closed while source and mutation tests are being assembled.
EXPECTED_IMPLEMENTATION_SHA256 = (
    "bcd8d6f59da4f7ea5f2be2c631ca31efe7b0cf2e70b8717c2d0a683d83ff42e7"
)
EXPECTED_CANONICAL_SHA256 = (
    "8381884bebd41a58dd2d9cbd220a77596a0ffaa8caa0613631d94a5ee920d911"
)
EXPECTED_RUNNER_SHA256 = (
    "1ae3aa81bd8260b43ef1e95e060938c3ef6d7372df5238d126a06f1066a10bf9"
)

PUBLIC_PROCEDURE = (
    "MCGFL1R64_HOST_SHAPED_POPULATION_COMPILE_ONLY_LOCKED"
)
A4_PROCEDURE = "MCGFL1R64_A2_A3_HOST_CLOSURE_COMPILE_ONLY_LOCKED"

REQUIRED_CHECKED_FLAGS = [
    "-std=f2008",
    "-pedantic-errors",
    "-Werror",
    "-Wimplicit-interface",
    "-Wimplicit-procedure",
    "-Wconversion-extra",
    "-Warray-temporaries",
    "-fimplicit-none",
    "-fcheck=all",
    "-ffp-contract=off",
    "-fno-fast-math",
]

EXPECTED_STATUS = {
    "classification":
        "IMPLEMENTED-COMPILE-ONLY-LOCKED-CONTEXT-POPULATION-PATH",
    "phase_a_static_closure": False,
    "compile_only": True,
    "link_authorized": False,
    "execution_authorized": False,
    "context_storage_schema_closed": True,
    "context_population_checked": True,
    "context_population_check_scope": "STATIC-A5-PRIVATE-PATH-ONLY",
    "context_population_executed": False,
    "field_lexical_source_map_checked": True,
    "locked_inactive_formals_canonically_defined": True,
    "a5_path_population_kind_checked": True,
    "real_context_provenance_bound": False,
    "runtime_object_provenance_validated": False,
    "carrier_proves_provenance": False,
    "public_A4_population_exclusive": False,
    "current_MCGFL1_callsite_bound": False,
    "production_REAL64_host_inputs_bound": False,
    "tracking_position_validated": False,
    "real_KPSYS_PJJ_directories_bound": False,
    "EXP1_identity_bound": False,
    "actual_moc_response_validated": False,
    "continuous_real64_lane": False,
    "production_route_connected": False,
    "default_runtime_route_changed": False,
    "transport_solves": 0,
    "dragon_processes_authorized": 0,
    "stage4_qualified": False,
    "stage5_authorized": False,
    "outer_convergence": "NOT-EVALUATED",
}

EXPECTED_LOCKED_BRANCH = {
    "calculation_type": "S",
    "door": "MCCG",
    "NDIM": 2,
    "K": 14,
    "KPN": 14,
    "NREG": 8,
    "NSOUT": 6,
    "groups": 370,
    "NANI": 1,
    "NLF": 1,
    "NFUNL": 1,
    "NMOD": 4,
    "NLFX": 1,
    "NLIN": 1,
    "NFUNLX": 1,
    "STIS": 1,
    "NPJJM": 1,
    "IDIR": 0,
    "CYCLIC": False,
    "LPRISM": False,
    "NGIND": "STRICTLY-CONSECUTIVE-TAIL-ENDING-AT-370",
    "NCONV_true_meaning": "ACTIVE-NOT-CONVERGED",
    "active_subset": "NONEMPTY-ARBITRARY-NONCONTIGUOUS-MASK",
}

EXPECTED_POPULATION_CONTRACT = {
    "public_context_argument": False,
    "public_context_result": False,
    "local_context_initial_enabled": False,
    "private_population_procedure": "populate_context",
    "A4_calls": 1,
    "A4_call_only_after_population_OK": True,
    "enabled_true_assignments": 1,
    "enabled_true_immediately_before_A4": True,
    "enabled_reset_after_A4": True,
    "context_escapes": False,
    "context_SAVE_or_COMMON": False,
    "copied_scalars": {
        "context%iftrak": "iftrak",
        "context%nbtr": "nbtr",
        "context%nmax": "n2max",
        "context%nbatch": "nbatch",
    },
    "copied_arrays": {
        "context%kpsys": "kpsys",
        "context%caz1": "caz1",
        "context%caz2": "caz2",
        "context%zmu": "zmu",
        "context%wzmu": "wzmu",
        "context%volume": "volume",
    },
    "locked_storage_definitions": {
        "context%caz0":
            "CANONICAL-DEFINED-0.0_real64; UNREAD-WHEN-NDIM-2",
        "context%cpo":
            "CANONICAL-DEFINED-0.0_real32; "
            "VALUES-UNREAD-IN-ISOTROPIC-2D",
        "context%xsi":
            "CANONICAL-DEFINED-0.0_real64; UNREAD-WHEN-IDIR-0",
        "context%isgnr": "INTEGER-ONE; EXACT-MOCIK3-ORDER-ZERO-NMOD-4",
        "context%pjjind": "INTEGER-ONE; EXACT-ISOTROPIC-MCGPJJ-PAIR",
    },
    "defined_zero_is_physical_coefficient": False,
    "empirical_coefficients_added": 0,
    "relaxation_or_acceleration_added": False,
    "threshold_or_tolerance_added": False,
    "interpolation_fit_clip_or_model_added": False,
    "A5_staging_matrices": 0,
    "binary64_to_binary32_mutable_state_conversion": False,
    "KPSYS_container_owned": True,
    "KPSYS_pointees_owned": False,
    "active_KPSYS_nonnull_checked": True,
    "active_KPSYS_directory_contents_checked": False,
    "adapter_performs_IO_or_LCM": False,
}

EXPECTED_PROVENANCE_BOUNDARY = {
    "lexical_host_source_map_closed": True,
    "private_population_encoded": True,
    "runtime_population_executed": False,
    "real_context_provenance_bound": False,
    "IFTRAK_open_identity_bound": False,
    "IFTRAK_first_track_position_bound": False,
    "IFTRAK_IPTRK_pair_identity_bound": False,
    "KPSYS_pointee_lifetime_bound": False,
    "KPSYS_group_order_bound": False,
    "KPSYS_PJJ_record_identity_bound": False,
    "SC_SIGAL_KPSYS_geometry_material_identity_bound": False,
    "EXP1_same_image_epoch_bound": False,
    "production_QFR_PHIIN_REAL64": False,
    "production_host_callsite_bound": False,
    "tracking_stream_double_consumption_prevented": False,
    "legal_XSI_storage_is_production_fix": False,
}

EXPECTED_SOURCE_HASHES = {
    "validation/iterative/real64_phase_a1/SPOR64_A1.f90":
        "13f341a99fa99c21ff34821339d0347565489134379193a1bfcf58dfa65726da",
    "validation/iterative/real64_phase_a2/SPOR64_A2.f90":
        "9c0d209d29d99a910559e3b207d98ec466be751a8d7aa56e040fb382989579c2",
    "validation/iterative/real64_phase_a3/SPOR64_A3.f90":
        "3d8d9ebb2417f0c2139b88ecee157bcf16fa189e6f87e5dd6e76df8058f05ccc",
    "validation/iterative/real64_phase_a4/SPOR64_A4.f90":
        "a656aac0b3a11a5610c4724ab67b3e66c1cdd0f0a0b7043fdec324b577c27fe8",
}
EXPECTED_PREREQUISITE_RECEIPTS = {
    "validation/iterative/real64_phase_a4/"
    "phase_a4_implementation_receipt.sha256":
        "2b0388b94374feace3bb70ad2be595f12c16db434633bbf4f0efe9869996b291",
}
EXPECTED_LEGACY_HASHES = {
    "src/MCGFL1.f":
        "6701db8972bd92e339d99879787a126f1ce38b72936852ba331259877894df9f",
    "src/MCGFCF.f":
        "60c841dbd2a0a2de2023de8a424b0162bc9898c5c5b877cc4d59f5b892b0deb9",
    "src/MCGFFIR.f":
        "b0400eb5211b5551f86f02608aa122e1301f38996c576dde818834da851cec6b",
    "src/MOCIK3.f":
        "5193a5a8a4922f4c20b34fae19f1d1278722c31c33dae143bf970b7e2595e007",
    "src/MCGPJJ.f":
        "b695949d91921778a7fbe9e1a377057e87d821b8d2cd8027de9413ccfcc36de2",
    "src/MCGFST.f":
        "bda4ec2376d91e5cf12427288c6bc1c565980cf916639937dca21ad7ad62b5e3",
    "src/MCGSCA.f":
        "fb16fe47c842d3a8c6e8726efb05195ce47ec88c6fdf6c00c65a91a3573a0159",
    "src/MCCGF.f":
        "621fba6d02d1b1efae2d6d6db8e61d1463a3a24bcf4d0efe3579bfba97c55546",
    "src/DOORFV.f":
        "630f84ba8c738e520e471f63f67e2a9813bc9723d3e7ec30db59e478579b0a8d",
    "src/FLU.f":
        "f9391eb48be9ab1f8d9c3250a23409de2dcfb6111d22db283d1c29d030d26fd0",
    "src/XDRTA2.f":
        "625f5738da3ecc62b82ef29217111c2e789bd853e392ae6ecbe7c2c64e456fff",
}

EXPECTED_HOST_SOURCE_MAP = {
    "iftrak": "MCGFL1 dummy; borrowed sequential unit",
    "nbtr": "MCGFL1 tracking-header local",
    "nmax": "MCGFL1 N2MAX under LPRISM=false",
    "nbatch": "MCGFL1 dummy from MCCGF state-vector normalization",
    "kpsys": "MCGFL1 C_PTR dummy array selected by DOORFV",
    "caz1_caz2":
        "MCGFL1 host arrays initialized by locked MCCGF 2D branch",
    "zmu_wzmu_volume": "MCGFL1 host arrays borrowed from IPTRK",
    "caz0": "structural storage only; MCGFCF 2D branch does not read",
    "cpo":
        "structural length storage; locked MCGFCF values are not read",
    "xsi": "legal structural storage; MCGFFIR IDIR=0 does not read",
    "isgnr": "exact frozen MOCIK3 order-zero sign table",
    "pjjind": "exact frozen MCGPJJ isotropic pair",
}

EXPECTED_CALL_BOUNDARY = {
    "allowed_direct_module_call": A4_PROCEDURE,
    "direct_A2_calls": 0,
    "direct_A3_calls": 0,
    "direct_legacy_calls": 0,
    "link_barrier_owner": "PHASE-A3",
    "link_barrier_count": 1,
    "A5_link_barriers": 0,
    "production_callers": 0,
}

EXPECTED_REMAINING_OPEN_PATH = [
    "production-default-off host callsite without changing the legacy default",
    "runtime IFTRAK open identity and exact first-track positioning",
    "live KPSYS lifetime group ordering and PJJ$MCCG preflight",
    "IFTRAK IPTRK KPSYS cross-object identity",
    "EXP1 initialization epoch in the same process image",
    "SC SIGAL KPSYS NZON VOLUME geometry material and group-order identity",
    "continuous REAL64 QFR PHIIN source and terminal-state host lane",
    "separately authorized removal of the Phase-A3 link barrier",
    "one bounded primary-response execution and independent replay",
    "MCGFCA MCGFCR and live ACA correction",
    "MCGABG cutoff instrumentation",
    "MCGMRE correction accumulation and terminal norm",
    "MCCGF and DOORFV active-group routing",
    "FLU2DR eight-slice mutable state and terminal norms",
    "FLUBAL and FLU2AC binary64 updates",
    "type-4 authoritative archive and terminal type-2 adapter",
]

EXPECTED_INTERPRETATION = [
    "Phase-A5 closes only the private static population path for the "
    "exact locked host shape.",
    "The structural zeros are defined values for unread legacy formals, "
    "and the integer ones are exact frozen discrete identities; none is "
    "an empirical coefficient.",
    "Copying a file-unit integer or C address does not establish an open "
    "stream, record position, pointee lifetime, LCM directory contents, "
    "or cross-object identity.",
    "No A5 or prerequisite object is linked or executed by this gate, "
    "no real MOC response is evaluated, and no production route is changed.",
    "No physical accuracy, radial convergence, Stage-4 qualification, "
    "or Picard trajectory is established.",
]

# The final receipt may add hash-locked production evidence before release.
# Its exact ordered list is validated once present; no globbing is allowed.
EXPECTED_RECEIPT_PATHS = [
    "validation/iterative/real64_phase_a1/SPOR64_A1.f90",
    "validation/iterative/real64_phase_a2/SPOR64_A2.f90",
    "validation/iterative/real64_phase_a3/SPOR64_A3.f90",
    "validation/iterative/real64_phase_a4/SPOR64_A4.f90",
    "validation/iterative/real64_phase_a4/"
    "phase_a4_implementation_receipt.sha256",
    "src/MCGFL1.f",
    "src/MCGFCF.f",
    "src/MCGFFIR.f",
    "src/MOCIK3.f",
    "src/MCGPJJ.f",
    "src/MCGFST.f",
    "src/MCGSCA.f",
    "src/MCCGF.f",
    "src/DOORFV.f",
    "src/FLU.f",
    "src/XDRTA2.f",
    "validation/iterative/real64_phase_a5/README.md",
    "validation/iterative/real64_phase_a5/SPOR64_A5.f90",
    "validation/iterative/real64_phase_a5/compile_spor64_a5_anchor.f90",
    "validation/iterative/real64_phase_a5/"
    "compile_fail_real32_lane.f90",
    "validation/iterative/real64_phase_a5/"
    "compile_fail_integer_kpsys.f90",
    "validation/iterative/real64_phase_a5/"
    "compile_fail_real32_caz.f90",
    "validation/iterative/real64_phase_a5/"
    "compile_fail_real64_operator_data.f90",
    "validation/iterative/real64_phase_a5/"
    "compile_fail_noncontiguous_population_actual.f90",
    "validation/iterative/real64_phase_a5/precision_manifest.json",
    "validation/iterative/real64_phase_a5/check_phase_a5.py",
    "validation/iterative/real64_phase_a5/test_phase_a5_contract.py",
    "validation/iterative/real64_phase_a5/run_phase_a5.sh",
]


class PhaseA5Error(RuntimeError):
    """Raised when the Phase-A5 contract is not exact."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise PhaseA5Error(message)


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_sha256(data: dict[str, Any]) -> str:
    encoded = json.dumps(data, sort_keys=True, separators=(",", ":")).encode()
    return sha256_bytes(encoded)


def git_blob(commit: str, relative_path: str) -> bytes:
    result = subprocess.run(
        ["git", "show", f"{commit}:{relative_path}"],
        cwd=ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    require(
        result.returncode == 0,
        f"cannot read baseline blob {relative_path}: "
        f"{result.stderr.decode(errors='replace').strip()}",
    )
    return result.stdout


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise PhaseA5Error(f"cannot load manifest: {exc}") from exc
    require(isinstance(data, dict), "manifest root must be an object")
    return data


def normalize_fortran(text: str) -> str:
    return re.sub(r"[\s&]+", "", text.lower())


def extract_subroutine(source: str, name: str) -> str:
    match = re.search(
        rf"(?ims)^\s*subroutine\s+{re.escape(name)}\b"
        rf".*?^\s*end\s+subroutine\s+{re.escape(name)}\s*$",
        source,
    )
    require(match is not None, f"missing subroutine {name}")
    return match.group(0)


def validate_makefile_contract(makefile: str) -> None:
    phase_a5_block = (
        ".PHONY: spot-real64-phase-a5\n"
        "spot-real64-phase-a5 :\n"
        "\tsh validation/iterative/real64_phase_a5/run_phase_a5.sh\n"
    )
    require(
        makefile.count(phase_a5_block) == 1,
        "exact isolated Phase-A5 Makefile block",
    )
    baseline = git_blob(BASELINE_COMMIT, "Makefile").decode()
    require(
        makefile.replace(phase_a5_block, "", 1) == baseline,
        "Makefile differs from baseline beyond exact Phase-A5 block",
    )
    target = re.search(
        r"(?m)^spot-real64-phase-a5\s*:(?P<prerequisites>[^\n]*)\n"
        r"(?P<recipes>(?:\t[^\n]*(?:\n|$))*)",
        makefile,
    )
    require(target is not None, "missing Phase-A5 target")
    require(
        target.group("prerequisites").strip() == "",
        "Phase-A5 target has prerequisite",
    )
    require(
        target.group("recipes").splitlines()
        == ["\tsh validation/iterative/real64_phase_a5/run_phase_a5.sh"],
        "Phase-A5 recipe is not exact",
    )
    ordinary = re.findall(
        r"(?m)^([A-Za-z][A-Za-z0-9_.-]*)\s*:",
        makefile,
    )
    require(ordinary and ordinary[0] == "all", "default Make target changed")
    for target_name in ("all", "tests", "spot-fast"):
        dependency = re.search(
            rf"(?m)^{re.escape(target_name)}\s*:(.*)$",
            makefile,
        )
        require(dependency is not None, f"missing Make target {target_name}")
        require(
            "spot-real64-phase-a5" not in dependency.group(1),
            f"Phase-A5 added to {target_name}",
        )


def validate_implementation_source(source: str) -> None:
    lower = source.lower()
    normalized = normalize_fortran(source)
    require(
        re.search(r"(?im)^\s*module\s+spor64_a5\s*$", source) is not None,
        "module name",
    )
    require(
        re.search(r"(?im)^\s*implicit\s+none\s*$", source) is not None,
        "implicit none",
    )
    require(
        len(re.findall(r"(?im)^\s*private\s*$", source)) == 1,
        "module default privacy",
    )
    require(
        lower.count(
            "public :: "
            "mcgfl1r64_host_shaped_population_compile_only_locked"
        )
        == 1,
        "single public A5 procedure",
    )
    require(
        re.search(r"(?im)^\s*public\s*::[^\n]*populate_context", source)
        is None,
        "population helper exposed",
    )
    require(
        "type(spor64_a4_context) :: context" in lower,
        "wrapper-local A4 context",
    )
    require(
        "type(spor64_a4_context), intent(out) :: context" in lower,
        "private population output context",
    )

    wrapper = extract_subroutine(source, PUBLIC_PROCEDURE)
    helper = extract_subroutine(source, "populate_context")
    wrapper_lower = wrapper.lower()
    helper_lower = helper.lower()
    require(
        "context" not in wrapper.split(")", 1)[0].lower(),
        "context escaped through public wrapper signature",
    )
    require(
        len(re.findall(r"(?im)^\s*call\s+", source)) == 2,
        "A5 call count",
    )
    require(
        len(re.findall(r"(?im)^\s*call\s+populate_context\b", source)) == 1,
        "population call count",
    )
    require(
        len(
            re.findall(
                rf"(?im)^\s*call\s+{re.escape(A4_PROCEDURE)}\b",
                source,
            )
        )
        == 1,
        "A4 call count",
    )
    for forbidden_call in (
        "MCGFL1R64_POST_STIS_RAW_FACADE_LOCKED",
        "MCGFCF_MCGFST_R64_COMPILE_ONLY_LOCKED",
        "MCGFCF", "MCGFST", "MCGFCS", "MCGSCA", "MCGFFIR",
    ):
        require(
            re.search(
                rf"(?im)^\s*call\s+{re.escape(forbidden_call)}\b",
                source,
            )
            is None,
            f"direct forbidden call: {forbidden_call}",
        )

    for exact_guard in (
        "if (n /= 14 .or. ndim /= 2 .or. kpn /= 14 .or. nreg /= 8) "
        "return",
        "if (nani /= 1 .or. nlin /= 1 .or. nfunl /= 1 .or. stis /= 1) "
        "return",
        "if (idir /= 0 .or. ng /= 370 .or. cyclic .or. lprism) return",
        "if (m < 0 .or. ngeff <= 0 .or. ngeff > ng) return",
        "if (iftrak <= 0 .or. nbtr <= 0 .or. n2max <= 0) return",
        "if (nbatch <= 0) return",
        "if (size(ngind) /= ngeff .or. size(nconv) /= ngeff) return",
        "if (size(kpsys) /= ngeff) return",
        "if (size(caz1) <= 0 .or. size(caz2) /= size(caz1)) return",
        "if (size(zmu) <= 0 .or. size(wzmu) /= size(zmu)) return",
        "if (size(volume) /= n) return",
        "if (.not. any(nconv)) return",
        "if (ngind(1) /= ng-ngeff+1 .or. ngind(ngeff) /= ng) return",
        "if (nconv(group) .and. .not. c_associated(kpsys(group))) return",
    ):
        require(exact_guard in wrapper_lower, f"locked guard: {exact_guard}")
    require(
        normalize_fortran(
            "do group = 2, ngeff\n"
            "if (ngind(group) /= ngind(group-1)+1) return\n"
            "end do"
        )
        in normalize_fortran(wrapper),
        "strictly consecutive NGIND loop",
    )
    require(
        normalize_fortran(
            "do group = 1, ngeff\n"
            "if (nconv(group) .and. "
            ".not. c_associated(kpsys(group))) return\n"
            "end do"
        )
        in normalize_fortran(wrapper),
        "active KPSYS association loop",
    )

    populate_call = (
        "callpopulate_context(iftrak,nbtr,n2max,nbatch,kpsys,caz1,"
        "caz2,zmu,wzmu,volume,n-nreg,context,population_status)"
    )
    require(populate_call in normalize_fortran(wrapper), "exact population call")
    a4_call = (
        "callmcgfl1r64_a2_a3_host_closure_compile_only_locked("
        "n,ndim,nzon,qn,fi,m,nani,nlin,nfunl,sc,source,kpn,nreg,keyflx,"
        "keycur,ibc,sigal,stis,cyclic,lprism,idir,ng,ngeff,ngind,nconv,"
        "context,raw_response,status)"
    )
    require(a4_call in normalize_fortran(wrapper), "exact A4 actual list")

    initial_false = wrapper_lower.index("context%enabled = .false.")
    population = wrapper_lower.index("call populate_context")
    population_check = wrapper_lower.index(
        "if (population_status /= spor64_a5_ok) then"
    )
    enable_true = wrapper_lower.index("context%enabled = .true.")
    a4_position = wrapper_lower.index("call " + A4_PROCEDURE.lower())
    reset_false = wrapper_lower.rindex("context%enabled = .false.")
    require(
        initial_false < population < population_check < enable_true
        < a4_position < reset_false,
        "context enable/call/reset order",
    )
    require(
        wrapper_lower.count("context%enabled = .true.") == 1,
        "context true count",
    )
    require(
        wrapper_lower.count("context%enabled = .false.") == 2,
        "wrapper false count",
    )
    require(
        "status = spor64_a5_ok" not in wrapper_lower,
        "wrapper forges success",
    )

    allocation = (
        "allocate(context%isgnr(4,1),context%pjjind(1,2),"
        "context%kpsys(size(kpsys)),context%cpo(size(zmu)),"
        "context%zmu(size(zmu)),context%wzmu(size(wzmu)),"
        "context%volume(size(volume)),context%caz0(size(caz1)),"
        "context%caz1(size(caz1)),context%caz2(size(caz2)),"
        "context%xsi(nsout),stat=allocation_status)"
    )
    require(allocation in normalize_fortran(helper), "exact context allocation")
    require(
        helper_lower.count("context%enabled = .false.") == 1,
        "helper disabled context",
    )
    require(
        "if (allocation_status /= 0) return" in helper_lower,
        "allocation status check",
    )

    expected_assignments = {
        "iftrak": "iftrak",
        "nbtr": "nbtr",
        "nmax": "n2max",
        "nbatch": "nbatch",
        "kpsys": "kpsys",
        "caz1": "caz1",
        "caz2": "caz2",
        "zmu": "zmu",
        "wzmu": "wzmu",
        "volume": "volume",
        "caz0": "0.0_real64",
        "cpo": "0.0_real32",
        "xsi": "0.0_real64",
        "isgnr": "1",
        "pjjind": "1",
    }
    assignments = re.findall(
        r"(?im)^\s*context%([a-z0-9_]+)\s*=(?!=)\s*([^\n]+?)\s*$",
        helper,
    )
    actual_assignments = {
        name.lower(): value.strip().lower() for name, value in assignments
    }
    require(
        actual_assignments
        == {"enabled": ".false.", **expected_assignments},
        "context population assignment set",
    )
    require(
        len(assignments) == len(actual_assignments),
        "duplicate context population assignment",
    )
    require(
        helper_lower.rstrip().endswith("end subroutine populate_context"),
        "helper ending",
    )
    ok_position = helper_lower.index("status = spor64_a5_ok")
    for name in expected_assignments:
        require(
            helper_lower.index(f"context%{name} =") < ok_position,
            f"success before population: {name}",
        )

    require(
        re.search(r"(?im)^\s*(source|raw_response)\s*=(?!=)", source)
        is None,
        "direct SOURCE or RAW_RESPONSE assignment",
    )
    require(
        re.search(r"(?im)^\s*(real|integer|logical|type)\b[^\n]*\bsave\b",
                  source)
        is None,
        "SAVE state",
    )
    require(
        re.search(r"(?im)^\s*common\b", source) is None,
        "COMMON state",
    )
    require(
        re.search(r"(?im)^\s*(real|integer|logical|type)\b[^\n]*\bpointer\b",
                  source)
        is None,
        "Fortran pointer state",
    )
    for token in (
        "read", "rewind", "open", "close", "write", "print", "inquire",
        "backspace", "endfile", "flush", "wait", "format", "lcmget",
        "lcmgpd", "lcmlen", "lcmsix", "c_f_pointer",
    ):
        require(
            re.search(rf"(?im)^\s*{re.escape(token)}\b", source) is None,
            f"forbidden I/O or LCM operation: {token}",
        )
    for token in (
        "relax", "aitken", "anderson", "damping", "alpha", "tolerance",
        "threshold", "clip", "fitted", "empirical",
    ):
        require(
            re.search(rf"(?i)\b{re.escape(token)}\b", source) is None,
            f"empirical mechanism: {token}",
        )
    for token in ("reshape", "pack", "unpack", "transfer"):
        require(token not in lower, f"forbidden population transform: {token}")
    require(
        re.search(r"(?i)=\s*real\s*\(", source) is None,
        "explicit precision conversion",
    )
    require(
        "spor64_a3_compile_only_link_forbidden" not in lower,
        "A5 duplicates the A3 barrier",
    )
    require(
        normalized.count("context%enabled=.true.") == 1,
        "normalized enable count",
    )


def validate_runner_contract(
    runner: str,
    *,
    verify_hash: bool = True,
    expected_counts: dict[str, int] | None = None,
) -> None:
    if verify_hash:
        require(bool(EXPECTED_RUNNER_SHA256), "runner hash is not frozen")
        require(
            sha256_bytes(runner.encode()) == EXPECTED_RUNNER_SHA256,
            "runner hash mismatch",
        )
    lower = runner.lower()
    for old_runner in (
        "run_phase_a1.sh", "run_phase_a2.sh",
        "run_phase_a3.sh", "run_phase_a4.sh",
    ):
        require(old_runner not in lower, f"old runner invoked: {old_runner}")
    for token in (
        "phase_a4_implementation_receipt.sha256",
        "phase_a5_implementation_receipt.sha256",
        "check_phase_a5.py",
        "test_phase_a5_contract",
        "SPOR64_A1.f90", "SPOR64_A2.f90", "SPOR64_A3.f90",
        "SPOR64_A4.f90", "SPOR64_A5.f90",
        "compile_spor64_a5_anchor.f90",
        "a3_unresolved.log", "a4_unresolved.log",
        "a5_unresolved.log", "anchor_unresolved.log",
        "SPOR64_A3_COMPILE_ONLY_LINK_FORBIDDEN",
    ):
        require(token.lower() in lower, f"runner token: {token}")
    for flag in REQUIRED_CHECKED_FLAGS:
        require(flag in runner, f"runner flag: {flag}")
    for token in (
        "LC_ALL=C",
        'EXPECTED_FC_BANNER="GNU Fortran (Homebrew GCC 15.2.0_1) 15.2.0"',
        'test "$(uname -s)" != Darwin',
        'test "$(uname -m)" != arm64',
    ):
        require(token in runner, f"audited toolchain gate: {token}")

    logical_runner = re.sub(r"\\\n\s*", " ", runner)
    fc_commands = [
        line.strip()
        for line in logical_runner.splitlines()
        if re.search(r'^\s*"?\$FC"?(\s|$)', line)
    ]
    require(fc_commands, "no compiler commands")
    for command in fc_commands:
        require(" -c " in f" {command} ", f"non-object compiler command: {command}")
        require(
            not re.search(r"(?i)(^|\s)(-o\s+)?[^\s]*test_spor64[^\s]*$", command),
            "compiler builds executable",
        )
    for pattern in (
        r"(?im)^\s*(ld|ar|ranlib)\b",
        r"(?im)^\s*(?:command\s+)?"
        r"(?:[\"']?/[^ \t\n\"']*/)?"
        r"(?:gfortran(?:-[0-9.]+)?|ifort|ifx|flang|nvfortran|f90|f95)"
        r"[\"']?(?:\s|$)",
        r"(?im)^\s*(?:\"[^\"]*/)?(?:rdragon|dragon)(?:\"|\s)",
        r"(?im)^\s*\"\$ROOT/[^\"]*/(?:Dragon|rdragon)\"",
        r"(?im)^\s*make\s+-c\s+src\b",
    ):
        require(re.search(pattern, runner) is None, "link or execution command")
    for line in logical_runner.splitlines():
        artifact = re.match(
            r'^\s*["\']?\$BUILD_DIR/(?P<name>[^ \t"\']+)["\']?\s*$',
            line,
        )
        require(artifact is None, "build artifact executed")
    require(
        re.search(r"(?im)^\s*program\b", runner) is None,
        "runner embeds program",
    )

    if expected_counts is not None:
        for stem, count in expected_counts.items():
            token = f'{stem}_unresolved.log")" -ne {count}'
            require(token in runner, f"exact unresolved count: {stem}")
    require(
        re.search(
            r"(?i)\btransport-(?:solves|applications)=0\b",
            runner,
        )
        is not None,
        "zero transport declaration",
    )
    require(
        re.search(r"(?i)\bdragon-runs=0\b", runner) is not None,
        "zero Dragon declaration",
    )


def validate_scoped_receipt() -> None:
    require(RECEIPT.is_file(), "missing receipt")
    entries: dict[str, str] = {}
    for line in RECEIPT.read_text().splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\s].*)", line)
        require(match is not None, "malformed receipt line")
        digest, relative = match.groups()
        require(relative not in entries, f"duplicate receipt path: {relative}")
        entries[relative] = digest
    require(
        list(entries) == EXPECTED_RECEIPT_PATHS,
        "receipt scope or order mismatch",
    )
    for relative, expected in entries.items():
        require(
            sha256_file(ROOT / relative) == expected,
            f"receipt mismatch: {relative}",
        )


def validate(data: dict[str, Any], *, verify_canonical: bool = True) -> None:
    if verify_canonical:
        require(
            bool(EXPECTED_CANONICAL_SHA256),
            "canonical manifest hash is not frozen",
        )
        require(
            canonical_sha256(data) == EXPECTED_CANONICAL_SHA256,
            "canonical manifest hash mismatch",
        )
    require(
        data["schema"]
        == "spot-radial-real64-phase-a5-compile-only-private-host-shaped-"
           "population-v1",
        "schema",
    )
    require(
        data["title"]
        == "Compile-only REAL64 private host-shaped context population",
        "title",
    )
    require(data["status"] == EXPECTED_STATUS, "status or authorization")
    baseline = data["baseline"]
    require(baseline["commit"] == BASELINE_COMMIT, "baseline commit")
    require(
        baseline["source_sha256"] == EXPECTED_SOURCE_HASHES,
        "prerequisite source hash map",
    )
    require(
        baseline["prerequisite_receipt_sha256"]
        == EXPECTED_PREREQUISITE_RECEIPTS,
        "prerequisite receipt hash map",
    )
    require(
        baseline["legacy_source_sha256"] == EXPECTED_LEGACY_HASHES,
        "legacy evidence hash map",
    )
    for relative, expected in {
        **EXPECTED_SOURCE_HASHES,
        **EXPECTED_PREREQUISITE_RECEIPTS,
        **EXPECTED_LEGACY_HASHES,
    }.items():
        require(
            sha256_bytes(git_blob(BASELINE_COMMIT, relative)) == expected,
            f"baseline evidence mismatch: {relative}",
        )
        require(
            sha256_file(ROOT / relative) == expected,
            f"live evidence changed: {relative}",
        )
    require(data["locked_branch"] == EXPECTED_LOCKED_BRANCH, "locked branch")
    require(
        data["population_contract"] == EXPECTED_POPULATION_CONTRACT,
        "population contract",
    )
    require(
        data["provenance_boundary"] == EXPECTED_PROVENANCE_BOUNDARY,
        "provenance boundary",
    )
    require(
        data["host_source_map"] == EXPECTED_HOST_SOURCE_MAP,
        "host source map",
    )
    require(
        data["call_boundary"] == EXPECTED_CALL_BOUNDARY,
        "call boundary",
    )

    implementation = data["implementation"]
    require(
        implementation["location"]
        == "validation/iterative/real64_phase_a5/SPOR64_A5.f90",
        "implementation path",
    )
    require(implementation["module"] == "SPOR64_A5", "module")
    require(implementation["procedure"] == PUBLIC_PROCEDURE, "procedure")
    require(
        implementation["context_type"] == "SPOR64_A4_CONTEXT",
        "context type",
    )
    require(
        implementation["context_visibility"] == "LOCAL-A5-ACTIVATION-ONLY",
        "context visibility",
    )
    require(
        implementation["sha256"] == EXPECTED_IMPLEMENTATION_SHA256,
        "implementation digest field",
    )
    require(implementation["validation_tree_only"] is True, "tree scope")
    require(
        implementation["included_by_src_wildcard_build"] is False,
        "production wildcard inclusion",
    )
    require(implementation["scientific_use"] == "NONE", "scientific use")
    require(
        sha256_file(IMPLEMENTATION) == EXPECTED_IMPLEMENTATION_SHA256,
        "live implementation digest",
    )
    validate_implementation_source(IMPLEMENTATION.read_text())

    tests = data["compile_tests"]
    for field in (
        "phase_a5_fortran_objects_linked",
        "phase_a5_fortran_executables_built",
        "phase_a5_fortran_objects_executed",
        "synthetic_executions", "context_population_executions",
        "tracking_reads",
        "transport_solves", "dragon_runs",
    ):
        require(tests[field] == 0, f"compile-only count: {field}")
    require(tests["A3_link_barrier_rechecked"] is True, "A3 barrier")
    require(tests["prerequisite_runners_executed"] == 0, "old runners")
    expected_counts = {
        "a3": tests["A3_unresolved_symbol_count_rechecked"],
        "a4": tests["A4_unresolved_symbol_count_rechecked"],
        "a5": tests["A5_unresolved_symbol_count"],
        "anchor": tests["anchor_unresolved_symbol_count"],
    }
    require(expected_counts["a3"] == 8, "A3 unresolved count")
    require(expected_counts["a4"] == 10, "A4 unresolved count")
    for count in expected_counts.values():
        require(isinstance(count, int) and count > 0, "unresolved count type")
    anchor = ROOT / tests["positive_anchor"]
    require(anchor.is_file(), "anchor file")
    require(
        re.search(r"(?im)^\s*program\b", anchor.read_text()) is None,
        "anchor is executable program",
    )
    require(
        tests["positive_anchor_has_program"] is False,
        "anchor program claim",
    )
    negative_sources = tests["negative_sources"]
    require(
        set(negative_sources)
        == {
            "validation/iterative/real64_phase_a5/"
            "compile_fail_real32_lane.f90",
            "validation/iterative/real64_phase_a5/"
            "compile_fail_integer_kpsys.f90",
            "validation/iterative/real64_phase_a5/"
            "compile_fail_real32_caz.f90",
            "validation/iterative/real64_phase_a5/"
            "compile_fail_real64_operator_data.f90",
            "validation/iterative/real64_phase_a5/"
            "compile_fail_noncontiguous_population_actual.f90",
        },
        "negative source scope",
    )
    for relative, expected in negative_sources.items():
        require(
            sha256_file(ROOT / relative) == expected,
            f"negative source digest: {relative}",
        )

    build = data["build_contract"]
    require(build["top_level_target"] == "spot-real64-phase-a5", "target")
    for field in ("added_to_default_all", "added_to_tests",
                  "added_to_spot_fast"):
        require(build[field] is False, field)
    require(build["temporary_build_directory"] is True, "temporary build")
    require(
        build["all_fortran_commands_compile_only"] is True,
        "object-only compiler contract",
    )
    require(build["link_commands_allowed"] == [], "link commands")
    require(build["runner_sha256"] == EXPECTED_RUNNER_SHA256, "runner digest")
    require(
        build["top_level_makefile_delta"]
        == "PHASE-A4-BASELINE-PLUS-EXACT-ISOLATED-PHASE-A5-BLOCK",
        "Makefile delta",
    )
    require(
        build["unresolved_symbol_policy"]
        == "FOUR-OBJECT-EXACT-ALLOWLISTS-WITH-EXACT-COUNTS",
        "unresolved policy",
    )
    require(
        build["required_checked_flags"] == REQUIRED_CHECKED_FLAGS,
        "checked flags",
    )
    validate_makefile_contract((ROOT / "Makefile").read_text())

    require(
        data["remaining_open_path"] == EXPECTED_REMAINING_OPEN_PATH,
        "remaining path",
    )
    require(
        data["next_step"]
        == "Add a separate compile-only production-default-off host "
           "callsite and runtime-provenance preflight design while "
           "preserving the Phase-A3 link barrier and performing no "
           "tracking or transport execution.",
        "next step",
    )
    require(
        "no tracking or transport execution"
        in data["next_step"].lower(),
        "next step expands execution authority",
    )
    require(data["interpretation"] == EXPECTED_INTERPRETATION,
            "interpretation")

    require(RUNNER.is_file(), "missing runner")
    validate_runner_contract(
        RUNNER.read_text(),
        expected_counts=expected_counts,
    )
    validate_scoped_receipt()

    production = "\n".join(
        path.read_text(errors="replace")
        for pattern in ("*.c", "*.f", "*.F", "*.f90", "*.F90")
        for path in (ROOT / "src").glob(pattern)
        if path.is_file()
    )
    require(
        re.search(
            rf"(?i)\buse\s+spor64_a5\b|"
            rf"\bcall\s+{re.escape(PUBLIC_PROCEDURE)}\b",
            production,
        )
        is None,
        "Phase-A5 connected to production",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    args = parser.parse_args()
    try:
        validate(load_manifest(args.manifest))
    except (KeyError, OSError, PhaseA5Error) as exc:
        raise SystemExit(f"SPOR64 PHASE-A5 REJECTED: {exc}") from exc
    print(
        "SPOR64 PHASE-A5 CONTRACT PASS: "
        "COMPILE-ONLY-PRIVATE-POPULATION; "
        "A5-LINKS=0; A5-EXECUTIONS=0; "
        "TRANSPORT-SOLVES=0; DRAGON-RUNS=0"
    )


if __name__ == "__main__":
    main()
