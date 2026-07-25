#!/usr/bin/env python3
"""Independent, read-only verifier for a GMRES activity census artifact."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import hashlib
from pathlib import Path
import re
import stat
import sys


NGROUP = 370
MAX_K = 10
RUN_PROTOCOL_SHA256 = (
    "feee3d0a4989718137145d8136c246afc4ffebbb9dea9a0d105181be4a7be5d1"
)
SOURCE_IMPLEMENTATION_COMMIT = "5816c8aad4fbb43542514d5bd571ebccecdb6d72"
METHOD_PROTOCOL_SHA256 = (
    "8f1e1165e7d30b0e5b693e65a842a10581ec9ecb83b3d6bc3bc52ee8eb130bb9"
)
METHOD_IMPLEMENTATION_MANIFEST_SHA256 = (
    "22ff5770263a5f100382f4fd9f9d9e91babe51e51f6b32bb51f394ad3c67178b"
)
TRACK_SHA256 = (
    "2d868b87e2003c10c09da1ec8f8e6fd97f2a2629a680a46d7f898e2e5e1ed598"
)
LEGACY_OFF_XSM_SHA256 = (
    "c27ec11a833e0435dce5390e1c1ffbe81c931c21108d036b5af5fbd10a4f3789"
)
LEGACY_ON_XSM_SHA256 = (
    "de27778fb23f035aafab0e6ca877faf0f64a0662d255fa485b8174fea81f87ae"
)
LEGACY_OFF_DECK_SHA256 = (
    "4d62c27a38995e941b9ec38d7910e5a553c8856cf260af6af05fbca455189833"
)
LEGACY_ON_DECK_SHA256 = (
    "22b3460f6b1c51af795129459f8c2fe05b19cde264ad4f90c849d33cfccab8ec"
)
NORMALIZED_OFF_SHA256 = (
    "46bb92f9bddcf793b036e1dfbe3aa31e6e7f42cc43e2e5e70fffb65bf9bb2604"
)
NORMALIZED_ON_SHA256 = (
    "ff07ead583c85e5fc983e64d6a1d26cada7c1bb8836db11f1185fc637fc4ba39"
)
COMPILER_SHA256 = (
    "0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492"
)
FROZEN_EXECUTABLE_SHA256 = (
    "df83931c4ba0e5f5a7dfa534438967536a71d82e62e77ba4fc6bcb2e8f19f84a"
)
EXPECTED_BUILD_EVIDENCE_SHA256 = {
    "source_identity.tsv":
        "d416a68375414dfbb6ade504e771cbbc1b54775e741150c2678e1038cf6be4b8",
    "build_receipt.tsv":
        "0a0a69a704b5b998810eb145adf79659f711df21ac1d7a35266902a00d4734c9",
    "toolchain.sha256":
        "0220833d749d4351775ad80b42c6a1819d31104887ac4621eb302d8a46d5d0a3",
    "symbol_audit.txt":
        "6e0982061829dd8e9dd9fd5b3a7a743df93479d487803d3042e11b6e70d584b9",
    "instrumented_source_manifest.sha256":
        "2f06fbdff14e066c906ea8a97acf16c9ba85069e9d9832a915fa50b27875e25a",
    "executable.sha256":
        "8fe811eec396ad9eee8d7c6aaa56a022c1a822b52a8f048ada135abe922ad34a",
}
EXPECTED_RUN_IMPLEMENTATION_PATHS = {
    "validation/iterative/gmres_activity_run_reference.sha256",
    "validation/iterative/gmres_activity_probe.x2m.in",
    "validation/iterative/run_bounded_gmres_activity.py",
    "validation/iterative/test_bounded_gmres_activity.py",
    "validation/iterative/check_gmres_activity_run_logs.py",
    "validation/iterative/test_gmres_activity_run_logs.py",
    "validation/iterative/check_gmres_activity_pair_xsm.f90",
    "validation/iterative/check_gmres_activity_artifact.py",
    "validation/iterative/test_gmres_activity_artifact.py",
    "validation/iterative/run_gmres_activity_production.sh",
    "validation/iterative/gmres_activity_run_protocol.json",
    "validation/iterative/check_gmres_activity_run_protocol.py",
    "validation/iterative/gmres_activity_implementation.sha256",
    "validation/iterative/build_gmres_activity_overlay.sh",
    "validation/iterative/check_gmres_activity_implementation.py",
    "validation/iterative/check_gmres_activity_xsm.f90",
    "validation/iterative/normalize_gmres_activity_log.py",
    "validation/iterative/run_gmres_activity_preflight.sh",
}
EPSI_BITS_AS_INTEGER = int("3727C5AC", 16)

ACTIVE = "VALID-GMRES-UPDATE-ACTIVE"
INACTIVE = "VALID-GMRES-UPDATE-INACTIVE"
INVALID = "INVALID"

REQUIRED_PAYLOAD = (
    "gmres_activity_run_protocol.json",
    "gmres_activity_run_implementation.sha256",
    "run_receipt.tsv",
    "run_commit.txt",
    "source_identity.tsv",
    "build_receipt.tsv",
    "toolchain.sha256",
    "symbol_audit.txt",
    "instrumented_source_manifest.sha256",
    "implementation_replay.log",
    "inputs_before.sha256",
    "inputs_after.sha256",
    "executable.sha256",
    "preflight.log",
    "postflight.log",
    "track.xsm",
    "off/deck.x2m",
    "off/run.log",
    "off/normalized.log",
    "off/result.xsm",
    "on_a/deck.x2m",
    "on_a/run.log",
    "on_a/normalized.log",
    "on_a/result.xsm",
    "on_a/ledger.txt",
    "on_a/ledger_repeat.txt",
    "on_a/non_audit_identity.txt",
    "on_b/deck.x2m",
    "on_b/run.log",
    "on_b/normalized.log",
    "on_b/result.xsm",
    "on_b/ledger.txt",
    "on_b/ledger_repeat.txt",
    "on_b/non_audit_identity.txt",
    "log_identity.txt",
    "reader_replay.sha256",
    "artifact_check_a.log",
    "artifact_check_b.log",
    "result.txt",
    "artifact_manifest.sha256",
)

EXPECTED_INPUT_HASHES = {
    "validation/artifacts/raw-moc-capture/common/initial_radial_track.bin":
        "f7b27cb4a5d37f903b93e49610e2daa2290d55c164e2ca0e73ccb8d22fe486b8",
    "validation/artifacts/raw-moc-capture/common/restart_macro0.xsm":
        "6eb2920473f4cb8d27b6377bcb59b42833c8ebf9a0fc57925341d12ccac0a617",
    "validation/artifacts/raw-moc-capture/common/restart_source.xsm":
        "6942f61ba2cc7ab0d5cf9a4104959809a388fab441da82730cf64de74a48769f",
    "validation/artifacts/raw-moc-capture/common/restart_system.xsm":
        "a8797a7d42fdab574eb183bc2ecf0e2b53c992fdd2dd4c61d40c72a53746e599",
    "validation/artifacts/raw-moc-capture/common/restart_track.xsm":
        TRACK_SHA256,
    "validation/artifacts/raw-moc-capture/stationary/off.xsm":
        LEGACY_OFF_XSM_SHA256,
    "validation/artifacts/raw-moc-capture/stationary/on.xsm":
        LEGACY_ON_XSM_SHA256,
    "validation/artifacts/raw-moc-capture/stationary/pre.xsm":
        "6e297fe92b03609ddbac84128623a14ac8638d5d86147ca6a8ee1298f71f3b3e",
    "validation/artifacts/raw-moc-capture/stationary_off/probe.log":
        "b15a3c9e0ad3bdc54ed3e50bba9e9cbb22a885bb68f712fb83ea02ef1e109234",
    "validation/artifacts/raw-moc-capture/stationary_on/probe.log":
        "03f802bea77875419e126ec51282924b2717bed7b987c8171febc2738a2bfe25",
}

SHA_ROW = re.compile(r"([0-9a-f]{64})  (.+)")
INTEGER = re.compile(r"-?(?:0|[1-9][0-9]*)")
HEX40 = re.compile(r"[0-9a-f]{40}")
CPU_TIME_RE = re.compile(
    r"(FLU2DR: CPU TIME=)[ \t]*"
    r"[+-]?(?:\d+(?:\.\d+)?|\.\d+)(?:[EeDd][+-]?\d+)?"
    r"(?=\.[ \t]+(?:INTERNAL|EXTERNAL))"
)
MODULE_RECEIPT_RE = re.compile(
    r"^(?P<prefix>-->>MODULE FLU:        : TIME SPENT=)"
    r"(?P<time>.{13})"
    r"(?P<middle> MEMORY USAGE=)"
    r"(?P<memory>.{10})$",
    re.MULTILINE,
)
MODULE_TIME_RE = re.compile(r" *(?:0|[1-9][0-9]*)\.[0-9]{3}")
MODULE_MEMORY_RE = re.compile(r" [0-9]\.[0-9]{3}E[+-][0-9]{2}")
MODULE_TIME_MARKER = "<MODULE-TIME>"
MODULE_MEMORY_MARKER = "<MEM-TELE>"
CLE_CPU_RE = re.compile(
    r"^(?P<prefix>cle2000_c: cpu time= )"
    r"(?P<value>(?:0|[1-9][0-9]*)\.[0-9]{2})"
    r"(?P<suffix> second)$",
    re.MULTILINE,
)
CLE_CPU_MARKER = "<CLE-CPU>"
SOURCE_GMRA_RE = re.compile(
    r"^ACCE[^\n]* MOCA 2 GMRA ;[ \t]+0028[ \t]*$",
    re.MULTILINE,
)
TRACE_GMRA_RE = re.compile(
    r"^<\|ACCE[^\n]* MOCA 2 GMRA ;[^\n]*\|<0028[ \t]*$",
    re.MULTILINE,
)


class ArtifactError(RuntimeError):
    """A fail-closed artifact contract violation."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ArtifactError(message)


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha256(path: Path) -> str:
    require(path.is_file() and not path.is_symlink(), f"invalid file: {path}")
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_bytes(path: Path, *, ascii_only: bool = True) -> bytes:
    require(path.is_file() and not path.is_symlink(), f"invalid text file: {path}")
    raw = path.read_bytes()
    require(raw.endswith(b"\n"), f"missing final newline: {path}")
    require(b"\r" not in raw and b"\0" not in raw, f"noncanonical text: {path}")
    if ascii_only:
        try:
            raw.decode("ascii")
        except UnicodeDecodeError as exc:
            raise ArtifactError(f"non-ASCII text: {path}") from exc
    return raw


