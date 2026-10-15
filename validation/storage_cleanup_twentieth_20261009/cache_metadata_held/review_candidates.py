"""Read-only project inventory; TMP-only archive measurement and candidate evidence."""
from pathlib import Path
import collections, gzip, hashlib, json, os, stat

OUT=Path('/private/tmp/spot_storage_twentieth_compiled_and_metadata_review_20261009')
ART=Path('/Users/wen/spot/validation/artifacts')
ROOT=Path('/Users/wen/spot')
G=ART/'axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-v9-20261009/input_graph.json'
B=ART/'axial-material-production-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-last-cprime-trim-file-snapshot-scipy-env-physical-basis-own-pid-peak-v9-20261009/own_rss_binding.json'
F=Path('/private/tmp/spot_v9_actual_finalization_full_source_independent_review_20261009/REPORT.json')
C=Path('/private/tmp/axmat_v9_cold_actual_finalization_postterminal_scope_20261009/finalization_config_ROOT_OBSERVED.json')
INV=Path('/private/tmp/spot_storage_twentieth_root_20261009/inventory.json')
FIELDS=('dev','ino','mode','size','mtime_ns','ctime_ns','nlink')
PINS=[]

def ident(p):
    s=p.lstat();return [getattr(s,'st_'+k) for k in FIELDS]

def raw(p,sha=None):
    p=Path(p);before=ident(p);s=p.lstat()
    if not stat.S_ISREG(s.st_mode) or s.st_nlink!=1:raise ValueError('regular single-link source required '+str(p))
    b=p.read_bytes();h=hashlib.sha256(b).hexdigest()
    if before!=ident(p) or sha is not None and h!=sha:raise ValueError('pin or identity changed '+str(p))
    PINS.append({'path':str(p),'sha256':h,'bytes':len(b),'identity':before});return b

def load(p,sha=None):return json.loads(raw(p,sha))

