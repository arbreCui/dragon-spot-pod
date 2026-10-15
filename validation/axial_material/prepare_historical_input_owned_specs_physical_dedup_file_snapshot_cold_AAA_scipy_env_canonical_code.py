"""Reviewed canonical cold factory with genuine complete cp314 SciPy environment.

Derived from frozen b92. Original science, constructor, controller, full INPUT
ancestry and all budgets remain unchanged. Normal genuine SciPy imports and
complete code-environment owners/namespaces are added. Actual new controls and
cold execution remain required; this source grants no physical qualification.
"""
import argparse
import ast
import copy
import difflib
import hashlib
import importlib
import importlib.util
import json
import math
import os
from pathlib import Path
import platform
import re
import stat
import shutil
import sys
import time

sys.dont_write_bytecode = True
ROOT = Path('/Users/wen/spot')
ART = ROOT / "validation/artifacts"
OLD = ART / "axial-material-production-qualified-AB-white-trace-refined-envpin-20261005"
PARENT_SOURCE = ART / "axial-material-qualified-AB-white-trace-refined-envpin-admission-20261005"
SOURCE = ART / "axial-material-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-file-snapshot-admission-scipy-env-canonical-code-20261008"
OUTPUT = ART / "axial-material-production-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-file-snapshot-scipy-env-canonical-code-20261008"
BUILD_FACTORY = ROOT / "validation/axial_material/prepare_qualified_AB_rank1_cache_production.py"
BUILD = ART / "axial-material-rank1-factor-cache-build-20261007"
BUILD_FACTORY_SHA = "92d73658e349ea2b2816b2b770549ca22378c2595f2c9e5c9331bbf91c6abf8a"
BUILD_SOURCE = ART / "axial-material-qualified-AB-rank1-factor-cache-build-admission-20261007"
BUILD_TERMINAL = ART / "axial-material-qualified-AB-rank1-factor-cache-build-terminal-20261007"
PARENT_FACTORY = ROOT / "validation/axial_material/prepare_qualified_AB_source_factor_coupling.py"
PARENT_FACTORY_SHA = "7763b83ef4c77cd9eda8a76a42124cc4df758b14009d71f68a7087e77b458db6"
CAPTURE = ART / "axial-material-AAA-production-angular-capture-20261006"
FULL = ART / "axial-material-AAA-white-trace-refined-layered-full-20261005"
CAUSAL = ART / "axial-material-AAA-white-trace-refined-layered-propagation-causal-20261005"
PREPARED_SHA = "024ffb9263e3d3b6cf10301d6fe2bac5a87a9b368008440e01038982291a6d53"
CAPTURE_SEAL = "16f67ec74e41d3282a7e90fe342e0165c81a8fb97a6cfc1cd72615e6a9ac9c0a"
OLD_RUNTIME_SHA = "51b2d3ff947daa3ea523932bcc28276b054632f0bfc6cf76fa21ac458a4f7be4"
EXPERIMENT = "axial-material-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-file-snapshot-scipy-env-canonical-code-20261008"
OBSERVER_PREFIX = "AXMAT-MOMENT-ORDER SELECTOR "
OBSERVER_EXPECTED = [32, 3, 2, 3, 1]
HISTORY_SCOPE_POLICY = "AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1"
CACHE_OBSERVER_PREFIX = "AXMAT-RANK1-CACHE TERMINAL "
CACHE_BUDGET_BYTES = 512 * 2**20
CACHE_OBSERVER_CONTRACT = dict(prefix=CACHE_OBSERVER_PREFIX,
    columns=["builtblocks", "reusedblocks", "validated_hits", "peak_accounted_bytes", "cap_bytes"],
    cap_bytes=CACHE_BUDGET_BYTES, exact_operator_identity_required=True,
    positive_build_reuse_and_validation_required=True, all_actual_full_logs_required=True)
THREADS = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS")
UNCHANGED_NAMES = ("production_inputs.py", "snapshot_control_preflight.py", "white_receiver_tracking.py",
    "analyze_r64_snapshot.py", "analyze_r64_tracking_moments.py", "check_r64_audit_rejections.py",
    "check_r64_normalization_rejections.py")



BASE_FACTORY = ROOT/'validation/axial_material/prepare_qualified_AB_rank1_cache_coupling.py'
BASE_FACTORY_SHA = '96e54f36e1939a7edc7d112661c1e44066d7a3e869354a932ad9b967ec0d666d'
BASE_WORK = ART/'axial-material-production-qualified-AB-rank1-factor-cache-20261007'
BASE_CONTROLLER = BASE_WORK/'runtime/production_runner.py'
BASE_CONTROLLER_SHA = '844fe18738a2232d2947a8c65dc13afebcfbfd2e2afc9f0743c1c94c06fd0f7d'
BASE_PREPARED_SHA = '7d2154e9c722eab23f4411c9a8588ed8250da658ae880298c24dfb53308656b5'
BASE_RUNTIME_SHA = '292c10b259ead4d9123dcba7efd48dea0bf31b41963c620149c685c93906663c'
HOST = ROOT/'validation/axial_material/combined_cold_own_rss_host_canonical_code.py'
HOST_SHA = '32144151b0b0e40e99023be1dd880aa17f256360d1775ddd1aaaae10fc02e387'
CONTROLS = ROOT/'validation/axial_material/combined_cold_own_rss_controls.py'
CONTROLS_SHA = 'd0982ba8446ae59810e0320a188ea7250c975fffa35db648fba6036ca49c60bc'
DECK_HELPER = ROOT/'validation/axial_material/combined_cold_file_snapshot_decks.py'
DECK_HELPER_SHA = '6606ff241ae98ca193bd1e1c002ac066661fbba76a151c42ea2f62f8b979aee0'
FORMAL_FACTORY = ROOT/'validation/axial_material/prepare_historical_input_owned_specs_physical_dedup_file_snapshot_cold_AAA_scipy_env_canonical_code.py'
FORMAL_FACTORY_SHA = None  # Documentary unknown; external AXMAT_COLD_FACTORY_SHA256 avoids a self-hash cycle.
COMBINED_FACTORY = ROOT/'validation/axial_material/prepare_historical_input_owned_specs_combined_physical_dedup_file_snapshot_runtime_build.py'
COMBINED_FACTORY_SHA = 'e1b05500c855e3d639db95e03d2e158335f83aae2ce94a74cca334b31f0684c3'
COMBINED_BUILD = ART/'axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-20261007'
COMBINED_BUILD_SEAL = '33a10dd0f285b3698b0aaa7e3500f639da85c1b95f53cad10face4416fe749e9'
COMBINED_TERMINAL = ART/'axial-material-qualified-AB-historical-input-physical-dedup-combined-runtime-build-terminal-owned-specs-20261007/terminal_return.json'
COMBINED_TERMINAL_SHA = 'e1555ff8a42d26886431baaf1cb42c2adf637dc5e08f67511a5591c071f7d1a9'
COMBINED_RUNTIME = ART/'axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-20261007/runtime/Dragon'
COMBINED_RUNTIME_SHA = '550c4ac12fe55e3601c4ba5b71b21cfefc5689459bfeb55f379731179cf47294'
COMBINED_SCHEMA = 'AXMAT_HISTORICAL_INPUT_OWNED_SPECS_COMBINED_PHYSICAL_DEDUP_RUNTIME_PRODUCTION_RUNTIME_INPUT_ADMISSION_V1'
COMBINED_ADMISSION = 'COMBINED_RUNTIME_INPUT_ONLY'
PRIVATE_INPUT_CONSUMER = ROOT/'validation/axial_material/cold_component_input_consumer.py'
PRIVATE_INPUT_CONSUMER_SHA = '9a472591d6d40fc597ddbdd44d61923ee52b9da5d834d01284286360e3ce0855'
COMPONENT_INTAKE_DESCRIPTOR = ROOT/'validation/axial_material/cold_owned_specs_component_input_intake_binding_20261008.json'
COMPONENT_INTAKE_DESCRIPTOR_SHA = 'f05a3c54ee5050f0219c943ad6e03aae76766ef839ef77096e9bde9f29969497'
INPUT_REUSE_SCHEMA = 'AXMAT_COLD_COMPLETE_HISTORICAL_COMPONENT_INPUT_INTAKE_V1'
INPUT_REUSE_SEMANTICS = 'COMPLETE_FRESH_COLD_INPUT_REUSE_NOT_COMPONENT_API_REEXECUTION'
CALLBACK_METADATA_SCHEMA = 'AXMAT_HISTORICAL_INPUT_OWNED_SPECS_SCIPY_ENV_COMBINED_FILE_SNAPSHOT_COLD_INPUT_ADMISSION_V1'
SCIPY_HELPER = ROOT/'validation/axial_material/cold_scipy_environment_admission_namespace_v3_20261008.py'
SCIPY_HELPER_SHA = '35a9aca4355d577395a5bf73fb79caa24b457c7a31febc7547de93b5a1e49557'
SCIPY_DEPENDENCY_ROOT = ART/'axial-material-cold-cp314-scipy-dependency-20261008'
SCIPY_TARGET_ROOT = SCIPY_DEPENDENCY_ROOT/'target'
SCIPY_MANIFEST = SCIPY_DEPENDENCY_ROOT/'environment_manifest.json'
SCIPY_MANIFEST_SHA = '1038450822d73d1b20c369b639d4991021bfb3121df83eb1a02b1dcf8f9c514b'
FROZEN_FAILED_PREP_FACTORY = ROOT/'validation/axial_material/prepare_historical_input_owned_specs_physical_dedup_file_snapshot_cold_AAA.py'
FROZEN_FAILED_PREP_FACTORY_SHA = 'b92c68177c3d6ad04e29a5367d4d1155bbbf51534fdece901a134113076be3e0'

PHYSICAL_FACTORY = ROOT/'validation/axial_material/prepare_qualified_AB_spoasm_physical_abi_serial_guarded_production.py'
PHYSICAL_FACTORY_SHA = 'b7f361bc1d8dcdcfabf1cd2d33af3730ffb146ebe610e12370ea2b409f1ca230'
PHYSICAL_BUILD = ART/'axial-material-spoasm-physical-abi-serial-guarded-build-20261007'
PHYSICAL_SEAL = 'bad5921e7c7b5a21b9c983b80c74ce0938594200c267e16040242b1bfbf6777d'
PHYSICAL_TERMINAL = ART/'axial-material-qualified-AB-spoasm-physical-abi-serial-guarded-build-terminal-20261007/terminal_return.json'
PHYSICAL_TERMINAL_SHA = '16117d4183730050016cf96b9d8b513f596e286ad66a3107d20356e0f6c2f2f1'
DEDUP_FACTORY = ROOT/'validation/axial_material/prepare_qualified_AB_rank1_cache_memory_dedup_production.py'
DEDUP_FACTORY_SHA = '4ae768d5e06b64685c1626326de6e93d2e87b7d502f991bf1d7c06f169622c29'
DEDUP_BUILD = ART/'axial-material-rank1-factor-cache-memory-dedup-build-20261007'
DEDUP_SEAL = 'fd63bae4d542d735a8ad363de63c8e978b4318e4baea0176820d93624b39ea61'
DEDUP_TERMINAL = ART/'axial-material-qualified-AB-rank1-factor-cache-memory-dedup-build-terminal-20261007/terminal_return.json'
DEDUP_TERMINAL_SHA = '09b904094ecaf1fcc7d9979a02bf95629d26f761c53c06e66a7dd2ce52bd070e'
CURRENT_CAPTURE_FACTORY = ROOT/'validation/axial_material/prepare_rank1_cache_memory_dedup_file_snapshot_native_angular_capture.py'
CURRENT_CAPTURE_FACTORY_SHA = '48ffa6568487bd4d57503cb9a6e8ee8b70ae7e24584e1757363a1ab4874bfc6c'
CAPTURE_SUCCESS_FACTORY = CURRENT_CAPTURE_FACTORY  # Original-operator diagnostic only; no combined-cold RSS credit.
CAPTURE_SUCCESS_FACTORY_SHA = CURRENT_CAPTURE_FACTORY_SHA
CAPTURE_SUCCESS_SEAL = '12756df88672c4438149119026edba0b2ef78780dffa5dcc522bcd06771d5296'
CAPTURE_SUCCESS_TERMINAL = ART/'axial-material-rank1-cache-memory-dedup-file-snapshot-native-angular-capture-terminal-20261007/terminal_return.json'
CAPTURE_SUCCESS_TERMINAL_SHA = 'd5496707eb1ad08826eec599dbf6035b9e39df67cf68a92e84db62bcbb753e63'
BINDING_CONTROLS_ACTUAL = None  # Future CLI passes true completed descriptor; none is never qualification.
COLD_TERMINAL = ART/'axial-material-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-file-snapshot-terminal-scipy-env-canonical-code-20261008'
CONTROL_TERMINAL = ART/'axial-material-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-file-snapshot-own-rss-terminal-scipy-env-canonical-code-20261008'
DRAFT_STATUS = 'REVIEWED_COLD_INPUT_REUSE_FACTORY_WITH_ACTUAL_BOUNDED_INTAKE'
SCHEMA = 'AXMAT_HISTORICAL_INPUT_OWNED_SPECS_SCIPY_ENV_COMBINED_FILE_SNAPSHOT_COLD_FACTORY_V1'
DECL_TERMINAL_SCHEMA = 'AXMAT_HISTORICAL_INPUT_OWNED_SPECS_SCIPY_ENV_COMBINED_FILE_SNAPSHOT_COLD_DECLARATION_ACTUAL_TERMINAL_V1'
COLD_TERMINAL_SCHEMA = 'AXMAT_HISTORICAL_INPUT_OWNED_SPECS_SCIPY_ENV_COMBINED_FILE_SNAPSHOT_COLD_ACTUAL_TERMINAL_V1'
COLD_TAIL = ('full_closeout_tail_gate','actual_elapsed_seconds','actual_archive_bytes','actual_resources')
ORIGINAL_COMPLETE_12_MAP_CASE_BYTES = 13265348616
ORIGINAL_COLD_RESERVE_BYTES = 20971764748
ORIGINAL_COMPLETE_SNAPSHOT_BYTES = 237955708
WORKING_SNAPSHOT_NAME = 'radial_snapshot_work.xsm'
OBSERVED_HISTORY_INPUT_ONLY = 73036237561
BUDGETS = dict(setup_seconds=120,bootstrap_axial_seconds=4200,bootstrap_radial_seconds=600,
    radial_seconds=300,axial_seconds=4200,host_seconds=120,max_maps=100,total_seconds=43200)
CORRECTION_SCOPE = ('Use physical NTOT0 and all self SIGW P0/P1/P2 for ISCAT3 axial assembly; '
    'preserve original radial P0/R, geometry/material/offline input/white/basis; '
    'retain exact lower-row and repeated-block storage with full-shape arithmetic; '
    'defer two unused SNAP deep copies to each first SPOLEAK using independent XSM work files; '
    'supervise every actual native/host child with genuine frozen OwnRSS512. '
    'No old numerical or independent-reference qualification is inherited.')
