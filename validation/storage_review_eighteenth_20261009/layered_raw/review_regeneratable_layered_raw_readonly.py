# Exact historical derived-raw candidates. Stdlib-only read/hash/source inspection.
import ast,hashlib,json,os,re,stat,time
from pathlib import Path
ROOT=Path('/Users/wen/spot');ART=ROOT/'validation/artifacts';SRC=ROOT/'validation/axial_material';N=ART/'native-layered-full-20261001';D=Path('/private/tmp/spot_storage_review_eighteenth_graph_20261009');PINS={};START=time.monotonic()
def identity(p):
 s=Path(p).lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
def pin(p,wanted=None):
 p=Path(p);before=identity(p);assert stat.S_ISREG(before[2])and p.resolve(strict=True)==p and before[6]==1,p
 h=hashlib.sha256()
 with p.open('rb')as f:
  assert os.fstat(f.fileno()).st_ino==before[1]
  while b:=f.read(4*2**20):h.update(b)
 assert identity(p)==before,p
 row=dict(path=str(p),identity=before,logical_bytes=before[3],allocated_bytes=p.stat().st_blocks*512,sha256=h.hexdigest())
 if wanted is not None:assert row['sha256']==wanted,p
 PINS[str(p)]=row;return row

def read(p,wanted=None):pin(p,wanted);return json.loads(Path(p).read_bytes())
def digest(v):
 h=hashlib.sha256()
 for b in json.JSONEncoder(sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).iterencode(v):h.update(b.encode())
 return h.hexdigest()
manifest_path=N/'result.sha256';manifest_pin=pin(manifest_path,'6ab0927cb9570715607c260873e907d6b6a429327773909ceb4b2e4f0af3ac2d');old={}
for line in manifest_path.read_text().splitlines():
 sha,name=line.split(None,1);name=name.lstrip('*');assert name not in old and re.fullmatch('[0-9a-f]{64}',sha);old[name]=sha

def sealed_read(rel):return read(N/rel,old[rel])
plan=sealed_read('plan.json');jobs=sealed_read('full_jobs.json');frozen=sealed_read('frozen_inputs.json');final=sealed_read('verification/result.json')
assert len(jobs)==2191 and len(frozen)==303 and final['full_batches']==1080 and final['scientific_replay_files']==16200 and final['independent_audits']==24 and final['independent_full_traces']==288
assert all(final[k]is True for k in('full_native_physical_operator_qualified','full_native_white_qualified','full_previous_zero_gradient_regression_completed'))and final['production_changed']is False and final['coupled_eigenproblem_qualified']is False
fullcases={r['id']:r for r in plan['batches']if not r.get('preflight',False)};assert len(fullcases)==1080
primary={r['args'][0]:r for r in jobs if r['script']=='run_native_layered_full_batch.py'and r['args'][1]=='primary'}
replay={r['args'][0]:r for r in jobs if r['script']=='run_native_layered_full_batch.py'and r['args'][1]=='replay'}
assert set(primary)==set(replay)==set(fullcases)
# Complete original fixed input/build/source hashes, including source copies actually executed.
for name,wanted in frozen.items():pin(Path(name)if Path(name).is_absolute()else N/name,wanted)
producer=N/'build/run_native_layered_full_batch.py';storage=N/'build/native_layered_batch_storage.py';auditor=N/'build/audit_native_layered_full.py'
for p in(producer,storage,auditor):assert str(p)in PINS
pt=producer.read_text();st=storage.read_text();at=auditor.read_text()
assert "scientific(root,phase,case_id,f'raw_g"in pt and "scientific(root,phase,case_id,'operators.npz'"in pt and "scientific(root,phase,case_id,'controls.npz'"in pt
assert "elif"not in '' # no-op; all meaningful gates above and below are concrete source assertions.
assert "with path.open('xb')"in st and "actual==sha"in st and 'serialize_npz' in st
assert "raw=read(folder/f'raw_g"in at and "result_dir/'operators.npz'"in at and 'all_checks_passed=True' in at
source_proof={}
for p,names in[(producer,['main']),(storage,['scientific','serialize_npz','records']),(auditor,['main'])]:
 text=p.read_text();tree=ast.parse(text);defs={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)}
 source_proof[str(p)]=dict(whole_source=PINS[str(p)],functions=[dict(name=name,line=defs[name].lineno,complete_source_sha256=hashlib.sha256(ast.get_source_segment(text,defs[name]).encode()).hexdigest())for name in names])
