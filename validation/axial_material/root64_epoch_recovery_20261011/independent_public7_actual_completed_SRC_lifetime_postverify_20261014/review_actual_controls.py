#!/usr/bin/env python3
"""Independent read-only actual public control/lifetime postverification."""
import hashlib,json,os,shlex,stat
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
O=Path('/Users/wen/spot/validation/artifacts/axial-material-new-BQ64-genuine-public-READ-seven-controls-20261014-v7')
D=R/'independent_public7_actual_completed_SRC_lifetime_postverify_20261014'
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def norm(q):return{k:q[k]for k in('path','sha256','size_bytes','identity')}
def read(p,q=None,capture=True):
 p=Path(p);s=p.lstat();assert stat.S_ISREG(s.st_mode)and not p.is_symlink()
 h=hashlib.sha256();parts=[];fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
 try:
  assert ids(os.fstat(fd))==ids(s)
  while True:
   b=os.read(fd,1048576)
   if not b:break
   h.update(b)
   if capture:parts.append(b)
  assert ids(os.fstat(fd))==ids(s)
 finally:os.close(fd)
 assert ids(p.lstat())==ids(s);pf=dict(path=str(p),sha256=h.hexdigest(),size_bytes=s.st_size,identity=ids(s))
 if q is not None:assert pf==norm(q),(str(p),'fullEOF')
 return b''.join(parts)if capture else None,pf
def load(p,q=None):
 b,pf=read(p,q);return json.loads(b),pf
j,sp=load(O/'Root_actual_control_summary.json');assert sp['sha256']=='97b50c6490f8cea18ee72dea25a9e96d6fc29343c405acd663c033e82374d159'and sp['size_bytes']==8123234
assert sp['identity']==[16777229,50075795,33188,1,8123234,1791910840987681573,1791910840987681573]
tool,tp=load(R/'ROOT_ACTUAL_PUBLIC7_COMPLETED_SRC_LIFETIME_TRUE_TOOL_RETURNS_20261014.json');assert tp['sha256']=='7269d33786602bb42b8ebc3f6b98edaa11b356a2679a0f85722ce85899149b93'
assert tool['observed_closed']is True and type(tool['original_integer_exit_code'])is int and tool['original_integer_exit_code']==0
initial=tool['actual_initial_return'];terminal=tool['actual_terminal_return']
assert initial['chunk_id']=='e74529'and initial['session_id']==46091 and terminal['chunk_id']=='a574a0'and type(terminal['exit_code'])is int and terminal['exit_code']==0 and terminal.get('session_id')is None
cli,clip=load(R/'ROOT_EXACT_COMPACT_BQ_PUBLIC_CONTROLS_V7_ARGV_BOUND_TO_ACTUAL_BUILD_20261014.json')
assert shlex.split(tool['exact_executed_command'])==cli['argv']and len(cli['argv'])==30
assert j['status']=='ACTUAL_SEVEN_GENUINE_PUBLIC_READ_CONTROLS_NINE_PHASES_CLOSED0_ONLY'
assert j['failure']is None and j['after_check_error']is None and j['secondary_failures']==[]
assert j['actual_seven_genuine_public_READ_controls_passed']is True and j['final_report_resource_check_passed']is True
for key in ['actual_model_controls_passed','old17_PASS_inherited','physics_qualified','new_reader_qualified','three_plane_qualified','GLOBAL_qualified','rank_qualified','online_BOOT_qualified','AAA_qualified','ABA_admitted','goal_complete']:assert j[key]is False,key
assert j['compiler_executed']is True and j['synthetic_protocol_fixture_only']is True and j['private_model_does_not_independently_qualify_public_reader']is True
hf,hfp=load(j['actual_host_Source_freeze_pin']['path'],j['actual_host_Source_freeze_pin']);assert hfp['sha256']=='394f0bc9b7b5492bc7465fbfd105ac331f9b6b07c83cc89d4b733312e461b6e6'
_,hostp=read(hf['host_source']['path'],hf['host_source']);plan,planp=load(hf['control_host_plan_pin']['path'],hf['control_host_plan_pin'])
life,lifep=load(hf['selected_completed_first_SRC_bundle_lifetime_Source_plan_pin']['path'],hf['selected_completed_first_SRC_bundle_lifetime_Source_plan_pin'])
base,bp=load(j['actual_new_build70_report_pin']['path'],j['actual_new_build70_report_pin']);assert bp['sha256']=='74197904b3225f511408d609cb087db59ef963fe1162ec8b78c7751e2bdc307f'
_,newq=read(j['actual_new_BOOTQ_object_pin']['path'],j['actual_new_BOOTQ_object_pin'],False);assert newq in base['output_pins']and newq['sha256'].startswith('1118')
assert j['actual_Source_freeze_pin']==hf['selected_control_Source_freeze_pin']and j['actual_control_Source_pin']==plan['control_Source_pin']
fixed=j['fixed_current_pins'];assert len(fixed)==2642 and len({q['path']for q in fixed})==2642
for q in fixed:read(q['path'],q,False)
ft={q['path']:norm(q)for q in fixed}
for q in hf['dependencies']+[hf['host_source'],hfp,planp,j['actual_Source_freeze_pin'],bp,newq]+base['fixed_current_pins']+base['output_pins']:assert ft[q['path']]==norm(q),q['path']
records=j['records'];labels=['build/compile_control','build/link_control','public_read_positive_all3/control_single','public_read_GLOBAL64_lowbit/control_single','public_read_SEED_lowbit/control_single','public_read_GLOBAL64_extra_inventory/control_single','public_read_SEED_extra_inventory/control_single','public_read_stale_BQ_SRC/control_prepare','public_read_stale_BQ_SRC/control_read','public_read_stale_BQ_MAC/control_prepare','public_read_stale_BQ_MAC/control_read']
assert len(records)==11 and [q['label']for q in records]==labels and all(q['status']=='PASS'for q in records)
raw,rawp=load(O/'compact-public-controls/stages.json');assert raw['stages']==records
assert records[0]['command']==j['actual_compile_command']and records[1]['command']==j['actual_link_command']
outputs=[];assert len(j['output_pins'])==34
for q in j['output_pins']:
 _,p=read(q['path'],q,False);assert p['identity'][3]==1;outputs.append(p)
