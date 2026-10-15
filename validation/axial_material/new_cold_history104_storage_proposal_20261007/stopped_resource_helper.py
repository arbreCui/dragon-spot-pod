"""Stopped source proposal: a NEW cold-family history cap of 104 GiB.

Nothing in this file executes a resource check, fixture, API, prepare or native
calculation. Import creates only stdlib bindings, literal Paths and definitions.
All resource construction and filesystem business entrypoints begin with an
unconditional UNREADY guard. Approval and the new addendum are absent (None).
This file can never become ready by changing metadata globals at runtime.
A future reviewed source, new family and actual source-bound storage addendum
would be required; existing frozen 96-GiB INPUT evidence is never upgraded.

The complete original fe811 accounting algorithm is retained in the extracted
resource class. Its only planned numerical limit change is 96 -> 104 GiB;
free-space remains 8 GiB. No instance/subclass/global/module overlay exists.
104 is a planning recommendation, never a 100-map completion guarantee.
64 MiB is the controls archive reservation. Fixtures RSS remains 512 MiB.
"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import time

ROOT = Path('/Users/wen/spot')
ART = ROOT / 'validation/artifacts'
ORIGINAL_RESOURCE_SOURCE = ROOT / 'validation/axial_material/prepare_qualified_AB_moment_order_production.py'
ORIGINAL_RESOURCE_SOURCE_SHA256 = 'fe81150fbf270cac44e241ad64f352cf2f623fa65f7ccb4a9b0ded0a4f2c2d41'
RESOURCE_SPEC = ART / "axial-material-qualified-AB-white-trace-refined-envpin-admission-20261005/case_spec.json"
RESOURCE_SPEC_SHA = "8c2297533ff582e81cef6430947a0557e921830304673a6a8a6c0149fd7a33ae"
RESOURCE_ADDENDUM = RESOURCE_SPEC.with_name("resource_addendum.json")
RESOURCE_ADDENDUM_SHA = "b68ca3ee2802b69900c5085757898872a220de4f038ab9cd14cb4287b9c5fd15"
HISTORY_SCOPE_POLICY = "AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1"
PROPOSAL_STATUS = 'UNREADY_CANDIDATE104_NO_USER_APPROVAL_OR_NEW_STORAGE_ADDENDUM'
USER_APPROVAL = None
STORAGE_ADDENDUM_DESCRIPTOR = None
NEW_COLD_CASE_SPEC_DESCRIPTOR = None
NEW_RESOURCE_HELPER_SOURCE_DESCRIPTOR = None
CANDIDATE_HISTORY_CAP_BYTES = 104 * 2**30
UNCHANGED_FREE_FLOOR_BYTES = 8 * 2**30
ORIGINAL_COLD_RESERVATION_BYTES = 20971764748


def _require_ready():
    """First business step; no caller or mutable flag admits this stopped source."""
    raise RuntimeError('UNREADY: candidate104 has no user approval, new storage '
                       'addendum, new cold-family case specification or reviewed '
                       'ready source. No resource instance or filesystem business '
                       'is admitted by this stopped proposal.')


def source_contract():
    """Pure proposal metadata; this does not read a file or admit a resource."""
    return dict(schema='AXMAT_NEW_COLD_HISTORY104_STOPPED_SOURCE_PROPOSAL_V1',
        status=PROPOSAL_STATUS, user_approval=USER_APPROVAL,
        storage_addendum_descriptor=STORAGE_ADDENDUM_DESCRIPTOR,
        new_cold_case_spec_descriptor=NEW_COLD_CASE_SPEC_DESCRIPTOR,
        new_resource_helper_source_descriptor=NEW_RESOURCE_HELPER_SOURCE_DESCRIPTOR,
        original_resource_source=dict(path=str(ORIGINAL_RESOURCE_SOURCE),sha256=ORIGINAL_RESOURCE_SOURCE_SHA256),
        candidate_history_cap_bytes=CANDIDATE_HISTORY_CAP_BYTES,
        unchanged_min_free_bytes=UNCHANGED_FREE_FLOOR_BYTES,
        original_cold_reservation_bytes=ORIGINAL_COLD_RESERVATION_BYTES,
        history_scope_policy=HISTORY_SCOPE_POLICY,
        all_declared_extras_and_dynamic_current_axial_family_roots_retained=True,
        regular_file_apparent_bytes_no_follow_and_no_inode_dedup_retained=True,
        old96_contract_is_historical_INPUT_only=True,
        original96_factory_and_API_return_body_are_immutable=True,
        old96_component_API_is_not_upgraded_to104=True,
        new_cold_family_new_source_new_case_spec_and_new_addendum_required=True,
        approval_required_before_any_business=True,
        unconditional_stopped_guard_has_no_ready_branch=True,
        resource_instantiation_or_check_executed=False,
        actual_new_resource_counts_observed=False,
        new_104_cap_is_not_a_100_map_archive_guarantee=True,
        controls_archive_reserve_bytes=64 * 2**20,
        fixtures_rss_cap_mib=512,controls_total_seconds=120,controls_stage_seconds=60,
        cold_total_seconds=43200,max_maps=100,threads=1,children_at_once=1,retries=0,
        science_thresholds_and_physics_unchanged=True,
        scientific_qualification=False,AAA_accuracy_qualified=False,ABA_admitted=False)



class DynamicHistoryFailure(RuntimeError):
    def __init__(self, snapshot):
        self.snapshot = snapshot
        super().__init__("FAIL_RESOURCE: " + snapshot["reason"])



def history_roots(declared, artifacts_root):
    """Keep all declared extras and current axial-family roots; reject aliases."""
    _require_ready()
    artifacts_root = Path(artifacts_root)
    return sorted(set(declared) | {str(p) for pattern in ("axial-material-*",)
        for p in artifacts_root.glob(pattern)})



def historical_input_resource_scope_contract():
    _require_ready()
    spec = read(require(RESOURCE_SPEC, RESOURCE_SPEC_SHA))
    addendum = read(require(RESOURCE_ADDENDUM, RESOURCE_ADDENDUM_SHA))
    notes = ("Caps are limits, not runtime promises. Existing material/native jobs retain their separate "
        "already-declared supervisors and caps. Routine implementation/debug fixes may be tested in new "
        "directories; no overwrite or numerical gate relaxation.")
    if (spec["resource_caps"]["notes"] != notes or spec["resource_caps"]["new_case_artifact_budget_GiB"] != 96
            or spec["resource_caps"]["disk_min_free_GiB"] != 8
            or spec["conditional_white_trace_trial"]["resource_addendum"] != dict(
                path=str(RESOURCE_ADDENDUM), sha256=RESOURCE_ADDENDUM_SHA)
            or addendum["new_storage_budget_GiB"] != 96 or addendum["min_free_GiB"] != 8
            or any(Path(root).parent != ART or not Path(root).name.startswith("axial-material-")
                for root in addendum["resources_before"]["resource_roots"])):
        raise ValueError("actual inherited axial-family96GiB/global-disk8GiB scope required")
    return dict(schema="AXMAT_INHERITED_AXIAL_FAMILY_RESOURCE_SCOPE_V1",
        case_spec=dict(path=str(RESOURCE_SPEC), sha256=RESOURCE_SPEC_SHA),
        resource_addendum=dict(path=str(RESOURCE_ADDENDUM), sha256=RESOURCE_ADDENDUM_SHA),
        resource_scope_policy=HISTORY_SCOPE_POLICY,
        artifact_bytes_scope="All explicit declared roots plus current direct axial-material experiment-family roots",
        all_declared_extras_retained=True, entire_project_artifact_cap_claimed=False,
        existing_material_native_jobs_retain_separate_declared_supervisors_and_caps=True,
        native_readonly_dependency_pins_are_not_a_project_wide_storage_scope=True,
        free_disk_floor_applies_to_entire_filesystem=True, artifact_budget_GiB=96, min_free_GiB=8)



def validate_history_roots(values, artifacts_root):
    _require_ready()
    base = Path(artifacts_root).resolve(strict=True)
    if not isinstance(values, list) or not values:
        raise ValueError("explicit complete-history resource roots required")
    roots = []
    for value in values:
        if not isinstance(value, str):
            raise ValueError("resource roots must be absolute directory paths")
        path = Path(value)
        if (not path.is_absolute() or ".." in path.parts or path == base or not path.is_relative_to(base)):
            raise ValueError("resource roots must be strict validation/artifacts descendants")
        cursor = path
        while cursor != base:
            if cursor.is_symlink() or (cursor.exists() and not cursor.is_dir()):
                raise ValueError("resource root or ancestor is a symlink/non-directory")
            cursor = cursor.parent
        if any(path == old or path.is_relative_to(old) or old.is_relative_to(path) for old in roots):
            raise ValueError("resource roots overlap or repeat")
        roots.append(path)
    return roots



def resource_scope_contract():
    """Unreachable candidate contract shape; not actual cap admission evidence."""
    _require_ready()
    historical_input = historical_input_resource_scope_contract()
    return dict(schema='AXMAT_NEW_COLD_EXPLICIT_HISTORY_CAP_RESOURCE_SCOPE_V1',
        resource_scope_policy=HISTORY_SCOPE_POLICY,
        original96_historical_INPUT_resource_scope_contract=historical_input,
        old96_component_API_is_not_upgraded_to104=True,
        new_cold_case_spec=NEW_COLD_CASE_SPEC_DESCRIPTOR,
        new_storage_addendum=STORAGE_ADDENDUM_DESCRIPTOR,
        user_approval=USER_APPROVAL,
        actual_new_resource_helper_source=NEW_RESOURCE_HELPER_SOURCE_DESCRIPTOR,
        artifact_bytes_scope=historical_input['artifact_bytes_scope'],
        all_declared_extras_retained=True,entire_project_artifact_cap_claimed=False,
        existing_material_native_jobs_retain_separate_declared_supervisors_and_caps=True,
        native_readonly_dependency_pins_are_not_a_project_wide_storage_scope=True,
        free_disk_floor_applies_to_entire_filesystem=True,
        artifact_budget_GiB=104,min_free_GiB=8,
        original_cold_reservation_bytes=ORIGINAL_COLD_RESERVATION_BYTES,
        new_cold_family_only=True,scientific_qualification=False)



class DynamicHistoryResources:
    """Original apparent-byte/no-follow accounting with a dynamic root union.

    This is an explicit resource-only addition, not a claim that the original
    DiskResources AST is unchanged. A caller can retain its original failure
    type; read-only admission does not import a canonical production controller.
    """
    def __init__(self, artifacts_root, roots, min_free_bytes, max_bytes, failure_type=None):
        _require_ready()
        self.artifacts_root = Path(artifacts_root)
        self.declared_roots = list(roots)
        validate_history_roots(self.declared_roots, self.artifacts_root)
        if min_free_bytes != 8 * 2**30 or max_bytes != 104 * 2**30:
            raise ValueError("new cold candidate104GiB/unchanged free8GiB caps required")
        self.min_free_bytes, self.max_bytes = min_free_bytes, max_bytes
        self.failure_type = failure_type or DynamicHistoryFailure
        self.latest = None

    def check(self):
        _require_ready()
        snapshot = dict(checked_unix=time.time(), min_free_bytes=self.min_free_bytes,
            artifact_budget_bytes=self.max_bytes, declared_resource_roots=list(self.declared_roots),
            resource_scope_policy=HISTORY_SCOPE_POLICY, resource_scope_contract=resource_scope_contract())
        try:
            roots = validate_history_roots(history_roots(self.declared_roots, self.artifacts_root),
                self.artifacts_root)
            snapshot["resource_roots"] = [str(p) for p in roots]
            total, count, stack = 0, 0, list(roots)
            while stack:
                directory = stack.pop()
                try:
                    descriptor = os.open(directory, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
                    try:
                        with os.scandir(descriptor) as entries:
                            for entry in entries:
                                try:
                                    item = entry.stat(follow_symlinks=False)
                                except FileNotFoundError:
                                    continue
                                if stat.S_ISDIR(item.st_mode):
                                    stack.append(directory / entry.name)
                                elif stat.S_ISREG(item.st_mode):
                                    total += item.st_size
                                    count += 1
                    finally:
                        os.close(descriptor)
                except FileNotFoundError:
                    continue
            # Refuse a root that appeared during this traversal. A subsequent
            # check may include it, but this check must not report a false PASS.
            if snapshot["resource_roots"] != history_roots(self.declared_roots, self.artifacts_root):
                raise ValueError("complete-history root set changed during resource observation")
            validate_history_roots(snapshot["resource_roots"], self.artifacts_root)
            snapshot.update(artifact_bytes=total, regular_files=count,
                disk_free_bytes=shutil.disk_usage(self.artifacts_root).free)
            self.latest = snapshot
            reasons = []
            if snapshot["disk_free_bytes"] < self.min_free_bytes:
                reasons.append("free disk space below declared minimum")
            if total > self.max_bytes:
                reasons.append("complete history regular-file total exceeds declared artifact budget")
            if reasons:
                snapshot["reason"] = "; ".join(reasons)
                raise self.failure_type(snapshot)
            return snapshot
        except self.failure_type:
            raise
        except (OSError, ValueError) as error:
            snapshot["reason"] = "cannot verify complete dynamic resource scope: " + str(error)
            self.latest = snapshot
            raise self.failure_type(snapshot) from error



def read(path):
    _require_ready()
    return json.loads(Path(path).read_text())



def digest(path):
    _require_ready()
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()



def require(path, expected=None):
    _require_ready()
    path = Path(path)
    if path.is_symlink() or not path.is_file() or (expected is not None and digest(path) != expected):
        raise ValueError("missing, symlink or changed declared file: " + str(path))
    return path

