"""Actual resource comparison with the unchanged original OwnRSS supervisor."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import stat
import sys
import time
ROOT=Path('/Users/wen/spot')
ART=ROOT/'validation/artifacts'
PYTHON=Path('/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12')
DRIVER=ROOT/'validation/axial_material/complete_history_root_index_source_v15_20261010/actual_control_sources/resource_comparison_driver.py'
DRIVER_SHA='8836bc67a2353f97c40232cfd5c8822c602df4a89fda635c39230471ba875948'
OLD_HELPER=ROOT/'validation/axial_material/prepare_qualified_AB_source_factor_production.py'
OLD_HELPER_SHA='619ed1e3115e0f9f25fd20cc259d384891f2fff52d913acebd5d9ca8f39d5743'
RESOURCE=ROOT/'validation/axial_material/prepare_qualified_AB_rank1_factor_cache_cross_group_identity_key_delta_production.py'
RESOURCE_SHA='f136baab5047a8727cfd2c0abb5399acf617c25c4f4e7692242419e6f9daef4e'
FULL=ROOT/'validation/axial_material/qualify_refined_AAA_layered_full.py'
FULL_SHA='70516d764e05cffa6e82e780a991ff64e56b9c29bc99f3f1b18bcb0ff63195c6'
PARENT=ART/'axial-material-production-qualified-AB-white-trace-refined-envpin-20261005/runtime/production_runner.py'
PARENT_SHA='38de03ed0f5b3e2d82b4153a45d1e548d58a34747f526f8bcd51bbe01e935128'
BOUNDED=PARENT.parent/'run_bounded_dragon.py'
BOUNDED_SHA='bc4ff7a5dc82ed023b726f2304b6a298954f54d7891414925b7d6d68dd80cf09'
HOST=ART/'axial-material-complete-history-root-index-host-v15-20261010'
OUT=ART/'axial-material-complete-history-root-index-controls-v15-20261010'
WALL,RSS,ARCHIVE=120,512,64*2**20
THREAD_KEYS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')

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
    started=time.monotonic()
    if len(sys.argv)!=1 or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE') or sys.getprofile() is not None or any(os.environ.get(k)!='1' for k in THREAD_KEYS) or Path(sys.executable).resolve()!=PYTHON:
        raise ValueError('fixed nonoptimized unprofiled single-thread host required')
    sys.dont_write_bytecode=True
    if os.path.lexists(HOST) or os.path.lexists(OUT):
        raise ValueError('fresh exclusive resource control roots required; no retry')
    diagnostic,d_pin=load(DRIVER,DRIVER_SHA,'axmat_v15_root_resource_control_driver')
    sources=[d_pin,pin(diagnostic.OLD,diagnostic.OLD_SHA),pin(diagnostic.NEW,diagnostic.NEW_SHA),pin(diagnostic.DECL,diagnostic.DECL_SHA),pin(FULL,FULL_SHA),pin(PARENT,PARENT_SHA),pin(BOUNDED,BOUNDED_SHA)]
    h,hpin=load(OLD_HELPER,OLD_HELPER_SHA,'axmat_v15_original_resource_supervisor_helper619')
    r,rpin=load(RESOURCE,RESOURCE_SHA,'axmat_v15_original_resource_supervisor_f136')
    full,production=h.modules()
    if full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,) or Path(full.__file__).resolve()!=FULL or Path(production.__file__).resolve()!=PARENT:
        raise ValueError('genuine original supervisor/MRO required')
    h.guard_admission(full)
    d=json.loads(diagnostic.DECL.read_text())
    roots=r.history_roots(sorted(set(d['resource_roots'])|{str(HOST),str(OUT)}),ART)
    resources=r.resources_for(roots,production.ResourceFailure)
    before=resources.check()
    if before['artifact_bytes']+ARCHIVE>=96*2**30 or before['disk_free_bytes']-ARCHIVE<8*2**30:
        raise ValueError('unchanged full-history/free-space reservation required')
    HOST.mkdir();OUT.mkdir()
    for name in ('runtime','run','RESOURCE_COMPARE'):(HOST/name).mkdir()
    shutil.copy2(BOUNDED,HOST/'runtime/run_bounded_dragon.py')
    remaining=WALL-(time.monotonic()-started)
    if remaining<=0:raise ValueError('whole host budget exhausted before child')
    runner=full.OwnRSSSerialExecutor(HOST,remaining,'RESOURCE_COMPARE',resources)
    if type(runner) is not full.OwnRSSSerialExecutor or runner.resources is not resources or Path(runner.bounded.__file__).resolve()!=HOST/'runtime/run_bounded_dragon.py':
        raise ValueError('genuine unchanged own-RSS constructor required')
    command=[str(PYTHON),'-B',str(DRIVER)]
    try:
        runner.execute(HOST/'run','compare',command,remaining)
        log=HOST/'run/compare.log';stdout=json.loads(log.read_text())
        result_path=OUT/'result.json';result=json.loads(result_path.read_text())
        watch_path=log.with_suffix('.watchdog.json');watch=json.loads(watch_path.read_text())
        after=resources.check();elapsed=time.monotonic()-started;archived=archive_bytes((HOST,OUT))
        if stdout['status']!='PASS_RESOURCE_MODULE_COMPARISON_ONLY' or result['status']!=stdout['status'] or stdout['result']['sha256']!=pin(result_path)['sha256'] or result['profile_used'] is not False or result['fresh_complete_history_checks'] is not True or result['all_semantic_snapshot_fields_equal'] is not True:
            raise ValueError('actual full comparison result and complete snapshot agreement required')
        if len(result['normal_import_ABBA_resource_checks'])!=4 or [x['label'] for x in result['normal_import_ABBA_resource_checks']]!=['old','new','new','old'] or len(result['normal_import_validator_controls'])!=15 or len(result['normal_import_constructor_cap_rejections'])!=2:
            raise ValueError('all normal-import control and full ABBA checks required')
        if len(runner.records)!=1 or runner.records[0]['status']!='PASS' or type(watch['returncode']) is not int or watch['returncode']!=0 or watch['limit_failure'] is not None or watch['command']!=command or watch['own_child_only'] is not True or watch['liveness_group_cleanup'] is not True:
            raise ValueError('one closed genuine guarded child PASS required')
        if type(watch['pid']) is not int or watch['pid']<=0 or watch['rss_cap_mib']!=RSS or not 0<watch['elapsed_seconds']<watch['wall_cap_seconds']<=runner.records[0]['wall_cap_seconds']<=WALL or not 0<=watch['sampled_peak_rss_mib']<RSS or not elapsed<WALL or not archived<ARCHIVE:
            raise ValueError('all actual original resource control caps required')
        for source in sources+[hpin,rpin]:
            if pin(source['path'],source['sha256'])!=source:raise ValueError('source changed during actual resource comparison')
        value=dict(schema='AXMAT_V15_GENUINE_RESOURCE_COMPARISON_HOST_V1',status='ACTUAL_RESOURCE_COMPARISON_CLOSED_EXTERNAL_ROOT_REQUIRED',input_sources=sources,original_helper=hpin,resource_factory=rpin,
            actual_command=command,actual_full_merged_stdout_stderr=pin(log),actual_control_result=pin(result_path),actual_watchdog=pin(watch_path),stage_records=runner.records,watchdog=watch,
            resources_before=before,resources_after=after,whole_elapsed_seconds=elapsed,archive_bytes_before_host_result=archived,
            qualified_caps=dict(history_bytes=96*2**30,free_floor_bytes=8*2**30,host_wall_seconds=WALL,rss_mib=RSS,archive_bytes=ARCHIVE,threads=1,children=1,retries=0),
            original_supervisor_or_MRO_modified=False,normal_import_resource_module_comparison_only=True,
            reliable_whole_component_runtime_gain_proven=False,full86_executed=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False)
        write_new(HOST/'result.json',value)
        if archive_bytes((HOST,OUT))>=ARCHIVE or time.monotonic()-started>=WALL:raise ValueError('final host whole cap exceeded')
        print(json.dumps(dict(status=value['status'],host_result=pin(HOST/'result.json'),external_Root_actual_terminal_required=True),allow_nan=False),flush=True)
    except BaseException as error:
        write_new(HOST/'failed_host_result.json',dict(status='FAILED_RESOURCE_COMPARISON_NO_RETRY',error=repr(error),stage_records=runner.records,elapsed_seconds=time.monotonic()-started,full86_executed=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False))
        raise

if __name__=='__main__':main()
