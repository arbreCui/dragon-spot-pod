#!/usr/bin/env python3
"""Read-only verification of the genuine failed public controls. Never imports business Source."""
import hashlib,json,os,shlex,stat
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
O=Path('/Users/wen/spot/validation/artifacts/axial-material-new-BQ64-genuine-public-READ-seven-controls-20261013-v5')
D=R/'independent_compact_BQ_public_v5_auxiliary128_failure_postverify_20261014'
CAUSE='original remaining runtime/context/log/meta storage planning bound128MiB'
def seven(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def norm(q):return {k:q[k]for k in ('path','sha256','size_bytes','identity')}
def read(p,expected=None,capture=True):
 p=Path(p);s=p.lstat();assert stat.S_ISREG(s.st_mode)and not p.is_symlink()
 h=hashlib.sha256();parts=[];fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
 try:
  assert seven(os.fstat(fd))==seven(s)
  while True:
   b=os.read(fd,1024*1024)
   if not b:break
   h.update(b)
   if capture:parts.append(b)
  assert seven(os.fstat(fd))==seven(s)
 finally:os.close(fd)
 assert seven(p.lstat())==seven(s)
 q=dict(path=str(p),sha256=h.hexdigest(),size_bytes=s.st_size,identity=seven(s))
 if expected is not None:assert q==norm(expected),(str(p),'fullEOF mismatch')
 return q,b''.join(parts)if capture else None
def load(p,expected=None):
 q,b=read(p,expected);return json.loads(b),q
def current(q):
 p=Path(q['path']);s=p.lstat();assert stat.S_ISREG(s.st_mode)and not p.is_symlink()
 assert seven(s)==q['identity']and s.st_size==q['size_bytes'],str(p)
j,sp=load(O/'Root_actual_control_summary.json')
assert sp['sha256']=='c60ae9b8eb0b410fd286e0b93e11dc110b029f69d5a3240b4b23184895d1652e'and sp['size_bytes']==5377582
assert sp['identity']==[16777229,50072524,33188,1,5377582,1791907360247363139,1791907360247363139]
t,tp=load(R/'ROOT_ACTUAL_COMPACT_BQ_PUBLIC_V5_AUXILIARY128_FAILURE_TRUE_TOOL_RETURNS_20261013.json')
i=t['actual_initial_return'];end=t['actual_terminal_return']
assert i['chunk_id']=='abfd87'and i['session_id']==10645
assert end['chunk_id']=='f70e1a'and type(end['exit_code'])is int and end['exit_code']==1 and 'session_id'not in end
assert t['original_auxiliary_cap_bytes']==134217728
for key in ['public_controls_qualified','production_reader_qualified','physics_qualified']:assert t[key]is False
cli,clip=load(R/'ROOT_EXACT_COMPACT_BQ_PUBLIC_CONTROLS_V5_ARGV_BOUND_TO_ACTUAL_BUILD_20261013.json')
assert len(cli['argv'])==30 and shlex.split(t['exact_executed_command'])==cli['argv']
hf,hfp=load(j['actual_host_Source_freeze_pin']['path'],j['actual_host_Source_freeze_pin'])
assert hfp['sha256']=='ddfdd1f10faf646541f6f13b174b71ad6f0d431da0edb3d96a232dd430603345'
hostp,host=read(hf['host_source']['path'],hf['host_source'])
assert hostp['sha256']=='5821c08988fd8f60a9a342ff4c1f5b411e3881420857c2e82a1ec09def754b20'
plan,planp=load(hf['control_host_plan_pin']['path'],hf['control_host_plan_pin'])
sourcep,source=read(j['actual_control_Source_pin']['path'],j['actual_control_Source_pin'])
sf,sfp=load(j['actual_Source_freeze_pin']['path'],j['actual_Source_freeze_pin'])
prod_sfp,_=read(hf['selected_new_Fortran_Source_freeze_pin']['path'],hf['selected_new_Fortran_Source_freeze_pin'])
base,bp=load(j['actual_new_build70_report_pin']['path'],j['actual_new_build70_report_pin'])
assert bp['sha256']=='74197904b3225f511408d609cb087db59ef963fe1162ec8b78c7751e2bdc307f'
newq,_=read(j['actual_new_BOOTQ_object_pin']['path'],j['actual_new_BOOTQ_object_pin'],False)
assert newq['sha256'].startswith('1118')and newq in base['output_pins']
assert j['schema']=='ACTUAL_GENUINE_PUBLIC_READ_COMPACT_BQ_ADMISSION_GUARDED_CONTROL_REPORT_V1'
assert j['status']=='ACTUAL_CONTROL_FAILED_UNQUALIFIED'
assert j['failure']==repr(RuntimeError(CAUSE))and j['after_check_error']==repr(RuntimeError(CAUSE))
assert j['secondary_failures']==[dict(where='after_check',error=repr(RuntimeError(CAUSE))),dict(where='publication',error=repr(RuntimeError(CAUSE)))]
assert j['final_report_resource_check_passed']is False
assert 'self.error=error;self.traceback=error.__traceback__'in host.decode()and 'raise self.error.with_traceback(self.traceback)'in host.decode()
assert 'first.reraise()'in end['output']and 'raise self.error.with_traceback(self.traceback)'in end['output']
assert 'runner.execute' in end['output'] and 'direct_aux_inventory'in end['output']and CAUSE in end['output']
for key in ['actual_model_controls_passed','actual_seven_genuine_public_READ_controls_passed','old17_PASS_inherited','physics_qualified','new_reader_qualified','three_plane_qualified','GLOBAL_qualified','rank_qualified','online_BOOT_qualified','AAA_qualified','ABA_admitted','goal_complete']:
 assert j[key]is False,key
fixed=j['fixed_current_pins'];assert len(fixed)==2622 and len({q['path']for q in fixed})==2622
for q in fixed:current(q)
table={q['path']:norm(q)for q in fixed}
for q in hf['dependencies']+[hf['host_source'],hf['control_host_plan_pin'],j['actual_Source_freeze_pin'],j['actual_new_build70_report_pin'],j['actual_new_BOOTQ_object_pin']]+base['fixed_current_pins']+base['output_pins']:
 assert table.get(q['path'])==norm(q),q['path']
for path in j['actual_link_core_paths']:assert path in table
records=j['records'];assert len(records)==10 and [r['status']for r in records]==['PASS']*9+['FAILED']
expected=['build/compile_control','build/link_control','public_read_positive_all3/control_single','public_read_GLOBAL64_lowbit/control_single','public_read_SEED_lowbit/control_single','public_read_GLOBAL64_extra_inventory/control_single','public_read_SEED_extra_inventory/control_single','public_read_stale_BQ_SRC/control_prepare','public_read_stale_BQ_SRC/control_read','public_read_stale_BQ_MAC/control_prepare']
assert [r['label']for r in records]==expected and records[-1]['error']==CAUSE
raw,rawp=load(O/'compact-public-controls/stages.json');assert raw['stages']==records
assert records[0]['command']==j['actual_compile_command']and records[1]['command']==j['actual_link_command']
binding,bindingp=load(O/'Root_planned_control_binding.json');assert binding['fixed_current_pins']==fixed
for key in ['actual_compile_command','actual_link_command','actual_new_build70_report_pin','actual_new_BOOTQ_object_pin','actual_Source_freeze_pin','original_caps','original_aux_cap_bytes','original_pending_metadata_bytes']:assert binding[key]==j[key],key
outputs=[]
for q in j['output_pins']:
 p,_=read(q['path'],q,False);assert p['identity'][3]==1;outputs.append(p)
assert len(outputs)==30 and len({q['path']for q in outputs})==30
assert {str(p)for p in O.rglob('*')if p.is_file()}=={q['path']for q in outputs}|{sp['path']}
for p in O.rglob('*'):assert not p.is_symlink()
for q in j['owned_runtime_pins']:assert q in j['output_pins'];current(q)
assert len(j['actual_watchdog_checks'])==9
watches=[]
for ix,rec in enumerate(records):
 w,wp=load(O/(rec['label']+'.watchdog.json'))
 assert w['command']==rec['command']and w['rss_cap_mib']==512 and 0<w['wall_cap_seconds']<=600
 assert w['own_child_only']is True and w['liveness_group_cleanup']is True and 0<=w['sampled_peak_rss_mib']<=512
 assert type(w['returncode'])is int and w['returncode']==0
 lp,lb=read(O/(rec['label']+'.log'))
 if ix<9:
  rw=j['actual_watchdog_checks'][ix];assert wp['path']==rw['path']and wp['sha256']==rw['sha256']
  assert w['limit_failure']is None and lp['sha256']==rec['log_sha256']
 else:assert w['limit_failure']==repr(RuntimeError(CAUSE))
 watches.append(dict(label=rec['label'],record_status=rec['status'],watchdog_pin=wp,log_pin=lp,actual_child_returncode=w['returncode'],limit_failure=w['limit_failure'],sampled_peak_rss_mib=w['sampled_peak_rss_mib'],elapsed_seconds=w['elapsed_seconds']))
assert j['logical_control_count']==7 and j['actual_run_phase_count']==9
assert len(j['actual_control_results'])==7 and len(j['actual_stale_host_evidence'])==1
counts=[(3,3,3),(1,1,3),(1,1,3),(1,1,3),(1,1,3),(0,0,6),(1,1,0)]
results=[]
for result,(status,calls,baseline)in zip(j['actual_control_results'],counts):
 lp,lb=read(result['actual_log_pin']['path'],result['actual_log_pin'])
 terminal=json.loads(lb.decode().strip());assert terminal==result['actual_terminal']
 assert terminal['schema']=='GENUINE_PUBLIC_READ_COMPACT_BQ_ADMISSION_CONTROL_V1'
 assert (terminal['actual_public_read_status'],terminal['actual_control_public_read_calls'],terminal['actual_baseline_public_read_calls'])==(status,calls,baseline)
 assert terminal['case']==result['case']and terminal['phase']==result['phase']
 assert terminal['all_actual_assertions_completed']is True and terminal['synthetic_fixture']is True
 for key in ['private_matcher_used_as_assertion_oracle','physics_qualified','reader_qualified','AAA_qualified','ABA_admitted']:assert terminal[key]is False
 results.append(result)
stale=j['actual_stale_host_evidence'][0];assert stale['case']=='public_read_stale_BQ_SRC'
assert stale['actual_bundle_before_pin']==stale['actual_bundle_after_pin']and stale['actual_stale_before_pin']==stale['actual_stale_after_pin']
mf,mfp=load(stale['actual_before_manifest_pin']['path'],stale['actual_before_manifest_pin'])
assert mf['genuine_prepare_child_closed0']is True and mf['actual_bundle_pin']==stale['actual_bundle_before_pin']and mf['actual_stale_pin']==stale['actual_stale_before_pin']
assert mf['actual_prepare_record']==records[7]and stale['actual_read_record']==records[8]
for key in ['actual_two_files_full_EOF_SHA_all7_unchanged','actual_other_BQ_absent','genuine_read_child_closed0']:assert stale[key]is True
assert not (O/'public_read_stale_BQ_SRC/BQ64-MAC-ST').exists()and not(O/'public_read_stale_BQ_MAC/BQ64-SRC-ST').exists()
assert not (O/'public_read_stale_BQ_MAC/Host_independent_stale_before_full_EOF_SHA_all7.json').exists()
assert not (O/'public_read_stale_BQ_MAC/control_read.log').exists()and not(O/'public_read_stale_BQ_MAC/control_read.watchdog.json').exists()
bundles=[q for q in outputs if q['path'].endswith('coherent_complete_context.xsm')]
assert len(bundles)==2 and all(q['size_bytes']==100163528 for q in bundles)and bundles[0]['sha256']==bundles[1]['sha256']=='2ba7398987f21ce747691ca5d635a374e5793ce7f2dbad2a30b1bb827d4c9061'
assert bundles[0]['identity'][:2]!=bundles[1]['identity'][:2]and all(q['identity'][3]==1 for q in bundles)
stale_pins=[q for q in outputs if q['path'].endswith('BQ64-SRC-ST')or q['path'].endswith('BQ64-MAC-ST')]
assert len(stale_pins)==2 and all(q['size_bytes']==820 for q in stale_pins)
lastlog,lastb=read(O/'public_read_stale_BQ_MAC/control_prepare.log');unadmitted=json.loads(lastb.decode().strip())
assert unadmitted['phase']=='prepare'and (unadmitted['actual_public_read_status'],unadmitted['actual_control_public_read_calls'],unadmitted['actual_baseline_public_read_calls'])==(0,0,6)
caps={'original_stage_wall_cap_seconds':600,'whole_wall_cap_seconds':1800,'SELF_and_each_own_child_RSS_cap_bytes':536870912,'threads':1,'children_at_once':1,'retries':0,'fresh_output_cap_bytes':2147483648,'history_cap_bytes':103079215104,'filesystem_floor_bytes':8589934592,'original_cold_reserve_bytes':20971764748}
assert j['original_caps']==caps==hf['original_caps']==plan['original_caps']==base['original_caps']
assert j['original_aux_cap_bytes']==134217728 and j['original_pending_metadata_bytes']==8388608
assert j['original_guard_MRO_unchanged']is True and j['original_guard_class']=='OwnRSSSerialExecutor'
assert j['SELF_peak_bytes']==151486464 and j['SELF_peak_bytes']<536870912 and 0<j['wall_seconds']<1800
total=sum(q['size_bytes']for q in outputs)+sp['size_bytes']
assert total+8388608>134217728 and total<2147483648
assert sum(q['size_bytes']for q in bundles)==200327056 and 200327056>134217728
lastgood=j['resources_after'];assert lastgood['control_direct_auxiliary']['auxiliary_bytes']+8388608<=134217728
assert lastgood['fresh_output']['regular_files']==26
for q in fixed:current(q)
for q in outputs+[sp,tp,clip,hfp,hostp,planp,sourcep,sfp,prod_sfp,bp,newq,mfp]:current(q)
report=dict(schema='INDEPENDENT_ACTUAL_PUBLIC_BQ_V5_AUXILIARY128_FAILURE_POSTVERIFICATION_V1',status='PASS_GENUINE_PUBLIC_V5_FAILED_RUN_POSTVERIFIED_UNQUALIFIED',failure=None,
 actual_run_status=j['status'],actual_run_failure=j['failure'],actual_after_check_error=j['after_check_error'],actual_secondary_failures=j['secondary_failures'],
 actual_summary_pin=sp,actual_root_true_tools_pin=tp,actual_Root_initial_return=i,actual_Root_terminal_return=end,actual_root_CLI_pin=clip,
 actual_host_freeze_pin=hfp,actual_host_source_pin=hostp,actual_plan_pin=planp,actual_control_source_pin=sourcep,actual_control_fortran_source_freeze_pin=sfp,production_fortran_source_freeze_pin=prod_sfp,
 actual_new_build70_report_pin=bp,actual_new_BOOTQ_object_pin=newq,actual_stages_pin=rawp,actual_planned_binding_pin=bindingp,
 actual_record_count=10,actual_PASS_record_count=9,actual_FAILED_record_count=1,actual_last_failed_record_label=expected[-1],
 all_actual_watchdog_records=watches,actual_last_child_returncode=0,actual_last_watch_limit_failure=repr(RuntimeError(CAUSE)),
 last_watch_semantic='Final child returned0 and emitted prepare assertions, but original storage guard recorded non-null limit_failure; Host stageFAILED and RootEXIT1. No manufactured nonzero child exit or kill.',
 Host_admitted_partial_oracle_count=7,Host_admitted_distinct_case_count=6,Host_admitted_partial_actual_results=results,
 unadmitted_failed_MAC_prepare_terminal=unadmitted,unadmitted_failed_MAC_prepare_log_pin=lastlog,
 planned_logical_case_count=7,planned_run_phase_count=9,actual_guarded_run_phase_count=8,missing_MAC_READ_never_executed=True,
 first_stale_bundle_and_sentinel_before_after_all7_fullEOF_unchanged=True,first_stale_before_manifest_pin=mfp,
 first_stale_evidence={k:v for k,v in stale.items()if k!='actual_read_record'},second_stale_before_manifest_absent=True,
 both_physical_context_bundle_fullEOF_pins=bundles,actual_retained_stale_sentinel_pins=stale_pins,
 duplicate_independent_context_bundle_bytes=200327056,auxiliary_cap_causal_overflow_confirmed=True,
 current_output_fullEOF_count=31,current_output_total_bytes=total,actual_output_pins=outputs,
 current_fixed_all7_count=len(fixed),all_current_fixed_all7_reobserved_before_and_after=True,
 fixed_current_table_canonical_sha256=hashlib.sha256(json.dumps(fixed,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
 all_HF_dependencies_and_actual_build_inputs_outputs_exactly_retained=True,host_dependencies_count=len(hf['dependencies']),
 original_caps=caps,original_aux_cap_bytes=134217728,original_pending_metadata_bytes=8388608,SELF_peak_bytes=j['SELF_peak_bytes'],wall_seconds=j['wall_seconds'],
 last_successful_resource_snapshot={k:lastgood[k]for k in ['artifact_bytes','regular_files','disk_free_bytes','fresh_output','control_direct_auxiliary']},
 last_successful_snapshot_not_final_failed_inventory=True,first_exception_object_and_original_traceback_preserved_in_Source_and_true_Root_terminal=True,
 final_report_resource_check_passed=False,all_seven_controls_passed=False,production_reader_qualified=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,
 fixed_fullEOF_limitation='No repeated scientific EOF scan. Root guarded check_full_current genuine before/after evidence and full table remain bound to the summary; all2622 fixed seven fields independently reobserved and selected Source/metadata/newQ fullEOF.',
 original_failed_scene_preserved=True,independent_business_executed=False,independent_compiler_executed=False,independent_numerical_executed=False,deletion_executed=False,all_file_descriptors_closed=True)
D.mkdir(exist_ok=True);path=D/'REVIEW.json';fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o644)
try:
 payload=(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode()
 with os.fdopen(fd,'wb',closefd=False)as f:f.write(payload);f.flush();os.fsync(fd)
finally:os.close(fd)
rp,_=read(path)
print(json.dumps(dict(status=report['status'],review_pin=rp,actual_Root_integer_exit_code=end['exit_code'],actual_record_count=10,actual_PASS_count=9,actual_FAILED_count=1,actual_last_child_returncode=0,actual_limit_failure=repr(RuntimeError(CAUSE)),current_fixed_all7_count=len(fixed),current_output_fullEOF_count=31,all_seven_controls_passed=False,all_file_descriptors_closed=True),ensure_ascii=False))
