#!/usr/bin/env python3
"""Static fail-closed contract for the Phase-A9b B2n source boundary."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE = ROOT / "src/SPOR64_B2N.f90"
BUILDER = HERE / "build_b2n_real64_frozen_qfiss.f90"
POSTERIOR = HERE / "check_b2n_real64_frozen_qfiss.f90"
BOUNDED = HERE / "run_bounded_b2n.py"
BOUNDED_TEST = HERE / "test_run_bounded_b2n.py"
CONTRACT_TEST = HERE / "test_phase_a9b_b2n_real64_frozen_qfiss_contract.py"
RUNNER = HERE / "run_phase_a9b_b2n_real64_frozen_qfiss.sh"
README = HERE / "README.md"
MANIFEST = HERE / "precision_manifest.json"
RUNTIME_RESULT = HERE / "runtime_result.txt"
RECEIPT = HERE / "phase_a9b_b2n_real64_frozen_qfiss_receipt.sha256"
MAKEFILE = ROOT / "Makefile"
ROOT_README = ROOT / "README.md"
ITERATIVE_README = ROOT / "validation/iterative/README.md"


class GateError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise GateError(message)


def code_only(text: str) -> str:
    return "\n".join(line.split("!", 1)[0] for line in text.splitlines())


def packed_fortran(text: str) -> str:
    return re.sub(r"\s+", "", code_only(text)).upper()


def routine_region(text: str, name: str) -> str:
    match = re.search(
        rf"(?is)\bsubroutine\s+{re.escape(name)}\b.*?"
        rf"\bend\s+subroutine\s+{re.escape(name)}\b",
        text,
    )
    require(match is not None, f"missing routine {name}")
    return match.group(0)


def check_source(text: str) -> None:
    packed = packed_fortran(text)
    require("MODULESPOR64_B2N" in packed, "production B2n module")
    require("SPOR64_B2N_PREFLIGHT_FAILED=1" in packed, "preflight status")
    require("SPOR64_B2N_COMMITTED=2" in packed, "commit status")
    region = packed_fortran(routine_region(text, "SPOR64_B2N_BUILD"))
    require(
        "SUBROUTINESPOR64_B2N_BUILD(IPPROJECTED,PLANE_INDEX,"
        "IPMACRO_OUT,IPSOURCE_OUT,STATUS)" in region,
        "exact public build ABI",
    )
    require("STATUS=SPOR64_B2N_PREFLIGHT_FAILED" in region, "fail-closed entry")
    require(region.count("STATUS=SPOR64_B2N_COMMITTED") == 1, "one commit")
    require("NGRP=370" in packed, "370 groups")
    require("NREG=8" in packed, "8 regions")
    require("NUNKNO=14" in packed, "14 unknowns")
    require("NMAT=8" in packed, "8 materials")
    require("NFIS=32" in packed or "NIFIS=32" in packed, "32 fissile components")
    require("REAL(REAL64)" in packed, "REAL64 source storage")
    require("'PROJECTED'" in packed, "PROJECTED admission")
    require("'FROZEN-QFIS'" in packed, "frozen authority state")
    for name in (
        "'SPOT-R64'", "'RHO'", "'PLANE'", "'STATE'", "'QFISS'",
        "'EPOCH'", "'DSOUR'", "'SPOT-QINT'", "'SPOT-FROZEN'",
        "'SPOT-KEFF'", "'NUSIGF'", "'CHI'",
    ):
        require(name in region, f"missing source record {name}")
    require("LCMEQU" in region, "recursive macrolib copy")
    require("LCMPDL" in region and ",4," in region, "type-4 publication")
    require(",2," in region, "type-2 compatibility publication")
    require("TRANSFER" in region, "bit-identity admission")
    require("IEEE_IS_FINITE" in region, "finite admission")
    require("C_ASSOCIATED" in region, "pointer admission")
    require("LCMINF" in packed, "fresh-root admission")

    epoch_write = max(region.rfind("'EPOCH'"), region.rfind('"EPOCH"'))
    commit = region.rfind("STATUS=SPOR64_B2N_COMMITTED")
    require(0 <= epoch_write < commit, "epoch precedes sole commit status")

    # The frozen formula must be a nested region/fissile/old-group/new-group
    # loop.  Variable names are intentionally restricted to the production
    # implementation's explicit physical indices.
    formula_start = region.find("Q64=+0.0_REAL64")
    formula_end = region.find("QINT64=+0.0_REAL64", formula_start)
    require(0 <= formula_start < formula_end, "isolated QFISS formula region")
    formula = region[formula_start:formula_end]
    loop_patterns = (
        r"DO(?:IR|IREG)=1,NREG",
        r"DO(?:JF|IFIS)=1,(?:NFIS|NIFIS)",
        r"DO(?:H|JGR)=1,NGRP",
        r"DO(?:G|IGR)=1,NGRP",
    )
    positions = []
    for pattern in loop_patterns:
        match = re.search(pattern, formula)
        require(match is not None, f"missing ordered source loop {pattern}")
        positions.append(match.start())
    require(positions == sorted(positions), "source loop order changed")
    require(re.search(r"FIS\w*=FIS\w*\+", formula) is not None,
            "ordered fission-rate accumulation")
    require(re.search(r"(?:SOURCE\w*|Q64)\([^)]*\)="
                      r"(?:SOURCE\w*|Q64)\([^)]*\)\+", formula)
            is not None, "ordered QFISS accumulation")
    for operation in (
        "PRODUCT64=REAL(NUSIGF32(IM,IFIS,H),REAL64)*PHI64(IU,H)",
        "FIS64=FIS64+PRODUCT64",
        "CONTRIBUTION64=REAL(CHI32(IM,IFIS,G),REAL64)*FIS64",
        "CONTRIBUTION64=CONTRIBUTION64*RHO64",
        "Q64(IU,G)=Q64(IU,G)+CONTRIBUTION64",
    ):
        require(formula.count(operation) == 1,
                f"exact production formula operation {operation}")

    require(region.count("IF(.NOT.EMPTY_LCM_ROOT(IPMACRO_OUT))RETURN") == 2,
            "two MACRO fresh-root checks")
    require(region.count("IF(.NOT.EMPTY_LCM_ROOT(IPSOURCE_OUT))RETURN") == 2,
            "two SOURCE fresh-root checks")
    epoch_call = (
        "CALLLCMPUT(SOURCE_AUTHORITY,'EPOCH',1,1,FROZEN_SOURCE_EPOCH)"
    )
    require(region.count(epoch_call) == 1, "one exact EPOCH commit write")
    epoch_position = region.find(epoch_call)
    after_epoch = region[epoch_position + len(epoch_call):commit]
    for mutation in (
        "CALLLCMPUT(", "CALLLCMPTC(", "CALLLCMPDL(", "CALLLCMEQU(",
        "LCMDID(", "LCMLID(", "LCMLIL(",
    ):
        require(mutation not in after_epoch,
                f"output mutation after EPOCH commit: {mutation}")

    forbidden_calls = (
        "FLU", "FLUDRV", "FLU2DR", "ASM", "SPOR64K", "DOORFV",
        "MCCGF", "MCGMRE", "SPOFSRC", "SPOFCHK", "SPOPROJ", "CONT",
    )
    for name in forbidden_calls:
        require(f"CALL{name}(" not in region,
                f"forbidden production call {name}")
    for term in ("RELAX", "DAMP", "CLIP", "FLOOR", "FIT_COEF", "EMPIRICAL"):
        require(term not in region, f"forbidden empirical mechanism {term}")
    require("LCMGID(IPFLUX,'FLUX')" not in region,
            "root binary32 FLUX fallback forbidden")
    require("LCMGID(IPFLUX,'SOUR')" not in region,
            "terminal SOUR reuse forbidden")


def check_builder(text: str) -> None:
    packed = packed_fortran(text)
    require(packed.count("CALLSPOR64_B2N_BUILD(") == 1, "one production build call")
    require("CALLSPOR64_B2N_BUILD(PROJECTED,1,MACRO,SOURCE,STATUS)" in packed,
            "plane-1 build actual list")
    require("SPOR64_B2N_COMMITTED" in packed, "committed status required")
    require(packed.count("CALLLCMEQU(") == 2, "two whole-object evidence copies")
    require(packed.count("CALLLCMOP(") >= 5, "input, memory, and XSM roots")
    for token in ("FLU", "ASM", "SPOR64K", "DRAGON", "SPOFSRC", "SPOFCHK"):
        require(re.search(rf"\bCALL{token}\b", packed) is None,
                f"builder calls forbidden {token}")
    for marker in (
        "B2NREAL64FROZEN-QFISSBUILDPASS",
        "B2NPRODUCTION-BUILD-CALLS=1PLANE=1STATE=FROZEN-QFIS/1",
        "B2NWHOLE-OBJECT-XSM-COPIES=2",
        "B2NDRAGON=0ASM=0FLU=0TRANSPORT=0PICARD=0",
        "B2NCONVERGENCE=NOT-EVALUATED",
    ):
        require(marker in packed, f"missing builder marker {marker}")


def check_posterior(text: str) -> None:
    packed = packed_fortran(text)
    compact = packed.replace("&", "")
    require("USESPOR64_B2N" not in packed, "posterior must not link producer")
    for token in ("CALLFLU", "CALLASM", "CALLSPOR64K", "CALLDOORFV", "CALLSPOR64_B2N"):
        require(token not in packed, f"posterior calls forbidden {token}")
    for count in ("5180", "94720", "2960", "2220", "370"):
        require(count in packed, f"posterior count {count}")
    require("TRANSFER" in packed, "posterior bit comparisons")
    require("IEEE_IS_FINITE" in packed, "posterior finite checks")
    require("EXACT_INVENTORY" in packed, "posterior exact inventories")
    require("RECURS" in packed or "LCMNXT" in packed, "recursive macrolib comparison")
    for opening in (
        "CALLLCMOP(PROJECTED,TRIM(PROJECTED_PATH),2,2,0)",
        "CALLLCMOP(MACRO_OUTPUT,TRIM(MACRO_PATH),2,2,0)",
        "CALLLCMOP(SOURCE_OUTPUT,TRIM(SOURCE_PATH),2,2,0)",
    ):
        require(packed.count(opening) == 1,
                f"exact read-only posterior open {opening}")
    for closing in (
        "CALLLCMCL(SOURCE_OUTPUT,1)", "CALLLCMCL(MACRO_OUTPUT,1)",
        "CALLLCMCL(PROJECTED,1)",
    ):
        require(packed.count(closing) == 1,
                f"exact read-only posterior close {closing}")
    for mutation in (
        "CALLLCMPUT(", "CALLLCMPTC(", "CALLLCMPDL(", "CALLLCMEQU(",
        "LCMDID(", "LCMLID(", "LCMLIL(", "CALLLCMSIX(",
    ):
        require(mutation not in packed, f"posterior write path {mutation}")

    oracle = packed_fortran(routine_region(text, "RECOMPUTE_QFISS"))
    for operation in (
        "PRODUCT=REAL(NUSIGF32(IBM,IFIS,H),REAL64)*FLUX(IUNK,H)",
        "FISSION_RATE=FISSION_RATE+PRODUCT",
        "CONTRIBUTION=REAL(CHI32(IBM,IFIS,G),REAL64)*FISSION_RATE",
        "CONTRIBUTION=CONTRIBUTION*RHO",
        "QFISS(IUNK,G)=QFISS(IUNK,G)+CONTRIBUTION",
    ):
        require(oracle.count(operation) == 1,
                f"exact posterior formula operation {operation}")
    for comparison in (
        "EXPECTED_QINT32=REAL(QINT,REAL32)",
        "TRANSFER(QINT32,0_INT32,NGRP)/="
        "TRANSFER(EXPECTED_QINT32,0_INT32,NGRP)",
        "QFISS64_BITS=TRANSFER(AUTHORITY_QFISS,0_INT64,NUNKNO)",
        "EXPECTED64_BITS=TRANSFER(QFISS(:,G),0_INT64,NUNKNO)",
        "ANY(QFISS64_BITS/=EXPECTED64_BITS)",
        "QFISS32_BITS=TRANSFER(DSOUR32,0_INT32,NUNKNO)",
        "EXPECTED32_BITS=TRANSFER(REAL(QFISS(:,G),REAL32),0_INT32,NUNKNO)",
        "ANY(QFISS32_BITS/=EXPECTED32_BITS)",
        "TRANSFER(OUTPUT_NUSIGF,0_INT32,NMAT*NIFIS)/=0_INT32",
    ):
        require(comparison in compact,
                f"posterior expected-vs-output comparison {comparison}")
    for marker in (
        "B2NREAL64FROZEN-QFISSPOSTERIORPASS",
        "B2NQFISS-R64-BITS=5180DSOUR-R32-PROJECTIONS=5180QINT-R32-PROJECTIONS=370",
        "B2NPOSITIVE-REGION-FLUX=2960NONREGION-POSITIVE-ZERO-QFISS=2220",
        "B2NNUSIGF-POSITIVE-ZERO=94720MACRO-OTHER-RECORDS=BIT-IDENTICAL",
        "B2NSTATE=FROZEN-QFIS/1PLANE=1SAME-RHO=BIT-IDENTICAL",
        "B2NFIRST-GROUP-INTEGRAL=POSITIVE",
        "B2NDRAGON=0ASM=0FLU=0CONVERGENCE=NOT-EVALUATED",
        "B2NEMPIRICAL-CONTROLS=0CONT=0",
    ):
        require(marker in packed, f"missing posterior marker {marker}")


def check_bounded(text: str) -> None:
    require(set(re.findall(r'^\s*"([a-z0-9]+)"\s*:\s*\{', text, re.M)) ==
            {"prepare", "build", "posterior"}, "exact bounded profiles")
    expected_profiles = {
        "prepare": {
            "wall_seconds": "30", "cpu_seconds": "20",
            "rss_bytes": r"2\s*\*\s*1024\*\*3",
            "file_bytes": r"512\s*\*\s*1024\*\*2",
            "log_bytes": r"16\s*\*\s*1024\*\*2",
        },
        "build": {
            "wall_seconds": "30", "cpu_seconds": "20",
            "rss_bytes": r"2\s*\*\s*1024\*\*3",
            "file_bytes": r"128\s*\*\s*1024\*\*2",
            "log_bytes": r"16\s*\*\s*1024\*\*2",
        },
        "posterior": {
            "wall_seconds": "30", "cpu_seconds": "20",
            "rss_bytes": r"2\s*\*\s*1024\*\*3",
            "file_bytes": r"16\s*\*\s*1024\*\*2",
            "log_bytes": r"16\s*\*\s*1024\*\*2",
        },
    }
    for profile_name, fields in expected_profiles.items():
        match = re.search(
            rf'(?ms)^\s*"{profile_name}"\s*:\s*\{{(.*?)^\s*\}},?\s*$',
            text,
        )
        require(match is not None, f"bounded profile body {profile_name}")
        body = match.group(1)
        for field, expression in fields.items():
            require(
                len(re.findall(rf'"{field}"\s*:\s*{expression}\s*,?', body)) == 1,
                f"bounded {profile_name}.{field}",
            )
    for token in (
        "start_new_session=True", "RLIMIT_CPU", "RLIMIT_FSIZE", "RLIMIT_CORE",
        "os.killpg", "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS",
    ):
        require(token in text, f"bounded control {token}")
    require("retry" not in code_only(text).lower(), "bounded runner has no retry path")


def check_runner(text: str) -> None:
    require("RUN_B2N=${RUN_B2N:-0}" in text, "runtime default off")
    require('case "$RUN_B2N" in' in text and "0|1" in text, "binary activation")
    require(text.count('python3 "$BOUNDED" prepare') == 1, "one prepare invocation")
    require(text.count('python3 "$BOUNDED" build') == 1, "one build invocation")
    require(text.count('python3 "$BOUNDED" posterior') == 2, "two posterior invocations")
    require("RUN_B2M=1" not in text, "no nested B2m runtime")
    require("Dragon.b2" not in text and "/Dragon" not in text, "no Dragon executable")
    for marker in (
        "REAL-SOURCE-BUILDS=0 DRAGON=0 ASM=0 SPOR64K=0 FLU=0",
        "QFISS-R64-BITS=5180",
        "RETRIES=0",
        "RADIAL-FLUX-SOLVE=NOT-EXECUTED",
    ):
        require(marker in text, f"runner marker {marker}")
    require("EXPECTED_PROJECTED_HASH=" in text, "frozen input hash")
    for accepted_output in (
        "EXPECTED_MACRO_HASH=6430b5e43b03125f8bd94c350bae2d8fc97978f86b3a5bb25f2026fd10914ada",
        "EXPECTED_MACRO_BYTES=9878532",
        "EXPECTED_SOURCE_HASH=37a3499742125db65fb51e505797e2890f6ae29461af9640bf14352aad898f2d",
        "EXPECTED_SOURCE_BYTES=625560",
        '[ "$MACRO_HASH" = "$EXPECTED_MACRO_HASH" ]',
        '[ "$SOURCE_HASH" = "$EXPECTED_SOURCE_HASH" ]',
    ):
        require(accepted_output in text,
                f"accepted output identity {accepted_output}")
    require("verify_receipts" in text, "receipt verification")
    for frozen_parent in (
        "EXPECTED_B2C_HASH=9028d686aa20f96bbda59994fa59b4dd1c5489b52f8ad448d1db8b56f5e63e18",
        "EXPECTED_B2I_HASH=3c54d50d21795c5907917fc35b09c8f93a3c7a40c001dcaa85dda82e95a79446",
        "EXPECTED_B2H_HASH=3ce30d8e5a3f42b2d407c6abec4d95725b8f8eb1b6c04fed8fac5b543cb35994",
        "EXPECTED_B2J_HASH=3efe5f83579f0e59e6a486c5857ea3ab3b517fe5c47e4da0ccab4e8de2c8aaaa",
        "EXPECTED_PREPARER_HASH=5b57989f0095f35fccde54e1453621d584ed447eab50abeff443b8a98c4b10d8",
        "require_parent_entry src/SPOR64_B2C.f90",
        "require_parent_entry src/SPOR64_B2I.f90",
        "require_parent_entry src/SPOR64_B2H.f90",
        "require_parent_entry src/SPOR64_B2J.f90",
        "prepare_b2l_projected.f90",
    ):
        require(frozen_parent in text, f"frozen parent input {frozen_parent}")
    require('nm -g "$BUILD_DIR/prepare_b2l_projected"' in text,
            "preparer symbol census")
    require('"$BUILD_DIR/prepare.nm" "$BUILD_DIR/build.nm"' in text,
            "preparer included in forbidden-solver census")
    require("cmp \"$CASE_DIR/posterior_a.log\"" in text, "repeatable posterior")
    require(re.search(
        r'wc -l <"\$CASE_DIR/build\.log".{0,100}-eq 5.{0,100}'
        r'builder output inventory differs', text, re.S) is not None,
        "five-line builder inventory")
    require(re.search(
        r'wc -l <"\$CASE_DIR/posterior_a\.log".{0,100}-eq 8.{0,100}'
        r'posterior output inventory differs', text, re.S) is not None,
        "eight-line posterior inventory")
    for immutable in (
        "MACRO0 mutated during read-only posterior",
        "FSOURCE mutated during read-only posterior",
        "MACRO0 byte count changed during posterior",
        "FSOURCE byte count changed during posterior",
    ):
        require(immutable in text, f"posterior immutability check {immutable}")


def check_manifest(data: dict[str, object]) -> None:
    require(data.get("phase") == "A9b-B2n", "manifest phase")
    require(data.get("parent") == "A9b-B2m", "manifest parent")
    require(data.get("input_state") == "PROJECTED", "manifest input state")
    formula = data.get("formula")
    require(isinstance(formula, dict), "manifest formula")
    require(formula.get("loop_order") ==
            ["region", "fissile_component", "old_group", "destination_group"],
            "manifest operation order")
    require(formula.get("qfiss") ==
            "q[r,g]=sum_j((CHI[m(r),j,g]*f[r,j])*rho)",
            "manifest exact QFISS operation order")
    for key in (
        "fp_contraction", "fast_math", "empirical_tolerance",
        "relaxation_or_damping", "clipping_or_floor", "normalization",
        "model_completion",
    ):
        require(formula.get(key) is False, f"manifest forbids {key}")
    policy = data.get("execution_policy")
    require(isinstance(policy, dict), "manifest execution policy")
    require(policy.get("runtime_default_off") is True,
            "manifest runtime default off")
    for key in (
        "dragon_executions", "asm_executions", "spor64k_executions",
        "flu_executions", "transport_solves", "picard_maps",
        "automatic_retries",
    ):
        require(policy.get(key) == 0, f"manifest zero {key}")
    posterior = data.get("posterior_contract")
    require(isinstance(posterior, dict), "manifest posterior")
    require(posterior.get("qfiss_binary64_bit_checks") == 5180,
            "manifest QFISS checks")
    require(posterior.get("dsour_binary32_projection_checks") == 5180,
            "manifest DSOUR checks")
    require(posterior.get("qint_binary32_projection_checks") == 370,
            "manifest QINT checks")
    require(posterior.get("positive_region_flux_checks") == 2960,
            "manifest region-flux checks")
    require(posterior.get("nonregion_positive_zero_checks") == 2220,
            "manifest non-region checks")
    require(posterior.get("independent_solver_free_checker") is True,
            "manifest independent checker")
    require(posterior.get("posterior_repetitions") == 2,
            "manifest posterior repetitions")
    require(posterior.get("posterior_outputs_byte_identical") is True,
            "manifest byte-identical posterior")
    macro0 = data.get("macro0")
    require(isinstance(macro0, dict), "manifest MACRO0")
    require(macro0.get("nusigf_positive_zero_values") == 94720,
            "manifest NUSIGF zero checks")
    semantic = data.get("semantic_boundary")
    require(isinstance(semantic, dict), "manifest semantic boundary")
    for key in (
        "radial_flux_solved", "radial_convergence_evaluated",
        "outer_picard_map_executed", "outer_picard_convergence_evaluated",
        "balance_residual_evaluated", "response_accuracy_evaluated",
        "spod_accuracy_evaluated",
    ):
        require(semantic.get(key) is False, f"manifest semantic false {key}")
    evaluated = semantic.get("real_execution_evaluated")
    require(isinstance(evaluated, bool), "manifest real-execution state")
    accepted = data.get("accepted_runtime")
    if evaluated:
        require(isinstance(accepted, dict), "manifest accepted runtime")
        expected_identity = {
            "projected_sha256": "c010c0a860884a4e4d3842dffe45ffb4898f2aaca99557e0411ee8c66d60b90c",
            "projected_bytes": 225315452,
            "macro0_sha256": "6430b5e43b03125f8bd94c350bae2d8fc97978f86b3a5bb25f2026fd10914ada",
            "macro0_bytes": 9878532,
            "fsource_sha256": "37a3499742125db65fb51e505797e2890f6ae29461af9640bf14352aad898f2d",
            "fsource_bytes": 625560,
            "materializer_executions": 1,
            "source_builder_executions": 1,
            "posterior_executions": 2,
        }
        for key, value in expected_identity.items():
            require(accepted.get(key) == value,
                    f"manifest accepted identity {key}")
        for key in (
            "prepare_wall_seconds", "build_wall_seconds",
            "posterior_a_wall_seconds", "posterior_b_wall_seconds",
        ):
            value = accepted.get(key)
            require(isinstance(value, (int, float)) and 0 < value < 30,
                    f"manifest accepted bounded time {key}")
        require(RUNTIME_RESULT.is_file(), "accepted runtime result file")
        require(RECEIPT.is_file(), "accepted receipt file")
    else:
        require(accepted is None, "no accepted runtime before execution")


def check_runtime_result(text: str, data: dict[str, object]) -> None:
    accepted = data.get("accepted_runtime")
    require(isinstance(accepted, dict), "runtime manifest identity")
    lines = text.splitlines()
    require(lines and lines[0] ==
            "SPOR64 PHASE-A9b-B2n ACCEPTED RUNTIME RESULT",
            "runtime header")
    records: dict[str, str] = {}
    for line in lines[1:]:
        if not line:
            continue
        require("=" in line, "runtime key/value line")
        key, value = line.split("=", 1)
        require(re.fullmatch(r"[A-Z0-9-]+", key) is not None,
                f"runtime key syntax {key}")
        require(key not in records, f"duplicate runtime key {key}")
        records[key] = value

    expected = {
        "UTC": str(accepted["utc"]),
        "CLAIM": "PLANE1-SAME-EPOCH-REAL64-QFISS-BITWISE-VERIFIED-AND-ZERO-LIVE-FISSION-MACRO0-VERIFIED",
        "ACCEPTED-RUN-MATERIALIZER-EXECUTIONS": str(accepted["materializer_executions"]),
        "ACCEPTED-RUN-SOURCE-BUILDER-EXECUTIONS": str(accepted["source_builder_executions"]),
        "ACCEPTED-RUN-POSTERIOR-EXECUTIONS": str(accepted["posterior_executions"]),
        "ACCEPTED-RUN-PREPARE-WALL-SECONDS": f'{accepted["prepare_wall_seconds"]:.3f}',
        "ACCEPTED-RUN-BUILD-WALL-SECONDS": f'{accepted["build_wall_seconds"]:.3f}',
        "ACCEPTED-RUN-POSTERIOR-A-WALL-SECONDS": f'{accepted["posterior_a_wall_seconds"]:.3f}',
        "ACCEPTED-RUN-POSTERIOR-B-WALL-SECONDS": f'{accepted["posterior_b_wall_seconds"]:.3f}',
        "DRAGON-EXECUTIONS": "0", "ASM-EXECUTIONS": "0",
        "SPOR64K-EXECUTIONS": "0", "FLU-EXECUTIONS": "0",
        "TRANSPORT-SOLVES": "0", "CONT-EXECUTIONS": "0",
        "PICARD-MAPS": "0", "AUTOMATIC-RETRIES": "0",
        "QFISS-REAL64-BIT-CHECKS": "5180",
        "DSOUR-REAL32-PROJECTION-CHECKS": "5180",
        "QINT-REAL32-PROJECTION-CHECKS": "370",
        "POSITIVE-REGION-FLUX-CHECKS": "2960",
        "NONREGION-POSITIVE-ZERO-QFISS-CHECKS": "2220",
        "NUSIGF-POSITIVE-ZERO-CHECKS": "94720",
        "POSTERIOR-OUTPUTS": "BYTE-IDENTICAL",
        "PROJECTED-SHA256": str(accepted["projected_sha256"]),
        "PROJECTED-BYTES": str(accepted["projected_bytes"]),
        "MACRO0-SHA256": str(accepted["macro0_sha256"]),
        "MACRO0-BYTES": str(accepted["macro0_bytes"]),
        "FSOURCE-SHA256": str(accepted["fsource_sha256"]),
        "FSOURCE-BYTES": str(accepted["fsource_bytes"]),
        "EMPIRICAL-PHYSICS-COEFFICIENTS": "0",
        "RELAXATION-OR-DAMPING": "0", "CLIPPING-OR-FLOOR": "0",
        "NORMALIZATION": "0", "MODEL-COMPLETION": "0",
        "RADIAL-FLUX-SOLVE": "NOT-EXECUTED",
        "RADIAL-CONVERGENCE": "NOT-EVALUATED",
        "OUTER-PICARD": "NOT-EVALUATED", "LONG-CALCULATIONS": "0",
    }
    require(records == expected, "exact runtime/manifest inventory")


def check_docs(readme: str, root_readme: str, iterative_readme: str,
               makefile: str) -> None:
    for term in (
        "B2n", "SPOT-R64/QFISS", "does not run `FLU`",
        "PLANE1-SAME-EPOCH-REAL64-QFISS-BITWISE-VERIFIED",
        "cutoff", "NOT-EVALUATED",
    ):
        require(term in readme, f"B2n README term {term}")
    target = "spot-real64-phase-a9b-b2n-real64-frozen-qfiss"
    require(makefile.count(target) == 2, "one Makefile target and recipe")
    # Root summaries are mandatory once the evidence gate is added.
    require("B2n" in root_readme, "root README B2n summary")
    require("B2n" in iterative_readme, "iterative README B2n summary")


def check_receipt() -> None:
    if not RECEIPT.exists():
        return
    seen: set[str] = set()
    for line in RECEIPT.read_text().splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        require(match is not None, "receipt line format")
        digest, relative = match.groups()
        require(relative not in seen, f"duplicate receipt path {relative}")
        seen.add(relative)
        path = ROOT / relative
        require(path.is_file() and not path.is_symlink(),
                f"receipt regular file {relative}")
        require(hashlib.sha256(path.read_bytes()).hexdigest() == digest,
                f"receipt hash {relative}")
    required = {
        "README.md", "Makefile", "validation/iterative/README.md",
        "Ganlib/lib/Darwin_arm64/libGanlib.a",
        "Ganlib/lib/Darwin_arm64/modules/ganlib.mod",
        "Utilib/lib/Darwin_arm64/libUtilib.a",
        "src/SPOR64_B2C.f90", "src/SPOR64_B2I.f90",
        "src/SPOR64_B2H.f90", "src/SPOR64_B2J.f90",
        "src/SPOR64_B2N.f90",
        str(BUILDER.relative_to(ROOT)),
        str(POSTERIOR.relative_to(ROOT)),
        str(BOUNDED.relative_to(ROOT)),
        str(BOUNDED_TEST.relative_to(ROOT)),
        str(CONTRACT_TEST.relative_to(ROOT)),
        str(RUNNER.relative_to(ROOT)),
        str(Path("validation/iterative/real64_phase_a9b_b2l_one_plane_real_asm/") /
            "prepare_b2l_projected.f90"),
        str(Path("validation/iterative/real64_phase_a9b_b2m_three_plane_real_asm_commit/") /
            "phase_a9b_b2m_three_plane_real_asm_commit_receipt.sha256"),
        "validation/artifacts/iterative-map1/state1_axial.xsm",
        "validation/artifacts/iterative-map1/state1_snapshots.xsm",
        "validation/artifacts/iterative-seed/initial_axial_track.xsm",
        str(MANIFEST.relative_to(ROOT)),
        str(README.relative_to(ROOT)),
        str(RUNTIME_RESULT.relative_to(ROOT)),
    }
    require(required <= seen, "receipt source inventory")


def main() -> None:
    for path in (
        SOURCE, BUILDER, POSTERIOR, BOUNDED, BOUNDED_TEST, CONTRACT_TEST, RUNNER,
        README, MANIFEST, MAKEFILE, ROOT_README, ITERATIVE_README,
    ):
        require(path.is_file(), f"missing {path.relative_to(ROOT)}")
    check_source(SOURCE.read_text())
    check_builder(BUILDER.read_text())
    check_posterior(POSTERIOR.read_text())
    check_bounded(BOUNDED.read_text())
    check_runner(RUNNER.read_text())
    manifest = json.loads(MANIFEST.read_text())
    check_manifest(manifest)
    if manifest["semantic_boundary"]["real_execution_evaluated"]:
        check_runtime_result(RUNTIME_RESULT.read_text(), manifest)
    check_docs(
        README.read_text(), ROOT_README.read_text(),
        ITERATIVE_README.read_text(), MAKEFILE.read_text(),
    )
    check_receipt()
    print("SPOR64 PHASE-A9b-B2n STATIC CONTRACT PASS")


if __name__ == "__main__":
    main()
