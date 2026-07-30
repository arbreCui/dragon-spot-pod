#!/usr/bin/env python3
"""Fail-closed checker for the Phase-A6 host-rendezvous boundary."""

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
IMPLEMENTATION = HERE / "SPOR64_A6.f90"
MANIFEST = HERE / "precision_manifest.json"
RUNNER = HERE / "run_phase_a6.sh"
RECEIPT = HERE / "phase_a6_implementation_receipt.sha256"
POSITIVE_FIXTURE = HERE / "compile_spor64_a6_host_callsite.f90"
BASELINE_COMMIT = "2974832ff26914f15f3b26ddef99e6ca73b4f90e"

# These three values deliberately remain fail-closed until every Phase-A6
# artifact has stopped changing.  The release owner freezes them together.
EXPECTED_IMPLEMENTATION_SHA256 = (
    "49aebc5bc8c3a3eb370219c1b3f00c4ea64f98a5b83765c86bfb655276bd3bcf"
)
EXPECTED_CANONICAL_SHA256 = (
    "9e905cacb8369c0f0f504b181b251c9660e46821aba7caffd176ff4dd684e3be"
)
EXPECTED_RUNNER_SHA256 = (
    "2324e9e168d0700ca518def77d2cdf0182d55da0d778e040f5ddf56db7f42a6f"
)

PUBLIC_PROCEDURE = (
    "MCGFL1R64_DEFAULT_OFF_HOST_ADAPTER_COMPILE_ONLY_LOCKED"
)
A5_PROCEDURE = (
    "MCGFL1R64_HOST_SHAPED_POPULATION_COMPILE_ONLY_LOCKED"
)

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
        "FROZEN-IMPLEMENTED-COMPILE-ONLY-HOST-RENDEZVOUS-READINESS",
    "host_rendezvous_contract_frozen": True,
    "host_rendezvous_readiness_implemented": True,
    "phase_a_static_closure": False,
    "compile_only": True,
    "link_authorized": False,
    "execution_authorized": False,
    "production_admission": False,
    "production_admission_reason": [
        "CURRENT-MCGFL1-QFR-PHIIN-ARE-REAL32",
        "NO-COMPLETE-ORDERED-SC-BUNDLE-EXISTS-AT-RENDEZVOUS",
    ],
    "runtime_preflight_implemented": False,
    "runtime_object_provenance_validated": False,
    "tracking_position_validated": False,
    "real_KPSYS_PJJ_directories_bound": False,
    "EXP1_identity_bound": False,
    "continuous_real64_lane": False,
    "production_route_connected": False,
    "default_runtime_route_changed": False,
    "actual_moc_response_validated": False,
    "transport_solves": 0,
    "dragon_processes_authorized": 0,
    "outer_convergence": "NOT-EVALUATED",
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
    "validation/iterative/real64_phase_a5/SPOR64_A5.f90":
        "bcd8d6f59da4f7ea5f2be2c631ca31efe7b0cf2e70b8717c2d0a683d83ff42e7",
}

EXPECTED_PREREQUISITE_RECEIPTS = {
    "validation/iterative/real64_phase_a5/"
    "phase_a5_implementation_receipt.sha256":
        "61a757384df26104b677a698fcc577869050325af86fca50a587f9f44b3fb67d",
}

EXPECTED_LEGACY_HASHES = {
    "src/MCGFL1.f":
        "6701db8972bd92e339d99879787a126f1ce38b72936852ba331259877894df9f",
    "src/MCGFLX.f":
        "89f03dca19474663460736359ff1acf0b3648086d2780286033b85824333344f",
    "src/MCCGF.f":
        "621fba6d02d1b1efae2d6d6db8e61d1463a3a24bcf4d0efe3579bfba97c55546",
    "src/MOCIK3.f":
        "5193a5a8a4922f4c20b34fae19f1d1278722c31c33dae143bf970b7e2595e007",
    "src/MCGFCF.f":
        "60c841dbd2a0a2de2023de8a424b0162bc9898c5c5b877cc4d59f5b892b0deb9",
    "src/MCGFCS.f":
        "14661cff68e916e0fdc962320c434d5eb7aba247bce138a696cc809aaac78ec6",
    "src/MCGFST.f":
        "bda4ec2376d91e5cf12427288c6bc1c565980cf916639937dca21ad7ad62b5e3",
    "src/MCGSCA.f":
        "fb16fe47c842d3a8c6e8726efb05195ce47ec88c6fdf6c00c65a91a3573a0159",
    "src/MCGPJJ.f":
        "b695949d91921778a7fbe9e1a377057e87d821b8d2cd8027de9413ccfcc36de2",
    "src/DOORFV.f":
        "630f84ba8c738e520e471f63f67e2a9813bc9723d3e7ec30db59e478579b0a8d",
    "src/FLU.f":
        "f9391eb48be9ab1f8d9c3250a23409de2dcfb6111d22db283d1c29d030d26fd0",
    "src/XDRTA2.f":
        "625f5738da3ecc62b82ef29217111c2e789bd853e392ae6ecbe7c2c64e456fff",
}

