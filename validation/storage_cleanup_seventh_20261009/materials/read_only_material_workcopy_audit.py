"""Read-only material staging duplicate audit; writes only this TMP evidence folder."""
from pathlib import Path
import datetime, hashlib, json, os, re, stat, time

ROOT = Path('/Users/wen/spot')
ART = ROOT/'validation/artifacts'
OUT = Path('/private/tmp/spot_storage_seventh_material_workcopy_review_20261009')
INV = Path('/private/tmp/spot_storage_seventh_inventory_20261009')
M = ART/'d4a-actual-temperature-material-run-20261003'
A = ART/'axial-material-inputs-20261003'
L = ART/'d4a-actual-temperature-library-run-20261003'
PROD = Path('/Users/wen/draglib_output/shem370_endfb8r1_v5p1/draglibshem370_endfb8r1_v5p1.xsm')
DLIB_SHA = '66b9a7b3e8534a54cf590db63a7c1dbd96b4a95c636f0e3a6eee5b219bbcc1e9'
BIN_SHA = 'e78b87094b67bd4d1bcdc3a5dd2beeb168318853a48321473bb9b86df5ba19cc'
ASCII_SHA = '44772b86d87e90532f89e786369749b373114f0c0f3d90b282ded6b8432ca1c2'
GRAPH = ART/'axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-v7-20261009/input_graph.json'
GRAPH_SHA = '9103f35a3f121972969270162be56babe72143869b050f5220af6f3eb0715e68'
PROTECT = ROOT/'validation/storage_review_more_20261008/normalized_protection_index.json'
PROTECT_SHA = '30893b4a333c6dc39df420b136b095e076e0ad2ac6255336b8e3eb26ced49b86'
TARGETS = [M/f'material{t}'/'DLIB8R1_370' for t in (650,750,850)] + [A/s/'DLIB8R1_370' for s in ('A','B')] + [L/'merge/28-U238/tape30',L/'import/EXPORT']

def ident(p):
    s=p.lstat()
    return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]

def fresh(p, expected=None):
    pre=ident(p)
    if not stat.S_ISREG(pre[2]): raise ValueError('not a regular file: '+str(p))
    h=hashlib.sha256()
    with p.open('rb') as f:
        if [os.fstat(f.fileno()).st_dev,os.fstat(f.fileno()).st_ino] != pre[:2]: raise ValueError('inode changed')
        for chunk in iter(lambda:f.read(8*1024**2),b''):h.update(chunk)
    post=ident(p)
    if pre != post:raise ValueError('changed while reading: '+str(p))
    got=h.hexdigest()
    if expected is not None and got != expected:raise ValueError('digest mismatch: '+str(p))
    return dict(path=str(p),sha256=got,identity=pre,logical_bytes=pre[3],allocated_bytes=p.stat().st_blocks*512,expected_sha256=expected,stable_regular_read=True)

def write(name,data):
    p=OUT/name
    with p.open('x') as f:json.dump(data,f,ensure_ascii=False,indent=2);f.write('\n')

def load(p):return json.loads(p.read_text())

def seal(p):
    out={}
    for line in p.read_text().splitlines():
        h,n=line.split(maxsplit=1);out[n.lstrip('*')]=h
    return out

started=time.monotonic()
inv_rows={}
for line in (INV/'regular_files.jsonl').open():
    row=json.loads(line)
    if row['path'] in {str(p) for p in TARGETS}:inv_rows[row['path']]=row
if set(inv_rows) != {str(p) for p in TARGETS}:raise ValueError('inventory target missing')

# Decode saved metadata only. No graph verifier, project API or business import runs.
gp=fresh(GRAPH,GRAPH_SHA);g=load(GRAPH)
pp=fresh(PROTECT,PROTECT_SHA);pro=load(PROTECT)
canon={r['path']:r for r in g['canonical_files']};pool=set(g['requirements']['paths'])
deps={}
for p in TARGETS:
    t=str(p)
    ns=[]
    for n in g['namespaces']:
        root=Path(n['canonical_root'])
        if p.is_relative_to(root):
            rel=str(p.relative_to(root));ns.append(dict(root=str(root),relative_path=rel,member=rel in n['files']))
    aliases=[r for r in g['aliases'] if r['path']==t or r['target']==t or (r['kind']=='directory' and p.is_relative_to(r['target']))]
    traces=[r for r in g['read_trace']['records'] if r.get('path')==t or r.get('literal_path')==t]
    deps[t]=dict(canonical_member=t in canon,requirement_path_pool_member=t in pool,
        namespace_ancestor_matches=ns,aliases=aliases,exact_read_trace_matches=traces,
        declared_absence=t in g['absence_inputs'],new_declared_path=t in g['newly_declared_input_paths'],
        live_resource_directory_ancestors=[r for r in g['live_resource_roots'] if p.is_relative_to(r)],
        previous_index_file=t in pro['protected_files'],previous_index_inbound_target=t in pro['inbound_alias_targets'],
        previous_index_directory_ancestors=[r for r in pro['protected_directories'] if p.is_relative_to(r)])
    d=deps[t]
    if d['canonical_member'] or d['requirement_path_pool_member'] or ns or aliases or traces or d['declared_absence'] or d['new_declared_path'] or d['previous_index_file'] or d['previous_index_inbound_target'] or d['previous_index_directory_ancestors']:
        raise ValueError('target has protection dependency: '+t)

