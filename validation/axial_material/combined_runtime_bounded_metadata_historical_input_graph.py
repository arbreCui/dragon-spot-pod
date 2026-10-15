"""Fresh complete combined-runtime input graph mechanics; source-only draft.

Retargeted schema/category literals from the reviewed 884 throughput draft.
All reader, owner, namespace, alias, negative-input, trace and verification
functions are byte-exact inherited. This module is not an adapter or a business
factory. The caller must provide a source-audited complete transitive closure,
bind the actual historical Root PREP and unfiltered component INPUT bodies,
observe the new actual Root declaration exit, and separately recheck all mutable
predicates in every phase. Historical INPUT reuse requires reviewed complete
source-owned closure. It never claims that the original APIs were rerun now. It grants no mathematical, native-RSS, cold, AAA or ABA qualification.

This is a new complete-input-graph contract. It is not evidence that the parent
APIs or their controls were executed again during a later verification phase.
There is no scope filtering or persistent hash/stat cache. Optional inherited
consumer functions are not a combined-runtime business path; the combined
factory must require the complete schema, consumer_scope=None and all owners.
No combined-runtime API, native child or artifact family is invoked here.
"""

from __future__ import annotations

import copy
import hashlib
import errno
import json
import math
import os
import stat
import sys
from collections.abc import Mapping
from pathlib import PurePosixPath


SCHEMA = 'AXMAT_COMBINED_RUNTIME_VERIFIED_INPUT_GRAPH_V5'
CONSUMER_SCHEMA = 'AXMAT_COMBINED_RUNTIME_CONSUMER_SCOPED_INPUT_GRAPH_V2'
CONSUMER_CONTRACT_SCHEMA = 'AXMAT_COMBINED_RUNTIME_EXPLICIT_CONSUMER_INPUT_SCOPE_V1'
CONSUMER_PARENT_OWNER = "Externally pinned complete combined-runtime declaration graph metadata only"
CONSUMER_PHASES = ()
CONSUMER_SELECTION = "UNUSED_COMBINED_RUNTIME_CONSUMER_SCOPE_NO_BUSINESS_ADMISSION"
VERIFICATION_SCHEMA = 'AXMAT_COMBINED_RUNTIME_FRESH_INPUT_GRAPH_VERIFICATION_V2'
REQUIREMENT_TABLE_SCHEMA = 'AXMAT_COMBINED_RUNTIME_COMPLETE_TYPED_REQUIREMENT_TABLE_V1'
REQUIREMENT_COLUMNS = ("path", "canonical_path", "owner", "category", "binding_role")
OWNER_TABLE_SCHEMA = 'AXMAT_COMBINED_RUNTIME_COMPLETE_EXPECTED_OWNER_TABLE_V1'
NAMESPACE_SCHEMA = 'AXMAT_EXPLICIT_SEALED_INPUT_NAMESPACE_V1'
TRACE_SCHEMA = 'AXMAT_READ_OPEN_ATTEMPT_TRACE_V1'
LIVE_IO_SCOPE = "LIVE_OS_PROBE_STDIO_ONLY_NO_INPUT_BYTES_OR_SCIENCE"
INPUT_SCOPE = "INPUT_ONLY_NO_SCIENCE_OR_RESOURCE_DECISION"
NEW_INPUT_ROLE = "NEWLY_DECLARED_INPUT_ONLY"
ABSENCE_INPUT_ROLE = "NEWLY_DECLARED_ABSENCE_INPUT_ONLY"
REQUIREMENT_ROLES = ("EXPECTED_INPUT_BYTES", "OWNED_EXHAUSTIVE_NAMESPACE_BYTES",
                     "OWNED_EXHAUSTIVE_NAMESPACE_ALIAS_TARGET_BYTES", NEW_INPUT_ROLE)
ABSENCE_SCHEMA = 'AXMAT_COMBINED_RUNTIME_DECLARED_INPUT_ABSENCE_OBSERVATION_V1'
CHUNK_BYTES = 8 * 1024 * 1024
MAX_JSON_BYTES = 64 * 1024 * 1024
FRESH_READER_CONTRACT = {
    "schema": "AXMAT_REFERENCE_FRESH_UNION_SINGLE_PARENT_JSON_READER_V1",
    "chunk_bytes": CHUNK_BYTES,
    "max_json_bytes": MAX_JSON_BYTES,
    "canonical_union_fresh_bytes_required_every_phase": True,
    "parent_json_read_once_in_its_existing_typed_union_owner": True,
    "parent_json_parsed_from_same_phase_fresh_pinned_bytes": True,
    "no_persistent_hash_or_stat_cache": True,
    "no_input_scope_or_typed_edge_filtering": True,
    "strict_utf8_duplicate_key_and_nonfinite_rejection": True,
    "original_requirement_and_owner_tables_lossless_and_unchanged": True,
}
CLOSURE_CATEGORIES = ('code_environment', 'original92_build', 'memory_build', 'dedup_build', 'physical_build', 'capture', 'component_ancestry', 'component_terminals', 'source_namespace')


class InputGraphError(ValueError):
    """A declared input requirement, byte identity, or coverage is not satisfied."""


def _require(condition, message):
    if not condition:
        raise InputGraphError(message)


def _path(value):
    value = os.fspath(value)
    _require(isinstance(value, str) and value and "\x00" not in value,
             "an input path must be a nonempty filesystem string")
    _require(os.path.isabs(value) and os.path.normpath(value) == value,
             f"an input path must be absolute and normalized: {value!r}")
    return value


def _relative(value):
    _require(isinstance(value, str) and value and "\x00" not in value,
             "a namespace member must be a nonempty relative string")
    parts = PurePosixPath(value).parts
    _require(not value.startswith("/") and "\\" not in value
             and all(p not in ("", ".", "..") for p in parts)
             and str(PurePosixPath(value)) == value,
             f"unsafe namespace member: {value!r}")
    return value


def _sha(value):
    _require(isinstance(value, str) and len(value) == 64
             and all(c in "0123456789abcdef" for c in value),
             f"expected a lowercase SHA256, got {value!r}")
    return value


def _label(value, field):
    _require(isinstance(value, str) and value.strip(), f"missing {field}")
    return value


def _category(value):
    _require(value in CLOSURE_CATEGORIES, f"unknown closure category: {value!r}")
    return value


def _json_clone(value):
    # Builtin finite JSON data can be copied without a complete text/byte round
    # trip. Each mutable dict/list is independently rebuilt; immutable strings
    # may share representation. Sorted key order and all value types are kept.
    class CanonicalFallback(Exception):
        pass

    def clone(item):
        kind = type(item)
        if kind is dict:
            if not all(type(key) is str for key in item):
                raise CanonicalFallback()
            return {key: clone(item[key]) for key in sorted(item)}
        if kind is list:
            return [clone(part) for part in item]
        if kind in (str, bool, type(None)):
            return item
        if kind is int:
            str(item)  # retain Python's original JSON decimal conversion limit
            return item
        if kind is float:
            if not math.isfinite(item):
                raise ValueError("nonfinite JSON value")
            return item
        raise CanonicalFallback()

    try:
        try:
            return clone(value)
        except (CanonicalFallback, RecursionError):
            encoded = json.dumps(value, sort_keys=True, separators=(",", ":"),
                                 ensure_ascii=True, allow_nan=False)
            return json.loads(encoded)
    except (TypeError, ValueError, OverflowError) as exc:
        raise InputGraphError("snapshot/descriptors must be finite JSON data") from exc


