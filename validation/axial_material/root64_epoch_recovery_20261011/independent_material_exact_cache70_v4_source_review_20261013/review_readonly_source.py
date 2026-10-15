"""Independent readonly material v4 audit; no import, compile or business run."""
import ast,hashlib,json,os,resource,stat,time
from pathlib import Path
REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
BASE=REC/'current_formal_material_authority_exact_cache70_source_v4'
COMMON=REC/'current_mount_full_identity_common_source_v1'
OUT=Path(__file__).resolve().parent
START=time.monotonic();checks=[];files={}
def need(ok,name):
 if not ok:raise RuntimeError(name)
 checks.append(name)
def identity(p):
 s=Path(p).lstat();return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=Path(p);before=identity(p);need(stat.S_ISREG(before[2]),'regular:'+str(p))
 with p.open('rb')as f:
  s=os.fstat(f.fileno());need([s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]==before,'open7ID:'+str(p))
  sha=hashlib.file_digest(f,'sha256').hexdigest();s=os.fstat(f.fileno());need([s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]==before==identity(p),'fullEOF7ID:'+str(p))
 return dict(path=str(p),sha256=sha,size_bytes=before[4],identity=before)
def verify(p):
 need(p['path']not in files or files[p['path']]==p,'no PF conflict:'+p['path'])
 if p['path']not in files:
  need(pin(p['path'])==p,'actual fullEOF exact SHA/7ID:'+p['path']);files[p['path']]=p