def ascii_lines(path: Path) -> list[str]:
    return canonical_bytes(path).decode("ascii").splitlines()


def parse_integer(token: str, owner: str) -> int:
    require(INTEGER.fullmatch(token) is not None, f"{owner} is not canonical integer")
    return int(token)


def parse_sha_rows(path: Path, *, safe_relative: bool) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for line in ascii_lines(path):
        match = SHA_ROW.fullmatch(line)
        require(match is not None, f"malformed SHA256 row: {path}")
        digest, name = match.groups()
        require(name and "\t" not in name, f"invalid SHA256 name: {path}")
        if safe_relative:
            candidate = Path(name)
            require(
                not candidate.is_absolute()
                and ".." not in candidate.parts
                and candidate.as_posix() == name,
                f"unsafe manifest path: {name}",
            )
        rows.append((digest, name))
    require(rows, f"empty SHA256 file: {path}")
    require(
        len({name for _, name in rows}) == len(rows),
        f"duplicate SHA256 name: {path}",
    )
    return rows


def parse_tsv(path: Path) -> list[tuple[str, str]]:
    result: list[tuple[str, str]] = []
    for line in ascii_lines(path):
        fields = line.split("\t")
        require(len(fields) == 2 and all(fields), f"malformed TSV row: {path}")
        result.append((fields[0], fields[1]))
    require(
        len({key for key, _ in result}) == len(result),
        f"duplicate TSV key: {path}",
    )
    return result


