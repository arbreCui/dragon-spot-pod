"""Pure metadata selection for three conservative reference consumer scopes.

No import performs I/O.  This module imports neither a project API nor the graph
helper, and never hashes, opens, resolves or probes an input.  The caller must
supply the actual immutable full graph, its genuine normalized owners and the
explicit inventories returned by the retained source-owner implementations.

All three phases select the same conservative scientific input set.  This is a
source dependency plan, not a replay of the full-admission read trace, a fresh
byte check, a complete nine-category closure, or a scientific/resource/terminal
decision.  A consumer graph must still freshly read its complete selected bytes
and namespaces, check its actual aliases against the full parent's contract and
bind its actual current producer outputs separately after those producers run.
"""

from __future__ import annotations

import copy
import os
from collections.abc import Mapping


SCHEMA = "AXMAT_REFERENCE_CONSUMER_SOURCE_INPUT_PLAN_V1"
SCOPE = "CONSERVATIVE_SOURCE_DECLARED_CONSUMER_INPUT_SUBSET_ONLY"
PHASES = ("fine/physical", "AAA/project", "AAA/collect")
NEW_INPUT_ROLE = "NEWLY_DECLARED_INPUT_ONLY"
REQUIREMENT_COLUMNS = ("path", "canonical_path", "owner", "category", "binding_role")
REQUIREMENT_ROLES = ("EXPECTED_INPUT_BYTES", "OWNED_EXHAUSTIVE_NAMESPACE_BYTES",
                     "OWNED_EXHAUSTIVE_NAMESPACE_ALIAS_TARGET_BYTES", NEW_INPUT_ROLE)
CATEGORIES = ("code_environment", "production_prepared_layout", "completed_cold_case",
              "cache_build", "predecessor_builds", "preserved_history", "capture",
              "terminal_failure_proofs", "reference_scientific_dependencies")
REQUIREMENT_TABLE_SCHEMA = "AXMAT_REFERENCE_COMPLETE_TYPED_REQUIREMENT_TABLE_V1"
NAMESPACE_SCHEMA = "AXMAT_EXPLICIT_SEALED_INPUT_NAMESPACE_V1"
SCIENTIFIC_SCHEMA = "AXMAT_REFERENCE_SCIENTIFIC_INPUT_OWNERS_V1"


class ConsumerInputPlanError(ValueError):
    """The explicit source inventory cannot form a faithful parent subset."""


def _require(value, message):
    if not value:
        raise ConsumerInputPlanError(message)


def _path(value):
    _require(isinstance(value, str) and value and "\x00" not in value,
             "an input path must be a nonempty string")
    _require(os.path.isabs(value) and os.path.normpath(value) == value,
             "an input path must be absolute and normalized")
    return value


def _relative(value):
    _require(isinstance(value, str) and value and "\x00" not in value
             and not value.startswith("/") and "\\" not in value
             and os.path.normpath(value) == value
             and all(part not in ("", ".", "..") for part in value.split("/")),
             "a namespace member must be a normalized relative path")
    return value


def _label(value):
    _require(isinstance(value, str) and value.strip(), "a typed owner label is required")
    return value


def _sha(value):
    _require(isinstance(value, str) and len(value) == 64
             and all(char in "0123456789abcdef" for char in value),
             "a source-provided lowercase SHA256 is required")
    return value


def _category(value):
    _require(value in CATEGORIES, "an original typed owner category is required")
    return value


