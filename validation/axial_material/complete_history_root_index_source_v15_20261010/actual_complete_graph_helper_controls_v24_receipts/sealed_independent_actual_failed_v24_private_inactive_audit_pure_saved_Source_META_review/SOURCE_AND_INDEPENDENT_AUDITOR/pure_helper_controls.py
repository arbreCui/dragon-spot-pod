"""UNREADY source only: one Root-owned bounded, metadata-only helper control.

Authoring this file did not import any helper or open either numeric payload.
Only the installed normal canonical helper may be imported by a future run.
This driver never calls a component API, verify_graph, scientific computation,
resource discovery, subprocess, or an executor. Root supplies the sole bounded
execution. A PASS is pure-helper control evidence, never fresh runtime INPUT,
native RSS, AAA, ABA, or scientific admission.
"""

from __future__ import annotations

import argparse
import copy
import gc
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import resource
import signal
import stat
import struct
import sys
import time


SOURCE_STATUS = 'READY_SOURCE_BOUND_BY_ROOT'
ACTUAL_SUCCESS_PINS = None

AUDIT_CONTROL_PATH = '/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_complete_graph_helper_controls_v24_sources/inactive_audit_snapshot_controls_SOURCE_ONLY.py'
AUDIT_CONTROL_SHA256 = 'd439eb9641f45e09c17814a38a16dc7e2cbb6120fc09119df901e415daf28483'
AUDIT_CONTROL_SOURCE_BYTES = 23962
HELPER_PATH = '/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_private_inactive_audit_snapshot_consume_20261010.py'
HELPER_SHA256 = '3b181f6366d5084fd6ccc87c1a6e7b757b706b7ba38cdf9156e1381cdb010092'
HELPER_SOURCE_BYTES = 150986
PARENT_HELPER_SHA256 = "e8f142bef9dede08e9e43eba995203dea17e0e48b6f383502ed18b89808a5c28"
MAX_JSON_BYTES = 67108864
MAX_OUTPUT_BYTES = 67108864
RSS_BYTES = 536870912
WALL_SECONDS = 60
CHILD_LIMIT = 1
RETRIES = 0
GRAPH_PIN = {
    "path": "/Users/wen/spot/validation/artifacts/axial-material-owned-specs-identity-key-delta-graph-table-combined-runtime-v12-20261009/input_graph.json",
    "sha256": "4ba5f793ca13018d2d9ac5d29d76827a1503b0368c7e5c9f70ba08e0435f0c9e",
    "identity": [16777229, 49300178, 33188, 1, 66558943, 1791548788922741249, 1791548788922741249],
}
TRACE_PIN = {
    "path": "/Users/wen/spot/validation/artifacts/axial-material-sender-window-root-index-graph-table-combined-runtime-v15-20261010/input_creation_python_open_trace.json",
    "sha256": "e0a9fc9254bf0b5717498b489d5e1f2e4dbe09ac5fc80983c27af4fefbc92fa0",
    "identity": [16777229, 49362270, 33188, 1, 40915887, 1791576673435570628, 1791576673435570628],
}
TRACE_ORIGINAL_ORDER_COMPACT_PIN = {
    "size_bytes": 35211756,
    "sha256": "3edb2c73250782d107202deaab6192beec269619fe76a39a6e3b645f79e6b422",
    "records": 63379,
    "subprocess_records": 0,
}
JSON_ENCODER = json.JSONEncoder(sort_keys=True, separators=(",", ":"),
                                ensure_ascii=True, allow_nan=False)
ORDER_PRESERVING_JSON_ENCODER = json.JSONEncoder(sort_keys=False, separators=(",", ":"),
                                                 ensure_ascii=True, allow_nan=False)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def identity(path):
    info = os.lstat(path)
    require(stat.S_ISREG(info.st_mode) and info.st_nlink == 1,
            "only a normal single-link regular metadata file is permitted")
    return [info.st_dev, info.st_ino, info.st_mode, info.st_nlink, info.st_size,
            info.st_mtime_ns, info.st_ctime_ns]


def file_sha(path):
    digest = hashlib.sha256()
    with open(path, "rb") as stream:
        for block in iter(lambda: stream.read(1048576), b""):
            digest.update(block)
    return digest.hexdigest()


def pinned_identity(pin):
    require(identity(pin["path"]) == pin["identity"],
            "saved metadata identity changed: " + pin["path"])


def complete_pin(pin):
    pinned_identity(pin)
    require(file_sha(pin["path"]) == pin["sha256"],
            "saved metadata bytes changed: " + pin["path"])
    pinned_identity(pin)
    return dict(pin)


def exact_value(left, right, where="root"):
    """Full comparison: builtin types, dict key order, list order, float bits."""
    require(type(left) is type(right), "JSON type differs at " + where)
    kind = type(left)
    if kind is dict:
        require(len(left) == len(right), "object field count differs at " + where)
        for (lk, lv), (rk, rv) in zip(left.items(), right.items()):
            require(type(lk) is str and lk == rk, "object field order differs at " + where)
            exact_value(lv, rv, where + "/" + lk)
    elif kind is list:
        require(len(left) == len(right), "array length differs at " + where)
        for index, (lv, rv) in enumerate(zip(left, right)):
            exact_value(lv, rv, where + "/" + str(index))
    elif kind is float:
        require(struct.pack(">d", left) == struct.pack(">d", right),
                "float bit pattern differs at " + where)
    else:
        require(kind in (str, int, bool, type(None)) and left == right,
                "JSON scalar differs at " + where)


def compact_pin(value, encoder=JSON_ENCODER):
    size = 0
    digest = hashlib.sha256()
    for piece in encoder.iterencode(value):
        chunk = piece.encode("ascii")
        size += len(chunk)
        digest.update(chunk)
    return {"size_bytes": size, "sha256": digest.hexdigest()}


def order_type_pin(value):
    """A complete order/type/value/float-bit fingerprint with no JSON copy."""
    digest = hashlib.sha256()
    counts = {"dict": 0, "list": 0, "str": 0, "int": 0, "bool": 0, "null": 0, "float": 0}

    def visit(item):
        kind = type(item)
        if kind is dict:
            counts["dict"] += 1
            digest.update(b"D" + str(len(item)).encode("ascii") + b":")
            for key, part in item.items():
                visit(key)
                visit(part)
        elif kind is list:
            counts["list"] += 1
            digest.update(b"L" + str(len(item)).encode("ascii") + b":")
            for part in item:
                visit(part)
        elif kind is str:
            counts["str"] += 1
            data = item.encode("utf-8", "surrogatepass")
            digest.update(b"S" + str(len(data)).encode("ascii") + b":" + data)
        elif kind is int:
            counts["int"] += 1
            data = str(item).encode("ascii")
            digest.update(b"I" + str(len(data)).encode("ascii") + b":" + data)
        elif kind is float:
            counts["float"] += 1
            digest.update(b"F" + struct.pack(">d", item))
        elif kind is bool:
            counts["bool"] += 1
            digest.update(b"T" if item else b"B")
        else:
            require(item is None, "not builtin JSON in full value fingerprint")
            counts["null"] += 1
            digest.update(b"N")

    visit(value)
    return {"sha256": digest.hexdigest(), "complete_builtin_type_counts": counts}


def mutable_ids(value):
    result = set()

    def visit(part):
        if type(part) in (dict, list):
            if id(part) in result:
                return
            result.add(id(part))
            for child in (part.values() if type(part) is dict else part):
                visit(child)

    visit(value)
    return result


class Artifacts:
    def __init__(self, path):
        self.root = Path(path)
        require(self.root.is_absolute() and os.path.normpath(str(self.root)) == str(self.root),
                "output directory must be absolute and normalized")
        require(not self.root.exists(), "output directory must be fresh; no retry or reuse")
        self.root.mkdir(mode=0o700)
        self.sizes = {}

    def remaining(self):
        return MAX_OUTPUT_BYTES - sum(self.sizes.values())

    def write_json(self, name, value, expected=None, encoder=JSON_ENCODER):
        target = self.root / name
        require(name not in self.sizes and target.parent == self.root,
                "artifact name must be new and immediate")
        size = 0
        digest = hashlib.sha256()
        remaining = self.remaining()
        with open(target, "xb") as stream:
            for piece in encoder.iterencode(value):
                chunk = piece.encode("ascii")
                size += len(chunk)
                require(size <= remaining and size <= MAX_JSON_BYTES,
                        "fixed output budget exceeded")
                stream.write(chunk)
                digest.update(chunk)
        pin = {"path": str(target), "size_bytes": size, "sha256": digest.hexdigest(),
               "identity": identity(target)}
        if expected is not None:
            require(size == expected["size_bytes"] and pin["sha256"] == expected["sha256"],
                    "streamed encoded artifact differs from complete stored-size pass")
        self.sizes[name] = size
        return pin

    def write_bytes(self, name, payload):
        require(type(payload) is bytes and len(payload) <= self.remaining(), "fixture budget exceeded")
        target = self.root / name
        require(name not in self.sizes and target.parent == self.root, "fixture must be new and immediate")
        with open(target, "xb") as stream:
            stream.write(payload)
        self.sizes[name] = len(payload)
        return str(target)

    def drop(self, name):
        require(name in self.sizes, "only an owned artifact can be removed")
        (self.root / name).unlink()
        del self.sizes[name]