def verify_inventory(root: Path) -> None:
    require(root.is_dir() and not root.is_symlink(), "invalid artifact root")
    files: set[str] = set()
    directories: set[str] = set()
    for path in root.rglob("*"):
        relative = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        require(not stat.S_ISLNK(mode), f"artifact symlink: {relative}")
        if stat.S_ISREG(mode):
            files.add(relative)
        elif stat.S_ISDIR(mode):
            directories.add(relative)
        else:
            raise ArtifactError(f"artifact special file: {relative}")
    require(files == set(REQUIRED_PAYLOAD), "artifact file census differs")
    require(directories == {"off", "on_a", "on_b"}, "artifact directory census differs")


def verify_manifest(root: Path) -> None:
    rows = parse_sha_rows(root / "artifact_manifest.sha256", safe_relative=True)
    expected_names = sorted(set(REQUIRED_PAYLOAD) - {"artifact_manifest.sha256"})
    require([name for _, name in rows] == expected_names, "artifact manifest census/order")
    for expected, name in rows:
        require(sha256(root / name) == expected, f"artifact hash differs: {name}")


@dataclass(frozen=True)
class RoleEvent:
    call: int
    index: int
    role: int
    iteration: int
    block: int
    active_count: int
    mask: tuple[int, ...]


@dataclass(frozen=True)
class Block:
    call: int
    index: int
    iteration: int
    active_count: int
    active: tuple[int, ...]
    kmax: tuple[int, ...]


@dataclass(frozen=True)
class RawScience:
    roles: tuple[RoleEvent, ...]
    blocks: tuple[Block, ...]


@dataclass(frozen=True)
class ScienceResult:
    blocks: int
    histogram: tuple[int, ...]
    nonzero: int
    sum_k: int
    max_k: int
    role_calls: tuple[int, int, int]
    role_groups: tuple[int, int, int]
    last_iteration: int
    classification: str


@dataclass(frozen=True)
class ReaderDerived:
    state: tuple[int, ...]
    call: tuple[int, int, int, int, int]
    role_sums: tuple[tuple[int, int], ...]
    histogram: tuple[int, ...]
    nonzero: int
    sum_k: int
    max_k: int
    classification: str


def split_exact(line: str, prefix: tuple[str, ...], count: int, owner: str) -> list[str]:
    fields = line.split()
    require(
        len(fields) == len(prefix) + count and tuple(fields[:len(prefix)]) == prefix,
        f"malformed {owner}",
    )
    return fields[len(prefix):]