CONSTRUCTOR_BEFORE = '    executor = SerialExecutor(work, budget.total_seconds, case, resources)\n'
CONSTRUCTOR_AFTER = ('    from combined_cold_own_rss_host import make_executor\n'
    '    executor = make_executor(work, budget.total_seconds, case, resources,\n'
    '                             info["own_child_supervision"])\n')
DECK_HOOK = '    from combined_cold_file_snapshot_decks import defer_freshly_generated_axial_decks\n    generated_manifest_path = output / "decks/production_inputs.json"\n    generated_manifest = json.loads(generated_manifest_path.read_text())\n    original_generated_decks = {name: (output / "decks" / name).read_bytes()\n                                for name in generated_manifest["deck_sha256"]}\n    deferred_decks, deferred_proof = defer_freshly_generated_axial_decks(original_generated_decks)\n    for name in ("bootstrap_axial.x2m", "picard_axial.x2m"):\n        if generated_manifest["deck_sha256"][name] != deferred_proof["independent_deck_inverses"][name]["original_sha256"]:\n            raise Refusal("generator-only original complete deck identity differs")\n        (output / "decks" / name).write_bytes(deferred_decks[name])\n        generated_manifest["deck_sha256"][name] = sha256(output / "decks" / name)\n    generated_manifest["runner_deferred_snapshot_inputs"] = deferred_proof\n    dump_json(generated_manifest_path, generated_manifest)\n    dump_json(output / "decks/deferred_snapshot_inverse.json", deferred_proof)\n'

