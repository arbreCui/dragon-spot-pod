"""Independent read-only T11 fixed-manifest/source/preflight audit; no cleanup/restore/business execution."""
import ast,collections,hashlib,json,os,re,stat,time
from pathlib import Path
ROOT=Path('/Users/wen/spot');ART=ROOT/'validation/artifacts';R=ROOT/'validation/storage_cleanup_eleventh_20261009'
OUT=Path('/private/tmp/spot_storage_eleventh_full_preapply_independent_review_20261009')
M_SHA='5a2462cb67b387543e98607911d16100d0cf67ab347c0a555195b1390db7f853';PF_SHA='35d3fc027c4d26a3de0e68859844047d106c872166cf9a1e8a240e72f20fc870'
SOURCE_SHA='8ee7ea6dd3b7162ce06f687167fcc035c0804ba9f0b9bf72444abb7ca32c2e8b';DOC_SHA='cc44e60f886f2f15eaa6e33b96d05c18a542b53ab58fdcccb3c818834574c420';TERMINAL_SHA='b4cd9ef027df1c6204a6f5b9fb73452445da5fbe13f85e0cff148d91e3305474'
PINS={};START=time.monotonic()
def identity(p):
    s=p.lstat()
    return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]

def fullpin(p,expected=None):
    p=Path(p);before=identity(p)
    assert p.is_absolute() and '..' not in p.parts and p.parent.resolve(strict=True)==p.parent and stat.S_ISREG(before[2])
    if isinstance(expected,dict):
        assert before==expected['identity'] and before[3]==expected['size'],str(p)
    h=hashlib.sha256();length=0
    with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb') as f:
        s=os.fstat(f.fileno());assert [s.st_dev,s.st_ino]==before[:2]
        while block:=f.read(1024**2):h.update(block);length+=len(block)
    assert identity(p)==before and length==before[3]
    digest=h.hexdigest()
    if expected is not None:assert digest==(expected['sha256'] if isinstance(expected,dict) else expected),(str(p),digest)
    record=dict(path=str(p),identity=before,size=length,sha256=digest)
    if str(p) in PINS:assert PINS[str(p)]==record,str(p)
    PINS[str(p)]=record
    return record

def load(p,expected=None):
    record=fullpin(p,expected);data=Path(p).read_bytes();assert hashlib.sha256(data).hexdigest()==record['sha256'] and identity(Path(p))==record['identity']
    return json.loads(data)

def save(name,value):
    with (OUT/name).open('xb') as f:
        f.write((json.dumps(value,sort_keys=True,indent=2,allow_nan=False)+'\n').encode());f.flush();os.fsync(f.fileno())

def allstrings(value):
    if type(value) is dict:
        for k,v in value.items():
            if type(k)is str:yield k
            yield from allstrings(v)
    elif type(value)is list:
        for v in value:yield from allstrings(v)
    elif type(value)is str:yield value