def parse_ledger(path: Path) -> tuple[RawScience, ReaderDerived]:
    lines = ascii_lines(path)
    position = 0

    def take(owner: str) -> str:
        nonlocal position
        require(position < len(lines), f"missing {owner}")
        line = lines[position]
        position += 1
        return line

    require(
        take("TRACK row") == "GMRES-ACTIVITY RAW TRACK 20 10 3727C5AC",
        "TRACK row differs",
    )
    state: list[int] = []
    for field in range(1, 25):
        values = split_exact(
            take("STATE row"),
            ("GMRES-ACTIVITY", "RAW", "STATE"),
            2,
            "STATE row",
        )
        require(parse_integer(values[0], "STATE index") == field, "STATE index order")
        state.append(parse_integer(values[1], "STATE value"))
    for group in range(1, NGROUP + 1):
        values = split_exact(
            take("NGIND row"),
            ("GMRES-ACTIVITY", "RAW", "NGIND"),
            2,
            "NGIND row",
        )
        require(
            parse_integer(values[0], "NGIND row") == group
            and parse_integer(values[1], "NGIND value") == group,
            "NGIND identity/order",
        )

    call_values = split_exact(
        take("CALL row"),
        ("GMRES-ACTIVITY", "RAW", "CALL"),
        5,
        "CALL row",
    )
    call = tuple(parse_integer(value, "CALL value") for value in call_values)
    require(len(call) == 5, "internal CALL width")

    role_sums: list[tuple[int, int]] = []
    for role in range(1, 4):
        values = split_exact(
            take("ROLE-SUM row"),
            ("GMRES-ACTIVITY", "RAW", "ROLE-SUM"),
            3,
            "ROLE-SUM row",
        )
        require(parse_integer(values[0], "ROLE-SUM role") == role, "ROLE-SUM order")
        role_sums.append(
            (
                parse_integer(values[1], "ROLE-SUM calls"),
                parse_integer(values[2], "ROLE-SUM groups"),
            )
        )

    roles: list[RoleEvent] = []
    while position < len(lines) and lines[position].startswith("GMRES-ACTIVITY RAW ROLE "):
        values = split_exact(
            take("ROLE row"),
            ("GMRES-ACTIVITY", "RAW", "ROLE"),
            6,
            "ROLE row",
        )
        metadata = [parse_integer(value, "ROLE value") for value in values]
        mask: list[int] = []
        event_ordinal = len(roles) + 1
        for group in range(1, NGROUP + 1):
            active_values = split_exact(
                take("ROLE-ACTIVE row"),
                ("GMRES-ACTIVITY", "RAW", "ROLE-ACTIVE"),
                3,
                "ROLE-ACTIVE row",
            )
            require(
                parse_integer(active_values[0], "ROLE-ACTIVE event")
                == event_ordinal
                and parse_integer(active_values[1], "ROLE-ACTIVE group") == group,
                "ROLE-ACTIVE event/group order",
            )
            mask.append(parse_integer(active_values[2], "ROLE-ACTIVE mask"))
        roles.append(RoleEvent(*metadata, tuple(mask)))

    blocks: list[Block] = []
    while position < len(lines) and lines[position].startswith("GMRES-ACTIVITY RAW BLOCK "):
        values = split_exact(
            take("BLOCK row"),
            ("GMRES-ACTIVITY", "RAW", "BLOCK"),
            4,
            "BLOCK row",
        )
        metadata = [parse_integer(value, "BLOCK value") for value in values]
        active: list[int] = []
        kmax: list[int] = []
        block_ordinal = len(blocks) + 1
        for group in range(1, NGROUP + 1):
            group_values = split_exact(
                take("BLOCK-GROUP row"),
                ("GMRES-ACTIVITY", "RAW", "BLOCK-GROUP"),
                4,
                "BLOCK-GROUP row",
            )
            require(
                parse_integer(group_values[0], "BLOCK-GROUP block")
                == block_ordinal
                and parse_integer(group_values[1], "BLOCK-GROUP group") == group,
                "BLOCK-GROUP block/group order",
            )
            active.append(parse_integer(group_values[2], "BLOCK-GROUP active"))
            kmax.append(parse_integer(group_values[3], "BLOCK-GROUP KMAX"))
        blocks.append(Block(*metadata, tuple(active), tuple(kmax)))

    histogram: list[int] = []
    for k_value in range(MAX_K + 1):
        values = split_exact(
            take("K-HISTOGRAM row"),
            ("GMRES-ACTIVITY", "RAW", "K-HISTOGRAM"),
            2,
            "K-HISTOGRAM row",
        )
        require(
            parse_integer(values[0], "K-HISTOGRAM bin") == k_value,
            "K-HISTOGRAM order",
        )
        histogram.append(parse_integer(values[1], "K-HISTOGRAM count"))

    nonzero_fields = split_exact(
        take("NONZERO row"),
        ("GMRES-ACTIVITY", "NONZERO-K-GROUP-BLOCKS"),
        1,
        "NONZERO row",
    )
    sum_fields = split_exact(
        take("SUM-K row"),
        ("GMRES-ACTIVITY", "SUM-K"),
        1,
        "SUM-K row",
    )
    max_fields = split_exact(
        take("MAX-K row"),
        ("GMRES-ACTIVITY", "MAX-K"),
        1,
        "MAX-K row",
    )
    require(take("threshold row") == "GMRES-ACTIVITY THRESHOLD NONE", "threshold differs")
    class_fields = split_exact(
        take("CLASSIFICATION row"),
        ("GMRES-ACTIVITY", "CLASSIFICATION"),
        1,
        "CLASSIFICATION row",
    )
    require(take("COMPLETE row") == "GMRES-ACTIVITY COMPLETE", "COMPLETE row differs")
    require(position == len(lines), "extra ledger rows")

    return (
        RawScience(tuple(roles), tuple(blocks)),
        ReaderDerived(
            tuple(state),
            call,  # type: ignore[arg-type]
            tuple(role_sums),
            tuple(histogram),
            parse_integer(nonzero_fields[0], "NONZERO count"),
            parse_integer(sum_fields[0], "SUM-K"),
            parse_integer(max_fields[0], "MAX-K"),
            class_fields[0],
        ),
    )


