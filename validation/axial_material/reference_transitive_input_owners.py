"""Typed, read-only dependency ownership for one verified-input declaration.

The caller supplies the genuine full-ready semantic snapshot and explicit root
pins. This helper follows descriptor objects and documented manifest fields;
it never guesses that an arbitrary string is a path. It reads JSON metadata,
but never hashes files, invokes a project API, evaluates scientific fields,
scans directories, or creates outputs. No scientific or resource PASS results.

Root seed forms: [{path, sha256, owner, category, kind?, relative_root?}] or
{absolute_path: {sha256, owner, category, kind?, relative_root?}}. Kind is json,
file, or pin (JSON pins are traversed by suffix). An unpinned root needs an
explicit reason and is returned as NEWLY_DECLARED_INPUT_ONLY. Namespace specs
are requirements, not actual observations. An old exhaustive files/links map
still needs fresh directory membership; unknown bytes need caller's new pins.
"""

from __future__ import annotations

import ast
from collections import deque
import json
import os
from pathlib import Path
import re


SCHEMA = "AXMAT_REFERENCE_TRANSITIVE_INPUT_OWNERS_V1"
CLOSURE_CATEGORIES = (
    "code_environment", "production_prepared_layout", "completed_cold_case",
    "cache_build", "predecessor_builds", "preserved_history", "capture",
    "terminal_failure_proofs", "reference_scientific_dependencies",
)
HASH_MAP_FIELDS = frozenset((
    "files", "outputs", "local_files", "sha256", "control_files",
    "input_sha256", "input_identities", "source_inputs", "all_stage_logs",
))
MAX_JSON_BYTES = 64 * 2**20
# These frozen saved-reference factories write AAA/analysis_result.json but
# expressly construct outputs with path.relative_to(OUT). The older serial CE
# collectors instead write path.name relative to their AAA case directory.
OUT_RELATIVE_AAA_ANALYSIS_FAMILIES = frozenset((
    "axial-material-qualified-AAA-white-trace-refined-reference-20261005",
    "axial-material-qualified-AAA-white-trace-refined-reference-hostpath-20261005",
    "axial-material-qualified-AAA-source-factor-reference-20261006",
    "axial-material-qualified-AAA-moment-order-reference-20261006",
    "axial-material-qualified-AAA-rank1-factor-cache-reference-20261007",
    "axial-material-qualified-AAA-rank1-input-graph-reference-20261007",
))


def _path(value):
    if not isinstance(value, (str, Path)):
        raise ValueError("typed input path must be an absolute string or Path")
    path = Path(value)
    if not path.is_absolute() or ".." in path.parts:
        raise ValueError("typed input path must be absolute without parent traversal")
    return str(path)


def _sha(value):
    if not isinstance(value, str) or re.fullmatch(r"[0-9a-f]{64}", value) is None:
        raise ValueError("typed input expected hash must be SHA256")
    return value


def _relative(value):
    if not isinstance(value, str) or not value:
        raise ValueError("typed manifest member must be a nonempty relative string")
    path = Path(value)
    if path.is_absolute() or ".." in path.parts or str(path) != value or value in (".", ".."):
        raise ValueError("typed manifest relative member escapes its explicit root")
    return value


def _category(value):
    if value not in CLOSURE_CATEGORIES:
        raise ValueError("unknown exact transitive closure category: " + repr(value))
    return value


def _label(value):
    if not isinstance(value, str) or not value:
        raise ValueError("typed input owner/reason must be a nonempty string")
    return value


def _object(value, owner):
    if type(value) is not dict:
        raise ValueError("typed manifest object missing: " + owner)
    return value


def _read(path):
    def unique(pairs):
        out = {}
        for name, item in pairs:
            if name in out:
                raise ValueError("duplicate metadata JSON field in " + str(path))
            out[name] = item
        return out
    def nonfinite(value):
        raise ValueError("nonfinite metadata JSON constant in " + str(path) + ": " + value)
    with Path(path).open("rb") as stream:
        raw = stream.read(MAX_JSON_BYTES + 1)
    if len(raw) > MAX_JSON_BYTES:
        raise ValueError("explicit input metadata exceeds its read-only size bound")
    return json.loads(raw, object_pairs_hook=unique, parse_constant=nonfinite)


def _graph_categories():
    """Read the graph's literal category contract, without importing its code."""
    path = Path(__file__).with_name("reference_verified_input_graph.py")
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    values = [node.value for node in tree.body if isinstance(node, ast.Assign)
              and any(isinstance(target, ast.Name) and target.id == "CLOSURE_CATEGORIES"
                      for target in node.targets)]
    if len(values) != 1 or tuple(ast.literal_eval(values[0])) != CLOSURE_CATEGORIES:
        raise ValueError("actual graph closure category contract differs")
    return str(path.absolute())