def snapshot():
    files={};links={};dirs=[]
    for current,sub,names in os.walk(ROOT,followlinks=False):
        base=Path(current)
        if base==ROOT:sub[:]=[s for s in sub if s!='.git']
        sub[:]=[s for s in sub if base/s!=R]
        dirs.append(str(base.relative_to(ROOT)))
        for name in sub+names:
            p=base/name;s=p.lstat();rel=str(p.relative_to(ROOT))
            ident=[s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
            if stat.S_ISLNK(s.st_mode):links[rel]=[ident,os.readlink(p)]
            elif stat.S_ISREG(s.st_mode):files[rel]=ident
    result={'files':files,'links':links,'dirs':sorted(dirs)}
    return result,hashlib.sha256(json.dumps(result,sort_keys=True,separators=(',',':')).encode()).hexdigest()


m=load(R/'manifest.json',M_SHA);pre=load(R/'preflight.json',PF_SHA);terminal=load(R/'preflight_terminal_observation.json',TERMINAL_SHA)
assert type(terminal['exit_code']) is int and terminal['exit_code']==0 and terminal['closed'] is True and terminal['actual_deletion_completed'] is False and terminal['solver_or_API_executed'] is False
assert terminal['initial_chunk_id']=='3cf8b4' and terminal['session_id']==84533 and terminal['terminal_chunk_id']=='55000b'
assert terminal['manifest_sha256']==M_SHA and terminal['preflight_sha256']==PF_SHA
for name,key in (('preflight.stdout','stdout_sha256'),('preflight.stderr','stderr_sha256')):fullpin(R/name,terminal[key])
assert json.loads((R/'preflight.stdout').read_text())==pre and (R/'preflight.stderr').stat().st_size==0
assert pre['status']=='PASS_FIXED_FULL_SHA_PREFLIGHT' and pre['executed'] is False and pre['manifest_sha256']==M_SHA
assert type(m['exact_count']) is int and m['exact_count']==pre['candidates']==len(m['candidates'])==15
assert m['cleanup_source_sha256']==SOURCE_SHA and m['result_document_baseline_sha256']==DOC_SHA and m['scientific_credit'] is False
assert m['current_default_iterative_seed_explicitly_preserved'] is True and m['four_differing_SHA_large_bootstrap_files_explicitly_preserved'] is True
assert not (R/'retirement_ledger.jsonl').exists() and not (R/'cleanup_result.json').exists()
source=fullpin(R/'cleanup_fixed_duplicates.py',SOURCE_SHA);source_text=(R/'cleanup_fixed_duplicates.py').read_text();old=(ROOT/'validation/storage_cleanup_tenth_20261009/cleanup_fixed_duplicates.py').read_text()
assert old.replace('validation/storage_cleanup_tenth_20261009','validation/storage_cleanup_eleventh_20261009').replace("p.suffix not in {'.xsm'}","p.suffix not in {'.xsm', '.npz', '.bin'}")==source_text
st=ast.parse(source_text);compile(st,str(R/'cleanup_fixed_duplicates.py'),'exec');unlinks=[n.lineno for n in ast.walk(st) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='unlink'];assert unlinks==[122]
assert not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr in ('rmdir','rmtree') for n in ast.walk(st))
restore=fullpin(R/'restore_retired_work_copies.py','53a51f0f70c5194b13328d01b356d33260cd1b310753fda743b8ad6af6a687bd');assert (R/'restore_retired_work_copies.py').read_bytes()==(ROOT/'validation/storage_cleanup_tenth_20261009/restore_retired_work_copies.py').read_bytes()
assert "if not args.restore_all and not args.path:" in (R/'restore_retired_work_copies.py').read_text()
rows=m['candidates'];selected={x['path'] for x in rows};primaries={x['path']:x for x in m['retained_primaries']};assert len(selected)==15 and len(primaries)==len(m['retained_primaries'])==17 and not selected.intersection(primaries)
assert len({tuple(x['identity'][:2]) for x in rows})==15 and collections.Counter(x['work_copy_class'] for x in rows)=={'OLD_NATIVE_REPLAY_GREEN_INPUT':9,'OLD_COARSE_BOOTSTRAP_WORK_COPY':6}
assert collections.Counter(Path(x['path']).suffix for x in rows)=={'.npz':9,'.xsm':5,'.bin':1}
assert sum(x['size'] for x in rows)==m['logical_bytes']==843222425 and sum(x['allocated_bytes'] for x in rows)==m['allocated_bytes']==843251712
assert len(m['source_and_review_pins'])==4164 and len({x['path'] for x in m['source_and_review_pins']})==4164
before,digest=snapshot();assert digest==pre['untouched_snapshot_sha256']=='605d019f617ffdb3208a346962aaefbb68a722c6fc558ffefe9ff99cae661d1b';save('independent_before_project_snapshot.json',before)
print(json.dumps(dict(phase='snapshot_matches_actual_Root_preflight',files=len(before['files']),links=len(before['links']),dirs=len(before['dirs']))),flush=True)
green=load(R/'green_candidate_review/fixed_exact9_recommendations.json');coarse=load(R/'coarse_candidate_review/REPORT_six_exact_candidates.json');scope=load(R/'green_candidate_review/protection_and_current_intake_scope.json')
assert len(green)==9 and len(coarse['candidate_restore_mapping'])==6 and coarse['approved_apply'] is False
G={x['path']:x for x in green};C={x['candidate']['path']:x for x in coarse['candidate_restore_mapping']};assert set(G)|set(C)==selected and not set(G)&set(C)
for row in rows:
 assert row['category']=='EXACT_DUPLICATE_OLD_WORK_COPY' and row['identity'][6]==1 and Path(row['path']).is_relative_to(ART)
 if row['path'] in G:
  z=G[row['path']]
  for k in ('path','size','sha256','identity'):assert row[k]==z[k],(row['path'],k)
  assert row['retained_primary']==z['primary']['path'] and row['original_manifest_edges']==z['original_manifest_edges']
  assert z['current_canonical_namespace_alias_allstring_cold_critical_prior_restore_and_symlink_intersections']==[]
  assert row['static_current_dependency_intersections']==[]
 else:
  z=C[row['path']]
  for k in ('path','size','sha256','identity'):assert row[k]==z['candidate'][k],(row['path'],k)
  assert row['retained_primary']==z['retained_primary']['path']
 p=Path(row['path']);fullpin(p,row);assert p.lstat().st_blocks*512==row['allocated_bytes'];primary=primaries[row['retained_primary']]
 assert (row['size'],row['sha256'])==(primary['size'],primary['sha256']) and row['identity'][:2]!=primary['identity'][:2]
