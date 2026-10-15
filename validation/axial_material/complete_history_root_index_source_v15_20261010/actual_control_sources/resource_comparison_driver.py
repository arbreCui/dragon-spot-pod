"""One normal-import full-history resource comparison; no business CLI calls."""
import ast
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import sys
import time

ROOT = Path('/Users/wen/spot')
ART = ROOT / 'validation/artifacts'
OLD = ROOT / 'validation/axial_material/prepare_qualified_AB_moment_order_production.py'
OLD_SHA = 'fe81150fbf270cac44e241ad64f352cf2f623fa65f7ccb4a9b0ded0a4f2c2d41'
NEW = ROOT / 'validation/axial_material/moment_order_complete_history_resource_trie_20261010.py'
NEW_SHA = 'ebbb0235ca5eaf7f7d896c225925f6705d2ba32f70295d957206548571575022'
DECL = ART / 'axial-material-sender-contiguous-flux-window-streaming-sha-build-v14b-20261010/declaration.json'
DECL_SHA = 'd0eab52ad5c938cb7acf1e5216475f5d72c5c0a785ec589effad0951a00ed117'
OUT = ART / 'axial-material-complete-history-root-index-controls-v15-20261010'
HOST = ART / 'axial-material-complete-history-root-index-host-v15-20261010'

def pin(path, wanted=None):
    path = Path(path)
    a = path.lstat()
    ident = lambda x: [x.st_dev,x.st_ino,x.st_mode,x.st_nlink,x.st_size,x.st_mtime_ns,x.st_ctime_ns]
    if not stat.S_ISREG(a.st_mode):
        raise ValueError('regular pinned input required')
    with path.open('rb') as stream:
        value = hashlib.file_digest(stream,'sha256').hexdigest()
    if ident(a) != ident(path.lstat()) or (wanted is not None and value != wanted):
        raise ValueError('whole source or input changed: '+str(path))
    return dict(path=str(path),sha256=value,identity=ident(a),size_bytes=a.st_size)