def main():
    g=load(G,'0e365ebbaafa0d9e9b3a34eee89cc9c3e1de3ee47812d985135b8201bd001be3')
    b=load(B,'4e8de93043fa08ac0c6e1f1702b69606a6bf0b155c30007c356ec4837919c930')
    full=load(F,'ead5085edb5b09ab3a2de65102565bc7493672302c2f4873512b0b3c7594d85e');c=load(C,'8f5936308ad6ee031fc4328423966b9f0db069d27b5c1ce932f41a72d8a87174');inv=load(INV)
    protected=set(b['files'])|{p['path'] for p in g['canonical_files']}|set(g['requirements']['paths'])|{str(G),str(B)}|{p['path'] for p in full['all_fresh_pins']}
    for n in g['namespaces']:
        protected|={str(Path(n['canonical_root'])/p) for p in n['files']}
        protected|={str(Path(n['canonical_root'])/p) for p in n['symlinks']}
    for a in g['aliases']:protected|={a['path'],a['target']}
    held_roots=list(c['roots'].values())
    def held(p):return str(p) in protected or any(str(p)==r or str(p).startswith(r+'/') for r in held_roots)
    selected=[];skipped=[]
    for r in inv['all_large_regular_files']:
        p=Path(r['path'])
        if not str(p).startswith(str(ART)+'/') or p.name not in ('input_graph.json','own_rss_binding.json','complete_input_graph.json','ALL_FILES.jsonl'):continue
        if held(p):skipped.append({'path':str(p),'reason':'CURRENT_COMPLETE_INPUT_SOURCE_OR_NAMESPACE_PROTECTION'});continue
        if ident(p)!=r['identity']:raise ValueError('inventory candidate changed '+str(p))
        selected.append(r)
    archives=[];archive_dir=OUT/'measured_lossless_archives';archive_dir.mkdir(exist_ok=False)
    for i,r in enumerate(selected,1):
        p=Path(r['path']);before=ident(p);raw_hash=hashlib.sha256();n=0
        q=archive_dir/(f'{i:02d}-'+p.parent.name+'-'+p.name+'.gz')
        with p.open('rb') as src,q.open('xb') as dst:
            with gzip.GzipFile(filename='',mode='wb',compresslevel=6,fileobj=dst,mtime=0) as gz:
                while True:
                    chunk=src.read(1024*1024)
                    if not chunk:break
                    raw_hash.update(chunk);n+=len(chunk);gz.write(chunk)
        restored_hash=hashlib.sha256();restored_n=0
        with gzip.open(q,'rb') as src:
            while True:
                chunk=src.read(1024*1024)
                if not chunk:break
                restored_hash.update(chunk);restored_n+=len(chunk)
        if ident(p)!=before or restored_hash.hexdigest()!=raw_hash.hexdigest() or restored_n!=n or n!=r['size_bytes']:raise ValueError('whole original byte inverse failed '+str(p))
        qb=q.read_bytes();s=q.lstat();archives.append({'original_path':str(p),'original_sha256':raw_hash.hexdigest(),'original_bytes':n,'original_allocated_bytes':r['allocated_bytes'],'original_identity':before,'measured_TMP_archive_path':str(q),'archive_sha256':hashlib.sha256(qb).hexdigest(),'archive_bytes':len(qb),'archive_allocated_bytes':s.st_blocks*512,'whole_original_byte_inverse_exact':True,'excluded_from_current37395_canonical35647_requirements_namespaces86_aliases186_current2096_source_and_all4_current_roots':True,'action_candidate':'LOSSLESS_ARCHIVE_ONLY_NO_INFORMATION_DELETION','retained_use_requirement':'Superseded audit only. Old verifiers require restoring the exact original path and bytes, checking original SHA, before use; current V9 graph/binding/docs remain unchanged.'})
    D=ART/'gmres-activity-build';S=D/'source';objects=[];sources=[]
    recipe=raw(D/'build_receipt.tsv').decode();manifest=raw(D/'instrumented_source_manifest.sha256').decode()
    for p in sorted(S.rglob('*.o')):
        if not p.is_file() or p.is_symlink():continue
        if held(p):raise ValueError('gmres object current protected '+str(p))
        sibling=[p.with_suffix(e) for e in ('.f','.f90','.F','.F90','.c','.cpp') if p.with_suffix(e).is_file() and not p.with_suffix(e).is_symlink()]
        if len(sibling)!=1:raise ValueError('one retained same-name source required '+str(p))
        q=sibling[0];source_bytes=raw(q);ob=raw(p);s=p.lstat()
        objects.append({'path':str(p),'sha256':hashlib.sha256(ob).hexdigest(),'bytes':len(ob),'allocated_bytes':s.st_blocks*512,'identity':ident(p),'retained_source_path':str(q),'retained_source_sha256':hashlib.sha256(source_bytes).hexdigest(),'outside_current_complete_protection':True,'candidate_kind':'REBUILDABLE_OBJECT_ONLY'})
    manifest_pins=[]
    for line in manifest.splitlines():
        h,name=line.split(None,1);p=S/name.strip();raw(p,h);manifest_pins.append({'path':str(p),'sha256':h})
    kept=[]
    for name in ('build_receipt.tsv','source_identity.tsv','instrumented_source_manifest.sha256','symbol_audit.txt','executable.sha256','Dragon.otool','Dragon.nm','toolchain.sha256'):
        p=D/name;x=raw(p);kept.append({'path':str(p),'sha256':hashlib.sha256(x).hexdigest(),'bytes':len(x)})
    binary=S/'bin/Darwin_arm64/Dragon';binary_raw=raw(binary);kept.append({'path':str(binary),'sha256':hashlib.sha256(binary_raw).hexdigest(),'bytes':len(binary_raw)})
    for line in recipe.splitlines():
        parts=line.split('\t')
        if len(parts)==2 and parts[0].endswith(('.a','/Dragon')):
            p=S/parts[0];x=raw(p,parts[1]);kept.append({'path':str(p),'sha256':parts[1],'bytes':len(x)})
    if 'status\tPASS' not in recipe or 'build_command\tenv -i LC_ALL=C' not in recipe or len(objects)!=1348:raise ValueError('actual original complete build recipe and all object source coverage')
    if any(ident(Path(p['path']))!=p['identity'] for p in PINS):raise ValueError('all input/source/candidate window identities stable')
    result={'schema':'SPOT_STORAGE20_COMPILED_AND_LOSSLESS_METADATA_CANDIDATE_REVIEW_V1','status':'READONLY_MEASURED_CANDIDATES_ONLY_NO_PROJECT_DELETION','current_protection':{'binding_expected_files':len(b['files']),'canonical_files':len(g['canonical_files']),'graph_namespaces':len(g['namespaces']),'aliases':len(g['aliases']),'full_source_report_pins':len(full['all_fresh_pins']),'current_roots':held_roots,'union_explicit_protected_paths':len(protected),'inventory_protection_is_prefilter_only':True},
      'metadata_archives':archives,'metadata_summary':{'files':len(archives),'original_bytes':sum(r['original_bytes'] for r in archives),'original_allocated_bytes':sum(r['original_allocated_bytes'] for r in archives),'measured_archive_bytes':sum(r['archive_bytes'] for r in archives),'measured_archive_allocated_bytes':sum(r['archive_allocated_bytes'] for r in archives),'measured_possible_allocated_saving_bytes':sum(r['original_allocated_bytes']-r['archive_allocated_bytes'] for r in archives)},'current_metadata_explicitly_kept':skipped,
      'gmres_objects':objects,'gmres_summary':{'candidate_files':len(objects),'candidate_bytes':sum(r['bytes'] for r in objects),'candidate_allocated_bytes':sum(r['allocated_bytes'] for r in objects),'every_object_has_retained_source_with_actual_fullSHA':True,'original_source_manifest_fresh_SHA_entries':len(manifest_pins),'retained_recipe_metadata_and_final_binary_and_libraries':kept,'compiled_libraries_modules_executables_not_selected':True,'old_object_exact_recovery_requires_isolated_original_recipe_build_then_SHA_match':True},
      'source_manifest_fresh_pins':manifest_pins,'all_read_pins':PINS,'project_written':False,'project_deleted':False,'business_executed_or_retried':False,'scientific_qualification':False,'ready_for_Root_and_independent_retention_review_not_automatic_delete_authorization':True}
    p=OUT/'REPORT.json'
    with p.open('x') as f:json.dump(result,f,indent=2,ensure_ascii=False,allow_nan=False);f.write('\n')
    data=p.read_bytes();print(json.dumps({'status':result['status'],'report_path':str(p),'report_sha256':hashlib.sha256(data).hexdigest(),'report_bytes':len(data),'metadata_summary':result['metadata_summary'],'gmres_summary':{k:v for k,v in result['gmres_summary'].items() if k!='retained_recipe_metadata_and_final_binary_and_libraries'},'project_written':False},ensure_ascii=False))

if __name__=='__main__':main()