def rejection(g, name, callback, records, expected_message=None, expected_type=None):
    try:
        callback()
    except Exception as error:
        kind = type(error)
        require(kind is (expected_type or g.InputGraphError),
                "unexpected rejection class for " + name + ": " + kind.__name__)
        if expected_message is not None:
            require(str(error) == expected_message,
                    "unexpected rejection message for " + name + ": " + str(error))
        result = {"case": name, "class": kind.__name__, "message": str(error)}
        records.append(result)
        return result
    raise AssertionError("malformed control accepted: " + name)


def paired_rejection(g, name, kwargs, records):
    left = rejection(g, name + ":original", lambda: g.create_wire_graph(**kwargs), records)
    right = rejection(g, name + ":fresh", lambda: g.create_fresh_complete_wire_graph(**kwargs), records)
    require((left["class"], left["message"]) == (right["class"], right["message"]),
            "producer rejection class/order/message changed: " + name)


def caller_integrity_snapshot(value):
    """Strict caller identity/type/order/value/floatbits, including str attrs.

    This caller-only witness does not relax exact_value for output JSON. The
    base str encoder below observes the underlying text without __str__.
    """
    def visit(part):
        kind = type(part)
        typename = kind.__module__ + "." + kind.__qualname__
        if kind is dict:
            return ["dict", id(part), [[visit(key), visit(child)] for key, child in part.items()]]
        if kind is list:
            return ["list", id(part), [visit(child) for child in part]]
        if isinstance(part, str):
            text_hex = str.encode(part, "utf-8", "surrogatepass").hex()
            attributes = getattr(part, "__dict__", None) if kind is not str else None
            return ["str", typename, id(part), text_hex,
                    visit(attributes) if attributes is not None else None]
        if kind is float:
            return ["float", struct.pack(">d", part).hex()]
        require(kind in (int, bool, type(None)), "unexpected accepted caller fixture type")
        return [typename, part]

    return visit(value)


def accepted_str_subclass_controls(g, kwargs, artifacts):
    """Two original-accepted string subtype groups; strict complete outputs."""
    class PlainAcceptedStr(str):
        pass

    class OverrideAcceptedStr(str):
        def __str__(self):
            return "OVERRIDE_MUST_NOT_REPLACE_UNDERLYING_JSON_TEXT"

    results = []
    for name, subtype in [("plain_accepted_str", PlainAcceptedStr),
                          ("accepted_str_with_str_override", OverrideAcceptedStr)]:
        arguments = copy.deepcopy(kwargs)

        def foreign(text):
            require(type(text) is str, "subclass fixture starts with builtin underlying text")
            value = subtype(text)
            value.caller_marker = {"case": name, "kept": [None, True, 1, "1", -0.0]}
            require(str.encode(value) == str.encode(text), "subclass underlying text changed")
            return value

        first = arguments["owners"][0]
        for field in ("owner", "category", "path", "sha256"):
            first[field] = foreign(first[field])
        new_inputs = arguments["newly_declared_input_paths"]
        arguments["newly_declared_input_paths"] = {
            foreign(path): {field: foreign(text) for field, text in descriptor.items()}
            for path, descriptor in new_inputs.items()}
        for alias in arguments["aliases"]:
            for field in ("path", "text", "target", "kind"):
                alias[field] = foreign(alias[field])
        arguments["namespaces"][0]["owner"] = foreign(arguments["namespaces"][0]["owner"])
        arguments["typed_snapshot"]["accepted_subclass_text"] = foreign("underlying snapshot text")
        arguments["read_trace"]["records"][0]["fixture_extra_descriptor"]["accepted_subclass_text"] = foreign("underlying trace text")
        before = caller_integrity_snapshot(arguments)
        original = g.create_wire_graph(**arguments)
        exact_value(before, caller_integrity_snapshot(arguments), name + "/caller_after_original")
        fresh = g.create_fresh_complete_wire_graph(**arguments)
        exact_value(before, caller_integrity_snapshot(arguments), name + "/caller_after_fresh")
        exact_value(original, fresh, name + "/complete_values_types_order_floatbits")
        require(compact_pin(original) == compact_pin(fresh), name + "/complete canonical bytes differ")
        require(original["content_sha256"] == fresh["content_sha256"]
                and original["wire_encoding"]["decoded_content_sha256"]
                == fresh["wire_encoding"]["decoded_content_sha256"],
                name + "/wire or legacy semantic SHA differs")
        require(not (mutable_ids(arguments) & mutable_ids(fresh)), name + "/fresh borrows caller mutable containers")
        artifacts.write_json("accepted_subclass_" + name + "_original_wire_graph.json", original)
        artifacts.write_json("accepted_subclass_" + name + "_fresh_wire_graph.json", fresh)
        artifacts.write_json("accepted_subclass_" + name + "_caller_witness.json", {
            "case": name, "complete_caller_identity_type_order_value_floatbit_snapshot": before,
            "class": subtype.__module__ + "." + subtype.__qualname__,
            "str_override_output": (str(first["owner"]) if name == "accepted_str_with_str_override" else None),
            "underlying_owner_text_hex": str.encode(first["owner"]).hex(),
            "complete_original_and_fresh_outputs_exact": True,
            "caller_before_after_all_values_types_order_ids_attrs_and_floatbits_exact": True,
        })
        results.append({"case": name, "producer_canonical_pin": compact_pin(fresh),
                        "wire_content_sha256": fresh["content_sha256"],
                        "legacy_semantic_sha256": fresh["wire_encoding"]["decoded_content_sha256"],
                        "complete_builtin_output_values_types_order_floatbits_equal": True,
                        "complete_caller_identity_type_order_value_attrs_floatbits_unchanged": True})
    return results