for x in m['retained_primaries']:fullpin(x['path'],x)
for i,x in enumerate(m['source_and_review_pins'],1):
 fullpin(x['path'],x)
 if i%1500==0:print(json.dumps(dict(phase='source_and_review_full_SHA',count=i,total=4164)),flush=True)
print(json.dumps(dict(phase='all15_candidate17_primary4164_sourcepins_verified',fresh_files=len(PINS))),flush=True)
exact=set();prefixes=set()
def protect(p):
 if type(p)is str and p.startswith('/') and '\n' not in p:
  exact.add(p)
  if '#' in p:exact.add(p.split('#',1)[0])
def prefix(p):
 if type(p)is str and p.startswith('/'):prefixes.add(p.rstrip('/'))
graph=load(scope['graph']['path'],scope['graph']);oldindex=load(scope['old_index']['path'],scope['old_index']);m9=load(ROOT/'validation/storage_cleanup_ninth_20261009/manifest.json');m8=load(ROOT/'validation/storage_cleanup_eighth_20261009/manifest.json')
for p in oldindex['protected_files']+oldindex['inbound_alias_targets']:protect(p)
for p in oldindex['protected_directories']:prefix(p)
for x in graph['canonical_files']:protect(x['path'])
for x in graph['namespaces']:prefix(x['canonical_root'])
for x in graph['aliases']:
 if x['kind']=='directory':prefix(x['path']);prefix(x['target'])
 else:protect(x['path']);protect(x['target'])
for s in allstrings(graph):protect(s)
for p in m9['critical_roots']:prefix(p)
for p in m9['current_cold_extra_protected_files']:protect(p)
for k in ('retained_primaries','source_and_review_pins'):
 for x in m9[k]:protect(x['path'])
resource_roots=graph['live_resource_roots'];assert len(resource_roots)==228
for p in resource_roots:assert Path(p).exists();prefix(p)
counts=dict(canonical=len(graph['canonical_files']),namespaces=len(graph['namespaces']),aliases=len(graph['aliases']),resource_roots=len(resource_roots));assert counts==dict(canonical=35647,namespaces=86,aliases=186,resource_roots=228)
del graph
restore_sources=load(ROOT/'validation/storage_cleanup_ninth_20261009/reviews/prior_restore_cross_176/all_9124_existing_old_restoration_sources_fresh_stat_canonical_paths.json');assert len(restore_sources)==9124
for x in restore_sources:protect(x['path'])
for s in allstrings(load(coarse['screen']['current_cold1534_pin']['path'],coarse['screen']['current_cold1534_pin'])):protect(s)
prior=[p for p in sorted((ROOT/'validation').glob('storage_cleanup*/manifest.json')) if p.parent!=R]+[ROOT/'validation/storage_review_20261008/first_batch_24_files.json',ROOT/'validation/storage_review_20261008/second_batch_replay_arrays.json',ROOT/'validation/storage_review_more_20261008/exact_retirement_manifest.json']
prior_retired=set()
for p in prior:
 pm=load(p)
 if type(pm)is dict:
  for k,v in pm.items():
   if any(t in k.lower() for t in ('retained','source_pins','source_and_review_pins','source_metadata_pins')):
    for s in allstrings(v):protect(s)
  for k in ('candidates','files','retired_files'):
   if type(pm.get(k))is list:
    for x in pm[k]:
     if type(x)is dict:
      q=x.get('path') or x.get('candidate')
      if type(q)is str:prior_retired.add(q if q.startswith('/') else str(ROOT/q))
 elif type(pm)is list:
  for x in pm:
   if type(x)is dict and type(x.get('path'))is str:prior_retired.add(x['path'])