# Current ordinary full owner union is independently expected, never derived from candidate fresh hashes.
G=Path('/private/tmp/axmat_v9_actual_controls_graph_resource_scope_20261009');B=Path('/private/tmp/axmat_v9_actual_cold_binding_graph_resource_independent_review_20261009')
g=read(G/'REPORT.json','891ba5161ae1759187bd5f840419e2b1cc8125aba8865ffed4476121e30af0ba');bp=read(B/'REPORT.json','03ebde650f63e045ae7a35f1018e02f787aac47fef28812a9a7a7fd719760e3c')
S=ART/'axial-material-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-last-cprime-trim-file-snapshot-admission-scipy-env-physical-basis-own-pid-peak-v9-20261009'
m=read(S/'rank1_factor_cache_admission.json','564592df0acffc7bbc2c0743cd1b4849db859ec7e83b6101def72ce4a5175742');expected=dict(m['files']);expected.update(bp['additional_expected_files']);assert len(expected)==37395 and digest(expected)==g['expected_map_sha256']
assert digest({p:identity(p)for p in m['files']})==g['metadata37339_beforeafter_identity_digest']
gp=g['graph_whole_pin'];assert identity(gp['path'])==gp['identity'];graph=json.loads(Path(gp['path']).read_bytes());assert identity(gp['path'])==gp['identity']
canonical={r['path']for r in graph['canonical_files']};assert len(canonical)==35647
namespace_roots={r['root']for r in graph['namespaces']};assert len(graph['namespaces'])==86
alias_endpoints={r[k]for r in graph['aliases']for k in('path','target')};assert len(graph['aliases'])==186
strings=set();stack=[graph]
while stack:
 v=stack.pop()
 if type(v)is str:strings.add(v)
 elif type(v)is list:stack.extend(v)
 elif type(v)is dict:strings.update(v.keys());stack.extend(v.values())
root_expected={p:w for p,w in expected.items()if Path(p).is_relative_to(N)};assert len(root_expected)==1
assert not any(Path(r).is_relative_to(N)or N.is_relative_to(Path(r))for r in namespace_roots)
# Trace the current source contract without calling any of these functions.
F=SRC/'prepare_historical_input_owned_specs_physical_last_cprime_trim_file_snapshot_cold_AAA_scipy_env_physical_basis_own_pid_peak.py';C=SRC/'cold_component_input_consumer_last_cprime_trim_own_pid_peak.py';H=Path(m['component_current_context']['runtime_context']['root'])/'combined_cold_own_rss_host.py'if 'component_current_context'in m else S/'combined_cold_own_rss_host.py'
current_defs={}
for p,wanted,names in[(F,'59d0c9b0f0a3b9ca6764f628ade537ec9b09eaa6edfe69e734994a7323adbfc8',['materialize_metadata','component_current_context','cold_launch_in_clean_process','cold_terminal_admission']), (C,'2fa0cb00ec458e9bbbbdf2f15db703a1c0547b08d35f585b6c7e6e6274d06d59',['expected_union','complete_input_phase','post_graph_metadata','consume_completed_inputs','consume_metadata'])]:
 pin(p,wanted);text=p.read_text();tree=ast.parse(text);defs={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)}
 current_defs[str(p)]=dict(whole_source=PINS[str(p)],complete_functions=[dict(name=name,line=defs[name].lineno,source_sha256=hashlib.sha256(ast.get_source_segment(text,defs[name]).encode()).hexdigest())for name in names])