outtable={q['path']:q for q in outputs}
assert len(outtable)==34 and {str(p)for p in O.rglob('*')if p.is_file()}==set(outtable)|{sp['path']}
for p in O.rglob('*'):assert not p.is_symlink()
for q in j['owned_runtime_pins']:assert outtable[q['path']]==q
watches=[];assert len(j['actual_watchdog_checks'])==11
for rec,reported in zip(records,j['actual_watchdog_checks']):
 w,wp=load(O/(rec['label']+'.watchdog.json'));assert wp['sha256']==reported['sha256']and wp['path']==reported['path']
 assert w['command']==rec['command']and type(w['returncode'])is int and w['returncode']==0 and w['limit_failure']is None
 assert w['rss_cap_mib']==512 and 0<w['wall_cap_seconds']<=600 and w['own_child_only']is True and w['liveness_group_cleanup']is True and 0<=w['sampled_peak_rss_mib']<=512
 _,lp=read(O/(rec['label']+'.log'));assert lp['sha256']==rec['log_sha256']
 watches.append(dict(label=rec['label'],watchdog_pin=wp,log_pin=lp,actual_child_integer_returncode=0,limit_failure=None,sampled_peak_rss_mib=w['sampled_peak_rss_mib'],elapsed_seconds=w['elapsed_seconds']))
assert j['logical_control_count']==7 and j['actual_run_phase_count']==9 and len(j['actual_control_results'])==9
counts=[(3,3,3),(1,1,3),(1,1,3),(1,1,3),(1,1,3),(0,0,6),(1,1,0),(0,0,6),(1,1,0)]
actual=j['actual_control_results']
for k,(result,(status,calls,baseline))in enumerate(zip(actual,counts)):
 b,lp=read(result['actual_log_pin']['path'],result['actual_log_pin']);t=json.loads(b.decode().strip())
 assert t==result['actual_terminal']and t['case']==result['case']and t['phase']==result['phase']
 assert t['schema']=='GENUINE_PUBLIC_READ_COMPACT_BQ_ADMISSION_CONTROL_V1'
 for key,value in [('actual_public_read_status',status),('actual_control_public_read_calls',calls),('actual_baseline_public_read_calls',baseline)]:assert type(t[key])is int and t[key]==value
 assert t['all_actual_assertions_completed']is True and t['synthetic_fixture']is True
 for key in ['private_matcher_used_as_assertion_oracle','physics_qualified','reader_qualified','AAA_qualified','ABA_admitted']:assert t[key]is False
 assert result['actual_log_pin']['path']==str(O/(labels[k+2]+'.log'))