assert not selected&prior_retired
prefix(str(ROOT/'validation/storage_cleanup_ninth_20261009/packed_material_intermediates'))
links=[]
for rel,[ident,text] in before['links'].items():
 p=ROOT/rel;target=p.resolve(strict=False);links.append(dict(path=str(p),target=str(target),identity=ident,text=text))
 if p.is_dir():prefix(str(p));prefix(str(target))
 else:protect(str(p));protect(str(target))
for p in selected:
 assert p not in exact,(p,'direct protected')
 assert not any(p==d or p.startswith(d+'/') for d in prefixes),(p,'protected directory')
 assert not any(p==x['target'] or p.startswith(x['target']+'/') for x in links),(p,'symbolic inbound')
holds=coarse['bootstrap_four_holds']['rows'];assert len(holds)==6 and len({x['sha256'] for x in holds})==6
for x in holds:assert x['path'] not in selected and identity(Path(x['path']))==x['identity']
assert holds[0]['sha256']!=holds[2]['sha256'] and holds[1]['sha256']!=holds[3]['sha256']
seed_path=ART/'iterative-seed/initial_axial_macrolib.xsm';seed=dict(path=str(seed_path),identity=identity(seed_path),full_SHA_not_repeated_outside_fixed_review_scope=True);assert seed['path'] not in selected
edge_records=[]
for row in rows:
 if row['path'] in G:
  candidates=0;primary=0
  for e in row['original_manifest_edges']:
   ep=Path(e['path']);fullpin(ep,e['manifest_sha256']);line=ep.read_text().splitlines()[e['line']-1];z=re.fullmatch(r'([0-9a-f]{64})\s+\*?(.+)',line);assert z and z.group(1)==e['sha256']==row['sha256'] and z.group(2)==e['original_path']
   bound=os.path.normpath(str(Path(z.group(2)) if Path(z.group(2)).is_absolute() else ep.parent/z.group(2)))
   assert bound in selected or bound in primaries;edge_records.append(dict(candidate=row['path'],manifest=str(ep),resolved_original_path=bound,line=e['line'],sha256=z.group(1)))
   candidates+=bound==row['path'];primary+=bound==row['retained_primary']
  assert candidates>0 and primary>0
 else:
  ep=Path(row['original_candidate_manifest']);fullpin(ep);hits=[]
  for number,line in enumerate(ep.read_text().splitlines(),1):
   z=re.fullmatch(r'([0-9a-f]{64})\s+\*?(.+)',line)
   if not z:continue
   bound=os.path.normpath(str(Path(z.group(2)) if Path(z.group(2)).is_absolute() else ep.parent/z.group(2)))
   if bound==row['path']:assert z.group(1)==row['sha256'];hits.append(dict(candidate=row['path'],manifest=str(ep),resolved_original_path=bound,line=number,sha256=z.group(1)))
  assert hits,(row['path'],'missing original candidate path SHA entry');edge_records.extend(hits)
docs=load(R/'result_document_full_sha_baseline.json',DOC_SHA);assert len(docs['rows'])==pre['result_documents_full_sha_checked']==32585 and len({x['path'] for x in docs['rows']})==32585
assert sum(x['size'] for x in docs['rows'])==docs['bytes']==pre['result_document_bytes']==3797135364
for i,x in enumerate(docs['rows'],1):
 p=ROOT/x['path'];assert p.is_relative_to(ROOT) and str(p) not in selected;fullpin(p,x)
 if i%8000==0:print(json.dumps(dict(phase='complete_result_doc_full_SHA',checked=i,total=32585)),flush=True)