def _requirement_rows(value):
    """Iterate complete original edges, retaining their original row indexes."""
    if isinstance(value, list):
        for index, row in enumerate(value):
            _require(isinstance(row, Mapping) and set(row) == set(REQUIREMENT_COLUMNS),
                     "unexpected original logical requirement fields")
            fields = tuple(row[name] for name in REQUIREMENT_COLUMNS)
            _path(fields[0]); _path(fields[1]); _label(fields[2]); _category(fields[3])
            _require(fields[4] in REQUIREMENT_ROLES, "unknown original input role")
            yield index, fields
        return
    _require(isinstance(value, Mapping) and set(value) == {
        "schema", "columns", "paths", "owners", "categories", "binding_roles",
        "rows", "duplicate_edges_retained", "scope"}, "unexpected requirement table fields")
    _require(value["schema"] == REQUIREMENT_TABLE_SCHEMA
             and value["columns"] == list(REQUIREMENT_COLUMNS)
             and value["categories"] == list(CATEGORIES)
             and value["binding_roles"] == list(REQUIREMENT_ROLES)
             and value["duplicate_edges_retained"] is True
             and value["scope"] == "INPUT_ONLY_NO_SCIENCE_OR_RESOURCE_DECISION",
             "the complete parent requirement table contract changed")
    for field, validate in (("paths", _path), ("owners", _label)):
        pool = value[field]
        _require(isinstance(pool, list), "a requirement symbol pool must be a list")
        for symbol in pool:
            validate(symbol)
        _require(pool == sorted(set(pool)), "a requirement symbol pool must be sorted and unique")
    pools = (value["paths"], value["paths"], value["owners"], value["categories"], value["binding_roles"])
    _require(isinstance(value["rows"], list), "logical requirement rows must be a list")
    for index, row in enumerate(value["rows"]):
        _require(isinstance(row, list) and len(row) == len(pools)
                 and all(type(item) is int and 0 <= item < len(pool)
                         for item, pool in zip(row, pools)), "invalid parent requirement index")
        yield index, tuple(pool[item] for item, pool in zip(row, pools))


def _owner(value):
    _require(isinstance(value, Mapping) and set(value) in (
        {"owner", "category", "expected_files"},
        {"owner", "category", "expected_files", "newly_declared_input_paths"}),
        "genuine normalized source owners are required")
    _label(value["owner"]); _category(value["category"])
    _require(isinstance(value["expected_files"], Mapping), "expected files must be a source SHA map")
    for path, digest in value["expected_files"].items():
        _path(path); _sha(digest)
    if "newly_declared_input_paths" in value:
        paths = value["newly_declared_input_paths"]
        _require(isinstance(paths, list), "normalized owner new paths must be a list")
        for path in paths:
            _path(path)
        _require(paths == sorted(set(paths)), "normalized owner new paths must be sorted and unique")
    return value


def _namespace(value):
    _require(isinstance(value, Mapping) and set(value) == {
        "schema", "root", "canonical_root", "owner", "category", "files",
        "symlinks", "directories", "namespace_exhaustive"}
        and value["schema"] == NAMESPACE_SCHEMA and value["namespace_exhaustive"] is True,
        "a full explicit parent namespace is required")
    _path(value["root"]); _path(value["canonical_root"])
    _label(value["owner"]); _category(value["category"])
    _require(isinstance(value["files"], Mapping) and isinstance(value["symlinks"], Mapping),
             "namespace member maps are required")
    for name, digest in value["files"].items():
        _relative(name); _sha(digest)
    for name, alias in value["symlinks"].items():
        _relative(name)
        _require(isinstance(alias, Mapping) and set(alias) <= {"text", "target", "kind", "sha256"}
                 and {"text", "target", "kind"} <= set(alias), "invalid parent namespace alias")
        _label(alias["text"]); _path(alias["target"])
        _require(alias["kind"] in ("file", "directory"), "unsupported parent alias target")
        if "sha256" in alias:
            _require(alias["kind"] == "file", "a directory alias cannot supply regular bytes")
            _sha(alias["sha256"])
    _require(isinstance(value["directories"], list), "namespace directories must be a list")
    for directory in value["directories"]:
        _relative(directory)
    _require(len(value["directories"]) == len(set(value["directories"])),
             "duplicate namespace directory")
    return value


