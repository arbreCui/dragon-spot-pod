#!/usr/bin/env python3
"""Fail-closed verifier for the published raw-MOC ULP bridge result."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import stat


ROOT = Path(__file__).resolve().parents[2]
ITERATIVE = ROOT / "validation" / "iterative"
ARTIFACT = ROOT / "validation" / "artifacts" / "raw-moc-ulp-bridge"
RECEIPT = ITERATIVE / "raw_moc_ulp_bridge_result_receipt.sha256"

RUN_COMMIT = "0a7e0e3fa951bcb12a5cd29dbffbe4fb3de44618"
PROTOCOL_SHA256 = (
    "a2ad98ff63500a85e4d161468d9c2691403f104a4732179d48e8817232d549a3"
)
IMPLEMENTATION_MANIFEST_SHA256 = (
    "0a4f40a0be68c1f961ac239ec5188d7e9bd797b33b831c53d76a01cd392ae9bb"
)
ARTIFACT_MANIFEST_SHA256 = (
    "c8aacee484a5afdf3684cad4f87c5150093ee7fd1afda232ab6f7265f869b31c"
)

EXPECTED_PUBLIC_HASHES = {
    "validation/iterative/raw_moc_ulp_bridge_status.txt":
        "c19f5a7879daae494ebdd6542b6b50f9d06a3dd82875964bd3db2cb6c295c813",
    "validation/iterative/raw_moc_ulp_bridge_result.txt":
        "25c941b02b42d120864f7924437a5b48a7ac685873790b625809be98e0a63e94",
    "validation/iterative/raw_moc_ulp_bridge_result.md":
        "e7ffbcd1e483e1fc563a728559ceeaaed1a6d7ca8225cd03eec4d19bec75a272",
    "validation/iterative/raw_moc_ulp_bridge_protocol.json":
        PROTOCOL_SHA256,
    "validation/iterative/raw_moc_ulp_bridge_implementation.sha256":
        IMPLEMENTATION_MANIFEST_SHA256,
}

EXPECTED_IMPLEMENTATION = [
    (
        "a2ad98ff63500a85e4d161468d9c2691403f104a4732179d48e8817232d549a3",
        "validation/iterative/raw_moc_ulp_bridge_protocol.json",
    ),
    (
        "859c824488a211b41214b3559756047a6ffdd01527c13cd04a799e5b9d9653b6",
        "validation/iterative/check_raw_moc_ulp_bridge_xsm.f90",
    ),
    (
        "fd0359866d74f0a93bd78ce688855f81934ad4f6586f22d9f2978bbcb54d3201",
        "validation/iterative/make_raw_moc_ulp_bridge_fixture.f90",
    ),
    (
        "3fa5d8f978cef96be3fcd98b38315bb91cb1eef0bdc4d15ece946b6738f9e321",
        "validation/iterative/check_raw_moc_ulp_bridge_log.py",
    ),
    (
        "a8775d0e352da01c86531199f552eae9a49688f4449bb4adcd82dd6bdc224a56",
        "validation/iterative/run_raw_moc_ulp_bridge_checker_test.sh",
    ),
    (
        "95e46f797aa65fef25c1fc7c870e98ff41094b9fcd2883e513695039a87daed6",
        "validation/iterative/run_raw_moc_ulp_bridge_audit.sh",
    ),
    (
        "7dc03f0af8c4816279fc480f574ee50a4083b05a13f20609494a8bbb058f520b",
        "validation/iterative/check_raw_moc_ulp_bridge_contract.py",
    ),
]

EXPECTED_ARTIFACT = [
    (
        "d303df70625424cc74659b197217d6b14395a715b652ba8ee78bbc17880d4a61",
        "check_raw_moc_ulp_bridge_xsm",
    ),
    (
        "152d60ae38a701a6d2908111f163a7fa91e48d5ff4ff13c896cda254c67866ec",
        "checker_a.log",
    ),
    (
        "152d60ae38a701a6d2908111f163a7fa91e48d5ff4ff13c896cda254c67866ec",
        "checker_b.log",
    ),
    (
        "bbf1c46bb7cad5aea1a408c222564077fff7fa3c3627285750721e8010207ff3",
        "compact.log",
    ),
    (
        "030cb4cb8cc40f50e7a26d933074e5b86e1e81568771c7fa6dd505c39c8864b5",
        "fixture_test.log",
    ),
    (
        "29a7afb1901ee97ce18ca1b88d920206762dc84428fb7212246a43bdddd40f70",
        "full.log",
    ),
    (
        "de2dba33c0856d8db0af1c37ca12e1a48f8889e1aebb4759e9b28e10c244d138",
        "dependency_hashes.sha256",
    ),
    (
        IMPLEMENTATION_MANIFEST_SHA256,
        "implementation.sha256",
    ),
    (
        "362361ca3d2c6dcb6cf844eeabe08ce937126d0aae4b1b3bcd519f9de4098792",
        "inputs_after.log",
    ),
    (
        "a13d4a32fd2f4dff0029f2139aafd879297443d9c3e79f68fa830c40bfc478eb",
        "inputs_before.sha256",
    ),
    (
        "7dc03f0af8c4816279fc480f574ee50a4083b05a13f20609494a8bbb058f520b",
        "implementation/validation/iterative/check_raw_moc_ulp_bridge_contract.py",
    ),
    (
        "3fa5d8f978cef96be3fcd98b38315bb91cb1eef0bdc4d15ece946b6738f9e321",
        "implementation/validation/iterative/check_raw_moc_ulp_bridge_log.py",
    ),
    (
        "859c824488a211b41214b3559756047a6ffdd01527c13cd04a799e5b9d9653b6",
        "implementation/validation/iterative/check_raw_moc_ulp_bridge_xsm.f90",
    ),
    (
        "fd0359866d74f0a93bd78ce688855f81934ad4f6586f22d9f2978bbcb54d3201",
        "implementation/validation/iterative/make_raw_moc_ulp_bridge_fixture.f90",
    ),
    (
        PROTOCOL_SHA256,
        "implementation/validation/iterative/raw_moc_ulp_bridge_protocol.json",
    ),
    (
        "95e46f797aa65fef25c1fc7c870e98ff41094b9fcd2883e513695039a87daed6",
        "implementation/validation/iterative/run_raw_moc_ulp_bridge_audit.sh",
    ),
    (
        "a8775d0e352da01c86531199f552eae9a49688f4449bb4adcd82dd6bdc224a56",
        "implementation/validation/iterative/run_raw_moc_ulp_bridge_checker_test.sh",
    ),
    (
        "d0c6ac6155d1e890969211c4112ceeafab1fe9d26a69a919181bd80b46668a55",
        "native_a.log",
    ),
    (
        "d0c6ac6155d1e890969211c4112ceeafab1fe9d26a69a919181bd80b46668a55",
        "native_b.log",
    ),
    (
        "3309bd89d8094915ad458e4a4fa612a9e3d51fff26bc9a587d800b74c7b99569",
        "parent_native.log",
    ),
    (
        "8a57826442fb9be160fc3c2ce0b9e08e7dbe12ec71992fd14c9f5351022ed930",
        "parent_stationary.log",
    ),
    (
        "aeec42c12eb4fa7a2f93d74e5a97ec2063f8fa046bf39fa963a132881d597533",
        "postflight.log",
    ),
    (
        "aeec42c12eb4fa7a2f93d74e5a97ec2063f8fa046bf39fa963a132881d597533",
        "preflight.log",
    ),
    (
        PROTOCOL_SHA256,
        "protocol.json",
    ),
    (
        "6b725befd48af580dcfc155c1f3bc6c45b39fc1ddf3117048a7d61768849876a",
        "reader.nm",
    ),
    (
        "e8c48b6569697796374d9a482ebf77cd4fb77150cdfb78294099b9b0c221edf6",
        "reader.object.nm",
    ),
    (
        "fc7f7430f14235cb57925ebdf97b452931227a658ad00ecc5ab32dbd9f27a62d",
        "run_commit.txt",
    ),
    (
        "51a56afdde0ef95995de7d7ee591c8bf2ab229fa20d5aaa405c2514fa1ba0440",
        "selftest_a.log",
    ),
    (
        "51a56afdde0ef95995de7d7ee591c8bf2ab229fa20d5aaa405c2514fa1ba0440",
        "selftest_b.log",
    ),
    (
        "6dbc44944665d1a92a78dfb7cdac54fcdf4713b83fa919902737babadfc25447",
        "stationary_a.log",
    ),
    (
        "6dbc44944665d1a92a78dfb7cdac54fcdf4713b83fa919902737babadfc25447",
        "stationary_b.log",
    ),
    (
        "9f95a3a15b2687d7bd0a7022b0e07db7067686a7b39c054852e92b68a91f4222",
        "toolchain.txt",
    ),
]

TRACKED_RECEIPT_PATHS = (
    "validation/iterative/raw_moc_ulp_bridge_status.txt",
    "validation/iterative/raw_moc_ulp_bridge_result.txt",
    "validation/iterative/raw_moc_ulp_bridge_result.md",
    "validation/iterative/check_raw_moc_ulp_bridge_result.py",
    "validation/iterative/raw_moc_ulp_bridge_protocol.json",
    "validation/iterative/raw_moc_ulp_bridge_implementation.sha256",
    "validation/iterative/check_raw_moc_ulp_bridge_xsm.f90",
    "validation/iterative/check_raw_moc_ulp_bridge_log.py",
    "validation/iterative/run_raw_moc_ulp_bridge_audit.sh",
    "validation/iterative/run_raw_moc_ulp_bridge_checker_test.sh",
    "validation/iterative/check_raw_moc_ulp_bridge_contract.py",
    "README.md",
    "SPOT_doc/validation_plan.md",
    "validation/iterative/README.md",
    "validation/run_fast.sh",
)

ARTIFACT_RECEIPT_PATHS = (
    "validation/artifacts/raw-moc-ulp-bridge/artifact_manifest.sha256",
    "validation/artifacts/raw-moc-ulp-bridge/full.log",
    "validation/artifacts/raw-moc-ulp-bridge/compact.log",
    "validation/artifacts/raw-moc-ulp-bridge/checker_a.log",
    "validation/artifacts/raw-moc-ulp-bridge/checker_b.log",
    "validation/artifacts/raw-moc-ulp-bridge/run_commit.txt",
    "validation/artifacts/raw-moc-ulp-bridge/inputs_after.log",
    "validation/artifacts/raw-moc-ulp-bridge/preflight.log",
    "validation/artifacts/raw-moc-ulp-bridge/postflight.log",
)

EXPECTED_RECEIPT_PATHS = TRACKED_RECEIPT_PATHS + ARTIFACT_RECEIPT_PATHS

EXPECTED_RECEIPT_ARTIFACT_HASHES = {
    "validation/artifacts/raw-moc-ulp-bridge/artifact_manifest.sha256":
        ARTIFACT_MANIFEST_SHA256,
    "validation/artifacts/raw-moc-ulp-bridge/full.log":
        "29a7afb1901ee97ce18ca1b88d920206762dc84428fb7212246a43bdddd40f70",
    "validation/artifacts/raw-moc-ulp-bridge/compact.log":
        "bbf1c46bb7cad5aea1a408c222564077fff7fa3c3627285750721e8010207ff3",
    "validation/artifacts/raw-moc-ulp-bridge/checker_a.log":
        "152d60ae38a701a6d2908111f163a7fa91e48d5ff4ff13c896cda254c67866ec",
    "validation/artifacts/raw-moc-ulp-bridge/checker_b.log":
        "152d60ae38a701a6d2908111f163a7fa91e48d5ff4ff13c896cda254c67866ec",
    "validation/artifacts/raw-moc-ulp-bridge/run_commit.txt":
        "fc7f7430f14235cb57925ebdf97b452931227a658ad00ecc5ab32dbd9f27a62d",
    "validation/artifacts/raw-moc-ulp-bridge/inputs_after.log":
        "362361ca3d2c6dcb6cf844eeabe08ce937126d0aae4b1b3bcd519f9de4098792",
    "validation/artifacts/raw-moc-ulp-bridge/preflight.log":
        "aeec42c12eb4fa7a2f93d74e5a97ec2063f8fa046bf39fa963a132881d597533",
    "validation/artifacts/raw-moc-ulp-bridge/postflight.log":
        "aeec42c12eb4fa7a2f93d74e5a97ec2063f8fa046bf39fa963a132881d597533",
}

EXPECTED_STATUS = [
    "RAW-MOC-ULP RESULT DESCRIPTIVE-ULP-CENSUS",
    f"RAW-MOC-ULP RUN-COMMIT {RUN_COMMIT}",
    "RAW-MOC-ULP TRANSPORT-RUNS 0",
    "RAW-MOC-ULP OPERATOR-APPLICATIONS 0",
    "RAW-MOC-ULP INPUTS FROZEN-HASHED-READ-ONLY",
    "RAW-MOC-ULP READER GANLIB-ONLY REPLAYS=4 BYTE-IDENTICAL-PAIRS=2",
    "RAW-MOC-ULP CHECKER INDEPENDENT-RNE-REPLAY RUNS=2 BYTE-IDENTICAL",
    "RAW-MOC-ULP LEDGERS 4 ROWS=11840",
    "RAW-MOC-ULP RAW-BRIDGE DECLARED-DIRECT-PROJECTION",
    "RAW-MOC-ULP PRODUCTION-STEP PRE-TO-OFF",
    "RAW-MOC-ULP LEDGERS NOT-SUBTRACTED",
    "RAW-MOC-ULP ACCEPTANCE-THRESHOLD NONE",
    "RAW-MOC-ULP EMPIRICAL-PARAMETERS NONE",
    "RAW-MOC-ULP ATTRIBUTION NONE",
    "RAW-MOC-ULP ARM-RANKING NOT-AUTHORIZED",
    "RAW-MOC-ULP TRANSPORT-ERROR-BOUND NOT-ESTABLISHED",
    "RAW-MOC-ULP OUTER-CONVERGENCE NOT-EVALUATED",
    "RAW-MOC-ULP STAGE4 NOT-AUTHORIZED",
    f"RAW-MOC-ULP ARTIFACT-MANIFEST {ARTIFACT_MANIFEST_SHA256}",
    "RAW-MOC-ULP COMPLETE",
]

EXPECTED_CENSUS = {
    ("NATIVE", "RAW-BRIDGE"): {
        "TOTAL": 2960,
        "UNCHANGED": 135,
        "UPWARD": 977,
        "DOWNWARD": 1848,
        "ADJACENT": 248,
        "RAW-EXACT": 0,
        "ROUND-COLLAPSED-NONZERO": 135,
        "ROUNDED-TO-ZERO": 0,
        "ROUNDED-SUBNORMAL": 0,
        "MAX-STEPS": 877,
        "MAX-TIES": [(345, 4, 4, -877, 877)],
    },
    ("NATIVE", "PRODUCTION-STEP"): {
        "TOTAL": 2960,
        "UNCHANGED": 288,
        "UPWARD": 136,
        "DOWNWARD": 2536,
        "ADJACENT": 265,
        "MAX-STEPS": 17,
        "MAX-TIES": [
            (142, 6, 6, -17, 17),
            (142, 7, 7, -17, 17),
            (142, 8, 8, -17, 17),
        ],
    },
    ("STATIONARY", "RAW-BRIDGE"): {
        "TOTAL": 2960,
        "UNCHANGED": 133,
        "UPWARD": 975,
        "DOWNWARD": 1852,
        "ADJACENT": 251,
        "RAW-EXACT": 0,
        "ROUND-COLLAPSED-NONZERO": 133,
        "ROUNDED-TO-ZERO": 0,
        "ROUNDED-SUBNORMAL": 0,
        "MAX-STEPS": 878,
        "MAX-TIES": [(345, 4, 4, -878, 878)],
    },
    ("STATIONARY", "PRODUCTION-STEP"): {
        "TOTAL": 2960,
        "UNCHANGED": 272,
        "UPWARD": 88,
        "DOWNWARD": 2600,
        "ADJACENT": 220,
        "MAX-STEPS": 12,
        "MAX-TIES": [
            (102, region, region, -12, 12) for region in range(1, 9)
        ],
    },
}

SHA_LINE = re.compile(r"([0-9a-f]{64})  ([A-Za-z0-9_./-]+)")
LEDGER_LINE = re.compile(
    r"RAW-MOC-ULP (NATIVE|STATIONARY) "
    r"(RAW-BRIDGE|PRODUCTION-STEP) LEDGER "
)
HIST_LINE = re.compile(
    r"RAW-MOC-ULP (NATIVE|STATIONARY) "
    r"(RAW-BRIDGE|PRODUCTION-STEP) HIST (-?[0-9]+) ([1-9][0-9]*)"
)


def fail(message: str) -> None:
    raise SystemExit(f"RAW-MOC-ULP RESULT FAIL: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def sha256(path: Path) -> str:
    require(path.is_file() and not path.is_symlink(), f"invalid file: {path}")
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_bytes(path: Path) -> bytes:
    require(path.is_file() and not path.is_symlink(), f"invalid file: {path}")
    raw = path.read_bytes()
    require(raw.endswith(b"\n"), f"missing final newline: {path}")
    require(b"\r" not in raw and b"\x00" not in raw, f"noncanonical file: {path}")
    return raw


def ascii_lines(path: Path) -> list[str]:
    raw = canonical_bytes(path)
    try:
        return raw.decode("ascii").splitlines()
    except UnicodeDecodeError as exc:
        fail(f"non-ASCII file {path}: {exc}")


def parse_sha_lines(path: Path) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for line in ascii_lines(path):
        match = SHA_LINE.fullmatch(line)
        require(match is not None, f"malformed SHA-256 row in {path}")
        digest, relative = match.groups()
        candidate = Path(relative)
        require(
            not candidate.is_absolute()
            and ".." not in candidate.parts
            and relative == candidate.as_posix(),
            f"unsafe SHA-256 path in {path}",
        )
        rows.append((digest, relative))
    require(
        len({relative for _, relative in rows}) == len(rows),
        f"duplicate SHA-256 path in {path}",
    )
    return rows


def expected_result_lines() -> list[str]:
    result: list[str] = []
    for arm in ("NATIVE", "STATIONARY"):
        result.extend(
            [
                f"RAW-MOC-ULP ARM {arm}",
                "RAW-MOC-ULP DIMS 370 8 14",
                "RAW-MOC-ULP ROUNDING IEEE-BINARY64-TO-BINARY32-RNE-ONCE",
                "RAW-MOC-ULP RAW-BRIDGE DECLARED-DIRECT-PROJECTION",
            ]
        )
        for ledger in ("RAW-BRIDGE", "PRODUCTION-STEP"):
            census = EXPECTED_CENSUS[(arm, ledger)]
            fields = [
                "TOTAL",
                "UNCHANGED",
                "UPWARD",
                "DOWNWARD",
                "ADJACENT",
            ]
            if ledger == "RAW-BRIDGE":
                fields.extend(
                    [
                        "RAW-EXACT",
                        "ROUND-COLLAPSED-NONZERO",
                        "ROUNDED-TO-ZERO",
                        "ROUNDED-SUBNORMAL",
                    ]
                )
            fields.append("MAX-STEPS")
            result.extend(
                f"RAW-MOC-ULP {arm} {ledger} {field} {census[field]}"
                for field in fields
            )
            result.extend(
                "RAW-MOC-ULP "
                f"{arm} {ledger} MAX-TIE {' '.join(map(str, tie))}"
                for tie in census["MAX-TIES"]
            )
        result.extend(
            [
                f"RAW-MOC-ULP {arm} LEDGERS NOT-SUBTRACTED",
                f"RAW-MOC-ULP {arm} ATTRIBUTION NONE",
                f"RAW-MOC-ULP {arm} ACCEPTANCE-THRESHOLD NONE",
                f"RAW-MOC-ULP {arm} CLASSIFICATION DESCRIPTIVE-ULP-CENSUS",
                f"RAW-MOC-ULP {arm} OUTER-CONVERGENCE NOT-EVALUATED",
                f"RAW-MOC-ULP {arm} STAGE4 NOT-AUTHORIZED",
                f"RAW-MOC-ULP {arm} COMPLETE",
            ]
        )
    require(len(result) == 67, "internal result grammar census")
    return result


def verify_public_hashes() -> None:
    for relative, expected in EXPECTED_PUBLIC_HASHES.items():
        require(sha256(ROOT / relative) == expected, f"public hash differs: {relative}")


def verify_protocol() -> None:
    path = ITERATIVE / "raw_moc_ulp_bridge_protocol.json"
    try:
        protocol = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(f"protocol cannot be decoded: {exc}")
    require(protocol["status"] == "FROZEN-BEFORE-IMPLEMENTATION", "protocol status")
    require(protocol["scope"]["transport_runs"] == 0, "protocol transport count")
    require(
        protocol["scope"]["operator_applications"] == 0,
        "protocol operator count",
    )
    require(protocol["acceptance"]["threshold"] is None, "protocol threshold")
    limits = protocol["interpretation_limits"]
    require(
        limits
        == {
            "subtract_RAW_BRIDGE_and_PRODUCTION_STEP_ledgers": False,
            "attribute_to_binary32": False,
            "call_projection_actual_production_storage_loss": False,
            "attribute_to_GMRES_ACA_SCR_rebalancing_or_acceleration": False,
            "rank_Native_vs_Stationary": False,
            "transport_residual_or_error_bound": False,
            "inner_or_outer_convergence": False,
            "authorize_Stage4_or_Stage5": False,
            "introduce_model_term_relaxation_clipping_or_empirical_parameter": False,
        },
        "protocol interpretation limits",
    )


def verify_implementation() -> None:
    manifest = ITERATIVE / "raw_moc_ulp_bridge_implementation.sha256"
    require(parse_sha_lines(manifest) == EXPECTED_IMPLEMENTATION, "implementation manifest")
    for expected, relative in EXPECTED_IMPLEMENTATION:
        require(sha256(ROOT / relative) == expected, f"implementation differs: {relative}")


def verify_status_and_result() -> list[str]:
    status = ascii_lines(ITERATIVE / "raw_moc_ulp_bridge_status.txt")
    require(status == EXPECTED_STATUS, "published status grammar or value differs")

    result = ascii_lines(ITERATIVE / "raw_moc_ulp_bridge_result.txt")
    require(result == expected_result_lines(), "published result grammar or value differs")
    for (arm, ledger), census in EXPECTED_CENSUS.items():
        require(
            census["TOTAL"]
            == census["UNCHANGED"] + census["UPWARD"] + census["DOWNWARD"],
            f"{arm} {ledger} direction census",
        )
        require(
            census["ADJACENT"] <= census["UPWARD"] + census["DOWNWARD"],
            f"{arm} {ledger} adjacency census",
        )
        if ledger == "RAW-BRIDGE":
            require(
                census["UNCHANGED"]
                == census["RAW-EXACT"] + census["ROUND-COLLAPSED-NONZERO"],
                f"{arm} RAW exact/collapsed partition",
            )
        maximum = census["MAX-STEPS"]
        require(
            all(abs(tie[3]) == tie[4] == maximum for tie in census["MAX-TIES"]),
            f"{arm} {ledger} maximum tie",
        )
    return result


def verify_markdown() -> None:
    path = ITERATIVE / "raw_moc_ulp_bridge_result.md"
    raw = canonical_bytes(path)
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        fail(f"result Markdown is not UTF-8: {exc}")
    normalized = " ".join(text.split())
    required = [
        RUN_COMMIT,
        ARTIFACT_MANIFEST_SHA256,
        "No Dragon process, transport solve, operator application, model term, "
        "relaxation, clipping or empirical coefficient was added.",
        "not an assertion that the production path actually stores RAW at that point",
        "The two ledgers must not be subtracted.",
        "not a measured rounding loss, cancellation, correction, or contribution "
        "from any named algorithm",
        "The two arms start from different states.",
        "There is no acceptance threshold",
        "does not authorize Stage 4 or Stage 5.",
        "a minimal, default-off REAL64 radial working-iteration experiment",
        "retaining the same physical equation and all frozen solver controls.",
        "It does not predict that the experiment will converge.",
        "2825 of 2960 NATIVE coordinates",
        "2827 of 2960 STATIONARY coordinates",
    ]
    for phrase in required:
        require(phrase in normalized, f"result Markdown omits boundary: {phrase}")


def verify_receipt(public_only: bool) -> dict[str, str]:
    rows = parse_sha_lines(RECEIPT)
    paths = tuple(relative for _, relative in rows)
    require(paths == EXPECTED_RECEIPT_PATHS, "result receipt path order/set differs")
    receipt = {relative: digest for digest, relative in rows}
    for relative in TRACKED_RECEIPT_PATHS:
        require(
            sha256(ROOT / relative) == receipt[relative],
            f"result receipt tracked hash differs: {relative}",
        )
    for relative, expected in EXPECTED_PUBLIC_HASHES.items():
        require(receipt[relative] == expected, f"result receipt public identity: {relative}")
    for relative, expected in EXPECTED_RECEIPT_ARTIFACT_HASHES.items():
        require(
            receipt[relative] == expected,
            f"result receipt artifact identity: {relative}",
        )
        if not public_only:
            require(
                sha256(ROOT / relative) == expected,
                f"result receipt artifact hash differs: {relative}",
            )
    return receipt


def verify_artifact_inventory() -> None:
    require(ARTIFACT.is_dir() and not ARTIFACT.is_symlink(), "artifact directory")
    expected_files = {
        relative for _, relative in EXPECTED_ARTIFACT
    } | {"artifact_manifest.sha256"}
    expected_directories = {
        "implementation",
        "implementation/validation",
        "implementation/validation/iterative",
    }
    files: set[str] = set()
    directories: set[str] = set()
    for path in ARTIFACT.rglob("*"):
        relative = path.relative_to(ARTIFACT).as_posix()
        mode = path.lstat().st_mode
        require(not stat.S_ISLNK(mode), f"artifact symlink: {relative}")
        if stat.S_ISREG(mode):
            files.add(relative)
        elif stat.S_ISDIR(mode):
            directories.add(relative)
        else:
            fail(f"artifact nonregular entry: {relative}")
    require(files == expected_files, "artifact regular-file inventory")
    require(len(files) == 33, "artifact regular-file census")
    require(directories == expected_directories, "artifact directory inventory")


def verify_artifact_manifest() -> None:
    manifest = ARTIFACT / "artifact_manifest.sha256"
    require(sha256(manifest) == ARTIFACT_MANIFEST_SHA256, "artifact manifest identity")
    require(parse_sha_lines(manifest) == EXPECTED_ARTIFACT, "artifact manifest rows")
    require(len(EXPECTED_ARTIFACT) == 32, "internal artifact manifest census")
    for expected, relative in EXPECTED_ARTIFACT:
        require(sha256(ARTIFACT / relative) == expected, f"artifact hash differs: {relative}")


def verify_histograms(full: list[str]) -> None:
    histograms: dict[tuple[str, str], list[tuple[int, int]]] = {
        key: [] for key in EXPECTED_CENSUS
    }
    for line in full:
        if " HIST " not in line:
            continue
        match = HIST_LINE.fullmatch(line)
        require(match is not None, "malformed histogram row")
        arm, ledger, step_text, count_text = match.groups()
        histograms[(arm, ledger)].append((int(step_text), int(count_text)))

    for key, rows in histograms.items():
        arm, ledger = key
        require(rows, f"{arm} {ledger} histogram missing")
        steps = [step for step, _ in rows]
        require(steps == sorted(set(steps)), f"{arm} {ledger} histogram order")
        histogram = Counter(dict(rows))
        census = EXPECTED_CENSUS[key]
        require(sum(histogram.values()) == census["TOTAL"], f"{arm} {ledger} histogram total")
        require(histogram[0] == census["UNCHANGED"], f"{arm} {ledger} histogram zero")
        require(
            sum(count for step, count in histogram.items() if step > 0)
            == census["UPWARD"],
            f"{arm} {ledger} histogram upward",
        )
        require(
            sum(count for step, count in histogram.items() if step < 0)
            == census["DOWNWARD"],
            f"{arm} {ledger} histogram downward",
        )
        require(
            histogram[-1] + histogram[1] == census["ADJACENT"],
            f"{arm} {ledger} histogram adjacency",
        )
        require(
            max(abs(step) for step in histogram) == census["MAX-STEPS"],
            f"{arm} {ledger} histogram maximum",
        )


def verify_artifact_logs(result: list[str]) -> None:
    native_a = canonical_bytes(ARTIFACT / "native_a.log")
    native_b = canonical_bytes(ARTIFACT / "native_b.log")
    stationary_a = canonical_bytes(ARTIFACT / "stationary_a.log")
    stationary_b = canonical_bytes(ARTIFACT / "stationary_b.log")
    checker_a = canonical_bytes(ARTIFACT / "checker_a.log")
    checker_b = canonical_bytes(ARTIFACT / "checker_b.log")
    require(native_a == native_b, "NATIVE reader replay differs")
    require(stationary_a == stationary_b, "STATIONARY reader replay differs")
    require(checker_a == checker_b, "independent checker replay differs")

    full_raw = canonical_bytes(ARTIFACT / "full.log")
    compact_raw = canonical_bytes(ARTIFACT / "compact.log")
    require(full_raw == native_a + stationary_a, "full log is not the two arm logs")
    full = full_raw.decode("ascii").splitlines()
    compact = compact_raw.decode("ascii").splitlines()
    require(
        compact == [line for line in full if " LEDGER " not in line],
        "compact/full ledger filtering differs",
    )
    require(
        result == [line for line in compact if " HIST " not in line],
        "published result/compact histogram filtering differs",
    )
    require(len(full) == 12639 and len(compact) == 799, "full/compact line census")

    ledger_counts = Counter()
    for line in full:
        if " LEDGER " not in line:
            continue
        match = LEDGER_LINE.match(line)
        require(match is not None, "malformed ledger row")
        ledger_counts[match.groups()] += 1
    require(
        ledger_counts == Counter({key: 2960 for key in EXPECTED_CENSUS}),
        "four-ledger row census",
    )
    require(sum(ledger_counts.values()) == 11840, "total ledger row census")
    verify_histograms(full)

    expected_checker = (
        b"RAW-MOC-ULP LOG CHECK PASS: ARMS=NATIVE,STATIONARY; "
        b"LEDGERS=4; ROWS=11840; RNE-REPLAY=5920\n"
    )
    require(checker_a == expected_checker, "independent checker result line")
    require(
        canonical_bytes(ARTIFACT / "run_commit.txt")
        == f"{RUN_COMMIT}\n".encode("ascii"),
        "artifact run commit",
    )
    require(
        canonical_bytes(ARTIFACT / "preflight.log")
        == canonical_bytes(ARTIFACT / "postflight.log"),
        "preflight/postflight differs",
    )
    require(
        canonical_bytes(ARTIFACT / "protocol.json")
        == canonical_bytes(ITERATIVE / "raw_moc_ulp_bridge_protocol.json"),
        "artifact/tracked protocol differs",
    )
    require(
        canonical_bytes(ARTIFACT / "implementation.sha256")
        == canonical_bytes(ITERATIVE / "raw_moc_ulp_bridge_implementation.sha256"),
        "artifact/tracked implementation manifest differs",
    )
    for _, relative in EXPECTED_IMPLEMENTATION:
        packaged = ARTIFACT / "implementation" / relative
        require(
            packaged.read_bytes() == (ROOT / relative).read_bytes(),
            f"packaged implementation differs: {relative}",
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify the published raw-MOC ULP bridge result."
    )
    parser.add_argument(
        "--public-only",
        action="store_true",
        help="verify tracked evidence and receipt without requiring the ignored artifact",
    )
    args = parser.parse_args()

    verify_public_hashes()
    verify_protocol()
    verify_implementation()
    result = verify_status_and_result()
    verify_markdown()
    verify_receipt(args.public_only)

    if args.public_only:
        print(
            "RAW-MOC-ULP RESULT CHECK PASS: PUBLIC; "
            "STATUS=20; RESULT=67; RECEIPT=24; ARTIFACT=SKIPPED"
        )
        return

    require(
        ARTIFACT.exists(),
        "artifact is absent; use --public-only for a tracked-only verification",
    )
    verify_artifact_inventory()
    verify_artifact_manifest()
    verify_artifact_logs(result)
    print(
        "RAW-MOC-ULP RESULT CHECK PASS: PUBLIC+ARTIFACT; "
        "MANIFEST=32; FILES=33; LEDGERS=4; ROWS=11840; RNE-REPLAY=5920"
    )


if __name__ == "__main__":
    main()