# Inventory every currently present project symlink anew (do not follow directories).
links=[]
for parent,dirs,files in os.walk(ROOT,followlinks=False):
    for name in dirs+files:
        p=Path(parent)/name
        if not p.is_symlink():continue
        pre=ident(p);text=os.readlink(p);resolved=str(p.resolve());post=ident(p)
        if pre!=post:raise ValueError('symlink changed')
        links.append(dict(path=str(p),text=text,resolved=resolved,identity=pre))
        if resolved in deps or any(q.is_relative_to(resolved) for q in TARGETS):raise ValueError('inbound symlink protection: '+str(p))
write('fresh_dependency_review.json',dict(schema='SPOT_SEVENTH_MATERIAL_WORKCOPY_DEPENDENCY_REVIEW_V1',
    graph=gp,graph_schema=g['schema'],canonical_count=len(canon),requirements_rows=len(g['requirements']['rows']),
    namespaces=len(g['namespaces']),aliases=len(g['aliases']),read_trace_records=len(g['read_trace']['records']),
    previous_protection_index=pp,targets=deps,fresh_symlink_count=len(links),
    fresh_symlink_inventory_sha256=hashlib.sha256(json.dumps(sorted(links,key=lambda x:x['path']),sort_keys=True,separators=(',',':')).encode()).hexdigest(),
    live_resource_directory_membership_is_not_input_protection=True,project_API_executed=False))
source_paths=(OUT/'project_source_reference_paths.txt').read_text().splitlines()
pat=re.compile(r'required_staging_per_state|axial-material-inputs-20261003|d4a-actual-temperature-material-run-20261003|28-U238/tape30|import/EXPORT')
sources=[]
for name in source_paths:
    p=ROOT/name.removeprefix('./');x=fresh(p);lines=p.read_text().splitlines()
    if ident(p)!=x['identity']:raise ValueError('source changed after read')
    x['current_graph_canonical_member']=str(p) in canon
    x['matched_lines']=[dict(line=i+1,text=s[:1200],truncated=len(s)>1200) for i,s in enumerate(lines) if pat.search(s)]
    x['matches_do_not_establish_file_consumption_without_body_review']=True
    sources.append(x)
write('project_source_reference_sweep.json',dict(schema='SPOT_SEVENTH_SOURCE_REFERENCE_SWEEP_V1',
    extensions=['.py','.sh','.c2m','.x2m'],no_ignore=True,pattern=pat.pattern,files=sources,
    source_executed=False,business_imports=False,limitation='Static references plus saved V7 trace; arbitrary future user-configured paths are not proven impossible.'))
del g,pro,canon,pool

proof=[]
for p in TARGETS+[PROD]:
    expected=DLIB_SHA if p.name=='DLIB8R1_370' or p==PROD else ASCII_SHA
    d=fresh(p,expected)
    if str(p) in inv_rows and d['identity'] != inv_rows[str(p)]['identity']:raise ValueError('inventory identity changed')
    proof.append(d)
    print(json.dumps(dict(checked=p.name,parent=p.parent.name,sha256=d['sha256'],bytes=d['logical_bytes'])),flush=True)
write('fresh_duplicate_byte_proof.json',dict(schema='SPOT_SEVENTH_FULL_FRESH_DUPLICATE_BYTE_PROOF_V1',files=proof,
    five_work_libraries_equal_external_production=True,final_ascii_equals_import_staging_copy=True,
    independent_inodes=len({tuple(r['identity'][:2]) for r in proof})==len(proof),
    file_digest_only_not_native_API_or_physics_qualification=True))