def reconstruct_science(raw: RawScience) -> ScienceResult:
    """Derive every K identity from raw role/mask/block rows only."""

    roles = raw.roles
    blocks = raw.blocks
    require(roles, "raw ledger has no role event")
    require(len(blocks) <= 19, "raw correction-block bound")

    previous_global = [1] * NGROUP
    role_calls = [0, 0, 0]
    role_groups = [0, 0, 0]
    last_iteration = 0
    for ordinal, event in enumerate(roles, start=1):
        require(event.call == 1 and event.index == ordinal, "raw role identity/order")
        require(event.role in (1, 2, 3), "raw role outside range")
        require(1 <= event.iteration <= 19, "raw role ITER outside range")
        require(event.iteration >= last_iteration, "raw role ITER decreases")
        last_iteration = event.iteration
        require(len(event.mask) == NGROUP, "raw role mask width")
        require(all(value in (0, 1) for value in event.mask), "raw role mask is not binary")
        require(
            all(value <= previous for value, previous in zip(event.mask, previous_global)),
            "raw role mask changes from zero to one",
        )
        previous_global = list(event.mask)
        active_count = sum(event.mask)
        require(active_count > 0 and active_count == event.active_count, "raw role active count")
        if event.role == 1:
            require(event.block == 0, "raw PRIMARY block identity")
        else:
            require(1 <= event.block <= len(blocks), "raw nonprimary block identity")
        role_calls[event.role - 1] += 1
        role_groups[event.role - 1] += active_count
    require(role_calls[0] >= 1 and role_calls[1] <= 1, "raw role call census")

    block_maxima: list[int] = []
    all_k: list[int] = []
    pointer = 0
    expected_primary_iter = 1
    for ordinal, block in enumerate(blocks, start=1):
        require(
            block.call == 1 and block.index == ordinal,
            "raw block identity/order",
        )
        require(1 <= block.iteration <= 19, "raw block ITER outside range")
        require(len(block.active) == NGROUP and len(block.kmax) == NGROUP, "raw block width")
        require(all(value in (0, 1) for value in block.active), "raw block mask not binary")
        require(all(0 <= value <= MAX_K for value in block.kmax), "raw KMAX outside range")
        require(
            all(active or value == 0 for active, value in zip(block.active, block.kmax)),
            "raw inactive group has nonzero KMAX",
        )
        require(
            sum(block.active) == block.active_count and block.active_count > 0,
            "raw block active count",
        )

        require(pointer < len(roles), "raw block lacks preceding PRIMARY")
        primary = roles[pointer]
        require(
            primary.role == 1
            and primary.block == 0
            and primary.iteration == expected_primary_iter,
            "raw block PRIMARY sequence",
        )
        require(
            all(active <= mask for active, mask in zip(block.active, primary.mask)),
            "raw block mask is not PRIMARY subset",
        )
        pointer += 1

        if ordinal == 1:
            require(pointer < len(roles), "raw first block lacks AFFINE-RHS")
            affine = roles[pointer]
            require(
                affine.role == 2
                and affine.block == ordinal
                and affine.iteration == primary.iteration
                and affine.mask == block.active,
                "raw AFFINE-RHS sequence/mask",
            )
            pointer += 1

        krylov: list[RoleEvent] = []
        while (
            pointer < len(roles)
            and roles[pointer].role == 3
            and roles[pointer].block == ordinal
        ):
            krylov.append(roles[pointer])
            pointer += 1

        maximum = max(block.kmax, default=0)
        require(len(krylov) == maximum, "raw Krylov count/MAX-K identity")
        reconstructed = [
            sum(event.mask[group] for event in krylov) for group in range(NGROUP)
        ]
        require(tuple(reconstructed) == block.kmax, "raw KMAX reconstruction differs")
        if krylov:
            require(krylov[0].mask == block.active, "raw first Krylov/block mask differs")
            previous = krylov[0].mask
            for offset, event in enumerate(krylov, start=1):
                require(
                    event.iteration == primary.iteration + offset,
                    "raw Krylov ITER sequence",
                )
                require(
                    all(current <= old for current, old in zip(event.mask, previous)),
                    "raw Krylov mask changes from zero to one",
                )
                previous = event.mask
            require(
                block.iteration == krylov[-1].iteration,
                "raw block end ITER differs",
            )
        else:
            require(
                ordinal == len(blocks) and block.iteration == 19,
                "raw zero-K block is not terminal MAXIT block",
            )
        require(
            all(
                not active or maximum == 0 or value >= 1
                for active, value in zip(block.active, block.kmax)
            ),
            "raw active group lacks first Krylov visit",
        )
        block_maxima.append(maximum)
        all_k.extend(block.kmax)
        expected_primary_iter = block.iteration + 1

    if pointer < len(roles):
        require(pointer == len(roles) - 1, "raw extra terminal role events")
        terminal = roles[pointer]
        require(
            terminal.role == 1
            and terminal.block == 0
            and terminal.iteration == expected_primary_iter,
            "raw terminal PRIMARY sequence",
        )
        pointer += 1
    require(pointer == len(roles), "raw event sequence not consumed")
    require((len(blocks) == 0) == (role_calls[1] == 0), "raw block/AFFINE presence")
    require(role_calls[2] == sum(block_maxima), "raw Krylov calls/block maxima")

    histogram_counter = Counter(all_k)
    histogram = tuple(histogram_counter[k_value] for k_value in range(MAX_K + 1))
    nonzero = sum(count for k_value, count in histogram_counter.items() if k_value > 0)
    sum_k = sum(k_value * count for k_value, count in histogram_counter.items())
    max_k = max(all_k, default=0)
    require(sum(histogram) == NGROUP * len(blocks), "raw histogram row census")
    require(role_groups[2] == sum_k, "raw Krylov groups/SUM-K identity")
    classification = ACTIVE if nonzero > 0 else INACTIVE
    return ScienceResult(
        len(blocks),
        histogram,
        nonzero,
        sum_k,
        max_k,
        tuple(role_calls),  # type: ignore[arg-type]
        tuple(role_groups),  # type: ignore[arg-type]
        last_iteration,
        classification,
    )


