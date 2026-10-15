"""Finite read-only follow-up candidate report. All cache/metadata candidates HOLD."""
from pathlib import Path
import hashlib, json, os, stat

O=Path('/private/tmp/spot_storage_twentieth_compiled_and_metadata_review_20261009')
A=Path('/Users/wen/spot/validation/artifacts')
G=A/'axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-v9-20261009/input_graph.json'
B=A/'axial-material-production-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-last-cprime-trim-file-snapshot-scipy-env-physical-basis-own-pid-peak-v9-20261009/own_rss_binding.json'
F=Path('/private/tmp/spot_v9_actual_finalization_full_source_independent_review_20261009/REPORT.json')
C=Path('/private/tmp/axmat_v9_cold_actual_finalization_postterminal_scope_20261009/finalization_config_ROOT_OBSERVED.json')
I=Path('/private/tmp/spot_storage_twentieth_root_20261009/inventory.json')
FIELDS=('dev','ino','mode','size','mtime_ns','ctime_ns','nlink');pins=[]

def identity(p):
    s=p.lstat();return [getattr(s,'st_'+k) for k in FIELDS]

def raw(p,h=None):
    p=Path(p);s=p.lstat();before=identity(p)
    if not stat.S_ISREG(s.st_mode):raise ValueError('regular metadata source')
    b=p.read_bytes();sha=hashlib.sha256(b).hexdigest()
    if identity(p)!=before or h is not None and h!=sha:raise ValueError('metadata source changed')
    pins.append({'path':str(p),'sha256':sha,'bytes':len(b),'identity':before});return b

def load(p,h=None):return json.loads(raw(p,h))