def digest(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()

def require(path, wanted=None):
    path = Path(path)
    if not path.is_file() or (wanted is not None and digest(path) != wanted):
        raise ValueError("missing or changed moment-order pipeline dependency: " + str(path))
    return path

def pin(path):
    path = require(path).resolve()
    return dict(path=str(path), sha256=digest(path))

def read(path):
    return json.loads(Path(path).read_text())

def write_new(path, data):
    with Path(path).open("x") as stream:
        json.dump(data, stream, indent=2, allow_nan=False)
        stream.write("\n")

def verify(files):
    for path, wanted in files.items():
        require(path, wanted)

def producer_environment():
    import numpy as np
    old_info = read(require(OLD / "prepared.json", PREPARED_SHA))
    path = require(PARENT_SOURCE / "analysis_environment.json")
    env = read(path)
    if (env["schema"] != "AXMAT_EXACT_OFFLINE_REPLAY_ENVIRONMENT_V1"
            or env["python_version"] != "3.14.4" or env["numpy_version"] != "2.4.4"
            or str(Path(sys.executable).resolve()) != env["executable"]
            or platform.python_version() != env["python_version"] or np.__version__ != env["numpy_version"]
            or str(Path(np.__file__).parent.resolve()) != env["numpy_root"]
            or any(os.environ.get(k) != "1" for k in THREADS)):
        raise ValueError("original exact offline producer Python3.14.4/NumPy2.4.4 and single threads required")
    verify(env["files"])
    for name, wanted in old_info["local_files"].items():
        require(OLD / name, wanted)
    for item in old_info["inputs"].values():
        require(item["path"], item["sha256"])
    for key in ("case_spec", "rank_addendum"):
        require(old_info[key]["path"], old_info[key]["sha256"])
    admitted=scipy_dependency_admission()
    helper=load(require(SCIPY_HELPER,SCIPY_HELPER_SHA),SCIPY_HELPER.stem)
    env=helper.expanded_environment(env,pin(path),admitted,
        dict(path=str(SCIPY_HELPER),sha256=SCIPY_HELPER_SHA))
    return old_info, env, path

def restore_metadata(candidate, parent, allowed, added=()):
    restored = copy.deepcopy(candidate)
    for keys in allowed:
        a, b = restored, parent
        for key in keys[:-1]:
            a, b = a[key], b[key]
        a[keys[-1]] = b[keys[-1]]
    for keys in added:
        a = restored
        for key in keys[:-1]:
            a = a[key]
        del a[keys[-1]]
    if restored != parent:
        raise ValueError("pipeline metadata changed outside explicit source/runtime identity fields")

def patched(original, replacements, target, allowed_functions=()):
    result = original
    for old, new in replacements:
        if result.count(old) != 1:
            raise ValueError("pipeline source anchor absent or ambiguous: " + old[:120])
        result = result.replace(old, new, 1)
    restored = result
    for old, new in reversed(replacements):
        if restored.count(new) != 1:
            raise ValueError("pipeline source restoration anchor is ambiguous")
        restored = restored.replace(new, old, 1)
    if restored != original:
        raise ValueError("source changed outside explicit admission additions")
    def definitions(text):
        return {n.name: ast.dump(n, include_attributes=False) for n in ast.parse(text).body
                if isinstance(n, (ast.FunctionDef, ast.ClassDef))}
    before, after = definitions(original), definitions(result)
    if (before.keys() != after.keys()
            or any(before[k] != after[k] for k in before if k not in allowed_functions)):
        raise ValueError("unlisted pipeline function or supervision/scientific gate changed")
    target.write_text(result)
    target.with_suffix(target.suffix + ".patch").write_text("".join(difflib.unified_diff(
        original.splitlines(True), result.splitlines(True),
        fromfile="frozen-actual-production-runtime", tofile="explicit-moment-order-admission")))
    return dict(candidate=pin(target), original_sha256=hashlib.sha256(original.encode()).hexdigest(),
        replacements=replacements, full_text_restored_byte_exact=True,
        unchanged_function_AST=sorted(set(before) - set(allowed_functions)),
        admitted_function_changes=list(allowed_functions))


def nonzero_sha(value):
    if type(value) is not str or re.fullmatch('[0-9a-f]{64}',value) is None or value=='0'*64:
        raise ValueError('actual nonplaceholder SHA256 required')
    return value


def require_input_ready():
    if sys.flags.optimize!=0 or 'PYTHONOPTIMIZE' in os.environ:
        raise ValueError('source predicates require optimize0 before project input read')
    if DRAFT_STATUS != 'REVIEWED_COLD_INPUT_REUSE_FACTORY_WITH_ACTUAL_BOUNDED_INTAKE':
        raise ValueError('UNREADY: no bounded intake, canonical cold fixture or business permission')
    for p in (FORMAL_FACTORY,COMBINED_FACTORY,COMBINED_BUILD,COMBINED_TERMINAL,COMBINED_RUNTIME,
              DECK_HELPER,CAPTURE_SUCCESS_FACTORY,CAPTURE_SUCCESS_TERMINAL,
              PRIVATE_INPUT_CONSUMER,COMPONENT_INTAKE_DESCRIPTOR):
        if p is None or not Path(p).is_absolute():raise ValueError('unbound actual canonical INPUT/source path')
    for s in (COMBINED_FACTORY_SHA,COMBINED_BUILD_SEAL,COMBINED_TERMINAL_SHA,
              COMBINED_RUNTIME_SHA,CAPTURE_SUCCESS_FACTORY_SHA,CAPTURE_SUCCESS_SEAL,CAPTURE_SUCCESS_TERMINAL_SHA,
              PRIVATE_INPUT_CONSUMER_SHA,COMPONENT_INTAKE_DESCRIPTOR_SHA):nonzero_sha(s)
    if Path(__file__).resolve()!=Path(FORMAL_FACTORY) or digest(__file__)!=nonzero_sha(os.environ.get('AXMAT_COLD_FACTORY_SHA256')):
        raise ValueError('TMP/source identity cannot perform a cold business action')


def factory_source_descriptor():
    require_input_ready()
    return dict(path=str(FORMAL_FACTORY),sha256=nonzero_sha(os.environ.get("AXMAT_COLD_FACTORY_SHA256")))


def add_expected(files,path,wanted):
    path=str(Path(path));nonzero_sha(wanted)
    if not Path(path).is_absolute() or '..' in Path(path).parts:raise ValueError('absolute typed owner required')
    if path in files and files[path]!=wanted:raise ValueError('expected owner SHA conflict: '+path)
    files[path]=wanted


def load(path,name):
    """Normal import only; existing different names/sources are refused."""
    p=require(path).resolve()
    old=sys.modules.get(name)
    if old is not None:
        if getattr(old,'__file__',None) is None or Path(old.__file__).resolve()!=p:
            raise ValueError('existing normal module binding differs: '+name)
        return old
    if name!=p.stem:raise ValueError('real ordinary module stem required')
    sys.path.insert(0,str(p.parent));m=importlib.import_module(name)
    if Path(m.__file__).resolve()!=p or m.__spec__ is None or Path(m.__spec__.origin).resolve()!=p:
        raise ValueError('normal import did not bind actual reviewed source')
    return m


def working_snapshot_storage_forecast():
    """Pure original planning-size metadata, never a live/resource/RSS admission.

    Original twelve-map planning and its reservation formula remain intact.
    Every real bootstrap/map working file is included by the original stage
    seal_directory, whole WORK namespace and live96GiB history accounting.
    Maximum100 is still a convergence bound, not a twelve-map size guarantee.
    """
    planning_maps=12
    planning_work_files=1+planning_maps
    maximum_work_files=1+BUDGETS['max_maps']
    work_bytes=planning_work_files*ORIGINAL_COMPLETE_SNAPSHOT_BYTES
    metadata_allowance=2**30
    return dict(schema='AXMAT_COMBINED_COLD_FILE_SNAPSHOT_STORAGE_FORECAST_INPUT_ONLY_V1',
        classification='PLANNING_INPUT_ONLY_NO_ACTUAL_OUTPUT_RESOURCE_OR_RSS_CREDIT',
        working_snapshot_name=WORKING_SNAPSHOT_NAME,storage_medium='XSM_FILE',
        original_complete_snapshot_bytes=ORIGINAL_COMPLETE_SNAPSHOT_BYTES,
        original_snapshot_size_is_planning_not_new_native_measurement=True,
        planning_previous_maps=planning_maps,planning_bootstrap_work_files=1,
        planning_map_work_files=planning_maps,planning_work_file_count=planning_work_files,
        planning_additional_work_bytes=work_bytes,
        original_complete_12_map_case_bytes=ORIGINAL_COMPLETE_12_MAP_CASE_BYTES,
        original_source_and_runtime_metadata_allowance_bytes=metadata_allowance,
        combined_SOURCE_and_WORK_planning_bytes=(ORIGINAL_COMPLETE_12_MAP_CASE_BYTES+work_bytes+metadata_allowance),
        original_reservation_bytes=ORIGINAL_COLD_RESERVE_BYTES,
        reservation_formula_and_amount_unchanged=True,all_actual_work_files_counted_by_original_namespace=True,
        maximum_maps=BUDGETS['max_maps'],maximum_possible_work_file_count=maximum_work_files,
        maximum_possible_work_file_bytes=maximum_work_files*ORIGINAL_COMPLETE_SNAPSHOT_BYTES,
        twelve_map_planning_is_not_maximum100_map_archive_guarantee=True,
        actual_dynamic_history_gate_required_for_every_stage=True,
        actual_snapshot_or_bootstrap_or_cold_RSS_proved=False,scientific_qualification=False)


def source_contract():
    return dict(schema=SCHEMA,status=DRAFT_STATUS,formal_factory=str(FORMAL_FACTORY),
        proposed_roots=[str(SOURCE),str(OUTPUT),str(COLD_TERMINAL),str(CONTROL_TERMINAL)],
        actual_component_scope='COMPLETE_FRESH_HISTORICAL_INPUT_REUSE_NOT_COMPONENT_API_REEXECUTION',
        standalone_bounded_intake_pins=dict(path=str(COMPONENT_INTAKE_DESCRIPTOR),sha256=COMPONENT_INTAKE_DESCRIPTOR_SHA),original_budgets=BUDGETS,
        original_reservation_bytes=ORIGINAL_COLD_RESERVE_BYTES,history_cap_bytes=96*2**30,free_floor_bytes=8*2**30,
        independent_working_snapshot_storage_forecast=working_snapshot_storage_forecast(),
        current_actual_storage_pass_claimed=False,initial_prepared_input_only=True,
        prepared_cold_only_added_field='own_child_supervision',original_Serial_class_byte_exact=True,
        original_layout_receiver_and_science_callers_byte_exact=True,
        genuine_scipy_additional_environment=scipy_environment_contract(),
        new_callback_only_metadata_INPUT_acquisition=True,whole_component_returns_preserved=True,
        new_callback_has_no_component_API_or_child_or_producer_modules_call=True,
        frozen_old_MRO_fixture_credit_inherited=False,new_binding_fixture_actual=None,
        actual_cold_positive_and_oversize_RootEXIT0_required=True,source_only_no_API_or_artifact_or_child=True)


def scipy_environment_contract():
    return dict(schema='AXMAT_COMPLETE_SCIPY_ADDITIONAL_COLD_ENVIRONMENT_V1',
        manifest=dict(path=str(SCIPY_MANIFEST),sha256=SCIPY_MANIFEST_SHA),
        helper=dict(path=str(SCIPY_HELPER),sha256=SCIPY_HELPER_SHA),
        expected_PYTHONPATH=str(SCIPY_TARGET_ROOT),complete_package_and_wheel_owned=True,
        original430_environment_fields_and_expected_entries_retained=True,
        normal_import_only_no_module_global_or_class_overlay=True,
        old_failed_prepare_factory=dict(path=str(FROZEN_FAILED_PREP_FACTORY),sha256=FROZEN_FAILED_PREP_FACTORY_SHA),
        old_failed_prepare_has_no_new_fixture_or_native_credit=True,
        new_cold_or_fixture_or_scientific_credit=False)


def scipy_dependency_admission(*, require_import=True):
    require_input_ready()
    helper=load(require(SCIPY_HELPER,SCIPY_HELPER_SHA),SCIPY_HELPER.stem)
    admitted=helper.dependency_admission(require_import=require_import)
    if (admitted['manifest']!=dict(path=str(SCIPY_MANIFEST),sha256=SCIPY_MANIFEST_SHA)
            or admitted['expected_PYTHONPATH']!=str(SCIPY_TARGET_ROOT)
            or admitted['native_transport_or_fixture_or_scientific_credit'] is not False):
        raise ValueError('complete independently pinned SciPy environment INPUT required')
    return admitted


def component_return_admission(physical,dedup,capture,combined,*,fresh_input_phase=None):
    prior=physical['inherited_rank1_cache_admission']
    memory=dedup['inherited_rank1_factor_cache_memory_admission']
    if (physical['schema']!='AXMAT_SPOASM_PHYSICAL_PRODUCTION_RUNTIME_INPUT_ADMISSION_V1'
        or physical['admission']!='SPOASM_PHYSICAL_ASSEMBLY_RUNTIME_INPUT_ONLY'
        or physical['build_root']!=str(PHYSICAL_BUILD) or physical['build_seal_sha256']!=PHYSICAL_SEAL
        or physical['actual_external_terminal_evidence']!=dict(path=str(PHYSICAL_TERMINAL),sha256=PHYSICAL_TERMINAL_SHA)
        or physical['collision_self_operator_unchanged'] is not False
        or any(physical[k] is not True for k in ('all_actual370x3_radial_inputs_and_physical_macro_moments_bitexact',
            'all_defined_original_archive_and_rebuilt_fields_bitexact','radial_P0_R_basis_source_and_recipe_unchanged',
            'legacy_scalar_assembly_bitexact','no_extra_2l_plus_1_in_self_coefficients','physical_data_unchanged',
            'angle_grid_unchanged','white_closure_unchanged','radial_arithmetic_unchanged'))
        or any(physical[k] is not False for k in ('actual_full_FLU_entry_executed',
            'new_transport_RSS_fitness_proved_by_assembly_controls','AAA_accuracy_qualified','ABA_admitted'))):
        raise ValueError('actual whole physical component INPUT-only contract differs')
    if (dedup['schema']!='AXMAT_RANK1_FACTOR_CACHE_MEMORY_DEDUP_PRODUCTION_RUNTIME_INPUT_ADMISSION_V1'
        or dedup['admission']!='RANK1_FACTOR_CACHE_MEMORY_DEDUP_RUNTIME_INPUT_ONLY'
        or dedup['build_root']!=str(DEDUP_BUILD) or dedup['build_seal_sha256']!=DEDUP_SEAL
        or dedup['actual_external_terminal_evidence']!=dict(path=str(DEDUP_TERMINAL),sha256=DEDUP_TERMINAL_SHA)
        or dedup['inherited_rank1_factor_cache_admission']!=prior
        or memory['inherited_rank1_factor_cache_admission']!=prior
        or any(dedup[k] is not True for k in ('lower_structural_zero_rows_losslessly_packed',
            'lower_repeated_blocks_losslessly_deduplicated','full_shape_MATMUL_and_RHS_order_unchanged',
            'all_original_memory_and_dictionary_controls_bitwise_passed',
            'canonical_dictionary_signed_zero_and_all_unique_fallback_verified',
            'dictionary_dimensions_indices_canonical_and_release_negative_controls_passed'))
        or any(dedup[k] is not False for k in ('native_RSS_proof_obtained','actual_full_FLU_entry_executed',
            'AAA_accuracy_qualified','ABA_admitted'))):raise ValueError('actual whole dedup/438/92 return differs')
    # Future successful capture schema must be the separately frozen observer factory's real return.
    if (capture['admission']!='CURRENT_MAP012_NATIVE_ANGULAR_DIAGNOSTIC_ONLY'
        or capture['capture_seal']['sha256']!=CAPTURE_SUCCESS_SEAL
        or capture['source']!=dict(path=str(CAPTURE_SUCCESS_FACTORY),sha256=CAPTURE_SUCCESS_FACTORY_SHA)
        or capture['actual_external_terminal_evidence']!=dict(path=str(CAPTURE_SUCCESS_TERMINAL),sha256=CAPTURE_SUCCESS_TERMINAL_SHA)
        or capture['inherited_current_build_admission']!=prior or capture['inherited_memory_build_admission']!=memory
        or capture['inherited_dedup_build_admission']!=dedup or capture['actual_native_RSS_under_512_guard_passed'] is not True
        or any(capture[k] is not False for k in ('scientific_qualification','AAA_accuracy_qualified','ABA_admitted','production_solver_promoted'))):
        raise ValueError('actual measured512 map012 diagnostic required; no cold/physical runtime equivalence')
    if (combined['schema']!=COMBINED_SCHEMA or combined['admission']!=COMBINED_ADMISSION
        or combined['build_root']!=str(COMBINED_BUILD) or combined['build_seal_sha256']!=COMBINED_BUILD_SEAL
        or combined['corrected_runtime']!=dict(path=str(COMBINED_RUNTIME),sha256=COMBINED_RUNTIME_SHA)
        or combined['actual_external_terminal_evidence']!=dict(path=str(COMBINED_TERMINAL),sha256=COMBINED_TERMINAL_SHA)
        or combined['actual_components']!=dict(original92=prior,physical=physical,dedup=dedup,capture=capture,
            mathematical_controls_inherited_not_newly_executed=True,
            capture_scope_is_original_operator_only=True,combined_runtime_RSS_not_proved=True)
        or combined['inherited_rank1_cache_admission']!=prior or combined['inherited_physical_admission']!=physical
        or combined['inherited_dedup_admission']!=dedup or combined['original_operator_capture_dependency']!=capture
        or combined['collision_self_operator_unchanged'] is not False
        or any(combined[k] is not False for k in ('combined_runtime_native_RSS_proved',
            'actual_full_FLU_entry_executed','native_transport_executed','AAA_accuracy_qualified','ABA_admitted'))):
        raise ValueError('actual standalone whole combined-runtime INPUT admission differs')
    files=combined['descriptor_files']
    if type(files) is not dict or any(not Path(p).is_absolute() for p in files):
        raise ValueError('complete canonical expected input owner union required')
    if (type(fresh_input_phase)is not dict or fresh_input_phase.get('semantics')!=INPUT_REUSE_SEMANTICS
        or fresh_input_phase.get('original_component_APIs_executed_in_this_process')is not False
        or fresh_input_phase.get('consumer_scope_used')is not False
        or fresh_input_phase.get('science_qualification')is not False):
        raise ValueError('whole component equality requires the just-completed full fresh INPUT phase')
    if combined['component_INPUT_semantics']!='HISTORICAL_PREP_REUSE_WITH_COMPLETE_FRESH_PHASES_NOT_API_REEXECUTION' or combined['original_component_APIs_executed_now']is not False:
        raise ValueError('ancestor historical INPUT reuse must not be relabelled as API reexecution')
    return dict(original92=prior,memory438=memory,physical=physical,dedup=dedup,capture=capture,combined=combined)


def input_consumer():
    require_input_ready()
    name='cold_component_input_consumer';old=sys.modules.get(name)
    choices=[SOURCE/(name+'.py'),OUTPUT/'runtime'/(name+'.py'),Path(PRIVATE_INPUT_CONSUMER)]
    current=sys.modules.get('production_runner')
    if current is not None:
        runtime=Path(current.__file__).parent
        if runtime not in (SOURCE,OUTPUT/'runtime') or current.__spec__ is None or current.__spec__.origin!=str(runtime/'production_runner.py'):
            raise ValueError('normally bound current cold controller source required')
        choices=[runtime/(name+'.py')]
    if old is not None:
        actual=Path(old.__file__)
        if actual not in choices:raise ValueError('foreign normally imported INPUT consumer source')
        require(actual,PRIVATE_INPUT_CONSUMER_SHA)
        if old.__spec__ is None or old.__spec__.origin!=str(actual):raise ValueError('actual INPUT consumer spec differs')
        return old
    path=next((p for p in choices if p.is_file()),None)
    if path is None:raise ValueError('actual independently source-pinned consumer missing')
    return load(require(path,PRIVATE_INPUT_CONSUMER_SHA),name)


def component_current_context(metadata=None, *, allow_unbound_initial=False):
    if metadata is None:
        if not allow_unbound_initial:raise ValueError('explicit initial INPUT-only phase required')
        info=read(require(OLD/'prepared.json',PREPARED_SHA))
        roots=sorted(set(info['resource_roots'])|{str(p)for p in ART.glob('axial-material-*')}|
            {str(SOURCE),str(OUTPUT),str(COLD_TERMINAL),str(CONTROL_TERMINAL)})
        return dict(resource_roots=roots,resource_info={k:info[k]for k in ('artifact_root','resource_roots','case_spec')},
            runtime_context=None,allow_unbound_initial_INPUT_declaration=True,additional_expected_files={})
    consumer=input_consumer();runtime=Path(consumer.__file__).parent
    if runtime not in (SOURCE,OUTPUT/'runtime'):raise ValueError('actual copied cold metadata consumer required')
    return dict(resource_roots=metadata['component_resource_roots'],resource_info=metadata['component_resource_info'],
        runtime_context=dict(root=str(runtime),files=metadata['component_runtime_file_hashes']),
        allow_unbound_initial_INPUT_declaration=False,additional_expected_files=metadata['files'])


def component_intake():
    require_input_ready()
    value=read(require(COMPONENT_INTAKE_DESCRIPTOR,COMPONENT_INTAKE_DESCRIPTOR_SHA))
    if value['schema']!=INPUT_REUSE_SCHEMA or value['semantics']!=INPUT_REUSE_SEMANTICS:
        raise ValueError('actual immutable complete INPUT-intake schema required')
    if 'binding_descriptor' in value:
        raise ValueError('INPUT descriptor must not contain a circular SHA of its own bytes')
    return dict(value,binding_descriptor=dict(path=str(COMPONENT_INTAKE_DESCRIPTOR),sha256=COMPONENT_INTAKE_DESCRIPTOR_SHA))


def materialize_metadata(metadata, admission_descriptor, *, phase):
    require_input_ready();scipy_dependency_admission()
    if metadata['schema']!=CALLBACK_METADATA_SCHEMA or metadata['component_input_intake']!=component_intake():
        raise ValueError('compact INPUT metadata binding changed')
    context=component_current_context(metadata)
    for item in (admission_descriptor,dict(path=str(Path(input_consumer().__file__)),sha256=PRIVATE_INPUT_CONSUMER_SHA)):
        add_expected(context['additional_expected_files'],item['path'],item['sha256'])
    data=dict(metadata);data['component_current_context']=context
    expanded,evidence=input_consumer().consume_metadata(data,phase=phase)
    component_return_admission(expanded['actual_components']['physical'],expanded['actual_components']['dedup'],
        expanded['actual_components']['capture'],expanded['actual_components']['combined'],fresh_input_phase=evidence)
    scipy_dependency_admission()
    return expanded


def completed_components():
    require_input_ready()
    if SOURCE.is_dir():
        d=read(require(SOURCE/'declaration.json'))
        item=d['rank1_factor_cache_revision']
        metadata=read(require(item['path'],item['sha256']))
        return materialize_metadata(metadata,item,phase='factory/metadata-reuse')['actual_components']
    scipy_dependency_admission()
    consumer=input_consumer();binding=component_intake()
    components,evidence=consumer.consume_completed_inputs(binding,component_current_context(allow_unbound_initial=True),
        phase='factory/initial-INPUT-declaration')
    result=component_return_admission(components['physical'],components['dedup'],components['capture'],components['combined'],fresh_input_phase=evidence)
    scipy_dependency_admission()
    return result


def complete_history_resources(roots):
    require_input_ready()
    m=load(require(BUILD_FACTORY,BUILD_FACTORY_SHA),BUILD_FACTORY.stem)
    return m.DynamicHistoryResources(ART,[str(p) for p in roots],8*2**30,96*2**30)


def build_terminal_chain(admitted):
    # Original92 whole return is retained; this proof remains an ancestor INPUT only.
    chain=dict(factory=pin(require(BUILD_FACTORY,BUILD_FACTORY_SHA)),declaration=pin(BUILD/'declaration.json'),
        build_seal=pin(BUILD/'seal.json'),driver_result=pin(BUILD/'driver_result.json'),
        full_stdout=admitted['actual_external_terminal_validation']['full_stdout'],
        terminal_evidence=admitted['actual_external_terminal_evidence'])
    for item in chain.values():require(item['path'],item['sha256'])
    return chain


def namespace(root):
    root=Path(root)
    if root.is_symlink() or not root.is_dir():raise ValueError('actual nonalias owned root required')
    files={};dirs=[];links={}
    for p in sorted(root.rglob('*')):
        rel=p.relative_to(root).as_posix()
        if p.is_symlink():links[rel]=dict(text=os.readlink(p),target=str(p.resolve(strict=True)))
        elif p.is_dir():dirs.append(rel)
        elif p.is_file():files[rel]=digest(p)
        else:raise ValueError('nonregular namespace member')
    return dict(files=files,directories=dirs,symlinks=links)


def check_flat_namespace(root,files):
    actual=namespace(root)
    if actual['directories'] or actual['symlinks'] or set(actual['files'])!=set(files):
        raise ValueError('exact flat code/source namespace required')
    if any(actual['files'][name]!=wanted for name,wanted in files.items()):raise ValueError('source bytes changed')


def definition_sources(source):
    return {n.name:ast.get_source_segment(source,n) for n in ast.parse(source).body
            if isinstance(n,(ast.FunctionDef,ast.ClassDef))}


def render_controller(original,runtime_sha):
    nonzero_sha(runtime_sha)
    if hashlib.sha256(original.encode()).hexdigest()!=BASE_CONTROLLER_SHA:raise ValueError('entire actual844 source required')
    replacements=[];candidate=original
    def change(old,new):
        nonlocal candidate
        if candidate.count(old)!=1:raise ValueError('one exact original controller anchor required')
        candidate=candidate.replace(old,new,1);replacements.append([old,new])
    change('DRAGON_SHA = "'+BASE_RUNTIME_SHA+'"','DRAGON_SHA = "'+runtime_sha+'"')
    anchor='    shutil.copy2(Path(__file__).with_name("rank1_factor_cache_admission.json"), runtime / "rank1_factor_cache_admission.json")'
    change(anchor,anchor+'\n    shutil.copy2(Path(__file__).with_name("combined_cold_own_rss_host.py"), runtime / "combined_cold_own_rss_host.py")'
        +'\n    shutil.copy2(Path(__file__).with_name("combined_cold_own_rss_controls.py"), runtime / "combined_cold_own_rss_controls.py")'
        +'\n    shutil.copy2(Path(__file__).with_name("combined_cold_file_snapshot_decks.py"), runtime / "combined_cold_file_snapshot_decks.py")'
        +'\n    shutil.copy2(Path(__file__).with_name("cold_component_input_consumer.py"), runtime / "cold_component_input_consumer.py")')
    change('    write_inputs(output / "decks", config)\n','    write_inputs(output / "decks", config)\n'+DECK_HOOK)
    change(CONSTRUCTOR_BEFORE,CONSTRUCTOR_AFTER)
    restored=candidate
    for old,new in reversed(replacements):
        if restored.count(new)!=1:raise ValueError('complete source inverse anchor changed')
        restored=restored.replace(new,old,1)
    if restored!=original:raise ValueError('complete controller source inverse differs')
    before,after=definition_sources(original),definition_sources(candidate)
    if set(before)!=set(after) or any(before[k]!=after[k] for k in before if k not in ('prepare','run')):
        raise ValueError('unlisted class/resource/scientific/qualification source changed')
    if after['run'].replace(CONSTRUCTOR_AFTER,CONSTRUCTOR_BEFORE,1)!=before['run']:
        raise ValueError('original c.run must retain every byte except one constructor callsite')
    return candidate,dict(schema='AXMAT_COMBINED_FILE_SNAPSHOT_COLD_844_FULL_SOURCE_INVERSE_V1',
        original_sha256=BASE_CONTROLLER_SHA,candidate_sha256=hashlib.sha256(candidate.encode()).hexdigest(),
        replacements=replacements,whole_inverse_byte_exact=True,whole_SerialExecutor_byte_exact=True,
        unchanged_definitions=sorted(set(before)-{'prepare','run'}),run_only_one_genuine_constructor=True,
        prepare_only_four_source_copies_two_complete_copy_permutations_and_two_file_medium_declarations=True,
        original_write_inputs_byte_exact=True,all_original_budgets_unchanged=True,actual_fixture_credit=False)


def write_controller(original,runtime_sha,target):
    candidate,proof=render_controller(original,runtime_sha)
    target.write_text(candidate)
    proof['candidate']=pin(target)
    target.with_suffix('.py.patch').write_text(''.join(difflib.unified_diff(original.splitlines(True),candidate.splitlines(True))))
    return proof



def verify_baseline_package(original_info):
    data=read(require(BASE_WORK/'prepared.json',BASE_PREPARED_SHA))
    require(BASE_FACTORY,BASE_FACTORY_SHA)
    for name,wanted in data['local_files'].items():require(BASE_WORK/name,wanted)
    if data['production_config']!=original_info['production_config'] or data['budgets']!=BUDGETS:
        raise ValueError('actual original844 prepared contract differs from original input/config/caps')
    for name,item in original_info['inputs'].items():
        if name!='material_results' and data['inputs'][name]!=item:
            raise ValueError('physical/material baseline input differs')
    return data


def guard_owner_files():
    folder=FULL/'preflight/live_guard'
    path=require(folder/'guard_controls.json','ae4d7e86423a187c29efd5bf87d54053081d7b7fcf18ac88cd9e49639cb07454')
    guard=read(path)
    files={str(path):'ae4d7e86423a187c29efd5bf87d54053081d7b7fcf18ac88cd9e49639cb07454'}
    add_expected(files,folder/'tested_driver_source.py',guard['source_sha256'])
    for name,wanted in guard['control_files'].items():
        if Path(name).is_absolute() or '..' in Path(name).parts:raise ValueError('typed relative original guard member')
        add_expected(files,folder/name,wanted)
    # These are actual source pins, never a fixture PASS for the new MRO.
    for path,wanted in ((BASE_CONTROLLER,BASE_CONTROLLER_SHA),
        (ROOT/'validation/axial_material/qualify_refined_AAA_layered_full.py','70516d764e05cffa6e82e780a991ff64e56b9c29bc99f3f1b18bcb0ff63195c6'),
        (ROOT/'validation/axial_material/prepare_qualified_AB_source_factor_production.py','619ed1e3115e0f9f25fd20cc259d384891f2fff52d913acebd5d9ca8f39d5743'),
        (ROOT/'validation/axial_material/prepare_qualified_AB_moment_order_production.py','fe81150fbf270cac44e241ad64f352cf2f623fa65f7ccb4a9b0ded0a4f2c2d41')):
        add_expected(files,path,wanted)
    source_decl=FULL/'declaration.json'
    source_decl_sha='f032eee5a6dfb9844a57043d1a357a8bfe383f2d6c2c71761841717f3ed6c94b'
    actual_source_owners=read(require(source_decl,source_decl_sha))['files']
    actual_project_sources={path:wanted for path,wanted in actual_source_owners.items()
                            if Path(path).is_relative_to(ROOT/'validation') and Path(path).suffix=='.py'}
    expected_project_sources={'/Users/wen/spot/validation/axial_material/probe_refined_AAA_white_odd_response.py': '304a3111081e9ce5085eafb350716c5684e4bd4b19c2d9888604bbfc59e6d2bf', '/Users/wen/spot/validation/iterative/qualify_native_signed_axial.py': '395f3b11233614a8a945f754f69c8ad0c140af7ca1c88f5f288ced2fd7797f8a', '/Users/wen/spot/validation/artifacts/axial-material-production-qualified-AB-white-trace-refined-envpin-20261005/runtime/production_runner.py': '38de03ed0f5b3e2d82b4153a45d1e548d58a34747f526f8bcd51bbe01e935128', '/Users/wen/spot/validation/artifacts/axial-material-production-qualified-AB-white-trace-refined-envpin-20261005/runtime/snapshot_control_preflight.py': 'f60309e54947de8dc43e7080fd19ca6255652d840493db23b37ff7003c6a0819', '/Users/wen/spot/validation/artifacts/axial-material-production-qualified-AB-white-trace-refined-envpin-20261005/runtime/qualified_snapshot_ingestion.py': '4ea482a6f3536bdb61e0de2c0693a8f128893fd7e0ecdaa72b7bd424645f8658', '/Users/wen/spot/validation/axial_material/white_side_trace_kernel.py': '999b28a3f2b9ccc2adda075f421f85478b669efb22af4681881111883a69087b', '/Users/wen/spot/validation/artifacts/axial-material-AAA-white-trace-refined-native-odd-response-20261005/runtime/run_bounded_dragon.py': 'bc4ff7a5dc82ed023b726f2304b6a298954f54d7891414925b7d6d68dd80cf09', '/Users/wen/spot/validation/axial_material/measure_refined_AAA_native_angular_response.py': 'a4c28d6b26dcd79f53b65f8b44e9d1256ce392e5028423349fd842f40baf882e', '/Users/wen/spot/validation/artifacts/axial-material-AAA-white-trace-refined-native-angular-response-20261005/runtime/run_bounded_dragon.py': 'bc4ff7a5dc82ed023b726f2304b6a298954f54d7891414925b7d6d68dd80cf09', '/Users/wen/spot/validation/axial_material/qualify_refined_AAA_layered_input_pilot.py': 'f0477135df43bbfaf02403f389c27b8ee2d47f79d85437a7b3c97eb829ea5061', '/Users/wen/spot/validation/artifacts/axial-material-AAA-white-trace-refined-layered-input-pilot-20261005/runtime/run_bounded_dragon.py': 'bc4ff7a5dc82ed023b726f2304b6a298954f54d7891414925b7d6d68dd80cf09', '/Users/wen/spot/validation/iterative/native_layered_cached.py': '5f3dc64a87f37c053b17f780eeb857c86bcd8a34c2f6f0ad11094fa4934f611d', '/Users/wen/spot/validation/iterative/native_layered_reference.py': 'abe05996b031f899c700b7aedfd75922e52f1cfef9966cea117342f19c9938ab', '/Users/wen/spot/validation/iterative/native_oblique_streaming.py': 'dabb6dbd1373f8c12f27ccb02c4d60b22cc5ba6852ce8341664322faf7805f53', '/Users/wen/spot/validation/axial_material/qualify_refined_AAA_layered_full.py': '70516d764e05cffa6e82e780a991ff64e56b9c29bc99f3f1b18bcb0ff63195c6', '/Users/wen/spot/validation/axial_material/run_refined_AAA_layered_full_batch.py': '8eb8fa32b52704682fef069a5ddd81e4e96fb66573c82650df5d093ad6023236', '/Users/wen/spot/validation/axial_material/audit_refined_AAA_layered_full.py': 'b9910396b3c0e3546a0427ceb6d22a8f5642e1dcb22d77ec1e6c02d8a9409899', '/Users/wen/spot/validation/iterative/native_layered_full_action.py': '7e41ed0bc2587c810a8f18a886447e398f30c53272dc27d432b6af8813b68b8e', '/Users/wen/spot/validation/iterative/test_native_layered_full_action.py': '3f21e216588a02065958d97e8316728d0c5a9f93af93bb95e58bf69ced351c13', '/Users/wen/spot/validation/iterative/audit_native_layered_full.py': 'eaa890e0c696a46fff1f4cb435ee9a1f724d5d873922f50f161f5ab87e340e2b', '/Users/wen/spot/validation/iterative/native_layered_batch_storage.py': 'a1bc78b37646592b40ed3b7098294cb27b12bf7ffc69d0515151ef930a6c956c', '/Users/wen/spot/validation/iterative/native_layered_storage.py': '2392451477853704466d03b0e64442ca5a3103db34f41034f3b8c0f50287fdc0', '/Users/wen/spot/validation/iterative/native_layered_transport.py': '09eafc292b84ab0f2eeb37b1d56433eead5fc79f1889eded5d336088d0130609', '/Users/wen/spot/validation/iterative/calibrate_native_oblique_streaming.py': '3b9ece36d7a1428922df1476322a79888f2b7f91e977de23ac37bd0ea6485ea0', '/Users/wen/spot/validation/artifacts/axial-material-AAA-white-trace-refined-layered-full-20261005/runtime/run_bounded_dragon.py': 'bc4ff7a5dc82ed023b726f2304b6a298954f54d7891414925b7d6d68dd80cf09', '/Users/wen/spot/validation/artifacts/axial-material-AAA-white-trace-refined-layered-full-20261005/preflight/live_guard/tested_driver_source.py': 'c194e958d080585abb82a2affee4e6974c44d2d9e8527b599ed648dd49c52285'}
    if len(actual_project_sources)!=26 or actual_project_sources!=expected_project_sources:
        raise ValueError('entire26 original supervisor source-owner set differs')
    add_expected(files,source_decl,source_decl_sha)
    # These26 exact immutable source owners bind genuine705/probe imports.
    # They are INPUT bytes, not component API predicates or prior MRO fixture credit.
    for path,wanted in expected_project_sources.items():add_expected(files,path,wanted)
    for path,wanted in scipy_dependency_admission(require_import=False)['files'].items():
        add_expected(files,path,wanted)
    add_expected(files,SCIPY_HELPER,SCIPY_HELPER_SHA)
    add_expected(files,FROZEN_FAILED_PREP_FACTORY,FROZEN_FAILED_PREP_FACTORY_SHA)
    verify(files);return files

ADMISSION_HOST = '"""Actual terminal admission, axial selector and exact rank1 cache log guards."""\nimport copy\nimport hashlib\nimport importlib\nimport importlib.util\nimport json\nfrom pathlib import Path\nimport re\nimport sys\n\nEXPECTED_BUILD_ROOT = __BUILD_ROOT__\nEXPECTED_BUILD_SEAL = __BUILD_SEAL__\nEXPECTED_RUNTIME_SHA = __RUNTIME_SHA__\nEXPECTED_RUNTIME_PATH = __RUNTIME_PATH__\nFACTORY_DESCRIPTOR = __FACTORY_DESCRIPTOR__\nEXPECTED_PARENT_PREPARED_SHA = __PREPARED_SHA__\nEXPECTED_BUILD_FACTORY = __BUILD_FACTORY__\nEXPECTED_BUILD_FACTORY_SHA = __BUILD_FACTORY_SHA__\nEXPECTED_TERMINAL_EVIDENCE = __TERMINAL_EVIDENCE__\nEXPECTED_TERMINAL_VALIDATION = __TERMINAL_VALIDATION__\nEXPECTED_TERMINAL_CHAIN = __TERMINAL_CHAIN__\nEXPECTED_CORRECTION_SCOPE = __CORRECTION_SCOPE__\nEXPECTED_RESOURCE_SCOPE_CONTRACT = __RESOURCE_SCOPE_CONTRACT__\nOBSERVER_PREFIX = "AXMAT-MOMENT-ORDER SELECTOR "\nOBSERVER_EXPECTED = [32, 3, 2, 3, 1]\nHISTORY_SCOPE_POLICY = "AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1"\nCACHE_OBSERVER_PREFIX = "AXMAT-RANK1-CACHE TERMINAL "\nCACHE_BUDGET_BYTES = 512 * 2**20\nCACHE_OBSERVER_CONTRACT = dict(prefix=CACHE_OBSERVER_PREFIX,\n    columns=["builtblocks", "reusedblocks", "validated_hits", "peak_accounted_bytes", "cap_bytes"],\n    cap_bytes=CACHE_BUDGET_BYTES, exact_operator_identity_required=True,\n    positive_build_reuse_and_validation_required=True, all_actual_full_logs_required=True)\n\n\ndef require(path, wanted):\n    path = Path(path)\n    with path.open("rb") as stream:\n        observed = hashlib.file_digest(stream, "sha256").hexdigest()\n    if observed != wanted:\n        raise ValueError("moment-order admission dependency changed: " + str(path))\n    return path\n\n\ndef actual_build_factory():\n    factory = require(EXPECTED_BUILD_FACTORY, EXPECTED_BUILD_FACTORY_SHA)\n    name = factory.stem\n    old = sys.modules.get(name)\n    if old is not None and Path(old.__file__).resolve()!=factory.resolve():\n        raise ValueError("existing actual resource factory binding differs")\n    sys.path.insert(0,str(factory.parent));builder=importlib.import_module(name)\n    if Path(builder.__file__).resolve()!=factory.resolve():\n        raise ValueError("normally imported genuine resource factory differs")\n    return builder\n\n\ndef complete_history_resources(artifacts_root, roots, min_free_bytes, max_bytes, failure_type):\n    builder = actual_build_factory()\n    return builder.DynamicHistoryResources(artifacts_root, roots, min_free_bytes, max_bytes, failure_type)\n\n\ndef metadata(item):\n    path = require(item["path"], item["sha256"])\n    local = require(Path(__file__).with_name("rank1_factor_cache_admission.json"), item["sha256"])\n    data = json.loads(local.read_text())\n    if (data[\'schema\']!=\'AXMAT_HISTORICAL_INPUT_OWNED_SPECS_SCIPY_ENV_COMBINED_FILE_SNAPSHOT_COLD_INPUT_ADMISSION_V1\'\n        or data[\'correction_scope\']!=EXPECTED_CORRECTION_SCOPE\n        or data[\'resource_scope_policy\']!=HISTORY_SCOPE_POLICY\n        or data[\'resource_scope_contract\']!=EXPECTED_RESOURCE_SCOPE_CONTRACT\n        or data[\'combined_runtime\']!=dict(path=EXPECTED_RUNTIME_PATH,sha256=EXPECTED_RUNTIME_SHA)\n        or data[\'collision_self_operator_unchanged\'] is not False\n        or any(data[k] is not True for k in (\'physical_inputs_unchanged\',\'common_training_unchanged\',\n            \'white_closure_unchanged\',\'radial_arithmetic_unchanged\',\'original_controls_and_gates_unchanged\',\n            \'fresh_training_bootstrap_and_maps_required\',\'all_actual_axial_selector_observers_required\',\n            \'all_actual_rank1_factor_cache_observers_required\',\'reference_reassessment_pending\',\n            \'old_reference_recipe_is_dependency_only\',\n            \'new_actual_prepared_status_observables_physical_and_collector_receipt_rebinding_required\'))\n        or any(data[k] is not False for k in (\'old_moment_closure_numerical_replay_claimed\',\'CE_fitting\',\n            \'reference_qualification_created\',\'AAA_accuracy_qualified\',\'ABA_admitted\'))):\n        raise ValueError(\'truthful combined-runtime INPUT contract required\')\n    fpath=require(FACTORY_DESCRIPTOR[\'path\'],FACTORY_DESCRIPTOR[\'sha256\'])\n    stem=fpath.stem\n    old=sys.modules.get(stem)\n    if old is not None and Path(old.__file__).resolve()!=fpath.resolve():raise ValueError(\'foreign factory binding\')\n    sys.path.insert(0,str(fpath.parent));factory=importlib.import_module(stem)\n    if Path(factory.__file__).resolve()!=fpath.resolve():raise ValueError(\'actual normal factory source changed\')\n    data=factory.materialize_metadata(data,item,phase=\'private-rank1/metadata\')\n    actual=data[\'actual_components\']\n    if (actual!=data[\'actual_components\'] or actual[\'original92\']!=data[\'build_admission\']\n        or actual[\'combined\']!=data[\'combined_runtime_admission\']\n        or actual[\'combined\'][\'corrected_runtime\']!=data[\'combined_runtime\']):\n        raise ValueError(\'entire actual dual/capture/combined admission return changed\')\n    return data\n\n\ndef admit_actual_axial_selector(text, log):\n    log = Path(log)\n    if log.read_text(errors="replace") != text:\n        raise ValueError("axial selector guard must consume the complete actual archived solver log")\n    rows = []\n    stem = OBSERVER_PREFIX.rstrip()\n    pattern = re.compile(r"\\s*" + re.escape(stem) + r"\\s+([+-]?\\d+)\\s+([+-]?\\d+)\\s+([+-]?\\d+)\\s+([+-]?\\d+)\\s+([+-]?\\d+)\\s*")\n    for line_number, line in enumerate(text.splitlines(), 1):\n        if stem not in line:\n            continue\n        match = pattern.fullmatch(line)\n        if match is None:\n            raise ValueError("malformed actual axial selector observer at line " + str(line_number))\n        values = [int(value) for value in match.groups()]\n        if values != OBSERVER_EXPECTED:\n            raise ValueError("actual axial selector differs at line " + str(line_number) + ": " + str(values))\n        rows.append(dict(line=line_number, actual=values))\n    if not rows:\n        raise ValueError("mandatory actual axial selector observer is missing")\n    with log.open("rb") as stream:\n        observed = hashlib.file_digest(stream, "sha256").hexdigest()\n    return dict(status="PASS", log=dict(path=str(log.resolve()), sha256=observed),\n        observer_prefix=OBSERVER_PREFIX, expected=OBSERVER_EXPECTED, actual_observers=rows,\n        all_actual_observers_checked=True, complete_solver_log_checked=True,\n        scientific_accuracy_qualification=False)\n\n\ndef admit_actual_rank1_factor_cache(text, log, selector_count):\n    log = Path(log)\n    if log.read_text(errors="replace") != text:\n        raise ValueError("cache guard requires the complete actual archived solver log")\n    if type(selector_count) is not int or selector_count < 1:\n        raise ValueError("complete actual axial selector count is required")\n    rows = []\n    stem = CACHE_OBSERVER_PREFIX.rstrip()\n    for line_number, line in enumerate(text.splitlines(), 1):\n        if stem not in line:\n            continue\n        words = line.split()\n        if (len(words) != 7 or words[:2] != stem.split()\n                or any(re.fullmatch("[0-9]+", word) is None for word in words[2:])):\n            raise ValueError("malformed actual rank1 cache observer at line " + str(line_number))\n        values = [int(word) for word in words[2:]]\n        built, reused, validated, peak, cap = values\n        if (not all(value > 0 for value in values) or cap != CACHE_BUDGET_BYTES or peak > cap\n                or built % 49 != 0 or reused % 49 != 0 or built > 370 * 49\n                or validated < reused // 49):\n            raise ValueError("actual rank1 cache reuse/operator/resource guard differs at line " + str(line_number))\n        rows.append(dict(line=line_number, actual=values))\n    if len(rows) != selector_count:\n        raise ValueError("every actual completed axial FLU selector requires its cache terminal record")\n    with log.open("rb") as stream:\n        observed = hashlib.file_digest(stream, "sha256").hexdigest()\n    return dict(schema="AXMAT_RANK1_FACTOR_CACHE_ACTUAL_FULL_LOG_GUARD_V1", status="PASS",\n        log=dict(path=str(log.resolve()), sha256=observed), observer_contract=CACHE_OBSERVER_CONTRACT,\n        selector_count=selector_count, actual_observers=rows, all_actual_observers_checked=True,\n        complete_solver_log_checked=True, fixed_operator_identity_validation_recorded=True,\n        cache_budget_is_not_a_process_RSS_measurement=True, scientific_accuracy_qualification=False)\n\n\ndef admit_rank1_factor_cache_variant(variant):\n    revision = variant.get("rank1_factor_cache_revision", {})\n    data = metadata(revision["admission"])\n    if (variant["candidate_runtime"] != data["combined_runtime"]\n            or revision.get("fresh_complete_coupling_required") is not True\n            or revision.get("physical_inputs_changed") is not False\n            or revision.get("white_closure_changed") is not False\n            or revision.get("original_thresholds_changed") is not False):\n        raise ValueError("new runtime variant differs from moment-order build admission")\n    parent_item = data["parent_variant"]\n    parent = json.loads(require(parent_item["path"], parent_item["sha256"]).read_text())\n    restored = copy.deepcopy(variant)\n    for key in ("candidate_runtime", "files"):\n        restored[key] = parent[key]\n    del restored["rank1_factor_cache_revision"]\n    if restored != parent:\n        raise ValueError("original layout, white-trace operator or parent admissions changed")\n    return dict(status="PASS_SEALED_RANK1_FACTOR_CACHE_RUNTIME_INPUT_ONLY", scientific_qualification=False)\n\n\ndef admit_rank1_factor_cache_receiver(receipts, resolved, spec):\n    data = metadata(receipts["rank1_factor_cache_revision"])\n    if receipts["online_receiver_sha256"] != EXPECTED_RUNTIME_SHA:\n        raise ValueError("new receiver identity is not the independently controlled runtime")\n    old_item = data["parent_producer_receipt"]\n    old = json.loads(require(old_item["path"], old_item["sha256"]).read_text())\n    restored = copy.deepcopy(receipts)\n    for key in ("online_receiver_sha256", "conditional_white_receiver_variant", "scope"):\n        restored[key] = old[key]\n    del restored["rank1_factor_cache_revision"]\n    if restored != old:\n        raise ValueError("original offline producer, payload, mirror or training records changed")\n    for name, pin in data["original_inputs"].items():\n        if name != "material_results" and resolved[name] != pin:\n            raise ValueError("physical/material input changed: " + name)\n    if (spec["production"]["groups"] != 370 or spec["production"]["scat"] != 3\n            or spec["production"]["sn"] != 32 or spec["geometry"]["cells_per_zone"] != 16\n            or spec["basis"]["requested_rank"] != 1 or spec["basis"]["training_slots"] != list("ABA")):\n        raise ValueError("moment-order runtime cannot substitute a proxy geometry or training set")\n    return dict(status="PASS_SAME_OFFLINE_PRODUCERS_AND_LEGACY_BOOT_INPUTS", runtime_correction_is_online_only=True)\n'
def declare():
    require_input_ready()
    if os.path.lexists(SOURCE) or os.path.lexists(OUTPUT) or os.path.lexists(COLD_TERMINAL) or os.path.lexists(CONTROL_TERMINAL):
        raise ValueError("fresh independent source and complete-coupling output roots required; no retry or overwrite")
    info, producer_env, env_path = producer_environment()
    verify_baseline_package(info)
    components = completed_components()
    combined = components["combined"]
    admitted = components["original92"]
    terminal_chain = build_terminal_chain(admitted)
    contract = admitted["future_contract"]
    if (contract["original_prepared"] != pin(OLD / "prepared.json")
            or contract["production_config"] != info["production_config"]
            or contract["budgets"] != info["budgets"] or contract["inputs"] != info["inputs"]
            or contract["retained_reference"]["active_batches"] != 2000
            or contract["retained_reference"]["active_statepoints"] != [
                f"statepoint.{batch:04d}.h5" for batch in range(101, 2101)]
            or contract["producer_environment"]["path"] != str(env_path)
            or contract["producer_environment"]["sha256"] != digest(env_path)):
        raise ValueError("original production input/configuration/budget and full reference contract required")
    runtime = combined["corrected_runtime"]
    require(runtime["path"], runtime["sha256"])
    parent_variant = read(OLD / "runtime/conditional_white_receiver_variant.json")
    parent_receipt = read(info["inputs"]["material_results"]["path"])
    parent_spec = read(info["case_spec"]["path"])
    parent_resource_addendum = parent_spec["conditional_white_trace_trial"]["resource_addendum"]
    parent_resource = read(require(parent_resource_addendum["path"], parent_resource_addendum["sha256"]))
    if (parent_spec["resource_caps"]["new_case_artifact_budget_GiB"] != 96
            or parent_spec["resource_caps"]["disk_min_free_GiB"] != 8
            or parent_resource["prior_storage_budget_GiB"] != 40
            or parent_resource["new_storage_budget_GiB"] != 96 or parent_resource["min_free_GiB"] != 8):
        raise ValueError("actual complete-history 96 GiB/free8 GiB production specification required")
    parent_declaration = read(OLD / "declaration.json")
    if parent_declaration["production_config"] != info["production_config"] or parent_declaration["budgets"] != info["budgets"]:
        raise ValueError("actual parent declaration differs from sealed preparation")
    roots = sorted(set(info["resource_roots"]) | set(read(BUILD / "declaration.json")["resource_roots"])
        | set(read(FULL / "declaration.json")["resource_roots"])
        | set(read(CAUSAL / "declaration.json")["resource_roots"])
        | {str(p) for pattern in ("axial-material-*",) for p in ART.glob(pattern)}
        | set(read(Path(COMBINED_BUILD) / "declaration.json")["resource_roots"])
        | {str(SOURCE), str(OUTPUT), str(COLD_TERMINAL), str(CONTROL_TERMINAL), str(BUILD_TERMINAL)})
    resources = complete_history_resources(roots)
    before = resources.check()
    parent_bytes = sum(p.stat().st_size for p in OLD.rglob("*") if p.is_file() and not p.is_symlink())
    # AAA is the presently executable case. Later ABA remains independently
    # gated and must receive a fresh storage admission after its CE guard.
    reserve = math.ceil(1.5 * parent_bytes) + 2**30
    if parent_bytes != ORIGINAL_COMPLETE_12_MAP_CASE_BYTES or reserve != ORIGINAL_COLD_RESERVE_BYTES:
        raise ValueError("original full-case reservation provenance changed")
    if before["artifact_bytes"] + reserve >= 96 * 2**30 or before["disk_free_bytes"] - reserve < 8 * 2**30:
        raise ValueError("fresh complete AAA reservation exceeds unchanged history/free-space caps")
    SOURCE.mkdir(exist_ok=False)
    source_proofs = {}
    for src, wanted, name in ((HOST, HOST_SHA, "combined_cold_own_rss_host.py"),
        (CONTROLS, CONTROLS_SHA, "combined_cold_own_rss_controls.py"),
        (DECK_HELPER, DECK_HELPER_SHA, "combined_cold_file_snapshot_decks.py"),
        (PRIVATE_INPUT_CONSUMER, PRIVATE_INPUT_CONSUMER_SHA, "cold_component_input_consumer.py"),
        (SCIPY_HELPER, SCIPY_HELPER_SHA, "cold_scipy_environment_admission_namespace_v3_20261008.py")):
        shutil.copy2(require(src, wanted), SOURCE / name)
        require(SOURCE / name, wanted)
    for name in UNCHANGED_NAMES:
        shutil.copy2(OLD / "runtime" / name, SOURCE / name)
        if digest(SOURCE / name) != digest(OLD / "runtime" / name):
            raise ValueError("unchanged pipeline component copy differs")
    expanded_env=copy.deepcopy(producer_env)
    add_expected(expanded_env['files'],SOURCE/'cold_scipy_environment_admission_namespace_v3_20261008.py',SCIPY_HELPER_SHA)
    write_new(SOURCE / "analysis_environment.json",expanded_env)
    generated_host = ADMISSION_HOST
    for token, value in [("__BUILD_ROOT__", str(BUILD)), ("__BUILD_SEAL__", admitted["build_seal_sha256"]),
                         ("__RUNTIME_SHA__", runtime["sha256"]),
                         ("__RUNTIME_PATH__", runtime["path"]), ("__FACTORY_DESCRIPTOR__", factory_source_descriptor()), ("__PREPARED_SHA__", PREPARED_SHA),
                         ("__BUILD_FACTORY__", str(BUILD_FACTORY)), ("__BUILD_FACTORY_SHA__", BUILD_FACTORY_SHA),
                         ("__TERMINAL_EVIDENCE__", admitted["actual_external_terminal_evidence"]),
                         ("__TERMINAL_VALIDATION__", admitted["actual_external_terminal_validation"]),
                         ("__TERMINAL_CHAIN__", terminal_chain), ("__CORRECTION_SCOPE__", CORRECTION_SCOPE),
                         ("__RESOURCE_SCOPE_CONTRACT__", admitted["resource_scope_contract"])]:
        if generated_host.count(token) != 1:
            raise ValueError("admission template token is ambiguous")
        generated_host = generated_host.replace(token, repr(value), 1)
    (SOURCE / "rank1_factor_cache_admission.py").write_text(generated_host)
    original_runner = require(BASE_CONTROLLER, BASE_CONTROLLER_SHA).read_text()
    source_proofs["production_runner.py"] = write_controller(original_runner, runtime["sha256"], SOURCE / "production_runner.py")
    original_ingestion = (BASE_WORK / "runtime/qualified_snapshot_ingestion.py").read_text()
    ingestion_changes = [("ONLINE_SHA = '" + BASE_RUNTIME_SHA + "'", "ONLINE_SHA = '" + runtime["sha256"] + "'")]
    source_proofs["qualified_snapshot_ingestion.py"] = patched(original_ingestion, ingestion_changes,
        SOURCE / "qualified_snapshot_ingestion.py")
    shutil.copy2(BASE_WORK / "runtime/numerical_layout_admission.py", SOURCE / "numerical_layout_admission.py")
    source_proofs["numerical_layout_admission.py"] = dict(parent=pin(BASE_WORK / "runtime/numerical_layout_admission.py"),
        candidate=pin(SOURCE / "numerical_layout_admission.py"), full_text_restored_byte_exact=True,
        unchanged_file_byte_exact=True)
    write_new(SOURCE / "source_equivalence.json", dict(
        schema="AXMAT_RANK1_FACTOR_CACHE_PIPELINE_SOURCE_EQUIVALENCE_V1", patches=source_proofs,
        unchanged_files={name: dict(parent=pin(OLD / "runtime" / name), candidate=pin(SOURCE / name)) for name in UNCHANGED_NAMES},
        original_offline_replay_body_restored_exactly=True, original_native_ingress_body_restored_exactly=True,
        original_layout_body_restored_exactly=True, production_config_and_deck_generator_byte_exact=True,
        only_two_complete_unused_snapshot_copy_statements_deferred=True,
        only_two_SNAP_declarations_changed_to_independent_XSM_files=True,
        working_snapshot_name=WORKING_SNAPSHOT_NAME,mathematical_call_parameters_byte_exact=True,
        bootstrap_RSS_not_proved_by_warm_capture=True, physics_repair_not_old_operator_equivalence=True,
        run_AST_exact=False, run_only_delta_is_genuine_own_child_constructor=True,
        run_inverse_patch_restores_original_bytes_exactly=True,
        actual_complete_log_each_selector_values_required=OBSERVER_EXPECTED,
        selector_guard_failure_prevents_seal_and_next_stage=True,
        rank1_factor_cache_guard_failure_prevents_seal_and_next_stage=True,
        actual_factor_cache_observer_contract=CACHE_OBSERVER_CONTRACT,
        resource_monitor_AST_exact=True, resource_monitor_unmodified_from_actual844=True,
        resource_monitor_inverse_patch_restores_original_bytes_exactly=True,
        byte_copied_original_DiskResources_AST_exact=True,
        actual_runtime_resource_class_is_explicit_dynamic_build_guard=True,
        resource_scope_policy=HISTORY_SCOPE_POLICY,
        resource_scope_contract=admitted["resource_scope_contract"],
        qualify_ABA_and_serial_class_source_byte_exact=True, frozen_module_identity_reassigned=False,
        existing_pipeline_sources_changed=False, candidate_output_numerical_replay_to_old_closure_claimed=False,
        component_input_reuse_semantics=INPUT_REUSE_SEMANTICS,original_component_APIs_executed_in_cold_process=False,
        current_cold_source_and_real_MRO_required=True,original_705_38_MRO_is_immutable_INPUT_only=True,
        actual_new_binding_positive_and_oversize_RootEXIT0_still_required=True,
        private_metadata_callback_has_no_child_or_API=True))
    build_seal = read(require(BUILD / "seal.json", admitted["build_seal_sha256"]))
    dependencies = {str(BUILD / name): sha for name, sha in build_seal["files"].items()}
    add_expected(dependencies,BASE_FACTORY,BASE_FACTORY_SHA)
    add_expected(dependencies,BASE_WORK/"prepared.json",BASE_PREPARED_SHA)
    for name,wanted in read(BASE_WORK/"prepared.json")["local_files"].items():add_expected(dependencies,BASE_WORK/name,wanted)
    for path,wanted in parent_variant["files"].items():add_expected(dependencies,path,wanted)
    for p in [Path(__file__).resolve(), PARENT_FACTORY, BUILD_FACTORY, BUILD / "seal.json",
        CAPTURE / "seal.json", OLD / "prepared.json", OLD / "declaration.json", env_path,
        FULL / "declaration.json", CAUSAL / "declaration.json", Path(contract["reference_analysis_recipe"]["path"]),
        Path(parent_resource_addendum["path"]), Path(info["case_spec"]["path"]), Path(info["inputs"]["material_results"]["path"]),
        OLD / "runtime/conditional_white_receiver_variant.json", *[p for p in SOURCE.iterdir() if p.is_file()]]:
        add_expected(dependencies,p,digest(p))
    for item in terminal_chain.values():add_expected(dependencies,item["path"],item["sha256"])
    for p,wanted in combined['descriptor_files'].items():add_expected(dependencies,p,wanted)
    intake=component_intake()
    for p,wanted in intake['intake_proof_files'].items():add_expected(dependencies,p,wanted)
    for item in (intake['binding_source'],intake['binding_descriptor']):
        add_expected(dependencies,item['path'],item['sha256'])
    add_expected(dependencies,COMPONENT_INTAKE_DESCRIPTOR,COMPONENT_INTAKE_DESCRIPTOR_SHA)
    add_expected(dependencies,PRIVATE_INPUT_CONSUMER,PRIVATE_INPUT_CONSUMER_SHA)
    for p,wanted in guard_owner_files().items():add_expected(dependencies,p,wanted)
    for p in SOURCE.iterdir():
        if p.is_file():add_expected(dependencies,p,digest(p))
    verify(dependencies)
    write_new(SOURCE / "rank1_factor_cache_admission.json", dict(
        schema=CALLBACK_METADATA_SCHEMA, files=dependencies, combined_runtime=runtime,
        component_input_intake=component_intake(),
        whole_component_body_source=component_intake()['api_return'],
        component_resource_roots=roots,
        component_resource_info=dict(artifact_root=info['artifact_root'],resource_roots=roots,case_spec=info['case_spec']),
        component_runtime_file_hashes={name:digest(SOURCE/name)for name in
            ('production_inputs.py','snapshot_control_preflight.py','qualified_snapshot_ingestion.py',
             'numerical_layout_admission.py','rank1_factor_cache_admission.py','white_receiver_tracking.py','production_runner.py')},
        whole_component_return_encoding='COMPLETE_EXTERNAL_API_JSON_POINTER_MATERIALIZED_AFTER_FRESH_GRAPH',
        component_API_reexecution_in_cold_process=False,
        genuine_scipy_additional_environment=scipy_environment_contract(),
        input_aliases=combined["input_aliases"], new_binding_controls_not_yet_executed=True,
        whole_component_returns_preserved=True, deferred_deck_helper=pin(SOURCE / "combined_cold_file_snapshot_decks.py"),
        parent_prepared=pin(OLD / "prepared.json"), parent_variant=pin(OLD / "runtime/conditional_white_receiver_variant.json"),
        parent_producer_receipt=pin(info["inputs"]["material_results"]["path"]), original_inputs=info["inputs"],
        producer_environment=pin(SOURCE / "analysis_environment.json"), reference_analysis_recipe=contract["reference_analysis_recipe"],
        correction_scope=CORRECTION_SCOPE, build_terminal_evidence=admitted["actual_external_terminal_evidence"],
        build_terminal_validation=admitted["actual_external_terminal_validation"], build_terminal_chain=terminal_chain,
        resource_scope_policy=HISTORY_SCOPE_POLICY,
        resource_scope_contract=admitted["resource_scope_contract"],
        physical_inputs_unchanged=True, common_training_unchanged=True, white_closure_unchanged=True,
        radial_arithmetic_unchanged=True, collision_self_operator_unchanged=False,
        original_controls_and_gates_unchanged=True, fresh_training_bootstrap_and_maps_required=True,
        all_actual_axial_selector_observers_required=True, all_actual_rank1_factor_cache_observers_required=True,
        actual_factor_cache_observer_contract=CACHE_OBSERVER_CONTRACT,
        reference_reassessment_pending=True, old_reference_recipe_is_dependency_only=True,
        new_actual_prepared_status_observables_physical_and_collector_receipt_rebinding_required=True,
        reference_qualification_created=False,
        old_moment_closure_numerical_replay_claimed=False, CE_fitting=False,
        AAA_accuracy_qualified=False, ABA_admitted=False))
    admission = pin(SOURCE / "rank1_factor_cache_admission.json")
    variant = copy.deepcopy(parent_variant)
    variant.update(candidate_runtime=runtime, rank1_factor_cache_revision=dict(admission=admission,
        fresh_complete_coupling_required=True, physical_inputs_changed=False,
        white_closure_changed=False, original_thresholds_changed=False,
        old_moment_closure_numerical_replay_claimed=False))
    for path,wanted in dependencies.items():add_expected(variant["files"],path,wanted)
    variant["files"][admission["path"]] = admission["sha256"]
    write_new(SOURCE / "conditional_white_receiver_variant.json", variant)
    receipt = copy.deepcopy(parent_receipt)
    receipt.update(online_receiver_sha256=runtime["sha256"],
        conditional_white_receiver_variant=pin(SOURCE / "conditional_white_receiver_variant.json"),
        rank1_factor_cache_revision=admission,
        scope="Same audited A/B offline producer archives and exact REAL32 BOOT mirror. Correct the online SPOT "
              "angular selector and NANIS clamp, retain the sealed NDIM1 raw Legendre source correction, and require "
              "every actual axial selector and fixed-operator cache terminal observer; all fixed-point and independent scientific gates remain mandatory. Physical axial NTOT0/all self P0-P2 is now repaired; radial R/white/input untouched; two unused SNAP copies deferred to independent XSM work files; genuine own-child512 required.")
    restore_metadata(receipt, parent_receipt, [(k,) for k in (
        "online_receiver_sha256", "conditional_white_receiver_variant", "scope")], [("rank1_factor_cache_revision",)])
    write_new(SOURCE / "producer_ingestion_receipt.json", receipt)
    spec = copy.deepcopy(parent_spec)
    spec.update(experiment_id=EXPERIMENT, status="PREDECLARED_RANK1_FACTOR_CACHE_FULL_COUPLED_TRIAL")
    spec["production"]["implementation"] = ("Same production data/layout/white/radial arithmetic; repair physical axial NTOT0/self P0-P2, preserve full-shape exact dedup math and correct the SPOT "
        "angular selector/NANIS clamp, retain the sealed raw Legendre sender fix and require actual axial observers; SHA256 "
        + runtime["sha256"])
    spec["qualified_snapshot_producers"].update(receiver_sha256=runtime["sha256"],
        receipt=pin(SOURCE / "producer_ingestion_receipt.json"))
    spec["conditional_white_trace_trial"]["variant"] = pin(SOURCE / "conditional_white_receiver_variant.json")
    spec["rank1_factor_cache_trial"] = dict(admission=admission, combined_runtime=runtime,
        physical_axial_collision_repaired=True, collision_self_operator_unchanged=False,
        two_deferred_copy_decks_required=True,two_independent_XSM_SNAP_working_files_required=True,
        working_snapshot_name=WORKING_SNAPSHOT_NAME,genuine_own_child_512_required=True,fresh_complete_coupling_required=True,
        reused_training_or_bootstrap_or_maps=False, white_trace_K_changed=False, original_four_thresholds_changed=False,
        actual_axial_observers_required=dict(prefix=OBSERVER_PREFIX, expected=OBSERVER_EXPECTED,
            all_observers=True, missing_or_mismatched_refused=True),
        actual_build_terminal_chain=terminal_chain, actual_combined_runtime_admission=combined, inherited_CE_qualification=False,
        resource_scope_policy=HISTORY_SCOPE_POLICY,
        resource_scope_contract=admitted["resource_scope_contract"],
        original_independent_eight_gates_required=True, complete_original_2000_active_reference_batches_required=True,
        reference_reassessment_pending=True, old_reference_recipe_is_dependency_only=True,
        new_actual_prepared_status_observables_physical_and_collector_receipt_rebinding_required=True,
        reference_qualification_created=False,
        old_AAA_outputs_are_not_equivalent=True, CE_fitting=False)
    restore_metadata(spec, parent_spec, [("experiment_id",), ("status",), ("production", "implementation"),
        ("qualified_snapshot_producers", "receiver_sha256"), ("qualified_snapshot_producers", "receipt"),
        ("conditional_white_trace_trial", "variant")], [("rank1_factor_cache_trial",)])
    write_new(SOURCE / "case_spec.json", spec)
    rank = read(info["rank_addendum"]["path"])
    parent_rank = copy.deepcopy(rank)
    rank.update(experiment_id=EXPERIMENT, case_spec_sha256=digest(SOURCE / "case_spec.json"))
    restore_metadata(rank, parent_rank, [("experiment_id",), ("case_spec_sha256",)])
    write_new(SOURCE / "rank_addendum.json", rank)
    write_new(SOURCE / "resource_admission.json", dict(
        schema="AXMAT_RANK1_FACTOR_CACHE_FRESH_AAA_STORAGE_ADMISSION_V1", resources_before=before,
        parent_resource_addendum=parent_resource_addendum, initial_history_cap_GiB=40,
        inherited_complete_history_cap_GiB=96, inherited_free_floor_GiB=8,
        resource_roots=roots, complete_history_scope_extended_to_new_family=True,
        resource_scope_policy=HISTORY_SCOPE_POLICY,
        resource_scope_contract=admitted["resource_scope_contract"],
        dynamic_current_axial_family_roots_checked_on_every_resource_poll=True,
        fresh_reservation_rechecked_before_prepare_and_full_AAA_handoffs=True,
        unchanged_history_cap_bytes=96 * 2**30, unchanged_min_free_bytes=8 * 2**30,
        original_complete_12_map_case_bytes=parent_bytes, fresh_AAA_reserve_bytes=reserve,
        independent_working_snapshot_storage_forecast=working_snapshot_storage_forecast(),
        forecast_bytes=before["artifact_bytes"] + reserve, original_case_budgets=info["budgets"],
        original_max_maps=100, planning_previous_maps=12, complete_native_convergence_required=True,
        retries=0, threads=1, numeric_children_at_once=1,
        actual_build_terminal_root=str(BUILD_TERMINAL), actual_build_terminal_evidence=admitted["actual_external_terminal_evidence"],
        later_ABA_requires_fresh_storage_check=True, resource_caps_changed=False))
    write_new(SOURCE / "input_and_gate_equivalence.json", dict(
        schema="AXMAT_RANK1_FACTOR_CACHE_INPUT_AND_GATE_EQUIVALENCE_V1", parent_case_spec=pin(info["case_spec"]["path"]),
        candidate_case_spec=pin(SOURCE / "case_spec.json"), all_unlisted_spec_fields_exact=True,
        physical_material_snapshot_and_tracking_input_descriptors_exact=True,
        producer_receipt_restore_to_parent_exact=True, production_config=info["production_config"], budgets=info["budgets"],
        four_thresholds=dict(radial=2.5e-7, axial=5e-8, MCCG=2.5e-8, coupled_outer=5e-7),
        fresh_common_ABA_training_and_cold_bootstrap_and_full_maps=True,
        complete_independent_reference_recipe=contract["reference_analysis_recipe"],
        reference_reassessment_pending=True, old_reference_recipe_is_dependency_only=True,
        new_actual_prepared_status_observables_physical_and_collector_receipt_rebinding_required=True,
        reference_qualification_created=False,
        original_2000_batch_history_mandatory=True, producer_environment=pin(SOURCE / "analysis_environment.json"),
        source_equivalence=pin(SOURCE / "source_equivalence.json"),
        parent_coupling_factory=pin(require(PARENT_FACTORY, PARENT_FACTORY_SHA)),
        actual_build_terminal_chain=terminal_chain, actual_axial_observer_expected=OBSERVER_EXPECTED,
        run_only_genuine_own_child_constructor_delta=True,
        resource_monitor_actual844_source_byte_exact=True,
        resource_scope_policy=HISTORY_SCOPE_POLICY,
        resource_scope_contract=admitted["resource_scope_contract"],
        old_source_moment_closure_numerical_replay_claimed=False, AAA_accuracy_qualified=False, ABA_admitted=False))
    declaration = copy.deepcopy(parent_declaration)
    declaration.update(experiment_id=EXPERIMENT, case_spec=pin(SOURCE / "case_spec.json"),
        rank_addendum=pin(SOURCE / "rank_addendum.json"), resource_roots=roots,
        conditional_white_receiver_variant=pin(SOURCE / "conditional_white_receiver_variant.json"),
        helper=pin(Path(__file__).resolve()), rank1_factor_cache_revision=admission,
        rank1_factor_cache_equivalence=pin(SOURCE / "input_and_gate_equivalence.json"),
        rank1_factor_cache_resource_admission=pin(SOURCE / "resource_admission.json"))
    declaration["inputs"]["material_results"] = pin(SOURCE / "producer_ingestion_receipt.json")
    restore_metadata(declaration, parent_declaration, [("experiment_id",), ("case_spec",), ("rank_addendum",),
        ("resource_roots",), ("conditional_white_receiver_variant",), ("helper",), ("inputs", "material_results")],
        [("rank1_factor_cache_revision",), ("rank1_factor_cache_equivalence",), ("rank1_factor_cache_resource_admission",)])
    write_new(SOURCE / "declaration.json", declaration)
    write_new(SOURCE / "factory_seal.json", dict(schema="AXMAT_COMBINED_PHYSICAL_DEDUP_FILE_SNAPSHOT_COLD_FACTORY_SEAL_V1",
        files={p.name: digest(p) for p in SOURCE.iterdir() if p.is_file()}))
    print(json.dumps(dict(classification="DECLARED_COMBINED_PHYSICAL_DEDUP_FILE_SNAPSHOT_COLD_INPUT_ONLY",
        declaration=pin(SOURCE / "declaration.json"), output=str(OUTPUT),
        factory_seal=pin(SOURCE / "factory_seal.json"), source_equivalence=pin(SOURCE / "source_equivalence.json"))))

def fresh_storage_admission(declaration):
    require_input_ready()
    item = declaration["rank1_factor_cache_resource_admission"]
    storage = read(require(item["path"], item["sha256"]))
    if (storage["resource_scope_policy"] != HISTORY_SCOPE_POLICY
            or storage["resource_roots"] != declaration["resource_roots"]
            or storage["unchanged_history_cap_bytes"] != 96 * 2**30
            or storage["unchanged_min_free_bytes"] != 8 * 2**30
            or storage["independent_working_snapshot_storage_forecast"] != working_snapshot_storage_forecast()
            or type(storage["fresh_AAA_reserve_bytes"]) is not int or storage["fresh_AAA_reserve_bytes"] <= 0):
        raise ValueError("original fresh full-AAA reservation and dynamic history policy required")
    before = complete_history_resources(declaration["resource_roots"]).check()
    if before["resource_scope_contract"] != storage["resource_scope_contract"]:
        raise ValueError("original axial-family storage scope contract changed")
    reserve = storage["fresh_AAA_reserve_bytes"]
    if before["artifact_bytes"] + reserve >= 96 * 2**30 or before["disk_free_bytes"] - reserve < 8 * 2**30:
        raise ValueError("fresh complete AAA reservation no longer fits unchanged history/free-space caps")
    return before


def verify_factory(expected_declaration):
    require_input_ready()
    declaration_path=require(SOURCE/'declaration.json',nonzero_sha(expected_declaration))
    seal=read(require(SOURCE/'factory_seal.json'))
    if seal['schema']!='AXMAT_COMBINED_PHYSICAL_DEDUP_FILE_SNAPSHOT_COLD_FACTORY_SEAL_V1':raise ValueError('new cold source inventory schema required')
    check_flat_namespace(SOURCE,{**seal['files'],'factory_seal.json':digest(SOURCE/'factory_seal.json')})
    d=read(declaration_path);m=read(require(d['rank1_factor_cache_revision']['path'],d['rank1_factor_cache_revision']['sha256']))
    m=materialize_metadata(m,d['rank1_factor_cache_revision'],phase='factory/verify')
    if m['combined_runtime_admission']!=m['actual_components']['combined']:
        raise ValueError('whole materialized actual component chain changed')
    for k in ('rank1_factor_cache_equivalence','rank1_factor_cache_resource_admission','case_spec','rank_addendum',
              'conditional_white_receiver_variant','helper'):
        require(d[k]['path'],d[k]['sha256'])
    if d['budgets']!=BUDGETS:raise ValueError('original full cold budget fields changed')
    return d


def declaration_terminal_admission(expected_declaration,terminal_sha):
    require_input_ready()
    path=COLD_TERMINAL/'declaration_terminal_return.json'
    e=read(require(path,nonzero_sha(terminal_sha)))
    actual=e['actual_tool_result']
    command=[read(SOURCE/'analysis_environment.json')['executable'],str(FORMAL_FACTORY),'declare','--factory-sha256',factory_source_descriptor()['sha256']]
    if (e['schema']!=DECL_TERMINAL_SCHEMA or e['record_producer']!='root'
        or e['actual_tool_terminal_return_observed'] is not True
        or e['record_written_after_actual_terminal_return'] is not True
        or type(actual['exit_code']) is not int or actual['exit_code']!=0
        or not actual['initial_chunk_id'] or not actual['terminal_chunk_id']
        or type(e['returncode']) is not int or e['returncode']!=0 or e['command']!=command
        or e['source']!=factory_source_descriptor()
        or e['declaration']!=dict(path=str(SOURCE/'declaration.json'),sha256=expected_declaration)
        or e['factory_seal']!=pin(SOURCE/'factory_seal.json')
        or e['scientific_qualification'] is not False or e['transport_started'] is not False):
        raise ValueError('actual Root declaration EXIT0 INPUT-only witness required')
    stdout=require(e['full_stdout']['path'],e['full_stdout']['sha256'])
    stderr=require(e['full_stderr']['path'],e['full_stderr']['sha256'])
    if stdout.parent!=COLD_TERMINAL or stderr.parent!=COLD_TERMINAL or len({path,stdout,stderr})!=3:
        raise ValueError('independent complete declaration stdout/stderr required')
    value=read(stdout)
    if (value['classification']!='DECLARED_COMBINED_PHYSICAL_DEDUP_FILE_SNAPSHOT_COLD_INPUT_ONLY'
        or value['declaration']!=e['declaration'] or value['factory_seal']!=e['factory_seal']):
        raise ValueError('actual retained declaration output differs')
    verify_factory(expected_declaration)
    return dict(path=str(path),sha256=terminal_sha)


def normal_runtime_preload(runtime):
    scipy_dependency_admission()
    for name in ('production_inputs','snapshot_control_preflight','qualified_snapshot_ingestion',
                 'numerical_layout_admission','rank1_factor_cache_admission','white_receiver_tracking'):
        load(runtime/(name+'.py'),name)
    current=load(runtime/'production_runner.py','production_runner')
    scipy_dependency_admission()
    return current


def child_environment():
    return dict(os.environ,**{k:'1' for k in THREADS},PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(SCIPY_TARGET_ROOT))


def normal_factory_command(python,expression):
    # The factory is ordinarily imported, never installed under an invented file name.
    program=('import hashlib,sys,os; from pathlib import Path\n'
        'if sys.flags.optimize!=0 or \"PYTHONOPTIMIZE\" in os.environ: raise ValueError(\"nonoptimized cold source predicates required\")\n'
        'sys.dont_write_bytecode=True; '
        'p=Path('+repr(str(FORMAL_FACTORY))+'); assert hashlib.sha256(p.read_bytes()).hexdigest()=='+repr(factory_source_descriptor()['sha256'])+'; '
        'sys.path.insert(0,str(p.parent)); import '+Path(FORMAL_FACTORY).stem+' as f; '
        'assert Path(f.__file__).resolve()==p; '+expression)
    return [python,'-c',program]


def prepare(expected_declaration,declare_terminal_sha):
    require_input_ready();producer_environment()
    declaration=verify_factory(expected_declaration)
    declaration_terminal_admission(expected_declaration,declare_terminal_sha)
    if os.path.lexists(OUTPUT):raise ValueError('fresh full cold WORK root must be absent')
    fresh_storage_admission(declaration)  # Original reserve96/free8 is still a hard refusal before mkdir.
    python=read(SOURCE/'analysis_environment.json')['executable']
    command=normal_factory_command(python,'c=f.normal_runtime_preload(f.SOURCE); '
        'r=c.prepare(f.SOURCE/"declaration.json",'+repr(expected_declaration)+',f.OUTPUT); '
        'import json; print(json.dumps(r,sort_keys=True,allow_nan=False),flush=True)')
    os.execve(python,command,child_environment())


def prepare_binding_in_clean_process(prepared_sha,declare_terminal_sha):
    require_input_ready()
    p=require(OUTPUT/'prepared.json',nonzero_sha(prepared_sha));info=read(p)
    if info['classification']!='PREPARED_NO_TRANSPORT' or 'own_child_supervision' in info:
        raise ValueError('actual original prepare INPUT-only complete info required')
    # Bind the genuinely copied current canonical controller before any frozen full/probe import.
    for name,wanted in info['local_files'].items():require(OUTPUT/name,wanted)
    c=normal_runtime_preload(OUTPUT/'runtime')
    d=verify_factory(info['declaration']['sha256'])
    declaration_terminal_admission(info['declaration']['sha256'],declare_terminal_sha)
    fresh_storage_admission(d)
    actual=c.verify_prepared(p,prepared_sha)
    if actual!=info:raise ValueError('true original input verifier result differs')
    resources=c.resource_monitor(info);resources.check()
    h=load(require(OUTPUT/'runtime/combined_cold_own_rss_host.py',HOST_SHA),'combined_cold_own_rss_host')
    full=load(require(h.FULL,h.FULL_SHA),'qualify_refined_AAA_layered_full')
    guard=load(require(h.GUARD_FACTORY,h.GUARD_FACTORY_SHA),h.GUARD_FACTORY.stem)
    tested=guard.guard_admission(full)
    m=read(require(d['rank1_factor_cache_revision']['path'],d['rank1_factor_cache_revision']['sha256']))
    m=materialize_metadata(m,d['rank1_factor_cache_revision'],phase='factory/prepare-real-cold-binding')
    files=dict(m['files'])
    for name,wanted in info['local_files'].items():add_expected(files,OUTPUT/name,wanted)
    for path,wanted in read(SOURCE/'analysis_environment.json')['files'].items():add_expected(files,path,wanted)
    add_expected(files,FORMAL_FACTORY,factory_source_descriptor()["sha256"])
    add_expected(files,p,prepared_sha)
    for key in ('case_spec','rank_addendum','declaration'):add_expected(files,info[key]['path'],info[key]['sha256'])
    for item in info['inputs'].values():add_expected(files,item['path'],item['sha256'])
    for path,wanted in guard_owner_files().items():add_expected(files,path,wanted)
    source_seal=read(SOURCE/"factory_seal.json")
    for name,wanted in source_seal["files"].items():add_expected(files,SOURCE/name,wanted)
    add_expected(files,SOURCE/"factory_seal.json",digest(SOURCE/"factory_seal.json"))
    declaration_receipt=read(require(COLD_TERMINAL/"declaration_terminal_return.json",declare_terminal_sha))
    add_expected(files,COLD_TERMINAL/"declaration_terminal_return.json",declare_terminal_sha)
    for k in ("full_stdout","full_stderr"):add_expected(files,declaration_receipt[k]["path"],declaration_receipt[k]["sha256"])
    # No current-module fresh hash may silently become an expected owner.
    modules={}
    for name,obj in list(sys.modules.items()):
        source=getattr(obj,'__file__',None)
        if source is None:continue
        endpoint=Path(source).resolve()
        if endpoint.is_relative_to(ROOT/'validation'):
            wanted=files.get(str(endpoint))
            if wanted is None:raise ValueError('actual project module lacks independently expected owner: '+name)
            require(endpoint,wanted);modules[name]=dict(path=str(endpoint),sha256=wanted)
    modules['__main__']=dict(path=str(OUTPUT/'runtime/combined_cold_own_rss_controls.py'),sha256=CONTROLS_SHA)
    runtime=namespace(OUTPUT/'runtime')
    if runtime['directories'] or runtime['symlinks']:raise ValueError('runtime must be exact flat regular files')
    b=dict(schema=h.SCHEMA,caps=h.CAPS,work_root=str(OUTPUT),control_terminal_root=str(CONTROL_TERMINAL),
        scientific_qualification=False,module_global_or_class_overlay=False,canonical_controller_name='production_runner',
        controller=pin(OUTPUT/'runtime/production_runner.py'),host=pin(OUTPUT/'runtime/combined_cold_own_rss_host.py'),
        controls_source=pin(OUTPUT/'runtime/combined_cold_own_rss_controls.py'),
        bounded_helper=dict(path=str(OUTPUT/'runtime/run_bounded_dragon.py'),sha256=h.BOUNDED_SHA),
        serial_baseline=dict(path=str(BASE_CONTROLLER),sha256=BASE_CONTROLLER_SHA),
        own_rss_source=dict(path=str(h.FULL),sha256=h.FULL_SHA),
        guard_factory=dict(path=str(h.GUARD_FACTORY),sha256=h.GUARD_FACTORY_SHA),
        resource_class_source=dict(path=str(h.RESOURCE_CLASS_SOURCE),sha256=h.RESOURCE_CLASS_SHA),
        producer_environment=read(SOURCE/'analysis_environment.json'),
        runtime_namespace=dict(files=runtime['files'],directories=[]),
        runtime_module_owners={name:pin(OUTPUT/'runtime'/(name+'.py')) for name in h.PRELOAD_RUNTIME_MODULES},
        module_owners=modules,tested_guard_files=[pin(path) for path in tested],files=files,
        resource_info={k:info[k] for k in ('artifact_root','resource_roots','case_spec')},
        actual_component_returns=m['actual_components'],input_declaration_terminal_evidence=dict(
            path=str(COLD_TERMINAL/'declaration_terminal_return.json'),sha256=declare_terminal_sha))
    path=OUTPUT/'own_rss_binding.json';write_new(path,b)
    descriptor=pin(path)
    actual_c,actual_full,actual_b=h.bind_controller(descriptor)
    if actual_c is not c or actual_full is not full or actual_b!=b:raise ValueError('actual normal binding differs')
    h.resource_provenance(resources,c,b)
    proof=h.source_mro_proof(c,full,b)
    return dict(classification='PREPARED_NEW_CANONICAL_BINDING_INPUT_ONLY_NO_FIXTURE_CREDIT',binding=descriptor,
        actual_source_identity=proof,new_binding_fixtures_executed=False,scientific_qualification=False)


def prepare_binding(prepared_sha,declare_terminal_sha):
    require_input_ready()
    python=read(SOURCE/'analysis_environment.json')['executable']
    command=normal_factory_command(python,'r=f.prepare_binding_in_clean_process('+repr(prepared_sha)+','+repr(declare_terminal_sha)+'); '
        'import json; print(json.dumps(r,sort_keys=True,allow_nan=False),flush=True)')
    os.execve(python,command,child_environment())


def run_controls(binding_sha,declare_terminal_sha):
    require_input_ready()
    binding=read(require(OUTPUT/'own_rss_binding.json',nonzero_sha(binding_sha)))
    if binding['input_declaration_terminal_evidence']['sha256']!=declare_terminal_sha:
        raise ValueError('same true Root declaration evidence required')
    python=binding['producer_environment']['executable']
    command=[python,str(OUTPUT/'runtime/combined_cold_own_rss_controls.py'),'run-controls',
        '--binding',str(OUTPUT/'own_rss_binding.json'),'--binding-sha256',binding_sha]
    # Only d098 itself claims and runs the two actual isolated children, under original120/60/512.
    os.execve(python,command,child_environment())


def final_cold_info(input_only_info,supervision):
    """Pure metadata: only the new real supervision descriptor is added."""
    if (input_only_info.get('classification')!='PREPARED_NO_TRANSPORT'
            or 'own_child_supervision' in input_only_info
            or set(supervision)!={'binding','controls'}
            or set(supervision['controls'])!={'seal','terminal_evidence'}):
        raise ValueError('unchanged INPUT-only original preparation and real completed new controls required')
    for item in (supervision['binding'],supervision['controls']['seal'],supervision['controls']['terminal_evidence']):
        if set(item)!={'path','sha256'} or not Path(item['path']).is_absolute():raise ValueError('real explicit supervision descriptor required')
        nonzero_sha(item['sha256'])
    result=copy.deepcopy(input_only_info);result['own_child_supervision']=copy.deepcopy(supervision)
    inverse=copy.deepcopy(result);del inverse['own_child_supervision']
    if inverse!=input_only_info:raise ValueError('all original prepared input fields must remain exact')
    return result


def finalize_cold_in_clean_process(prepared_sha,binding_sha,control_seal_sha,control_terminal_sha,declare_terminal_sha):
    require_input_ready()
    info=read(require(OUTPUT/'prepared.json',nonzero_sha(prepared_sha)))
    c=normal_runtime_preload(OUTPUT/'runtime')
    h=load(require(OUTPUT/'runtime/combined_cold_own_rss_host.py',HOST_SHA),'combined_cold_own_rss_host')
    supervision=dict(binding=dict(path=str(OUTPUT/'own_rss_binding.json'),sha256=nonzero_sha(binding_sha)),
        controls=dict(seal=dict(path=str(OUTPUT/'binding_controls/seal.json'),sha256=nonzero_sha(control_seal_sha)),
            terminal_evidence=dict(path=str(CONTROL_TERMINAL/'terminal_return.json'),sha256=nonzero_sha(control_terminal_sha))))
    actual_c,full,b=h.bind_controller(supervision['binding'])
    if actual_c is not c:raise ValueError('canonical source binding differs')
    h.controls_admission(b,supervision['binding'],supervision['controls'])
    declaration_terminal_admission(info['declaration']['sha256'],declare_terminal_sha)
    d=verify_factory(info['declaration']['sha256']);fresh_storage_admission(d)
    if c.verify_prepared(OUTPUT/'prepared.json',prepared_sha)!=info:raise ValueError('complete original input info differs')
    cold=final_cold_info(info,supervision)
    write_new(OUTPUT/'prepared_cold.json',cold)
    return dict(classification='PREPARED_COLD_INPUT_AND_ACTUAL_NEW_BINDING_CONTROLS_ONLY',
        original_prepared=pin(OUTPUT/'prepared.json'),prepared=pin(OUTPUT/'prepared_cold.json'),
        scientific_qualification=False,AAA_accuracy_qualified=False,ABA_admitted=False)


def finalize_cold(prepared_sha,binding_sha,control_seal_sha,control_terminal_sha,declare_terminal_sha):
    require_input_ready()
    for value in (prepared_sha,binding_sha,control_seal_sha,control_terminal_sha,declare_terminal_sha):nonzero_sha(value)
    python=read(SOURCE/'analysis_environment.json')['executable']
    expr='r=f.finalize_cold_in_clean_process('+','.join(repr(x) for x in
        (prepared_sha,binding_sha,control_seal_sha,control_terminal_sha,declare_terminal_sha))+'); '
    command=normal_factory_command(python,expr+'import json; print(json.dumps(r,sort_keys=True,allow_nan=False),flush=True)')
    os.execve(python,command,child_environment())


def combined_archive_bytes():
    return sum(p.stat().st_size for root in (SOURCE,OUTPUT) for p in root.rglob('*')
               if p.is_file() and not p.is_symlink())


def cold_launch_in_clean_process(prepared_sha,declare_terminal_sha):
    started=time.monotonic()
    require_input_ready()
    info=read(require(OUTPUT/'prepared_cold.json',nonzero_sha(prepared_sha)))
    if any(os.path.lexists(OUTPUT/name) for name in ('AAA','archives','training')):
        raise ValueError('one full fresh cold attempt, no bootstrap/map/training reuse')
    c=normal_runtime_preload(OUTPUT/'runtime')
    h=load(require(OUTPUT/'runtime/combined_cold_own_rss_host.py',HOST_SHA),'combined_cold_own_rss_host')
    supervision=info['own_child_supervision']
    actual_c,full,b=h.bind_controller(supervision['binding'])
    if actual_c is not c:raise ValueError('canonical MRO controller differs')
    h.controls_admission(b,supervision['binding'],supervision['controls'])
    declaration_terminal_admission(info['declaration']['sha256'],declare_terminal_sha)
    d=verify_factory(info['declaration']['sha256']);fresh_storage_admission(d)
    if info['budgets']!=BUDGETS:raise ValueError('every original production cap is mandatory')
    # This is the actual explicit prepared filename accepted by the unchanged original verifier.
    # Never call h.launch(), whose old convenience branch hardcodes prepared.json.
    try:
        result=c.run(OUTPUT/'prepared_cold.json',prepared_sha,'AAA',None,None)
        if (result['classification']!='WAITING_REFERENCE' or result['case']!='AAA'
            or result['prepared_sha256']!=prepared_sha or result['cases']['AAA']['classification']!='VALID_MET'):
            raise ValueError('actual full fresh cold case must first meet the original coupled gate')
        verify_factory(info['declaration']['sha256'])
        c.verify_prepared(OUTPUT/'prepared_cold.json',prepared_sha)
        resources=c.resource_monitor(info);h.resource_provenance(resources,c,b);snapshot=resources.check()
        elapsed=time.monotonic()-started;actual_bytes=combined_archive_bytes()
        if elapsed>=43200:
            raise ValueError('all-entry through complete cold closeout exceeds original whole reservation/time')
        write_new(OUTPUT/'cold_source_complete_result.json',dict(schema=SCHEMA,original_controller_return=result,
            input_declaration_terminal_evidence=b['input_declaration_terminal_evidence'],
            scientific_qualification=False,AAA_accuracy_qualified=False,ABA_admitted=False))
        write_new(OUTPUT/'cold_closeout_seal.json',dict(schema='AXMAT_COMBINED_COLD_COMPLETE_NAMESPACE_SEAL_V1',
            source=pin(SOURCE/'factory_seal.json'),work=namespace(OUTPUT),scientific_qualification=False))
        snapshot=resources.check();elapsed=time.monotonic()-started;actual_bytes=combined_archive_bytes()
        if elapsed>=43200:raise ValueError('cold closeout tail exceeds original cap')
        return dict(original_controller_return=result,full_closeout_tail_gate='PASS',actual_elapsed_seconds=elapsed,
            actual_archive_bytes=actual_bytes,actual_resources=snapshot,scientific_qualification=False,
            AAA_accuracy_qualified=False,ABA_admitted=False)
    except BaseException as error:
        write_new(OUTPUT/'cold_source_failure.json',dict(schema=SCHEMA,classification='FAILED_COMBINED_COLD_NO_RETRY',
            error=repr(error),actual_elapsed_seconds=time.monotonic()-started,scientific_qualification=False,
            AAA_accuracy_qualified=False,ABA_admitted=False))
        raise


def run_AAA(prepared_sha,declare_terminal_sha):
    require_input_ready()
    for value in (prepared_sha,declare_terminal_sha):nonzero_sha(value)
    python=read(SOURCE/'analysis_environment.json')['executable']
    command=normal_factory_command(python,'r=f.cold_launch_in_clean_process('+repr(prepared_sha)+','+repr(declare_terminal_sha)+'); '
        'import json; print(json.dumps(r,sort_keys=True,allow_nan=False),flush=True)')
    os.execve(python,command,child_environment())



def cold_terminal_admission(prepared_sha,declare_terminal_sha,terminal_sha):
    require_input_ready()
    expected_prepared=dict(path=str(OUTPUT/'prepared_cold.json'),sha256=nonzero_sha(prepared_sha))
    path=COLD_TERMINAL/'terminal_return.json';e=read(require(path,nonzero_sha(terminal_sha)))
    actual=e['actual_tool_result']
    python=read(SOURCE/'analysis_environment.json')['executable']
    expression='r=f.cold_launch_in_clean_process('+repr(prepared_sha)+','+repr(declare_terminal_sha)+'); '
    command=normal_factory_command(python,expression+'import json; print(json.dumps(r,sort_keys=True,allow_nan=False),flush=True)')
    if (e['schema']!=COLD_TERMINAL_SCHEMA or e['record_producer']!='root'
        or e['actual_tool_terminal_return_observed'] is not True or e['record_written_after_actual_terminal_return'] is not True
        or type(actual['exit_code']) is not int or actual['exit_code']!=0
        or not actual['initial_chunk_id'] or not actual['terminal_chunk_id']
        or type(e['returncode']) is not int or e['returncode']!=0
        or e['command']!=[python,str(FORMAL_FACTORY),'run-AAA','--factory-sha256',factory_source_descriptor()['sha256'],
            '--sha256',prepared_sha,'--declaration-terminal-sha256',declare_terminal_sha]
        or e['handoff_command']!=command
        or e['source']!=factory_source_descriptor() or e['prepared']!=expected_prepared
        or e['input_declaration_terminal_evidence']!=dict(path=str(COLD_TERMINAL/'declaration_terminal_return.json'),sha256=declare_terminal_sha)
        or any(e[k] is not False for k in ('scientific_qualification','AAA_accuracy_qualified','ABA_admitted'))):
        raise ValueError('actual external Root cold EXIT0, not a predeclared completion flag, required')
    stdout=require(e['full_stdout']['path'],e['full_stdout']['sha256']);stderr=require(e['full_stderr']['path'],e['full_stderr']['sha256'])
    if stdout.parent!=COLD_TERMINAL or stderr.parent!=COLD_TERMINAL or len({path,stdout,stderr})!=3:
        raise ValueError('retain complete independent cold stdout and stderr')
    value=read(stdout);tail={k:value[k] for k in COLD_TAIL}
    r=tail['actual_resources']
    if (any(e[k]!=tail[k] for k in COLD_TAIL) or tail['full_closeout_tail_gate']!='PASS'
        or type(tail['actual_elapsed_seconds']) not in (int,float) or not 0<tail['actual_elapsed_seconds']<43200
        or type(tail['actual_archive_bytes']) is not int or tail['actual_archive_bytes']!=combined_archive_bytes()
        or r['artifact_budget_bytes']!=96*2**30 or r['min_free_bytes']!=8*2**30
        or r['artifact_bytes']>96*2**30 or r['disk_free_bytes']<8*2**30 or 'reason' in r
        or r['resource_scope_policy']!=HISTORY_SCOPE_POLICY):raise ValueError('actual complete cold four-tail gate required')
    p=require(expected_prepared['path'],prepared_sha);info=read(p)
    c=normal_runtime_preload(OUTPUT/'runtime')
    h=load(require(OUTPUT/'runtime/combined_cold_own_rss_host.py',HOST_SHA),'combined_cold_own_rss_host')
    supervision=info['own_child_supervision'];actual_c,full,b=h.bind_controller(supervision['binding'])
    if actual_c is not c:raise ValueError('actual cold canonical controller differs')
    h.controls_admission(b,supervision['binding'],supervision['controls'])
    declaration_terminal_admission(info['declaration']['sha256'],declare_terminal_sha)
    verify_factory(info['declaration']['sha256']);c.verify_prepared(p,prepared_sha)
    resources=c.resource_monitor(info);h.resource_provenance(resources,c,b);resources.check()
    sealed_path=require(e['cold_closeout_seal']['path'],e['cold_closeout_seal']['sha256'])
    if sealed_path!=OUTPUT/'cold_closeout_seal.json':raise ValueError('fixed complete cold closeout seal required')
    seal=read(sealed_path);now=namespace(OUTPUT);old=seal['work']
    if (seal['schema']!='AXMAT_COMBINED_COLD_COMPLETE_NAMESPACE_SEAL_V1'
        or seal['source']!=pin(SOURCE/'factory_seal.json') or seal['scientific_qualification'] is not False
        or now['directories']!=old['directories'] or now['symlinks']!=old['symlinks']
        or set(now['files'])!=set(old['files'])|{'cold_closeout_seal.json'}
        or any(now['files'][k]!=v for k,v in old['files'].items())):
        raise ValueError('complete finished cold namespace differs or a failure appeared after seal')
    status=read(OUTPUT/'AAA/run_status.json');case=status['cases']['AAA'];maps=case['maps']
    if (status!=value['original_controller_return'] or status['classification']!='WAITING_REFERENCE'
        or status['prepared_sha256']!=prepared_sha or case['classification']!='VALID_MET'
        or not 1<=len(maps)<=100 or [m['epoch'] for m in maps]!=list(range(1,len(maps)+1))
        or any(m['classification']!='VALID_NOT_MET' for m in maps[:-1]) or maps[-1]['classification']!='VALID_MET'
        or case['final_directory']!=str(OUTPUT/'AAA'/f'map{len(maps):03d}')):
        raise ValueError('continuous original maps ending at first MET required')
    stages=read(OUTPUT/'AAA/stages.json')['stages']
    if not stages or any(stage['status']!='PASS' for stage in stages):raise ValueError('all actual guarded cold stages must PASS')
    for stage in stages:
        folder=OUTPUT/Path(stage['label']).parent;label=Path(stage['label']).name
        watch=read(require(folder/(label+'.watchdog.json')))
        if (watch['command']!=stage['command'] or watch['returncode']!=0 or watch['limit_failure'] is not None
            or watch['own_child_only'] is not True or watch['liveness_group_cleanup'] is not True
            or watch['rss_cap_mib']!=512 or not 0<watch['sampled_peak_rss_mib']<512
            or not 0<=watch['elapsed_seconds']<watch['wall_cap_seconds']<=stage['wall_cap_seconds']):
            raise ValueError('every native/host own-child stage must have real512 bounded cleanup proof')
        require(folder/(label+'.log'),stage['log_sha256'])
    for folder in (OUTPUT/'archives',OUTPUT/'training',OUTPUT/'AAA/bootstrap',
                   *(OUTPUT/'AAA'/f'map{n:03d}' for n in range(1,len(maps)+1))):
        c.verify_sealed_directory(folder)
    return dict(schema='AXMAT_COMBINED_COLD_COMPLETE_INPUT_AND_NATIVE_EXECUTION_ONLY_V1',
        admission='COMPLETE_NEW_COLD_AAA_WAITING_INDEPENDENT_REFERENCE_ONLY',prepared=expected_prepared,
        actual_external_terminal_evidence=dict(path=str(path),sha256=terminal_sha),completed_maps=len(maps),
        final_directory=case['final_directory'],actual_native_children_under_512=True,
        scientific_qualification=False,AAA_accuracy_qualified=False,ABA_admitted=False,
        mandatory_original2000_eight_gate_and120_reference_closeout_pending=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=('declare','prepare','prepare-binding','run-controls','finalize-cold','run-AAA'))
    parser.add_argument('--factory-sha256',required=True);parser.add_argument('--sha256');parser.add_argument('--declaration-terminal-sha256')
    parser.add_argument('--binding-sha256');parser.add_argument('--control-seal-sha256');parser.add_argument('--control-terminal-sha256')
    a=parser.parse_args();
    if nonzero_sha(a.factory_sha256)!=os.environ.get('AXMAT_COLD_FACTORY_SHA256'):raise ValueError('explicit external reviewed source pin and environment differ')
    require_input_ready()  # Every CLI action is currently rejected before any business read/import/write.
    if a.action=='declare':declare()
    elif a.action=='prepare':prepare(a.sha256,a.declaration_terminal_sha256)
    elif a.action=='prepare-binding':prepare_binding(a.sha256,a.declaration_terminal_sha256)
    elif a.action=='run-controls':run_controls(a.binding_sha256,a.declaration_terminal_sha256)
    elif a.action=='finalize-cold':finalize_cold(a.sha256,a.binding_sha256,a.control_seal_sha256,a.control_terminal_sha256,a.declaration_terminal_sha256)
    elif a.action=='run-AAA':run_AAA(a.sha256,a.declaration_terminal_sha256)


if __name__=='__main__':main()
