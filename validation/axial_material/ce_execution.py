#!/usr/bin/env python3
"""Run a frozen OpenMC input in one bounded process group, once, without retries."""
import argparse
import datetime
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import signal
import subprocess
import time

import production_inputs
import production_runner
from production_runner import DiskResources, ResourceFailure, validate_resource_roots


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def load_contract(manifest, expected_sha256):
    """Verify the actual imported runtime and explicit resource scope, read-only."""
    manifest = Path(manifest).resolve(strict=True)
    folder = manifest.parent
    if digest(manifest) != expected_sha256:
        raise RuntimeError('execution declaration identity changed')
    contract = json.loads(manifest.read_text())
    if any((folder/name).exists() for name in ('run_claim.json', 'native_result.json', 'openmc.log')):
        raise RuntimeError('existing execution evidence: no duplicate claim or automatic retry')
    if any(folder.glob('statepoint.*.h5')):
        raise RuntimeError('existing statepoints: no automatic retry')
    files = contract['files']
    if not isinstance(files, dict) or not files:
        raise RuntimeError('files must explicitly pin all execution inputs')
    required = [Path(__file__).resolve(), Path(production_runner.__file__).resolve(),
                Path(production_inputs.__file__).resolve(), Path(contract['watchdog_source']).resolve(),
                Path(contract['executable']).resolve()]
    protocol = contract['case_spec']
    case_path = Path(protocol['path']).resolve(strict=True)
    required.append(case_path)
    for path in required:
        if str(path) not in files:
            raise RuntimeError('actual runtime/input file is not frozen: ' + str(path))
    if files[str(case_path)] != protocol['sha256']:
        raise RuntimeError('case_spec identity differs from files manifest')
    for path, expected in contract['files'].items():
        if not Path(path).is_absolute():
            raise RuntimeError('frozen paths must be absolute: ' + path)
        if digest(path) != expected:
            raise RuntimeError('frozen input changed: ' + path)
    case_spec = json.loads(case_path.read_text())
    caps = case_spec['resource_caps']
    cap = contract['wall_seconds']
    if type(cap) is not int or cap not in (120, 1800, 5400) or contract['threads'] != 1:
        raise RuntimeError('undeclared execution budget')
    if (caps['new_numeric_children_at_once'] != 1 or caps['new_child_threads'] != 1
            or caps['automatic_retries_after_solver_failure'] != 0):
        raise RuntimeError('case_spec must retain one child/thread and no retries')
    if cap == 5400:
        path = Path(contract['resource_addendum']).resolve(strict=True)
        if str(path) not in files:
            raise RuntimeError('resource addendum must be frozen')
        supplement = json.loads(path.read_text())
        reference = case_spec['reference']
        if (supplement.get('schema') != 'AXMAT_CE_RESOURCE_ADDENDUM_V1'
                or supplement.get('status') != 'PREDECLARED_BEFORE_FORMAL_CE_TRANSPORT'
                or supplement.get('case_spec_sha256') != protocol['sha256']
                or supplement.get('formal_ce_wall_seconds_per_case') != cap
                or supplement.get('automatic_retries') != 0
                or supplement.get('threads') != 1 or supplement.get('new_numeric_children_at_once') != 1
                or supplement.get('formal_particles_per_batch') != reference['particles_per_batch']
                or supplement.get('formal_inactive_batches') != reference['inactive_batches']
                or supplement.get('formal_active_batches') != reference['active_batches']):
            raise RuntimeError('resource addendum does not admit this run')
    elif cap not in (caps['ce_smoke_wall_s'], caps['ce_production_wall_s_per_case']):
        raise RuntimeError('wall limit differs from frozen case_spec')
    if not isinstance(contract.get('artifact_root'), str):
        raise RuntimeError('manifest must explicitly declare artifact_root')
    artifact_root = Path(contract['artifact_root'])
    if (not artifact_root.is_absolute() or '..' in artifact_root.parts or artifact_root.is_symlink()
            or artifact_root.resolve(strict=True) != artifact_root or not artifact_root.is_dir()):
        raise RuntimeError('artifact_root must be an explicit canonical absolute directory')
    roots = validate_resource_roots(contract['resource_roots'], artifact_root)
    if not any(folder == root or folder.is_relative_to(root) for root in roots):
        raise RuntimeError('resource_roots do not cover this execution output directory')
    if caps['disk_min_free_GiB'] <= 0 or caps['new_case_artifact_budget_GiB'] <= 0:
        raise RuntimeError('resource byte limits must be positive')
    resources = DiskResources(artifact_root, [str(path) for path in roots],
                              int(caps['disk_min_free_GiB']*2**30),
                              int(caps['new_case_artifact_budget_GiB']*2**30))
    before_resources = resources.check()
    return contract, folder, resources, before_resources