def verify_reader_derived(derived: ReaderDerived, science: ScienceResult) -> None:
    state = derived.state
    require(len(state) == 24, "reader STATE width")
    require(
        state[:10] == (1, 1, 2, 1, 370, 14, 370, 10, 1, 1),
        "reader STATE static identity",
    )
    require(state[10:13] == science.role_calls, "reader STATE role calls differ")
    require(state[13:16] == science.role_groups, "reader STATE role groups differ")
    require(
        state[16:20]
        == (science.blocks, science.nonzero, science.sum_k, science.max_k),
        "reader STATE K summary differs",
    )
    require(
        state[20:] == (20, EPSI_BITS_AS_INTEGER, 0, 0),
        "reader STATE controls differ",
    )
    require(
        derived.call
        == (1, 1, sum(science.role_calls), science.blocks, science.last_iteration),
        "reader CALL summary differs",
    )
    require(
        derived.role_sums
        == tuple(zip(science.role_calls, science.role_groups)),
        "reader ROLE-SUM differs",
    )
    require(derived.histogram == science.histogram, "reader K-HISTOGRAM differs")
    require(derived.nonzero == science.nonzero, "reader NONZERO differs")
    require(derived.sum_k == science.sum_k, "reader SUM-K differs")
    require(derived.max_k == science.max_k, "reader MAX-K differs")
    require(derived.classification == science.classification, "reader CLASSIFICATION differs")


def normalize_log(raw: bytes, mode: str) -> bytes:
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError as exc:
        raise ArtifactError("run log is not ASCII") from exc
    require(text.endswith("\n") and "\r" not in text, "run log is not canonical")
    if mode == "legacy":
        require("GMRA" not in text, "OFF log contains GMRA")
    else:
        require(text.count("GMRA") == 2, "ON log GMRA token census")
        for pattern, owner in (
            (SOURCE_GMRA_RE, "ON source GMRA line"),
            (TRACE_GMRA_RE, "ON trace GMRA line"),
        ):
            matches = list(pattern.finditer(text))
            require(len(matches) == 1, f"{owner} census")
            line = matches[0].group(0)
            require(line.count(" MOCA 2 GMRA ;") == 1, f"{owner} grammar")
            replacement = line.replace(" MOCA 2 GMRA ;", " MOCA 2 ;     ", 1)
            text = text[:matches[0].start()] + replacement + text[matches[0].end():]
        require("GMRA" not in text, "GMRA remains after normalization")
    text, substitutions = CPU_TIME_RE.subn(r"\1<CPU-TELEMETRY>", text)
    require(substitutions == 2, "CPU telemetry census")
    require(text.count("<CPU-TELEMETRY>") == 2, "normalized CPU marker census")
    require(
        MODULE_TIME_MARKER not in text and MODULE_MEMORY_MARKER not in text,
        "forged module telemetry marker",
    )
    require(
        len(re.findall(r"^-->>MODULE ", text, re.MULTILINE)) == 1,
        "module receipt census",
    )
    module_matches = list(MODULE_RECEIPT_RE.finditer(text))
    require(len(module_matches) == 1, "FLU module telemetry census")
    module = module_matches[0]
    require(
        MODULE_TIME_RE.fullmatch(module.group("time")) is not None,
        "FLU module time telemetry grammar",
    )
    require(
        MODULE_MEMORY_RE.fullmatch(module.group("memory")) is not None,
        "FLU module memory telemetry grammar",
    )
    module_replacement = (
        module.group("prefix")
        + MODULE_TIME_MARKER
        + module.group("middle")
        + MODULE_MEMORY_MARKER
    )
    require(
        len(module_replacement) == len(module.group(0)),
        "FLU module telemetry width",
    )
    text = text[:module.start()] + module_replacement + text[module.end():]
    require(
        text.count(MODULE_TIME_MARKER) == 1
        and text.count(MODULE_MEMORY_MARKER) == 1,
        "normalized module telemetry marker census",
    )
    require(CLE_CPU_MARKER not in text, "forged CLE CPU marker")
    cle_matches = list(CLE_CPU_RE.finditer(text))
    require(len(cle_matches) == 1, "CLE CPU telemetry census")
    cle = cle_matches[0]
    text = (
        text[:cle.start()]
        + cle.group("prefix")
        + CLE_CPU_MARKER
        + cle.group("suffix")
        + text[cle.end():]
    )
    require(text.count(CLE_CPU_MARKER) == 1, "normalized CLE CPU marker census")
    return text.encode("ascii")


