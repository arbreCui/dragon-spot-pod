"""Explicit immutable input owners for the retained AAA physical/CE checks.

This module only inventories the fields actually read by the retained physical
review and collector.  It does not hash large inputs, run a project API, inspect
scientific arrays, or establish a physical or accuracy PASS.  A new declaration
must freshly pin ``newly_declared_input_paths`` and verify all ``expected_files``.
The actual XSM/white/material/geometry/volume and all-reference statistical and
current calculations remain required on every new analysis.

``scientific_input_owners(artifacts_root, production_root, observation_root,
prepared_info=None)`` returns a JSON-compatible typed inventory.  The observation
root is the new analysis's ``fine`` directory; its parent is the analysis root.
``prepared_info`` may be the genuine controller's already verified return.  The
saved prepared JSON must still agree with it.  No fallback looks for arbitrary
strings resembling paths: every extracted edge below has an explicit owner and
field.  Importing this module performs no file I/O.
"""

from __future__ import annotations

import json
from pathlib import Path
import re


SCHEMA = "AXMAT_REFERENCE_SCIENTIFIC_INPUT_OWNERS_V1"
OLD_PREPARED_SHA = "88640bfd32cbca03d4e527b99760f99288528bb0ff5720c81f758bca60beffbf"
PRIOR_PHYSICAL_SHA = "7758243c80bdfae56ded546079d18379a19bbc605fd0a7b7f3646eaab6653a34"
CE_EXECUTION_SHA = "17c4e48d4de450bc5e3232caf3238da519f23c3836bd54f0a91d122d300ae52c"
RECIPE_SHA = "56ebbfcc334dc77b1134a218f46a60393503a79bd9b167f2ef2e74aba11e5806"
PHYSICAL_FIELDS = (
    "ISOTOPERNAME", "ISOTOPESMIX", "ISOTOPESDENS", "ISOTOPESTEMP",
    "ISOTOPESUSED", "ISOTOPESVOL", "MIXTURESVOL", "ENERGY",
)
RADIAL_FIELDS = (
    "MATCOD", "KEYFLX", "VOLUME", "NZON$MCCG", "V$MCCG",
    "ZMU$MCCG", "WZMU$MCCG", "XMU$MCCG",
)
GEOMETRY_FIELDS = (
    "AREA2D", "NCODE", "ICODE", "ZCODE", "U", "W", "PL",
    "MAT1D", "MATCOD", "VOL1D", "VOLUME",
)
MEASUREMENT_DESCRIPTOR_FIELDS = (
    "prepared", "AAA_status", "final_seal", "input_equivalence",
    "production_checks", "CE_manifest", "implementation",
    "sampling_declaration", "sampling_review", "smoke_activation",
    "parent_measurement_admission",
)


def _absolute(value):
    if not isinstance(value, (str, Path)):
        raise ValueError("an input owner path must be an absolute string or Path")
    path = Path(value)
    if not path.is_absolute() or ".." in path.parts:
        raise ValueError("an input owner path must be absolute without parent traversal")
    # Do not resolve here: the graph must preserve the literal path, every alias
    # component, and the final canonical target as separate identity evidence.
    return str(path)


def _sha(value):
    if not isinstance(value, str) or re.fullmatch(r"[0-9a-f]{64}", value) is None:
        raise ValueError("an expected input hash must be a literal SHA256")
    return value


def _relative(value, flat=False):
    if not isinstance(value, str) or not value:
        raise ValueError("a manifest member must be a nonempty relative string")
    path = Path(value)
    if (path.is_absolute() or ".." in path.parts or str(path) != value
            or value in (".", "..") or (flat and path.name != value)):
        raise ValueError("invalid explicitly owned relative manifest member")
    return value


def _object(value, owner):
    if type(value) is not dict:
        raise ValueError("the explicitly owned JSON object is missing: " + owner)
    return value


