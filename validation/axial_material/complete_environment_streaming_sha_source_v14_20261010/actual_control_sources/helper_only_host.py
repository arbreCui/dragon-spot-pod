"""One real helper verifier control child under unchanged genuine OwnRSS.

Root alone binds reviewed source pins and observes the actual host terminal.
This host never executes a numerical component, failed V13 audit, transport,
AAA or ABA. Optional history reading is a separate action and fresh namespace.
No imports of business modules or filesystem writes occur at import time.
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

STATUS = 'READY_ROOT_BOUND_HELPER_ONLY_GENUINE_SUPERVISOR'
ROOT = Path('/Users/wen/spot')
ART = ROOT / 'validation/artifacts'
PYTHON = Path('/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12')
DRIVER = ROOT / 'validation/axial_material/complete_environment_streaming_sha_source_v14_20261010/actual_control_sources/helper_only_controls.py'
DRIVER_SHA256 = '6cac4ee465d8c944ae778a403644908f5a9999dd666120c42d7b99357870e9fe'
HELPER = ROOT / 'validation/axial_material/complete_environment_streaming_sha_helper_v14.py'
HELPER_SHA256 = '839ea8cc88e4f10d36b6bd8fcb283c9c774702e4c3688fc8a66831431c1cb5fa'
PROOF = ROOT / 'validation/axial_material/complete_environment_streaming_sha_source_v14_20261010/source_patch_proof.json'
PROOF_SHA256 = 'c7984abe2579399cd6e158a53fe94052e074fec08c03cf596ed859b6fa9321a6'
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
    parser.add_argument('--action', choices=('fixtures', 'historical-environment'), default='fixtures')
    args = parser.parse_args()
    started = time.monotonic()
    if STATUS != 'READY_ROOT_BOUND_HELPER_ONLY_GENUINE_SUPERVISOR':
        raise ValueError('UNREADY: complete independent source review and exact bindings required')
    for value in (DRIVER_SHA256, HELPER_SHA256, PROOF_SHA256):
        if type(value) is not str or len(value) != 64 or any(c not in '0123456789abcdef' for c in value):
            raise ValueError('all actual reviewed source pins required')
    if sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE') or any(os.environ.get(k) != '1' for k in THREAD_KEYS):
        raise ValueError('nonoptimized single-thread interpreter required')
    sys.dont_write_bytecode = True
    if Path(sys.executable).resolve() != PYTHON:
        raise ValueError('declared genuine Python3.12 required')
    token = '20261010' if args.action == 'fixtures' else 'historical-read-20261010'
    host_root = ART / ('axial-material-complete-environment-streaming-sha-helper-only-host-v14-' + token)
    control_root = ART / ('axial-material-complete-environment-streaming-sha-helper-only-controls-v14-' + token)
    if os.path.lexists(host_root) or os.path.lexists(control_root):
        raise ValueError('fresh helper-only evidence namespaces required; no retry')
    inputs = [pin(DRIVER, DRIVER_SHA256), pin(HELPER, HELPER_SHA256), pin(PROOF, PROOF_SHA256),
              pin(FULL, FULL_SHA256), pin(PARENT, PARENT_SHA256), pin(BOUNDED, BOUNDED_SHA256)]
    h, hpin = load(OLD_HELPER, OLD_HELPER_SHA256, 'axmat_v14_controls_genuine_original619')
    resource_factory, resource_pin = load(RESOURCE_FACTORY, RESOURCE_FACTORY_SHA256, 'axmat_v14_controls_genuine_resources_f136')
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
    for name in ('runtime', 'run', 'HELPER_ONLY_CONTROLS'):
        (host_root / name).mkdir()
    shutil.copy2(BOUNDED, host_root / 'runtime/run_bounded_dragon.py')
    remaining = WALL_CAP - (time.monotonic() - started)
    if remaining <= 0:
        raise ValueError('whole helper-control budget exhausted before child launch')
    runner = full.OwnRSSSerialExecutor(host_root, remaining, 'HELPER_ONLY_CONTROLS', resources)
    if (type(runner) is not full.OwnRSSSerialExecutor or runner.resources is not resources
            or Path(runner.bounded.__file__).resolve() != host_root / 'runtime/run_bounded_dragon.py'):
        raise ValueError('genuine supervisor constructor binding differs')
    command = [str(PYTHON), '-B', str(DRIVER), '--action', args.action, '--out', str(control_root)]
    try:
        runner.execute(host_root / 'run', 'controls', command, remaining)
        log = host_root / 'run/controls.log'
        stdout = json.loads(log.read_text())
        result_path = control_root / 'result.json'
        result = json.loads(result_path.read_text())
        watch_path = log.with_suffix('.watchdog.json')
        watch = json.loads(watch_path.read_text())
        after = resources.check()
        elapsed = time.monotonic() - started
        archived = archive_bytes((host_root, control_root))
        expected_status = 'PASS_HELPER_PROTOCOL_ONLY' if args.action == 'fixtures' else 'BOTH_COMPLETE_ENVIRONMENT_PREDICATES_RETURNED'
        if (stdout['status'] != expected_status or result['status'] != expected_status or result['action'] != args.action
                or len(runner.records) != 1 or runner.records[0]['status'] != 'PASS'
                or type(watch['returncode']) is not int or watch['returncode'] != 0
                or watch['command'] != command or watch['limit_failure'] is not None
                or watch['own_child_only'] is not True or watch['liveness_group_cleanup'] is not True
                or not 0 <= watch['sampled_peak_rss_mib'] < RSS_CAP or not elapsed < WALL_CAP
                or not archived < ARCHIVE_CAP):
            raise ValueError('complete actual bounded helper-only control return required')
        for entry in inputs:
            if pin(entry['path'], entry['sha256']) != entry:
                raise ValueError('whole source or proof identity changed during controls')
        value = {'schema': 'AXMAT_V14_HELPER_ONLY_GENUINE_SUPERVISOR_ACTUAL_HOST_V1',
                 'status': 'PASS_HELPER_ONLY_ACTUAL_BOUNDED_HOST', 'action': args.action,
                 'input_sources': inputs, 'original_helper': hpin, 'resource_factory': resource_pin,
                 'actual_command': command, 'actual_full_merged_stdout_stderr': pin(log),
                 'actual_child_result': pin(result_path), 'actual_watchdog': pin(watch_path),
                 'stage_records': runner.records, 'watchdog': watch,
                 'resources_before': before, 'resources_after': after,
                 'resource_roots': [str(x) for x in roots],
                 'whole_elapsed_seconds': elapsed, 'whole_archive_bytes': archived,
                 'whole_wall_cap_seconds': WALL_CAP, 'rss_cap_mib': RSS_CAP,
                 'archive_cap_bytes': ARCHIVE_CAP, 'threads': 1, 'children_at_once': 1, 'retries': 0,
                 'supervisor_class_or_MRO_modified': False, 'failed_V13_audit_reexecuted': False,
                 'numerical_component_or_transport_executed': False,
                 'native_RSS_verified': False, 'AAA_accuracy_qualified': False, 'ABA_admitted': False}
        write_new(host_root / 'result.json', value)
        print(json.dumps({'status': value['status'], 'action': args.action,
                          'host_result': pin(host_root / 'result.json'),
                          'actual_external_Root_terminal_still_required': True}, allow_nan=False), flush=True)
    except BaseException as error:
        write_new(host_root / 'failed_host_result.json', {'status': 'FAILED_HELPER_ONLY_HOST_NO_RETRY',
                  'action': args.action, 'error': repr(error), 'stage_records': runner.records,
                  'elapsed_seconds': time.monotonic() - started,
                  'native_RSS_verified': False, 'AAA_accuracy_qualified': False, 'ABA_admitted': False})
        raise

if __name__ == '__main__':
    main()