def consumer_input_plan(*, phase, full_graph, normalized_owners, scientific_inventory,
                        declaration_files, parsed_metadata_documents, production_runtime_root):
    """Return a conservative, source-evidenced subset without input I/O.

    ``declaration_files`` is the real absolute-path -> expected-SHA map for all
    original/generated declaration sources and binding dependencies.  Parsed
    metadata documents are the transitive inventory's explicit ``path`` entries;
    every entire JSON body is selected, without guessing from its contents.

    Stored new-input descriptors retain ``binding_role``.  Before passing them
    to the original graph constructor, the caller removes only that field; the
    constructor recreates the same INPUT_ONLY role.  Its freshly created new
    input pins must equal ``new_input_pins`` from the immutable full parent.
    ``selected_requirement_row_indexes`` refers to the original complete parent
    requirement representation, including duplicate rows.  It is source lineage,
    not a fabricated consumer execution trace or a replacement for fresh bytes.
    """
    _require(phase in PHASES, "unsupported source consumer phase")
    _require(isinstance(full_graph, Mapping)
             and full_graph.get("scope") == "INPUT_ONLY_NO_SCIENCE_OR_RESOURCE_DECISION"
             and full_graph.get("closure_categories") == list(CATEGORIES),
             "the complete original parent input graph is required")
    parent_digest = _sha(full_graph["content_sha256"])
    requirements = full_graph["requirements"]
    full_union, literal_to_canonical = set(), {}
    requirement_count = 0
    for index, row in _requirement_rows(requirements):
        literal, canonical = row[:2]
        previous = literal_to_canonical.get(literal)
        _require(previous is None or previous == canonical, "one parent literal has conflicting canonical identities")
        literal_to_canonical[literal] = canonical
        full_union.update((literal, canonical)); requirement_count += 1
    _require(isinstance(normalized_owners, list), "the actual normalized owner list is required")
    owners = [_owner(value) for value in normalized_owners]
    _require(isinstance(full_graph["namespaces"], list), "the original namespace list is required")
    namespaces = [_namespace(value) for value in full_graph["namespaces"]]
    new_inputs, new_pins = full_graph["newly_declared_input_paths"], full_graph["newly_declared_input_pins"]
    _require(isinstance(new_inputs, Mapping) and isinstance(new_pins, Mapping)
             and set(new_inputs) == set(new_pins), "complete original new-input bindings are required")
    for path, value in new_inputs.items():
        _path(path); _sha(new_pins[path])
        _require(isinstance(value, Mapping) and set(value) == {"owner", "category", "reason", "binding_role"}
                 and value["binding_role"] == NEW_INPUT_ROLE, "original new-input role changed")
        _label(value["owner"]); _category(value["category"]); _label(value["reason"])

    # Authority comes exclusively from explicitly typed source expected maps,
    # the parent's separately declared INPUT_ONLY pins, and namespace SHA maps.
    # canonical_files is never consulted for an expected digest.
    source_digests = {}
    def bind(path, digest):
        path, digest = _path(path), _sha(digest)
        _require(path in full_union, "source binding is outside the complete parent input union")
        old = source_digests.get(path)
        _require(old is None or old == digest, "conflicting source-provided input digests")
        source_digests[path] = digest
    for owner in owners:
        for path, digest in owner["expected_files"].items():
            bind(path, digest)
        for path in owner.get("newly_declared_input_paths", []):
            _require(path in new_inputs, "owner new role lost its original explicit parent binding")
    for path, digest in new_pins.items():
        bind(path, digest)
    for namespace in namespaces:
        for name, digest in namespace["files"].items():
            bind(os.path.join(namespace["root"], name), digest)
        for name, alias in namespace["symlinks"].items():
            if alias["kind"] == "file" and "sha256" in alias:
                bind(os.path.join(namespace["root"], name), alias["sha256"])
                bind(alias["target"], alias["sha256"])
    canonical_source_digests = {}
    for literal, digest in source_digests.items():
        canonical = literal_to_canonical.get(literal, literal)
        _require(canonical in full_union, "source literal lost its original canonical relation")
        old = canonical_source_digests.get(canonical)
        _require(old is None or old == digest, "conflicting original source identities at one canonical target")
        canonical_source_digests[canonical] = digest

    _require(isinstance(scientific_inventory, Mapping)
             and scientific_inventory.get("schema") == SCIENTIFIC_SCHEMA,
             "the explicit retained scientific input inventory is required")
    records = scientific_inventory["input_records"]
    _require(isinstance(records, list) and records, "all original scientific input records are required")
    future = scientific_inventory.get("fresh_analysis_output_requirements", [])
    _require(isinstance(future, list), "future producer outputs must remain a separate inventory")
    future_paths = {_path(item["path"]) for item in future}
    selected = set()
    def pick(path, expected=None):
        path = _path(path)
        _require(path in full_union, "picked input is outside the complete parent input union")
        _require(path not in future_paths, "a future producer output is not an immutable input")
        canonical = literal_to_canonical.get(path, path)
        digest = source_digests.get(path, canonical_source_digests.get(canonical))
        _require(digest is not None, "picked input has no source-authoritative expected or INPUT_ONLY binding")
        if expected is not None:
            _require(digest == _sha(expected), "picked input differs from its explicit source expectation")
        selected.add(path)
    scientific_paths = set()
    for record in records:
        _require(isinstance(record, Mapping) and "path" in record, "an explicit scientific input record is required")
        path = _path(record["path"])
        _require(path not in scientific_paths, "duplicate scientific input record")
        scientific_paths.add(path); pick(path, record.get("expected_sha256"))
    for owner in owners:
        if owner["category"] == "code_environment":
            for path, digest in owner["expected_files"].items():
                pick(path, digest)
            for path in owner.get("newly_declared_input_paths", []):
                pick(path)
    for path, value in new_inputs.items():
        if value["category"] == "code_environment":
            pick(path)
    _require(isinstance(declaration_files, Mapping), "all declaration sources need an explicit SHA map")
    for path, digest in declaration_files.items():
        pick(path, digest)
    _require(isinstance(parsed_metadata_documents, list), "all parsed metadata document records are required")
    metadata_paths = []
    for metadata in parsed_metadata_documents:
        _require(isinstance(metadata, Mapping) and "path" in metadata, "a parsed document needs its explicit path")
        path = _path(metadata["path"]); pick(path, metadata.get("expected_sha256")); metadata_paths.append(path)

    specs = scientific_inventory["namespace_requirements"]
    _require(isinstance(specs, list), "all scientific namespace requirements are required")
    scientific_roots = {_path(spec["root"]) for spec in specs}
    runtime_root = _path(production_runtime_root)
    parent_roots = {namespace["root"] for namespace in namespaces}
    _require(scientific_roots | {runtime_root} <= parent_roots,
             "scientific/runtime namespace has no exact complete parent namespace")
    chosen_roots = scientific_roots | {runtime_root} | {
        namespace["root"] for namespace in namespaces if namespace["category"] == "code_environment"}
    # A selected root preserves every original descriptor at that same root,
    # including different owners/categories and duplicate descriptor instances.
    chosen_namespaces = [namespace for namespace in namespaces if namespace["root"] in chosen_roots]
    for namespace in chosen_namespaces:
        for name, digest in namespace["files"].items():
            pick(os.path.join(namespace["root"], name), digest)
        for name, alias in namespace["symlinks"].items():
            if alias["kind"] == "file":
                pick(os.path.join(namespace["root"], name), alias.get("sha256"))
                pick(alias["target"], alias.get("sha256"))
    # Include only targets named by the full parent's literal->canonical mapping;
    # do not resolve inputs or infer aliases/expected bytes from observations.
    pending = list(selected)
    while pending:
        target = literal_to_canonical.get(pending.pop())
        if target is not None and target not in selected:
            pick(target); pending.append(target)

    subset_owners = []
    for owner in owners:
        expected = {path: digest for path, digest in owner["expected_files"].items() if path in selected}
        paths = [path for path in owner.get("newly_declared_input_paths", []) if path in selected]
        if expected or paths or owner["category"] == "code_environment":
            item = {"owner": owner["owner"], "category": owner["category"], "expected_files": expected}
            if "newly_declared_input_paths" in owner:
                item["newly_declared_input_paths"] = paths
            subset_owners.append(item)
    subset_new = {path: copy.deepcopy(value) for path, value in new_inputs.items() if path in selected}
    selected_indexes = [index for index, row in _requirement_rows(requirements) if row[0] in selected]
    canonical_paths = {literal_to_canonical.get(path, path) for path in selected}
    observed_sizes = {}
    _require(isinstance(full_graph["canonical_files"], list), "saved canonical size metadata is required")
    for observed in full_graph["canonical_files"]:
        _require(isinstance(observed, Mapping), "invalid saved canonical size metadata")
        path, size = _path(observed["path"]), observed["size_bytes"]
        _require(type(size) is int and size >= 0 and path not in observed_sizes,
                 "invalid or duplicate saved canonical size metadata")
        observed_sizes[path] = size
    _require(canonical_paths <= set(observed_sizes), "a selected canonical target lacks saved size metadata")
    return {
        "schema": SCHEMA, "scope": SCOPE, "phase": phase,
        "owners": subset_owners, "newly_declared_input_paths": subset_new,
        "new_input_pins": {path: new_pins[path] for path in subset_new},
        "namespaces": copy.deepcopy(chosen_namespaces), "selected_paths": sorted(selected),
        "selected_canonical_paths": sorted(canonical_paths),
        "selected_requirement_row_indexes": selected_indexes,
        "requirement_lineage": {"parent_content_sha256": parent_digest,
            "parent_ref": "full_graph.requirements", "columns": list(REQUIREMENT_COLUMNS),
            "representation": "complete_original_expanded_rows" if isinstance(requirements, list)
                              else REQUIREMENT_TABLE_SCHEMA,
            "row_indexes_retain_all_original_selected_literal_owner_category_role_duplicates": True},
        "scope_source_predicates": {
            "scientific_inputs": "All scientific_inventory.input_records; future outputs are separate and forbidden",
            "code_environment": "Every normalized code_environment expected/new edge and every parent code_environment new-input path",
            "declaration_sources": "Every exact declaration_files absolute path and expected SHA",
            "metadata_bodies": "Every parsed_metadata_documents explicit path, entire body without field filtering",
            "namespaces": "All code_environment roots, exact scientific requirement roots and exact production runtime root; all parent descriptors at each chosen root",
            "canonical_targets": "Full parent literal-to-canonical relations only; preserve existing original owners/new roles, create no target owner",
            "aliases": "Caller captures actual needed aliases and compares every entry with the immutable full-parent alias contract",
            "selection_basis": "Conservative complete scientific/source contract; no observed trace or filename/suffix/native-kind inference",
            "execution_scope": "Input source plan only; consumer/science execution traces are not declared by this helper"},
        "counts": {"selected_literal_and_canonical_paths": len(selected),
            "selected_unique_canonical_regular_files": len(canonical_paths),
            "saved_metadata_canonical_bytes": sum(observed_sizes[path] for path in canonical_paths),
            "bytes_scope": "FULL_PARENT_SAVED_SIZE_METADATA_ONLY_NOT_A_FRESH_BYTE_READ",
            "selected_normalized_owner_descriptors": len(subset_owners),
            "selected_expected_owner_edges": sum(len(owner["expected_files"]) for owner in subset_owners),
            "selected_owner_new_role_edges": sum(len(owner.get("newly_declared_input_paths", [])) for owner in subset_owners),
            "selected_parent_new_inputs": len(subset_new), "selected_namespace_descriptors": len(chosen_namespaces),
            "selected_namespace_roots": len(chosen_roots), "scientific_input_records": len(records),
            "parsed_metadata_document_records": len(metadata_paths), "declaration_source_paths": len(declaration_files),
            "selected_original_requirement_rows": len(selected_indexes), "full_parent_requirement_rows": requirement_count},
        "limits": "No input I/O or verification. Not a full nine-category recheck, a live resource/terminal decision, a scientific result or a qualification. Fresh consumer bytes/namespaces/aliases and actual new producer outputs remain mandatory.",
    }