def fixture_controls(g, artifacts):
    fixture = artifacts.root / "fixture"
    fixture.mkdir(mode=0o700)
    files = {}
    owners = []
    for index, category in enumerate(g.CLOSURE_CATEGORIES):
        path = str(fixture / (str(index) + "_" + category + ".txt"))
        payload = ("pure helper fixture " + category + "\n").encode("ascii")
        with open(path, "xb") as stream:
            stream.write(payload)
        artifacts.sizes["fixture/" + Path(path).name] = len(payload)
        files[path] = hashlib.sha256(payload).hexdigest()
        owners.append({"owner": "fixture_owner_" + category, "category": category,
                       "kind": "pin", "path": path, "sha256": files[path]})
    ns = fixture / "sealed"
    ns.mkdir(mode=0o700)
    (ns / "subdir").mkdir(mode=0o700)
    ns_file = str(ns / "subdir" / "owned.txt")
    ns_payload = b"explicit complete namespace fixture\n"
    with open(ns_file, "xb") as stream:
        stream.write(ns_payload)
    artifacts.sizes["fixture/sealed/subdir/owned.txt"] = len(ns_payload)
    digest = hashlib.sha256(ns_payload).hexdigest()
    link = str(ns / "alias.txt")
    os.symlink("subdir/owned.txt", link)
    external_link = str(fixture / "file_alias.txt")
    target = next(iter(files))
    os.symlink(os.path.basename(target), external_link)
    aliases = g.capture_aliases([external_link])
    namespace = g.explicit_sealed_namespace(
        str(ns), {"subdir/owned.txt": digest},
        {"alias.txt": {"text": "subdir/owned.txt", "target": ns_file, "kind": "file", "sha256": digest}},
        owner="fixture_namespace_owner", category="source_namespace", directories=["subdir"])
    owners.append({"owner": "fixture_alias_owner", "category": "code_environment",
                   "kind": "pin", "path": external_link, "sha256": files[target]})
    new_path = str(fixture / "newly_declared.txt")
    with open(new_path, "xb") as stream:
        stream.write(b"new input only\n")
    artifacts.sizes["fixture/newly_declared.txt"] = 15
    # Preserve repeated complete owner descriptors and logical edges, plus the
    # distinction between missing and explicitly empty/new owner path lists.
    owners.append(copy.deepcopy(owners[3]))
    repeated_path = list(files)[1]
    owners.extend([
        {"owner": "fixture_repeated_owner", "category": "original92_build",
         "expected_files": {repeated_path: files[repeated_path]}},
        {"owner": "fixture_repeated_owner", "category": "original92_build",
         "expected_files": {repeated_path: files[repeated_path]}, "newly_declared_input_paths": []},
        {"owner": "fixture_repeated_owner", "category": "original92_build",
         "expected_files": {repeated_path: files[repeated_path]}, "newly_declared_input_paths": [new_path]},
    ])
    absent = str(fixture / "known_absent.txt")
    with g.ReadOpenAudit() as audit:
        for path in [*files, ns_file, link, external_link, new_path, target]:
            with open(path, "rb") as stream:
                stream.read()
        try:
            with open(absent, "rb"):
                raise AssertionError("declared absent fixture exists")
        except FileNotFoundError:
            pass
        descriptor = os.open(str(ns), os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        os.close(descriptor)
    trace = audit.snapshot()
    trace["records"][0]["fixture_extra_descriptor"] = {
        "z": [None, False, 0, "0", -0.0], "a": {"kept": "all original trace fields remain"}}
    kwargs = {
        "typed_snapshot": {"fixture": {"order": [None, True, 1, "1", -0.0, 0.0],
                                      "unicode": "\u4e2d\u6587", "nested": {"z": 0, "a": 1}}},
        "owners": owners, "namespaces": [namespace], "aliases": aliases, "read_trace": trace,
        "newly_declared_input_paths": {new_path: {"owner": "fixture_new_owner", "category": "capture",
                                                    "reason": "new fixture input only"}},
        "absence_inputs": {absent: {"owner": "fixture_absence_owner", "category": "code_environment",
                                     "reason": "explicit optional fixture candidate"}},
        "declared_new_source_roots": [str(fixture)],
        "coverage_requirements": {category: {"minimum_files": 1, "minimum_bytes": 1,
                                              "required_owner_names": ["fixture_owner_" + category]}
                                  for category in g.CLOSURE_CATEGORIES},
    }
    before = copy.deepcopy(kwargs)
    caller_ids = mutable_ids(kwargs)
    original = g.create_wire_graph(**kwargs)
    exact_value(kwargs, before, "caller_after_original")
    fresh = g.create_fresh_complete_wire_graph(**kwargs)
    exact_value(kwargs, before, "caller_after_fresh")
    require(mutable_ids(kwargs) == caller_ids, "caller mutable identities changed")
    require(not (caller_ids & mutable_ids(fresh)), "fresh graph borrows caller mutable containers")
    exact_value(original, fresh, "full_small_producer_value")
    require(compact_pin(original) == compact_pin(fresh), "small producer canonical bytes differ")
    require(original["content_sha256"] == fresh["content_sha256"]
            and original["wire_encoding"]["decoded_content_sha256"] == fresh["wire_encoding"]["decoded_content_sha256"],
            "small producer wire/legacy digests differ")
    legacy = g.decode_graph_wire(original)
    require(legacy["content_sha256"] == fresh["wire_encoding"]["decoded_content_sha256"],
            "small full legacy semantic inverse differs")
    original_rows = list(g.iter_graph_requirement_rows(original))
    fresh_rows = list(g.iter_graph_requirement_rows(fresh))
    require(len(original_rows) == original["requirements"]["rows"]["row_count"]
            and all(type(row) is tuple and len(row) == 5 for row in original_rows + fresh_rows),
            "complete requirement iterator did not retain every five-column tuple")
    exact_value([list(row) for row in original_rows], [list(row) for row in fresh_rows],
                "complete_ordered_original_vs_fresh_requirement_iterator")
    exact_value(legacy["requirements"]["rows"], [list(row) for row in fresh_rows],
                "complete_requirement_iterator_vs_full_legacy_inverse")
    accepted_subclasses = accepted_str_subclass_controls(g, kwargs, artifacts)
    rejections = []
    cases = []

    def bad(name, change):
        altered = copy.deepcopy(kwargs)
        change(altered)
        cases.append({"case": name, "arguments": altered})
        paired_rejection(g, name, altered, rejections)

    bad("missing_owner_name", lambda k: k["owners"][0].pop("owner"))
    bad("unknown_owner_category", lambda k: k["owners"][0].update(category="not_a_category"))
    bad("unknown_owner_field", lambda k: k["owners"][0].update(unknown=True))
    bad("wrong_expected_sha", lambda k: k["owners"][0].update(sha256="0" * 64))
    bad("missing_closure_class", lambda k: k.update(
        owners=[owner for owner in k["owners"] if owner["category"] != "code_environment"], aliases=[]))
    bad("wrong_required_owner", lambda k: k["coverage_requirements"]["memory_build"].update(required_owner_names=["wrong_owner"]))
    bad("insufficient_category_bytes", lambda k: k["coverage_requirements"]["memory_build"].update(minimum_bytes=1000000))
    bad("bool_coverage_minimum", lambda k: k["coverage_requirements"]["memory_build"].update(minimum_files=True))
    bad("bad_trace_attempt_bool", lambda k: k["read_trace"]["records"][0].update(attempt_count=True))
    bad("bad_trace_flags_bool", lambda k: k["read_trace"]["records"][0].update(flags=False))
    bad("wrong_trace_access", lambda k: k["read_trace"]["records"][0].update(access="readwrite"))
    bad("empty_trace", lambda k: k["read_trace"].update(records=[]))
    bad("unavailable_traced_path", lambda k: k["read_trace"]["records"][0].update(path=str(fixture / "unknown.txt")))
    bad("undeclared_alias", lambda k: k.update(aliases=[]))
    bad("wrong_alias_text", lambda k: k["aliases"][0].update(text="wrong_target"))
    bad("wrong_namespace_inventory", lambda k: k["namespaces"][0]["files"].clear())
    bad("wrong_new_owner", lambda k: k["newly_declared_input_paths"][new_path].update(owner=""))
    bad("nonfinite_snapshot", lambda k: k["typed_snapshot"].update(nonfinite=float("inf")))
    # A consumer scope is the new API's explicit extra rejection, not a claimed
    # old/new rejection equivalence for an unsupported complete producer mode.
    rejection(g, "fresh_consumer_scope", lambda: g.create_fresh_complete_wire_graph(**dict(kwargs, consumer_scope={})),
              rejections, "fresh complete producer cannot declare consumer scope")
    # JSON cannot encode the nonfinite rejected input. Store its exact mutation
    # description and error; every serializable malformed argument is retained.
    for case in cases:
        if case["case"] == "nonfinite_snapshot":
            case["arguments"] = {"mutation": "typed_snapshot.nonfinite = positive infinity"}
    result = {
        "real_fixture_open_audit": trace, "fixture_arguments": kwargs,
        "producer_full_exact_values_types_order_floatbits": True,
        "producer_canonical_pin": compact_pin(fresh), "wire_content_sha256": fresh["content_sha256"],
        "legacy_semantic_sha256": fresh["wire_encoding"]["decoded_content_sha256"],
        "caller_full_value_and_mutable_identity_preserved": True,
        "fresh_graph_has_no_caller_mutable_container": True,
        "all_nine_closure_categories": list(fresh["coverage"]),
        "duplicate_owner_descriptors_edges_and_optional_new_lists_preserved": True,
        "real_trace_attempt_multiplicity_and_extra_fields_preserved": True,
        "complete_requirement_iterator_order_values_and_duplicate_edges_equal": True,
        "canonical_files": len(fresh["canonical_files"]), "requirement_rows": fresh["requirements"]["rows"]["row_count"],
        "accepted_str_subclass_equivalence_controls": accepted_subclasses,
        "complete_rejected_arguments": cases, "rejections": rejections,
    }
    artifacts.write_json("small_fixture_original_wire_graph.json", original)
    artifacts.write_json("small_fixture_fresh_wire_graph.json", fresh)
    artifacts.write_json("small_fixture_controls.json", result)
    return fresh, result


def codec_controls(g, graph, artifacts):
    records = [
        {"z": "", "a": None, "x": 1, "bool": True, "f": -0.0,
         "nested": {"z": [None, False, 2, "2", 0.0], "a": {"q": "\u4e2d\u6587"}}},
        {"x": "1", "a": None, "z": "", "bool": 1, "f": 0.0},
        {"x": "1", "z": ""},
        {},
        {"z": "", "a": None, "x": 1, "bool": True, "f": -0.0,
         "nested": {"z": [None, False, 2, "2", 0.0], "a": {"q": "\u4e2d\u6587"}}},
    ]
    untouched = copy.deepcopy(records)
    table = g._encode_read_trace_record_table(records)
    table_before = copy.deepcopy(table)
    inverse = g._decode_read_trace_record_table(table)
    exact_value(records, untouched, "trace_encode_nonmutation")
    exact_value(table, table_before, "trace_decode_nonmutation")
    exact_value(records, inverse, "trace_default_inverse")
    # Consume controls are performed only on fresh parsed containers. A borrowed
    # encode view is never used with a private consume flag.
    parsed = g._parse_strict_json_text(json.dumps(table, allow_nan=False), "fresh_trace_fixture")
    expected_parsed_inverse = g._decode_read_trace_record_table(parsed)
    consumed = g._decode_read_trace_record_table(parsed, _consume=True)
    exact_value(expected_parsed_inverse, consumed, "trace_owned_inverse")
    require(all(parsed[field] == [] for field in ("columns", "layouts", "strings", "rows")),
            "trace owned consume retained its completed table arrays")
    empty = g._encode_read_trace_record_table([])
    require(g._decode_read_trace_record_table(empty) == [], "empty trace inverse rejected")
    canonical = g.encode_canonical_file_table_storage(graph)
    canonical_before = copy.deepcopy(canonical)
    canonical_inverse = g.decode_canonical_file_table_storage(canonical)
    exact_value(canonical, canonical_before, "canonical_default_nonmutation")
    exact_value(graph, canonical_inverse, "canonical_full_inverse")
    storage = g.encode_complete_graph_table_storage(graph)
    storage_before = copy.deepcopy(storage)
    whole_inverse = g.decode_complete_graph_table_storage(storage)
    exact_value(storage, storage_before, "complete_default_nonmutation")
    exact_value(graph, whole_inverse, "complete_full_inverse")
    parsed_whole = g._parse_strict_json_text(json.dumps(storage, allow_nan=False), "fresh_complete_fixture")
    complete_consumed = g.decode_complete_graph_table_storage(parsed_whole, _consume=True)
    strict_expected_graph = g._json_clone(graph)
    exact_value(strict_expected_graph, complete_consumed, "complete_owned_inverse")
    require(parsed_whole["graph"]["canonical_files"]["rows"] == []
            and all(parsed_whole["graph"]["read_trace"]["records"][field] == []
                    for field in ("columns", "layouts", "strings", "rows")),
            "complete owned consume retained completed table arrays")
    rejections = []
    malformed = []

    def malformed_table(name, change, message):
        altered = copy.deepcopy(table)
        change(altered)
        malformed.append({"case": name, "table": altered})
        rejection(g, name, lambda: g._decode_read_trace_record_table(altered), rejections, message)

    malformed_table("trace_extra_header", lambda t: t.update(extra=None), "invalid complete trace table header")
    malformed_table("trace_duplicate_columns", lambda t: t["columns"].append(t["columns"][0]), "invalid trace storage columns")
    malformed_table("trace_unsorted_columns", lambda t: t["columns"].reverse(), "invalid trace storage columns")
    malformed_table("trace_nonstring_column", lambda t: t["columns"].append(7), "invalid trace storage columns")
    malformed_table("trace_duplicate_strings", lambda t: t["strings"].append(t["strings"][0]), "invalid trace storage string table")
    malformed_table("trace_nonstring_symbol", lambda t: t["strings"].append(1), "invalid trace storage string table")
    malformed_table("trace_bool_row_count", lambda t: t.update(row_count=True), "invalid complete trace row count")
    malformed_table("trace_wrong_row_count", lambda t: t.update(row_count=t["row_count"] + 1), "invalid complete trace row count")
    malformed_table("trace_nonlist_layout", lambda t: t["layouts"].__setitem__(0, None), "invalid trace storage layout")
    malformed_table("trace_bool_column_index", lambda t: t["layouts"][0][0].__setitem__(0, True), "invalid trace storage field/type discriminator")
    malformed_table("trace_bad_column_index", lambda t: t["layouts"][0][0].__setitem__(0, len(t["columns"])), "invalid trace storage field/type discriminator")
    malformed_table("trace_int_discriminator", lambda t: t["layouts"][0][0].__setitem__(1, 1), "invalid trace storage field/type discriminator")
    malformed_table("trace_duplicate_layout_field", lambda t: t["layouts"][0].append(copy.deepcopy(t["layouts"][0][0])), "duplicate trace layout field")
    malformed_table("trace_duplicate_layout", lambda t: t["layouts"].append(copy.deepcopy(t["layouts"][0])), "duplicate trace storage layout")
    malformed_table("trace_bool_layout_index", lambda t: t["rows"][0].__setitem__(0, True), "invalid trace storage row/layout index")
    malformed_table("trace_negative_layout_index", lambda t: t["rows"][0].__setitem__(0, -1), "invalid trace storage row/layout index")
    malformed_table("trace_large_layout_index", lambda t: t["rows"][0].__setitem__(0, len(t["layouts"])), "invalid trace storage row/layout index")
    malformed_table("trace_wrong_field_count", lambda t: t["rows"][0].append(None), "invalid trace storage row field count")
    malformed_table("trace_bool_string_index", lambda t: t["rows"][0].__setitem__(1, True), "invalid trace storage string index")
    malformed_table("trace_negative_string_index", lambda t: t["rows"][0].__setitem__(1, -1), "invalid trace storage string index")
    malformed_table("trace_large_string_index", lambda t: t["rows"][0].__setitem__(1, len(t["strings"])), "invalid trace storage string index")
    malformed_table("trace_string_for_nonstr_cell", lambda t: t["rows"][0].__setitem__(2, "null"), "trace cell disagrees with string type discriminator")
    malformed_table("trace_unused_string", lambda t: t["strings"].append("unused_symbol"), "unused trace storage symbols or layouts")
    malformed_table("trace_unused_column", lambda t: t["columns"].append("zz_unused_column"), "unused trace storage symbols or layouts")
    malformed_table("trace_unused_layout", lambda t: t["layouts"].append([[0, False]]), "unused trace storage symbols or layouts")

    def reorder_layouts(t):
        t["layouts"][0], t["layouts"][1] = t["layouts"][1], t["layouts"][0]
        for row in t["rows"]:
            if row[0] in (0, 1):
                row[0] = 1 - row[0]

    def reorder_strings(t):
        t["strings"][0], t["strings"][1] = t["strings"][1], t["strings"][0]
        for row in t["rows"]:
            for position, (_column, string_type) in enumerate(t["layouts"][row[0]], 1):
                if string_type and row[position] in (0, 1):
                    row[position] = 1 - row[position]

    malformed_table("trace_layout_first_occurrence", reorder_layouts, "trace layouts not in first-occurrence order")
    malformed_table("trace_string_first_occurrence", reorder_strings, "trace strings not in first-occurrence order")
    for name, value, message in [
        ("trace_nested_nonfinite", [{"a": [float("nan")]}], "trace nested JSON values must be finite"),
        ("trace_nested_nonstring_key", [{"a": {1: 2}}], "trace nested JSON object keys must be strings"),
        ("trace_cell_tuple", [{"a": (1, 2)}], "trace cells must preserve builtin JSON types"),
        ("trace_record_nonstring_key", [{1: 2}], "complete trace record must be a builtin JSON object"),
        ("trace_nonlist_records", ({"a": 1},), "complete trace records must be a list"),
    ]:
        rejection(g, name, lambda value=value: g._encode_read_trace_record_table(value), rejections, message)
    cycle = []
    cycle.append(cycle)
    rejection(g, "trace_nested_cycle", lambda: g._encode_read_trace_record_table([{"a": cycle}]), rejections,
              "trace nested JSON container cycle")
    cycle.clear()
    for name, callback, message in [
        ("trace_bad_consume_flag", lambda: g._decode_read_trace_record_table(table, _consume=1), "invalid private trace storage consume flag"),
        ("complete_bad_consume_flag", lambda: g.decode_complete_graph_table_storage(storage, _consume=1), "invalid private complete graph storage consume flag"),
        ("canonical_bad_consume_flag", lambda: g.decode_canonical_file_table_storage(canonical, _consume=1), "invalid private canonical-file storage consume flag"),
    ]:
        rejection(g, name, callback, rejections, message)

    def malformed_whole(name, change, message):
        altered = copy.deepcopy(storage)
        change(altered)
        malformed.append({"case": name, "whole_storage": altered})
        rejection(g, name, lambda: g.decode_complete_graph_table_storage(altered), rejections, message)

    malformed_whole("whole_extra_header", lambda s: s.update(extra=1), "invalid complete graph trace storage header")
    malformed_whole("whole_wrong_schema", lambda s: s.update(schema="wrong"), "invalid complete graph trace storage header")
    malformed_whole("whole_wrong_scope", lambda s: s["graph"].update(scope="wrong"), "invalid original decoded graph schema/scope")
    malformed_whole("canonical_wrong_columns", lambda s: s["graph"]["canonical_files"]["columns"].reverse(), "invalid canonical-file table header/columns")
    malformed_whole("canonical_short_row", lambda s: s["graph"]["canonical_files"]["rows"][0].pop(), "invalid canonical-file storage row shape")
    malformed_whole("canonical_bool_size", lambda s: s["graph"]["canonical_files"]["rows"][0].__setitem__(2, True), "invalid canonical-file storage row scalar types")
    malformed_whole("canonical_negative_size", lambda s: s["graph"]["canonical_files"]["rows"][0].__setitem__(2, -1), "invalid canonical-file storage row scalar types")
    malformed_whole("whole_missing_trace", lambda s: s["graph"].pop("read_trace"), "invalid complete graph trace descriptor")
    malformed_whole("whole_content_changed", lambda s: s["graph"].update(content_sha256="0" * 64), "decoded complete graph content changed")
    malformed_whole("whole_extra_original_value", lambda s: s["graph"].update(new_unbound_field=True), "decoded complete graph content changed")
    changed_graph = copy.deepcopy(graph)
    changed_graph["canonical_files"][0] = dict(reversed(list(changed_graph["canonical_files"][0].items())))
    rejection(g, "encode_canonical_pin_keyorder", lambda: g.encode_complete_graph_table_storage(changed_graph), rejections,
              "canonical-file storage pin fields/order differ")
    changed_graph = copy.deepcopy(graph)
    changed_graph["content_sha256"] = "0" * 64
    rejection(g, "encode_changed_digest", lambda: g.encode_complete_graph_table_storage(changed_graph), rejections,
              "original graph content changed before storage encoding")
    for name, payload, message in [
        ("duplicate_keys", b'{"a":1,"a":2}', "duplicate JSON key: 'a'"),
        ("nonfinite_NaN", b'{"a":NaN}', "nonfinite JSON constant: NaN"),
        ("nonfinite_Infinity", b'{"a":Infinity}', "nonfinite JSON constant: Infinity"),
        ("overflow_float", b'{"a":1e9999}', "snapshot/descriptors must be finite JSON data"),
    ]:
        path = artifacts.write_bytes("strict_reject_" + name + ".json", payload)
        rejection(g, "file_" + name, lambda path=path: g.strict_json(path), rejections, message)
        rejection(g, "payload_" + name, lambda payload=payload, path=path: g._parse_strict_json_payload(payload, path), rejections, message)
    path = artifacts.write_bytes("strict_reject_invalid_utf8.json", b'{"a":"\xff"}')
    rejection(g, "file_invalid_utf8", lambda: g.strict_json(path), rejections, "invalid UTF-8 JSON: " + path)
    rejection(g, "payload_invalid_utf8", lambda: g._parse_strict_json_payload(b'{"a":"\xff"}', path), rejections, "invalid UTF-8 JSON: " + path)
    ordinary = {"z": [True, 1, "1", None, -0.0], "a": {"z": 0, "a": ""}}
    ordinary_payload = json.dumps(ordinary, allow_nan=False).encode("utf-8")
    path = artifacts.write_bytes("strict_ordinary_compatibility.json", ordinary_payload)
    expected = g._json_clone(ordinary)
    exact_value(expected, g.strict_json(path), "ordinary_file")
    exact_value(expected, g._parse_strict_json_payload(ordinary_payload, path), "ordinary_payload")
    for name, encoded in [("canonical", canonical), ("complete", storage)]:
        pin = artifacts.write_json("strict_dispatch_" + name + ".json", encoded)
        exact_value(strict_expected_graph, g.strict_json(pin["path"], pin["sha256"]), name + "_file_dispatch")
        with open(pin["path"], "rb") as stream:
            payload = stream.read(MAX_JSON_BYTES + 1)
        require(len(payload) <= MAX_JSON_BYTES, "small dispatch payload exceeded bound")
        exact_value(strict_expected_graph, g._parse_strict_json_payload(payload, pin["path"]), name + "_payload_dispatch")
    complete_payload = JSON_ENCODER.encode(storage).encode("ascii")
    duplicate_storage = (b'{"schema":' + json.dumps(storage["schema"]).encode("ascii")
                         + b',' + complete_payload[1:])
    path = artifacts.write_bytes("strict_reject_duplicate_storage_header.json", duplicate_storage)
    rejection(g, "file_duplicate_storage_header", lambda: g.strict_json(path), rejections,
              "duplicate JSON key: 'schema'")
    rejection(g, "payload_duplicate_storage_header",
              lambda: g._parse_strict_json_payload(duplicate_storage, path), rejections,
              "duplicate JSON key: 'schema'")
    rejection(g, "strict_bool_read_bound", lambda: g.strict_json(path, max_bytes=True), rejections,
              "invalid JSON read bound")
    result = {"complete_trace_fixture": records, "encoded_trace_table": table,
              "all_lossless_missing_null_order_type_floatbit_duplicate_controls": True,
              "all_default_inputs_unmodified": True, "fresh_parsed_consume_arrays_released": True,
              "ordinary_and_both_storage_strict_dispatches": True,
              "all_malformed_serializable_tables": malformed,
              "non_json_rejected_input_descriptions": {
                  "trace_nested_nonfinite": "records=[{'a':[float('nan')]}]",
                  "trace_nested_nonstring_key": "records=[{'a':{1:2}}]",
                  "trace_cell_tuple": "records=[{'a':(1,2)}]",
                  "trace_record_nonstring_key": "records=[{1:2}]",
                  "trace_nonlist_records": "records=({'a':1},)",
                  "trace_nested_cycle": "cycle=[]; cycle.append(cycle); records=[{'a':cycle}]",
              },
              "rejections": rejections}
    artifacts.write_json("small_codec_and_rejection_controls.json", result)
    return {"accepted_trace_rows": len(records), "rejections": len(rejections),
            "small_controls_artifact": str(artifacts.root / "small_codec_and_rejection_controls.json")}


def strict_order_preserving_metadata(g, pin):
    """Same bounded strict scalar gates, retaining saved JSON insertion order.

    This is used only to inspect saved trace metadata. The normal graph strict
    wrappers deliberately sort parsed keys and are tested unchanged elsewhere.
    It is never a runtime graph admission entrance or a component API.
    """
    pinned_identity(pin)
    canonical = g._resolve(pin["path"], {}, kind="file")
    require(canonical == pin["path"], "saved metadata endpoint is not canonical")
    fresh_pin, payload = g._stream(canonical, collect=True, max_bytes=MAX_JSON_BYTES)
    require(fresh_pin["sha256"] == pin["sha256"] and fresh_pin["size_bytes"] == pin["identity"][4],
            "saved metadata fresh bytes differ from exact pin")
    require(g._resolve(pin["path"], {}, kind="file") == canonical, "saved metadata endpoint changed")
    try:
        text = payload.decode("utf-8")
    except UnicodeError as error:
        raise g.InputGraphError("invalid UTF-8 JSON: " + pin["path"]) from error
    del payload
    try:
        value = json.loads(text, object_pairs_hook=g._unique_object,
                           parse_constant=g._invalid_constant, parse_float=g._finite_float)
    except (UnicodeError, json.JSONDecodeError) as error:
        raise g.InputGraphError("invalid UTF-8 JSON: " + pin["path"]) from error
    del text
    pinned_identity(pin)
    return value


def full_trace_controls(g, artifacts):
    trace = strict_order_preserving_metadata(g, TRACE_PIN)
    require(type(trace) is dict and trace.get("schema") == g.TRACE_SCHEMA,
            "full creation trace schema changed")
    require(type(trace.get("records")) is list and len(trace["records"]) == TRACE_ORIGINAL_ORDER_COMPACT_PIN["records"],
            "full trace record count changed")
    require(len(trace.get("subprocess_records", [])) == TRACE_ORIGINAL_ORDER_COMPACT_PIN["subprocess_records"],
            "full trace subprocess record count changed")
    source_compact = compact_pin(trace, ORDER_PRESERVING_JSON_ENCODER)
    require(source_compact == {key: TRACE_ORIGINAL_ORDER_COMPACT_PIN[key] for key in ("size_bytes", "sha256")},
            "full trace compact metadata pin changed")
    # Full source trace is only saved metadata. Do not call _trace_records or
    # _trace_coverage, which would relabel it as a new runtime graph admission.
    before = order_type_pin(trace)
    table = g._encode_read_trace_record_table(trace["records"])
    encoded = {"schema": "AXMAT_COMPLETE_CREATION_TRACE_TABLE_PURE_CONTROL_STORAGE_V1",
               "trace": dict(trace, records=table)}
    restored = g._decode_read_trace_record_table(table)
    exact_value(trace["records"], restored, "all_63379_creation_trace_records")
    require(order_type_pin(trace) == before, "full trace input mutated")
    del restored
    gc.collect()
    stored_pin = compact_pin(encoded, ORDER_PRESERVING_JSON_ENCODER)
    trace_artifact = None
    # Reserve enough space for small reports. The later wholegraph stage has
    # priority and removes this optional owned artifact before any conflicting
    # write. There is never an over-budget transient output set.
    if stored_pin["size_bytes"] <= artifacts.remaining() - 1048576:
        trace_artifact = artifacts.write_json("full_new_creation_trace.encoded.json", encoded, stored_pin,
                                               ORDER_PRESERVING_JSON_ENCODER)
    result = {"input": dict(TRACE_PIN), "original_insertion_order_compact_source": source_compact,
              "sorted_canonical_semantic_compact_source": compact_pin(trace),
              "stored_complete_descriptor": stored_pin, "full_record_count": len(trace["records"]),
              "subprocess_record_count": len(trace.get("subprocess_records", [])),
              "actual_attempt_count": sum(record["attempt_count"] for record in trace["records"]),
              "table_columns": len(table["columns"]), "table_layouts": len(table["layouts"]),
              "table_strings": len(table["strings"]), "table_rows": table["row_count"],
              "complete_order_type_floatbit_value_pin": before,
              "exact_full_roundtrip": True, "default_source_nonmutation": True,
              "encoded_artifact": trace_artifact}
    del encoded, table, trace
    gc.collect()
    if trace_artifact is not None:
        stored = strict_order_preserving_metadata(g, trace_artifact)
        require(stored["schema"] == "AXMAT_COMPLETE_CREATION_TRACE_TABLE_PURE_CONTROL_STORAGE_V1",
                "stored full trace control envelope changed")
        fresh_trace = dict(stored["trace"])
        fresh_trace["records"] = g._decode_read_trace_record_table(stored["trace"]["records"], _consume=True)
        require(order_type_pin(fresh_trace) == before,
                "persisted full trace loses original order/types/floatbits/values")
        result["persisted_full_trace_exact_order_type_floatbit_inverse"] = True
        del fresh_trace, stored
        gc.collect()
    return result


def graph_metadata(g, graph):
    require(type(graph) is dict and graph.get("schema") == g.WIRE_GRAPH_SCHEMA
            and graph.get("scope") == g.INPUT_SCOPE, "complete saved wire graph required")
    require(graph.get("science_qualification_created") is False, "unexpected science credit in saved metadata")
    table = graph["requirements"]
    require(table["schema"] == g.WIRE_REQUIREMENT_TABLE_SCHEMA, "complete wire requirements required")
    limits = (len(table["paths"]), len(table["paths"]), len(table["owners"]),
              len(g.CLOSURE_CATEGORIES), len(g.REQUIREMENT_ROLES))
    row_count = 0
    category_rows = [0] * len(g.CLOSURE_CATEGORIES)
    role_rows = [0] * len(g.REQUIREMENT_ROLES)
    for row in g._decoded_requirement_rows(table["rows"], limits):
        row_count += 1
        category_rows[row[3]] += 1
        role_rows[row[4]] += 1
    require(row_count == table["rows"]["row_count"], "complete requirement iterator count differs")
    semantic_sha = g._wire_semantic_content_digest(graph)
    require(semantic_sha == graph["wire_encoding"]["decoded_content_sha256"],
            "complete saved legacy semantic SHA differs")
    return {
        "wire_content_sha256": graph["content_sha256"], "legacy_semantic_sha256": semantic_sha,
        "all_values_order_types_floatbits": order_type_pin(graph),
        "complete_counts": {
            "top_fields": len(graph), "canonical_files": len(graph["canonical_files"]),
            "requirements": row_count, "requirement_paths": len(table["paths"]),
            "requirement_owners": len(table["owners"]), "owners": len(graph["owners"]["rows"]),
            "namespaces": len(graph["namespaces"]), "aliases": len(graph["aliases"]),
            "new_paths": len(graph["newly_declared_input_paths"]), "new_pins": len(graph["newly_declared_input_pins"]),
            "absence_inputs": len(graph["absence_inputs"]), "absence_observations": len(graph["absence_observations"]),
            "read_trace_records": len(graph["read_trace"]["records"]),
            "read_trace_attempts": sum(record["attempt_count"] for record in graph["read_trace"]["records"]),
            "subprocess_records": len(graph["read_trace"]["subprocess_records"]),
            "category_requirement_rows": dict(zip(g.CLOSURE_CATEGORIES, category_rows)),
            "role_requirement_rows": dict(zip(g.REQUIREMENT_ROLES, role_rows)),
            "namespace_files": sum(len(ns["files"]) for ns in graph["namespaces"]),
            "namespace_symlinks": sum(len(ns["symlinks"]) for ns in graph["namespaces"]),
            "namespace_directories": sum(len(ns["directories"]) for ns in graph["namespaces"]),
        },
        "complete_closure_coverage": graph["coverage"],
        "complete_trace_coverage": graph["trace_coverage"],
    }


def full_graph_controls(g, artifacts, trace_result):
    pinned_identity(GRAPH_PIN)
    graph = g.strict_json(GRAPH_PIN["path"], GRAPH_PIN["sha256"], max_bytes=MAX_JSON_BYTES)
    pinned_identity(GRAPH_PIN)
    original_metadata = graph_metadata(g, graph)
    require(original_metadata["complete_counts"]["read_trace_records"] == 62332,
            "old complete trace row count changed")
    encoded = g.encode_complete_graph_table_storage(graph)
    restored = g.decode_complete_graph_table_storage(encoded)
    exact_value(graph, restored, "all_full_saved_graph_values_types_order_floatbits")
    require(g._wire_semantic_content_digest(restored) == original_metadata["legacy_semantic_sha256"],
            "full default inverse legacy semantic SHA differs")
    del restored
    gc.collect()
    # The full old graph and encoded view share the unchanged graph values;
    # no replacement of old read_trace by the new trace is performed here.
    stored_pin = compact_pin(encoded)
    require(stored_pin["size_bytes"] <= MAX_JSON_BYTES, "new encoded wholegraph exceeds fixed 64MiB read cap")
    optional_trace = "full_new_creation_trace.encoded.json"
    if stored_pin["size_bytes"] + 1048576 > artifacts.remaining() and optional_trace in artifacts.sizes:
        artifacts.drop(optional_trace)
        trace_result["encoded_artifact"] = None
        trace_result["artifact_omission_reason"] = "wholegraph retained; combined stored outputs would exceed fixed 64MiB"
    require(stored_pin["size_bytes"] + 1048576 <= artifacts.remaining(), "wholegraph plus reports exceeds fixed output cap")
    output_pin = artifacts.write_json("full_old_saved_graph.encoded.json", encoded, stored_pin)
    del encoded, graph
    gc.collect()
    # Two normal strict entrances read this same persisted byte file separately.
    # Each fresh parsed graph is released before the next entrance begins.
    strict = g.strict_json(output_pin["path"], output_pin["sha256"], max_bytes=MAX_JSON_BYTES)
    strict_metadata = graph_metadata(g, strict)
    exact_value(original_metadata, strict_metadata, "full_graph_normal_strict_file_metadata")
    del strict
    gc.collect()
    require(identity(output_pin["path"]) == output_pin["identity"], "encoded wholegraph identity changed")
    with open(output_pin["path"], "rb") as stream:
        payload = stream.read(MAX_JSON_BYTES + 1)
    require(len(payload) == output_pin["size_bytes"] and len(payload) <= MAX_JSON_BYTES
            and hashlib.sha256(payload).hexdigest() == output_pin["sha256"],
            "same encoded wholegraph bytes differ at strict payload entrance")
    strict = g._parse_strict_json_payload(payload, output_pin["path"])
    del payload
    gc.collect()
    strict_payload_metadata = graph_metadata(g, strict)
    exact_value(original_metadata, strict_payload_metadata, "full_graph_normal_strict_payload_metadata")
    del strict
    gc.collect()
    require(identity(output_pin["path"]) == output_pin["identity"], "strict payload changed wholegraph identity")
    return {"input": dict(GRAPH_PIN), "complete_original_metadata": original_metadata,
            "full_default_roundtrip_exact": True, "original_legacy_semantic_sha_preserved": True,
            "stored_wholegraph": output_pin,
            "normal_strict_file_entrance_full_semantics_and_counts": strict_metadata,
            "normal_strict_payload_entrance_full_semantics_and_counts": strict_payload_metadata,
            "no_two_complete_decoded_graphs_between_strict_stages": True,
            "old_read_trace_not_replaced_by_new_trace": True}


def current_peak_bytes():
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return int(value if sys.platform == "darwin" else value * 1024)


def private_owner_consume_controls(g, small_graph):
    """New metadata controls; all original protocol fixtures/controls stay whole."""
    # Borrow the already-created original small graph; create no new files.
    expanded = g._expand_owner_table(small_graph["owners"], small_graph["requirements"])
    require(type(expanded) is list and len(expanded) >= 2,
            "complete original expanded small owner fixture required")

    def descriptor_signature(value):
        """Every value/type/order/str attrs/float bit; output mutable ids may differ."""
        kind = type(value)
        typename = kind.__module__ + "." + kind.__qualname__
        if kind is dict:
            return ["dict", [[descriptor_signature(k), descriptor_signature(v)]
                             for k, v in value.items()]]
        if kind in (list, tuple):
            return [typename, [descriptor_signature(v) for v in value]]
        if isinstance(value, str):
            attributes = getattr(value, "__dict__", None) if kind is not str else None
            return ["str", typename, str.encode(value, "utf-8", "surrogatepass").hex(),
                    descriptor_signature(attributes) if attributes is not None else None]
        if kind is float:
            return ["float", struct.pack(">d", value).hex()]
        require(kind in (int, bool, type(None)), "unexpected owner descriptor fixture type")
        return [typename, value]

    def caller_snapshot(values):
        return {"outer_type": type(values).__module__ + "." + type(values).__qualname__,
                "outer_identity": id(values),
                "complete_rows": [caller_integrity_snapshot(row) for row in values]}

    baseline_input = copy.deepcopy(expanded)
    baseline_before = caller_snapshot(baseline_input)
    baseline = g._owners(baseline_input)
    exact_value(baseline_before, caller_snapshot(baseline_input), "owner baseline default caller")
    baseline_signature = descriptor_signature(baseline)
    positives = []
    for label, caller, explicit in [
            ("default_list", copy.deepcopy(expanded), False),
            ("default_tuple", tuple(copy.deepcopy(expanded)), False),
            ("explicit_False_list", copy.deepcopy(expanded), True)]:
        before = caller_snapshot(caller)
        result = g._owners(caller, _consume=False) if explicit else g._owners(caller)
        after = caller_snapshot(caller)
        exact_value(before, after, label + "/complete owner caller identity/attrs/floatbits")
        signature = descriptor_signature(result)
        exact_value(baseline_signature, signature, label + "/complete normalized descriptors")
        positives.append({"case": label,
                          "caller_full_identity_type_order_value_attrs_floatbits_unchanged": True,
                          "full_normalized_descriptor_types_order_values_attrs_floatbits_equal_default": True,
                          "expected_complete_descriptor_signature": baseline_signature,
                          "actual_complete_descriptor_signature": signature})
    owned = copy.deepcopy(expanded)
    require(type(owned) is list, "fresh exclusively owned builtin owner list required")
    result = g._owners(owned, _consume=True)
    require(owned == [], "successful private owner normalization must clear the source list")
    signature = descriptor_signature(result)
    exact_value(baseline_signature, signature, "owned True complete normalized descriptors")
    positives.append({"case": "owned_builtin_list_True",
                      "owned_list_completely_cleared_after_success": True,
                      "full_normalized_descriptor_types_order_values_attrs_floatbits_equal_default": True,
                      "expected_complete_descriptor_signature": baseline_signature,
                      "actual_complete_descriptor_signature": signature})

    class PlainAcceptedStr(str):
        pass

    class OverrideAcceptedStr(str):
        def __str__(self):
            return "OVERRIDE_MUST_NOT_REPLACE_UNDERLYING_OWNER_TEXT"

    subtypes = []
    for label, subtype in [("plain_accepted_str", PlainAcceptedStr),
                            ("accepted_str_with_str_override", OverrideAcceptedStr)]:
        rows = copy.deepcopy(expanded)

        def foreign(value):
            require(type(value) is str, "owner subtype starts with builtin underlying text")
            part = subtype(value)
            part.caller_marker = {"case": label, "bits": [-0.0, 1e-300, 1.25],
                                  "types": [None, True, False, 0, "0"]}
            return part

        row = rows[0]
        row["owner"] = foreign(row["owner"])
        row["category"] = foreign(row["category"])
        row["expected_files"] = {foreign(path): foreign(digest)
                                 for path, digest in row["expected_files"].items()}
        if "newly_declared_input_paths" in row:
            row["newly_declared_input_paths"] = [foreign(path)
                                                 for path in row["newly_declared_input_paths"]]
        before = caller_snapshot(rows)
        subtype_default = g._owners(rows)
        exact_value(before, caller_snapshot(rows), label + "/default full owner caller")
        owned = copy.deepcopy(rows)
        subtype_result = g._owners(owned, _consume=True)
        require(owned == [], label + "/successful owned list completely cleared")
        expected_signature = descriptor_signature(subtype_default)
        actual_signature = descriptor_signature(subtype_result)
        exact_value(expected_signature, actual_signature, label + "/owner types attrs bits")
        exact_value(before, caller_snapshot(rows), label + "/original default caller preserved")
        subtypes.append({"case": label,
                         "default_caller_full_identity_type_order_value_attrs_floatbits_unchanged": True,
                         "owned_list_completely_cleared_after_success": True,
                         "complete_normalized_descriptor_types_order_value_strattrs_floatbits_equal_default": True,
                         "expected_complete_descriptor_signature": expected_signature,
                         "actual_complete_descriptor_signature": actual_signature})

    class ListSubclass(list):
        pass

    negatives = []
    for label, caller, consume in [
            ("nonbool_consume", copy.deepcopy(expanded), 1),
            ("tuple_True", tuple(copy.deepcopy(expanded)), True),
            ("list_subclass_True", ListSubclass(copy.deepcopy(expanded)), True)]:
        before = caller_snapshot(caller)
        case = rejection(g, label, lambda: g._owners(caller, _consume=consume), negatives,
                         expected_message="private owner consume needs a bool and an exclusively owned builtin list")
        exact_value(before, caller_snapshot(caller), label + "/rejected owner caller unchanged")
        case["caller_full_identity_type_order_value_attrs_floatbits_unchanged"] = True

    default_partial = [copy.deepcopy(expanded[0]), {}]
    default_before = caller_snapshot(default_partial)
    partial_records = []
    left = rejection(g, "invalid_second_owner_default",
                     lambda: g._owners(default_partial), partial_records,
                     expected_message="missing file owner")
    exact_value(default_before, caller_snapshot(default_partial), "invalid default caller unchanged")
    first, invalid = copy.deepcopy(expanded[0]), {}
    first_before, invalid_before = caller_integrity_snapshot(first), caller_integrity_snapshot(invalid)
    owned_partial = [first, invalid]
    right = rejection(g, "invalid_second_owner_owned_True",
                      lambda: g._owners(owned_partial, _consume=True), partial_records,
                      expected_message="missing file owner")
    require(len(owned_partial) == 2 and owned_partial[0] is None and owned_partial[1] is invalid,
            "valid first row must be consumed only after append; invalid second row stays original")
    exact_value(first_before, caller_integrity_snapshot(first), "consumed row descriptor not mutated")
    exact_value(invalid_before, caller_integrity_snapshot(invalid), "invalid row not consumed or mutated")
    require((left["class"], left["message"]) == (right["class"], right["message"]),
            "original invalid owner rejection class/order/message must be preserved")
    require(len(positives) == 4 and len(negatives) == 3 and len(subtypes) == 2
            and len(partial_records) == 2, "complete new private owner control set required")
    return {"schema": "AXMAT_V22_PRIVATE_OWNER_CONSUME_ACTUAL_CONTROL_V1",
            "status": "ACTUAL_PRIVATE_OWNER_CONTROLS_RETURNED_METADATA_ONLY",
            "positive_controls": positives, "private_guard_rejections": negatives,
            "accepted_str_subclass_equivalence_controls": subtypes,
            "partial_invalid_second_owner_rejections": partial_records,
            "first_valid_slot_None_after_original_validate_and_append": True,
            "invalid_second_slot_original_identity_and_value_unchanged": True,
            "default_partial_caller_unchanged": True,
            "original_owner_rejection_class_order_message_preserved": True,
            "original_protocol_controls_fixtures_and_caps_unchanged": True,
            "no_new_fixture_file_or_IO_created": True,
            "new_helper_qualification_created": False,
            "business_or_science_qualification_created": False}



def load_snapshot_control_Source(path, sha256, source_bytes):
    # New controller dependency is full-pinned before and after import/use.
    source = Path(path)
    before = source.lstat()
    identity_before = [before.st_dev, before.st_ino, before.st_mode, before.st_nlink,
                       before.st_size, before.st_mtime_ns, before.st_ctime_ns]
    if before.st_size != source_bytes or hashlib.sha256(source.read_bytes()).hexdigest() != sha256:
        raise ValueError('complete private snapshot controller SOURCE differs')
    spec = importlib.util.spec_from_file_location('actual_root_private_snapshot_metadata_controls', source)
    if spec is None or spec.loader is None:
        raise ValueError('private snapshot controller loader missing')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    after = source.lstat()
    if identity_before != [after.st_dev, after.st_ino, after.st_mode, after.st_nlink,
                          after.st_size, after.st_mtime_ns, after.st_ctime_ns]:
        raise ValueError('private snapshot controller SOURCE changed during import')
    return module, dict(path=str(source), sha256=sha256, size_bytes=source_bytes, identity=identity_before)


def run(output_dir):
    started = time.monotonic()

    def deadline(_signal, _frame):
        raise TimeoutError("fixed 60-second pure helper control deadline exceeded")

    signal.signal(signal.SIGALRM, deadline)
    signal.setitimer(signal.ITIMER_REAL, WALL_SECONDS)
    require(SOURCE_STATUS == 'READY_SOURCE_BOUND_BY_ROOT' and type(HELPER_PATH) is str
            and type(AUDIT_CONTROL_PATH) is str, 'UNREADY qualification templates require actual Root SOURCE binding')
    artifacts = Artifacts(output_dir)
    report = {"schema": "AXMAT_ROOT_BOUNDED_PURE_HELPER_CONTROLS_V16",
              "source_status": SOURCE_STATUS, "status": "ACTUAL_PURE_HELPER_CONTROLS_RUNNING",
              "actual_success_pins": None,
              "caps": {"wall_seconds": WALL_SECONDS, "rss_bytes": RSS_BYTES, "json_read_bytes": MAX_JSON_BYTES,
                       "output_bytes": MAX_OUTPUT_BYTES, "children": CHILD_LIMIT, "retries": RETRIES},
              "business_component_executed": False, "fresh_runtime_INPUT_qualified": False,
              "native_RSS_qualified": False, "AAA_accuracy_qualified": False, "ABA_admitted": False,
              "helper": {"path": HELPER_PATH, "sha256": HELPER_SHA256, "source_bytes": HELPER_SOURCE_BYTES},
              "parent_helper_sha256": PARENT_HELPER_SHA256, "stages": []}
    try:
        require(sys.dont_write_bytecode, "Root must run with -B or PYTHONDONTWRITEBYTECODE=1")
        helper_identity = identity(HELPER_PATH)
        require(helper_identity[4] == HELPER_SOURCE_BYTES and file_sha(HELPER_PATH) == HELPER_SHA256,
                "installed canonical helper differs from source-reviewed exact candidate")
        require(identity(HELPER_PATH) == helper_identity, "canonical helper changed during source pin")
        spec = importlib.util.spec_from_file_location("axmat_normal_canonical_pure_helper", HELPER_PATH)
        require(spec is not None and spec.loader is not None, "canonical helper loader unavailable")
        g = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(g)
        require(identity(HELPER_PATH) == helper_identity, "canonical helper changed during import")
        require(g.MAX_JSON_BYTES == MAX_JSON_BYTES and g.CHUNK_BYTES == 8388608,
                "canonical helper's original read limits changed")
        report["helper"]["identity"] = helper_identity
        audit_controls, audit_control_pin = load_snapshot_control_Source(AUDIT_CONTROL_PATH, AUDIT_CONTROL_SHA256, AUDIT_CONTROL_SOURCE_BYTES)
        report["private_snapshot_control_Source"] = audit_control_pin
        report["saved_input_identity_before"] = [dict(GRAPH_PIN), dict(TRACE_PIN)]
        for pin in (GRAPH_PIN, TRACE_PIN):
            pinned_identity(pin)

        def checkpoint(name):
            gc.collect()
            peak = current_peak_bytes()
            require(peak <= RSS_BYTES, "fixed 512MiB RSS cap exceeded at " + name)
            elapsed = time.monotonic() - started
            require(elapsed < WALL_SECONDS, "fixed wall cap exceeded at " + name)
            report["stages"].append({"stage": name, "elapsed_seconds": elapsed,
                                     "peak_rss_bytes": peak, "owned_output_bytes": sum(artifacts.sizes.values())})

        small_graph, fixture_result = fixture_controls(g, artifacts)
        checkpoint("real_small_fixture_producer_equivalence_and_rejections")
        report["small_fixture"] = {key: fixture_result[key] for key in
                                   ("producer_canonical_pin", "wire_content_sha256", "legacy_semantic_sha256",
                                    "canonical_files", "requirement_rows", "caller_full_value_and_mutable_identity_preserved",
                                    "accepted_str_subclass_equivalence_controls")}
        report["small_codecs"] = codec_controls(g, small_graph, artifacts)
        report["private_owner_consume_controls"] = private_owner_consume_controls(g, small_graph)
        fixture_path = artifacts.root / "fixture" / "0_code_environment.txt"
        report["private_inactive_audit_snapshot_controls"] = audit_controls.small_private_snapshot_controls(g, fixture_path, exact_value, WALL_SECONDS)
        audit_controls.validate_small_control_report(report["private_inactive_audit_snapshot_controls"])
        report["private_inactive_audit_snapshot_controls_order_preserved_artifact"] = artifacts.write_json("ACTUAL_PRIVATE_INACTIVE_AUDIT_SNAPSHOT_CONTROLS.json", report["private_inactive_audit_snapshot_controls"], encoder=ORDER_PRESERVING_JSON_ENCODER)
        del small_graph, fixture_result
        checkpoint("all_new_codecs_and_both_strict_entrances_small_controls")
        report["full_new_creation_trace"] = full_trace_controls(g, artifacts)
        checkpoint("full_63379_creation_trace_roundtrip_and_stored_size")
        report["full_old_saved_graph"] = full_graph_controls(g, artifacts, report["full_new_creation_trace"])
        checkpoint("full_old_saved_graph_codec_and_two_normal_strict_entrances")
        report["saved_input_bytes_identity_after"] = [complete_pin(GRAPH_PIN), complete_pin(TRACE_PIN)]
        require(identity(HELPER_PATH) == helper_identity and file_sha(HELPER_PATH) == HELPER_SHA256,
                "canonical helper bytes/identity changed")
        require(identity(AUDIT_CONTROL_PATH) == audit_control_pin["identity"] and file_sha(AUDIT_CONTROL_PATH) == AUDIT_CONTROL_SHA256, "complete private controller SOURCE changed")
        checkpoint("all_original_saved_metadata_bytes_identity_unchanged")
        report["status"] = "ACTUAL_PURE_HELPER_CONTROLS_PASS_NO_RUNTIME_OR_SCIENCE_ADMISSION"
        report["actual_success_pins"] = {
            "helper": dict(report["helper"]),
            "encoded_wholegraph": dict(report["full_old_saved_graph"]["stored_wholegraph"]),
            "encoded_new_trace": report["full_new_creation_trace"]["encoded_artifact"],
        }
    except BaseException as error:
        report["status"] = "ACTUAL_PURE_HELPER_CONTROLS_FAIL_NO_ADMISSION"
        report["failure"] = {"class": type(error).__name__, "message": str(error)}
        report["actual_success_pins"] = None
        report["elapsed_seconds"] = time.monotonic() - started
        report["peak_rss_bytes"] = current_peak_bytes()
        signal.setitimer(signal.ITIMER_REAL, 0)
        artifacts.write_json("ACTUAL_REPORT.json", report)
        raise
    report["elapsed_seconds"] = time.monotonic() - started
    report["peak_rss_bytes"] = current_peak_bytes()
    require(report["elapsed_seconds"] < WALL_SECONDS and report["peak_rss_bytes"] <= RSS_BYTES,
            "final actual caps exceeded")
    report_pin = artifacts.write_json("ACTUAL_REPORT.json", report)
    total_elapsed = time.monotonic() - started
    require(total_elapsed < WALL_SECONDS and current_peak_bytes() <= RSS_BYTES,
            "actual caps exceeded while writing final report")
    print(json.dumps({"status": report["status"], "report": report_pin,
                      "elapsed_seconds": total_elapsed, "peak_rss_bytes": current_peak_bytes()},
                     sort_keys=True, allow_nan=False))
    signal.setitimer(signal.ITIMER_REAL, 0)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True,
                        help="fresh private output directory provided by Root's sole bounded execution")
    args = parser.parse_args()
    run(args.output_dir)


if __name__ == "__main__":
    main()