EXPECTED_LOCKED_BRANCH = {
    "calculation_type": "S",
    "door": "MCCG",
    "ISCH": 11,
    "scheme":
        "NON-CYCLIC-STIS-1-STEP-CHARACTERISTICS-TABULATED-EXPONENTIALS",
    "NDIM": 2,
    "K": 14,
    "KPN": 14,
    "NLONG": 14,
    "NREG": 8,
    "NSOUT": 6,
    "groups": 370,
    "NANI": 1,
    "NLIN": 1,
    "NFUNL": 1,
    "STIS": 1,
    "NPJJM": 1,
    "IDIR": 0,
    "CYCLIC": False,
    "LPRISM": False,
    "NGIND": "STRICTLY-CONSECUTIVE-TAIL-ENDING-AT-370",
    "initial_full_tail_allowed": True,
    "later_shorter_tail_allowed": True,
    "NGEFF_forced_to_370": False,
    "NCONV_true_meaning": "ACTIVE-NOT-CONVERGED",
    "active_subset": "NONEMPTY-ARBITRARY-NONCONTIGUOUS-MASK",
}

EXPECTED_DIRECT_HOST_MAP = {
    "n": {"host": "NLONG", "state": "DIRECT"},
    "ndim": {"host": "NDIM", "state": "DIRECT"},
    "nzon": {"host": "NZON", "state": "BORROWED-CONFORMING-VIEW"},
    "qn": {
        "host": "QFR",
        "state": "BLOCKED-HOST-REAL32-A5-REQUIRES-REAL64",
    },
    "fi": {
        "host": "PHIIN",
        "state": "BLOCKED-HOST-REAL32-A5-REQUIRES-REAL64",
    },
    "m": {"host": "M", "state": "DIRECT"},
    "nani_nlin_nfunl": {
        "host": "NANI-NLIN-NFUNL",
        "state": "DIRECT",
    },
    "sc": {
        "host": "COMPLETE-ORDERED-DRAGON-S0XSC-BUNDLE",
        "state":
            "BLOCKED-ONLY-ONE-BORROWED-GROUP-POINTER-EXISTS-AT-A-TIME",
    },
    "source": {"host": "S", "state": "DIRECT-REAL64"},
    "raw_response": {"host": "PHIOUT", "state": "DIRECT-REAL64"},
    "kpn_nreg": {"host": "KPN-NREG", "state": "DIRECT"},
    "keyflx_keycur": {
        "host": "KEYFLX-KEYCUR",
        "state": "BORROWED-CONFORMING-VIEWS",
    },
    "ibc": {
        "host": "IBC-FROM-BC-REFL+TRAN",
        "state": "BORROWED-CONFORMING-VIEW",
    },
    "sigal": {
        "host": "SIGAL",
        "state": "DIRECT-REAL32-OPERATOR-DATA",
    },
    "branch_controls": {
        "host": "STIS-CYCLIC-LPRISM-IDIR",
        "state": "DIRECT-EXACTLY-GUARDED",
    },
    "group_state": {
        "host": "NG-NGEFF-NGIND-NCONV",
        "state": "DIRECT-TAIL-AND-ACTIVE-MASK-GUARDED",
    },
    "iftrak": {
        "host": "IFTRAK",
        "state": "BORROWED-SEQUENTIAL-UNIT-NUMBER",
    },
    "nbtr": {
        "host": "NBTR",
        "state": "DIRECT-AFTER-TRACKING-HEADER-READ",
    },
    "n2max": {"host": "N2MAX", "state": "DIRECT-WHEN-LPRISM-FALSE"},
    "nbatch": {"host": "NBATCH", "state": "DIRECT"},
    "kpsys": {
        "host": "KPSYS",
        "state": "BORROWED-C_PTR-HANDLE-ARRAY",
    },
    "caz1_caz2": {
        "host": "CAZ1-CAZ2",
        "state": "DIRECT-REAL64",
    },
    "zmu_wzmu": {
        "host": "ZMU-WZMU",
        "state": "BORROWED-REAL32-TRACKING-VIEWS",
    },
    "volume": {
        "host": "V",
        "state": "BORROWED-REAL32-TRACKING-VIEW",
    },
}

EXPECTED_BLOCKERS = {
    "mutable_state": {
        "current_QFR_kind": "DEFAULT-REAL-REAL32",
        "current_PHIIN_kind": "DEFAULT-REAL-REAL32",
        "required_QN_kind": "REAL64",
        "required_FI_kind": "REAL64",
        "rendezvous_conversion_allowed": False,
        "reason":
            "PROMOTION-AFTER-REAL32-ROUNDING-DOES-NOT-CREATE-A-"
            "CONTINUOUS-REAL64-LANE",
    },
    "sc_bundle": {
        "required_shape": "SC(0:M,1,NGEFF)",
        "required_order": "CURRENT-STRICTLY-CONSECUTIVE-GATHERED-TAIL",
        "current_availability":
            "ONE-DRAGON-S0XSC-POINTER-PER-ACTIVE-GROUP-LOOP-VISIT",
        "complete_bundle_available": False,
        "rendezvous_gather_allowed": False,
        "rendezvous_LCM_read_allowed": False,
        "last_group_pointer_reuse_allowed": False,
    },
}

