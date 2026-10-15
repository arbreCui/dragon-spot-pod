"""One normal canonical complete preparation under the unchanged OwnRSS guard.
Unprofiled; all original preparation gates and complete resource scans remain.
"""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import stat
import sys
import time
ROOT = Path('/Users/wen/spot')
ART = ROOT / 'validation/artifacts'
PYTHON = Path('/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12')
BASE = ROOT / 'validation/axial_material/complete_history_root_index_source_v15_20261010'
DRIVER = BASE / 'actual_prepare_sources/prepare_cli_driver_v15.py'
DRIVER_SHA256 = 'c6984b157ff92b4ec7be9cda54f42e6d1ff0fd4391d25a0a85ab7bb2b2ca9c08'
TARGET = ROOT / 'validation/axial_material/prepare_qualified_AB_sender_contiguous_flux_window_root_index_production_v15.py'
TARGET_SHA = 'cc4b0fda4ab63d11debee532fdfbc399f5f7a68f753e20d1cff928e607a47447'
OLD_HELPER = ROOT / 'validation/axial_material/prepare_qualified_AB_source_factor_production.py'
OLD_HELPER_SHA = '619ed1e3115e0f9f25fd20cc259d384891f2fff52d913acebd5d9ca8f39d5743'
RESOURCE_FACTORY = ROOT / 'validation/axial_material/moment_order_complete_history_resource_trie_20261010.py'
RESOURCE_SHA = 'ebbb0235ca5eaf7f7d896c225925f6705d2ba32f70295d957206548571575022'
FULL = ROOT / 'validation/axial_material/qualify_refined_AAA_layered_full.py'
FULL_SHA = '70516d764e05cffa6e82e780a991ff64e56b9c29bc99f3f1b18bcb0ff63195c6'
PARENT = ART / 'axial-material-production-qualified-AB-white-trace-refined-envpin-20261005/runtime/production_runner.py'
PARENT_SHA = '38de03ed0f5b3e2d82b4153a45d1e548d58a34747f526f8bcd51bbe01e935128'
BOUNDED = PARENT.parent / 'run_bounded_dragon.py'
BOUNDED_SHA = 'bc4ff7a5dc82ed023b726f2304b6a298954f54d7891414925b7d6d68dd80cf09'
HOST_OUT = ART / 'axial-material-complete-prepare-host-v15-20261010'
PROFILE_OUT = ART / 'axial-material-complete-prepare-evidence-v15-20261010'
SOURCE = ART / 'axial-material-qualified-AB-sender-contiguous-flux-window-root-index-build-admission-v15-20261010'
OUT = ART / 'axial-material-sender-contiguous-flux-window-root-index-build-v15-20261010'
TERMINAL = ART / 'axial-material-qualified-AB-sender-contiguous-flux-window-root-index-build-terminal-v15-20261010'
WHOLE_CAP, STAGE_CAP, RSS_CAP = 1800, 600, 512
ARCHIVE_CAP = 2 * 2**30
THREAD_KEYS = ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')

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
    started = time.monotonic()
    if len(sys.argv) != 1 or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE') or sys.getprofile() is not None:
        raise ValueError('fixed nonoptimized preparation host required')
    if any(os.environ.get(k) != '1' for k in THREAD_KEYS) or Path(sys.executable).resolve() != PYTHON:
        raise ValueError('declared single-thread Python3.12 required')
    sys.dont_write_bytecode = True
    for path in (HOST_OUT, PROFILE_OUT, SOURCE, OUT, TERMINAL):
        if os.path.lexists(path):
            raise ValueError('all actual preparation namespaces must be fresh; no retry: '+str(path))
    inputs = [pin(DRIVER,DRIVER_SHA256),pin(TARGET,TARGET_SHA),pin(FULL,FULL_SHA),pin(PARENT,PARENT_SHA),pin(BOUNDED,BOUNDED_SHA)]
    diagnostic, diagnostic_pin = load(DRIVER,DRIVER_SHA256,'axmat_v15_complete_prepare_unprofiled_driver')
    inputs.append(pin(diagnostic.OLD_RECEIPT,diagnostic.OLD_RECEIPT_SHA))
    inputs.append(pin(BASE/'Root_actual_resource_module_admission.json','5a0b2c1870ba1f0cced713bb3528fb9c13928aaf436859763c97edb19afd7676'))
    h,hpin = load(OLD_HELPER,OLD_HELPER_SHA,'axmat_v15_complete_prepare_original619')
    resource_factory,rpin = load(RESOURCE_FACTORY,RESOURCE_SHA,'axmat_v15_complete_prepare_resources_root_index')
    full,production = h.modules()
    if full.OwnRSSSerialExecutor.__bases__ != (production.SerialExecutor,) or Path(full.__file__).resolve() != FULL or Path(production.__file__).resolve() != PARENT:
        raise ValueError('genuine supervisor/MRO/source paths required')
    h.guard_admission(full)
    roots = resource_factory.history_roots([str(p) for p in (HOST_OUT,PROFILE_OUT,SOURCE,OUT,TERMINAL)],ART)
    resources = resource_factory.DynamicHistoryResources(ART,roots,8*2**30,96*2**30,production.ResourceFailure)
    runner = None
    try:
        before = resources.check()
        if before['artifact_bytes']+ARCHIVE_CAP >= 96*2**30 or before['disk_free_bytes']-ARCHIVE_CAP < 8*2**30:
            raise ValueError('complete-history96GiB/free8GiB reserve required')
        HOST_OUT.mkdir();PROFILE_OUT.mkdir()
        for name in ('runtime','run','COMPLETE_PREPARE'):
            (HOST_OUT/name).mkdir()
        shutil.copy2(BOUNDED,HOST_OUT/'runtime/run_bounded_dragon.py')
        remaining = WHOLE_CAP-(time.monotonic()-started)
        if remaining <= 0:
            raise ValueError('whole preparation host budget exhausted')
        runner = full.OwnRSSSerialExecutor(HOST_OUT,remaining,'COMPLETE_PREPARE',resources)
        if type(runner) is not full.OwnRSSSerialExecutor or runner.resources is not resources or Path(runner.bounded.__file__).resolve() != HOST_OUT/'runtime/run_bounded_dragon.py':
            raise ValueError('genuine unchanged runner binding differs')
        command = [str(PYTHON),'-B',str(DRIVER)]
        runner.execute(HOST_OUT/'run','prepare',command,STAGE_CAP)
        log = HOST_OUT/'run/prepare.log'
        stdout = json.loads(log.read_text())
        child_path = PROFILE_OUT/'child_prepare_result.json'
        child = json.loads(child_path.read_text())
        watch_path = log.with_suffix('.watchdog.json')
        watch = json.loads(watch_path.read_text())
        declaration = OUT/'declaration.json'
        d = json.loads(declaration.read_text())
        after = resources.check()
        archived = archive_bytes((HOST_OUT,PROFILE_OUT,SOURCE,OUT))
        elapsed = time.monotonic()-started
        if stdout['classification'] != 'DECLARED_SENDER_CONTIGUOUS_FLUX_WINDOW_ROOT_INDEX_BUILD_ONLY_V15' or stdout['declaration'] != str(declaration) or stdout['declaration_sha256'] != pin(declaration)['sha256']:
            raise ValueError('actual normal canonical preparation stdout required')
        if child['status'] != 'PREPARE_RETURNED' or child['failure'] is not None or child['profile_used'] is not False or child['canonical_cli_completed'] is not True:
            raise ValueError('complete unprofiled canonical child preparation return required')
        if len(runner.records) != 1 or runner.records[0]['status'] != 'PASS' or type(watch['returncode']) is not int or watch['returncode'] != 0 or watch['command'] != command or watch['limit_failure'] is not None or watch['own_child_only'] is not True or watch['liveness_group_cleanup'] is not True:
            raise ValueError('one actual guarded child PASS required')
        if type(watch['pid']) is not int or watch['pid'] <= 0 or watch['rss_cap_mib'] != RSS_CAP or not 0 < watch['elapsed_seconds'] < watch['wall_cap_seconds'] <= runner.records[0]['wall_cap_seconds'] <= STAGE_CAP:
            raise ValueError('actual child PID and original wall/RSS limit metadata required')
        if not 0 <= watch['sampled_peak_rss_mib'] < RSS_CAP or not elapsed < WHOLE_CAP or not archived < ARCHIVE_CAP or os.path.lexists(TERMINAL):
            raise ValueError('original caps or prepare-only namespace boundary violated')
        if d['complete_stage_count'] != 86 or len(d['build_commands']) != 12 or (d['total_wall_seconds'],d['stage_wall_seconds'],d['rss_cap_mib'],d['archive_reserve_bytes']) != (1800,600,512,2*2**30) or d['AAA_accuracy_qualified'] or d['ABA_admitted']:
            raise ValueError('all original future stages/caps and science boundaries required')
        for entry in inputs+[hpin,rpin]:
            if pin(entry['path'],entry['sha256']) != entry:
                raise ValueError('complete preparation input source identity changed')
        value = dict(schema='AXMAT_V15_ROOT_COMPLETE_PREPARE_GENUINE_HOST_V1',status='ACTUAL_COMPLETE_PREPARE_CLOSED_EXTERNAL_ROOT_REQUIRED',
            input_sources=inputs,original_helper=hpin,resource_factory=rpin,actual_command=command,
            actual_full_merged_stdout_stderr=pin(log),actual_child_prepare_result=pin(child_path),actual_watchdog=pin(watch_path),
            actual_declaration=pin(declaration),actual_source_admission=pin(SOURCE/'source_admission.json'),
            stage_records=runner.records,watchdog=watch,resources_before=before,resources_after=after,
            profile_used=False,whole_elapsed_seconds=elapsed,whole_archive_bytes=archived,
            whole_wall_cap_seconds=WHOLE_CAP,stage_wall_cap_seconds=STAGE_CAP,rss_cap_mib=RSS_CAP,archive_cap_bytes=ARCHIVE_CAP,
            threads=1,children_at_once=1,retries=0,supervisor_class_or_MRO_modified=False,
            canonical_prepare_completed=True,full86_executed=False,compilation_or_transport_launched=False,
            native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False)
        write_new(HOST_OUT/'result.json',value)
        if archive_bytes((HOST_OUT,PROFILE_OUT,SOURCE,OUT)) >= ARCHIVE_CAP or time.monotonic()-started >= WHOLE_CAP:
            raise ValueError('final complete preparation host cap exceeded')
        print(json.dumps(dict(status=value['status'],host_result=pin(HOST_OUT/'result.json'),actual_external_Root_terminal_still_required=True),allow_nan=False),flush=True)
    except BaseException as error:
        if HOST_OUT.is_dir():
            write_new(HOST_OUT/'failed_host_result.json',dict(status='FAILED_COMPLETE_PREPARE_NO_RETRY',error=repr(error),
                stage_records=[] if runner is None else runner.records,profile_used=False,elapsed_seconds=time.monotonic()-started,
                full86_executed=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False))
        raise
if __name__ == '__main__':
    main()
