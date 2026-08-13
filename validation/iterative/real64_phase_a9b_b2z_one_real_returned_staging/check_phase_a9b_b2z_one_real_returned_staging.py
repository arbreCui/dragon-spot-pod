#!/usr/bin/env python3
"""Fail-closed static contract for one production B2z RETURNED staging."""

from __future__ import annotations

import importlib.util
import hashlib
import json
from pathlib import Path
import re


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RUNNER = HERE / "run_phase_a9b_b2z_one_real_returned_staging.sh"
BOUNDED = HERE / "run_bounded_b2z.py"
PUBLISHER = HERE / "publish_b2z_once.py"
DECK = HERE / "one_real_returned_staging.x2m"
POSTERIOR = HERE / "check_b2z_real_returned.f90"
MANIFEST = HERE / "precision_manifest.json"
README = HERE / "README.md"
RUNTIME_RESULT = HERE / "runtime_result.txt"
RECEIPT = HERE / "phase_a9b_b2z_one_real_returned_staging_receipt.sha256"
HOST = ROOT / "data/SpotStepR64.c2m"
ADAPTER = ROOT / "src/SPOR64_B2U.f90"
B2S = ROOT / "src/SPOR64_B2S.f90"
B2T = ROOT / "src/SPOR64_B2T.f90"

EXPECTED_RECEIPT_PATHS = {
    "Ganlib/lib/Darwin_arm64/libGanlib.a",
    "Ganlib/lib/Darwin_arm64/modules/ganlib.mod",
    "Ganlib/src/cle2000.h",
    "Ganlib/src/ganlib.h",
    "Ganlib/src/kdi.h",
    "Ganlib/src/lcm.h",
    "Ganlib/src/xsm.h",
    "Trivac/lib/Darwin_arm64/libTrivac.a",
    "Utilib/lib/Darwin_arm64/libUtilib.a",
    "data/SpotStepR64.c2m",
    "lib/Darwin_arm64/libDragon.a",
    "lib/Darwin_arm64/modules/spomoc_audit.mod",
    "lib/Darwin_arm64/modules/spor64_a9.mod",
    "src/ASM.f",
    "src/DRAGON.o",
    "src/KDRDRV.F",
    "src/SPOR64_B2B.f90",
    "src/SPOR64_B2C.f90",
    "src/SPOR64_B2H.f90",
    "src/SPOR64_B2I.f90",
    "src/SPOR64_B2J.f90",
    "src/SPOR64_B2K.f90",
    "src/SPOR64_B2N.f90",
    "src/SPOR64_B2O.f90",
    "src/SPOR64_B2R.f90",
    "src/SPOR64_B2S.f90",
    "src/SPOR64_B2T.f90",
    "src/SPOR64_B2U.f90",
    "src/SPOR64_B2W.f90",
    "src/SPOR64_B2X.f90",
    "validation/artifacts/iterative-map1/state1_axial.xsm",
    "validation/artifacts/iterative-map1/state1_snapshots.xsm",
    "validation/artifacts/iterative-seed/initial_axial_track.xsm",
    "validation/artifacts/iterative-seed/initial_radial_track.bin",
    "validation/iterative/real64_phase_a9b_b2k_system_assembly/compile_c2m.c",
    "validation/iterative/real64_phase_a9b_b2l_one_plane_real_asm/prepare_b2l_projected.f90",
    "validation/iterative/real64_phase_a9b_b2m_three_plane_real_asm_commit/phase_a9b_b2m_three_plane_real_asm_commit_receipt.sha256",
    "validation/iterative/real64_phase_a9b_b2n_real64_frozen_qfiss/phase_a9b_b2n_real64_frozen_qfiss_receipt.sha256",
    "validation/iterative/real64_phase_a9b_b2u_same_call_asm_host/phase_a9b_b2u_same_call_asm_host_receipt.sha256",
    "validation/iterative/real64_phase_a9b_b2v_one_real_continuation/phase_a9b_b2v_one_real_continuation_receipt.sha256",
    "validation/iterative/real64_phase_a9b_b2z_one_real_returned_staging/README.md",
    "validation/iterative/real64_phase_a9b_b2z_one_real_returned_staging/check_b2z_real_returned.f90",
    "validation/iterative/real64_phase_a9b_b2z_one_real_returned_staging/check_phase_a9b_b2z_one_real_returned_staging.py",
    "validation/iterative/real64_phase_a9b_b2z_one_real_returned_staging/one_real_returned_staging.x2m",
    "validation/iterative/real64_phase_a9b_b2z_one_real_returned_staging/precision_manifest.json",
    "validation/iterative/real64_phase_a9b_b2z_one_real_returned_staging/publish_b2z_once.py",
    "validation/iterative/real64_phase_a9b_b2z_one_real_returned_staging/run_bounded_b2z.py",
    "validation/iterative/real64_phase_a9b_b2z_one_real_returned_staging/run_phase_a9b_b2z_one_real_returned_staging.sh",
    "validation/iterative/real64_phase_a9b_b2z_one_real_returned_staging/runtime_result.txt",
    "validation/iterative/real64_phase_a9b_b2z_one_real_returned_staging/test_phase_a9b_b2z_one_real_returned_staging.py",
}