EXPECTED_LIFETIME = {
    "scope": "LEXICAL-FORTRAN-SOURCE-ORDER-ONLY",
    "IFTRAK_header_read_before_seam": True,
    "IFTRAK_expected_track_record_position_lexically_before_seam": True,
    "NBTR_established_before_seam": True,
    "NMAX_equals_N2MAX_for_locked_branch": True,
    "source_matrix_S_live_during_synchronous_call": True,
    "raw_response_matrix_PHIOUT_live_during_synchronous_call": True,
    "ISGNR_allocated_and_initialized_by_MOCIK3_before_seam": True,
    "ISGNR_deallocated_only_after_legacy_response_and_acceleration_region":
        True,
    "KPSYS_pointees_borrowed": True,
    "tracking_and_LCM_ownership_transferred": False,
    "A5_context_local_to_synchronous_call": True,
    "borrowed_resources_retained_after_return": False,
    "one_group_XSSC_is_complete_bundle": False,
    "runtime_lifetime_validated": False,
}

EXPECTED_PROVENANCE = {
    "lexical_host_source_map_closed": True,
    "real_context_provenance_bound": False,
    "IFTRAK_open_identity_bound": False,
    "IFTRAK_first_track_position_bound": False,
    "IFTRAK_IPTRK_pair_identity_bound": False,
    "KPSYS_pointee_lifetime_bound": False,
    "KPSYS_group_order_bound": False,
    "KPSYS_PJJ_record_identity_bound": False,
    "SC_bundle_identity_bound": False,
    "SC_SIGAL_KPSYS_NZON_VOLUME_geometry_material_identity_bound": False,
    "EXP1_same_image_epoch_bound": False,
    "production_QFR_PHIIN_REAL64": False,
    "production_host_callsite_bound": False,
    "tracking_stream_runtime_position_validated": False,
    "actual_transport_path_observed": False,
}

EXPECTED_FORBIDDEN = {
    "mutable_state_kind_conversion": True,
    "SC_gather_or_reconstruction": True,
    "file_IO": True,
    "LCM_IO": True,
    "tracking_read": True,
    "transport_application": True,
    "object_link": True,
    "object_execution": True,
    "Dragon_execution": True,
    "default_on_switch": True,
    "host_legacy_response_and_A5_double_visit": True,
    "host_MCGFST_after_A5": True,
    "empirical_parameter": True,
    "relaxation_or_acceleration": True,
    "threshold_or_tolerance": True,
    "interpolation_fit_clip_or_model_change": True,
}

EXPECTED_CALL_BOUNDARY = {
    "only_allowed_future_downstream_call":
        "PHASE-A5-HOST-SHAPED-POPULATION-WRAPPER",
    "direct_A4_calls": 0,
    "direct_A3_calls": 0,
    "direct_legacy_calls": 0,
    "link_barrier_owner": "PHASE-A3",
    "link_barrier_count": 1,
    "A6_link_barriers": 0,
    "production_callers": 0,
}

EXPECTED_RECEIPT_PATHS = [
    "validation/iterative/real64_phase_a5/"
    "phase_a5_implementation_receipt.sha256",
    "validation/iterative/real64_phase_a6/README.md",
    "validation/iterative/real64_phase_a6/SPOR64_A6.f90",
    "validation/iterative/real64_phase_a6/"
    "compile_spor64_a6_host_callsite.f90",
    "validation/iterative/real64_phase_a6/"
    "compile_fail_nonlogical_enable.f90",
    "validation/iterative/real64_phase_a6/"
    "compile_fail_legacy_real32_host_state.f90",
    "validation/iterative/real64_phase_a6/"
    "compile_fail_single_group_xssc.f90",
    "validation/iterative/real64_phase_a6/precision_manifest.json",
    "validation/iterative/real64_phase_a6/check_phase_a6.py",
    "validation/iterative/real64_phase_a6/test_phase_a6_contract.py",
    "validation/iterative/real64_phase_a6/run_phase_a6.sh",
]