def result_lines(science: ScienceResult) -> list[str]:
    lines = [
        "GMRES-ACTIVITY RESULT 1",
        "PROCESSES OFF=1 ON=2",
        f"CORRECTION-BLOCKS {science.blocks}",
        f"GROUP-BLOCKS {NGROUP * science.blocks}",
    ]
    lines.extend(
        f"K-HISTOGRAM {k_value} {count}"
        for k_value, count in enumerate(science.histogram)
    )
    lines.extend(
        [
            f"NONZERO-K-GROUP-BLOCKS {science.nonzero}",
            f"SUM-K {science.sum_k}",
            f"MAX-K {science.max_k}",
            "THRESHOLD NONE",
            f"CLASSIFICATION {science.classification}",
            "COMPLETE",
        ]
    )
    return lines


def verify_receipt_and_build(root: Path, classification: str) -> None:
    run_commit_lines = ascii_lines(root / "run_commit.txt")
    require(
        len(run_commit_lines) == 1 and HEX40.fullmatch(run_commit_lines[0]) is not None,
        "run commit grammar",
    )
    run_commit = run_commit_lines[0]

    implementation_sha = sha256(root / "gmres_activity_run_implementation.sha256")
    implementation_rows = parse_sha_rows(
        root / "gmres_activity_run_implementation.sha256",
        safe_relative=True,
    )
    require(
        [name for _, name in implementation_rows]
        == sorted(EXPECTED_RUN_IMPLEMENTATION_PATHS),
        "run implementation manifest census/order",
    )
    for name, expected_sha in EXPECTED_BUILD_EVIDENCE_SHA256.items():
        require(
            sha256(root / name) == expected_sha,
            f"frozen build evidence differs: {name}",
        )

    executable_rows = parse_sha_rows(root / "executable.sha256", safe_relative=False)
    require(
        len(executable_rows) == 1
        and executable_rows[0][0] == FROZEN_EXECUTABLE_SHA256
        and executable_rows[0][1] == "bin/Darwin_arm64/Dragon",
        "executable receipt grammar",
    )
    executable_sha = executable_rows[0][0]

    expected_receipt = [
        ("schema", "1"),
        ("run_commit", run_commit),
        ("source_implementation_commit", SOURCE_IMPLEMENTATION_COMMIT),
        ("method_protocol_sha256", METHOD_PROTOCOL_SHA256),
        ("run_protocol_sha256", RUN_PROTOCOL_SHA256),
        ("method_implementation_manifest_sha256", METHOD_IMPLEMENTATION_MANIFEST_SHA256),
        ("run_implementation_manifest_sha256", implementation_sha),
        ("executable_sha256", executable_sha),
        ("process_matrix", "OFF=1,ON=2"),
        ("classification", classification),
    ]
    require(parse_tsv(root / "run_receipt.tsv") == expected_receipt, "run receipt differs")

    source_identity = dict(parse_tsv(root / "source_identity.tsv"))
    require(
        source_identity.get("schema") == "1"
        and source_identity.get("source_implementation_commit")
        == SOURCE_IMPLEMENTATION_COMMIT
        and source_identity.get("tracked_live_src") == "UNCHANGED",
        "source identity evidence",
    )
    build = dict(parse_tsv(root / "build_receipt.tsv"))
    require(
        build.get("schema") == "1"
        and build.get("status") == "PASS"
        and build.get("platform") == "Darwin arm64"
        and build.get("compiler_sha256") == COMPILER_SHA256
        and build.get("executable_sha256") == executable_sha,
        "build receipt evidence",
    )
    toolchain = parse_sha_rows(root / "toolchain.sha256", safe_relative=False)
    require(any(digest == COMPILER_SHA256 for digest, _ in toolchain), "compiler toolchain hash")
    parse_sha_rows(root / "instrumented_source_manifest.sha256", safe_relative=True)
    require(
        ascii_lines(root / "symbol_audit.txt")[-1]
        == "GMRES-ACTIVITY SYMBOL AUDIT PASS",
        "symbol audit evidence",
    )
    require(
        ascii_lines(root / "implementation_replay.log")
        == ["GMRES-ACTIVITY IMPLEMENTATION CHECK PASS"],
        "implementation replay evidence",
    )


