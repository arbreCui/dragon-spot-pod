"""One real read-only metadata diagnostic under the unchanged original supervisor.

Only Root binds this source and starts the new exclusive diagnostic namespace.
No component prepare/build/audit/admit, numerical controls or transport action.
The original619/FULL705/parent38de/boundedbc/f136 resources remain genuine.
Importing this host creates no files and loads no business module.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import stat
import sys
import time

STATUS = 'UNREADY_ROOT_REVIEW_AND_SOURCE_BINDINGS_REQUIRED'
ROOT = Path('/Users/wen/spot')
ART = ROOT / 'validation/artifacts'
PYTHON = Path('/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12')
DRIVER = None
DRIVER_SHA256 = None
TARGET_FACTORY = None
TARGET_FACTORY_SHA256 = None
CANONICAL_TARGET = ROOT / 'validation/axial_material/prepare_qualified_AB_sender_contiguous_flux_window_streaming_sha_production_v14b.py'
HELPER_ADMISSION = ROOT / 'validation/axial_material/complete_environment_streaming_sha_source_v14b_20261010/Root_actual_helper_controls_admission.json'
HELPER_ADMISSION_SHA256 = '16d4548b1cc4ffe935bd8d28219e99a6e9da9af949e7577a82eb758e99d7f568'
HELPER = ROOT / 'validation/axial_material/complete_environment_streaming_sha_helper_v14b.py'
HELPER_SHA256 = '7d740b177f5e1c728f0729df031248fbb396f6978b9a3d5c8776a0c270db48d3'
PROOF = ROOT / 'validation/axial_material/complete_environment_streaming_sha_source_v14b_20261010/source_patch_proof.json'
PROOF_SHA256 = '1809278680379d2ef6ee5c76218d4614abbbc1c9cbcf379674e7540485db86f2'
OLD_HELPER = ROOT / 'validation/axial_material/prepare_qualified_AB_source_factor_production.py'
OLD_HELPER_SHA256 = '619ed1e3115e0f9f25fd20cc259d384891f2fff52d913acebd5d9ca8f39d5743'
RESOURCE_FACTORY = ROOT / 'validation/axial_material/prepare_qualified_AB_rank1_factor_cache_cross_group_identity_key_delta_production.py'
RESOURCE_FACTORY_SHA256 = 'f136baab5047a8727cfd2c0abb5399acf617c25c4f4e7692242419e6f9daef4e'
BOUNDED = ART / 'axial-material-production-qualified-AB-white-trace-refined-envpin-20261005/runtime/run_bounded_dragon.py'
BOUNDED_SHA256 = 'bc4ff7a5dc82ed023b726f2304b6a298954f54d7891414925b7d6d68dd80cf09'
FULL = ROOT / 'validation/axial_material/qualify_refined_AAA_layered_full.py'
FULL_SHA256 = '70516d764e05cffa6e82e780a991ff64e56b9c29bc99f3f1b18bcb0ff63195c6'
PARENT = ART / 'axial-material-production-qualified-AB-white-trace-refined-envpin-20261005/runtime/production_runner.py'
PARENT_SHA256 = '38de03ed0f5b3e2d82b4153a45d1e548d58a34747f526f8bcd51bbe01e935128'
THREAD_KEYS = ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS')
WALL_CAP = 120
RSS_CAP = 512
ARCHIVE_CAP = 64 * 2**20

def identity(path):
    value = Path(path).lstat()
    return [value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_size, value.st_mtime_ns, value.st_ctime_ns]

def pin(path, wanted=None):
    path = Path(path)
    before = identity(path)
    if not stat.S_ISREG(before[2]):
        raise ValueError('source must be a regular file: ' + str(path))
    with path.open('rb') as stream:
        value = hashlib.file_digest(stream, 'sha256').hexdigest()
    if identity(path) != before or (wanted is not None and value != wanted):
        raise ValueError('complete pinned input changed: ' + str(path))
    return {'path': str(path), 'sha256': value, 'identity': before}

def write_new(path, value):
    with Path(path).open('x') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write('\n')

def load(path, wanted, name):
    source = pin(path, wanted)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    if Path(module.__file__).resolve() != path.resolve() or pin(path, wanted) != source:
        raise ValueError('normal canonical source import binding differs')
    return module, source

def archive_bytes(roots):
    total = 0
    for root in roots:
        for parent, dirs, files in os.walk(root, followlinks=False):
            for name in files:
                value = (Path(parent) / name).lstat()
                if stat.S_ISREG(value.st_mode):
                    total += value.st_size
    return total

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    started = time.monotonic()
    if STATUS != 'READY_ROOT_BOUND_READONLY_METADATA_GENUINE_SUPERVISOR':
        raise ValueError('UNREADY: metadata diagnostic source and bindings require Root review')
    for value in (DRIVER_SHA256, TARGET_FACTORY_SHA256, HELPER_SHA256, PROOF_SHA256):
        if type(value) is not str or len(value) != 64 or any(c not in '0123456789abcdef' for c in value):
            raise ValueError('all reviewed metadata source pins required')
    if (DRIVER is None or not Path(DRIVER).is_absolute() or Path(DRIVER).parent.parent != ROOT/'validation/axial_material/complete_environment_streaming_sha_source_v14b_20261010'
            or TARGET_FACTORY is None or Path(TARGET_FACTORY) != CANONICAL_TARGET):
        raise ValueError('normal canonical target and Root-installed metadata driver required')
    if sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE') or any(os.environ.get(k) != '1' for k in THREAD_KEYS):
        raise ValueError('nonoptimized single-thread interpreter required')
    sys.dont_write_bytecode = True
    if Path(sys.executable).resolve() != PYTHON:
        raise ValueError('declared genuine Python3.12 required')
    host_root = ART / 'axial-material-complete-environment-metadata-timing-host-v14b-20261010'
    control_root = ART / 'axial-material-complete-environment-metadata-timing-v14b-20261010'
    if os.path.lexists(host_root) or os.path.lexists(control_root):
        raise ValueError('fresh metadata-only evidence namespaces required; no retry')
    inputs = [pin(DRIVER, DRIVER_SHA256), pin(TARGET_FACTORY, TARGET_FACTORY_SHA256),
              pin(HELPER, HELPER_SHA256), pin(PROOF, PROOF_SHA256), pin(HELPER_ADMISSION, HELPER_ADMISSION_SHA256),
              pin(FULL, FULL_SHA256), pin(PARENT, PARENT_SHA256), pin(BOUNDED, BOUNDED_SHA256)]
    # This imports only the same original supervisor/resource chain already
    # used by H14b. The target factory is imported exclusively by the child.
    h, hpin = load(OLD_HELPER, OLD_HELPER_SHA256, 'axmat_v14b_metadata_genuine_original619')
    resource_factory, resource_pin = load(RESOURCE_FACTORY, RESOURCE_FACTORY_SHA256, 'axmat_v14b_metadata_genuine_resources_f136')
    full, production = h.modules()
    if (full.OwnRSSSerialExecutor.__bases__ != (production.SerialExecutor,)
            or Path(full.__file__).resolve() != FULL or Path(production.__file__).resolve() != PARENT):
        raise ValueError('genuine unchanged supervisor and direct parent MRO required')
    h.guard_admission(full)
    roots = resource_factory.history_roots([str(host_root), str(control_root)], ART)
    resources = resource_factory.resources_for(roots, production.ResourceFailure)
    before = resources.check()
    if before['artifact_bytes'] + ARCHIVE_CAP >= 96 * 2**30 or before['disk_free_bytes'] - ARCHIVE_CAP < 8 * 2**30:
        raise ValueError('original complete-history/free-space allowance required')
    host_root.mkdir()
    for name in ('runtime', 'run', 'METADATA_TIMING'):
        (host_root / name).mkdir()
    shutil.copy2(BOUNDED, host_root / 'runtime/run_bounded_dragon.py')
    remaining = WALL_CAP - (time.monotonic() - started)
    if remaining <= 0:
        raise ValueError('whole metadata-diagnostic budget exhausted before child launch')
    runner = full.OwnRSSSerialExecutor(host_root, remaining, 'METADATA_TIMING', resources)
    if (type(runner) is not full.OwnRSSSerialExecutor or runner.resources is not resources
            or Path(runner.bounded.__file__).resolve() != host_root / 'runtime/run_bounded_dragon.py'):
        raise ValueError('genuine supervisor constructor binding differs')
    command = [str(PYTHON), '-B', str(DRIVER), '--out', str(control_root)]
    try:
        runner.execute(host_root / 'run', 'metadata', command, remaining)
        log = host_root / 'run/metadata.log'
        stdout = json.loads(log.read_text())
        result_path = control_root / 'result.json'
        result = json.loads(result_path.read_text())
        watch_path = log.with_suffix('.watchdog.json')
        watch = json.loads(watch_path.read_text())
        after = resources.check()
        elapsed = time.monotonic() - started
        archived = archive_bytes((host_root, control_root))
        expected_status = 'READONLY_METADATA_PROFILE_COMPLETE_DIAGNOSTIC_ONLY'
        if (stdout['status'] != expected_status or result['status'] != expected_status
                or stdout['result_sha256'] != pin(result_path)['sha256']
                or stdout['Root_actual_child_terminal_required_before_admission'] is not True
                or result['profile']['direct_invocations'] != {name:1 for name in ('sender_source_admission','sender_control_contract','stream_environment_helper_source_admission','source_inputs')}
                or result['profile']['profiler_cleared'] is not True or result['profile']['forbidden_canonical_calls']
                or len(runner.records) != 1 or runner.records[0]['status'] != 'PASS'
                or type(watch['returncode']) is not int or watch['returncode'] != 0
                or watch['command'] != command or watch['limit_failure'] is not None
                or watch['own_child_only'] is not True or watch['liveness_group_cleanup'] is not True
                or not 0 <= watch['sampled_peak_rss_mib'] < RSS_CAP or not elapsed < WALL_CAP
                or not archived < ARCHIVE_CAP):
            raise ValueError('complete actual bounded metadata-only diagnostic return required')
        for entry in inputs:
            if pin(entry['path'], entry['sha256']) != entry:
                raise ValueError('whole source or proof identity changed during metadata diagnostic')
        value = {'schema':'AXMAT_V14B_READONLY_METADATA_GENUINE_SUPERVISOR_ACTUAL_HOST_V1',
                 'status':'ACTUAL_BOUNDED_METADATA_DIAGNOSTIC_CLOSED_EXTERNAL_ROOT_REQUIRED',
                 'input_sources':inputs,'original_helper':hpin,'resource_factory':resource_pin,
                 'actual_command':command,'actual_full_merged_stdout_stderr':pin(log),
                 'actual_child_result':pin(result_path),'actual_watchdog':pin(watch_path),
                 'stage_records':runner.records,'watchdog':watch,
                 'resources_before':before,'resources_after':after,'resource_roots':[str(x) for x in roots],
                 'whole_elapsed_seconds':elapsed,'whole_archive_bytes':archived,
                 'whole_wall_cap_seconds':WALL_CAP,'rss_cap_mib':RSS_CAP,'archive_cap_bytes':ARCHIVE_CAP,
                 'threads':1,'children_at_once':1,'retries':0,
                 'supervisor_class_or_MRO_modified':False,'failed_V13_audit_reexecuted':False,
                 'old_failed_V13_factory_imported_or_called':False,'four_pure_metadata_calls_only':True,
                 'numerical_component_or_transport_executed':False,'original86_stage_count_increment':0,
                 'native_RSS_verified':False,'AAA_accuracy_qualified':False,'ABA_admitted':False}
        write_new(host_root/'result.json',value)
        print(json.dumps({'status':value['status'],'host_result':pin(host_root/'result.json'),
                          'actual_external_Root_terminal_still_required':True},allow_nan=False),flush=True)
    except BaseException as error:
        write_new(host_root/'failed_host_result.json',{'status':'FAILED_METADATA_ONLY_HOST_NO_RETRY',
            'error':repr(error),'stage_records':runner.records,'elapsed_seconds':time.monotonic()-started,
            'native_RSS_verified':False,'AAA_accuracy_qualified':False,'ABA_admitted':False})
        raise

if __name__ == '__main__':
    main()