def read(p):return json.loads(Path(p).read_text())
def bodies(text):return{n.name:ast.get_source_segment(text,n)for n in ast.parse(text).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
inv=read(BASE/'COMPLETE_CURRENT70_CURRENT_MATERIAL_SOURCE_INVERSE.json')
mapping=read(BASE/'EXPLICIT_CURRENT_MATERIAL_ORIGIN_REATTESTATION_SOURCE_ONLY.json')
sf=read(BASE/'COMPLETE_CURRENT_MATERIAL_OBSERVATION_MATH_SOURCE_FREEZE.json')
hf=read(BASE/'COMPLETE_CURRENT_OBSERVATION_BUILD_HOST_SOURCE_FREEZE.json')
phf=read(BASE/'COMPLETE_CURRENT_MATERIAL_OBSERVATION_HOST_SOURCE_FREEZE.json')
esf=read(BASE/'COMPLETE_CURRENT_MATERIAL_EVIDENCE_SOURCE_FREEZE.json')
ehf=read(BASE/'COMPLETE_CURRENT_MATERIAL_EVIDENCE_HOST_SOURCE_FREEZE.json')
cli=read(BASE/'ROOT_REVIEWABLE_CURRENT70_OBSERVER75_STATIC_ARGV_AND_REQUIRED_ACTUAL_GATES_SOURCE_ONLY.json')
cb=read(COMMON/'CURRENT_WARM_A_COMPLETE_HOST_SOURCE_BINDING.json')
catalog=read(cb['current_mount_full_identity_catalog_pin']['path'])
for row in inv['old_frozen_package_fullpins']:verify(row)
for row in mapping['rows']:
 old,now=row['historical_pin'],row['current_pin'];need((old['path'],old['sha256'],old['size_bytes'],old['identity'][1:])==(now['path'],now['sha256'],now['size_bytes'],now['identity'][1:]),'only mount device changed:'+old['path']);need(old['identity'][0]in(16777234,16777229)and now['identity'][0]==16777229,'actual dev29:'+old['path']);verify(now)
for item in inv['entire_byte_copy_pins']:
 verify(item['original']);verify(item['copy']);need(Path(item['original']['path']).read_bytes()==Path(item['copy']['path']).read_bytes(),'entire numeric/original Source bytes identical:'+Path(item['copy']['path']).name)
need(len(inv['entire_byte_copy_pins'])==18,'all eighteen complete numeric Source copies')
for item in inv['changed_Source_full_old_new_bodies']:
 verify(item['old_pin']);verify(item['new_pin']);old=Path(item['old_pin']['path']).read_text();new=Path(item['new_pin']['path']).read_text()
 need(old==item['complete_old_source']and new==item['complete_new_source'],'inverse preserves complete real old/new Source:'+item['name'])
 before,after=bodies(old),bodies(new)
 for name in item['entire_unchanged_function_or_class_names']:need(before[name]==after[name],'entire unchanged scientific/capture/guard body:'+item['name']+'/'+name)
for row in sf['files']+sf['original_math_sources']+sf['complete_math_inverse_proof_pins']+hf['dependencies']+phf['dependencies']+esf['complete_source_file_pins']+ehf['dependencies']+[inv['actual_complete70_origin_pin']]:verify(row)
for row in cb['fixed_current_pins']:verify(row)
for row in catalog['rows']:verify(row['current_pin'])
for p in BASE.glob('*.py'):ast.parse(p.read_text());verify(pin(p))
actual=read(inv['actual_complete70_origin_pin']['path']);ordered=[x for x in actual['records'][-1]['command']if x.endswith(('.o','.a'))]
need(len(ordered)==70 and inv['complete70_order']==ordered,'exact actual complete70 link source')
need(Path(ordered[37]).name=='SPOT_GLOBAL_NATIVE_DRIVER64.o'and Path(ordered[57]).name=='SPOT1P64.o','original driver37 and helper57 exact')
need(len([p for p in ordered if p.endswith('.a')])==4,'same four archives')
at=next(i for i,p in enumerate(ordered)if p.endswith('.a'));need(at==58==inv['observer_insertion_zero_based_index_in70'],'new observer insertion before archive58 after helper57')
expected=ordered[:at]+inv['observer_objects']+ordered[at:]
need(len(expected)==75 and inv['complete75_order']==cli['planned_complete75_link_order']==expected,'all seventy exact inputs plus five ordered observers')
need([p for p in expected if p not in inv['observer_objects']]==ordered,'full original complete70 order retained')
caps=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
need(sf['original_caps']==hf['original_caps']==caps,'all original math/build cap constants unchanged')
compiler=inv['compiler_exact_immutable_role_pin'];verify(compiler);need(compiler==cb['compiler']and compiler['identity'][3]==2,'only exact immutable compiler role link2')
need(all(row['identity'][3]==(2 if row==compiler else 1)for row in files.values()),'other immutable/owned file roles remain link1')
need(cli['is_complete_executable_argv']is False and cli['mandatory_actual_arguments_to_append']==['--aaa3-summary','--aaa3-sha256','--aaa3-seven-id','--saved-audit-summary','--saved-audit-sha256','--saved-audit-seven-id'],'six real prerequisite arguments required no future PF')
for key in ('AAA_qualified','ABA_admitted','goal_complete'):need(sf[key]is False and hf[key]is False and phf[key]is False,'Source does not grant physics:'+key)
gate=(BASE/'current_material_prerequisite_admission.py').read_text();build=(BASE/'build_current_observation_runtime.py').read_text();producer=(BASE/'produce_current_formal_material_observations.py').read_text();evidence=(BASE/'run_current_material_lineage_evidence.py').read_text();common=(COMMON/'guarded_warm_A_common.py').read_text()
for literal in("os.open(path,os.O_RDWR|os.O_NOFOLLOW)","hashlib.file_digest(stream,'sha256').hexdigest()==wanted['sha256']","s.st_nlink==1","stream.seek(0);stream.write(raw);stream.truncate();stream.flush();os.fsync(stream.fileno())"):
 need(literal in gate,'same fd owned failure publication:'+literal)
legacy=Path('/Users/wen/spot/validation/artifacts/axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v8/Root_actual_three_plane_engineering_summary.json')
legacy_pin=pin(legacy);v8=read(legacy);negatives=[(i,r)for i,r in enumerate(v8['records'])if r['status']=='FAILED']
need(negatives and all('log_sha256'not in r for i,r in negatives),'actual old FAILED protocol does not publish PASS-only log_sha256')
need("table[str(lp)]['sha256']==compact['log_sha256']"in gate,'actual faulty unconditional prerequisite key confirmed in current v4')
findings=[dict(priority=1,file=str(BASE/'current_material_prerequisite_admission.py'),problem='Unconditional compact.log_sha256 lookup rejects real intended FAILED records, which lack that PASS-only field.',actual_protocol_evidence_pin=legacy_pin,actual_v8_FAILED_record_count=len(negatives),first_actual_FAILED_record_index=negatives[0][0],first_actual_FAILED_record_keys=list(negatives[0][1]),required_change='Only PASS compares its log_sha256; each intended FAILED must instead bind exact matching actual_operator_refusals.actual_log_pin to output table PF, verify fullEOF and exact expected_abort, retaining real FAILED and complete33 refusal coverage.'),dict(priority=2,files=[str(BASE/'build_current_observation_runtime.py'),str(BASE/'produce_current_formal_material_observations.py'),str(BASE/'run_current_material_lineage_evidence.py')],problem='Final report/manifest paths call Common disk resources.check and SELF check without directly rechecking whole1800 after their last writes/fullEOF.',required_change='Explicitly enforce original whole1800 at each final publication path; preserve same owned fd FAILED publication and all original numeric code/cap constants.')]
report=dict(schema='INDEPENDENT_READONLY_MATERIAL_EXACT_CACHE70_V4_SOURCE_REVIEW_20261013',status='SOURCE_REVIEW_FAILED_REAL_NEGATIVE_GATE_PROTOCOL_AND_FINAL_WHOLE_CAP_GAP_NO_BUSINESS_EXECUTED',successful_checks=len(checks),findings=findings,unique_fullEOF_files=len(files),unique_fullEOF_bytes=sum(p['size_bytes']for p in files.values()),all18_numeric_Source_bytes_preserved=True,complete_original70_order_driver37_helper57_plus_five_observer75_verified=True,all_original_cap_constants_preserved=True,current_identity_reattestation_only_actual_device_changes=True,same_owned_fd_failure_rewrite_source_correct=True,future_v9_or_saved_or_build75_receipt_PF_not_invented=True,candidate_imported_or_executed=False,compiler_or_material_or_parser_business_started=False,Source_v4_business_admission_granted=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,wall_seconds=time.monotonic()-START,SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
p=OUT/'REVIEW.json'
with p.open('x')as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
print(json.dumps(dict(status=report['status'],successful_checks=len(checks),findings=len(findings),fullEOF_unique_files=len(files),fullEOF_unique_bytes=report['unique_fullEOF_bytes'],report_pin=pin(p),candidate_executed=False),allow_nan=False))
raise SystemExit(1)