def verify_inputs_and_process_evidence(root: Path, classification: str) -> None:
    before_raw = canonical_bytes(root / "inputs_before.sha256")
    after_raw = canonical_bytes(root / "inputs_after.sha256")
    require(before_raw == after_raw, "input hashes changed")
    before = {
        name: digest
        for digest, name in parse_sha_rows(
            root / "inputs_before.sha256",
            safe_relative=True,
        )
    }
    require(before == EXPECTED_INPUT_HASHES, "frozen input receipt differs")

    require(sha256(root / "track.xsm") == TRACK_SHA256, "TRACK copy differs")
    require(
        sha256(root / "off/result.xsm") == LEGACY_OFF_XSM_SHA256,
        "OFF XSM identity differs",
    )
    on_a = (root / "on_a/result.xsm").read_bytes()
    on_b = (root / "on_b/result.xsm").read_bytes()
    require(on_a == on_b, "ON XSM replay differs")
    require(sha256_bytes(on_a) != LEGACY_ON_XSM_SHA256, "ON audit directory is absent")

    off_deck = canonical_bytes(root / "off/deck.x2m")
    on_a_deck = canonical_bytes(root / "on_a/deck.x2m")
    on_b_deck = canonical_bytes(root / "on_b/deck.x2m")
    require(sha256_bytes(off_deck) == LEGACY_OFF_DECK_SHA256, "OFF deck identity")
    require(on_a_deck == on_b_deck, "ON deck replay differs")
    require(on_a_deck.count(b" MOCA 2 GMRA ;") == 1, "ON deck activation grammar")
    require(on_a_deck.count(b"GMRA") == 1, "ON deck GMRA token census")
    require(
        sha256_bytes(on_a_deck.replace(b" GMRA", b"", 1))
        == LEGACY_ON_DECK_SHA256,
        "ON deck differs outside GMRA",
    )

    off_normalized = normalize_log(canonical_bytes(root / "off/run.log"), "legacy")
    on_a_normalized = normalize_log(canonical_bytes(root / "on_a/run.log"), "gmra")
    on_b_normalized = normalize_log(canonical_bytes(root / "on_b/run.log"), "gmra")
    require(
        canonical_bytes(root / "off/normalized.log") == off_normalized,
        "OFF normalized log differs",
    )
    require(
        canonical_bytes(root / "on_a/normalized.log") == on_a_normalized
        and canonical_bytes(root / "on_b/normalized.log") == on_b_normalized,
        "ON normalized log differs",
    )
    require(sha256_bytes(off_normalized) == NORMALIZED_OFF_SHA256, "OFF legacy log identity")
    require(
        sha256_bytes(on_a_normalized) == NORMALIZED_ON_SHA256
        and on_a_normalized == on_b_normalized,
        "ON legacy/replay log identity",
    )
    require(
        ascii_lines(root / "log_identity.txt")
        == ["GMRES-ACTIVITY RUN-LOGS PASS"],
        "log identity evidence",
    )

    for case, label in (("on_a", "ON-A"), ("on_b", "ON-B")):
        require(
            ascii_lines(root / f"{case}/non_audit_identity.txt")
            == ["GMRES-ACTIVITY PAIR CHECK PASS"],
            f"{label} XSM identity evidence",
        )

    for name in ("preflight.log", "postflight.log"):
        lines = ascii_lines(root / name)
        require(
            lines[-2:]
            == [
                "GMRES-ACTIVITY PREFLIGHT PASS",
                "GMRES-ACTIVITY PRODUCTION NOT AUTHORIZED",
            ],
            f"{name} terminal evidence",
        )
        require(
            not any("CLASSIFICATION" in line for line in lines),
            f"{name} contains scientific result",
        )

    expected_check = f"{classification}\n".encode("ascii")
    require(
        canonical_bytes(root / "artifact_check_a.log") == expected_check
        and canonical_bytes(root / "artifact_check_b.log") == expected_check,
        "artifact checker replay evidence",
    )


def verify_ledgers(root: Path) -> ScienceResult:
    paths = [
        root / "on_a/ledger.txt",
        root / "on_a/ledger_repeat.txt",
        root / "on_b/ledger.txt",
        root / "on_b/ledger_repeat.txt",
    ]
    payloads = [canonical_bytes(path) for path in paths]
    require(len(set(payloads)) == 1, "reader ledger replay differs")

    expected_replay_names = [
        "on_a/ledger.txt",
        "on_a/ledger_repeat.txt",
        "on_b/ledger.txt",
        "on_b/ledger_repeat.txt",
    ]
    replay_rows = parse_sha_rows(root / "reader_replay.sha256", safe_relative=True)
    require(
        [name for _, name in replay_rows] == expected_replay_names,
        "reader replay receipt census/order",
    )
    for expected, name in replay_rows:
        require(sha256(root / name) == expected, f"reader replay hash: {name}")

    raw, reader_derived = parse_ledger(paths[0])
    science = reconstruct_science(raw)
    verify_reader_derived(reader_derived, science)
    return science


def verify_artifact(root: Path) -> str:
    verify_inventory(root)
    verify_manifest(root)
    require(
        sha256(root / "gmres_activity_run_protocol.json") == RUN_PROTOCOL_SHA256,
        "run protocol identity",
    )
    science = verify_ledgers(root)
    require(
        ascii_lines(root / "result.txt") == result_lines(science),
        "published result differs from raw reconstruction",
    )
    verify_receipt_and_build(root, science.classification)
    verify_inputs_and_process_evidence(root, science.classification)
    return science.classification


def main() -> int:
    if len(sys.argv) != 2:
        print(INVALID)
        print(
            "GMRES-ACTIVITY ARTIFACT INVALID: expected exactly one artifact path",
            file=sys.stderr,
        )
        return 2
    try:
        classification = verify_artifact(Path(sys.argv[1]))
    except Exception as exc:
        print(INVALID)
        print(f"GMRES-ACTIVITY ARTIFACT INVALID: {exc}", file=sys.stderr)
        return 2
    print(classification)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
