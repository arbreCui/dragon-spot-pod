"""Independent readonly material v6 audit; no import, compile or business run."""
import ast,hashlib,json,os,resource,stat,time
from pathlib import Path
REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
BASE=REC/'current_formal_material_authority_exact_cache70_source_v6'
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

# A Source can be current without inventing an uncompleted business receipt.
handoff_path=REC/'material_exact_cache70_v6_author_finite_source_review_20261013/FINAL_FROZEN_SOURCE_AND_AUTHOR_REVIEW_HANDOFF.json'
handoff=read(handoff_path)
for row in handoff['complete_Source_tree_regular_pins']:verify(row)
verify(hf['required_actual_AAA3_host_freeze_pin'])
need(hf['required_actual_AAA3_host_freeze_pin']['sha256']=='aa75076e2ff7819eb164cecfd927b9485559b2282b0f7ac5ea9c8a5d9ead6861','exact actual v10 Source freeze mandatory')
need(hf['required_actual_AAA3_output_directory'].endswith('-20261012-v10'),'correct future v10 output directory')
need(hf['future_actual_receipts_not_predicted_or_pinned']is True and phf['future_actual75_report_not_predicted_or_pinned']is True,'no predicted future v10/audit/build75 business PF')
for delta_name in ('EXACT_V5_TO_V6_CURRENT_V10_SOURCE_BINDING_BYTE_DELTA.json',):
 delta=read(BASE/delta_name)
 for row in delta['modified_Source_full_old_new']:
  verify(row['old_fullpin']);verify(row['new_fullpin'])
  need(Path(row['old_fullpin']['path']).read_text()==row['complete_old_text']and Path(row['new_fullpin']['path']).read_text()==row['complete_new_text'],'true entire v5/v6 Source byte delta:'+row['name'])
need("refusals={case['original_execution_record_index']:case for case in boot['actual_operator_refusals']}"in gate,'source authority indexes all original refused stages')
need("len(refusals)==33 and set(refusals)=={i for i,r in enumerate(boot['records'])if r['status']=='FAILED'}"in gate,'all33 exact negative-stage index coverage no omissions')
gast=ast.parse(gate);admission=next(n for n in gast.body if isinstance(n,ast.FunctionDef)and n.name=='admit_prerequisites')
log_lookups=[]
for node in ast.walk(admission):
 if isinstance(node,ast.If)and ast.unparse(node.test)=="compact['status'] == 'PASS'":
  then_text='\n'.join(ast.get_source_segment(gate,n)for n in node.body)
  else_text='\n'.join(ast.get_source_segment(gate,n)for n in node.orelse)
  need("compact['log_sha256']"in then_text and "compact['log_sha256']"not in else_text,'PASS-only log digest branch in actual AST')
  need("case['actual_log_pin']==table[str(lp)]"in else_text and "case['actual_watchdog_pin']==table[str(wp)]"in else_text and "case['original_execution_record_label']==compact['label']"in else_text,'FAILED binds exact original log/watch/label fullPF')
  log_lookups.append(node)
need(len(log_lookups)==1,'one exact guarded PASS-only digest lookup')
need(sum(isinstance(n,ast.Subscript)and ast.unparse(n)=="compact['log_sha256']"for n in ast.walk(admission))==1,'no unconditional PASS-only digest field lookup remains')
protocol=[]
for version,wanted in ((8,25),(9,26)):
 rp=Path('/Users/wen/spot/validation/artifacts')/('axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v'+str(version))/'Root_actual_three_plane_engineering_summary.json'
 pp=pin(rp);d=read(rp);authority={p['path']:p for p in d['output_pins']};rows=d['actual_operator_refusals']
 need(len(rows)==wanted,'actual closed prior expected-negative evidence count v'+str(version))
 for case in rows:
  record=d['records'][case['original_execution_record_index']]
  need(record['status']=='FAILED'and 'log_sha256'not in record and record['error']=='own-child stage failed; no retry','actual original FAILED field shape v'+str(version))
  need(record['label']==case['original_execution_record_label'],'actual original negative label v'+str(version))
  lp=case['actual_log_pin'];wp=case['actual_watchdog_pin'];verify(lp);verify(wp)
  need(authority[lp['path']]==lp and authority[wp['path']]==wp,'same exact output authority fullPF v'+str(version))
  watch=read(wp['path'])
  need(watch['returncode']==1 and watch['limit_failure']is None and watch['command']==record['command']and watch['rss_cap_mib']==512 and watch['own_child_only']is True and watch['liveness_group_cleanup']is True,'actual intended exit1 watchdog v'+str(version))
  need(case['actual_abort_message_exact']is True and case['all_actual_assertions_completed']is True and Path(lp['path']).read_text().count(case['expected_abort'])==1,'exact actual component refusal message retained v'+str(version))
 protocol.append(dict(version=version,actual_failed_aggregate_summary_pin=pp,actual_expected_negative_evidence_count=wanted,FAILED_records_did_not_have_PASS_digest_field=True,entire_old_failed_aggregate_does_not_gain_current_business_admission=True))