def _canonical_json(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("utf-8")


def _content_digest(graph):
    # Same canonical JSON bytes and SHA as _canonical_json, without materializing
    # the entire JSON text plus a second complete UTF-8 byte buffer in memory.
    data = dict(graph)
    data.pop("content_sha256", None)
    encoder = json.JSONEncoder(sort_keys=True, separators=(",", ":"),
                               ensure_ascii=True, allow_nan=False)
    digest = hashlib.sha256()
    for piece in encoder.iterencode(data):
        digest.update(piece.encode("utf-8"))
    return digest.hexdigest()


def _requirement_table(requirements):
    """Losslessly represent every logical edge with explicit string tables.

    This changes only the serialized representation.  Literal and canonical
    paths are separate columns, duplicate edges are retained, and the row order
    is the same complete order as the former expanded dictionaries.  No digest,
    owner, role, or fresh filesystem observation is inferred from an index.
    Verification rebuilds this entire table from the freshly checked owners,
    namespaces, aliases and new-input roles, then compares it exactly.  It never
    expands the saved table into a second set of large dictionaries.
    """
    fields = set(REQUIREMENT_COLUMNS)
    roles = REQUIREMENT_ROLES
    for entry in requirements:
        _require(isinstance(entry, Mapping) and set(entry) == fields,
                 "unexpected logical requirement fields")
        _path(entry["path"])
        _path(entry["canonical_path"])
        _label(entry["owner"], "logical requirement owner")
        _category(entry["category"])
        _require(entry["binding_role"] in roles, "unknown logical requirement role")
    ordered = sorted(requirements, key=lambda item: (
        item["canonical_path"], item["owner"], item["path"],
        item["category"], item["binding_role"]))
    paths = sorted({entry[field] for entry in ordered
                    for field in ("path", "canonical_path")})
    names = sorted({entry["owner"] for entry in ordered})
    path_ids = {value: index for index, value in enumerate(paths)}
    owner_ids = {value: index for index, value in enumerate(names)}
    category_ids = {value: index for index, value in enumerate(CLOSURE_CATEGORIES)}
    role_ids = {value: index for index, value in enumerate(roles)}
    return {
        "schema": REQUIREMENT_TABLE_SCHEMA,
        "columns": list(REQUIREMENT_COLUMNS),
        "paths": paths, "owners": names, "categories": list(CLOSURE_CATEGORIES),
        "binding_roles": list(roles),
        "rows": [[path_ids[entry["path"]], path_ids[entry["canonical_path"]],
                  owner_ids[entry["owner"]], category_ids[entry["category"]],
                  role_ids[entry["binding_role"]]] for entry in ordered],
        "duplicate_edges_retained": True,
        "scope": INPUT_SCOPE,
    }


def _validate_requirement_table(table):
    """Reject malformed saved indexes before touching the scientific inputs."""
    _require(isinstance(table, Mapping) and set(table) == {
        "schema", "columns", "paths", "owners", "categories", "binding_roles",
        "rows", "duplicate_edges_retained", "scope"},
        "unexpected logical requirement table fields")
    _require(table["schema"] == REQUIREMENT_TABLE_SCHEMA
             and table["columns"] == list(REQUIREMENT_COLUMNS)
             and table["categories"] == list(CLOSURE_CATEGORIES)
             and table["binding_roles"] == list(REQUIREMENT_ROLES)
             and table["duplicate_edges_retained"] is True
             and table["scope"] == INPUT_SCOPE, "logical requirement table contract changed")
    for key, validate in (("paths", _path), ("owners", lambda name: _label(name, "requirement owner"))):
        _require(isinstance(table[key], list), "logical requirement string table must be a list")
        for value in table[key]:
            _require(isinstance(value, str), "logical requirement symbols must be strings")
            validate(value)
        _require(table[key] == sorted(set(table[key])),
                 "logical requirement string table is not sorted and unique")
    _require(isinstance(table["rows"], list), "logical requirement rows must be a list")
    limits = (len(table["paths"]), len(table["paths"]), len(table["owners"]),
              len(CLOSURE_CATEGORIES), len(REQUIREMENT_ROLES))
    for row in table["rows"]:
        _require(isinstance(row, list) and len(row) == len(REQUIREMENT_COLUMNS)
                 and all(type(index) is int and 0 <= index < limit
                         for index, limit in zip(row, limits)),
                 "invalid or out-of-range logical requirement index")


def _owner_table(owners, requirements):
    """Preserve every original expected path/SHA edge using shared symbols.

    Expected digests come only from the normalized typed source owners, never
    from newly observed canonical-file bytes.  Literal aliases remain distinct
    from their targets.  Descriptor and map iteration order, repeated owners,
    and an absent versus explicitly empty new-input list are retained.
    """
    path_ids = {value: index for index, value in enumerate(requirements["paths"])}
    extra_names = sorted({owner["owner"] for owner in owners} - set(requirements["owners"]))
    names = requirements["owners"] + extra_names
    owner_ids = {value: index for index, value in enumerate(names)}
    category_ids = {value: index for index, value in enumerate(CLOSURE_CATEGORIES)}
    digests = sorted({digest for owner in owners for digest in owner["expected_files"].values()})
    digest_ids = {value: index for index, value in enumerate(digests)}
    pins = sorted({(path_ids[path], digest_ids[digest]) for owner in owners
                   for path, digest in owner["expected_files"].items()})
    pin_ids = {value: index for index, value in enumerate(pins)}
    rows = []
    for owner in owners:
        row = [owner_ids[owner["owner"]], category_ids[owner["category"]],
               [pin_ids[(path_ids[path], digest_ids[digest])]
                for path, digest in owner["expected_files"].items()]]
        if "newly_declared_input_paths" in owner:
            row.append([path_ids[path] for path in owner["newly_declared_input_paths"]])
        rows.append(row)
    return {"schema": OWNER_TABLE_SCHEMA, "scope": INPUT_SCOPE,
            "symbol_source": REQUIREMENT_TABLE_SCHEMA,
            "columns": ["owner", "category", "expected_file_pin_indices", "optional_new_input_path_indices"],
            "extra_owner_names": extra_names, "expected_sha256s": digests,
            "expected_file_pins": [list(pin) for pin in pins], "rows": rows,
            "duplicate_descriptors_retained": True,
            "expected_hashes_come_from_typed_owners_not_observed_files": True}


def _expand_owner_table(table, requirements):
    """Strictly decode the complete expected-owner table without new authority."""
    _require(isinstance(table, Mapping) and set(table) == {
        "schema", "scope", "symbol_source", "columns", "extra_owner_names",
        "expected_sha256s", "expected_file_pins", "rows", "duplicate_descriptors_retained",
        "expected_hashes_come_from_typed_owners_not_observed_files"},
        "unexpected expected-owner table fields")
    _require(table["schema"] == OWNER_TABLE_SCHEMA and table["scope"] == INPUT_SCOPE
             and table["symbol_source"] == REQUIREMENT_TABLE_SCHEMA
             and table["columns"] == ["owner", "category", "expected_file_pin_indices", "optional_new_input_path_indices"]
             and table["duplicate_descriptors_retained"] is True
             and table["expected_hashes_come_from_typed_owners_not_observed_files"] is True,
             "expected-owner table contract changed")
    paths = requirements["paths"]
    extras = table["extra_owner_names"]
    _require(isinstance(extras, list), "additional owner names must be a list")
    for name in extras:
        _label(name, "additional empty file owner")
    _require(extras == sorted(set(extras)) and not set(extras) & set(requirements["owners"]),
             "additional owner names conflict or are not sorted and unique")
    names = requirements["owners"] + extras
    digests = table["expected_sha256s"]
    _require(isinstance(digests, list), "expected SHA pool must be a list")
    for digest in digests:
        _sha(digest)
    _require(digests == sorted(set(digests)), "expected SHA pool is not sorted and unique")
    pins = table["expected_file_pins"]
    _require(isinstance(pins, list), "expected file pin pool must be a list")
    for pin in pins:
        _require(isinstance(pin, list) and len(pin) == 2
                 and type(pin[0]) is int and 0 <= pin[0] < len(paths)
                 and type(pin[1]) is int and 0 <= pin[1] < len(digests),
                 "invalid expected literal-path/SHA indexes")
    _require(pins == [list(pin) for pin in sorted({tuple(pin) for pin in pins})],
             "expected file pin pool is not sorted and unique")
    _require(isinstance(table["rows"], list), "expected owner rows must be a list")
    owners = []
    for row in table["rows"]:
        _require(isinstance(row, list) and len(row) in (3, 4)
                 and type(row[0]) is int and 0 <= row[0] < len(names)
                 and type(row[1]) is int and 0 <= row[1] < len(CLOSURE_CATEGORIES)
                 and isinstance(row[2], list)
                 and all(type(index) is int and 0 <= index < len(pins) for index in row[2]),
                 "invalid expected-owner descriptor indexes")
        literal_ids = [pins[index][0] for index in row[2]]
        _require(len(literal_ids) == len(set(literal_ids)),
                 "duplicate literal path in one expected-owner descriptor")
        owner = {"owner": names[row[0]], "category": CLOSURE_CATEGORIES[row[1]],
                 "expected_files": {paths[pins[index][0]]: digests[pins[index][1]] for index in row[2]}}
        if len(row) == 4:
            _require(isinstance(row[3], list)
                     and all(type(index) is int and 0 <= index < len(paths) for index in row[3]),
                     "invalid explicit new-input path indexes")
            new_paths = [paths[index] for index in row[3]]
            _require(new_paths == sorted(set(new_paths)), "explicit new-input paths are not sorted and unique")
            owner["newly_declared_input_paths"] = new_paths
        owners.append(owner)
    _require(_owner_table(owners, requirements) == table,
             "expected owner table has unused/conflicting symbols or changed full representation")
    return owners


def _alias_descriptor(value):
    _require(isinstance(value, Mapping), "alias descriptor must be a mapping")
    allowed = {"path", "text", "target", "kind", "sha256"}
    _require(set(value) <= allowed, f"unknown alias fields: {set(value) - allowed}")
    path, target = _path(value["path"]), _path(value["target"])
    text = value["text"]
    _require(isinstance(text, str) and text and "\x00" not in text,
             f"invalid symlink text for {path}")
    kind = value.get("kind", "file")
    _require(kind in ("file", "directory"), f"invalid alias target kind: {path}")
    result = {"path": path, "text": text, "target": target, "kind": kind}
    if value.get("sha256") is not None:
        _require(kind == "file", "a directory alias cannot have a byte digest")
        result["sha256"] = _sha(value["sha256"])
    return result


def _alias_map(values):
    result = {}
    for value in values:
        value = _alias_descriptor(value)
        old = result.get(value["path"])
        if old is not None:
            for field in ("path", "text", "target", "kind"):
                _require(old[field] == value[field],
                         f"conflicting alias owners: {value['path']}")
            if "sha256" in old and "sha256" in value:
                _require(old["sha256"] == value["sha256"],
                         f"conflicting alias digests: {value['path']}")
            if "sha256" in value:
                old["sha256"] = value["sha256"]
        else:
            result[value["path"]] = value
    return result


def _resolve(path, aliases, *, kind=None, stack=()):
    """Resolve only through explicitly declared, literal symlink components."""
    path = _path(path)
    _require(len(stack) < 64, f"too many symlink components: {path}")
    current = "/"
    parts = PurePosixPath(path).parts[1:]
    for index, part in enumerate(parts):
        candidate = os.path.join(current, part)
        try:
            info = os.lstat(candidate)
        except OSError as exc:
            raise InputGraphError(f"input component is unavailable: {candidate}") from exc
        if stat.S_ISLNK(info.st_mode):
            _require(candidate in aliases, f"undeclared symlink component: {candidate}")
            _require(candidate not in stack, f"symlink cycle: {candidate}")
            expected = aliases[candidate]
            raw = os.readlink(candidate)
            _require(raw == expected["text"], f"symlink text changed: {candidate}")
            target = raw if os.path.isabs(raw) else os.path.join(os.path.dirname(candidate), raw)
            target = os.path.normpath(target)
            current = _resolve(target, aliases, kind=expected["kind"],
                               stack=stack + (candidate,))
            _require(current == expected["target"],
                     f"symlink canonical target changed: {candidate}")
            # The symlink's lstat describes the literal alias, not its target.
            # Preserve a fresh target observation for the kind check below.
            info = None
        else:
            current = candidate
        if index < len(parts) - 1:
            if info is None:
                info = os.lstat(current)
            _require(stat.S_ISDIR(info.st_mode),
                     f"input ancestor is not a directory: {current}")
    # Reuse only the observation just made in this walk, never another path or
    # phase's filesystem state. The root and a terminal alias still need lstat.
    if not parts or info is None:
        info = os.lstat(current)
    _require(not stat.S_ISLNK(info.st_mode), f"canonical endpoint is a symlink: {current}")
    if kind == "file":
        _require(stat.S_ISREG(info.st_mode), f"input endpoint is not regular: {current}")
    elif kind == "directory":
        _require(stat.S_ISDIR(info.st_mode), f"input endpoint is not a directory: {current}")
    return current


def capture_aliases(paths):
    """Explicit declaration helper: capture literal aliases, without byte/PASS claims.

    Every supplied path must exist.  This is a declaration snapshot, not proof of
    an older alias expectation.  The caller must bind the returned descriptors to
    the actual input admission and pin them in its new declaration.
    """
    found = {}

    def walk(path, stack=()):
        path = _path(path)
        _require(len(stack) < 64, f"too many symlink components: {path}")
        current = "/"
        parts = PurePosixPath(path).parts[1:]
        for index, part in enumerate(parts):
            candidate = os.path.join(current, part)
            info = os.lstat(candidate)
            if stat.S_ISLNK(info.st_mode):
                _require(candidate not in stack, f"symlink cycle: {candidate}")
                raw = os.readlink(candidate)
                target = raw if os.path.isabs(raw) else os.path.join(os.path.dirname(candidate), raw)
                current = walk(os.path.normpath(target), stack + (candidate,))
                mode = os.lstat(current).st_mode
                _require(stat.S_ISREG(mode) or stat.S_ISDIR(mode),
                         f"unsupported alias target: {candidate}")
                value = {"path": candidate, "text": raw, "target": current,
                         "kind": "file" if stat.S_ISREG(mode) else "directory"}
                _require(candidate not in found or found[candidate] == value,
                         f"alias changed while capturing: {candidate}")
                found[candidate] = value
            else:
                current = candidate
            if index < len(parts) - 1:
                _require(stat.S_ISDIR(os.lstat(current).st_mode),
                         f"input ancestor is not a directory: {current}")
        return current

    for path in paths:
        walk(path)
    return [found[path] for path in sorted(found)]


def _file_signature(info):
    return (info.st_dev, info.st_ino, info.st_mode, info.st_size,
            info.st_mtime_ns, info.st_ctime_ns, info.st_nlink)


def _stream(canonical, *, collect=False, max_bytes=None):
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
    _require(hasattr(os, "O_NOFOLLOW"), "this platform lacks O_NOFOLLOW")
    fd = os.open(canonical, flags | os.O_NOFOLLOW)
    chunks = [] if collect else None
    digest = hashlib.sha256()
    length = 0
    try:
        before = os.fstat(fd)
        _require(stat.S_ISREG(before.st_mode), f"opened input is not regular: {canonical}")
        if max_bytes is not None:
            _require(before.st_size <= max_bytes, f"input exceeds read bound: {canonical}")
        while True:
            block = os.read(fd, CHUNK_BYTES)
            if not block:
                break
            length += len(block)
            if max_bytes is not None:
                _require(length <= max_bytes, f"input exceeds read bound: {canonical}")
            digest.update(block)
            if collect:
                chunks.append(block)
        after = os.fstat(fd)
        _require(_file_signature(before) == _file_signature(after)
                 and length == before.st_size,
                 f"input changed during byte read: {canonical}")
        endpoint = os.stat(canonical, follow_symlinks=False)
        _require(_file_signature(endpoint) == _file_signature(after),
                 f"input endpoint changed during byte read: {canonical}")
        result = {"path": canonical, "sha256": digest.hexdigest(), "size_bytes": length}
        return result, b"".join(chunks) if collect else None
    finally:
        os.close(fd)


def strict_pin(path, expected_sha256=None, *, aliases=()):
    """Stream one regular input with a no-follow endpoint and exact alias checks.

    With no expected SHA this makes only a *new input byte binding*.  It never
    says that an old scientific predicate holds.  An alias must be explicitly
    supplied even when an endpoint digest is supplied.
    """
    path = _path(path)
    declared = _alias_map(aliases)
    canonical = _resolve(path, declared, kind="file")
    result, _ = _stream(canonical)
    _require(_resolve(path, declared, kind="file") == canonical,
             f"alias changed during input read: {path}")
    if expected_sha256 is not None:
        _require(result["sha256"] == _sha(expected_sha256), f"input digest changed: {path}")
    for alias in declared.values():
        if alias["kind"] == "file" and alias["target"] == canonical and "sha256" in alias:
            _require(alias["sha256"] == result["sha256"], f"alias target digest changed: {alias['path']}")
    return {"path": path, "canonical_path": canonical, "sha256": result["sha256"],
            "size_bytes": result["size_bytes"],
            "binding_role": "EXPECTED_INPUT_BYTES" if expected_sha256 is not None else NEW_INPUT_ROLE}


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        _require(key not in result, f"duplicate JSON key: {key!r}")
        result[key] = value
    return result


def _invalid_constant(value):
    raise InputGraphError(f"nonfinite JSON constant: {value}")


def _finite_float(text):
    value = float(text)
    _require(math.isfinite(value), "snapshot/descriptors must be finite JSON data")
    return value


def _unique_sorted_object(pairs):
    # Preserve the former JSON roundtrip's object order without re-encoding the
    # complete parsed document. Duplicate rejection stays in the original hook.
    value = _unique_object(pairs)
    return {key: value[key] for key in sorted(value)}


def strict_json(path, expected_sha256=None, *, aliases=(), max_bytes=MAX_JSON_BYTES):
    """Read and parse a pinned JSON file once, rejecting duplicate/nonfinite data."""
    _require(type(max_bytes) is int and max_bytes > 0, "invalid JSON read bound")
    declared = _alias_map(aliases)
    canonical = _resolve(_path(path), declared, kind="file")
    pin, payload = _stream(canonical, collect=True, max_bytes=max_bytes)
    _require(_resolve(_path(path), declared, kind="file") == canonical,
             f"JSON alias changed during read: {path}")
    if expected_sha256 is not None:
        _require(pin["sha256"] == _sha(expected_sha256), f"JSON digest changed: {path}")
    for alias in declared.values():
        if alias["kind"] == "file" and alias["target"] == canonical and "sha256" in alias:
            _require(alias["sha256"] == pin["sha256"], f"JSON alias target digest changed: {alias['path']}")
    return _parse_strict_json_payload(payload, path)


def _parse_strict_json_payload(payload, path):
    """Interpret only this phase's fully checked, bounded UTF-8 JSON bytes."""
    _require(type(payload) is bytes, "fresh JSON payload must be immutable bytes")
    try:
        return json.loads(payload.decode("utf-8"), object_pairs_hook=_unique_sorted_object,
                          parse_constant=_invalid_constant, parse_float=_finite_float)
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise InputGraphError(f"invalid UTF-8 JSON: {path}") from exc


def _scan_namespace(root, aliases):
    canonical = _resolve(root, aliases, kind="directory")
    files, links, directories = set(), {}, set()
    pending = [(canonical, "")]
    while pending:
        absolute, relative = pending.pop()
        before = os.stat(absolute, follow_symlinks=False)
        _require(stat.S_ISDIR(before.st_mode), f"namespace directory changed: {absolute}")
        with os.scandir(absolute) as entries:
            values = list(entries)
        for entry in values:
            rel = entry.name if not relative else relative + "/" + entry.name
            _relative(rel)
            mode = entry.stat(follow_symlinks=False).st_mode
            if stat.S_ISREG(mode):
                files.add(rel)
            elif stat.S_ISLNK(mode):
                links[rel] = os.readlink(entry.path)
            elif stat.S_ISDIR(mode):
                directories.add(rel)
                pending.append((entry.path, rel))
            else:
                raise InputGraphError(f"nonregular namespace endpoint: {entry.path}")
        after = os.stat(absolute, follow_symlinks=False)
        _require(_file_signature(before) == _file_signature(after),
                 f"namespace directory changed while listing: {absolute}")
    _require(_resolve(root, aliases, kind="directory") == canonical,
             f"namespace root alias changed: {root}")
    return {"canonical_root": canonical, "files": files, "symlinks": links,
            "directories": directories}


def explicit_sealed_namespace(root, files, symlinks=None, *, owner, category,
                              directories=None, aliases=()):
    """Declare an exhaustive namespace from explicit old expected members.

    ``files`` maps relative regular names to expected SHA256.  ``symlinks`` maps
    relative names to {text,target,kind,sha256?}.  Unknown regular names fail;
    they are never silently granted an old seal/PASS by hashing them now.
    If directories is omitted, the actual directory-only inventory is captured
    as a new namespace binding.  File bytes are streamed by create/verify_graph.
    A seal JSON that lists only selected outputs is *not* an exhaustive inventory.
    """
    root = _path(root)
    _require(isinstance(files, Mapping), "namespace files must be a relative SHA map")
    regular = {_relative(name): _sha(digest) for name, digest in files.items()}
    link_values = {}
    for name, value in (symlinks or {}).items():
        name = _relative(name)
        _require(isinstance(value, Mapping), "namespace symlink requires an explicit descriptor")
        link_values[name] = _alias_descriptor(dict(value, path=os.path.join(root, name)))
    _require(not set(regular) & set(link_values), "file/symlink namespace ownership conflict")
    declared = _alias_map(list(aliases) + list(link_values.values()))
    actual = _scan_namespace(root, declared)
    _require(actual["files"] == set(regular), f"regular namespace differs: {root}")
    _require(actual["symlinks"] == {name: value["text"] for name, value in link_values.items()},
             f"symlink namespace differs: {root}")
    expected_dirs = actual["directories"] if directories is None else {_relative(name) for name in directories}
    _require(actual["directories"] == expected_dirs, f"directory namespace differs: {root}")
    for value in link_values.values():
        _require(_resolve(value["path"], declared, kind=value["kind"]) == value["target"],
                 f"namespace symlink target differs: {value['path']}")
    return {"schema": NAMESPACE_SCHEMA, "root": root,
            "canonical_root": actual["canonical_root"], "owner": _label(owner, "namespace owner"),
            "category": _category(category), "files": regular,
            "symlinks": {name: {key: val for key, val in value.items() if key != "path"}
                         for name, value in link_values.items()},
            "directories": sorted(expected_dirs), "namespace_exhaustive": True}


def _namespace_descriptor(value):
    _require(isinstance(value, Mapping) and value.get("schema") == NAMESPACE_SCHEMA
             and value.get("namespace_exhaustive") is True,
             "only an explicit exhaustive namespace descriptor is admissible")
    _require(set(value) == {"schema", "root", "canonical_root", "owner", "category", "files",
                            "symlinks", "directories", "namespace_exhaustive"},
             "unexpected namespace descriptor fields")
    _path(value["root"])
    _path(value["canonical_root"])
    _label(value["owner"], "namespace owner")
    _category(value["category"])
    _require(isinstance(value["files"], Mapping) and isinstance(value["symlinks"], Mapping)
             and isinstance(value["directories"], list), "invalid exhaustive namespace maps")
    for name, digest in value["files"].items():
        _relative(name)
        _sha(digest)
    for name, descriptor in value["symlinks"].items():
        _relative(name)
        _alias_descriptor(dict(descriptor, path=os.path.join(value["root"], name)))
    for name in value["directories"]:
        _relative(name)
    _require(len(set(value["directories"])) == len(value["directories"]), "duplicate namespace directory")
    _require(not set(value["files"]) & set(value["symlinks"]), "namespace endpoint kind conflict")
    return _json_clone(value)


def _owners(values):
    """Normalize only documented typed fields; never inspect arbitrary strings."""
    result = []
    for value in values:
        _require(isinstance(value, Mapping), "owner must be a typed mapping")
        owner = _label(value.get("owner"), "file owner")
        category = _category(value.get("category"))
        kind = value.get("kind", "files")
        if kind == "pin":
            _require(set(value) <= {"owner", "category", "kind", "path", "sha256"},
                     f"unknown pin owner fields: {owner}")
            mapping = {value["path"]: value["sha256"]}
        else:
            _require(kind in ("files", "outputs"), f"unsupported typed owner kind: {kind}")
            keys = [key for key in ("expected_files", "files", "outputs") if key in value]
            _require(len(keys) == 1, f"owner requires exactly one explicit SHA map: {owner}")
            _require(set(value) <= {"owner", "category", "kind", keys[0], "newly_declared_input_paths"},
                     f"unknown file owner fields: {owner}")
            mapping = value[keys[0]]
        _require(isinstance(mapping, Mapping), f"owner SHA map is invalid: {owner}")
        descriptor = {"owner": owner, "category": category,
                      "expected_files": {_path(path): _sha(digest) for path, digest in mapping.items()}}
        if "newly_declared_input_paths" in value:
            paths = value["newly_declared_input_paths"]
            _require(isinstance(paths, list), "owner new input paths must be an explicit list")
            descriptor["newly_declared_input_paths"] = sorted({_path(path) for path in paths})
        result.append(descriptor)
    return result


def _new_inputs(values):
    _require(isinstance(values, Mapping), "newly declared inputs require an explicit path descriptor map")
    result = {}
    for path, value in values.items():
        _require(isinstance(value, Mapping), "new input requires a reason and owner descriptor")
        _require(set(value) <= {"owner", "category", "reason"}, "unexpected new input fields")
        result[_path(path)] = {"owner": _label(value.get("owner"), "new input owner"),
                              "category": _category(value.get("category")),
                              "reason": _label(value.get("reason"), "new input reason"),
                              "binding_role": NEW_INPUT_ROLE}
    return result


def _under(path, root):
    return path == root or path.startswith(root.rstrip("/") + "/")


def _absence_inputs(values):
    _require(isinstance(values, Mapping), "absent inputs require an explicit path/owner/reason map")
    result = {}
    for path, value in values.items():
        _require(isinstance(value, Mapping) and set(value) == {"owner", "category", "reason"},
                 "absent input requires exactly owner/category/reason")
        result[_path(path)] = {"owner": _label(value["owner"], "absent input owner"),
                              "category": _category(value["category"]),
                              "reason": _label(value["reason"], "absent input reason"),
                              "binding_role": ABSENCE_INPUT_ROLE}
    return result


def _absence_observation(path, aliases):
    """Observe exact ENOENT and every existing directory, with declared aliases.

    Missing parent directories are valid only at the declared first missing
    component.  Existing files, broken aliases, inaccessible parents and every
    error other than ENOENT reject.  Directory identity excludes timestamps and
    unrelated contents; an ancestor replacement or new empty parent still
    changes this declared negative input and requires a new declaration.
    """
    path = _path(path)
    _require(path != "/", "the root directory cannot be an absent input")
    current, ancestors = "/", []
    root_info = os.lstat(current)
    _require(stat.S_ISDIR(root_info.st_mode), "absence root is not a directory")
    ancestors.append({"literal_component": "/", "canonical_path": "/",
                      "identity": _fd_identity(root_info)})
    parts = PurePosixPath(path).parts[1:]
    for index, part in enumerate(parts):
        candidate = os.path.join(current, part)
        literal = "/" + "/".join(parts[:index + 1])
        try:
            info = os.lstat(candidate)
        except OSError as exc:
            _require(exc.errno == errno.ENOENT,
                     f"absent input observation was not ENOENT: {candidate}: {exc}")
            return {"schema": ABSENCE_SCHEMA, "path": path,
                    "canonical_absent_path": os.path.join(candidate, *parts[index + 1:]),
                    "first_missing_component": candidate, "missing_errno": errno.ENOENT,
                    "existing_ancestors": ancestors, "regular_input_bytes": 0,
                    "scope": INPUT_SCOPE, "observation": "EXACT_DECLARED_ENOENT_ONLY"}
        _require(index < len(parts) - 1, f"declared absent input exists: {path}")
        if stat.S_ISLNK(info.st_mode):
            _require(candidate in aliases and aliases[candidate]["kind"] == "directory",
                     f"absent input has an undeclared/non-directory ancestor alias: {candidate}")
            current = _resolve(candidate, aliases, kind="directory")
            info = os.lstat(current)
        else:
            _require(stat.S_ISDIR(info.st_mode), f"absent input ancestor is not a directory: {candidate}")
            current = candidate
        _require(stat.S_ISDIR(info.st_mode) and not stat.S_ISLNK(info.st_mode),
                 f"absent input canonical ancestor is not a directory: {current}")
        ancestors.append({"literal_component": literal, "canonical_path": current,
                          "identity": _fd_identity(info)})
    raise InputGraphError(f"declared absent input was not absent: {path}")


def _absence_phase(values, aliases, *, expected=None):
    actual = {path: _absence_observation(path, aliases) for path in sorted(values)}
    if expected is not None:
        _require(isinstance(expected, Mapping) and set(expected) == set(values),
                 "declared absent input observation set changed")
        _require(actual == expected, "declared absent input or its existing ancestors/aliases changed")
    return actual


def _fd_identity(info):
    return {"device": info.st_dev, "inode": info.st_ino, "mode": info.st_mode,
            "rdev": info.st_rdev, "major": os.major(info.st_rdev),
            "minor": os.minor(info.st_rdev)}


def _identity(value):
    _require(isinstance(value, Mapping)
             and set(value) == {"device", "inode", "mode", "rdev", "major", "minor"}
             and all(type(item) is int and item >= 0 for item in value.values()),
             "invalid actual descriptor/device identity")
    _require(os.major(value["rdev"]) == value["major"]
             and os.minor(value["rdev"]) == value["minor"], "device number decomposition changed")
    return dict(value)


def capture_live_character_device(path, *, owner, reason):
    """Bind only actual os.devnull metadata, never device bytes or a PASS.

    The caller must explicitly allow this descriptor in live_io_requirements.
    A read/write open is admissible only when the same real stdlib Popen object
    later audits this exact device as one of its actual stdio handles.  All path
    components are literal, with no aliases.  Each graph verification repeats
    this metadata check; callers must separately recheck current OS identity.
    """
    path = _path(path)
    _require(path == os.devnull, "only the explicit platform null stdio device is supported")
    _require(os.path.realpath(path) == path, "live null device cannot use an alias")
    current = "/"
    for part in PurePosixPath(path).parts[1:]:
        current = os.path.join(current, part)
        _require(not stat.S_ISLNK(os.lstat(current).st_mode), "live device ancestor is an alias")
    info = os.lstat(path)
    _require(stat.S_ISCHR(info.st_mode), "the explicit null device is not a character device")
    return {"kind": "character_device", "path": path,
            "owner": _label(owner, "live device owner"), "reason": _label(reason, "live device reason"),
            "identity": _fd_identity(info), "scope": LIVE_IO_SCOPE,
            "requires_actual_subprocess_stdio": True}


def _executable_binding(literal, cwd, environment):
    """Fresh PATH lookup only; byte owners and actual child success are separate."""
    import shutil
    _require(isinstance(literal, str) and literal and "\x00" not in literal,
             "subprocess literal executable is missing")
    _path(cwd)
    if os.path.dirname(literal):
        candidate = literal if os.path.isabs(literal) else os.path.join(cwd, literal)
        selected = shutil.which(os.path.normpath(candidate))
        path_environment = None
    else:
        env = os.environ if environment is None else environment
        path_environment = env.get("PATH", os.defpath)
        _require(isinstance(path_environment, str), "unresolved actual PATH environment")
        # Relative PATH components are interpreted at the child's actual cwd;
        # this avoids changing cwd or replacing a production callable.
        search = os.pathsep.join(os.path.normpath(item if os.path.isabs(item)
                               else os.path.join(cwd, item))
                               for item in path_environment.split(os.pathsep))
        selected = shutil.which(literal, path=search)
    _require(selected is not None, "actual executable PATH candidate is unavailable")
    return _path(os.path.normpath(selected)), path_environment


def _command(value):
    _require(isinstance(value, Mapping)
             and set(value) == {"literal_executable", "executable", "argv", "cwd", "environment",
                               "path_environment"},
             "live subprocess command requires exact literal/PATH/executable/argv/cwd/environment")
    _path(value["executable"])
    _path(value["cwd"])
    _require(isinstance(value["argv"], list) and value["argv"]
             and all(isinstance(arg, str) and "\x00" not in arg for arg in value["argv"]),
             "subprocess argv must retain the actual nonempty argument list")
    env = value["environment"]
    _require(env is None or (isinstance(env, Mapping)
             and all(isinstance(key, str) and isinstance(item, str)
                     and "\x00" not in key and "\x00" not in item for key, item in env.items())),
             "subprocess environment must be exact or explicitly inherited (null)")
    _label(value["literal_executable"], "actual literal executable")
    _require(value["path_environment"] is None or isinstance(value["path_environment"], str),
             "actual PATH must be explicit or null for a qualified executable")
    return _json_clone(value)


def _live_io(values):
    result = []
    seen = set()
    for value in values:
        _require(isinstance(value, Mapping), "live I/O allowance must be explicit")
        kind = value.get("kind")
        _require(value.get("scope") == LIVE_IO_SCOPE, "live I/O cannot grant input or science semantics")
        owner, reason = _label(value.get("owner"), "live I/O owner"), _label(value.get("reason"), "live I/O reason")
        if kind == "character_device":
            _require(set(value) == {"kind", "path", "owner", "reason", "identity", "scope",
                                    "requires_actual_subprocess_stdio"}
                     and value["requires_actual_subprocess_stdio"] is True,
                     "null device requires a true command-owned stdio association")
            _require(_path(value["path"]) == os.devnull, "unsupported live character device")
            _require(stat.S_ISCHR(_identity(value["identity"])["mode"]), "null descriptor is not character type")
            key = (kind, value["path"])
        elif kind == "subprocess_stdio":
            _require(set(value) == {"kind", "owner", "reason", "command", "scope"},
                     "unknown live subprocess allowance fields")
            _command(value["command"])
            key = (kind, _canonical_json(value["command"]))
        else:
            raise InputGraphError("unsupported live I/O allowance kind")
        _require(key not in seen, "duplicate or conflicting live I/O allowance")
        seen.add(key)
        result.append(_json_clone(dict(value, owner=owner, reason=reason)))
    return result


def _trace_records(values):
    if isinstance(values, Mapping):
        _require(values.get("schema") == TRACE_SCHEMA, "unknown read trace schema")
        _require(values.get("coverage") == "PYTHON_AUDIT_OPEN_ATTEMPTS_ONLY",
                 "read trace must state its actual limited coverage")
        values = values.get("records")
    _require(isinstance(values, (list, tuple)), "read trace must be a list or audit descriptor")
    result = []
    for value in values:
        _require(isinstance(value, Mapping) and value.get("event") == "open",
                 "unrecognized read-open trace event")
        _require(value.get("kind") in ("path", "descriptor"), "unresolved descriptor/non-path read trace")
        _require(value.get("access") in ("read", "readwrite"), "unresolved input open access")
        _require(value.get("observation") == "OPEN_ATTEMPT", "trace cannot claim an unobserved open outcome")
        _require(type(value.get("attempt_count")) is int and value["attempt_count"] > 0,
                 "read-open trace must retain a positive actual attempt count")
        _require(type(value.get("flags")) is int, "read-open trace has unresolved access flags")
        access_bits = value["flags"] & os.O_ACCMODE
        _require(access_bits in (os.O_RDONLY, os.O_RDWR)
                 and value["access"] == ("readwrite" if access_bits == os.O_RDWR else "read"),
                 "read-open flags/access differ from the actual event")
        record = _json_clone(value)
        _path(record["cwd"])
        if record["kind"] == "path":
            record["path"] = _path(record["path"])
        else:
            _require(type(record.get("descriptor")) is int and record["descriptor"] >= 0,
                     "invalid original file descriptor")
            observed = record.get("descriptor_observation")
            _require(isinstance(observed, Mapping) and observed.get("status") == "FSTAT_OBSERVED",
                     "opaque or unavailable descriptor is never a declared input")
            _identity(observed["identity"])
            _require(observed.get("kind") in ("regular", "fifo", "socket", "character"),
                     "unsupported actual descriptor type")
            if observed["kind"] == "regular":
                _require(observed.get("endpoint_identity_verified_at_attempt") is True,
                         "regular descriptor lacks an actual endpoint identity")
                record["path"] = _path(observed["canonical_path"])
        result.append(record)
    return result


def _subprocess_records(trace):
    values = trace.get("subprocess_records", []) if isinstance(trace, Mapping) else []
    _require(isinstance(values, list), "subprocess audit records must be a list")
    result, seen = [], set()
    for value in values:
        _require(isinstance(value, Mapping) and value.get("event") == "subprocess.Popen"
                 and value.get("observation") == "EXECUTE_CHILD_AUDIT_ATTEMPT"
                 and value.get("actual_stdlib_Popen_object_and_frame") is True,
                 "unresolved or nonstdlib subprocess audit context")
        identifier = value.get("command_id")
        _require(type(identifier) is int and identifier > 0 and identifier not in seen,
                 "invalid/duplicate actual subprocess audit identifier")
        seen.add(identifier)
        _path(value["subprocess_source_path"])
        _command(value["command"])
        _require("audit_cwd_argument" in value and (value["audit_cwd_argument"] is None
                 or isinstance(value["audit_cwd_argument"], str)), "original subprocess cwd argument missing")
        _require(isinstance(value.get("stdio_descriptors"), Mapping), "subprocess stdio identities missing")
        for role, descriptor in value["stdio_descriptors"].items():
            _require(role in ("stdin_read", "stdin_write", "stdout_read", "stdout_write",
                             "stderr_read", "stderr_write", "devnull"), "unrecognized actual stdio role")
            _require(type(descriptor.get("descriptor")) is int and descriptor["descriptor"] >= 0,
                     "invalid actual stdio descriptor")
            _identity(descriptor["identity"])
        result.append(_json_clone(value))
    return result


def _phase(owners, namespaces, aliases, new_inputs, *, frozen_new_pins=None,
           json_input=None):
    expectations = {}
    requirements = []
    new_pins = {}
    # A duplicate logical owner is not a new filesystem observation.  Resolve
    # each distinct literal once before, and once after, this phase's byte reads.
    # The cache is local to this call and never stands in for a fresh byte hash.
    resolved_paths = {}

    def add(path, digest, owner, category, role):
        path = _path(path)
        if path not in resolved_paths:
            resolved_paths[path] = _resolve(path, aliases, kind="file")
        canonical = resolved_paths[path]
        if digest is not None:
            digest = _sha(digest)
            old = expectations.get(canonical)
            _require(old is None or old == digest, f"conflicting expected SHA owners: {canonical}")
            expectations[canonical] = digest
        requirements.append({"path": path, "canonical_path": canonical,
                             "owner": owner, "category": category, "binding_role": role})

    for owner in owners:
        for path, digest in owner["expected_files"].items():
            add(path, digest, owner["owner"], owner["category"], "EXPECTED_INPUT_BYTES")
    for namespace in namespaces:
        actual = _scan_namespace(namespace["root"], aliases)
        _require(actual["canonical_root"] == namespace["canonical_root"], "namespace canonical root changed")
        _require(actual["files"] == set(namespace["files"]), f"regular namespace changed: {namespace['root']}")
        _require(actual["symlinks"] == {name: val["text"] for name, val in namespace["symlinks"].items()},
                 f"symlink namespace changed: {namespace['root']}")
        _require(actual["directories"] == set(namespace["directories"]),
                 f"directory namespace changed: {namespace['root']}")
        for name, digest in namespace["files"].items():
            add(os.path.join(namespace["root"], name), digest, namespace["owner"],
                namespace["category"], "OWNED_EXHAUSTIVE_NAMESPACE_BYTES")
        for name, link in namespace["symlinks"].items():
            if link["kind"] == "file" and "sha256" in link:
                add(os.path.join(namespace["root"], name), link["sha256"], namespace["owner"],
                    namespace["category"], "OWNED_EXHAUSTIVE_NAMESPACE_ALIAS_TARGET_BYTES")
    for path, value in new_inputs.items():
        digest = None if frozen_new_pins is None else frozen_new_pins.get(path)
        if frozen_new_pins is not None:
            _require(digest is not None, f"new input lost its declared byte binding: {path}")
        add(path, digest, value["owner"], value["category"], NEW_INPUT_ROLE)
    for owner in owners:
        for path in owner.get("newly_declared_input_paths", []):
            _require(path in new_inputs, f"owner new input lacks an explicit reason/role: {path}")
            digest = None if frozen_new_pins is None else frozen_new_pins.get(path)
            add(path, digest, owner["owner"], owner["category"], NEW_INPUT_ROLE)
    for alias in aliases.values():
        actual = _resolve(alias["path"], aliases, kind=alias["kind"])
        _require(actual == alias["target"], f"alias canonical target changed: {alias['path']}")
        if alias["kind"] == "file" and "sha256" in alias:
            old = expectations.get(actual)
            _require(old is None or old == alias["sha256"], f"conflicting alias SHA: {alias['path']}")
            expectations[actual] = alias["sha256"]
    canonical_paths = {record["canonical_path"] for record in requirements}
    for alias in aliases.values():
        if alias["kind"] == "file":
            _require(alias["target"] in canonical_paths,
                     f"alias target has no typed file owner: {alias['path']}")
    # The exact parent JSON remains one normal typed canonical-file input.
    # Collect its bytes during the one mandatory union SHA read, not through a
    # second reader/cache. Read it last only to shorten payload lifetime. Every
    # logical requirement keeps its original order, multiplicity and role.
    json_canonical = None
    json_descriptor = None
    fresh_json_payload = None
    if json_input is not None:
        _require(isinstance(json_input, Mapping) and set(json_input) == {"path", "sha256"},
                 "phase JSON must have one exact externally pinned descriptor")
        json_descriptor = {"path": _path(json_input["path"]), "sha256": _sha(json_input["sha256"])}
        _require(json_descriptor["path"] in resolved_paths,
                 "phase JSON must already have an explicit typed file owner")
        json_canonical = resolved_paths[json_descriptor["path"]]
        strict_parent_canonical = _resolve(json_descriptor["path"], {}, kind="file")
        _require(json_canonical == strict_parent_canonical,
                 "parent JSON path or ancestor must not be a declared alias")
        _require(expectations.get(json_canonical) == json_descriptor["sha256"],
                 "phase JSON expected SHA differs from its typed union owner")
    ordered_canonical_paths = sorted(canonical_paths)
    if json_canonical is not None:
        ordered_canonical_paths.remove(json_canonical)
        ordered_canonical_paths.append(json_canonical)
    actual = {}
    for canonical in ordered_canonical_paths:
        collect_json = canonical == json_canonical
        pin, payload = _stream(canonical, collect=collect_json,
                               max_bytes=MAX_JSON_BYTES if collect_json else None)
        expected = expectations.get(canonical)
        _require(expected is None or pin["sha256"] == expected, f"input digest changed: {canonical}")
        actual[canonical] = pin
        if collect_json:
            fresh_json_payload = payload
    for path, canonical in resolved_paths.items():
        _require(_resolve(path, aliases, kind="file") == canonical,
                 f"owner alias changed during phase: {path}")
    for path in new_inputs:
        # Every new input was added above and its literal was freshly resolved
        # again in the preceding post-read loop. Reuse that validated identity.
        canonical = resolved_paths[path]
        new_pins[path] = actual[canonical]["sha256"]
    # Namespace and alias metadata are checked again after all byte reads.  This
    # does not use a prior phase's stat result as evidence for current bytes.
    for namespace in namespaces:
        after = _scan_namespace(namespace["root"], aliases)
        _require(after["canonical_root"] == namespace["canonical_root"]
                 and after["files"] == set(namespace["files"])
                 and after["symlinks"] == {name: val["text"] for name, val in namespace["symlinks"].items()}
                 and after["directories"] == set(namespace["directories"]),
                 f"namespace changed during phase: {namespace['root']}")
    for alias in aliases.values():
        _require(_resolve(alias["path"], aliases, kind=alias["kind"]) == alias["target"],
                 f"alias changed during phase: {alias['path']}")
        if alias["kind"] == "file" and "sha256" in alias:
            _require(actual[alias["target"]]["sha256"] == alias["sha256"],
                     f"alias target byte digest changed: {alias['path']}")
    fresh_json = None
    if json_descriptor is not None:
        _require(type(fresh_json_payload) is bytes,
                 "the complete phase JSON bytes were not read from the typed union")
        fresh_json = {"descriptor": json_descriptor,
                      "pin": actual[json_canonical],
                      "parsed": _parse_strict_json_payload(fresh_json_payload, json_descriptor["path"])}
    return requirements, actual, new_pins, fresh_json


def _coverage(requirements, actual, contract):
    _require(isinstance(contract, Mapping) and set(contract) <= set(CLOSURE_CATEGORIES),
             "invalid explicit coverage contract")
    paths_by_category = {category: set() for category in CLOSURE_CATEGORIES}
    names_by_category = {category: set() for category in CLOSURE_CATEGORIES}
    for entry in requirements:
        category = entry["category"]
        if category in paths_by_category:
            paths_by_category[category].add(entry["canonical_path"])
            names_by_category[category].add(entry["owner"])
    result = {}
    for category in CLOSURE_CATEGORIES:
        paths = paths_by_category[category]
        names = names_by_category[category]
        _require(paths, f"missing transitive closure class: {category}")
        descriptor = contract.get(category, {})
        _require(isinstance(descriptor, Mapping)
                 and set(descriptor) <= {"minimum_files", "minimum_bytes", "required_owner_names"},
                 f"invalid coverage descriptor: {category}")
        count = descriptor.get("minimum_files", 1)
        size = descriptor.get("minimum_bytes", 0)
        _require(type(count) is int and count >= 1 and type(size) is int and size >= 0,
                 "coverage minimum must be a nonnegative integer (files >= 1)")
        required = descriptor.get("required_owner_names", [])
        _require(isinstance(required, list) and all(isinstance(name, str) and name for name in required),
                 "invalid required owner names")
        total = sum(actual[path]["size_bytes"] for path in paths)
        _require(len(paths) >= count and total >= size and set(required) <= names,
                 f"declared closure coverage is incomplete: {category}")
        result[category] = {"canonical_files": len(paths), "bytes": total, "owners": sorted(names)}
    return result


def _consumer_contract(value):
    _require(isinstance(value, Mapping) and set(value) == {
        "schema", "phase", "parent_input_graph", "dependency_selection",
        "full_original_input_semantics_replayed", "complete_global_closure_claimed"},
        "unexpected explicit consumer scope contract")
    _require(value["schema"] == CONSUMER_CONTRACT_SCHEMA
             and value["phase"] in CONSUMER_PHASES
             and value["dependency_selection"] == CONSUMER_SELECTION
             and value["full_original_input_semantics_replayed"] is False
             and value["complete_global_closure_claimed"] is False,
             "consumer graph must not claim complete global input admission or replay")
    parent = value["parent_input_graph"]
    _require(isinstance(parent, Mapping) and set(parent) == {"path", "sha256"},
             "consumer graph needs an explicit externally pinned parent graph")
    _path(parent["path"])
    _sha(parent["sha256"])
    return _json_clone(value)


def _consumer_coverage(requirements, actual, contract):
    """Describe the explicit subset, without credit for absent global classes."""
    _require(contract == {}, "consumer coverage cannot impersonate the complete global minimums")
    paths = {category: set() for category in CLOSURE_CATEGORIES}
    names = {category: set() for category in CLOSURE_CATEGORIES}
    for entry in requirements:
        paths[entry["category"]].add(entry["canonical_path"])
        names[entry["category"]].add(entry["owner"])
    _require(any(paths.values()), "consumer graph needs explicit regular-file inputs")
    return {category: {"canonical_files": len(paths[category]),
                       "bytes": sum(actual[path]["size_bytes"] for path in paths[category]),
                       "owners": sorted(names[category])}
            for category in CLOSURE_CATEGORIES}


def _consumer_lineage(graph, owners, namespaces, aliases, new_inputs, *, fresh_parent):
    """Verify only metadata lineage, never grant fresh whole-parent bytes.

    The actual declaration and current bounded parent must be authenticated by
    the caller.  This binds the subset's original literal expected SHA owners,
    exhaustive namespaces, aliases, negative inputs and explicitly new roles to
    that parent's exact JSON bytes.  It does not execute the original admission
    API or promote a saved scientific result.  Parent bytes outside this subset
    still require the caller's real global entry and final fresh verification.
    """
    contract = _consumer_contract(graph["consumer_scope"])
    item = contract["parent_input_graph"]
    _require(isinstance(fresh_parent, Mapping) and set(fresh_parent) == {"descriptor", "pin", "parsed"}
             and fresh_parent["descriptor"] == item,
             "consumer parent must come from this phase's exact union read")
    observed = fresh_parent["pin"]
    _require(isinstance(observed, Mapping) and set(observed) == {"path", "sha256", "size_bytes"}
             and observed["path"] == _resolve(item["path"], {}, kind="file")
             and observed["sha256"] == item["sha256"]
             and type(observed["size_bytes"]) is int and 0 <= observed["size_bytes"] <= MAX_JSON_BYTES,
             "fresh consumer parent bytes do not match their current typed pin")
    parent = fresh_parent["parsed"]
    _require(isinstance(parent, Mapping), "fresh parent JSON must be one complete object")
    _require(parent.get("fresh_reader_contract") == FRESH_READER_CONTRACT,
             "complete parent reader contract changed")
    _require(isinstance(parent, Mapping) and parent.get("schema") == SCHEMA
             and parent.get("scope") == INPUT_SCOPE and parent.get("consumer_scope") is None
             and parent.get("closure_categories") == list(CLOSURE_CATEGORIES)
             and parent.get("science_qualification_created") is False
             and parent.get("live_resources_verified") is False
             and parent.get("external_declaration_exit0_verified") is False,
             "consumer parent must be the immutable complete input-only graph")
    _require(_sha(parent.get("content_sha256")) == _content_digest(parent),
             "complete parent graph metadata content changed")
    _validate_requirement_table(parent["requirements"])
    parent_owners = _owners(_expand_owner_table(parent["owners"], parent["requirements"]))
    selected = set(graph["requirements"]["paths"])
    subset_owners = []
    for owner in parent_owners:
        files = {path: digest for path, digest in owner["expected_files"].items() if path in selected}
        extra = [path for path in owner.get("newly_declared_input_paths", []) if path in selected]
        if files or extra or owner["category"] == "code_environment":
            row = {"owner": owner["owner"], "category": owner["category"], "expected_files": files}
            if "newly_declared_input_paths" in owner:
                row["newly_declared_input_paths"] = extra
            subset_owners.append(row)
    parent_owner = {"owner": CONSUMER_PARENT_OWNER, "category": "code_environment",
                    "expected_files": {item["path"]: item["sha256"]}}
    _require(owners == subset_owners + [parent_owner],
             "consumer must retain all selected original expected-owner edges and one exact parent pin")
    selected_roots = {value["root"] for value in namespaces}
    _require(namespaces == [value for value in parent["namespaces"] if value["root"] in selected_roots],
             "consumer namespaces must retain every complete parent descriptor for each selected root")
    parent_aliases = _alias_map(parent["aliases"])
    for path, alias in aliases.items():
        _require(alias == parent_aliases.get(path), "consumer alias differs from its exact parent contract")
    _require(new_inputs == {path: value for path, value in parent["newly_declared_input_paths"].items()
                            if path in selected}, "consumer explicit new-input roles changed")
    _require(graph["newly_declared_input_pins"] == {
        path: value for path, value in parent["newly_declared_input_pins"].items() if path in selected},
        "consumer new-input byte binding differs from its parent declaration")
    _require(graph["absence_inputs"] == parent["absence_inputs"]
             and graph["absence_observations"] == parent["absence_observations"],
             "consumer explicit negative-input contract changed")
    _require(graph["live_io_requirements"] == parent["live_io_requirements"],
             "consumer live OS-probe input contract changed")
    _require(graph["declared_new_source_roots"] == parent["declared_new_source_roots"]
             and graph["live_resource_roots"] == parent["live_resource_roots"],
             "consumer source or live resource scope differs from its complete parent declaration")


def _trace_coverage(records, requirements, namespaces, aliases, source_roots, resource_roots,
                    subprocess_records, live_io, absent_inputs):
    owned = {entry["canonical_path"] for entry in requirements}
    namespace_roots = [entry["canonical_root"] for entry in namespaces]
    devices = {entry["path"]: entry for entry in live_io if entry["kind"] == "character_device"}
    commands = {_canonical_json(entry["command"]): entry for entry in live_io
                if entry["kind"] == "subprocess_stdio"}
    subprocess_by_id = {entry["command_id"]: entry for entry in subprocess_records}
    counts = {"owned_file_attempts": 0, "owned_namespace_directory_attempts": 0,
              "explicit_live_resource_directory_attempts": 0,
              "owned_regular_descriptor_attempts": 0,
              "explicit_subprocess_pipe_attempts": 0,
              "explicit_subprocess_null_device_attempts": 0,
              "explicit_declared_absent_file_attempts": 0,
              "actual_subprocess_audit_attempts": len(subprocess_records),
              "unique_records": len(records),
              "actual_read_open_attempts": sum(record["attempt_count"] for record in records)}
    for device in devices.values():
        _require(capture_live_character_device(device["path"], owner=device["owner"], reason=device["reason"])
                 == device, "live null device identity changed")
    for command in subprocess_records:
        _require(_canonical_json(command["command"]) in commands,
                 "actual subprocess command lacks an explicit live OS-probe allowance")
        actual_command = command["command"]
        selected, path_environment = _executable_binding(actual_command["literal_executable"],
                                                        actual_command["cwd"], actual_command["environment"])
        _require(selected == actual_command["executable"]
                 and path_environment == actual_command["path_environment"],
                 "actual PATH/literal executable candidate changed")
        for path in (command["subprocess_source_path"], command["command"]["executable"]):
            _require(_resolve(path, aliases, kind="file") in owned,
                     f"subprocess code/executable has no typed byte owner: {path}")

    def stdio(record, observation, *, device=False):
        identifier = record.get("subprocess_command_id")
        _require(type(identifier) is int and identifier in subprocess_by_id,
                 "live descriptor is not associated with a real stdlib Popen audit command")
        command = subprocess_by_id[identifier]
        _require(record.get("subprocess_source_path") == command["subprocess_source_path"]
                 and record.get("actual_stdlib_Popen_constructor_frame") is True,
                 "live descriptor lacks the same actual stdlib Popen constructor")
        roles = record.get("subprocess_stdio_roles")
        allowed = {"devnull"} if device else {"stdout_read", "stderr_read"}
        _require(isinstance(roles, list) and roles and set(roles) <= allowed,
                 "live read descriptor has no exact supported stdio role")
        for role in roles:
            target = command["stdio_descriptors"].get(role)
            _require(target is not None and target["identity"] == observation,
                     "Popen stdio descriptor identity differs from its actual open observation")
            if record["kind"] == "descriptor":
                _require(target["descriptor"] == record["descriptor"],
                         "actual Popen stdio descriptor number differs")
            if device:
                _require(any(entry["descriptor"] == target["descriptor"]
                             and entry["identity"] == target["identity"]
                             for name, entry in command["stdio_descriptors"].items()
                             if name in ("stdin_read", "stdout_write", "stderr_write")),
                         "observed null handle was not an actual child stdio handle")

    for record in records:
        attempts = record["attempt_count"]
        if record["kind"] == "descriptor":
            observed = record["descriptor_observation"]
            if observed["kind"] in ("fifo", "socket"):
                _require(record["access"] == "read", "live subprocess pipe open is not read-only")
                mode = observed["identity"]["mode"]
                _require((observed["kind"] == "fifo" and stat.S_ISFIFO(mode))
                         or (observed["kind"] == "socket" and stat.S_ISSOCK(mode)),
                         "descriptor type differs from actual fstat")
                stdio(record, observed["identity"])
                counts["explicit_subprocess_pipe_attempts"] += attempts
                continue
            if observed["kind"] == "character":
                path = observed.get("canonical_path")
                _require(observed.get("endpoint_identity_verified_at_attempt") is True
                         and path in devices and observed["identity"] == devices[path]["identity"],
                         "character descriptor is not the explicitly bound null device")
                stdio(record, observed["identity"], device=True)
                counts["explicit_subprocess_null_device_attempts"] += attempts
                continue
            _require(record["access"] == "read", "regular input descriptor attempted read/write")
            counts["owned_regular_descriptor_attempts"] += attempts
        path = record["path"]
        if path in absent_inputs:
            changing_flags = (getattr(os, "O_CREAT", 0) | getattr(os, "O_TRUNC", 0)
                              | getattr(os, "O_APPEND", 0) | getattr(os, "O_EXCL", 0))
            _require(record["kind"] == "path" and record["access"] == "read"
                     and not (record["flags"] & (getattr(os, "O_DIRECTORY", 0) | changing_flags)),
                     "declared absent input covers only the exact read-only file path attempt")
            counts["explicit_declared_absent_file_attempts"] += attempts
            continue
        if path in devices:
            _require(record.get("endpoint_at_attempt") == devices[path]["identity"],
                     "null path identity was not actually captured at the open attempt")
            stdio(record, devices[path]["identity"], device=True)
            counts["explicit_subprocess_null_device_attempts"] += attempts
            continue
        _require(record["access"] == "read", "input admission attempted a read/write open")
        try:
            canonical = _resolve(path, aliases)
            mode = os.lstat(canonical).st_mode
        except (InputGraphError, OSError):
            # Missing paths caught by a real live-resource scan have no saved
            # input semantic value.  Only explicitly scoped directory attempts
            # can use this branch; an unknown file read can never use it.
            is_directory_attempt = bool(record.get("flags", 0) & getattr(os, "O_DIRECTORY", 0))
            _require(is_directory_attempt and any(_under(path, root) for root in resource_roots),
                     f"unowned or unavailable read-open attempt: {path}")
            counts["explicit_live_resource_directory_attempts"] += attempts
            continue
        if stat.S_ISREG(mode):
            _require(canonical in owned, f"read-open file is missing a typed byte owner: {path}")
            counts["owned_file_attempts"] += attempts
        elif stat.S_ISDIR(mode):
            if any(_under(canonical, root) for root in namespace_roots):
                counts["owned_namespace_directory_attempts"] += attempts
            elif any(_under(path, root) for root in resource_roots):
                counts["explicit_live_resource_directory_attempts"] += attempts
            else:
                raise InputGraphError(f"directory read-open has no explicit namespace/resource scope: {path}")
        else:
            raise InputGraphError(f"unsupported read-open endpoint: {path}")
    for root in source_roots:
        # The source-root declaration is descriptive only.  It never exempts a
        # traced source file from its explicit owner/digest requirement.
        _path(root)
    for device in devices.values():
        _require(capture_live_character_device(device["path"], owner=device["owner"], reason=device["reason"])
                 == device, "live null device identity changed during trace coverage verification")
    for command in subprocess_records:
        value = command["command"]
        _require(_executable_binding(value["literal_executable"], value["cwd"], value["environment"])
                 == (value["executable"], value["path_environment"]),
                 "actual PATH/executable candidate changed during trace coverage verification")
    return counts


def create_graph(*, typed_snapshot, owners, namespaces=(), aliases=(), read_trace=(),
                 newly_declared_input_paths=None, declared_new_source_roots=(),
                 live_resource_roots=(), coverage_requirements=None, live_io_requirements=(),
                 absence_inputs=None, consumer_scope=None):
    """Create a JSON-only input graph after the real frozen input admission.

    Owner forms: {owner,category,kind:'pin',path,sha256}, or
    {owner,category,expected_files:{absolute_path:expected_sha256}}.  ``files``
    and ``outputs`` are accepted as explicitly typed map names.  Use
    explicit_sealed_namespace for exhaustive inventories.  New unpinned inputs
    must be an explicit path -> {owner,category,reason} map; their role is only
    NEWLY_DECLARED_INPUT_ONLY.  Unknown traced files always reject.

    All nine closure categories must be populated.  Complete transitive owner
    discovery and actual external declaration exit0 remain caller obligations.
    This function writes no files and produces no terminal receipt.

    Live subprocess stdio needs caller-supplied live_io_requirements: an exact
    {kind:'subprocess_stdio',owner,reason,command:{literal_executable,executable,
    argv,cwd,environment,path_environment},
    scope:LIVE_IO_SCOPE} and, if used, capture_live_character_device(os.devnull).
    Source/executable regular bytes still require typed owners.  Anonymous I/O
    is never input bytes; saved commands/results are not replayed or qualified.

    ``absence_inputs`` is an explicit path -> {owner,category,reason} map, for
    known optional input candidates derived by the caller from true interpreter
    paths/pinned source modules.  Trace discovery never creates such a contract.
    Only genuine ENOENT, with all existing parents and aliases validated before
    and after the full byte read, can cover that exact read-only path attempt.
    Negative inputs never count as regular bytes or as any closure class.
    """
    normalized_owners = _owners(owners)
    normalized_namespaces = [_namespace_descriptor(value) for value in namespaces]
    alias_values = list(aliases)
    for namespace in normalized_namespaces:
        for name, value in namespace["symlinks"].items():
            alias_values.append(dict(value, path=os.path.join(namespace["root"], name)))
    normalized_aliases = _alias_map(alias_values)
    normalized_new = _new_inputs(newly_declared_input_paths or {})
    source_roots = sorted({_path(path) for path in declared_new_source_roots})
    resource_roots = sorted({_path(path) for path in live_resource_roots})
    traces = _trace_records(read_trace)
    subprocess_records = _subprocess_records(read_trace)
    live_io = _live_io(live_io_requirements)
    absent_inputs = _absence_inputs(absence_inputs or {})
    contract = _json_clone(coverage_requirements or {})
    consumer = None if consumer_scope is None else _consumer_contract(consumer_scope)
    if consumer is not None:
        _require(not traces and not subprocess_records,
                 "consumer declaration must not relabel/filter the original full-ready audit as its execution trace")
    absence_observations = _absence_phase(absent_inputs, normalized_aliases)
    requirements, actual, new_pins, fresh_parent = _phase(normalized_owners, normalized_namespaces,
                                           normalized_aliases, normalized_new,
                                           json_input=None if consumer is None else consumer["parent_input_graph"])
    _absence_phase(absent_inputs, normalized_aliases, expected=absence_observations)
    coverage = (_coverage if consumer is None else _consumer_coverage)(requirements, actual, contract)
    trace_coverage = _trace_coverage(traces, requirements, normalized_namespaces,
                                     normalized_aliases, source_roots, resource_roots,
                                     subprocess_records, live_io, absent_inputs)
    _require(consumer is not None or trace_coverage["owned_file_attempts"] > 0,
             "a real input-admission read trace must contain an owned regular-file attempt")
    # Freeze the digest of every explicitly owned file alias, including aliases
    # whose input declaration supplied only literal text and canonical target.
    for alias in normalized_aliases.values():
        if alias["kind"] == "file":
            alias["sha256"] = actual[alias["target"]]["sha256"]
    requirement_table = _requirement_table(requirements)
    graph = {
        "schema": SCHEMA if consumer is None else CONSUMER_SCHEMA, "scope": INPUT_SCOPE,
        "consumer_scope": consumer,
        "fresh_reader_contract": copy.deepcopy(FRESH_READER_CONTRACT),
        "typed_snapshot": _json_clone(typed_snapshot),
        "owners": _owner_table(normalized_owners, requirement_table), "namespaces": normalized_namespaces,
        "aliases": [normalized_aliases[path] for path in sorted(normalized_aliases)],
        "newly_declared_input_paths": normalized_new, "newly_declared_input_pins": new_pins,
        "declared_new_source_roots": source_roots, "live_resource_roots": resource_roots,
        "read_trace": {"schema": TRACE_SCHEMA,
                       "coverage": "PYTHON_AUDIT_OPEN_ATTEMPTS_ONLY" if consumer is None else "NO_CONSUMER_EXECUTION_TRACE_CLAIMED",
                       "records": traces, "subprocess_records": subprocess_records},
        "live_io_requirements": live_io,
        "live_io_scope": LIVE_IO_SCOPE,
        "live_subprocess_results_are_not_saved_input_bytes_or_science": True,
        "absence_inputs": absent_inputs, "absence_observations": absence_observations,
        "absence_inputs_are_not_regular_bytes_or_science": True,
        "coverage_requirements": contract, "closure_categories": list(CLOSURE_CATEGORIES),
        "requirements": requirement_table,
        "canonical_files": [actual[path] for path in sorted(actual)],
        "coverage": coverage, "trace_coverage": trace_coverage,
        "science_qualification_created": False,
        "live_resources_verified": False, "external_declaration_exit0_verified": False,
        "caller_must_verify_live_environment_modules_PID_time_and_resources": True,
    }
    if consumer is not None:
        _consumer_lineage(graph, normalized_owners, normalized_namespaces, normalized_aliases, normalized_new,
                          fresh_parent=fresh_parent)
    graph["content_sha256"] = _content_digest(graph)
    return graph


def verify_graph(graph, *, expected_sha256=None, graph_aliases=(), phase="input_verification"):
    """Freshly verify every byte, full namespace, and alias in one new phase.

    If graph is a path, expected_sha256 is mandatory and pins its exact stored
    JSON bytes.  A mapping must already be externally bound by the caller's
    immutable declaration; its internal content digest is not external proof.
    The returned snapshot may be reused only as input semantics, alongside real
    current environment/module/PID/time/resource checks performed by the caller.
    """
    _label(phase, "verification phase")
    if isinstance(graph, (str, os.PathLike)):
        _require(expected_sha256 is not None, "a stored graph needs an external expected SHA256")
        graph = strict_json(graph, _sha(expected_sha256), aliases=graph_aliases)
    else:
        _require(expected_sha256 is None, "stored-byte SHA applies only to a graph path")
        graph = _json_clone(graph)
    _require(isinstance(graph, Mapping) and graph.get("schema") in (SCHEMA, CONSUMER_SCHEMA) and graph.get("scope") == INPUT_SCOPE,
             "unknown or non-input graph schema")
    consumer = None
    if graph["schema"] == CONSUMER_SCHEMA:
        consumer = _consumer_contract(graph["consumer_scope"])
        _require(phase == consumer["phase"], "consumer input graph belongs to a different phase")
        _require(isinstance(graph["read_trace"], Mapping)
                 and set(graph["read_trace"]) == {"schema", "coverage", "records", "subprocess_records"}
                 and graph["read_trace"]["schema"] == TRACE_SCHEMA
                 and graph["read_trace"]["coverage"] == "NO_CONSUMER_EXECUTION_TRACE_CLAIMED"
                 and type(graph["read_trace"]["records"]) is list and graph["read_trace"]["records"] == []
                 and type(graph["read_trace"]["subprocess_records"]) is list and graph["read_trace"]["subprocess_records"] == [],
                 "consumer graph cannot claim a saved execution/science trace")
    else:
        _require(graph.get("consumer_scope") is None
                 and graph["read_trace"]["coverage"] == "PYTHON_AUDIT_OPEN_ATTEMPTS_ONLY",
                 "complete global graph cannot change to a consumer-only scope")
    _require(graph.get("closure_categories") == list(CLOSURE_CATEGORIES), "closure class contract changed")
    _require(graph.get("science_qualification_created") is False
             and graph.get("live_resources_verified") is False
             and graph.get("external_declaration_exit0_verified") is False
             and graph.get("caller_must_verify_live_environment_modules_PID_time_and_resources") is True,
             "input graph falsely claims a live/scientific/terminal decision")
    _require(graph.get("live_io_scope") == LIVE_IO_SCOPE
             and graph.get("live_subprocess_results_are_not_saved_input_bytes_or_science") is True,
             "live I/O cannot grant saved input/science semantics")
    _require(graph.get("absence_inputs_are_not_regular_bytes_or_science") is True,
             "negative input must not grant byte/science semantics")
    _require(_sha(graph.get("content_sha256")) == _content_digest(graph), "input graph content changed")
    _validate_requirement_table(graph["requirements"])
    owners = _owners(_expand_owner_table(graph["owners"], graph["requirements"]))
    namespaces = [_namespace_descriptor(value) for value in graph["namespaces"]]
    aliases = _alias_map(graph["aliases"])
    new_values = {}
    for path, value in graph["newly_declared_input_paths"].items():
        _require(value.get("binding_role") == NEW_INPUT_ROLE, "new input role changed")
        new_values[path] = {key: val for key, val in value.items() if key != "binding_role"}
    new_inputs = _new_inputs(new_values)
    _require(graph.get("fresh_reader_contract") == FRESH_READER_CONTRACT,
             "fresh byte-reader/parser contract changed")
    _require(set(graph["newly_declared_input_pins"]) == set(new_inputs), "new input pin set changed")
    frozen_new = {path: _sha(digest) for path, digest in graph["newly_declared_input_pins"].items()}
    absence_values = {}
    for path, value in graph["absence_inputs"].items():
        _require(isinstance(value, Mapping) and value.get("binding_role") == ABSENCE_INPUT_ROLE,
                 "declared absent input role changed")
        absence_values[path] = {key: val for key, val in value.items() if key != "binding_role"}
    absent_inputs = _absence_inputs(absence_values)
    _absence_phase(absent_inputs, aliases, expected=graph["absence_observations"])
    requirements, actual, new_pins, fresh_parent = _phase(owners, namespaces, aliases, new_inputs,
                                           frozen_new_pins=frozen_new,
                                           json_input=None if consumer is None else consumer["parent_input_graph"])
    if consumer is not None:
        _consumer_lineage(graph, owners, namespaces, aliases, new_inputs, fresh_parent=fresh_parent)
    _absence_phase(absent_inputs, aliases, expected=graph["absence_observations"])
    _require(_requirement_table(requirements) == graph["requirements"],
             "complete typed owner/canonical path requirement table changed")
    _require([actual[path] for path in sorted(actual)] == graph["canonical_files"], "canonical input bytes/lengths changed")
    _require(new_pins == frozen_new, "newly declared input bytes changed")
    coverage = (_coverage if consumer is None else _consumer_coverage)(requirements, actual, graph["coverage_requirements"])
    _require(coverage == graph["coverage"], "closure coverage changed")
    trace_coverage = _trace_coverage(_trace_records(graph["read_trace"]["records"] if consumer is not None else graph["read_trace"]), requirements, namespaces, aliases,
                                    graph["declared_new_source_roots"], graph["live_resource_roots"],
                                    _subprocess_records(graph["read_trace"]),
                                    _live_io(graph["live_io_requirements"]), absent_inputs)
    _require(trace_coverage == graph["trace_coverage"], "read trace ownership changed")
    return {"schema": VERIFICATION_SCHEMA,
            "classification": "FRESH_INPUT_BYTES_NAMESPACES_ALIASES_VERIFIED_ONLY" if consumer is None else "FRESH_EXPLICIT_CONSUMER_INPUT_BYTES_NAMESPACES_ALIASES_VERIFIED_ONLY",
            "consumer_scope": copy.deepcopy(consumer),
            "consumer_selected_literal_and_canonical_paths": list(graph["requirements"]["paths"]) if consumer is not None else None,
            "consumer_complete_namespace_root_sequence": [value["root"] for value in namespaces] if consumer is not None else None,
            "scope": INPUT_SCOPE, "phase": phase, "graph_content_sha256": graph["content_sha256"],
            "fresh_reader_contract": copy.deepcopy(FRESH_READER_CONTRACT),
            "canonical_files_read": len(actual), "actual_bytes_read": sum(value["size_bytes"] for value in actual.values()),
            "byte_count_scope": "CANONICAL_INPUT_UNION_ONLY_EXCLUDES_STORED_GRAPH_JSON",
            "logical_owner_requirements": len(requirements), "exhaustive_namespaces_checked": len(namespaces),
            "explicit_aliases_checked": len(aliases), "coverage": coverage, "trace_coverage": trace_coverage,
            "live_io_scope": LIVE_IO_SCOPE, "live_subprocesses_reexecuted": False,
            "declared_absence_inputs_checked_before_and_after_bytes": len(absent_inputs),
            "absence_inputs_are_not_regular_bytes_or_science": True,
            "caller_must_recheck_current_OS_identity_and_live_probe_results": True,
            "typed_snapshot": copy.deepcopy(graph["typed_snapshot"]),
            "science_qualification_created": False, "live_resources_verified": False,
            "external_declaration_exit0_verified": False,
            "caller_must_verify_live_environment_modules_PID_time_and_resources": True}


_ACTIVE_TRACES = []
_AUDIT_HOOK_INSTALLED = False


def _popen_context(*, execution=False):
    """Observe actual stdlib frames/objects; never wrap or replace Popen."""
    module = sys.modules.get("subprocess")
    cls = getattr(module, "Popen", None)
    if cls is None:
        return None
    init_code = getattr(getattr(cls, "__init__", None), "__code__", None)
    execute_code = getattr(getattr(cls, "_execute_child", None), "__code__", None)
    frame, constructor, executor = sys._getframe(1), None, None
    try:
        for _ in range(64):
            if frame is None:
                break
            if frame.f_globals is module.__dict__:
                instance = frame.f_locals.get("self")
                if type(instance) is cls and frame.f_code is init_code:
                    constructor = instance
                if type(instance) is cls and frame.f_code is execute_code:
                    executor = (instance, dict(frame.f_locals))
            frame = frame.f_back
        if constructor is None or (execution and (executor is None or executor[0] is not constructor)):
            return None
        source = _path(os.path.abspath(module.__file__))
        _require(init_code.co_filename == module.__file__, "Popen constructor code/source identity differs")
        if execution:
            _require(execute_code.co_filename == module.__file__, "Popen executor code/source identity differs")
        return {"object": constructor, "source": source,
                "executor_locals": executor[1] if execution else None}
    finally:
        del frame


def _descriptor_endpoint(fd):
    if sys.platform == "darwin":
        import fcntl
        request = getattr(fcntl, "F_GETPATH", None)
        if request is None:
            raise OSError("this Python does not expose F_GETPATH")
        raw = fcntl.fcntl(fd, request, b"\x00" * 1024).split(b"\x00", 1)[0]
        return _path(os.fsdecode(raw))
    if sys.platform.startswith("linux"):
        return _path(os.readlink(f"/proc/self/fd/{fd}"))
    raise OSError("no supported actual regular-descriptor endpoint observer")


def _observe_descriptor(fd):
    try:
        info = os.fstat(fd)
        if stat.S_ISREG(info.st_mode):
            kind = "regular"
        elif stat.S_ISFIFO(info.st_mode):
            kind = "fifo"
        elif stat.S_ISSOCK(info.st_mode):
            kind = "socket"
        elif stat.S_ISCHR(info.st_mode):
            kind = "character"
        else:
            kind = "unsupported"
        result = {"status": "FSTAT_OBSERVED", "kind": kind, "identity": _fd_identity(info)}
        if kind in ("regular", "character"):
            try:
                path = _descriptor_endpoint(fd)
                endpoint = os.lstat(path)
                result["canonical_path"] = path
                result["endpoint_identity_verified_at_attempt"] = (
                    os.path.realpath(path) == path and not stat.S_ISLNK(endpoint.st_mode)
                    and _fd_identity(endpoint) == result["identity"]
                    and _fd_identity(os.fstat(fd)) == result["identity"])
            except (OSError, ValueError) as exc:
                result["endpoint_identity_verified_at_attempt"] = False
                result["endpoint_error"] = type(exc).__name__
        return result
    except OSError as exc:
        return {"status": "FSTAT_UNAVAILABLE", "error": type(exc).__name__, "errno": exc.errno}


def _actual_subprocess_record(arguments, context, identifier):
    executable, argv, cwd, env = arguments
    values = context["executor_locals"]
    command = {"literal_executable": os.fsdecode(executable),
               "argv": [os.fsdecode(arg) for arg in argv],
               "cwd": os.path.normpath(os.fsdecode(cwd)) if cwd is not None else os.getcwd(),
               "environment": None if env is None else {os.fsdecode(key): os.fsdecode(item)
                                                        for key, item in env.items()}}
    if not os.path.isabs(command["cwd"]):
        command["cwd"] = os.path.normpath(os.path.join(os.getcwd(), command["cwd"]))
    selected, path_environment = _executable_binding(command["literal_executable"], command["cwd"],
                                                    command["environment"])
    command["executable"], command["path_environment"] = selected, path_environment
    descriptors = {}
    for local, role in (("p2cread", "stdin_read"), ("p2cwrite", "stdin_write"),
                        ("c2pread", "stdout_read"), ("c2pwrite", "stdout_write"),
                        ("errread", "stderr_read"), ("errwrite", "stderr_write")):
        fd = values.get(local)
        if type(fd) is int and fd >= 0:
            observed = _observe_descriptor(fd)
            if observed.get("status") == "FSTAT_OBSERVED":
                descriptors[role] = {"descriptor": fd, "identity": observed["identity"]}
    fd = getattr(context["object"], "_devnull", None)
    if type(fd) is int and fd >= 0:
        observed = _observe_descriptor(fd)
        if observed.get("status") == "FSTAT_OBSERVED":
            descriptors["devnull"] = {"descriptor": fd, "identity": observed["identity"]}
    return {"event": "subprocess.Popen", "observation": "EXECUTE_CHILD_AUDIT_ATTEMPT",
            "command_id": identifier, "command": command,
            "audit_cwd_argument": None if cwd is None else os.fsdecode(cwd),
            "subprocess_source_path": context["source"], "stdio_descriptors": descriptors,
            "actual_stdlib_Popen_object_and_frame": True,
            "PATH_candidate_resolution_is_not_child_start_proof": True,
            "child_start_success_or_return_is_not_observed": True}


def _open_audit(event, arguments):
    if event not in ("open", "subprocess.Popen") or not _ACTIVE_TRACES:
        return
    if event == "subprocess.Popen":
        for trace in tuple(_ACTIVE_TRACES):
            if trace._recording:
                continue
            trace._recording = True
            try:
                context = _popen_context(execution=True)
                identifier = len(trace._subprocess_records) + 1
                if context is None:
                    value = {"event": event, "command_id": identifier,
                             "observation": "EXECUTE_CHILD_AUDIT_ATTEMPT",
                             "actual_stdlib_Popen_object_and_frame": False}
                else:
                    trace._popen_objects[id(context["object"])] = context["object"]
                    value = _actual_subprocess_record(arguments, context, identifier)
                    trace._popen_commands.setdefault(id(context["object"]), []).append(identifier)
                trace._subprocess_records.append(value)
            except Exception as exc:
                # Observation must not change the frozen callable's execution.
                # Preserve an explicit invalid audit record; graph creation then
                # rejects it, rather than omitting the event or granting input.
                trace._subprocess_records.append({"event": event,
                    "command_id": len(trace._subprocess_records) + 1,
                    "observation": "EXECUTE_CHILD_AUDIT_ATTEMPT",
                    "actual_stdlib_Popen_object_and_frame": False,
                    "observer_error": type(exc).__name__, "observer_error_message": str(exc)})
            finally:
                trace._recording = False
        return
    path, mode, flags = arguments
    # Write-only opens are not read attempts.  Read/write opens remain visible
    # and are rejected by an input graph rather than silently called read-only.
    access_bits = flags & os.O_ACCMODE if isinstance(flags, int) else None
    if access_bits == os.O_WRONLY:
        return
    access = "readwrite" if access_bits == os.O_RDWR else "read"
    for trace in tuple(_ACTIVE_TRACES):
        if trace._recording:
            continue
        trace._recording = True
        try:
            cwd = os.getcwd()
            if isinstance(path, (str, bytes, os.PathLike)):
                raw = os.fsdecode(os.fspath(path))
                absolute = os.path.normpath(raw if os.path.isabs(raw) else os.path.join(cwd, raw))
                value = {"event": "open", "kind": "path", "path": absolute,
                         "literal_path": raw, "cwd": cwd, "mode": mode, "flags": flags,
                         "access": access, "observation": "OPEN_ATTEMPT"}
                if absolute == os.devnull:
                    try:
                        value["endpoint_at_attempt"] = _fd_identity(os.lstat(absolute))
                    except OSError as exc:
                        value["endpoint_error"] = type(exc).__name__
            elif type(path) is int and path >= 0:
                value = {"event": "open", "kind": "descriptor", "descriptor": path,
                         "literal_descriptor": path, "cwd": cwd, "mode": mode, "flags": flags,
                         "access": access, "observation": "OPEN_ATTEMPT",
                         "descriptor_observation": _observe_descriptor(path)}
            else:
                value = {"event": "open", "kind": "unresolved_descriptor", "descriptor": path,
                         "cwd": cwd, "mode": mode, "flags": flags, "access": access,
                         "observation": "OPEN_ATTEMPT"}
            if value["kind"] == "descriptor" or value.get("path") == os.devnull:
                context = _popen_context()
                if context is not None:
                    trace._popen_objects[id(context["object"])] = context["object"]
                    value["_popen_identity"] = id(context["object"])
                    value["subprocess_source_path"] = context["source"]
                    value["actual_stdlib_Popen_constructor_frame"] = True
            key = _canonical_json(value)
            if key in trace._records:
                trace._records[key]["attempt_count"] += 1
            else:
                value["attempt_count"] = 1
                trace._records[key] = value
        except Exception as exc:
            value = {"event": "open", "kind": "unresolved_descriptor",
                     "descriptor": path if type(path) is int else None,
                     "literal_path": os.fsdecode(path) if isinstance(path, (str, bytes)) else None,
                     "cwd": os.getcwd(), "mode": mode, "flags": flags, "access": access,
                     "observation": "OPEN_ATTEMPT", "attempt_count": 1,
                     "observer_error": type(exc).__name__, "observer_error_message": str(exc)}
            key = _canonical_json(value)
            if key in trace._records:
                trace._records[key]["attempt_count"] += 1
            else:
                trace._records[key] = value
        finally:
            trace._recording = False


class ReadOpenAudit:
    """Record Python audit ``open`` attempts without replacing any callable.

    Hooks cannot be uninstalled; a single inert hook is installed on first use,
    and this context only activates recording.  This is not a native libc/HDF5,
    dynamic-loader, directory-stat, or successful-open tracer.  All such inputs
    need explicit typed owners/namespace and alias contracts from the caller.
    Identical complete records are stored once with their actual positive
    attempt_count.  Literal path/descriptor, cwd and access flags/mode remain.
    Descriptor fstat is taken at the actual open audit event.  Regular endpoints
    require actual endpoint identity; pipes/sockets require the same real stdlib
    Popen constructor/executor object, actual stdio FD identities and its audit
    command, plus a caller-declared exact OS-probe allowance.  Unknown/closed
    descriptors fail.  Deduplication never exempts a path from coverage.
    No trace creates an owner or a digest automatically.
    """

    def __init__(self):
        self._records = {}
        self._subprocess_records = []
        self._popen_objects = {}
        self._popen_commands = {}
        self._recording = False
        self._active = False

    def __enter__(self):
        global _AUDIT_HOOK_INSTALLED
        _require(not self._active, "read-open audit context already active")
        if not _AUDIT_HOOK_INSTALLED:
            sys.addaudithook(_open_audit)
            _AUDIT_HOOK_INSTALLED = True
        self._active = True
        _ACTIVE_TRACES.append(self)
        return self

    def __exit__(self, exc_type, exc, traceback):
        _ACTIVE_TRACES.remove(self)
        self._active = False
        return False

    def snapshot(self):
        _require(not self._active, "end the read-open audit phase before freezing its trace")
        records = []
        for value in self._records.values():
            record = dict(value)
            instance = record.pop("_popen_identity", None)
            if instance is not None:
                ids = self._popen_commands.get(instance, [])
                if len(ids) == 1:
                    command = self._subprocess_records[ids[0] - 1]
                    observation = record.get("descriptor_observation", {}).get("identity")
                    if record["kind"] == "path":
                        observation = record.get("endpoint_at_attempt")
                    roles = []
                    for role, descriptor in command["stdio_descriptors"].items():
                        if descriptor["identity"] == observation and (
                                record["kind"] == "path" or descriptor["descriptor"] == record["descriptor"]):
                            if record["kind"] == "path" or record.get("descriptor_observation", {}).get("kind") == "character":
                                if role == "devnull":
                                    roles.append(role)
                            elif role in ("stdout_read", "stderr_read"):
                                roles.append(role)
                    if roles:
                        record["subprocess_command_id"] = ids[0]
                        record["subprocess_stdio_roles"] = roles
            records.append(record)
        return {"schema": TRACE_SCHEMA, "coverage": "PYTHON_AUDIT_OPEN_ATTEMPTS_ONLY",
                "records": _json_clone(records),
                "subprocess_records": _json_clone(self._subprocess_records),
                "unique_records": len(self._records),
                "actual_read_open_attempts": sum(value["attempt_count"] for value in self._records.values()),
                "record_storage": "EXACT_RECORD_DEDUPLICATION_WITH_ACTUAL_ATTEMPT_COUNTS",
                "success_of_open_attempt_is_not_observed": True,
                "native_libc_HDF5_loader_and_directory_stat_are_not_traced": True}