def _read(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate key in an input-owner JSON document")
            result[key] = value
        return result
    def nonfinite(value):
        raise ValueError("nonfinite JSON constant in an input-owner document: " + value)
    with Path(_absolute(path)).open(encoding="utf-8") as stream:
        result = json.load(stream, object_pairs_hook=unique, parse_constant=nonfinite)
    return _object(result, str(path))


class _Owners:
    def __init__(self):
        self.files = {}
        self.owners = {}
        self.unpinned = set()
        self.namespaces = []

    def add(self, path, owner, expected=None):
        name = _absolute(path)
        if not isinstance(owner, str) or not owner:
            raise ValueError("every input edge needs an explicit owner")
        self.owners.setdefault(name, set()).add(owner)
        if expected is None:
            if name not in self.files:
                self.unpinned.add(name)
        else:
            wanted = _sha(expected)
            if name in self.files and self.files[name] != wanted:
                raise ValueError("conflicting expected hashes for one scientific input: " + name)
            self.files[name] = wanted
            self.unpinned.discard(name)
        return name

    def descriptor(self, value, owner):
        value = _object(value, owner)
        return self.add(value["path"], owner, value["sha256"])

    def hashes(self, value, owner, expected_count=None):
        value = _object(value, owner)
        if expected_count is not None and len(value) != expected_count:
            raise ValueError("complete original owner map changed: " + owner)
        for name, wanted in value.items():
            self.add(name, owner, wanted)

    def relative_hashes(self, root, value, owner, flat=False):
        value = _object(value, owner)
        for name, wanted in value.items():
            self.add(Path(root) / _relative(name, flat=flat), owner, wanted)

    def read(self, path, owner, expected=None):
        self.add(path, owner, expected)
        return _read(path)

    def stage_seal(self, root, owner):
        root = Path(root)
        seal = self.read(root / "result.json", owner + ".seal")
        if seal["classification"] != "SEALED_STAGE_OUTPUTS":
            raise ValueError("the original flat sealed-stage schema is required: " + str(root))
        covered = _object(seal["sha256"], owner + ".sha256")
        self.relative_hashes(root, covered, owner + ".sha256", flat=True)
        self.namespaces.append(dict(root=_absolute(root), owner=owner,
            manifest=_absolute(root / "result.json"), manifest_field="sha256",
            manifest_members=sorted(covered), manifest_is_namespace_exhaustive=False,
            snapshot_full_actual_namespace_on_declare=True,
            bind_regular_files_and_literal_aliases_and_targets=True,
            fresh_namespace_and_alias_check_each_checkpoint=True))


def scientific_input_owners(artifacts_root, production_root, observation_root,
                            prepared_info=None):
    """Return explicit additional input edges; never return a scientific PASS.

    The caller owns the new factory/runtime, all transitive build and environment
    closures, and the actual completed candidate.  This list adds the physical
    and collector endpoints not necessarily opened by the factory's full-ready
    check.  Returned new pins are pending until the caller's real declaration
    hashes and archives them.  Future output requirements must be bound only
    after their own actual producing stage completes.
    """
    art = Path(_absolute(artifacts_root))
    prod = Path(_absolute(production_root))
    fine = Path(_absolute(observation_root))
    analysis = fine.parent
    if (fine.name != "fine" or analysis.parent != art or not analysis.name.startswith("axial-material-")
            or prod.parent != art or not prod.name.startswith("axial-material-production-")):
        raise ValueError("explicit production and new fine-observation roots are required")
    ledger = _Owners()
    ledger.add(Path(__file__).absolute(), "input-owner inventory implementation")

    prepared_path = prod / "prepared.json"
    stored_info = ledger.read(prepared_path, "physical and collector.prepared")
    if prepared_info is None:
        info = stored_info
    else:
        info = _object(prepared_info, "actual verified prepared return")
        if stored_info != info:
            raise ValueError("typed verified prepared return differs from the saved JSON")
    for key in ("case_spec", "rank_addendum", "declaration"):
        ledger.descriptor(info[key], "verified prepared." + key)
    for key, item in _object(info["inputs"], "verified prepared.inputs").items():
        ledger.descriptor(item, "verified prepared.inputs." + key)
    ledger.relative_hashes(prod, info["local_files"], "verified prepared.local_files")

    status_path = prod / "AAA/run_status.json"
    status = ledger.read(status_path, "physical and collector.actual AAA status")
    case = _object(_object(status["cases"], "actual status.cases")["AAA"], "actual status.AAA")
    final = Path(_absolute(case["final_directory"]))
    if final.parent != prod / "AAA" or re.fullmatch(r"map[0-9]{3}", final.name) is None:
        raise ValueError("the actual final candidate must be an AAA map in its own production root")
    for root, owner in ((prod / "archives", "actual packed snapshot archives"),
                        (prod / "training", "actual common training"),
                        (prod / "AAA/bootstrap", "actual bootstrap"),
                        (final, "actual final map")):
        ledger.stage_seal(root, owner)

    old = art / "axial-material-production-qualified-AB-white-trace-20261004"
    ce = art / "axial-material-ce-qualified-AAA-white-trace-precision-specpin-20261004"
    case_dir = ce / "AAA"
    tools = art / "axial-material-tools-20261003"
    cold = art / "axial-material-AAA-white-trace-angular-convergence-20261005/cold48_sn32"
    old_info = ledger.read(old / "prepared.json", "physical.original prepared", OLD_PREPARED_SHA)
    ledger.descriptor(old_info["case_spec"], "physical.original case_spec")

    prior_path = ce / "input_equivalence_AAA.json"
    prior = ledger.read(prior_path, "physical.prior full input proof", PRIOR_PHYSICAL_SHA)
    ledger.hashes(prior["input_identities"], "physical.prior.input_identities", expected_count=54)
    ce_inputs = _object(prior["CE_inputs"], "physical.prior.CE_inputs")
    if set(ce_inputs) != {"materials.xml", "geometry.xml", "settings.xml", "tallies.xml", "reference_contract.json"}:
        raise ValueError("all five original physical CE inputs are required")
    for key, item in ce_inputs.items():
        ledger.descriptor(item, "physical.prior.CE_inputs." + key)

    # The receipt document itself was read without an expected hash in the
    # original child.  Its bytes must be newly declared, as well as its 7-member
    # proof map and the independent base proof's complete 62-member input map.
    base_path = tools / "input_equivalence_rank1_AAA.json"
    receipt_path = tools / "input_equivalence_rank1_AAA_receipt.json"
    receipt = ledger.read(receipt_path, "physical.tools receipt document")
    ledger.hashes(receipt["files"], "physical.tools receipt.files", expected_count=7)
    if str(base_path) not in ledger.files:
        raise ValueError("the original tools receipt must pin the actual base proof JSON")
    base = ledger.read(base_path, "physical.tools base proof", ledger.files[str(base_path)])
    ledger.hashes(base["input_sha256"], "physical.tools base.input_sha256", expected_count=62)

    tracked = prod / "AAA/bootstrap/initial_axial_track.xsm"
    unmarked = prod / "AAA/bootstrap/initial_axial_track_unmarked.xsm"
    original_track = old / "AAA/bootstrap/initial_axial_track.xsm"
    admitted_track = cold / "track.xsm"
    snapshot = art / "axial-material-inputs-20261003/A/snapshot_A.xsm"
    archive = prod / "archives/aaa_snapshots.xsm"
    for path, owner in ((unmarked, "physical.white original complete inherited records"),
                        (tracked, "physical.white and fine geometry records"),
                        (original_track, "physical.original 12-cell geometry records"),
                        (admitted_track, "physical.admitted SN32 U/W/PL words"),
                        (snapshot, "physical.original A material and radial records"),
                        (archive, "physical.all three actual AAA archive slots")):
        ledger.add(path, owner)
    ledger.add(case_dir / "reference_contract.json", "physical and statistics.original 96-bin/13-plane contract")

    execution_path = case_dir / "execution.json"
    execution = ledger.read(execution_path, "collector.original CE execution", CE_EXECUTION_SHA)
    ledger.hashes(execution["files"], "collector.original CE execution.files")
    ledger.read(case_dir / "run_claim.json", "collector.original CE run claim")
    native = ledger.read(case_dir / "native_result.json", "collector.original complete native result")
    ledger.add(case_dir / "openmc.log", "collector.original native stdout", native["log_sha256"])
    outputs = _object(native["outputs"], "collector.original native outputs")
    expected_statepoints = {f"statepoint.{batch:04d}.h5" for batch in range(101, 2101)}
    actual_statepoints = {name for name in outputs if name.startswith("statepoint.") and name.endswith(".h5")}
    if actual_statepoints != expected_statepoints:
        raise ValueError("all 2000 original zero-padded native reference statepoints are required")
    ledger.relative_hashes(case_dir, outputs, "collector.original complete native outputs", flat=True)
    ledger.namespaces.append(dict(root=_absolute(case_dir), owner="original immutable native reference",
        manifest=_absolute(case_dir / "native_result.json"), manifest_field="outputs",
        manifest_members=sorted(outputs), manifest_is_namespace_exhaustive=False,
        statepoint_glob="statepoint.*.h5", required_statepoint_members=sorted(expected_statepoints),
        snapshot_full_actual_namespace_on_declare=True,
        bind_regular_files_and_literal_aliases_and_targets=True,
        fresh_namespace_and_alias_check_each_checkpoint=True))

    measurement_path = case_dir / "measurement_admission.json"
    measurement = ledger.read(measurement_path, "collector.historical reference measurement")
    for key in MEASUREMENT_DESCRIPTOR_FIELDS:
        ledger.descriptor(measurement[key], "collector.historical measurement." + key)
    sampling_path = measurement["sampling_review"]["path"]
    sampling = ledger.read(sampling_path, "collector.historical sampling review", measurement["sampling_review"]["sha256"])
    ledger.hashes(sampling["files"], "collector.historical sampling review.files")

    recipe_root = art / "axial-material-qualified-AB-white-trace-refined-envpin-admission-20261005"
    recipe = ledger.read(recipe_root / "refined_reference_analysis_recipe.json",
                         "factory.original immutable reference recipe", RECIPE_SHA)
    for key in ("refined_prepared", "reference_execution", "complete_independent_native_sample",
                "original_candidate_assessment", "observation_projection_recipe", "projection_precheck",
                "native_export_source_proof", "physical_input_precheck"):
        ledger.descriptor(recipe[key], "factory.original reference recipe." + key)
    for key, item in _object(recipe["unchanged_reference_implementations"], "recipe.implementations").items():
        ledger.descriptor(item, "factory.unchanged reference implementation." + key)
    ledger.add(ce / "statistical_rules.json", "fresh statistics.original statistical rules")
    ledger.add(ce / "balance_symmetry_rules.json", "fresh currents.original current rules")

    future = []
    def fresh(path, owner, fields):
        future.append(dict(path=_absolute(path), owner=owner, fields=fields,
            declaration_result_must_not_substitute_actual_new_output=True,
            hash_and_bind_only_after_actual_producing_stage=True))
    fresh(fine / "export_receipt.json", "physical.actual new complete exporter receipt",
          ["classification", "outputs", "protocol", "inputs_unchanged", "implementation_unchanged"])
    fresh(fine / "protocol.json", "physical.actual new saved-state export protocol",
          ["production_prepared", "AAA_status", "source_inputs", "implementation", "exporter", "exporter_source"])
    for suffix in ("regions.csv", "faces.csv", "summary.txt"):
        fresh(fine / ("observables." + suffix), "physical/project.actual fine observable fields", ["actual file bytes"])
        fresh(analysis / "observation" / ("observables." + suffix),
              "statistics/currents.actual conservative original-bin fields", ["actual file bytes"])
    for path, owner, fields in (
        (fine / "input_equivalence_AAA.json", "project.actual fine physical review", ["status", "input_identities"]),
        (analysis / "observation/projection_receipt.json", "collector.actual conservative projection", ["mapping", "face_map", "original_checks_on_all_fine_entries", "original_checks_on_observation_view"]),
        (analysis / "complete_fine_production_checks.json", "collector.actual complete fine checks", ["checks", "input_identities"]),
        (analysis / "input_equivalence_AAA.json", "collector.actual physical evidence", ["status", "input_identities"]),
        (analysis / "measurement_admission.json", "collector.actual new measurement admission", ["files", "production_prepared", "AAA_status", "common_basis_sha256"]),
        (analysis / "measurement_binding.json", "collector.actual parent-archived measurement", ["files", "declaration_sha256"]),
        (analysis / "AAA/statistics.json", "collector.actual all-2000 statistical evidence", ["input_identities", "statepoint_identities", "source_generation_history", "checks"]),
        (analysis / "AAA/currents_balance_symmetry.json", "collector.actual all-2000 current evidence", ["input_identities", "statepoint_identities", "checks"]),
    ):
        fresh(path, owner, fields)

    records = [dict(path=name, expected_sha256=ledger.files.get(name),
                    owners=sorted(ledger.owners[name]),
                    newly_declared_pin_required=name in ledger.unpinned)
               for name in sorted(ledger.owners)]
    owner_groups = []
    for owner in sorted({owner for names in ledger.owners.values() for owner in names}):
        owner_groups.append(dict(owner=owner, category="reference_scientific_dependencies",
            expected_files={name: ledger.files[name] for name in sorted(ledger.files)
                            if owner in ledger.owners[name]},
            newly_declared_input_paths=[name for name in sorted(ledger.unpinned)
                                       if owner in ledger.owners[name]]))
    return dict(schema=SCHEMA, production_root=str(prod), fine_observation_root=str(fine),
        expected_files=dict(sorted(ledger.files.items())), input_records=records,
        owners=owner_groups,
        newly_declared_input_paths=sorted(ledger.unpinned),
        namespace_requirements=ledger.namespaces,
        alias_requirements=dict(scope="every owned input path and every captured namespace member",
            bind_literal_path_component_symlink_chain=True, bind_literal_link_text_and_canonical_target=True,
            freshly_hash_each_unique_canonical_regular_file_at_each_checkpoint=True,
            reject_missing_special_aliased_or_changed_members=True,
            no_stat_only_or_cross_checkpoint_hash_cache=True),
        fresh_analysis_output_requirements=future,
        actual_physical_record_requirements=dict(geometry=list(GEOMETRY_FIELDS),
            white_copy="All inherited XSM directory/list/type/length/word records plus only the two admitted white markers",
            material_records=list(PHYSICAL_FIELDS), radial_records=list(RADIAL_FIELDS),
            actual_archive_slots=3, material_plus_radial_records=48,
            native_region_cell_entries=384, original_volume_bins=96, original_face_planes=13,
            all_formulas_and_word_comparisons_must_execute_on_actual_new_inputs=True),
        all_2000_actual_statepoints_and_all_original_eight_scientific_conditions_must_be_recomputed=True,
        counts=dict(unique_owned_input_paths=len(records), expected_hash_paths=len(ledger.files),
                    newly_declared_pin_paths=len(ledger.unpinned), original_tools_base_inputs=62,
                    original_tools_receipt_members=7, original_prior_physical_inputs=54,
                    actual_reference_statepoints=2000),
        scientific_predicates_evaluated=False, AAA_accuracy_qualified=False, ABA_admitted=False,
        limits="Additional explicit input ownership only. The caller must add the complete transitive build/environment/producer/cold/seal graph, genuine declaration-terminal evidence, live module/MRO/environment and resource/lifecycle checks. No cached scientific PASS or accuracy qualification is produced.")