def load_watchdog(path):
    spec = importlib.util.spec_from_file_location('axmat_liveness', path)
    if spec is None or spec.loader is None:
        raise RuntimeError('cannot load pinned liveness watchdog')
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    return helper


def execute(manifest, expected_sha256):
    contract, folder, resources, before_resources = load_contract(manifest, expected_sha256)
    cap = contract['wall_seconds']
    helper = load_watchdog(contract['watchdog_source'])
    with (folder/'run_claim.json').open('x') as stream:
        json.dump(dict(started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                       manifest_sha256=expected_sha256, wall_seconds=cap, retries=0,
                       case_spec=contract['case_spec'], artifact_root=contract['artifact_root'],
                       resource_roots=contract['resource_roots']), stream, indent=2)
        stream.flush()
        os.fsync(stream.fileno())
    env = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1',
               VECLIB_MAXIMUM_THREADS='1')
    started = time.monotonic()
    process = watchdog = None
    write_fd = None
    result = dict(status='FAILED', returncode=None, error=None, scientific_acceptance=False,
                  resources_before=before_resources)
    handlers = {sig: signal.signal(sig, signal.default_int_handler)
                for sig in (signal.SIGHUP, signal.SIGINT, signal.SIGTERM)}
    try:
        with (folder/'openmc.log').open('xb') as log:
            result['resources_latest'] = resources.check()
            process = subprocess.Popen([contract['executable'], '-s', '1'], cwd=folder,
                                       stdout=log, stderr=subprocess.STDOUT,
                                       stdin=subprocess.DEVNULL, env=env, start_new_session=True)
            read_fd, write_fd = os.pipe()
            try:
                watchdog = helper.start_liveness_watchdog(read_fd, process.pid, 5.0)
            finally:
                os.close(read_fd)
            deadline = time.monotonic() + cap
            while True:
                result['resources_latest'] = resources.check()
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise subprocess.TimeoutExpired(process.args, cap)
                try:
                    result['returncode'] = process.wait(timeout=min(1.0, remaining))
                    break
                except subprocess.TimeoutExpired:
                    continue
            result['resources_latest'] = resources.check()
            if result['returncode'] != 0:
                raise RuntimeError('OpenMC nonzero exit')
            result['status'] = 'NATIVE_COMPLETE_PENDING_INDEPENDENT_ANALYSIS'
    except BaseException as exc:
        result['error'] = repr(exc)
        if isinstance(exc, ResourceFailure):
            result['status'] = 'FAIL_RESOURCE'
            result['resources_failure'] = exc.snapshot
        if process is not None and process.poll() is None:
            helper.terminate_process_group(process.pid, 5.0, process)
            result['returncode'] = process.wait()
    finally:
        if write_fd is not None:
            if watchdog is not None:
                helper.finish_liveness_watchdog(write_fd, watchdog)
            else:
                os.close(write_fd)
        for sig, handler in handlers.items():
            signal.signal(sig, handler)
        result['elapsed_seconds'] = time.monotonic() - started
        result['log_sha256'] = digest(folder/'openmc.log') if (folder/'openmc.log').is_file() else None
        result['outputs'] = {p.name:digest(p) for p in folder.glob('*.h5')}
        with (folder/'native_result.json').open('x') as stream:
            json.dump(result, stream, indent=2)
            stream.write('\n')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('--sha256', required=True)
    parser.add_argument('--check', action='store_true', help='Verify inputs/resources without creating a claim or child process.')
    args = parser.parse_args()
    if args.check:
        contract, folder, resources, snapshot = load_contract(args.manifest, args.sha256)
        print(json.dumps(dict(status='PREFLIGHT_PASS', native_engines_started=0,
                              artifact_root=contract['artifact_root'], resources=snapshot)), flush=True)
        return
    result = execute(args.manifest, args.sha256)
    print(json.dumps(result), flush=True)
    if result['status'] in ('FAILED', 'FAIL_RESOURCE'):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