restore_terminal=load(R/'restore_default_listing_tool_observation.json','0cb236b70a2dc795cb0541cd3f8090c078920b9b6b0681ae80c9b7d0393fcd9e');assert type(restore_terminal['exit_code']) is int and restore_terminal['exit_code']==0 and restore_terminal['closed'] is True and restore_terminal['actual_chunk_id']=='2908e4' and restore_terminal['listed_paths']==15 and restore_terminal['restored'] is False
listing=load(R/'restore_default_listing.stdout',restore_terminal['stdout_sha256']);assert listing['restored'] is False and listing['copies']==[dict(path=x['path'],retained_primary=x['retained_primary']) for x in rows] and (R/'restore_default_listing.stderr').stat().st_size==0
fullpin(R/'restore_default_listing.stderr',restore_terminal['stderr_sha256'])
after,after_digest=snapshot();assert before==after and digest==after_digest==pre['untouched_snapshot_sha256']
for p,r in list(PINS.items()):assert identity(Path(p))==r['identity'],p
for x in rows:fullpin(x['path'],x)
assert fullpin(R/'manifest.json',M_SHA)['sha256']==M_SHA and fullpin(R/'preflight.json',PF_SHA)['sha256']==PF_SHA
assert not (R/'retirement_ledger.jsonl').exists() and not (R/'cleanup_result.json').exists()
report=dict(status='PASS_FINAL15_FIXED_MANIFEST_SOURCE_AND_ACTUAL_ROOT_PREFLIGHT_INDEPENDENT_REVIEW',schema='SPOT_ELEVENTH_INDEPENDENT_PREAPPLY_V1',manifest_sha256=M_SHA,cleanup_source_sha256=SOURCE_SHA,preflight_sha256=PF_SHA,Root_actual_preflight_terminal_sha256=TERMINAL_SHA,Root_actual_preflight=terminal,exact_candidates=15,green9=9,coarse6=6,retained_primaries=17,source_pins=4164,result_documents=32585,result_document_bytes=3797135364,allocated_bytes=843251712,logical_bytes=843222425,allocated_GiB=843251712/1024**3,all_candidates_primaries_source_and_result_documents_full_SHA_verified=True,all_pairs_distinct_inode_and_candidates_singlelink=True,all15_original_candidate_and_green_primary_manifest_edges_resolved=True,original_path_bound_edges=edge_records,source_two_region_T10_inverse_preserved=True,restore_source_sha256=restore['sha256'],restore_default_mapping_matches_all15=True,restore_default_actual_tool_receipt=restore_terminal,six_distinct_bootstrap_HOLD_paths_retained_fresh_identity_and_prior_review_SHA=True,default_iterative_seed_retained=seed,protection=dict(graph=counts,old_index=True,cold6248=len(m9['current_cold_extra_protected_files']),critical_roots_from_m9=len(m9['critical_roots']),prior_restore9124=len(restore_sources),prior_manifest_scopes=len(prior),exact_paths=len(exact),prefixes=len(prefixes),symlinks=len(links),intersection_empty=True,all228_dynamic_roots_still_present=True),whole_project_snapshot=dict(before=digest,after=after_digest,files=len(before['files']),links=len(before['links']),dirs=len(before['dirs']),all_regular_identity_and_links_and_dirs_equal=True,excludes=['.git','this round report directory']),unique_full_SHA_paths=len(PINS),unique_full_SHA_bytes=sum(x['size'] for x in PINS.values()),fresh_pin_records='independent_full_SHA_records.json',elapsed_seconds=time.monotonic()-START,actual_apply_tool=None,files_deleted=0,reviewer_ART_or_formal_writes=False,business_API_constructor_PREP_RUN_solver=False,scientific_credit=False,scope='Only exact manifest5a2462/source8ee7 and unchanged actual Root preflight baseline qualify; no actual deletion result yet.',limits=['Whole original manifest/replay/readers require restoring these retired15 exact paths from retained primaries before old replay; prior removals use prior recipes; no old inode/ctime is reconstructed.','Not all old generic artifact readers are absent; the retained primary bytes and restore mapping satisfy historical retirement boundary.','No final native/A_B material/current complete INPUT/cold namespace/unique science payload or differing bootstrap selected.','No scientific API, business phase, numerical reconstruction or actual cleanup/restore was executed.','The byte and identity baseline must still match at Root apply; any manifest/source/preflight or unrelated change requires fresh review.'])
save('independent_full_SHA_records.json',list(PINS.values()));save('independent_preapply_review.json',report)
print(json.dumps(dict(status='PASS',report=str(OUT/'independent_preapply_review.json'),sha256=hashlib.sha256((OUT/'independent_preapply_review.json').read_bytes()).hexdigest(),fresh_paths=len(PINS),fresh_bytes=report['unique_full_SHA_bytes'],snapshot=digest,files_deleted=0)),flush=True)
