"""Independent storage review: reads only project data, writes this TMP directory only."""
from pathlib import Path
import collections,hashlib,json,os,re,stat,time
ROOT=Path('/Users/wen/spot');ART=ROOT/'validation/artifacts'
OUT=Path('/private/tmp/spot_eighth_old_work_inputs_readonly_review_20261009')
SCAN=Path('/private/tmp/spot_eighth_storage_readonly_scan_20261009')
PINS={'exact_content_groups.json':'e88304048fb5c9c38b72a641891881a9ae352bfe41c6e91d00b6a8ddd2ddd564','track_and_initial_duplicates.json':'c80b6874a438dfc8c35b184ff3a34d0d6e74634539bddeab48eb2bf2847ce85e'}
EVIDENCE={};FRESH={};TEXT={};START=time.monotonic()
def require(v,m):
 if not v:raise ValueError(m)
def identity(p):
 s=Path(p).lstat();return[s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
def pin(p,expected=None,retain=False):
 p=Path(p);key=str(p)
 if key in FRESH:
  r=FRESH[key];require(expected is None or r['sha256']==expected,'cached expected mismatch')
  return r,TEXT.get(key)
 before=identity(p);require(stat.S_ISREG(before[2]),'not regular '+key);h=hashlib.sha256();parts=[]
 with p.open('rb')as f:
  fs=os.fstat(f.fileno());require([fs.st_dev,fs.st_ino]==before[:2],'opened different inode')
  while True:
   b=f.read(8*1024**2)
   if not b:break
   h.update(b)
   if retain:parts.append(b)
 require(identity(p)==before,'changed during read '+key)
 r={'path':key,'identity':before,'sha256':h.hexdigest(),'size':before[3],'allocated_bytes':p.lstat().st_blocks*512,'stable_full_content_read':True}
 require(expected is None or r['sha256']==expected,'SHA mismatch '+key);FRESH[key]=r
 if retain:TEXT[key]=b''.join(parts)
 return r,TEXT.get(key)
def doc(p):
 p=Path(p);r,b=pin(p,retain=True);EVIDENCE[str(p)]=r;return b.decode('utf-8')
def strict_load(b):
 def pairs(items):
  d={}
  for k,v in items:require(k not in d,'duplicate JSON key');d[k]=v
  return d
 return json.loads(b,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in()).throw(ValueError('nonfinite JSON')))