assert len({q['case']for q in actual})==7
assert len(j['actual_stale_host_evidence'])==2 and len(j['actual_completed_bundle_retirements'])==1
stale={q['case']:q for q in j['actual_stale_host_evidence']};src=stale['public_read_stale_BQ_SRC'];mac=stale['public_read_stale_BQ_MAC'];event=j['actual_completed_bundle_retirements'][0]
assert src['actual_completed_bundle_retirement']==event and event['case']=='public_read_stale_BQ_SRC'and event['retirement_completed']is True and event['current_bundle_pin']is None
assert event['post_receipt_failure']is None and event['secondary_operation_failures']==[]
intent,intentp=load(event['intent_pin']['path'],event['intent_pin']);receipt,receiptp=load(event['receipt_pin']['path'],event['receipt_pin'])
assert receipt==event['operation']and receipt['schema']=='EXACT_COMPLETED_FIRST_SRC_BUNDLE_RETIREMENT_RECEIPT_V1'
assert receipt['case']=='public_read_stale_BQ_SRC'and receipt['actual_intent_pin']==intentp
assert type(receipt['actual_retired_count'])is int and receipt['actual_retired_count']==1 and receipt['target_uid']==os.getuid()
for key in ['actual_before_equals_after_full_SHA_all7','other_BQ_absent','intent_parent_fsync_attempted','intent_parent_fsync_returned','unlink_attempted','unlink_returned','parent_fsync_attempted','parent_fsync_returned','target_absent_observed','removed_current_owned_fullpin','retirement_completed','retired_bundle_historical_only','no_retry','no_old_v5_file_targeted','receipt_written_before_directory_close_and_any_later_check','directory_close_not_claimed_by_receipt']:assert receipt[key]is True,key
assert receipt['primary_operation_failure']is None and receipt['secondary_operation_failures']==[]and receipt['current_bundle_pin']is None and receipt['physics_qualified']is False
historical=event['historical_bundle_before_pin'];assert historical==event['historical_bundle_after_completed_read_pin']==receipt['exact_retired_bundle_fullpin']==receipt['historical_completed_read_after_fullpin']==src['actual_bundle_before_pin']==src['actual_bundle_after_pin']
assert historical['path']==str(O/'public_read_stale_BQ_SRC/coherent_complete_context.xsm')and historical['size_bytes']==100163528 and historical['identity'][3]==1
assert not os.path.lexists(historical['path'])and historical['path']not in ft and historical['path']not in outtable and historical not in j['owned_runtime_pins']
assert intent['exact_bundle_fullpin']==historical and intent['actual_bundle_after_completed_READ_fullpin']==historical and intent['only_this_exact_bundle_may_be_unlinked']is True and intent['current_owned_target_count']==1
assert src['bundle_lifetime_status']=='RETIRED_AFTER_COMPLETED_READ_BEFORE_SECOND_PREPARE'and src['current_bundle_pin']is None
assert mac['bundle_lifetime_status']=='CURRENT_RETAINED_AFTER_COMPLETED_READ'and mac['current_bundle_pin']==mac['actual_bundle_after_pin']
for evidence,prepare_ix,read_ix,sentinel_name,opposite in [(src,7,8,'BQ64-SRC-ST','BQ64-MAC-ST'),(mac,9,10,'BQ64-MAC-ST','BQ64-SRC-ST')]:
 mf,mfp=load(evidence['actual_before_manifest_pin']['path'],evidence['actual_before_manifest_pin'])
 assert mf['actual_prepare_record']==records[prepare_ix]and evidence['actual_read_record']==records[read_ix]
 assert mf['actual_bundle_pin']==evidence['actual_bundle_before_pin']==evidence['actual_bundle_after_pin']
 assert mf['actual_stale_pin']==evidence['actual_stale_before_pin']==evidence['actual_stale_after_pin']
 for key in ['actual_two_files_full_EOF_SHA_all7_unchanged','actual_other_BQ_absent','genuine_read_child_closed0']:assert evidence[key]is True
 _,stp=read(evidence['actual_stale_after_pin']['path'],evidence['actual_stale_after_pin']);assert stp['size_bytes']==820 and Path(stp['path']).name==sentinel_name
 assert not os.path.lexists(O/evidence['case']/opposite)
 if evidence is mac:
  _,currentmac=read(evidence['current_bundle_pin']['path'],evidence['current_bundle_pin'],False)
  assert currentmac['size_bytes']==100163528 and currentmac['sha256']=='2ba7398987f21ce747691ca5d635a374e5793ce7f2dbad2a30b1bb827d4c9061'
 else:
  assert receipt['actual_before_manifest_pin']==mfp and receipt['actual_prepare_record']==records[prepare_ix]and receipt['actual_completed_read_record']==records[read_ix]and receipt['actual_read_oracle']==actual[6]
  assert intent['actual_prepare_record']==records[prepare_ix]and intent['actual_completed_read_record']==records[read_ix]and intent['actual_read_oracle']==actual[6]
  assert receipt['actual_stale_before_fullpin']==evidence['actual_stale_before_pin']and receipt['actual_stale_after_fullpin']==evidence['actual_stale_after_pin']