retained=[]
meta=[]
for root in (M,L):
    seals=seal(root/'result.sha256')
    for n in ['result.sha256','inputs.json','staged_inputs.json','output_hashes.json','receipts.json','completed.json']:
        p=root/n;meta.append(fresh(p,seals.get(n)))
    for p in [q for q in TARGETS if q.is_relative_to(root)]:
        h=seals[str(p.relative_to(root))]
        if h!=next(r['sha256'] for r in proof if r['path']==str(p)):raise ValueError('historic target seal differs')
    if root==M:
        for t in (650,750,850):
            for n in ['input_hashes.json','receipt.json','material_check.json','material.log','material.x2m','D4ActualTone.c2m','microlib.ascii','macro.ascii','metadata.ascii','DLIB_ACTUAL']:
                p=root/f'material{t}'/n
                d=fresh(p,seals.get(str(p.relative_to(root))))
                if n=='DLIB_ACTUAL' and d['sha256']!=BIN_SHA:raise ValueError('DLIB_ACTUAL differs')
                retained.append(d)
        meta.append(fresh(root/'material_checks.json',seals.get('material_checks.json')))
    else:
        for n in ['import/DLIB_370_bin','export/DLIB_370_bin','import/input_hashes.json','import/receipt.json','merge/28-U238/input_hashes.json','merge/28-U238/receipt.json','roundtrip_check.json']:
            p=root/n;d=fresh(p,seals.get(n))
            if 'DLIB_370_bin' in n and d['sha256']!=BIN_SHA:raise ValueError('retained binary differs')
            retained.append(d)
for n in ['material_inputs.json','material_results.json','frozen_inputs.json','execution_progress.json','case_spec.json','production_declaration.json','production_declaration_v2.json','production_declaration_rank1.json']:
    meta.append(fresh(A/n))
frozen=load(A/'frozen_inputs.json')['files'];results=load(A/'material_results.json')
if results['inputs_manifest_sha256']!=next(r['sha256'] for r in meta if r['path']==str(A/'material_inputs.json')):raise ValueError('A/B manifest binding differs')
for s in ('A','B'):
    if frozen[s+'/DLIB8R1_370']!=DLIB_SHA:raise ValueError('frozen library input differs')
    for n in ['DLIB_ACTUAL','material.xsm','material.log','material.x2m','microlib.ascii','macro.ascii','metadata.ascii','material_audit.json','material_native.json','material_claim.json','snapshot_'+s+'.xsm','snapshot.log','snapshot_native.json','snapshot_claim.json']:
        p=A/s/n
        expected=frozen.get(s+'/'+n)
        if n=='DLIB_ACTUAL':expected=BIN_SHA
        if n=='material_audit.json':expected=results['states'][s]['material_audit_sha256']
        if n=='snapshot_'+s+'.xsm':expected=results['states'][s]['archive_sha256']
        if n=='snapshot.log':expected=results['states'][s]['snapshot_log_sha256']
        retained.append(fresh(p,expected))
write('retained_material_results_and_original_documents.json',dict(schema='SPOT_SEVENTH_RETAINED_MATERIAL_RESULT_DOCUMENT_PROOF_V1',
    retained_material_and_library_results=retained,original_result_documents=meta,
    old_frozen_input_SHA_records_preserved=True,original_seals_unmodified=True,
    no_new_science_or_current_API_success=True))

# Final time-of-audit consistency check on every evidence file already read.
for r in proof+retained+meta+sources+[gp,pp]:
    if ident(Path(r['path'])) != r['identity']:raise ValueError('changed before audit completed: '+r['path'])
write('read_only_completion.json',dict(status='READ_ONLY_DUPLICATE_EVIDENCE_COMPLETE_PENDING_ROOT_REVIEW',
    timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-started,
    target_files_checked=len(TARGETS),retained_results_checked=len(retained),original_document_files_checked=len(meta),
    full_fresh_hashes=len(proof)+len(retained)+len(meta),source_reference_files_checked=len(sources),
    files_deleted=0,formal_files_written=0,business_imports=0,project_API_executions=0,native_executions=0,
    retry_or_PREP_or_RUN_executions=0,original_codec_candidate_modified=False,
    recommendation_generated_by_source_review_separately=True))
print(json.dumps(dict(status='READ_ONLY_DUPLICATE_EVIDENCE_COMPLETE',files_deleted=0,full_hash_files=len(proof)+len(retained)+len(meta),elapsed_seconds=time.monotonic()-started)),flush=True)