def save(n,d):(OUT/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def canonical_declared(base,value):
 s=value.lstrip('*')
 if s.startswith('/'):p=Path(s)
 elif s.startswith('validation/'):p=ROOT/s
 else:p=base/s
 return os.path.normpath(str(p))
def seals(p,digest):
 """Exact path and digest entries, not loose basename/SHA co-occurrence."""
 p=Path(p);family=ART/p.relative_to(ART).parts[0];matches=[]
 dirs={p.parent,family}
 for d in sorted({x for y in dirs for x in y.glob('*.sha256')}):
  for ln,line in enumerate(doc(d).splitlines(),1):
   m=re.fullmatch(r'([a-f0-9]{64})\s+(.+)',line)
   if m and m[1]==digest and canonical_declared(d.parent,m[2])==str(p):
    matches.append({'manifest':str(d),'manifest_sha256':EVIDENCE[str(d)]['sha256'],'line':ln,'entry_sha256':m[1],'declared_path':m[2],'canonical_declared_path':str(p),'kind':'EXACT_SHA256_MANIFEST_ENTRY'})
 return matches

grouppin,groupraw=pin(SCAN/'exact_content_groups.json',PINS['exact_content_groups.json'],True)
shortpin,shortraw=pin(SCAN/'track_and_initial_duplicates.json',PINS['track_and_initial_duplicates.json'],True)
full=strict_load(groupraw);groups=strict_load(shortraw)
require(full['files_deleted']==0 and full['solver_or_API_executed']is False and full['full_read_files']==583,'unexpected Root scan scope')
M=ROOT/'validation/storage_cleanup_seventh_20261009/manifest.json'
mraw=doc(M);m=strict_load(mraw);require(len(m['critical_roots'])==88,'critical roots count')
gr,gb=pin(m['graph_pin']['path'],m['graph_pin']['sha256'],True)
ir,ib=pin(m['old_index_pin']['path'],m['old_index_pin']['sha256'],True)
require(gr['sha256']=='9103f35a3f121972969270162be56babe72143869b050f5220af6f3eb0715e68','not current frozen V7 graph')
graph,index=strict_load(gb),strict_load(ib);absolute=set()
def absolute_walk(v):
 if isinstance(v,dict):
  for k,x in v.items():absolute_walk(k);absolute_walk(x)
 elif isinstance(v,list):
  for x in v:absolute_walk(x)
 elif isinstance(v,str)and v.startswith('/'):absolute.add(v)
absolute_walk(graph)
protectfiles=absolute|set(index['protected_files'])|set(index['inbound_alias_targets'])
protectdirs=set(x['canonical_root']for x in graph['namespaces'])|{x['target']for x in graph['aliases']if x['kind']in('dir','directory')}|set(index['protected_directories'])|set(m['critical_roots'])
def protected(p):
 return str(p)in protectfiles or any(str(p)==d or str(p).startswith(d+'/')for d in protectdirs)
links=[]
for dp,dn,fn in os.walk(ROOT,followlinks=False):
 for n in dn+fn:
  p=Path(dp)/n
  if p.is_symlink():
   before=identity(p);text=os.readlink(p);target=p.resolve(strict=False);require(identity(p)==before,'link changed')
   links.append([str(p),text,str(target)])
links=sorted(links);linksha=hashlib.sha256(json.dumps(links).encode()).hexdigest();require(len(links)==687,'all-project link count changed')
screen=[]
for gi,g in enumerate(groups):
 for r in g['rows']:
  p=Path(r['path']);same=identity(p)==r['identity'];protect=protected(p);inbound=[x for x in links if str(p)==x[2]or str(p).startswith(x[2]+'/')]
  require(protect==r['protected'],'scan protection mismatch '+str(p))
  screen.append({'path':str(p),'group_index':gi,'sha256':g['sha256'],'size':g['size'],'identity_matches_Root_full_read':same,'protected':protect,'inbound_links':inbound,'role_screen':'KEEP_AXIAL_MATERIAL_SCOPE_OTHER_REVIEWER'if r['family'].startswith('axial-material-')else'IN_SCOPE_READONLY_SCREEN'})
# Explicit proposed work copies. Keep main input and scientific-output roots.
selection=[]
for gi,g in enumerate(groups):
 for r in g['rows']:
  p=Path(r['path']);rel=p.relative_to(ART);family=r['family'];name=p.name
  if protected(p)or any(str(p)==x[2]or str(p).startswith(x[2]+'/')for x in links):continue
  choose=(gi==5 and '/replay/'in str(p))
  if choose:selection.append((gi,g,r))
PRIMARY_BY_GROUP={0:ART/'r2-leak64-clean-replay/initial_axial_macrolib.xsm',1:ART/'d4a-corrected-closed0-runtime-release-20260920/initial_radial_track.bin',2:ART/'d4a-corrected-material-three-snapshots-detached-20260904/initial_axial_macrolib.xsm',3:ART/'iterative-d4a-rank2-picard-map1/initial_axial_macrolib.xsm'}
candidates=[];rejected=[];primaryrecords={};jsonproofs=[];source_paths=set()
for gi,g,r in selection:
 p=Path(r['path']);family=ART/r['family'];primary=PRIMARY_BY_GROUP.get(gi,Path(str(p).replace('/replay/','/',1)))
 require(primary!=p,'self primary');require(p.parent.resolve()==p.parent and primary.parent.resolve()==primary.parent,'symlink ancestor')
 require(identity(p)==r['identity']and r['identity'][-1]==1,'candidate identity changed or linked')
 cp,_=pin(p,g['sha256']);pp,_=pin(primary,g['sha256']);primaryrecords[str(primary)]=pp
 candidate_seals=seals(p,g['sha256']);primary_seals=seals(primary,g['sha256'])
 # A source-side original result or prepared seal must bind the primary too.
 require(primary_seals,'retained primary has no exact original SHA manifest '+str(primary))
 qualifying=[x for x in candidate_seals if Path(x['manifest']).name in {'result.sha256','prepared_inputs.sha256'}]
 if not qualifying:
  rejected.append({'path':str(p),'reason':'No exact candidate result/prepared SHA256 entry; keep','available_candidate_seals':candidate_seals});continue
 metadata=[];original_sources=[]
 for d in sorted(set(family.glob('*.json'))|set(p.parent.glob('*.json'))):
  if d.stat().st_size>8*1024**2:continue
  s=doc(d)
  try:v=strict_load(s)
  except(ValueError,UnicodeError):continue
  def visit(obj,trail):
   if isinstance(obj,dict):
    # Plain path -> SHA tables, source/destination use recorded path as declared.
    for k,x in obj.items():
     if isinstance(x,str)and x==g['sha256']and isinstance(k,str):
      declared=canonical_declared(d.parent,k)
      if declared in {str(p),str(primary)}:
       metadata.append({'document':str(d),'document_sha256':EVIDENCE[str(d)]['sha256'],'json_pointer':trail+'/'+k,'declared_path':k,'canonical_declared_path':declared,'sha256':x})
     visit(x,trail+'/'+str(k))
    if obj.get('sha256')==g['sha256']and isinstance(obj.get('source'),str)and obj['source'].startswith('/'):
     original_sources.append({'document':str(d),'document_sha256':EVIDENCE[str(d)]['sha256'],'json_pointer':trail,'source':obj['source'],'sha256':obj['sha256']})
   elif isinstance(obj,list):
    for k,x in enumerate(obj):visit(x,trail+'/'+str(k))
  visit(v,'')
 provenance=p.parent/'symlink_provenance.tsv'
 if provenance.exists():
  for lineno,line in enumerate(doc(provenance).splitlines(),1):
   cols=line.split('\t')
   if len(cols)==3 and cols[0]==p.name and cols[2].startswith('/'):
    original_sources.append({'document':str(provenance),'document_sha256':EVIDENCE[str(provenance)]['sha256'],'line':lineno,'source':cols[2],'sha256':g['sha256'],'role':'saved resolved source for detached copy'})
 for x in original_sources:
  op=Path(x['source'])
  if op.exists()and op.is_file()and not op.is_symlink():
   oprecord,_=pin(op,g['sha256']);primaryrecords[str(op)]=oprecord;x['fresh_retained_source_pin']=oprecord
  else:x['fresh_retained_source_pin']=None;x['source_missing_or_link_retained_primary_is_exact_alternative']=True
 # Local producer/deck/verifier source evidence, all retained untouched.
 local=[]
 for d in sorted(set(family.glob('*.py'))|set(family.glob('*.sh'))|set(p.parent.glob('*.py'))|set(p.parent.glob('*.x2m'))):
  if d.stat().st_size>1024**2:continue
  s=doc(d);hits=[{'line':n,'text':line}for n,line in enumerate(s.splitlines(),1)if p.name in line or ('copy' in line and (gi in(1,2,3)or'/replay/'in str(p)))or ('replay'in line and gi>=5)]
  if hits:local.append({'path':str(d),'sha256':EVIDENCE[str(d)]['sha256'],'matching_lines':hits});source_paths.add(str(d))
 candidates.append(dict(cp,category='EXACT_OLD_REPLAY_INPUT_COPY'if gi>=5 else'EXACT_OLD_TRACK_OR_INITIAL_MACRO_WORK_COPY',group_index=gi,restoration_primary=pp,candidate_original_seal_entries=candidate_seals,primary_original_seal_entries=primary_seals,metadata_exact_bindings=metadata,producer_or_lineage_original_sources=original_sources,retained_producer_or_readonly_input_source=local,original_mode=stat.S_IMODE(cp['identity'][2]),original_mtime_ns=cp['identity'][4],
  historical_verification_limitation='Original result/input manifests and verification programs remain unchanged; any full original seal verification, copied-input audit, or historical replay that names this retired path needs exact restoration first. SHA equality is restoration evidence, not path-presence equivalence.',
  restore_policy='Only from this retained pinned project primary to this enumerated canonical artifact path if absent, never overwrite; require fresh full primary SHA and identity, reject links/ancestor substitution, preserve recorded mode and mtime. No restore executed.',
  protection_screen={'current_V7_all_absolute_namespace_alias':False,'old_index_files_directories_alias':False,'critical_88roots':False,'all_687links_inbound':False},
  new_scientific_or_RSS_or_runtime_credit=False))
# Preserve results/docs/logs/source, all original non-replay input per native family,
# scientific analysis outputs and official initial libraries; proposals contain no such path.
selected={x['path']for x in candidates}
require(not(selected&set(primaryrecords)),'a retained source was also selected')
for p in selected:
 require(not protected(p),'selected became protected')
 require(Path(p).name in {'initial_axial_macrolib.xsm','initial_radial_track.bin','macro.xsm','track_data.bin','green_51.npz','green_61.npz','green_98.npz'},'unexpected result/doc/source candidate')
# Static all-current-source reference sweep outside artifact trees. No source is imported.
families=sorted({Path(p).relative_to(ART).parts[0]for p in selected});refs=[];source_read_bytes=0
for dp,dn,fn in os.walk(ROOT,followlinks=False):
 dn[:]=[n for n in dn if n not in {'.git','.venv','node_modules','artifacts','storage_cleanup_seventh_20261009'}]
 for n in fn:
  d=Path(dp)/n
  if d.is_symlink()or d.suffix not in {'.py','.sh','.md','.json','.c2m','.x2m','.f','.f90','.cpp','.h'}:continue
  if d.stat().st_size>2*1024**2:continue
  try:s=d.read_text()
  except(UnicodeError,OSError):continue
  source_read_bytes+=len(s.encode());hit=[{'line':ln,'text':line[:1500],'families':[f for f in families if f in line]}for ln,line in enumerate(s.splitlines(),1)if any(f in line for f in families)]
  if hit:
   doc(d);refs.append({'path':str(d),'sha256':EVIDENCE[str(d)]['sha256'],'matches':hit,'classification':'historical/static path reference; not evidence of a live consumer'})
# End-of-audit identity stability, symlinks repeated complete project screen.
last=[]
for dp,dn,fn in os.walk(ROOT,followlinks=False):
 for n in dn+fn:
  p=Path(dp)/n
  if p.is_symlink():last.append([str(p),os.readlink(p),str(p.resolve(strict=False))])
require(sorted(last)==links,'all-project symlinks changed')
for r in FRESH.values():require(identity(Path(r['path']))==r['identity'],'fresh source changed after read '+r['path'])
proposed=sum(c['allocated_bytes']for c in candidates);logical=sum(c['size']for c in candidates)
save('fresh_current_protection_screen.json',dict(status='READ_ONLY_PASS_NO_DELETION',graph_pin=gr,old_index_pin=ir,critical_root_source_pin=EVIDENCE[str(M)],critical_roots=m['critical_roots'],all_absolute_graph_strings=len(absolute),canonical_files=len(graph['canonical_files']),requirements_rows=len(graph['requirements']['rows']),namespaces=len(graph['namespaces']),aliases=len(graph['aliases']),live_resource_roots=len(graph['resource_snapshot']['roots'])if'roots'in graph.get('resource_snapshot',{})else None,all_project_symlinks={'count':len(links),'sha256':linksha,'complete_before_after_equal':True},rows=screen))
save('project_static_historical_reference_screen.json',dict(status='READ_ONLY_SOURCE_SCAN_NO_BUSINESS_IMPORT',matching_sources=refs,all_source_bytes_read=source_read_bytes,limitations='Text references are historical users and producers, not active process evidence. Current admitted source closure is the complete fresh V7 graph/old protection index plus roots/links; original historical manifests/verifiers are deliberately retained and require restoration of retired enumerated paths.'))
save('candidate_exact_restoration_mapping.json',dict(schema='SPOT_EIGHTH_OLD_WORK_INPUT_EXACT_COPY_CANDIDATES_V1',status='READ_ONLY_RECOMMENDATION_NO_DELETION',Root_exact_content_groups_pin=grouppin,Root_track_summary_pin=shortpin,exact_count=len(candidates),logical_bytes=logical,allocated_bytes=proposed,allocated_GiB=proposed/1024**3,candidates=candidates,rejected_keep=rejected,
 excluded_scope='Root narrowed review to ten native replay track_data.bin copies only. All initial macros, all non-replay tracks, green input NPZ, every analysis NPZ, every axial-material-* macro, A/B material and seed, archives, compiled/cache, TRACK_f scientific output, iterative/seed snapshots are HOLD or outside this precise candidate set.',
 pending_actual_deletion_result_sha256=None,files_deleted=0,formal_or_ART_writes=False,solver_or_API_or_PREP_RUN_executed=False,new_scientific_credit=False))
save('all_retained_primary_fresh_SHA_identity.json',list(primaryrecords.values()))
save('all_evidence_fresh_SHA_identity.json',list(EVIDENCE.values()))
report=dict(schema='SPOT_EIGHTH_OLD_WORK_INPUTS_READONLY_REVIEW_V1',status='PASS_READ_ONLY_RECOMMENDATION_NO_DELETION',exact_count=len(candidates),logical_bytes=logical,allocated_bytes=proposed,allocated_GiB=proposed/1024**3,categories=dict(collections.Counter(c['category']for c in candidates)),retained_primaries=len(primaryrecords),evidence_files=len(EVIDENCE),fresh_full_read_files=len(FRESH),fresh_full_read_bytes=sum(x['size']for x in FRESH.values()),rejected_keep=len(rejected),selected_all_unprotected=True,all_selected_exact_original_result_or_prepared_seal_bound=True,all_restore_primaries_exact_original_seal_bound=True,all_fresh_identities_stable=True,files_deleted=0,restore_executed=False,solver_or_API_or_native_PREP_RUN_executed=False,formal_or_ART_written=False,actual_cleanup_result_sha256=None,elapsed_seconds=time.monotonic()-START)
save('independent_recommendation.json',report)
print(json.dumps(report,indent=2),flush=True)