current_text=C.read_text();assert 'original_component_APIs_executed_in_this_process=False'in current_text and 'additional={p:sha for p,sha in all_expected.items()'in current_text
pilot=SRC/'qualify_refined_AAA_layered_input_pilot.py';pilottext=pilot.read_text();pin(pilot);assert "selected=['build/cached.dylib','build/native_layered_cached.cpp','build/native_layered_geometry.hpp',"in pilottext
# All primary retained aggregate numerics and exact raw source job evidence are freshly sealed.
rawnames=[f'raw_g{group}_o{o}_m{sign}.npz'for group in(51,61,98)for o in(1,-1)for sign in(-1,1)]
rows=[];retained=[];commands=[];families=set()
for i,cid in enumerate(sorted(fullcases)):
 case=fullcases[cid];families.add(cid.rsplit('_b',1)[0])
 p=sealed_read('receipts/primary/'+cid+'.json');r=sealed_read('receipts/replay/'+cid+'.json')
 assert p['files']==r['files']and p['all_scientific_bytes_identical']is False and r['all_scientific_bytes_identical']is True
 assert set(p['files'])==set(rawnames)|{'operators.npz','controls.npz','result.json'}
 summary=sealed_read('primary/'+cid+'/result.json');assert summary['case']==case and summary['all_checks_passed']is True and summary['full_cell_face_regression_byte_exact']is True
 watch=sealed_read('runs/primary_'+cid+'_watchdog.json');rw=sealed_read('runs/replay_'+cid+'_watchdog.json')
 for w,phase in[(watch,'primary'),(rw,'replay')]:
  assert type(w['returncode'])is int and w['returncode']==0 and w['limit_failure']is None and 0<w['elapsed_seconds']<600 and 0<w['sampled_peak_rss_mib']<512
  assert w['command'][1:]==[str(producer),str(N),cid,phase]
 commands.append(dict(job=primary[cid],original_primary_command=watch['command'],original_replay_command=rw['command'],case=case,primary_watch=PINS[str(N/'runs'/('primary_'+cid+'_watchdog.json'))],replay_watch=PINS[str(N/'runs'/('replay_'+cid+'_watchdog.json'))],primary_receipt=PINS[str(N/'receipts/primary'/(cid+'.json'))],replay_receipt=PINS[str(N/'receipts/replay'/(cid+'.json'))],retained_result=PINS[str(N/'primary'/cid/'result.json')]))
 for name in('operators.npz','controls.npz'):
  rel='primary/'+cid+'/'+name;rp=pin(N/rel,old[rel]);assert rp['sha256']==p['files'][name]['sha256']and rp['logical_bytes']==p['files'][name]['bytes'];retained.append(rp)
 for name in rawnames:
  rel='primary/'+cid+'/'+name;path=str(N/rel);assert path not in expected and path not in canonical and path not in alias_endpoints and path not in strings
  assert all(not Path(path).is_relative_to(Path(root))for root in namespace_roots)
  rp=pin(path,old[rel]);assert rp['sha256']==p['files'][name]['sha256']and rp['logical_bytes']==p['files'][name]['bytes']
  row=dict(rp,original_manifest=manifest_pin,original_manifest_relative_path=rel,job_id=primary[cid]['name'],case_id=cid,primary_result_path=str(N/'primary'/cid/'result.json'),retained_operators_path=str(N/'primary'/cid/'operators.npz'),retained_controls_path=str(N/'primary'/cid/'controls.npz'),primary_receipt_path=str(N/'receipts/primary'/(cid+'.json')),replay_receipt_path=str(N/'receipts/replay'/(cid+'.json')),current_exact_expected_canonical_namespace_alias_literal_hits=0,category='COMPLETED_REGENERATABLE_PER_TRACK_RAW_WITNESS',recoverability='Recompute under preserved original plan+303 inputs/build/source and original command in an isolated scratch root; verify each regenerated raw SHA and size against preserved manifest/receipt before any explicit restoration. No lossless archive or instant restore is claimed.')
  rows.append(row)
 if i%120==0:print(json.dumps(dict(completed_batches=i+1,raw_files=len(rows),elapsed_seconds=time.monotonic()-START)),flush=True)
assert len(rows)==12960 and len(families)==24
for family in sorted(families):
 fr=sealed_read('verification/'+family+'/result.json');assert fr['all_checks_passed']is True and fr['raw_files']==540 and fr['original_tracks']==11364 and fr['all_original_indices_once']is True
 pin(N/'verification'/family/'operators.npz',old['verification/'+family+'/operators.npz'])
