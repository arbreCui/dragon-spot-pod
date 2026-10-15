"""Independent read-only postdelete audit. Writes only its own TMP reports."""
from pathlib import Path
import collections, datetime, hashlib, json, os, stat, subprocess, time

ROOT=Path('/Users/wen/spot')
ART=ROOT/'validation/artifacts'
R=ROOT/'validation/storage_cleanup_seventh_20261009'
OUT=Path('/private/tmp/spot_storage_seventh_actual_postdelete_independent_review_20261009')
PINS={'manifest.json':'80db08c34dcaa406950eb3680287f016d619ee76ac9503232dbf8e9348ee6038',
 'preflight.json':'63b88ddaca81a980ae6d62f70305f8d07acede3257937ad11642a6f64b992518',
 'independent_preflight_review.json':'b834a026f0a925d2f1a8f770be6091440df9354a562e8bf6da26c3d9fd03fe57',
 'cleanup_result.json':'ff3938cb499e56b4d185e3611fbf3f50d022afe8ec830ecb1e749763caed1b13',
 'cleanup_terminal_observation.json':'a06785d84eb06dd05368188b60263f649f8740ac68f28c89d6411e7793059904',
 'retirement_ledger.jsonl':'c27cdc4181141f908137012511d512da28040e5aa2ca5f486ec32c725f6dbe8d'}
TOOLS={'cleanup_exact_files.py':'8852b5213ee44039141ff67a35b97da27577d570b2097709b507d6a375057c56',
 'restore_retired_tar.py':'15af4d8112e7299d3cd9a93d12b3208cc5330a3a60fc906cd5c2145f8e4c5c32',
 'restore_retired_work_copies.py':'53a51f0f70c5194b13328d01b356d33260cd1b310753fda743b8ad6af6a687bd'}

def require(condition,message):
 if not condition:raise ValueError(message)