def main():
    g=load(G,'0e365ebbaafa0d9e9b3a34eee89cc9c3e1de3ee47812d985135b8201bd001be3')
    b=load(B,'4e8de93043fa08ac0c6e1f1702b69606a6bf0b155c30007c356ec4837919c930')
    f=load(F,'ead5085edb5b09ab3a2de65102565bc7493672302c2f4873512b0b3c7594d85e')
    c=load(C,'8f5936308ad6ee031fc4328423966b9f0db069d27b5c1ce932f41a72d8a87174');inv=load(I)
    held=set(b['files'])|{p['path'] for p in g['canonical_files']}|set(g['requirements']['paths'])|{str(G),str(B)}|{p['path'] for p in f['all_fresh_pins']}
    for n in g['namespaces']:
        held|={str(Path(n['canonical_root'])/p) for p in n['files']}
        held|={str(Path(n['canonical_root'])/p) for p in n['symlinks']}
    for n in g['aliases']:held|={n['path'],n['target']}
    current=list(c['roots'].values())
    def protected(p):return str(p) in held or any(str(p)==r or str(p).startswith(r+'/') for r in current)
    meta=[];mandatory=[]
    for row in inv['all_large_regular_files']:
        p=Path(row['path'])
        if not str(p).startswith(str(A)+'/') or p.name not in ('input_graph.json','own_rss_binding.json','complete_input_graph.json','ALL_FILES.jsonl','case_spec.json'):continue
        if identity(p)!=row['identity']:raise ValueError('candidate or keep metadata changed')
        r={'path':str(p),'logical_bytes':row['size_bytes'],'allocated_bytes':row['allocated_bytes'],'identity':row['identity'],'original_inventory_prefilter_flag':row['current_graph_protected']}
        if protected(p):r.update(status='KEEP_CURRENT_PROVEN_DEPENDENCY',reason='Current full source/input closure, explicit graph itself, canonical or namespace or four active evidence roots');mandatory.append(r)
        else:r.update(status='HOLD_NOT_SELECTED_THIS_ROUND',reason='Old audit metadata could be tested for whole-byte lossless gzip separately, but no compression or replacement measured or authorized in this fixed D4A30 cleanup');meta.append(r)
    D=A/'gmres-activity-build';S=D/'source';objects=[]
    for p in sorted(S.rglob('*.o')):
        if p.is_symlink() or not p.is_file():continue
        before=identity(p);q=[];seen_source_inodes=set()
        for e in ('.f','.f90','.F','.F90','.c','.cpp'):
            candidate=p.with_suffix(e)
            if not candidate.is_file() or candidate.is_symlink():continue
            s=candidate.lstat();key=(s.st_dev,s.st_ino)
            if key not in seen_source_inodes:q.append(candidate);seen_source_inodes.add(key)
        if len(q)!=1:raise ValueError('retained sibling source coverage')
        source=q[0];sb=raw(source);s=p.lstat()
        objects.append({'path':str(p),'logical_bytes':s.st_size,'allocated_bytes':s.st_blocks*512,'identity':before,'retained_source_path':str(source),'retained_source_sha256':hashlib.sha256(sb).hexdigest(),'outside_complete_current_protection':not protected(p),'status':'HOLD_NOT_SELECTED_THIS_ROUND','reason':'Source and original recipe retained; full historical toolchain/dependency/exact rebuild proof not completed, and Root fixed D4A30 scope excludes compiled cache deletion'})
        if identity(p)!=before:raise ValueError('held object changed during observation')
    if len(objects)!=1348 or not all(r['outside_complete_current_protection'] for r in objects):raise ValueError('exact old object coverage/current closure exclusion')
    retained=[]
    for n in ('build_receipt.tsv','source_identity.tsv','instrumented_source_manifest.sha256','symbol_audit.txt','executable.sha256','Dragon.otool','Dragon.nm','toolchain.sha256'):
        p=D/n;x=raw(p);retained.append({'path':str(p),'bytes':len(x),'sha256':hashlib.sha256(x).hexdigest()})
    p=S/'bin/Darwin_arm64/Dragon';x=raw(p);retained.append({'path':str(p),'bytes':len(x),'sha256':hashlib.sha256(x).hexdigest()})
    if any(identity(Path(p['path']))!=p['identity'] for p in pins):raise ValueError('all metadata/source reads stable')
    v={'schema':'SPOT_STORAGE20_FINITE_COMPILED_CACHE_METADATA_HOLD_REVIEW_V1','status':'PASS_READONLY_HOLD_NO_CACHE_OR_METADATA_MUTATION_THIS_ROUND','scope':'COMPILED_CACHE_AND_OLD_AUDIT_JSON_ONLY; ROOT_FIXED_D4A30_DELETE_HANDLED_SEPARATELY',
       'current_protection_scope':{'expected_files':len(b['files']),'canonical':len(g['canonical_files']),'namespaces':len(g['namespaces']),'aliases':len(g['aliases']),'source_pins':len(f['all_fresh_pins']),'explicit_graph_and_binding_kept':True,'four_current_source_work_terminal_controls_roots':current,'inventory_boolean_is_prefilter_only':True},
       'old_audit_metadata_HOLD':meta,'old_audit_metadata_totals':{'files':len(meta),'logical_bytes':sum(r['logical_bytes'] for r in meta),'allocated_bytes':sum(r['allocated_bytes'] for r in meta),'measured_compression_saving':None,'whole_byte_gzip_inverse_test':None},
       'mandatory_current_metadata_KEEP':mandatory,'old_gmres_object_cache_HOLD':objects,'old_gmres_cache_totals':{'files':len(objects),'logical_bytes':sum(r['logical_bytes'] for r in objects),'allocated_bytes':sum(r['allocated_bytes'] for r in objects),'every_source_still_present_and_fresh_fullSHA':True,'current_full_protection_intersections':0,'complete_rebuild_dependency_admission':False},
       'retained_source_recipe_runtime_libraries_modules_reports_logs':'Every original file retained. Only reading occurred. Full old Dragon binary and audit/recipe documents remain; no objects, libraries, modules, executables, metadata or directories removed.',
       'retained_small_metadata_and_binary_pins':retained,'source_and_input_metadata_read_pins':pins,'all_original_candidate_object_identity_window_stable':True,'unexecuted_broad_archive_measurement_source_not_run':str(O/'review_candidates.py'),'project_written':False,'project_deleted':False,'business_or_component_executed':False,'scientific_qualification':False,'cache_deletion_or_compression_admitted':False}
    p=O/'HOLD_REPORT.json'
    with p.open('x') as f:json.dump(v,f,indent=2,ensure_ascii=False,allow_nan=False);f.write('\n')
    x=p.read_bytes();print(json.dumps({'status':v['status'],'report_path':str(p),'report_sha256':hashlib.sha256(x).hexdigest(),'report_bytes':len(x),'old_audit_metadata_totals':v['old_audit_metadata_totals'],'old_gmres_cache_totals':v['old_gmres_cache_totals'],'cache_deletion_or_compression_admitted':False},ensure_ascii=False))

if __name__=='__main__':main()