a=receipt['parent_before_intent_identity'];b=receipt['parent_before_identity'];c=receipt['parent_after_identity']
assert a[:3]==b[:3]==c[:3]and b[3]==a[3]+1 and b[4]==a[4]+32 and b[5]>=a[5]and b[6]>=a[6]
assert c[3]==b[3]-1 and c[4]==b[4]-32 and c[5]>=b[5]and c[6]>=b[6]
old,oldp=load('/Users/wen/spot/validation/artifacts/axial-material-new-BQ64-genuine-public-READ-seven-controls-20261013-v5/Root_actual_control_summary.json')
assert oldp['sha256']=='c60ae9b8eb0b410fd286e0b93e11dc110b029f69d5a3240b4b23184895d1652e'
oldbundles=[q for q in old['output_pins']if q['path'].endswith('coherent_complete_context.xsm')];assert len(oldbundles)==2
for q in old['output_pins']:read(q['path'],q,False)
assert all(q['size_bytes']==100163528 for q in oldbundles)
caps=dict(original_stage_wall_cap_seconds=600,whole_wall_cap_seconds=1800,SELF_and_each_own_child_RSS_cap_bytes=536870912,threads=1,children_at_once=1,retries=0,fresh_output_cap_bytes=2147483648,history_cap_bytes=103079215104,filesystem_floor_bytes=8589934592,original_cold_reserve_bytes=20971764748)
assert j['original_caps']==caps==hf['original_caps']==plan['original_caps']==base['original_caps']
assert j['original_aux_cap_bytes']==134217728 and j['original_pending_metadata_bytes']==8388608
assert j['original_guard_class']=='OwnRSSSerialExecutor'and j['original_guard_MRO_unchanged']is True
assert j['SELF_peak_bytes']==152698880 and j['SELF_peak_bytes']<536870912 and 0<j['wall_seconds']<1800
total=sum(q['size_bytes']for q in outputs)+sp['size_bytes'];assert total+8388608<=134217728 and total<=2147483648
resource_brief={}
for key in ['resources_before','resources_after','resources_after_including_summary_bytes']:
 v=j[key];assert v['artifact_budget_bytes']==103079215104 and v['min_free_bytes']==8589934592 and v['artifact_bytes']<=103079215104 and v['disk_free_bytes']>=8589934592
 assert v['fresh_output']['artifact_bytes']<=2147483648 and v['fresh_output']['resource_roots']==[str(O)]
 if 'control_direct_auxiliary'in v:assert v['control_direct_auxiliary']['auxiliary_bytes']+8388608<=134217728
 resource_brief[key]={k:v.get(k)for k in ['artifact_bytes','regular_files','disk_free_bytes','fresh_output','control_direct_auxiliary']}