class PhaseA6Error(RuntimeError):
    """Raised when the Phase-A6 contract is not exact."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise PhaseA6Error(message)


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
        raise PhaseA6Error(f"cannot load manifest: {exc}") from exc
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
    block = (
        ".PHONY: spot-real64-phase-a6\n"
        "spot-real64-phase-a6 :\n"
        "\tsh validation/iterative/real64_phase_a6/run_phase_a6.sh\n"
    )
    require(makefile.count(block) == 1, "exact isolated Phase-A6 block")
    baseline = git_blob(BASELINE_COMMIT, "Makefile").decode()
    require(
        makefile.replace(block, "", 1) == baseline,
        "Makefile differs from baseline beyond exact Phase-A6 block",
    )
    target = re.search(
        r"(?m)^spot-real64-phase-a6\s*:(?P<prerequisites>[^\n]*)\n"
        r"(?P<recipes>(?:\t[^\n]*(?:\n|$))*)",
        makefile,
    )
    require(target is not None, "missing Phase-A6 target")
    require(
        target.group("prerequisites").strip() == "",
        "Phase-A6 target has prerequisite",
    )
    require(
        target.group("recipes").splitlines()
        == ["\tsh validation/iterative/real64_phase_a6/run_phase_a6.sh"],
        "Phase-A6 recipe is not exact",
    )
    ordinary = re.findall(
        r"(?m)^([A-Za-z][A-Za-z0-9_.-]*)\s*:", makefile
    )
    require(ordinary and ordinary[0] == "all", "default Make target changed")
    for name in ("all", "tests", "spot-fast"):
        dependency = re.search(
            rf"(?m)^{re.escape(name)}\s*:(.*)$", makefile
        )
        require(dependency is not None, f"missing Make target {name}")
        require(
            "spot-real64-phase-a6" not in dependency.group(1),
            f"Phase-A6 added to {name}",
        )


def validate_implementation_source(source: str) -> None:
    lower = source.lower()
    normalized = normalize_fortran(source)
    require(
        re.search(r"(?im)^\s*module\s+spor64_a6\s*$", source) is not None,
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
        normalized.count(
            "logical,parameter,public::spor64_a6_default_enabled=.false."
        ) == 1,
        "default route must be a single compile-time false constant",
    )
    require(
        lower.count("public :: " + PUBLIC_PROCEDURE.lower()) == 1,
        "single public A6 procedure",
    )

    wrapper = extract_subroutine(source, PUBLIC_PROCEDURE)
    wrapper_lower = wrapper.lower()
    wrapper_normalized = normalize_fortran(wrapper)
    require(
        wrapper_normalized.startswith(
            "subroutine" + PUBLIC_PROCEDURE.lower() + "(enabled,"
        ),
        "enabled is not the first host-adapter argument",
    )

    required_declarations = (
        "logical,intent(in)::enabled",
        "type(c_ptr),contiguous,intent(in)::kpsys(:)",
        "real(real64),contiguous,intent(in)::qfr64_host(:,:)",
        "real(real64),contiguous,intent(in)::phiin64_host(:,:)",
        "real(real32),contiguous,intent(in)::sc_by_group(0:,:,:)",
        "real(real64),contiguous,intent(inout)::source64(:,:)",
        "real(real32),contiguous,intent(in)::sigal(-6:,:)",
        "real(real64),contiguous,intent(inout)::raw_response64(:,:)",
        "logical,intent(out)::route_selected",
        "integer,intent(out)::status",
    )
    for declaration in required_declarations:
        require(
            declaration in wrapper_normalized,
            f"typed direct-map declaration: {declaration}",
        )

    exact_guards = (
        "route_selected = .false.",
        "status = SPOR64_A6_UNSUPPORTED",
        "if (.not. enabled) return",
        "route_selected = .true.",
        "status = SPOR64_A6_INVALID",
        "if (isch /= 11 .or. npjjm /= 1) return",
        "if (ndim /= 2 .or. cyclic .or. lprism) return",
        "if (stis /= 1 .or. idir /= 0) return",
        "if (k /= nlong .or. kpn /= nlong) return",
        "if (nsout /= nlong-nreg) return",
        "if (nlong /= 14 .or. nreg /= 8 .or. nsout /= 6) return",
        "if (ng /= 370 .or. nani /= 1 .or. nlin /= 1 .or. nfunl /= 1) "
        "return",
        "if (nangl <= 0 .or. nmu <= 0) return",
        "if (m < 0 .or. ngeff <= 0 .or. ngeff > ng) return",
        "if (size(kpsys) /= ngeff) return",
        "if (size(nzon) /= nlong) return",
        "if (size(sc_by_group,1) /= m+1 .or. "
        "size(sc_by_group,2) /= 1 .or. "
        "size(sc_by_group,3) /= ngeff) return",
        "if (size(keycur) /= nsout .or. size(ibc) /= nsout) return",
        "if (size(sigal,1) /= m+7 .or. size(sigal,2) /= ngeff) return",
        "if (size(ngind) /= ngeff .or. size(nconv) /= ngeff) return",
        "if (size(caz1) /= nangl .or. size(caz2) /= nangl) return",
        "if (size(zmu) /= nmu .or. size(wzmu) /= nmu) return",
        "if (size(volume) /= nlong) return",
    )
    for guard in exact_guards:
        require(
            normalize_fortran(guard) in wrapper_normalized,
            f"locked guard: {guard}",
        )
    for matrix in (
        "qfr64_host", "phiin64_host", "source64", "raw_response64"
    ):
        guard = (
            f"if (size({matrix},1) /= kpn .or. "
            f"size({matrix},2) /= ngeff) return"
        )
        require(
            normalize_fortran(guard) in wrapper_normalized,
            f"matrix-shape guard: {matrix}",
        )
    require(
        normalize_fortran(
            "if (size(keyflx,1) /= nreg .or. "
            "size(keyflx,2) /= nlin .or. "
            "size(keyflx,3) /= nfunl) return"
        ) in wrapper_normalized,
        "KEYFLX shape guard",
    )
    require(
        normalize_fortran(
            "if (iftrak <= 0 .or. nbtr <= 0 .or. "
            "n2max <= 0 .or. nbatch <= 0) return"
        ) in wrapper_normalized,
        "tracking scalar guard",
    )

    call_actuals = (
        "call MCGFL1R64_HOST_SHAPED_POPULATION_COMPILE_ONLY_LOCKED("
        "nlong,ndim,nzon,qfr64_host,phiin64_host,m,nani,nlin,nfunl,"
        "sc_by_group,source64,kpn,nreg,keyflx,keycur,ibc,sigal,stis,"
        "cyclic,lprism,idir,ng,ngeff,ngind,nconv,iftrak,nbtr,n2max,"
        "nbatch,kpsys,caz1,caz2,zmu,wzmu,volume,raw_response64,status)"
    )
    require(
        normalize_fortran(call_actuals) in wrapper_normalized,
        "exact A6-to-A5 host map",
    )
    require(
        len(re.findall(
            rf"(?im)^\s*call\s+{re.escape(A5_PROCEDURE)}\b", source
        )) == 1,
        "A5 call must be exact and unique",
    )
    require(
        len(re.findall(r"(?im)^\s*call\s+", source)) == 1,
        "A6 may contain only the one A5 call",
    )
    require(
        wrapper_lower.index("route_selected = .false.")
        < wrapper_lower.index("if (.not. enabled) return")
        < wrapper_lower.index("route_selected = .true.")
        < wrapper_lower.index("call " + A5_PROCEDURE.lower()),
        "default-off selection and fail-closed admission order",
    )

    for forbidden_call in (
        "MCGFL1R64_A2_A3_HOST_CLOSURE_COMPILE_ONLY_LOCKED",
        "MCGFCF_MCGFST_R64_COMPILE_ONLY_LOCKED",
        "MCGFL1R64_POST_STIS_RAW_FACADE_LOCKED",
        "MCGFCF", "MCGFST", "MCGFCS", "MCGSCA", "MCGFFIR",
    ):
        require(
            re.search(
                rf"(?im)^\s*call\s+{re.escape(forbidden_call)}\b", source
            ) is None,
            f"direct forbidden call: {forbidden_call}",
        )
    require(
        "spor64_a3_compile_only_link_forbidden" not in lower,
        "A6 duplicates the A3 link barrier",
    )
    require(
        re.search(
            r"(?im)^\s*(source64|raw_response64|qfr64_host|phiin64_host|"
            r"sc_by_group|kpsys)\s*=(?!=)", source
        ) is None,
        "host data assigned or reconstructed",
    )
    require(
        re.search(r"(?i)=\s*real\s*\(", source) is None,
        "explicit kind conversion",
    )
    for token in (
        "reshape", "pack", "unpack", "transfer", "spread", "allocate",
        "deallocate", "move_alloc",
    ):
        require(
            re.search(rf"(?i)\b{re.escape(token)}\b", source) is None,
            f"forbidden conversion or gather: {token}",
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
    require(
        re.search(
            r"(?im)^\s*(real|integer|logical|type)\b[^\n]*\bsave\b",
            source,
        ) is None,
        "SAVE state",
    )
    require(
        re.search(r"(?im)^\s*common\b", source) is None,
        "COMMON state",
    )
    require(
        re.search(r"(?im)^\s*[^!\n]*\bpointer\s*::", source) is None,
        "Fortran POINTER state",
    )
    require(
        re.search(r"(?im)^\s*program\b", source) is None,
        "implementation is executable program",
    )


def validate_positive_fixture(source: str) -> None:
    normalized = normalize_fortran(source)
    require(
        re.search(r"(?im)^\s*program\b", source) is None,
        "positive fixture is executable program",
    )
    require(
        normalized.count("usespor64_a6,only:") == 1,
        "fixture must explicitly import A6",
    )
    require(
        normalized.count(PUBLIC_PROCEDURE.lower()) == 2,
        "fixture must import and call the A6 procedure exactly once",
    )
    calls = re.findall(
        rf"(?is)\bcall\s+{re.escape(PUBLIC_PROCEDURE)}\s*\((.*?)\)",
        source,
    )
    require(len(calls) == 1, "positive fixture A6 call count")
    first_actual = calls[0].split(",", 1)[0]
    require(
        normalize_fortran(first_actual) == "spor64_a6_default_enabled",
        "positive fixture first actual is not the default-off constant",
    )
    require(
        normalized.count("spor64_a6_default_enabled") == 2,
        "fixture must import and pass the default-off constant once",
    )


def validate_legacy_mcgfl1_facts(source: str) -> None:
    normalized = normalize_fortran(source)
    require(
        "realqfr(kpn,ngeff),phiin(kpn,ngeff)" in normalized,
        "MCGFL1 QFR/PHIIN are no longer default REAL",
    )
    require(
        "doubleprecisionqfr(" not in normalized
        and "doubleprecisionphiin(" not in normalized,
        "MCGFL1 mutable host state unexpectedly REAL64",
    )
    require(
        "real,pointer,dimension(:)::xssc,z" in normalized,
        "MCGFL1 XSSC is not the one-group REAL pointer",
    )
    require(
        normalized.count(
            "calllcmgpd(jpsys,'dragon-s0xsc',xssc_ptr)"
        ) == 1,
        "DRAGON-S0XSC lexical acquisition count",
    )
    ordered_tokens = (
        "doii=1,ngeff",
        "if(nconv(ii))then",
        "jpsys=kpsys(ii)",
        "calllcmgpd(jpsys,'dragon-s0xsc',xssc_ptr)",
        "callc_f_pointer(xssc_ptr,xssc,(/(m+1)*nani/))",
        "callmcgfcs(",
        "endif",
        "enddo",
    )
    positions: list[int] = []
    cursor = 0
    for token in ordered_tokens:
        position = normalized.find(token, cursor)
        require(
            position >= 0,
            "MCGFL1 no longer acquires only one XSSC pointer per group visit",
        )
        positions.append(position)
        cursor = position + len(token)
    mcgfcs_actuals = normalized[
        positions[5]:positions[6]
    ]
    for actual in (
        "qfr(1,ii)", "phiin(1,ii)", "xssc", "s(1,ii)", "sigal(-6,ii)"
    ):
        require(actual in mcgfcs_actuals, f"MCGFCS per-group actual: {actual}")
    require(
        "xssc(" not in normalized,
        "MCGFL1 now owns an explicit complete XSSC array",
    )


def validate_runner_contract(
    runner: str,
    *,
    verify_hash: bool = True,
    expected_counts: dict[str, int] | None = None,
) -> None:
    if verify_hash:
        require(
            EXPECTED_RUNNER_SHA256 not in ("", "PLACEHOLDER"),
            "runner hash is not frozen",
        )
        require(
            sha256_bytes(runner.encode()) == EXPECTED_RUNNER_SHA256,
            "runner hash mismatch",
        )
    lower = runner.lower()
    for old_runner in (
        "run_phase_a1.sh", "run_phase_a2.sh", "run_phase_a3.sh",
        "run_phase_a4.sh", "run_phase_a5.sh",
    ):
        require(old_runner not in lower, f"old runner invoked: {old_runner}")
    required_tokens = (
        "phase_a5_implementation_receipt.sha256",
        "phase_a6_implementation_receipt.sha256",
        "check_phase_a6.py",
        "test_phase_a6_contract",
        "SPOR64_A1.f90", "SPOR64_A2.f90", "SPOR64_A3.f90",
        "SPOR64_A4.f90", "SPOR64_A5.f90", "SPOR64_A6.f90",
        "compile_spor64_a6_host_callsite.f90",
        "compile_fail_nonlogical_enable.f90",
        "compile_fail_legacy_real32_host_state.f90",
        "compile_fail_single_group_xssc.f90",
        "a3_unresolved.log", "a6_unresolved.log",
        "host_callsite_unresolved.log",
        "SPOR64_A3_COMPILE_ONLY_LINK_FORBIDDEN",
    )
    for token in required_tokens:
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
        require(
            " -c " in f" {command} ",
            f"non-object compiler command: {command}",
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
        require(
            set(expected_counts)
            == {"a3_poison_sentinel_object", "a6", "host_callsite"},
            "unresolved-count object set",
        )
        for stem, count in expected_counts.items():
            require(
                isinstance(count, int) and count > 0,
                f"unresolved count type: {stem}",
            )
            runner_stem = {
                "a3_poison_sentinel_object": "a3",
                "a6": "a6",
                "host_callsite": "host_callsite",
            }[stem]
            token = f'{runner_stem}_unresolved.log")" -ne {count}'
            require(token in runner, f"exact unresolved count: {stem}")
    for declaration in (
        "FORTRAN-OBJECT-LINKS=0",
        "FORTRAN-EXECUTABLES=0",
        "FORTRAN-OBJECT-EXECUTIONS=0",
        "PREREQUISITE-RUNNERS=0",
        "SYNTHETIC-EXECUTIONS=0",
        "HOST-RENDEZVOUS-EXECUTIONS=0",
        "TRACKING-READS=0",
        "TRANSPORT-APPLICATIONS=0",
        "DRAGON-RUNS=0",
    ):
        require(declaration in runner, f"zero declaration: {declaration}")


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
            EXPECTED_CANONICAL_SHA256 not in ("", "PLACEHOLDER"),
            "canonical manifest hash is not frozen",
        )
        require(
            canonical_sha256(data) == EXPECTED_CANONICAL_SHA256,
            "canonical manifest hash mismatch",
        )
    require(
        data["schema"]
        == "spot-radial-real64-phase-a6-compile-only-host-rendezvous-"
           "readiness-v1",
        "schema",
    )
    require(
        data["title"]
        == "Compile-only REAL64 host-rendezvous readiness with blocked "
           "production admission",
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
        "legacy source hash map",
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
        data["direct_host_map"] == EXPECTED_DIRECT_HOST_MAP,
        "direct host map",
    )
    require(
        data["production_admission_blockers"] == EXPECTED_BLOCKERS,
        "production admission blockers",
    )
    require(
        data["static_lifetime_contract"] == EXPECTED_LIFETIME,
        "static lifetime contract",
    )
    require(
        data["provenance_boundary"] == EXPECTED_PROVENANCE,
        "provenance boundary",
    )
    require(
        data["forbidden_actions"] == EXPECTED_FORBIDDEN,
        "forbidden actions",
    )
    require(
        data["call_boundary"] == EXPECTED_CALL_BOUNDARY,
        "call boundary",
    )

    rendezvous = data["host_rendezvous"]
    require(rendezvous["host"] == "MCGFL1", "host")
    require(
        rendezvous["location"]
        == "AFTER-SOURCE-CONSTRUCTION-AND-MOCIK3-BEFORE-REGULAR-"
           "NONCYCLIC-MCGFCF",
        "rendezvous location",
    )
    require(rendezvous["unique_future_seam"] is True, "unique seam")
    require(rendezvous["default_enabled"] is False, "default off")
    require(
        rendezvous["off_arm"]
        == "UNCHANGED-LEGACY-MCGFCF-THEN-MCGFST-RESPONSE-REGION",
        "off arm",
    )
    require(
        rendezvous["on_arm"]
        == "PHASE-A5-PATH-WHICH-ALREADY-COVERS-MCGFCF-THEN-MCGFST",
        "on arm",
    )
    require(
        rendezvous["rejoin_location"]
        == "AFTER-EXISTING-MCGFST-RESPONSE-REGION",
        "rejoin",
    )
    for field in (
        "arms_mutually_exclusive",
        "tracking_stream_double_consumption_prevented_by_contract",
        "STIS_double_application_prevented_by_contract",
    ):
        require(rendezvous[field] is True, field)
    for field in (
        "host_legacy_response_and_A5_permitted_in_same_visit",
        "host_MCGFST_after_A5_permitted",
        "production_insertion_present",
        "production_admission_satisfied",
    ):
        require(rendezvous[field] is False, field)
    require(
        rendezvous["disabled_state_action"] == "UNCHANGED-OFF-ARM",
        "disabled-state action",
    )
    require(
        rendezvous["enabled_route_selected_before_admission_checks"] is True,
        "enabled route selection",
    )
    require(
        rendezvous["enabled_invalid_state_action"]
        == "FAIL-CLOSED-WITHOUT-LEGACY-FALLBACK",
        "enabled-invalid action",
    )

    implementation = data["implementation"]
    require(
        implementation["location"]
        == "validation/iterative/real64_phase_a6/SPOR64_A6.f90",
        "implementation location",
    )
    require(implementation["module"] == "SPOR64_A6", "module")
    require(implementation["procedure"] == PUBLIC_PROCEDURE, "procedure")
    require(
        EXPECTED_IMPLEMENTATION_SHA256 not in ("", "PLACEHOLDER"),
        "implementation hash is not frozen",
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
    require(implementation["production_callers"] == 0, "production callers")
    require(implementation["runtime_calls"] == 0, "runtime calls")
    require(
        sha256_file(IMPLEMENTATION) == EXPECTED_IMPLEMENTATION_SHA256,
        "live implementation digest",
    )
    validate_implementation_source(IMPLEMENTATION.read_text())

    tests = data["compile_tests"]
    zero_fields = (
        "phase_a6_fortran_objects_linked",
        "phase_a6_fortran_executables_built",
        "phase_a6_fortran_objects_executed",
        "prerequisite_runners_executed",
        "synthetic_executions",
        "host_rendezvous_executions",
        "tracking_reads",
        "transport_solves",
        "dragon_runs",
    )
    for field in zero_fields:
        require(tests[field] == 0, f"compile-only count: {field}")
    require(
        tests["positive_anchor"]
        == "validation/iterative/real64_phase_a6/"
           "compile_spor64_a6_host_callsite.f90",
        "positive fixture path",
    )
    require(tests["positive_anchor_has_program"] is False, "anchor program")
    require(POSITIVE_FIXTURE.is_file(), "positive fixture missing")
    require(
        sha256_file(POSITIVE_FIXTURE) == tests["positive_anchor_sha256"],
        "positive fixture hash",
    )
    validate_positive_fixture(POSITIVE_FIXTURE.read_text())

    expected_negative_paths = {
        "validation/iterative/real64_phase_a6/"
        "compile_fail_nonlogical_enable.f90",
        "validation/iterative/real64_phase_a6/"
        "compile_fail_legacy_real32_host_state.f90",
        "validation/iterative/real64_phase_a6/"
        "compile_fail_single_group_xssc.f90",
    }
    require(
        set(tests["negative_sources"]) == expected_negative_paths,
        "negative source scope",
    )
    for relative, expected in tests["negative_sources"].items():
        require(
            sha256_file(ROOT / relative) == expected,
            f"negative source hash: {relative}",
        )
    counts = tests["unresolved_symbol_counts"]
    require(
        set(counts)
        == {"A3_poison_sentinel_object", "A6", "host_callsite"},
        "unresolved symbol object set",
    )
    require(counts["A3_poison_sentinel_object"] == 8,
            "A3 unresolved count")
    require(counts["A6"] == 2, "A6 unresolved count")
    require(counts["host_callsite"] == 5, "host-callsite unresolved count")
    for count in counts.values():
        require(
            isinstance(count, int) and not isinstance(count, bool) and count > 0,
            "unresolved symbol count type",
        )

    build = data["build_contract"]
    require(build["top_level_target"] == "spot-real64-phase-a6", "target")
    for field in (
        "added_to_default_all", "added_to_tests", "added_to_spot_fast"
    ):
        require(build[field] is False, field)
    require(build["temporary_build_directory"] is True, "temporary build")
    require(
        build["all_fortran_commands_compile_only"] is True,
        "object-only compiler contract",
    )
    require(build["runner_sha256"] == EXPECTED_RUNNER_SHA256, "runner hash")
    require(build["validated_platform"] == "Darwin-arm64", "platform")
    require(
        build["validated_compiler_banner"]
        == "GNU Fortran (Homebrew GCC 15.2.0_1) 15.2.0",
        "compiler banner",
    )
    require(build["validated_locale"] == "C", "locale")
    require(
        build["cross_toolchain_portability_claim"]
        == "NONE-SEPARATE-RECEIPT-REQUIRED",
        "portability claim",
    )
    require(
        build["top_level_makefile_delta"]
        == "PHASE-A5-BASELINE-PLUS-EXACT-ISOLATED-PHASE-A6-BLOCK",
        "Makefile delta",
    )
    require(
        build["unresolved_symbol_policy"]
        == "A3-POISON-SENTINEL-PLUS-A6-AND-HOST-CALLSITE-"
           "EXACT-ALLOWLISTS",
        "unresolved policy",
    )
    require(build["link_commands_allowed"] == [], "link command allowlist")
    require(build["forbidden_flag"] == "-fdefault-real-8", "forbidden flag")
    require(
        build["required_checked_flags"] == REQUIRED_CHECKED_FLAGS,
        "checked flags",
    )
    validate_makefile_contract((ROOT / "Makefile").read_text())
    require(RUNNER.is_file(), "runner missing")
    validate_runner_contract(
        RUNNER.read_text(),
        expected_counts={
            "a3_poison_sentinel_object":
                counts["A3_poison_sentinel_object"],
            "a6": counts["A6"],
            "host_callsite": counts["host_callsite"],
        },
    )

    validate_legacy_mcgfl1_facts((ROOT / "src/MCGFL1.f").read_text())
    production = "\n".join(
        path.read_text(errors="replace")
        for pattern in ("*.c", "*.f", "*.F", "*.f90", "*.F90")
        for path in (ROOT / "src").glob(pattern)
        if path.is_file()
    )
    require(
        re.search(
            rf"(?i)\buse\s+spor64_a6\b|"
            rf"\bcall\s+{re.escape(PUBLIC_PROCEDURE)}\b",
            production,
        ) is None,
        "Phase-A6 connected to production",
    )
    require(
        isinstance(data["remaining_unproved"], list)
        and len(data["remaining_unproved"]) == 11,
        "remaining unproved scope",
    )
    require(
        data["next_step"]
        == "First close the upstream continuous REAL64 QFR/PHIIN state "
           "and one complete ordered lifetime-bounded SC bundle; do not "
           "add a production callsite or execute transport before those "
           "blockers are closed.",
        "next step",
    )
    require(
        data["interpretation"]
        == [
            "Phase-A6 freezes only the compile-time location, direct map, "
            "lifetime scope, and fail-closed admission contract for one "
            "future MCGFL1 rendezvous.",
            "The only future ON arm is a mutually exclusive replacement "
            "for the existing regular non-cyclic MCGFCF-through-MCGFST "
            "response region, never an additional traversal or a precursor "
            "to a second MCGFST.",
            "Current production admission is false because QFR and PHIIN "
            "are REAL32 and no complete ordered SC bundle exists at the "
            "rendezvous.",
            "No conversion, gathering, LCM or file I/O, object execution, "
            "tracking read, transport solve, Dragon process, or empirical "
            "parameter is introduced.",
            "No runtime provenance, physical response, numerical accuracy, "
            "radial convergence, or Picard convergence is established.",
        ],
        "interpretation",
    )
    validate_scoped_receipt()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    args = parser.parse_args()
    try:
        validate(load_manifest(args.manifest))
    except (KeyError, OSError, PhaseA6Error) as exc:
        raise SystemExit(f"SPOR64 PHASE-A6 REJECTED: {exc}") from exc
    print(
        "SPOR64 PHASE-A6 CONTRACT PASS: "
        "COMPILE-ONLY-DEFAULT-OFF-HOST-RENDEZVOUS; "
        "PRODUCTION-ADMISSION=BLOCKED; "
        "HOST-RENDEZVOUS-EXECUTIONS=0; "
        "TRANSPORT-SOLVES=0; DRAGON-RUNS=0"
    )


if __name__ == "__main__":
    main()