def load(path, wanted, name):
    source = pin(path,wanted)
    spec = importlib.util.spec_from_file_location(name,path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    if Path(module.__file__).resolve() != path or module.ROOT != ROOT or module.ART != ART or pin(path,wanted) != source:
        raise ValueError('normal source/module/ROOT binding differs')
    return module,source

def main():
    if len(sys.argv) != 1 or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE') or sys.getprofile() is not None:
        raise ValueError('fixed nonoptimized unprofiled resource comparison required')
    if not OUT.is_dir() or list(OUT.iterdir()):
        raise ValueError('Root-created exclusive empty controls namespace required; no retry')
    started = time.monotonic()
    old,oldpin = load(OLD,OLD_SHA,'axmat_v15_original_resource_control')
    new,newpin = load(NEW,NEW_SHA,'axmat_v15_new_resource_control')
    pins = [oldpin,newpin,pin(DECL,DECL_SHA)]
    for module in (old,new):
        pins.extend([pin(module.RESOURCE_SPEC,module.RESOURCE_SPEC_SHA),pin(module.RESOURCE_ADDENDUM,module.RESOURCE_ADDENDUM_SHA)])
        if module.DynamicHistoryResources.__bases__ != (object,) or module.DynamicHistoryResources.__module__ != module.__name__:
            raise ValueError('real normally defined resource class required')
    def segments(path):
        source = path.read_text()
        return {n.name:ast.get_source_segment(source,n) for n in ast.parse(source).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
    a,b = segments(OLD),segments(NEW)
    if a.keys() != b.keys() or [name for name in a if a[name]!=b[name]] != ['validate_history_roots']:
        raise ValueError('sole validator edit and unchanged complete real class required')
    fixture = OUT/'fixtures';fixture.mkdir()
    directory = fixture/'directory';directory.mkdir()
    regular = fixture/'regular';regular.write_bytes(b'resource-control-payload\n')
    os.link(regular,fixture/'hardlink')
    (fixture/'directory_link').symlink_to(directory,target_is_directory=True)
    (fixture/'dangling').symlink_to(fixture/'missing_target')
    (fixture/'cycle').symlink_to(fixture/'cycle')
    cases = [([],False),([Path(directory)],False),(['relative'],False),([str(ART)],False),
        ([str(directory/'..'/'future')],False),([str(regular)],False),([str(fixture/'hardlink')],False),
        ([str(fixture/'directory_link')],False),([str(fixture/'directory_link'/'future')],False),
        ([str(fixture/'dangling')],False),([str(fixture/'cycle')],False),
        ([str(directory),str(directory)],False),([str(directory),str(directory/'future')],False),
        ([str(directory/'future'),str(directory)],False),([str(fixture/'future_b'),str(fixture/'future_a')],True)]
    outcomes = []
    for values,wanted in cases:
        pair=[]
        for module in (old,new):
            try:
                value=module.validate_history_roots(values,ART)
                pair.append(dict(ok=True,returned=[str(x) for x in value],types=[type(x).__name__ for x in value]))
            except BaseException as error:
                pair.append(dict(ok=False,type=type(error).__name__,message=str(error)))
        if pair[0] != pair[1] or pair[0]['ok'] != wanted:
            raise ValueError('normal-import negative/positive validator control differs')
        outcomes.append(dict(values=[str(v) for v in values],original=pair[0],candidate=pair[1]))
    constructor_rejections=[]
    for floor,budget in ((8*2**30-1,96*2**30),(8*2**30,96*2**30-1)):
        pair=[]
        for module in (old,new):
            try:
                module.DynamicHistoryResources(ART,[str(directory)],floor,budget,RuntimeError)
                raise ValueError('changed resource caps unexpectedly accepted')
            except ValueError as error:
                pair.append(dict(type=type(error).__name__,message=str(error)))
        if pair[0] != pair[1] or pair[0]['message'] != 'unchanged complete-history96GiB/free8GiB caps required':
            raise ValueError('original constructor resource caps rejection required')
        constructor_rejections.append(dict(floor=floor,budget=budget,original=pair[0],candidate=pair[1]))
    d=json.loads(DECL.read_text())
    roots=old.history_roots(sorted(set(d['resource_roots'])|{str(OUT),str(HOST)}),ART)
    if roots != new.history_roots(sorted(set(d['resource_roots'])|{str(OUT),str(HOST)}),ART):
        raise ValueError('complete original roots and dynamic family union required')
    objects={}
    for label,module in (('old',old),('new',new)):
        obj=module.DynamicHistoryResources(ART,roots,8*2**30,96*2**30,RuntimeError)
        if type(obj) is not module.DynamicHistoryResources or obj.failure_type is not RuntimeError or obj.declared_roots != roots:
            raise ValueError('normal genuine resource constructor and failure forwarding differ')
        objects[label]=obj
    validator_times=[];snapshots=[]
    for label in ('old','new','new','old'):
        module=old if label=='old' else new
        stamp=time.monotonic();returned=module.validate_history_roots(roots,ART)
        elapsed=time.monotonic()-stamp
        if [str(x) for x in returned] != roots:
            raise ValueError('all roots and original order must be preserved')
        validator_times.append(dict(label=label,seconds=elapsed,root_count=len(roots)))
        stamp=time.monotonic();snapshot=objects[label].check();elapsed=time.monotonic()-stamp
        if snapshot['artifact_budget_bytes'] != 96*2**30 or snapshot['min_free_bytes'] != 8*2**30 or snapshot['artifact_bytes'] >= 96*2**30 or snapshot['disk_free_bytes'] < 8*2**30:
            raise ValueError('all fresh resource limits required')
        snapshots.append(dict(label=label,seconds=elapsed,complete_snapshot=snapshot))
    # Observation timestamps and free disk are live values. Preserve all four
    # complete observations and compare every other field exactly.
    semantic=lambda x:{k:v for k,v in x.items() if k not in ('checked_unix','disk_free_bytes')}
    if any(semantic(x['complete_snapshot']) != semantic(snapshots[0]['complete_snapshot']) for x in snapshots):
        raise ValueError('all root, file count, apparent bytes and contract observations must agree')
    for source in pins:
        if pin(source['path'],source['sha256']) != source:
            raise ValueError('whole normal resource source inputs changed')
    value=dict(schema='AXMAT_V15_ACTUAL_RESOURCE_MODULE_COMPARISON_V1',status='PASS_RESOURCE_MODULE_COMPARISON_ONLY',
        source_inputs=pins,actual_unique_normal_module_names=[old.__name__,new.__name__],
        original_resource_class_check_init_MRO_source_unchanged=True,no_old_module_or_class_monkeypatch=True,
        normal_import_validator_controls=outcomes,normal_import_constructor_cap_rejections=constructor_rejections,
        complete_declared_and_dynamic_resource_roots=roots,
        normal_import_ABBA_validator_timings=validator_times,normal_import_ABBA_resource_checks=snapshots,
        all_semantic_snapshot_fields_equal=True,fresh_complete_history_checks=True,
        no_content_SHA_or_stat_cache_added=True,profile_used=False,elapsed_seconds=time.monotonic()-started,
        reliable_whole_component_runtime_gain_proven=False,full86_executed=False,
        native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False)
    with (OUT/'result.json').open('x') as stream:
        json.dump(value,stream,indent=2,allow_nan=False);stream.write('\n')
    print(json.dumps(dict(status=value['status'],result=pin(OUT/'result.json')),allow_nan=False),flush=True)

if __name__ == '__main__':
    main()