class GateError(RuntimeError):
    """Raised when the B2z contract differs."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise GateError(message)


def no_fortran_comments(text: str) -> str:
    return "\n".join(line.split("!", 1)[0] for line in text.splitlines())


def no_deck_comments(text: str) -> str:
    return "\n".join(
        line for line in text.splitlines() if not line.lstrip().startswith("*")
    )


def packed(text: str) -> str:
    return re.sub(r"[\s&]+", "", text).upper()


def check_deck(text: str) -> None:
    code = no_deck_comments(text).upper()
    compact = packed(code)
    required = (
        "SEQ_BINARYTRACK_F::FILE'./INITIAL_RADIAL_TRACK.BIN';",
        "XSM_FILEPROJ_XSM::FILE'./PROJECTED.XSM';",
        "XSM_FILERET_XSM::FILE'./RETURNED.XSM';",
        "PROJECTED:=PROJ_XSM;",
        "RETURNED:=SPOTSTEPR64PROJECTEDTRACK_F::;",
        "RET_XSM:=RETURNED;",
    )
    for token in required:
        require(compact.count(token) == 1, f"deck token count differs: {token}")
    begin = "B2Z-REAL-PRODUCTION-STAGING-BEGIN"
    complete = "B2Z-REAL-PRODUCTION-STAGING-COMPLETE"
    require(code.count(begin) == 1 and code.count(complete) == 1,
            "deck markers differ")
    order = [
        compact.index("PROJECTED:=PROJ_XSM;"),
        compact.index(begin),
        compact.index("RETURNED:=SPOTSTEPR64PROJECTEDTRACK_F::;"),
        compact.index("RET_XSM:=RETURNED;"),
        compact.index(complete),
    ]
    require(order == sorted(order), "deck lifecycle order differs")
    for token in (
        "WHILE", "REPEAT", "UNTIL", "PICARD", "RELAX", "DAMP", "CLIP",
        "SPOR64V:", "SPOR64X:", "FLU:", "SPOSTATE:", "SPOLEAK:", "CLOSED",
    ):
        require(token not in code, f"forbidden deck token: {token}")


def check_host(text: str) -> None:
    code = packed(no_deck_comments(text))
    require(code.count(":=ASM:") == 3, "SpotStepR64 ASM count differs")
    for plane in (1, 2, 3):
        fragment = (
            f"SYSTEM{plane}:=ASM:MACRO0TRACKTRACK_FPROJECTED::"
            f"EDIT0ARMLK1D{plane};"
        )
        require(fragment in code, f"plane-{plane} ASM call differs")
    dispatch = "RETURNED:=SPOR64T:PROJECTEDSYSTEM1SYSTEM2SYSTEM3TRACK_F::;"
    require(code.count(dispatch) == 1, "production SPOR64T dispatch differs")
    require(code.rfind(":=ASM:") < code.index(dispatch), "SPOR64T precedes ASM")
    for token in ("SPOR64V:", "SPOR64X:", "FLU:", "SPOSTATE:", "SPOLEAK:"):
        require(token not in code, f"forbidden host token: {token}")


def check_adapter(text: str) -> None:
    code = packed(no_fortran_comments(text))
    require(code.count("SUBROUTINESPOR64T(") == 1, "SPOR64T count differs")
    call = (
        "CALLSPOR64_B2T_HOST_STEP(KENTRY(1),KENTRY(2),SYSTEMS,KENTRY(6),"
        "STATUS,CUTOFF_BY_PLANE,.TRUE.)"
    )
    require(code.count(call) == 1, "B2T production call differs")
    require("IF(STATUS/=SPOR64_B2T_RETURNED)THEN" in code,
            "strict returned status gate differs")
    require("B2V-OBSERVER" not in text and "WRITE(6" not in code,
            "production adapter contains observer output")


def check_chain(b2s_text: str, b2t_text: str) -> None:
    s = packed(no_fortran_comments(b2s_text))
    t = packed(no_fortran_comments(b2t_text))
    require("DOPLANE=1,NSNAP" in s, "canonical three-plane loop missing")
    require(s.count("CALLSPOR64_B2B_INGRESS(") == 1, "B2B call count differs")
    require("IF(RADIAL_STATUS/=SPOR64_B2C_HOST_COMMITTED)THEN" in s,
            "radial status gate differs")
    require(s.count("CALLSPOR64_B2R_COLLECT(") == 1, "B2R count differs")
    require(t.count("CALLSPOR64_B2S_HOST_BRIDGE(") == 1, "B2S call differs")
    for token in ("RELAX", "DAMP", "CLIP", "EMPIRICAL"):
        require(token not in s + t, f"forbidden chain token: {token}")


def load_bounded(path: Path):
    spec = importlib.util.spec_from_file_location("b2z_bounded", path)
    require(spec is not None and spec.loader is not None, "bounded import failed")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_bounded(path: Path) -> None:
    module = load_bounded(path)
    require(module.PROFILES["dragon"] == {
        "wall_seconds": 60,
        "cpu_seconds": 55,
        "rss_bytes": 2 * 1024**3,
        "file_bytes": 512 * 1024**2,
        "log_bytes": 64 * 1024**2,
    }, "Dragon profile differs")
    require(module.PROFILES["prepare"]["wall_seconds"] == 30,
            "preparer wall cap differs")
    require(module.PROFILES["posterior"]["wall_seconds"] == 30,
            "posterior wall cap differs")
    require(module.RESOURCE_CLASS["dragon"] ==
            "INVALID-RUNTIME-BUDGET-NO-STAGED-RETURNED",
            "Dragon resource class differs")
    text = path.read_text()
    for token in (
        "class ManagedInterruption(Exception)",
        "start_new_session=True",
        "RLIMIT_CPU",
        "RLIMIT_FSIZE",
        "RLIMIT_CORE",
        "os.killpg(process.pid, signal.SIGTERM)",
        "os.killpg(process.pid, signal.SIGKILL)",
        "except BaseException:",
        "finally:",
        "signal.SIGHUP",
        "signal.SIGINT",
        "signal.SIGTERM",
    ):
        require(token in text, f"bounded helper missing: {token}")


def check_publisher(text: str) -> None:
    for token in (
        "renameatx_np",
        "RENAME_EXCL = 0x00000004",
        "AT_FDCWD = -2",
        "source.parent != target.parent",
        'lstat_absent(target, "publication target")',
        "stat.S_ISDIR(status.st_mode)",
        "stat.S_ISLNK(status.st_mode)",
        "source_status.st_dev != parent_status.st_dev",
        "published directory identity differs",
    ):
        require(token in text, f"publisher missing: {token}")
    for forbidden in (
        "os.replace(", "os.rename(", "shutil.move(", "RENAME_SWAP",
    ):
        require(forbidden not in text, f"publisher has overwrite fallback: {forbidden}")
    require(text.count("result = rename(") == 1, "publisher rename count differs")


def check_runner(text: str) -> None:
    require("RUN_B2Z=$" + "{RUN_B2Z:-0}" in text, "activation must default off")
    require(text.count('python3 "$BOUNDED" dragon ') == 1,
            "Dragon activation count differs")
    require(text.count('python3 "$PUBLISHER" "$PUBLISH_STAGE" "$ARTIFACT_DIR"') == 1,
            "publication call count differs")
    for token in (
        'ARTIFACT_DIR="$ARTIFACT_PARENT/iterative-b2z"',
        'LOCK_DIR="$ARTIFACT_PARENT/.iterative-b2z.lock"',
        'ATTEMPT_DIR="$ARTIFACT_PARENT/.iterative-b2z-attempted"',
        'if ! mkdir "$ATTEMPT_DIR"',
        "EXPECTED_RETURNED_HASH=dd41a37d484b85612a495ff7b1f2233a53fbae1b462d89bd84db2a8809cef054",
        "EXPECTED_RETURNED_BYTES=231572260",
        "SPOR64_B2U SPOR64_B2W SPOR64_B2X",
        '-c "$SOURCE_DIR/$source.f90"',
        '"$HOST_DIR/SPOR64_B2W.o"',
        '"$HOST_DIR/SPOR64_B2X.o"',
        '-o "$HOST_DIR/SPOR64_B2X.o"',
        "for symbol in spor64_a9_MOD_flu2dr64_core "
        "spor64_a8_MOD_doorfv64",
        "spomoc_audit_MOD_spomoc_active",
        "PRODUCTION-SPOR64T=PRIVATE-LINKED",
        "VALIDATION-OBSERVER-SPOR64T-EXECUTIONS=0",
        "ONE-REAL-PRODUCTION-RETURNED-BUT-NOT-B2Y-ADMISSIBLE",
        "NO-PUBLISH NO-B2Y NO-RETRY",
        "RENAMEATX_NP-RENAME_EXCL",
        'PUBLISH_STAGE=$(mktemp -d "$ARTIFACT_PARENT/.iterative-b2z-publish.XXXXXX")',
        'FINAL_OWNED_ID=$(stat -f',
        'PUBLISH_STAGE_ID=$(stat -f',
        'LOCK_ID=$(stat -f',
        'ATTEMPT_ID=$(stat -f',
        'find "$ARTIFACT_DIR" -mindepth 1 -maxdepth 1',
        "owned_final_id=$PUBLISH_STAGE_ID",
        '[ "$(stat -f \'%d:%i\' "$ARTIFACT_DIR")" = "$owned_final_id" ]',
        "RETRY-AFTER-ANY-ATTEMPT=DISABLED",
    ):
        require(token in text, f"runner missing: {token}")
    symbol_loop = (
        "for symbol in spor64_a9_MOD_flu2dr64_core "
        "spor64_a8_MOD_doorfv64"
    )
    require(text.count(symbol_loop) == 1,
            "frozen production symbol loop count differs")
    for forbidden in (
        "b2z_spor64t_observer", "RUN_B2Y=", "killall", "pkill",
        "PRESERVE_B2V", "&& +", "printf '%s\\n' +",
    ):
        require(forbidden not in text, f"runner has forbidden token: {forbidden}")
    off = text.index('if [ "$RUN_B2Z" = 0 ]')
    lock = text.index('if ! mkdir "$LOCK_DIR"')
    attempt = text.index('if ! mkdir "$ATTEMPT_DIR"')
    started = text.index("DRAGON_STARTED=1")
    dragon = text.index('python3 "$BOUNDED" dragon ')
    posterior_b = text.index('"$CASE_DIR/posterior_b.log" projected.xsm returned.xsm')
    identity = text.index('if [ "$RETURNED_HASH" != "$EXPECTED_RETURNED_HASH" ]')
    stage = text.index('PUBLISH_STAGE=$(mktemp -d')
    publish = text.index('python3 "$PUBLISHER" "$PUBLISH_STAGE" "$ARTIFACT_DIR"')
    final_check = text.index('cmp "$CASE_DIR/returned.xsm" "$ARTIFACT_DIR/returned.xsm"')
    summary = text.index("sed -n '1,80p' \"$ARTIFACT_DIR/runtime_result.txt\"")
    require(off < lock < attempt < started < dragon < posterior_b < identity < stage <
            publish < final_check < summary, "runner lifecycle order differs")
    cleanup = text[text.index("cleanup()"):text.index("LC_ALL=C")]
    for token in (
        "stat -f '%d:%i' \"$ARTIFACT_DIR\"",
        "stat -f '%d:%i' \"$PUBLISH_STAGE\"",
        "stat -f '%d:%i' \"$LOCK_DIR\"",
    ):
        require(token in cleanup, f"owned cleanup guard missing: {token}")
    preserve = cleanup.index('PRESERVE_B2Z_FAILURE')
    require(cleanup.index('FINAL_OWNED_ID') < preserve and
            cleanup.index('PUBLISH_STAGE_ID') < preserve and
            cleanup.index('LOCK_ID') < preserve,
            "owned rollback must precede failure preservation")
    require('rm -rf "$ATTEMPT_DIR"' not in text and
            'rmdir "$ATTEMPT_DIR"' not in text,
            "durable attempt sentinel must never be rolled back")


def check_posterior(text: str) -> None:
    code = packed(no_fortran_comments(text))
    require("PROGRAMCHECK_B2Z_REAL_RETURNED" in code, "posterior name differs")
    require("B2ZREALRETURNEDPOSTERIORPASS" in code, "posterior marker missing")
    require("CALLLCMOP" in code and "CALLLCMCL" in code,
            "posterior read-only lifecycle missing")
    for token in (
        "USESPOR64_", "CALLSPOR64", "CALLASM", "CALLFLU", "CALLSPOMOC",
        "CALLSPOSTATE", "CALLSPOLEAK",
    ):
        require(token not in code, f"posterior links production token: {token}")


def check_documents(manifest_text: str, readme: str) -> None:
    manifest = json.loads(manifest_text)
    require(manifest["deployment_default"] == "off", "manifest default differs")
    require(manifest["receipt"] == "frozen", "manifest receipt is not frozen")
    require(manifest["activation_count"]["dragon_maximum"] == 1,
            "manifest activation count differs")
    require(manifest["activation_count"]["automatic_retries"] == 0,
            "manifest retry count differs")
    attempt = manifest["durable_attempt_guard"]
    require(attempt["path"] ==
            "validation/artifacts/.iterative-b2z-attempted",
            "manifest attempt path differs")
    require(attempt["created_atomically_immediately_before_the_only_dragon"]
            is True and attempt["removed_after_failure"] is False,
            "manifest durable attempt lifecycle differs")
    require(manifest["identity_gate"]["bytes"] == 231572260,
            "manifest identity bytes differ")
    require(manifest["identity_gate"]["sha256"] ==
            "dd41a37d484b85612a495ff7b1f2233a53fbae1b462d89bd84db2a8809cef054",
            "manifest identity hash differs")
    require(manifest["publication"]["atomic_no_replace"] ==
            "Darwin renameatx_np RENAME_EXCL",
            "manifest publication differs")
    require(all(value == 0 for value in manifest["added_controls"].values()),
            "manifest adds a control")
    for token in (
        "privately linked production-source",
        "solver-independent",
        "retry of B2v",
        "does not expose or claim",
        "No second Dragon",
        "complete Picard map",
        "validation/artifacts/.iterative-b2z-attempted",
        "second Dragon is mechanically refused",
        "sole authorized B2z activation completed successfully",
        "control-flow/provenance inference",
        "not separate runtime print counters",
        "outer timing was not retained",
        "must never be run again",
    ):
        require(token in readme, f"README missing boundary: {token}")


def check_frozen_result(runtime_text: str, manifest_text: str) -> None:
    require(len(runtime_text.splitlines()) == 20,
            "runtime transcript line count differs")
    require(len(runtime_text.encode()) == 1735,
            "runtime transcript byte count differs")
    require(
        hashlib.sha256(runtime_text.encode()).hexdigest()
        == "6627924e8bed19e23537ede946c3c7c2cc7dcf2f53b84055a4b8e047fe444850",
        "runtime transcript hash differs",
    )
    for line in (
        "CLASSIFICATION=ONE-REAL-PRODUCTION-B2V-BYTE-IDENTICAL-RETURNED-STAGED",
        "DRAGON-EXECUTIONS=1 SPOTSTEPR64-CALLS=1 ASM-EXECUTIONS=3 PRODUCTION-SPOR64T-EXECUTIONS=1 RETRIES=0",
        "VALIDATION-OBSERVER-SPOR64T-EXECUTIONS=0 RADIAL-CONT-RETURNS=3",
        "RETURNED-SHA256=dd41a37d484b85612a495ff7b1f2233a53fbae1b462d89bd84db2a8809cef054 BYTES=231572260",
        "DRAGON-LOG-SHA256=13dfd1926df28699add09267ca8ce9d9f161ae84b6332fc490322b5293cab6f3",
        "POSTERIOR-LOG-SHA256=0d0d6216c8336058c7451e5813cb3dc9aa7cd7283e520e95df38c775a9eeb512 REPORTS-IDENTICAL=YES",
        "DURABLE-ATTEMPT-SENTINEL=16777230:32670273 RETRY-AFTER-ANY-ATTEMPT=DISABLED",
        "OUTER-PICARD-MAP=NOT-COMPLETED OUTER-PICARD-CONVERGENCE=NOT-EVALUATED",
        "RECEIPT=PENDING-RUNTIME-FREEZE PARENT=B2u B2V=HISTORICAL-CONTENT-REFERENCE",
    ):
        require(runtime_text.count(line + "\n") == 1,
                f"runtime result differs: {line}")
    result = json.loads(manifest_text).get("runtime_result", {})
    require(result.get("status") == "PASS", "manifest runtime status differs")
    require(result.get("scientific_classification") ==
            "ONE-REAL-PRODUCTION-B2V-BYTE-IDENTICAL-RETURNED-STAGED",
            "manifest runtime classification differs")
    require(result.get("dragon_executions") == 1 and
            result.get("automatic_retries") == 0,
            "manifest runtime census differs")
    require(result.get("production_spor64t_executions") == 1 and
            result.get("validation_observer_spor64t_executions") == 0 and
            result.get("radial_cont_returns") == 3,
            "manifest production route census differs")
    require("not three independent runtime prints" in
            result.get("radial_cont_returns_evidence", ""),
            "manifest internal route inference boundary differs")
    require(result.get("returned_sha256") ==
            "dd41a37d484b85612a495ff7b1f2233a53fbae1b462d89bd84db2a8809cef054" and
            result.get("returned_bytes") == 231572260,
            "manifest returned identity differs")
    require(result.get("artifact_manifest_sha256") ==
            "22949de59c8662c43ca7f7ec3293e27287571ae85b58ecddf24fc2148a67ca0f",
            "manifest artifact manifest identity differs")
    require(result.get("artifact_manifest_bytes") == 483 and
            result.get("artifact_inventory_regular_files") == 7,
            "manifest artifact dimensions differ")
    require(result.get("artifact_runtime_result_sha256") ==
            "6627924e8bed19e23537ede946c3c7c2cc7dcf2f53b84055a4b8e047fe444850",
            "manifest artifact transcript identity differs")
    require(result.get("runtime_transcript_lines") == 20 and
            result.get("runtime_transcript_bytes") == 1735,
            "manifest transcript dimensions differ")
    require(result.get("durable_attempt_sentinel_identity") ==
            "16777230:32670273",
            "manifest attempt identity differs")
    require("not a frozen result field" in
            json.loads(manifest_text).get("elapsed_time_evidence", ""),
            "manifest elapsed evidence boundary differs")


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def check_receipt(receipt_text: str) -> None:
    require(receipt_text.endswith("\n"), "receipt lacks terminal newline")
    entries: dict[str, str] = {}
    for line in receipt_text.splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\x00-\x1f]+)", line)
        require(match is not None, f"malformed receipt line: {line!r}")
        expected, relative = match.groups()
        require(relative not in entries, f"duplicate receipt path: {relative}")
        require(not Path(relative).is_absolute() and ".." not in Path(relative).parts,
                f"unsafe receipt path: {relative}")
        entries[relative] = expected
    require(set(entries) == EXPECTED_RECEIPT_PATHS,
            "receipt inventory differs")
    for relative, expected in entries.items():
        path = ROOT / relative
        require(path.is_file() and not path.is_symlink(),
                f"receipt input differs: {relative}")
        require(digest(path) == expected, f"receipt hash differs: {relative}")


def main() -> None:
    for path in (
        RUNNER, BOUNDED, PUBLISHER, DECK, POSTERIOR, MANIFEST, README,
        RUNTIME_RESULT, RECEIPT,
        HOST, ADAPTER, B2S, B2T,
    ):
        require(path.is_file(), f"missing input: {path}")
    check_deck(DECK.read_text())
    check_host(HOST.read_text())
    check_adapter(ADAPTER.read_text())
    check_chain(B2S.read_text(), B2T.read_text())
    check_bounded(BOUNDED)
    check_publisher(PUBLISHER.read_text())
    check_runner(RUNNER.read_text())
    check_posterior(POSTERIOR.read_text())
    check_documents(MANIFEST.read_text(), README.read_text())
    check_frozen_result(RUNTIME_RESULT.read_text(), MANIFEST.read_text())
    check_receipt(RECEIPT.read_text())
    print("B2Z STATIC ONE-REAL-PRODUCTION-RETURNED-STAGING PASS")
    print("B2Z ACTIVATION=DEFAULT-OFF DRAGON-MAX=1 RETRY=0")
    print("B2Z ROUTE=ASMx3->PRODUCTION-SPOR64T->RETURNED")
    print("B2Z POSTERIOR=GANLIB-ONLYx2 PUBLISH=ATOMIC-NO-REPLACE")
    print("B2Z AXIAL=0 OUTER-PICARD=NOT-EVALUATED ADDED-CONTROLS=0")
    print("B2Z FROZEN-RESULT=ONE-PRODUCTION-RETURNED-STAGED RECEIPT=VERIFIED")


if __name__ == "__main__":
    main()