# Leave every preflight sample and all audits/independent worst-field arrays untouched.
allraw={str(p)for p in(N/'primary').glob('*/raw_g*.npz')};held_samples=sorted(allraw-{r['path']for r in rows});assert len(held_samples)==12
for p in held_samples:pin(p,old[str(Path(p).relative_to(N))])
for p,r in PINS.items():assert identity(p)==r['identity'],p
assert digest({p:identity(p)for p in m['files']})==g['metadata37339_beforeafter_identity_digest']
assert identity(gp['path'])==gp['identity']
logical=sum(r['logical_bytes']for r in rows);allocated=sum({tuple(r['identity'][:2]):r['allocated_bytes']for r in rows}.values())
manifest=dict(schema='SPOT_R18_EXACT_REGENERATABLE_LAYERED_FULL_COMPLETED_RAW_CANDIDATES_V1',status='SOURCE_AND_BYTE_CANDIDATES_FOR_ROOT_PREFLIGHT_NOT_DELETED',candidate_count=len(rows),candidate_logical_bytes=logical,candidate_unique_inode_allocated_bytes=allocated,candidates=rows,held_preflight12=held_samples)
with(D/'layered_raw_candidates.json').open('x')as f:json.dump(manifest,f,indent=2,allow_nan=False);f.write('\n')
with(D/'layered_raw_kept_outputs_and_job_evidence.json').open('x')as f:json.dump(dict(retained_batch_operator_control2160=retained,all1080_job_evidence=commands,full_source_and_input_pins=PINS),f,indent=2,allow_nan=False);f.write('\n')
report=dict(schema='SPOT_R18_LAYERED_COMPLETED_DERIVED_RAW_DEPENDENCY_AND_REGENERATION_READONLY_SOURCE_REVIEW_V1',status='PASS',recommended_source_scope_only=True,approval_still_requires_Root_fixed_preflight_and_independent_review=True,candidate_count=len(rows),logical_bytes=logical,unique_inode_allocated_bytes=allocated,current_index_coverage_of_native_layered_entire_family=dict(expected_files=root_expected,logical_bytes=sum(identity(p)[3]for p in root_expected),canonical_namespace_records=0,candidate_currentexpected_canonical_namespace_alias_literal_hits=0),current_graph_endpoint=gp,current_graph_metadata_only_read=True,old35GB_scientific_payload_bytes_read=0,current_owner37395_expected_digest=digest(expected),current_source_readchain=current_defs,source_contract_exclusion_reason='F59 materialize_metadata -> copied consumer consume_metadata/complete_input_phase opens only canonical graph endpoints plus independent expected additional endpoints, exact successful namespaces and fixed current predicates; old component APIs are explicitly not executed. Future cold binds exactly original prepared/binding/MRO and these input phases. The current graph canonical/NS/alias/literal sets and full owner expected map contain none of these selected raw paths. OLD native input pilot prepare selects7 retained source/input/final result files; it does not iterate whole native result.sha256 payloads.',original_source_producer_and_raw_independent_reduction=source_proof,completed_original_1080_primary_and_replay_receipts_SHA_match=True,completed_original_24_independent_audits_and_final_flags=True,fresh_all303_original_frozen_inputs_SHA_valid=True,all12960_raw_fresh_fullSHA_original_manifest_and_both_receipts_equal=True,all2160_batch_operator_control_fresh_original_SHA_retained=True,all1080_summary_and_rawlogs_watchdog_commands_retained=True,all24_final_assembled_operator_arrays_fresh_original_SHA_retained=True,leave_preflight12_and_independent288_worst_traces_white_inputs_build_reports_and_logs=True,retained_operators_controls_are_final_numerical_results_not_lossless_raw_substitute=True,original_results_manifest_and_failure_history_unchanged=True,regeneration_recipe='For a historical per-raw audit/replay, construct an isolated scratch root using exact preserved plan/admission,303 original inputs/build/source files and recorded original Python command with scratch root replacing only artifact root argument; run original primary worker under original512MiB/600s serial limits, then require every raw regenerated size/fullSHA equals old primary+replay receipts and manifest before restoring exactly selected paths. Keep original operators/controls/results in original root; do not rerun original primary there because xb would encounter retained aggregate files. New generation/resource evidence must be truthful and separately authorized; no regeneration was performed here.',no_instant_restore_or_native_replay_after_retirement_claim=True,prior_restore_master_cross_check='Pending complementary reviewer/Root fixed preflight; any candidate serving a retained prior restore primary must be excluded before deletion.',all_contents_referenced_only_by_original_job_replay_audit_full_manifest_require_recompute_before_rerun=True,files_deleted=0,project_written=False,scientific_business_executed=False,source_only_api_or_consumer_called=False,elapsed_seconds=time.monotonic()-START,evidence_count=len(PINS))
with(D/'LAYERED_RAW_REVIEW.json').open('x')as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n')
print(json.dumps(dict(status='PASS',candidate_count=len(rows),logical_bytes=logical,allocated_bytes=allocated,old_raw_fullrevalidation_requires_recompute=True,files_deleted=0,project_written=False,elapsed_seconds=report['elapsed_seconds']),sort_keys=True),flush=True)