class _Inputs:
    def __init__(self, art, prod, build):
        self.art, self.prod, self.build = Path(art), Path(prod), Path(build)
        self.art_text, self.prod_text, self.build_text = str(self.art), str(self.prod), str(self.build)
        self.files, self.groups, self.new, self.aliases = {}, {}, {}, {}
        self.namespaces, self.queue, self.queued, self.parsed = [], deque(), set(), set()
        self.documents = []
        self.historical_observations = []
        self.historical_namespace_observations = []
        self.history_documents = {}
        self.explicit_json = set()
        self.known_roots = {str(self.prod), str(self.build)}

    def classify(self, path, fallback):
        # All real callers already pass _path-normalized paths. Preserve the
        # former Path normalization for direct callers without repeatedly
        # constructing Path parents/is_relative_to tuples on every edge.
        path = str(path)
        if "//" in path or "/./" in path or path.endswith(("/", "/.")):
            path = str(Path(path))
        def within(root):
            return path == root or path.startswith(root + "/")
        if path in (self.prod_text + "/prepared.json", self.prod_text + "/declaration.json") or (
                within(self.prod_text + "/runtime") or within(self.prod_text + "/decks")):
            return "production_prepared_layout"
        if within(self.prod_text):
            return "completed_cold_case"
        if within(self.build_text):
            return "cache_build"
        inside_art = within(self.art_text)
        if inside_art:
            relative = path[len(self.art_text):].lstrip("/")
            name = relative.split("/", 1)[0]
            if name == "axial-material-AAA-production-angular-capture-20261006":
                return "capture"
            if name in ("axial-material-moment-order-build-20261006", "axial-material-source-factor-build-20261006"):
                return "predecessor_builds"
            if name.startswith("axial-material-qualified-AB-") and "build-admission" in name:
                return "cache_build" if "rank1-factor-cache" in name else "predecessor_builds"
            if name == "axial-material-production-qualified-AB-moment-order-20261006" or (
                    name.startswith("axial-material-qualified-AAA-moment-order-production-terminal-")):
                return "terminal_failure_proofs"
            if "reference-terminal" in name or "production-terminal" in name or "build-terminal" in name:
                return fallback
            if "ce-" in name or "observables" in name or "reference" in name or name == "axial-material-tools-20261003":
                return "reference_scientific_dependencies"
            if "cold" in name or "angular-convergence" in name or "angular-closeout" in name:
                return "production_prepared_layout"
        suffixes = (".py", ".f", ".f90", ".so", ".dylib", ".a", ".mod")
        leaf = path.rsplit("/", 1)[-1]
        if (leaf not in suffixes and leaf.endswith(suffixes)) or not inside_art:
            return "code_environment"
        return _category(fallback)

    def add(self, path, sha, owner, category, *, relative_root=None, new_reason=None):
        path, owner, category = _path(path), _label(owner), _category(category)
        group = self.groups.setdefault((owner, category), {})
        if sha is None:
            reason = _label(new_reason)
            if path not in self.files:
                prior = self.new.get(path)
                if prior is None:
                    self.new[path] = dict(owner=owner, category=category, reason=reason)
        else:
            sha = _sha(sha)
            if path in self.files and self.files[path] != sha:
                raise ValueError("conflicting expected hashes for one typed input: " + path)
            self.files[path] = sha
            group[path] = sha
            self.new.pop(path, None)
        # Library package fixture JSON remains owned bytes, not a project
        # manifest schema. Only ART evidence or explicitly seeded JSON is read.
        metadata = path in self.explicit_json or (
            Path(path).suffix == ".json" and Path(path).is_relative_to(self.art))
        if metadata and path not in self.queued:
            self.queue.append((path, category, _path(relative_root) if relative_root is not None else None))
            self.queued.add(path)

    def descriptor(self, item, owner, category, *, relative_root=None):
        item = _object(item, owner)
        path = _path(item["path"])
        category = self.classify(path, category)
        self.add(path, item["sha256"], owner, category, relative_root=relative_root)

    def hashes(self, values, owner, category, *, root=None):
        values = _object(values, owner)
        if not values:
            return {}
        absolute = [Path(name).is_absolute() if isinstance(name, str) else False for name in values]
        if any(absolute) and not all(absolute):
            raise ValueError("mixed absolute/relative typed hash manifest: " + owner)
        result = {}
        for name, sha in values.items():
            if all(absolute):
                path = _path(name)
            else:
                if root is None:
                    raise ValueError("relative typed hash manifest lacks an explicit root: " + owner)
                member = _relative(name)
                path = _path(Path(root) / member)
                result[member] = _sha(sha)
            assigned = category if category == "preserved_history" else self.classify(path, category)
            self.add(path, sha, owner, assigned, relative_root=root)
        return result

    def namespace(self, root, files, links, owner, category, coverage, document):
        root = _path(root)
        self.known_roots.add(root)
        self.namespaces.append(dict(root=root, owner=_label(owner), category=_category(category),
            files=dict(files), symlinks={name: value["text"] for name, value in links.items()}, metadata_source=document,
            old_manifest_coverage=coverage, namespace_exhaustive=False,
            manifest_is_namespace_exhaustive=coverage.startswith("EXACT_OLD_REGULAR_AND_LITERAL_SYMLINK_MAP"),
            full_actual_namespace_snapshot_required=True,
            directory_membership_must_be_newly_declared=True,
            unknown_regular_members_require_explicit_new_input_only_pin=True,
            namespace_and_aliases_must_be_fresh_at_each_checkpoint=True))

    def literal_links(self, root, values, owner, category):
        values = _object(values, owner)
        links = {}
        for name, text in values.items():
            name = _relative(name)
            if not isinstance(text, str) or not text:
                raise ValueError("an old inventory link needs its exact literal text")
            path = _path(Path(root) / name)
            target = _path(os.path.normpath(text if os.path.isabs(text) else os.path.join(Path(path).parent, text)))
            entry = dict(path=path, text=text, lexical_target=target, owner=owner,
                         category=category, actual_canonical_target_capture_required=True)
            old = self.aliases.get(path, {})
            if "text" in old and old["text"] != text:
                raise ValueError("conflicting expected literal alias text: " + path)
            self.aliases[path] = dict(old, **entry)
            links[name] = dict(text=text, lexical_target=target,
                               actual_canonical_target_capture_required=True)
        return links

    def inventory(self, root, inventory, owner, category, document):
        root = _path(root)
        inventory = _object(inventory, owner)
        files = self.hashes(inventory["files"], owner + ".files", category, root=root)
        links = self.literal_links(root, inventory["symlinks"], owner + ".symlinks", category)
        if set(files) & set(links):
            raise ValueError("old inventory lists one member as both regular file and alias")
        self.namespace(root, files, links, owner, category,
                       "EXACT_OLD_REGULAR_AND_LITERAL_SYMLINK_MAP; directories were not inventoried", document)

    def relative_context(self, document, supplied):
        if supplied is not None:
            return supplied
        candidates = [root for root in self.known_roots if Path(document).is_relative_to(root)]
        return max(candidates, key=len) if candidates else str(Path(document).parent)

    def manifest_root(self, key, document, context, value):
        """Resolve documented manifest layouts, not arbitrary parent guesses."""
        if document.startswith("snapshot:"):
            return context
        path = Path(document)
        parent = str(path.parent)
        if key == "control_files" and path.name == "guard_controls.json":
            # FULL prepare() and capture guard_proof() both join these names
            # to the guard_controls.json directory, not their outer OUT.
            return parent
        if (key == "outputs" and path.name == "run_status.json"
                and path.parent in (
                    self.art / "axial-material-AAA-compensated-flight-20261004",
                    self.art / "axial-material-AAA-inner-terminal-capture-20261004")):
            # run_AAA_compensated_flight/run_AAA_inner_terminal_capture seal
            # names from work/AAA, and their later production consumers join
            # those entries to candidate/AAA.
            return str(path.parent / "AAA")
        if (key == "outputs" and path.name == "run_status.json"
                and path.parent.parent == self.art and path.parent.name.startswith("axial-material-r64-")):
            if value.get("mode") in ("first_call_probe", "snapshot_A"):
                # run_r64_snapshot_experiment writes work/A names.
                return str(path.parent / "A")
            if value.get("state") in ("A", "B") and "snapshot_qualified" in value:
                # run_r64_material_snapshot writes work/state names; state is
                # recorded explicitly in its immutable result metadata.
                return str(path.parent / value["state"])
        if key == "outputs" and path.name in ("analysis_result.json", "publication_failure.json"):
            if path.is_relative_to(self.art):
                relative = path.relative_to(self.art)
                if relative.parts[0] in OUT_RELATIVE_AAA_ANALYSIS_FAMILIES:
                    if relative.parts[1:] != ("AAA", path.name):
                        raise ValueError("known OUT-relative analysis result has an unexpected layout")
                    return str(self.art / relative.parts[0])
            # Original native CE serial collectors write each path.name.
            return parent
        if key in ("local_files", "outputs", "sha256"):
            # prepared.local_files, native_result.outputs, exporter outputs,
            # and a flat result.sha256 JSON all use their document directory.
            return parent
        if key == "files" and path.name in ("seal.json", "source_inventory.json", "factory_seal.json"):
            return parent
        if key == "files" and path.name == "build_identity.json" and path.parent.name == "runtime":
            # Capture/SOURCEFACTOR/MOM/CACHE write relative_to(OUT), while
            # their identity receipt itself lives in OUT/runtime.
            return str(path.parent.parent)
        return context

    def input_reuse_files(self, values, owner, category, classification):
        """Explicit CE reuse receipt variants; no permissive dict fallback."""
        for path, entry in _object(values, owner).items():
            path = _path(path)
            entry = _object(entry, owner + "/target")
            if set(entry) != {"sha256", "source"}:
                raise ValueError("independent physical input reuse entry has an unexpected schema")
            self.add(path, entry["sha256"], owner + "/target", self.classify(path, category))
            if classification == "IDENTICAL_UNRUN_PHYSICAL_CE_INPUTS_FOR_SEPARATE_RANK1_DIAGNOSIS":
                source = _path(entry["source"])
                self.add(source, None, owner + "/source", self.classify(source, category),
                    new_reason="Explicit legacy reuse source path has no independent source SHA descriptor; caller must pin it as input-only unless already owned")
            else:
                source = _object(entry["source"], owner + "/source")
                if set(source) != {"path", "sha256"}:
                    raise ValueError("independent physical input reuse source is not an exact descriptor")
                self.descriptor(source, owner + "/source", category)

    def walk(self, value, document, category, pointer="", context=None):
        if isinstance(value, list):
            for index, item in enumerate(value):
                self.walk(item, document, category, pointer + "/" + str(index), context)
            return
        if not isinstance(value, dict):
            return
        if pointer == "" and not document.startswith("snapshot:"):
            relative = document[len(self.art_text) + 1:] if document.startswith(self.art_text + "/") else ""
            if relative in self.history_document_names():
                self.history_documents[document] = value
        owner = document + "#" + (pointer or "/")
        if "path" in value and "sha256" in value and isinstance(value["sha256"], str):
            self.descriptor(value, owner, category)
        handled = set()
        if (pointer == ""
                and document == str(Path(self.art) / "axial-material-native-review-20261003/rank1_sensitivity_protocol_review.json")
                and value.get("classification") == "PASS_PROTOCOL_REVIEW_ONLY"
                and value.get("transport_executed_by_reviewer") is False):
            identities = _object(value.get("identities"), owner + "/identities")
            observed = _object(identities.get("production_input_generator"),
                               owner + "/identities/production_input_generator")
            original_path = str(Path(self.art).parent / "axial_material/production_inputs.py")
            if set(observed) != {"path", "sha256"} or _path(observed["path"]) != original_path:
                raise ValueError("historical protocol generator observation changed its exact field or path")
            observed = dict(path=original_path, sha256=_sha(observed["sha256"]))
            # The current controller verifies its prepared local generator,
            # never this review's 20261003 source-version observation. Retain
            # the whole review JSON pin and every other identity edge; only
            # this specifically authorized historical endpoint is not promoted
            # into a current source-byte requirement or a scientific PASS.
            self.historical_observations.append(dict(document=document,
                owner=owner + "/identities/production_input_generator",
                classification=value["classification"],
                transport_executed_by_reviewer=False, observed_descriptor=observed,
                current_dependency_endpoints=False, scientific_PASS_inherited=False,
                scope="Pinned historical protocol-review JSON retains the original generator version; actual prepared-generator and scientific input owners remain required"))
            for label, entry in identities.items():
                if label != "production_input_generator":
                    self.walk(entry, document, category, "/identities/" + label, context)
            handled.add("identities")
        if "preserved_predecessors" in value:
            entries = value["preserved_predecessors"]
            if not isinstance(entries, list):
                raise ValueError("typed preserved_predecessors must be a list")
            for index, entry in enumerate(entries):
                entry = _object(entry, owner + ".preserved_predecessors")
                self.inventory(entry["root"], entry["inventory"],
                    owner + "/preserved_predecessors/" + str(index), "preserved_history", document)
            handled.add("preserved_predecessors")
        if "source_inventory" in value:
            root = value.get("source_root")
            if root is None:
                raise ValueError("embedded source_inventory needs its explicit source_root")
            self.inventory(root, value["source_inventory"], owner + "/source_inventory", category, document)
            handled.add("source_inventory")
        if "failed_predecessor_files" in value:
            root = _path(value["failed_predecessor_root"])
            members = self.hashes(value["failed_predecessor_files"], owner + "/failed_predecessor_files",
                                  "terminal_failure_proofs", root=root)
            self.namespace(root, members, {}, owner + "/failed_predecessor_files",
                "terminal_failure_proofs", "OLD_FAILED_REGULAR_MAP; no success claimed", document)
            handled.add("failed_predecessor_files")
        if "native_library_aliases" in value:
            for path, target in _object(value["native_library_aliases"], owner + ".native_library_aliases").items():
                path, target = _path(path), _path(target)
                entry = dict(path=path, expected_resolved_target=target, owner=owner + "/native_library_aliases",
                             category="code_environment", actual_literal_link_text_capture_required=True)
                if path in self.aliases and self.aliases[path].get("expected_resolved_target", target) != target:
                    raise ValueError("conflicting native resolved-alias contract")
                self.aliases.setdefault(path, entry)
            handled.add("native_library_aliases")

        # Explicit composite root/hash contracts supplement descriptor objects.
        for root_key, seal_key, decl_key, fixed_category in (
            ("build_root", "build_seal_sha256", None, None),
            ("root", "seal_sha256", "declaration_sha256", None),
            ("full_root", "full_seal_sha256", "full_declaration_sha256", "production_prepared_layout"),
            ("angular_root", "angular_seal_sha256", None, "production_prepared_layout"),
            ("failed_predecessor_root", None, "failed_predecessor_declaration_sha256", "terminal_failure_proofs"),
        ):
            if root_key in value and ((seal_key is not None and seal_key in value) or
                                      (decl_key is not None and decl_key in value)):
                root = _path(value[root_key])
                assigned = fixed_category or self.classify(root, category)
                self.known_roots.add(root)
                for key, filename in ((seal_key, "seal.json"), (decl_key, "declaration.json")):
                    if key is not None and key in value:
                        self.add(Path(root) / filename, value[key], owner + "/" + key,
                                 assigned, relative_root=root)

        for key, item in value.items():
            if key in handled:
                continue
            if key in HASH_MAP_FIELDS and isinstance(item, dict):
                if key == "sha256" and "path" in value:
                    continue
                if (key == "files" and Path(document).name == "input_reuse_receipt.json"
                        and value.get("classification") in (
                            "IDENTICAL_INDEPENDENT_PHYSICAL_XML_AND_CONTRACT_REUSED",
                            "IDENTICAL_UNRUN_PHYSICAL_CE_INPUTS_FOR_SEPARATE_RANK1_DIAGNOSIS")):
                    self.input_reuse_files(item, owner + "/files", category, value["classification"])
                    continue
                if (key == "files" and Path(document).name == "compatible_snapshot_stopped_receipt.json"
                        and value.get("classification") == "STOPPED_BEFORE_ANY_VALID_NEW_SNAPSHOT"):
                    stopped = {}
                    for name, entry in item.items():
                        entry = _object(entry, owner + "/files")
                        if (set(entry) != {"bytes", "sha256"} or type(entry["bytes"]) is not int
                                or entry["bytes"] < 0):
                            raise ValueError("stopped snapshot byte inventory has an unexpected schema")
                        stopped[_relative(name)] = _sha(entry["sha256"])
                    # case_spec_rank1_moc_precision names this as historical
                    # remaining_budget_evidence. Frozen verify_prepared pins
                    # case_spec and check_protocol reads physical controls/caps;
                    # neither verifies this historical observation's members.
                    self.historical_observations.append(dict(document=document,
                        owner=owner + "/files", classification=value["classification"],
                        observation_root=str(Path(document).parent), files=stopped,
                        observed_bytes={name: entry["bytes"] for name, entry in item.items()},
                        current_dependency_endpoints=False, scientific_PASS_inherited=False,
                        scope="The pinned JSON contains an old stopped-state observation; actual read-trace dependencies must still be explicitly owned"))
                    continue
                if (key == "files" and Path(document).name == "result.json"
                        and Path(document).parent.name == "sum_test"
                        and value.get("classification") == "PASS_SUBULP_ACCUMULATION_NUMERICAL_TEST"):
                    # prepare_qualified_AB_compensated_production reads only
                    # this receipt's classification and pins its complete JSON.
                    # Its observed files even include a pre-write empty self
                    # hash; that observation is not a current file dependency.
                    observed = {_relative(name): _sha(sha) for name, sha in item.items()}
                    self.historical_observations.append(dict(document=document,
                        owner=owner + "/files", classification=value["classification"],
                        observation_root=str(Path(document).parent), files=observed,
                        current_dependency_endpoints=False, scientific_PASS_inherited=False,
                        scope="Pinned original accumulation-test JSON only; its creation-time file observations are not promoted into current dependencies or scientific qualification"))
                    continue
                if (key == "files" and Path(document).name.endswith(".receipt.json")
                        and set(value) == {"root", "files"}):
                    # Frozen layered reference/math/model receipt() explicitly
                    # writes {root: stage_folder, files: relative_to(folder)}.
                    root = _path(value["root"])
                    self.known_roots.add(root)
                    members = self.hashes(item, owner + "/files", category, root=root)
                    self.namespace(root, members, {}, owner + "/files", category,
                        "STAGE_RECEIPT_EXPECTED_REGULAR_MAP; actual namespace still needs fresh observation", document)
                    continue
                if (key == "files" and Path(document).name == "raw_binary_receipt.json"
                        and set(value) == {"files", "before_binary_gates"}
                        and type(value["before_binary_gates"]) is bool):
                    # Cache binary_audit() labels raw disassembly descriptors;
                    # these keys are roles, not relative filenames.
                    for label, entry in item.items():
                        _label(label)
                        entry = _object(entry, owner + "/files/" + label)
                        if set(entry) != {"path", "sha256"}:
                            raise ValueError("raw binary receipt member is not an exact descriptor")
                        self.descriptor(entry, owner + "/files/" + label, category)
                    continue
                relative_document = (Path(document).relative_to(self.art).parts
                    if not document.startswith("snapshot:") and Path(document).is_relative_to(self.art) else ())
                if (key == "files" and len(relative_document) == 4
                        and relative_document[0] == "axial-material-AAA-white-trace-refined-layered-full-20261005"
                        and relative_document[1] == "receipts" and relative_document[2] in ("primary", "replay")
                        and re.fullmatch(r"p[0-3]_h20_n4_b[0-9]{5}\.json", relative_document[3])):
                    # FULL check_receipt() verifies both primary and replay
                    # metadata against the primary scientific archive. Replay
                    # is a fresh byte comparison, not a second output folder.
                    entries = {}
                    for name, entry in item.items():
                        entry = _object(entry, owner + "/files")
                        if (set(entry) != {"bytes", "sha256"} or type(entry["bytes"]) is not int
                                or entry["bytes"] < 0):
                            raise ValueError("FULL scientific batch receipt has an unexpected schema")
                        entries[_relative(name)] = _sha(entry["sha256"])
                    batch_root = self.art / relative_document[0] / "primary" / Path(document).stem
                    members = self.hashes(entries, owner + "/files", category, root=str(batch_root))
                    self.namespace(batch_root, members, {}, owner + "/files", category,
                        "FULL_BATCH_EXPECTED_REGULAR_MAP; primary and replay verify this same primary archive", document)
                    continue
                parent = str(Path(document).parent) if not document.startswith("snapshot:") else context
                root = self.manifest_root(key, document, context, value)
                members = self.hashes(item, owner + "/" + key, category, root=root)
                if key == "files" and Path(document).name == "seal.json":
                    manifest_files = dict(members)
                    if document in self.files:
                        manifest_files["seal.json"] = self.files[document]
                    self.namespace(parent, manifest_files, {}, owner + "/files", category,
                        "SEALED_EXPECTED_REGULAR_MAP; actual namespace still needs fresh observation", document)
                elif key == "files" and Path(document).name == "source_inventory.json":
                    links = self.literal_links(parent, value.get("symlinks", {}), owner + "/symlinks", category)
                    self.namespace(parent, members, links, owner, category,
                        "SOURCE_INVENTORY_EXPECTED_MAP; directories require fresh declaration", document)
                    handled.add("symlinks")
                elif key == "sha256":
                    self.namespace(parent, members, {}, owner + "/sha256", category,
                        "PARTIAL_FLAT_STAGE_SEAL; no exhaustiveness claim", document)
                continue
            self.walk(item, document, category, pointer + "/" + key, context)

    @staticmethod
    def history_document_names():
        return frozenset((
            "axial-material-AAA-white-trace-refined-layered-propagation-causal-20261005/declaration.json",
            "axial-material-AAA-white-trace-refined-layered-full-20261005/seal.json",
            "axial-material-AAA-white-trace-refined-layered-full-20261005/result.json",
            "axial-material-AAA-white-trace-refined-layered-full-20261005/declaration.json",
            "axial-material-production-qualified-AB-storage-20261004/AAA/map001/result.json",
            "axial-material-production-qualified-AB-compensated-20261004/AAA/map004/result.json",
            "axial-material-production-qualified-AB-white-trace-20261004/AAA/map011/result.json",
            "axial-material-ce-qualified-AAA-long-generations-20261004/input_equivalence_AAA.json",
            "axial-material-ce-qualified-AAA-ufs-20261004/input_equivalence_AAA.json",
            "axial-material-qualified-AB-compensated-admission-20261004/input_equivalence_AAA.json",
            "axial-material-ce-qualified-AAA-white-trace-precision-specpin-20261004/input_equivalence_AAA.json",
            "axial-material-qualified-AAA-white-trace-reference-diagnostic-20261004/input_equivalence_AAA.json",
        ))

    def apply_authorized_historical_scope(self):
        """Drop only six source-reviewed, unconsumed payload-edge families.

        Keep every proof JSON and its original descriptor/map values. This is
        an edge classification, not a failed-hash exemption: another owner of
        the same payload always retains its expected byte requirement. The
        current cold/build/capture and exhaustive predecessor contracts are
        never matched by this policy.
        """
        full = self.art_text + "/axial-material-AAA-white-trace-refined-layered-full-20261005"
        causal_path = self.art_text + "/axial-material-AAA-white-trace-refined-layered-propagation-causal-20261005/declaration.json"
        causal = self.history_documents.get(causal_path, {})
        seal = self.history_documents.get(full + "/seal.json", {})
        result = self.history_documents.get(full + "/result.json", {})
        declaration = self.history_documents.get(full + "/declaration.json", {})
        full_enabled = (
            causal.get("schema") == "AXMAT_CURRENT_LAYERED_COMPARISON_DECLARATION_V1"
            and causal.get("full_root") == full
            and causal.get("full_seal_sha256") == "67a1e9e18e180c07f7316181966ed12793f0979c2bdb32b58adcc5407bdd1de0"
            and causal.get("full_declaration_sha256") == "f032eee5a6dfb9844a57043d1a357a8bfe383f2d6c2c71761841717f3ed6c94b"
            and self.files.get(full + "/seal.json") == causal.get("full_seal_sha256")
            and seal.get("schema") == "AXMAT_CURRENT_FULL_FIXED_SOURCE_WHITE_SEAL_V1"
            and declaration.get("schema") == "AXMAT_CURRENT_LAYERED_FULL_FAMILY_V1"
            and result.get("classification") == "COMPLETE_CURRENT_DATA_H20_N4_FULL_FIXED_SOURCE_WHITE_ONLY"
            and result.get("AAA_accuracy_qualified") is False and result.get("ABA_admitted") is False)
        full_live_inputs = {full + "/" + name for name in (
            "runtime/cached.dylib", "preflight/live_guard/tested_driver_source.py",
            "preflight/live_guard/positive.log", "preflight/live_guard/memorycap.log",
            "preflight/live_guard/positive.watchdog.json", "preflight/live_guard/memorycap.watchdog.json",
            "preflight/live_guard/guard_controls.json")}
        final_documents = {}
        for name in (
            "axial-material-production-qualified-AB-storage-20261004/AAA/map001/result.json",
            "axial-material-production-qualified-AB-compensated-20261004/AAA/map004/result.json",
            "axial-material-production-qualified-AB-white-trace-20261004/AAA/map011/result.json"):
            path = self.art_text + "/" + name
            value = self.history_documents.get(path, {})
            if set(value) == {"classification", "sha256"} and value["classification"] == "SEALED_STAGE_OUTPUTS":
                _object(value["sha256"], path + ".sha256")
                final_documents[path] = path.rsplit("/", 1)[0]
        archive_documents = {}
        for name, producer in (
            ("axial-material-ce-qualified-AAA-long-generations-20261004", "axial-material-production-qualified-AB-compensated-20261004"),
            ("axial-material-ce-qualified-AAA-ufs-20261004", "axial-material-production-qualified-AB-compensated-20261004"),
            ("axial-material-qualified-AB-compensated-admission-20261004", "axial-material-production-qualified-AB-compensated-20261004"),
            ("axial-material-ce-qualified-AAA-white-trace-precision-specpin-20261004", "axial-material-production-qualified-AB-white-trace-20261004"),
            ("axial-material-qualified-AAA-white-trace-reference-diagnostic-20261004", "axial-material-production-qualified-AB-white-trace-20261004")):
            path = self.art_text + "/" + name + "/input_equivalence_AAA.json"
            value = self.history_documents.get(path, {})
            archive = value.get("actual_archive", {})
            expected_path = self.art_text + "/" + producer + "/archives/aaa_snapshots.xsm"
            if (type(value.get("schema_version")) is int and value["schema_version"] == 1
                    and value.get("case") == "AAA" and value.get("status") == "PASS"
                    and isinstance(archive, dict) and set(archive) == {"path", "sha256"}
                    and archive["path"] == expected_path):
                _sha(archive["sha256"])
                archive_documents[path] = expected_path
        for (owner, category), files in self.groups.items():
            document, marker, pointer = owner.partition("#")
            removed = {}
            for path, wanted in list(files.items()):
                full_edge = (full_enabled and marker and document.startswith(full + "/")
                    and document.endswith(".json") and path.startswith(full + "/")
                    and not path.endswith(".json") and path not in full_live_inputs)
                final_edge = (document in final_documents
                    and pointer in ("/sha256", "//sha256", "/sha256.target", "//sha256.target")
                    and not path.endswith(".json"))
                archive_edge = (document in archive_documents
                    and pointer == "/actual_archive" and path == archive_documents[document])
                if full_edge or final_edge or archive_edge:
                    removed[path] = wanted
                    del files[path]
            if removed:
                self.historical_observations.append(dict(document=document, owner=owner,
                    category=category, observed_expected_files=removed,
                    current_dependency_endpoints=False, scientific_PASS_inherited=False,
                    scope="Source-reviewed unconsumed historical payload edge only; proof JSON and any independent current/scientific owner are retained"))
        required = {path for files in self.groups.values() for path in files}
        self.files = {path: wanted for path, wanted in self.files.items() if path in required}
        active_namespaces = []
        for spec in self.namespaces:
            root = str(spec["root"])
            namespace_document = spec["owner"].partition("#")[0]
            historical_full = (full_enabled and (root == full or root.startswith(full + "/"))
                and root != full + "/preflight/live_guard"
                and namespace_document.startswith(full + "/") and namespace_document.endswith(".json"))
            historical_final = (namespace_document in final_documents
                                and root == final_documents[namespace_document])
            if historical_full or historical_final:
                self.historical_namespace_observations.append(dict(spec,
                    current_namespace_required=False, scientific_PASS_inherited=False,
                    scope="Historical proof namespace description retained only; it must not trigger a fresh full payload namespace scan"))
            else:
                active_namespaces.append(spec)
        self.namespaces = active_namespaces

    def drain(self):
        while self.queue:
            path, category, supplied = self.queue.popleft()
            if path in self.parsed:
                continue
            context = self.relative_context(path, supplied)
            self.walk(_read(path), path, category, context=context)
            self.parsed.add(path)
            self.documents.append(dict(path=path, expected_sha256=self.files.get(path),
                category=category, relative_root=context,
                bytes_verified_by_this_helper=False))