def identity(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
def pin(p,expected_sha=None,expected_record=None,retain_bytes=False):
 p=Path(p);before=identity(p);require(stat.S_ISREG(before[2]),'not regular: '+str(p));h=hashlib.sha256();blocks=[]
 with p.open('rb') as f:
  require([os.fstat(f.fileno()).st_dev,os.fstat(f.fileno()).st_ino]==before[:2],'opened different inode')
  while True:
   block=f.read(8*1024**2)
   if not block:break
   h.update(block)
   if retain_bytes:blocks.append(block)
 require(identity(p)==before,'changed during fresh read: '+str(p));sha=h.hexdigest()
 if expected_sha is not None:require(sha==expected_sha,'SHA mismatch: '+str(p))
 row=dict(path=str(p),identity=before,sha256=sha,size=before[3])
 if expected_record is not None:require(row=={k:expected_record[k]for k in row},'pinned record mismatch: '+str(p))
 return row,(b''.join(blocks)if retain_bytes else None)
def object_pairs(items):
 out={}
 for k,v in items:
  require(k not in out,'duplicate JSON key');out[k]=v
 return out
def strict_json(data):
 return json.loads(data.decode('utf-8'),object_pairs_hook=object_pairs,
  parse_constant=lambda x:(_ for _ in ()).throw(ValueError('nonfinite JSON constant')))
def write(name,value):
 with(OUT/name).open('x')as f:json.dump(value,f,indent=2);f.write('\n')
def inventory(excluded):
 h=hashlib.sha256();counts=collections.Counter()
 for dp,dn,fn in os.walk(ROOT,followlinks=False):
  dn[:]=sorted(n for n in dn if Path(dp)/n!=R)
  for n in sorted(dn+fn):
   p=Path(dp)/n
   if str(p)in excluded:continue
   s=p.lstat();relative=str(p.relative_to(ROOT))
   if stat.S_ISLNK(s.st_mode):row=[relative,identity(p),os.readlink(p)];counts['symlinks']+=1
   elif stat.S_ISDIR(s.st_mode):row=[relative,'directory'];counts['directories']+=1
   elif stat.S_ISREG(s.st_mode):row=[relative,identity(p)];counts['regular_files']+=1
   else:raise ValueError('unexpected filesystem type: '+str(p))
   h.update(json.dumps(row,ensure_ascii=False,separators=(',',':')).encode()+b'\n')
 return dict(sha256=h.hexdigest(),**dict(counts))
def symlinks(selected):
 rows=[]
 for dp,dn,fn in os.walk(ROOT,followlinks=False):
  for n in dn+fn:
   p=Path(dp)/n
   if p.is_symlink():
    before=identity(p);target=p.resolve(strict=False);text=os.readlink(p)
    require(identity(p)==before,'link changed while reading')
    require(not any(Path(q)==target or Path(q).is_relative_to(target)for q in selected),'inbound link to retired target')
    rows.append([str(p),text,str(target)])
 return dict(count=len(rows),sha256=hashlib.sha256(json.dumps(sorted(rows)).encode()).hexdigest())

started=time.monotonic();OUT.mkdir(exist_ok=True);pinned={};raw={}
for n,sha in PINS.items():
 pinned[n],raw[n]=pin(R/n,sha,retain_bytes=True)
m,pf,review,result,terminal=[strict_json(raw[n])for n in ['manifest.json','preflight.json','independent_preflight_review.json','cleanup_result.json','cleanup_terminal_observation.json']]
require(result['status']=='PASS'and review['status']=='PASS'and pf['status']=='PASS','saved stage not PASS')
for obj in(pf,review,result,terminal):require(obj['manifest_sha256']==PINS['manifest.json'],'manifest association mismatch')
for obj in(review,result,terminal):require(obj['preflight_sha256']==PINS['preflight.json'],'preflight association mismatch')
require(result['independent_preflight_sha256']==PINS['independent_preflight_review.json']==terminal['independent_preflight_sha256'],'independent report binding mismatch')
require(terminal['cleanup_result_sha256']==PINS['cleanup_result.json']and terminal['retirement_ledger_sha256']==PINS['retirement_ledger.jsonl'],'actual terminal result/ledger mismatch')
require(terminal['closed']is True and terminal['exit_code']==0 and terminal['actual_deletion_completed']is True and terminal['actual_stdout_status']=='PASS','Root terminal is not closed EXIT0 PASS')
require((terminal['initial_chunk_id'],terminal['session_id'],terminal['terminal_chunk_id'])==('f19b41',33439,'33fbc8'),'unexpected actual tool chain')
require(result['solver_or_API_executed']is False and result['new_scientific_credit']is False,'unexpected new science or API claim')
require(len(m['candidates'])==m['exact_count']==result['deleted_files']==terminal['actual_deleted_files']==1183,'wrong exact deletion count')
selected={c['path']for c in m['candidates']};require(len(selected)==1183,'duplicate candidate')
require(len(m['retained_primaries'])==1216 and len(m['source_and_review_pins'])==540,'retained/evidence count changed')
require(len(set(m['critical_roots']))==len(m['critical_roots'])==88,'critical roots count changed')
require(result['deleted_logical_bytes']==m['logical_bytes']==sum(c['size']for c in m['candidates'])==7639813773,'logical byte total mismatch')
require(result['deleted_allocated_bytes']==m['allocated_bytes']==sum(c['allocated_bytes']for c in m['candidates'])==7642398720,'allocated byte total mismatch')
require(len(pf['verified_candidates'])==1183,'preflight candidate count mismatch')
ledger=[strict_json(line)for line in raw['retirement_ledger.jsonl'].splitlines()]
require(len(ledger)==1183,'ledger count mismatch')
for c,p,l in zip(m['candidates'],pf['verified_candidates'],ledger):
 require(p=={k:c[k]for k in('path','identity','sha256','size')},'preflight original candidate mismatch')
 require(l==dict(**p,category=c['category'],deleted=True),'ledger order/identity/SHA/category mismatch')
 path=Path(c['path']);require(path.is_absolute()and str(path)==c['path']and '..'not in path.parts and path.is_relative_to(ART)and path.parent.resolve(strict=True)==path.parent,'noncanonical retired path')
 try:path.lstat()
 except FileNotFoundError:pass
 else:raise ValueError('selected candidate not missing: '+str(path))

baseline=pf['preservation_baseline'];require(result['nonselected_before']==result['nonselected_after']==baseline,'Root post baseline mismatch')
require(baseline=={'sha256':'b1641e20aa2097be597feeaa7477cfdd695947e059301019141101b69666c8b5','directories':6978,'regular_files':175413,'symlinks':687},'unexpected baseline')
first_inventory=inventory(selected);require(first_inventory==baseline,'independent initial inventory mismatch')
print(json.dumps(dict(stage='candidate_absence_ledger_and_full_inventory_checked',missing=1183,baseline=first_inventory)),flush=True)

# Full independent byte reads of every primary/evidence record, not a sample.
primaries=[];evidence=[]
for group,dest in[(m['retained_primaries'],primaries),(m['source_and_review_pins'],evidence)]:
 for record in group:
  p,b=pin(record['path'],expected_record=record);dest.append(p)
require(len({p['path']for p in primaries+evidence})==1756,'overlap in primary/evidence byte proof')
require([p for p in primaries]==pf['verified_primaries'],'primary vector differs from actual preflight')
write('all_1216_retained_primaries_fresh_SHA_identity.json',primaries)
write('all_540_source_review_evidence_fresh_SHA_identity.json',evidence)
print(json.dumps(dict(stage='all_retained_primary_and_evidence_full_SHA_checked',files=1756,bytes=sum(p['size']for p in primaries+evidence))),flush=True)

graph_pin,graph_bytes=pin(m['graph_pin']['path'],expected_record=m['graph_pin'],retain_bytes=True)
index_pin,index_bytes=pin(m['old_index_pin']['path'],expected_record=m['old_index_pin'],retain_bytes=True)
graph,index=strict_json(graph_bytes),strict_json(index_bytes);absolute=set()
def walk(v):
 if isinstance(v,dict):
  for k,x in v.items():walk(k);walk(x)
 elif isinstance(v,list):
  for x in v:walk(x)
 elif isinstance(v,str)and v.startswith('/'):absolute.add(v)
walk(graph)
dirs=set(x['canonical_root']for x in graph['namespaces'])|set(x['target']for x in graph['aliases']if x['kind']in('directory','dir'))|set(index['protected_directories'])|set(m['critical_roots'])
protected=absolute|set(index['protected_files'])|set(index['inbound_alias_targets'])
require(not(selected&protected),'selected graph/index protected file intersection')
require(not[(p,d)for p in selected for d in dirs if p==d or p.startswith(d+'/')],'selected namespace/critical directory intersection')
link=symlinks(selected);require(link==pf['symlink_screen']==result['symlink_check_after'],'fresh symlink fingerprint mismatch')
tool_pins=[]
for n,sha in TOOLS.items():tool_pins.append(pin(R/n,sha)[0])
require(TOOLS['cleanup_exact_files.py']==m['cleanup_source_sha256'],'cleanup tool differs from manifest')
require((R/'cleanup_exact_files.py').read_bytes()==Path('/private/tmp/spot_storage_seventh_exact_cleanup_20261009.py').read_bytes(),'formal/TMP cleanup source differs')

# The verified tar utility's default only streams reconstruction; no --restore.
recipe_pin,recipe_bytes=pin(R/'tar/candidate.json',retain_bytes=True);tar_candidate=next(c for c in m['candidates']if c['category']=='EXACT_RECONSTRUCTIBLE_REHEARSAL_TAR')
require(recipe_pin['sha256']==tar_candidate['restoration_recipe_sha256'],'tar recipe differs')
proc=subprocess.run(['/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12',str(R/'restore_retired_tar.py')],capture_output=True,text=True)
require(proc.returncode==0,'default tar stream verification failed: '+proc.stderr)
tar_proof=strict_json(proc.stdout.encode())
require(tar_proof['status']=='PASS'and tar_proof['restored']is False and tar_proof['archive_sha256']==tar_candidate['sha256']and tar_proof['bytes']==tar_candidate['size'],'default tar exact proof mismatch')
require(not Path(tar_candidate['path']).exists()and not Path(tar_candidate['path']).is_symlink(),'default tar unexpectedly restored target')
write('actual_default_tar_stream_verification.json',dict(command=proc.args,returncode=proc.returncode,stdout=proc.stdout,stderr=proc.stderr,parsed=tar_proof,tool_sha256=TOOLS['restore_retired_tar.py'],restore_flag_passed=False,business_API=False))

last_inventory=inventory(selected);require(last_inventory==baseline==first_inventory,'final full nonselected inventory changed')
require(symlinks(selected)==link,'symlink screen changed during independent audit')
for p in primaries+evidence+tool_pins+[graph_pin,index_pin,recipe_pin]+list(pinned.values()):require(identity(Path(p['path']))==p['identity'],'file changed after fresh verification: '+p['path'])
for p in selected:
 try:Path(p).lstat()
 except FileNotFoundError:pass
 else:raise ValueError('retired target recreated before independent finalization')
allocated=int(subprocess.check_output(['/usr/bin/du','-k','-s',str(ROOT)],text=True).split()[0])*1024
summary=dict(schema='SPOT_SEVENTH_ACTUAL_POSTDELETE_INDEPENDENT_READ_ONLY_REVIEW_V1',status='PASS',
 manifest_sha256=PINS['manifest.json'],preflight_sha256=PINS['preflight.json'],cleanup_result_sha256=PINS['cleanup_result.json'],
 independent_preflight_sha256=PINS['independent_preflight_review.json'],ledger_sha256=PINS['retirement_ledger.jsonl'],Root_actual_terminal_pin=pinned['cleanup_terminal_observation.json'],
 actual_Root_tool_chain=dict(initial_chunk_id='f19b41',session_id=33439,terminal_chunk_id='33fbc8',exit_code=0,closed=True),
 exact_1183_candidates_missing_before_and_after=True,ledger_equals_preflight_order_all_SHA_identity_categories=True,
 deleted_logical_bytes=7639813773,deleted_allocated_bytes=7642398720,
 independent_full_content_hash_scope=dict(retained_primary_records=1216,evidence_records=540,total_unique_files=1756,total_bytes=sum(p['size']for p in primaries+evidence),all_records_complete_fresh_SHA_and_identity_not_sampled=True),
 original_result_docs_raw_matrices_and_current_material_outputs_in_evidence_unchanged=True,
 nonselected_before=first_inventory,nonselected_after=last_inventory,nonselected_identity_inventory_unmodified=True,
 nonselected_inventory_scope='Every project file/link/directory path outside this cleanup report folder; all regular identities and link texts. Full content SHA coverage is exactly all1756 declared primary/evidence files plus graph/index/tools/actual documents, not every project file.',
 graph_pin=graph_pin,old_index_pin=index_pin,graph_critical_closure=dict(canonical_files=len(graph['canonical_files']),requirements_rows=len(graph['requirements']['rows']),namespaces=len(graph['namespaces']),aliases=len(graph['aliases']),critical_roots=len(m['critical_roots']),candidate_intersections=[]),
 fresh_all_project_symlinks=link,reviewed_tool_pins=tool_pins,default_tar_exact_stream_verified_without_restore=True,tar_stream_proof=tar_proof,
 independent_project_allocated_bytes_after=allocated,Root_recorded_project_allocated_bytes_before=result['capacity_before']['project_allocated_bytes'],Root_recorded_project_allocated_bytes_after=result['capacity_after']['project_allocated_bytes'],
 independent_files_deleted=0,independent_restore_executions=0,independent_apply_executions=0,business_import_API_constructor_native_PREP_RUN_executed=False,
 formal_source_or_project_reports_written_by_independent_reviewer=False,new_scientific_or_RSS_credit=False,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-started)
write('independent_postdelete_review.json',summary)
print(json.dumps(dict(status='PASS',manifest_sha256=PINS['manifest.json'],preflight_sha256=PINS['preflight.json'],cleanup_result_sha256=PINS['cleanup_result.json'],report=str(OUT/'independent_postdelete_review.json'),report_sha256=hashlib.sha256((OUT/'independent_postdelete_review.json').read_bytes()).hexdigest(),all_primary_evidence_complete_SHA=1756,exact_missing=1183,nonselected=last_inventory,elapsed_seconds=time.monotonic()-started)),flush=True)
