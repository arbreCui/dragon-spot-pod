import ast,hashlib,json,math,os,stat,time
from pathlib import Path
ROOT=Path('/Users/wen/spot');V=ROOT/'validation';ART=V/'artifacts';R=V/'storage_cleanup_thirteenth_20261009';H=Path(__file__).resolve().parent
MANIFEST_SHA='810e1bb9ed07c24b633cf92e057551d8c3f7ebfdf2c474fb87f4096770dc25db'
CODE_SHA='773a3a5590b7e5ef5f3f449d188c173befd996ae8f865ce789ffe7640b03dd38';RESTORE_SHA='750173af18ef889b648f19fd6282aa5adad46838ccf67cfd89d408d388dc2b51'
BYTE_SHA='77fe179d3230eefcc7d9d7897650e414f342e7579ba65f9e6c641bfd9b1db7ba'
def out(v):return ART/f'axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-v{v}-20261009'
def source(v):return ART/f'axial-material-qualified-AB-historical-input-physical-dedup-combined-runtime-build-admission-owned-specs-last-cprime-trim-live-resource-scopes-v{v}-20261009'
def term(v):return ART/f'axial-material-qualified-AB-historical-input-physical-dedup-combined-runtime-build-terminal-owned-specs-last-cprime-trim-live-resource-scopes-v{v}-20261009'
FIXED={str(out(v)/'runtime/Dragon')for v in (7,8)};MASTER=out(9)/'runtime/Dragon';PINS={};BYTES=0
def identity(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
def pin(p,expected=None):
 global BYTES
 p=Path(p);before=identity(p);assert p.resolve(strict=True)==p and stat.S_ISREG(before[2])
 if str(p)not in PINS:
  h=hashlib.sha256()
  with p.open('rb')as f:
   while b:=f.read(1024*1024):h.update(b)
  assert before==identity(p);PINS[str(p)]=dict(path=str(p),sha256=h.hexdigest(),size=before[3],identity=before);BYTES+=before[3]
 q=PINS[str(p)];assert before==q['identity']
 if expected:
  assert q['sha256']==expected['sha256']
  if 'size'in expected:assert q['size']==expected['size']
  if 'identity'in expected:assert q['identity']==expected['identity']
 return q
def pairs(rr):
 d={}
 for k,v in rr:
  if k in d:raise ValueError('duplicate JSON key')
  d[k]=v
 return d
def floating(s):
 f=float(s)
 if not math.isfinite(f):raise ValueError('nonfinite JSON float')
 return f
def reject(s):raise ValueError(s)
def obj(p,sha=None):
 q=pin(p,dict(sha256=sha)if sha else None);d=json.loads(Path(p).read_text(),object_pairs_hook=pairs,parse_float=floating,parse_constant=reject);assert identity(Path(p))==q['identity'];return d
def strings(x):
 stack=[x];r=set()
 while stack:
  v=stack.pop()
  if type(v)is str:r.add(v)
  elif type(v)is dict:stack.extend(v);stack.extend(v.values())
  elif type(v)is list:stack.extend(v)
 return r
def under(p,roots):return any(p==r or p.startswith(r+'/')for r in roots)
def metadata():
 h=hashlib.sha256();counts=dict(regular_files=0,symlinks=0,directories=0);links=[]
 def visit(base):
  h.update(json.dumps(['directory',str(base.relative_to(ROOT))],separators=(',',':')).encode()+b'\n');counts['directories']+=1
  entries=sorted((Path(e.path)for e in os.scandir(base)if Path(e.path)not in {ROOT/'.git',R}),key=lambda p:p.name);sub=[]
  for p in entries:
   s=p.lstat()
   if stat.S_ISDIR(s.st_mode):sub.append(p);continue
   if str(p)in FIXED:continue
   if stat.S_ISLNK(s.st_mode):
    value=['link',str(p.relative_to(ROOT)),identity(p),os.readlink(p)];counts['symlinks']+=1;links.append(str(p.resolve(strict=False)))
   elif stat.S_ISREG(s.st_mode):value=['file',str(p.relative_to(ROOT)),identity(p)];counts['regular_files']+=1
   else:continue
   h.update(json.dumps(value,separators=(',',':')).encode()+b'\n')
  for p in sub:visit(p)
 visit(ROOT);assert not FIXED.intersection(links)
 return dict(sha256=h.hexdigest(),**counts)

m=obj(R/'manifest.json',MANIFEST_SHA);assert m['cleanup_source_sha256']==CODE_SHA and m['restore_source_sha256']==RESTORE_SHA
assert 'independent_preflight_review_sha256'not in m
assert len(m['candidates'])==2 and {r['path']for r in m['candidates']}==FIXED
assert len(m['retained_primaries'])==1 and m['retained_primaries'][0]['path']==str(MASTER)
assert len(m['retained_control_pins'])==132 and sum(r['size']for r in m['retained_control_pins'])==445221954
assert m['files_deleted_before_this_manifest']==0 and m['science_credit']is False
for r in m['candidates']+m['retained_primaries']:
 p=Path(r['path']);pin(p,r);assert r['sha256']==BYTE_SHA and r['size']==9225720 and r['identity'][6]==1
 assert p.stat().st_blocks*512==r['allocated_bytes']
for r in m['candidates']:
 assert r['retained_primary']==str(MASTER) and r['restore_byte_exact_mapping']['source']==str(MASTER)
 assert r['restore_byte_exact_mapping']['target']==r['path'] and r['restore_byte_exact_mapping']['expected_sha256']==BYTE_SHA
 assert r['restore_byte_exact_mapping']['restore_mode']==stat.S_IMODE(r['identity'][2]) and r['restore_byte_exact_mapping']['restore_mtime_ns']==r['identity'][4]
 assert all(v is True for v in r['current_dependency_exclusions'].values())
assert len({tuple(r['identity'][:2])for r in m['candidates']+m['retained_primaries']})==3
for r in m['retained_control_pins']:pin(r['path'],r)
controlset={r['path']for r in m['retained_control_pins']};family_count=0
for v in (7,8,9):
 for root in (source(v),out(v),term(v)):
  assert root.is_dir() and root.resolve(strict=True)==root
  for p in root.rglob('*'):
   if p.is_file() and str(p)not in FIXED:assert str(p)in controlset;family_count+=1
for name,sha in [('cleanup_fixed_build_copies.py',CODE_SHA),('restore_retired_build_copies.py',RESTORE_SHA)]:pin(R/name,dict(sha256=sha));ast.parse((R/name).read_text())
c=(R/'cleanup_fixed_build_copies.py').read_text();rs=(R/'restore_retired_build_copies.py').read_text()
assert "pre['manifest_sha256']!=args.manifest_sha"in c and "sha(REPORT/'independent_preflight_review.json')!=args.independent_review_sha"in c
assert c.count('.unlink(')==1 and "os.path.lexists(REPORT/'retirement_ledger.jsonl')"in c and "os.path.lexists(REPORT/'cleanup_result.json')"in c
assert "{r['path'] for r in rows}!=ALLOWED"in rs and 'master!=PRIMARY'in rs and "if not args.manifest_sha or sha(manifest)!=args.manifest_sha"in rs
assert "if args.restore_one is None and not args.restore_all:"in rs and "'LIST_ONLY_NO_WRITE'"in rs
assert not os.path.lexists(R/'retirement_ledger.jsonl')and not os.path.lexists(R/'cleanup_result.json')
root=obj(R/'Root_preflight_tool_return.json');t=root['actual_tool'];assert t==dict(initial_chunk_id='e29ad0',session_id=3917,terminal_chunk_id='d4373d',exit_code=0,closed=True)
assert type(t['exit_code'])is int and root['actual_tool_terminal_observed']is True and root['record_written_after_actual_terminal_return']is True
stdout=obj(R/'preflight.stdout',root['stdout_sha256']);pin(R/'preflight.stderr',dict(sha256=root['stderr_sha256']));assert (R/'preflight.stderr').stat().st_size==0
assert stdout==root['result'] and stdout['status']=='PASS_FIXED_TWO_COPY_PREFLIGHT'and stdout['executed']is False and root['files_deleted']==0
assert stdout['manifest_sha256']==MANIFEST_SHA and stdout['count']==2 and stdout['logical_bytes']==18451440 and stdout['allocated_bytes']==18456576
before=metadata();assert before==stdout['other_paths_before']
dependency=obj(m['current_dependency_review']['path'],m['current_dependency_review']['sha256']);assert dependency['status']=='PASS'
for key in ('exact_candidate_pin','full_current_readchain_source_proof_pin','base_review_pin','additional_tail_source_proof_pin'):pin(dependency[key]['path'],dependency[key])
base=obj(R/'candidate_current_dependency_review/REPORT.json','e8144d7b6d23f1c3901370f66209a3c781cbac37ecc01a6c742c926c8bccc9e5')
proof=obj(R/'candidate_current_dependency_review/current_actual_source_readchain_proof.json','26f7536790457d71715093b70fad3ae6089619ef49cefb797265d991e2b6609b')
tail=obj(R/'candidate_current_dependency_review/tail_and_R9_allocation_supplement.json','284b7e3689ab96d48c9aa647fe11635ee8e80563468ac5c5a70d98a8828c70be')
assert proof['status']=='PASS_READONLY_SOURCE_ONLY' and tail['status']=='PASS'
for r in base['fresh_control_source_candidate_pins']:pin(r['path'],r)
for r in tail['pins']:pin(r['path'],r)
clauses=proof['all_current_pipeline_clauses']+tail['source_clauses'];trees={};segments={}
for r in clauses:
 p=Path(r['source']['path']);pin(p,r['source'])
 if str(p)not in trees:
  text=p.read_text();trees[str(p)]=(text,ast.parse(text))
 text,tr=trees[str(p)];nodes=[n for n in ast.walk(tr)if isinstance(n,(ast.FunctionDef,ast.ClassDef))and n.name==r['definition']and n.lineno==r['start_line']and n.end_lineno==r['end_line']];assert len(nodes)==1
 seg=ast.get_source_segment(text,nodes[0]);assert seg==r['exact_definition']and hashlib.sha256(seg.encode()).hexdigest()==r['whole_definition_sha256'];segments[(str(p),r['definition'])]=seg
assert len(clauses)==37 and proof['selected_exact_paths_not_current_input']is True and proof['resource_history_directory_set_unpruned']is True
f=str(V/'axial_material/prepare_historical_input_owned_specs_trim_combined_physical_dedup_file_snapshot_runtime_build_live_resource_scopes_v9.py')
assert 'size!=archive_bytes()'in segments[(f,'external_terminal')]and "complete_archive_scope_roots']!=[str(SOURCE),str(OUT)]"in segments[(f,'declaration_admission')]
assert 'verify_inventory(SOURCE,snapshot)'in segments[(f,'prepare_terminal_admission')]
assert "g.strict_json(str(INPUT_SPECS),INPUT_SPECS_SHA)"in segments[(f,'actual_components')]
resource=str(V/'axial_material/prepare_qualified_AB_moment_order_production.py');rr=segments[(resource,'check')];assert 'read('not in rr and 'digest('not in rr and 'total > self.max_bytes'in rr
g=obj(out(9)/'input_graph.json','0e365ebbaafa0d9e9b3a34eee89cc9c3e1de3ee47812d985135b8201bd001be3');assert len(g['canonical_files'])==35647 and len(g['namespaces'])==86 and len(g['aliases'])==186 and len(g['absence_inputs'])==445 and len(g['live_resource_roots'])==231
canonical={x['path']for x in g['canonical_files']};ns={r[k]for r in g['namespaces']for k in ('root','canonical_root')};aliases={a[k]for a in g['aliases']for k in ('path','target')};adirs={a[k]for a in g['aliases']if a['kind']=='directory'for k in ('path','target')}
allgraph=strings(g);assert not FIXED.intersection(canonical|aliases|allgraph)and not any(under(p,ns|adirs)for p in FIXED)
assert all(Path(p).is_dir()for p in g['live_resource_roots'])
old=obj(Path('/private/tmp/spot_storage_second_dependency_20261008/protection_index.json'));assert not FIXED.intersection(old['canonical_protected_files'])and not any(under(p,old['exhaustive_dir_paths'])for p in FIXED)
m9=obj(V/'storage_cleanup_ninth_20261009/manifest.json');assert len(m9['current_cold_extra_protected_files'])==6248 and not FIXED.intersection(m9['current_cold_extra_protected_files'])
restore_paths=set()
for d in V.glob('storage_cleanup_*'):
 if d==R:continue
 for p in d.glob('*manifest*.json'):
  if p.name not in ('manifest.json','retire_manifest.json','cleanup_manifest.json','cache_manifest.json','cleanup_plan_manifest.json','retirement_manifest.json','approved_manifest.json'):continue
  prior=obj(p)
  for k in ('retained_primaries','retained_primaries_and_critical_sources','retained_tapes','final_merge_retained','retained_closed_anchors'):restore_paths.update(strings(prior.get(k)))
  for row in prior.get('candidates',[]):
   for k in ('retained_primary','retained_primary_pin','compressed_backup','restoration','restore_byte_exact_mapping'):restore_paths.update(strings(row.get(k)))
assert not any(under(p,restore_paths)for p in FIXED)
failed=[]
for v in (7,8):
 t=obj(term(v)/'terminal_return.json');assert type(t['returncode'])is int and t['returncode']==1 and t['successful_new_runtime_build_observed']is False
 stage=obj(out(v)/f'HISTORICAL_INPUT_TRIM_COMBINED_RUNTIME_LINK_V{v}/stages.json')['stages'];assert [s['status']for s in stage]==['PASS']*4+['FAILED']
 assert not os.path.lexists(out(v)/'seal.json')and not os.path.lexists(out(v)/'audit/result.json');failed.append(dict(version=v,actual_failed_returncode=1,seal_absent=True,stage_statuses=[s['status']for s in stage]))
seal=obj(out(9)/'seal.json','ece13c5594c48bb22af8d507f1f40ef88457efa824e28200c6ddfced70cf3aed');assert seal['files']['runtime/Dragon']==BYTE_SHA
current=obj(term(9)/'terminal_return.json','709a9592c8b4a56cba99c61b628db8fed91d0c49d76d75c360591f11fa1b9d27');assert type(current['returncode'])is int and current['returncode']==0
assert all(identity(Path(r['path']))==r['identity']for r in PINS.values())
after=metadata();assert after==before and not os.path.lexists(R/'retirement_ledger.jsonl')and not os.path.lexists(R/'cleanup_result.json')
report=dict(status='PASS',schema='SPOT_THIRTEENTH_EXACT_TWO_PREEXEC_INDEPENDENT_REVIEW_V1',manifest_sha256=MANIFEST_SHA,cleanup_source_sha256=CODE_SHA,restore_source_sha256=RESTORE_SHA,fixed_paths=sorted(FIXED),retained_primary=str(MASTER),full_byte_SHA=BYTE_SHA,each_size=9225720,allocated_bytes=18456576,
 Root_actual_preflight=root['actual_tool'],Root_preflight_receipt_sha256=PINS[str(R/'Root_preflight_tool_return.json')]['sha256'],Root_preflight_stdout_sha256=root['stdout_sha256'],preflight_no_deletion=True,
 whole132_retained_controls_full_SHA_size_identity=True,retained_control_logical_bytes=445221954,all_SOURCE_OUT_TERM_7_8_9_other_members_full_preserved=True,family_member_count=family_count,
 dynamic_source37clauses_exact_actual_AST_fullbytes=True,current_dependency_report_sha256=m['current_dependency_review']['sha256'],complete_graph_canonical_ns_alias_absence_roots_exclusion=dict(canonical=35647,namespaces=86,aliases=186,absence=445,roots=231),oldindex_cold6248_prior_restore_and_all687_links_excluded=True,
 original_V7_V8_failures_frozen=failed,current_sealed_V9_success_primary_retained=True,old_failed_package_replay_requires_exact_restore_and_prior_rounds=True,old_inode_ctime_not_restoreable=True,
 default_restore_static_LIST_ONLY_no_write=True,final_source_issues_repaired=True,whole_manifest_and_independent_report_SHA_separate_no_cycle=True,ledger_and_result_absent=True,
 whole_other_project_metadata_before=before,whole_other_project_metadata_after=after,fresh_full_SHA_unique_files=len(PINS),fresh_full_SHA_logical_bytes=BYTES,
 business_API_ctor_INPUT_cold_PREP_RUN_native_cleanup_restore_or_target_script_executed=False,formal_ART_written=False,scientific_credit=False,
 limitations=['Read-only preexec admission only; deletion outcome remains unknown.','Full selected/master/132controls and source/metadata proofs reread; complete 35GB canonical numerical payload not rehashed here.','Current directory resource roots remain all231; old audit selection is preserved as historical evidence and is not substituted for actual input contracts.','Metadata excludes .git and this report directory, compares regular file identities, link identities/targets and directory paths, not directory identities.'],actual_cleanup_outcome=None)
rp=H/'independent_preflight_review.json'
with rp.open('x')as f:json.dump(report,f,ensure_ascii=False,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
print(json.dumps(dict(status='PASS',report=str(rp),sha256=hashlib.sha256(rp.read_bytes()).hexdigest(),fixed_count=2,control_count=132,fullSHA_files=len(PINS),fullSHA_bytes=BYTES,other_paths=after),ensure_ascii=False),flush=True)