limits=next(n for n in gast.body if isinstance(n,ast.FunctionDef)and n.name=='check_original_host_limits')
limit_text=ast.get_source_segment(gate,limits)
need('time.monotonic()-start<1800'in limit_text and 'c.resource.getrusage(c.resource.RUSAGE_SELF).ru_maxrss<512*2**20'in limit_text,'genuine final host elapsed and SELF cap guard')
# Verify post-write guards are in the actual catch region that republishes FAILED.
for name,source,write_target in (('build_current_observation_runtime.py',build,'summary'),('run_current_material_lineage_evidence.py',evidence,'summary')):
 tree=ast.parse(source);main=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='main')
 qualifying=[]
 for n in ast.walk(main):
  if isinstance(n,ast.Try):
   body='\n'.join(ast.get_source_segment(source,s)for s in n.body)
   handlers='\n'.join(ast.get_source_segment(source,s)for s in n.handlers)
   if 'check_original_host_limits(c,start)'in body:
    need(body.index('resources.check()')<body.index('check_original_host_limits(c,start)'),'actual final scan before whole/SELF guard:'+name)
    need('replace_owned_failure_summary'in handlers and 'good=False'in handlers,'actual final cap errors republish FAILED same owned fd:'+name)
    qualifying.append(n)
 need(len(qualifying)==1,'one final publication guard region:'+name)
 need(source.index('c.write(summary,report)')<source.index('check_original_host_limits(c,start)',source.index('c.write(summary,report)')),'guard is after actual whole summary write:'+name)
ptree=ast.parse(producer);pmain=next(n for n in ptree.body if isinstance(n,ast.FunctionDef)and n.name=='main')
pbudget=next(n for n in ast.walk(pmain)if isinstance(n,ast.FunctionDef)and n.name=='budget')
need('resources.check();check_original_host_limits(c,start)'in ast.get_source_segment(producer,pbudget),'producer budget rechecks whole/SELF after actual disk scan')
need(producer.index('phase_pin=fullpin(phase)')<producer.index('try:c.check_full_current(fixed,owned);budget()',producer.index('phase_pin=fullpin(phase)')),'actual phase report guarded after publication')
manifest_at=producer.index("c.write(out/'ACTUAL_CURRENT_FORMAL_COMPLETE_OBSERVATION_MANIFEST.json'")
need('try:c.check_full_current(fixed,owned);resources.check();check_original_host_limits(c,start)'in producer[manifest_at:],'actual final manifest write guarded after complete final scan')
need('replace_owned_failure_summary(c,phase,fullpin(phase),failed)'in producer[manifest_at:],'manifest final cap error truthfully revises original owned phase to FAILED')
need(bodies(gate)['replace_owned_failure_summary']==bodies((REC/'current_formal_material_authority_exact_cache70_source_v4/current_material_prerequisite_admission.py').read_text())['replace_owned_failure_summary'],'same owned fd fullEOF/7ID failure rewrite body exact old correct implementation')
# Include all live seven-role material input rows, even when only A will run.
seed=read(BASE/'CURRENT_FORMAL_COMPLETE_AB_ORIGINAL_MATERIAL_SEED_PLAN_SOURCE_ONLY.json')
for state in ('A','B'):
 rows=seed['states'][state]['native_stage_inputs'];need(len(rows)==7,'all seven original material input roles:'+state)
 for row in rows:verify(row['input_pin'])
report=dict(schema='INDEPENDENT_READONLY_MATERIAL_EXACT_CACHE70_V6_COMPLETE_SOURCE_REVIEW_20261013',status='SOURCE_ONLY_COMPLETE_REVIEW_PASS_CONDITIONAL_ON_ROOT_TRUE_V10_AND_SAVED_AUDIT_AND_ACTUAL_GUARDED_TERMINAL',successful_checks=len(checks),findings=[],unique_fullEOF_files=len(files),unique_fullEOF_bytes=sum(p['size_bytes']for p in files.values()),all18_numeric_Source_bytes_preserved=True,complete_original70_order_driver37_helper57_plus_five_observer75_verified=True,all_original_cap_constants_preserved=True,current_identity_reattestation_only_actual_device_changes=True,original_capture_shared_inputs_and_closed_library_lifecycle_function_bodies_byte_exact=True,original_scientific_extract_aggregate_rawcompare_Budget_admit_function_bodies_byte_exact=True,PASS_digest_LOOKUP_only_in_PASS_branch=True,negative33_full_original_index_authority_mandatory=True,actual_closed_old_negative_shape_and_fullEOF_protocol_evidence=protocol,all_three_host_final_publication_paths_actual_whole1800_and_SELF512_enforced=True,same_owned_fd_failure_rewrite_source_byte_exact=True,actual_current_v10_Source_freeze_pin=hf['required_actual_AAA3_host_freeze_pin'],future_v10_or_saved_or_build75_receipt_PF_not_invented=True,candidate_imported_or_executed=False,compiler_or_material_or_parser_business_started=False,Root_true_v10_saved_audit_or_material_business_prerequisites_qualified_by_this_review=False,actual_business_admission_granted=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,Root_independent_main_host_and_actual_terminal_review_required=True,wall_seconds=time.monotonic()-START,SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,final_author_handoff_pin=pin(handoff_path),current_build_host_freeze_pin=pin(BASE/'COMPLETE_CURRENT_OBSERVATION_BUILD_HOST_SOURCE_FREEZE.json'),current_math_source_freeze_pin=pin(BASE/'COMPLETE_CURRENT_MATERIAL_OBSERVATION_MATH_SOURCE_FREEZE.json'),current_producer_host_freeze_pin=pin(BASE/'COMPLETE_CURRENT_MATERIAL_OBSERVATION_HOST_SOURCE_FREEZE.json'),current_static_incomplete_CLI_pin=pin(BASE/'ROOT_REVIEWABLE_CURRENT70_OBSERVER75_STATIC_ARGV_AND_REQUIRED_ACTUAL_GATES_SOURCE_ONLY.json'))
p=OUT/'REVIEW.json'
with p.open('x')as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
print(json.dumps(dict(status=report['status'],successful_checks=len(checks),findings=0,fullEOF_unique_files=len(files),fullEOF_unique_bytes=report['unique_fullEOF_bytes'],report_pin=pin(p),candidate_executed=False),allow_nan=False))