for q in fixed+outputs+[sp,tp,hfp,hostp,planp,lifep,bp,newq,intentp,receiptp,clip,oldp]:assert ids(Path(q['path']).lstat())==q['identity']
assert not os.path.lexists(historical['path'])
report=dict(schema='INDEPENDENT_ACTUAL_PUBLIC7_COMPLETED_SRC_LIFETIME_POSTVERIFICATION_V1',status='PASS_ACTUAL_PUBLIC7_ELEVEN_STAGES_NINE_PHASES_SEVEN_READ_CONTROLS_POSTVERIFIED',failure=None,
 actual_summary_pin=sp,actual_public7_report_pin=sp,actual_Root_true_tool_return_pin=tp,actual_Root_initial_return=initial,actual_Root_terminal_return=terminal,actual_Root_CLI_pin=clip,
 actual_host_Source_freeze_pin=hfp,actual_host_source_pin=hostp,actual_control_host_plan_pin=planp,actual_lifetime_Source_plan_pin=lifep,actual_new_build70_report_pin=bp,actual_new_BOOTQ_object_pin=newq,
 actual_guarded_stage_count=11,actual_all_eleven_stage_statuses=['PASS']*11,actual_stages_pin=rawp,actual_watchdog_checks=watches,logical_control_count=7,actual_run_phase_count=9,actual_control_results=actual,
 actual_seven_genuine_public_READ_controls_passed=True,genuine_public_READ_controls_scope_only=True,all_actual_log_JSON_oracles_strict_status_call_baseline_counts_verified=True,
 actual_completed_bundle_retirement_count=1,actual_retirement_intent_pin=intentp,actual_retirement_receipt_pin=receiptp,actual_retirement_receipt_true_operation_flags={k:v for k,v in receipt.items()if not isinstance(v,(dict,list))},
 historical_completed_SRC_bundle_before_after_equal_fullpin=historical,exact_first_SRC_retired_bundle_current_pin=None,exact_first_SRC_retired_bundle_absent=True,retired_SRC_not_in_current_fixed_owned_or_output_PFs=True,
 first_SRC_before_manifest_sentinel_and_both_logs_current_unchanged=True,MAC_context_bundle_current_fullEOF_pin=currentmac,both_stale_manifests_and_sentinels_fullEOF_current=True,
 SRC_intent_creation_APFS_nlink_plus1_size_plus32_and_times_monotone_verified=True,SRC_unlink_parent_minus1_minus32_verified=True,retirement_parent_before_intent_identity=a,retirement_parent_before_identity=b,retirement_parent_after_identity=c,
 no_first_or_secondary_retirement_exception=True,old_failed_public5_summary_pin=oldp,old_failed_public5_both_bundle_current_fullEOF_pins_preserved=oldbundles,old_failed_public5_all30_outputs_fullEOF_unchanged=True,
 all2642_current_fixed_pins_independent_fullEOF_SHA_all7=True,current_fixed_count=2642,all_current_HF2629_and_actual_build_fixed_outputs_retained=True,
 actual_output_pins=outputs,independent_all34_output_fullEOF_SHA_all7_verified=True,actual_current_output_file_count=35,actual_current_output_total_bytes=total,
 original_caps=caps,original_aux_bytes=134217728,original_pending_bytes=8388608,SELF_peak_bytes=j['SELF_peak_bytes'],wall_seconds=j['wall_seconds'],final_resource_check_passed=True,actual_reported_resources=resource_brief,
 current_published_bytes_minus_earlier_including_summary_observation=total-j['resources_after_including_summary_bytes']['fresh_output']['artifact_bytes'],
 qualification_scope='Genuine executed seven public READ controls on the fixed synthetic protocol fixture. Complete production pipeline and physics qualification are not inherited.',
 production_reader_qualified=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,
 independent_business_executed=False,independent_compiler_executed=False,independent_numerical_executed=False,independent_deletion_executed=False,all_file_descriptors_closed=True,
 downstream_v15_requires_exact_SRC_only_retired_admission_not_generic_missing_skip=True)
D.mkdir(exist_ok=True);p=D/'REVIEW.json';fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o644)
try:
 b=(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode();assert os.write(fd,b)==len(b);os.fsync(fd)
finally:os.close(fd)
_,qp=read(p);print(json.dumps(dict(status=report['status'],review_pin=qp,actual_guarded_stage_count=11,logical_control_count=7,actual_run_phase_count=9,sole_SRC_retirement_count=1,current_fixed_independent_fullEOF_count=2642,current_output_fullEOF_count=35,old_public5_preserved=True,all_file_descriptors_closed=True)))