def transitive_input_owners(*, artifacts_root, production_root, build_root,
                            typed_snapshot, root_paths):
    """Enumerate typed dependencies without declaring them verified or qualified."""
    art, prod, build = _path(artifacts_root), _path(production_root), _path(build_root)
    if Path(prod).parent != Path(art) or Path(build).parent != Path(art):
        raise ValueError("actual production/build roots must be direct artifact-family roots")
    typed_snapshot = _object(typed_snapshot, "genuine typed full-ready snapshot")
    inputs = _Inputs(art, prod, build)
    graph_source = _graph_categories()
    for path in (Path(__file__).absolute(), graph_source):
        inputs.add(path, None, "input ownership implementation", "code_environment",
                   new_reason="Explicit implementation input; caller must bind its actual source bytes")
    if isinstance(root_paths, dict):
        seeds = []
        for path, item in root_paths.items():
            item = dict(_object(item, "explicit root_paths member"))
            if "path" in item and _path(item["path"]) != _path(path):
                raise ValueError("root seed key and typed path disagree")
            item["path"] = path
            seeds.append(item)
    elif isinstance(root_paths, (list, tuple)):
        seeds = root_paths
    else:
        raise ValueError("root_paths must be an explicit typed list or mapping")
    for index, seed in enumerate(seeds):
        seed = _object(seed, "root_paths[" + str(index) + "]")
        if set(seed) - {"path", "sha256", "owner", "category", "kind", "relative_root", "reason"}:
            raise ValueError("unsupported root input ownership field")
        if seed.get("kind", "pin") not in ("pin", "file", "json"):
            raise ValueError("unsupported explicit root input kind")
        if seed.get("kind") == "json" or Path(seed["path"]).suffix == ".json":
            inputs.explicit_json.add(_path(seed["path"]))
        inputs.add(seed["path"], seed.get("sha256"), seed["owner"], seed["category"],
                   relative_root=seed.get("relative_root"), new_reason=seed.get("reason"))

    sample_root = Path(art) / "axial-material-ce-qualified-AAA-white-trace-precision-specpin-20261004/AAA"
    snapshot_contexts = {
        "info": (str(Path(prod)), "production_prepared_layout"),
        "status": (str(Path(prod) / "AAA"), "completed_cold_case"),
        "coupled": (str(Path(prod) / "AAA"), "completed_cold_case"),
        "build": (str(Path(build)), "cache_build"),
        "recipe": (str(Path(art) / "axial-material-qualified-AB-white-trace-refined-envpin-admission-20261005"), "reference_scientific_dependencies"),
        "native": (str(sample_root), "reference_scientific_dependencies"),
        "execution": (str(sample_root), "reference_scientific_dependencies"),
        "environment": (None, "code_environment"),
        "cold_terminal_evidence": (None, "completed_cold_case"),
    }
    for key, value in typed_snapshot.items():
        context, category = snapshot_contexts.get(key, (None, "reference_scientific_dependencies"))
        inputs.walk(value, "snapshot:" + key, category, context=context)
    inputs.drain()
    # An inventory binds old alias text, but may not bind an external target's
    # bytes. The caller must explicitly newly declare that missing input.
    processed_aliases = set()
    while set(inputs.aliases) - processed_aliases:
        for path in sorted(set(inputs.aliases) - processed_aliases):
            entry = inputs.aliases[path]
            target = entry.get("lexical_target", entry.get("expected_resolved_target"))
            if target in inputs.files:
                entry["target_expected_sha256"] = inputs.files[target]
            elif path in inputs.files:
                entry["target_expected_sha256"] = inputs.files[path]
                inputs.add(target, inputs.files[path], entry["owner"] + ".target", entry["category"])
            else:
                inputs.add(target, None, entry["owner"] + ".target", entry["category"],
                           new_reason="Old alias contract lacked an expected target hash; bind actual target as new input-only bytes")
            processed_aliases.add(path)
        inputs.drain()
    inputs.apply_authorized_historical_scope()
    owners = [dict(owner=owner, category=category, expected_files=dict(sorted(files.items())))
              for (owner, category), files in sorted(inputs.groups.items()) if files]
    return dict(schema=SCHEMA, scope="INPUT_ONLY_NO_SCIENCE_OR_RESOURCE_DECISION",
        closure_categories=list(CLOSURE_CATEGORIES), owners=owners,
        expected_files=dict(sorted(inputs.files.items())), namespace_specs=inputs.namespaces,
        alias_specs=[inputs.aliases[path] for path in sorted(inputs.aliases)],
        historical_observation_maps=inputs.historical_observations,
        historical_namespace_observations=inputs.historical_namespace_observations,
        new_decl_paths=dict(sorted(inputs.new.items())), parsed_json_documents=inputs.documents,
        counts=dict(expected_paths=len(inputs.files), owner_groups=len(owners),
                    namespace_specs=len(inputs.namespaces), literal_or_resolved_alias_specs=len(inputs.aliases),
                    newly_declared_input_paths=len(inputs.new), metadata_documents_read=len(inputs.documents)),
        hashes_computed=0, APIs_called=0, numerical_programs_executed=0,
        scientific_predicates_evaluated=False, AAA_accuracy_qualified=False, ABA_admitted=False,
        limits="Typed manifest closure only. Caller must genuinely verify all expected bytes, explicitly pin new inputs, capture complete actual namespaces/directories/alias chains, account for unknown actual read-trace paths, and retain actual scientific/lifecycle/environment/module/resource checks. No saved old PASS is promoted.")
