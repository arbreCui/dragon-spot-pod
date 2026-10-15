#!/usr/bin/env python3
"""Independent read-only actual model postverification; no business imports or execution."""
import hashlib, json, os, shlex, stat
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
O=Path('/Users/wen/spot/validation/artifacts/axial-material-new-BQ64-private-GANLIB-model-controls-20261013-v5')
D=R/'independent_compact_BQ_model_v5_actual_postverify_20261014'
def seven(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def norm(q):return {k:q[k] for k in ('path','sha256','size_bytes','identity')}
def read(p,expected=None):
 p=Path(p);s=p.lstat();assert stat.S_ISREG(s.st_mode) and not p.is_symlink()
 h=hashlib.sha256();chunks=[]
 fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
 try:
  assert seven(os.fstat(fd))==seven(s)
  while True:
   b=os.read(fd,1024*1024)
   if not b:break
   h.update(b);chunks.append(b)
  assert seven(os.fstat(fd))==seven(s)
 finally:os.close(fd)
 assert seven(p.lstat())==seven(s)
 q=dict(path=str(p),sha256=h.hexdigest(),size_bytes=s.st_size,identity=seven(s))
 if expected is not None:assert q==norm(expected),(str(p),'fullEOF PF mismatch')
 return q,b''.join(chunks)
def load(p,expected=None):
 q,b=read(p,expected);return json.loads(b),q
def current(q):
 s=Path(q['path']).lstat()
 assert stat.S_ISREG(s.st_mode) and not Path(q['path']).is_symlink()
 assert seven(s)==q['identity'] and s.st_size==q['size_bytes'],q['path']
sp,sb=read(O/'Root_actual_control_summary.json')
assert sp['sha256']=='a7724f8d8c9d334cd75a2c2e088269645385ef46d059af74ee9accff1c6b74f1' and sp['size_bytes']==2693213
assert sp['identity']==[16777229,50072317,33188,1,2693213,1791907269514309368,1791907269514309368]
j=json.loads(sb)
tool,tp=load(R/'ROOT_ACTUAL_COMPACT_BQ_PRIVATE_MODEL_V5_TRUE_TOOL_RETURNS_20261013.json')
initial=tool['actual_initial_return'];terminal=tool['actual_terminal_return']
assert initial['chunk_id']=='6556d0' and initial['session_id']==85313
assert terminal['chunk_id']=='557554' and type(terminal['exit_code'])is int and terminal['exit_code']==0 and 'session_id'not in terminal
assert tool['private_model_does_not_qualify_production_reader'] is True and tool['physics_qualified']is False
cli,clip=load(R/'ROOT_EXACT_COMPACT_BQ_MODEL_CONTROLS_V5_ARGV_BOUND_TO_ACTUAL_BUILD_20261013.json')
assert len(cli['argv'])==30 and shlex.split(tool['exact_executed_command'])==cli['argv']
hf,hfp=load(j['actual_host_Source_freeze_pin']['path'],j['actual_host_Source_freeze_pin'])
assert hfp['sha256']=='04d05551c688cee59e421a3f5e2cba9ff1a45905bd4333b1392c2ed60617c269'
hostp,host=read(hf['host_source']['path'],hf['host_source'])
assert hostp['sha256']=='fa55f74e435dae922b131e1d7568385a648f4e1c87432d3d61780176193da886'
plan,planp=load(hf['control_host_plan_pin']['path'],hf['control_host_plan_pin'])
assert planp['sha256']=='11f661579fcca9e35d7849f4dd7a3b8e8b253cc24fb53fb8ae69992d508fbd6d'
sourcep,sourcebytes=read(j['actual_control_Source_pin']['path'],j['actual_control_Source_pin'])
sfp,sfb=read(j['actual_Source_freeze_pin']['path'],j['actual_Source_freeze_pin'])
base,bp=load(j['actual_new_build70_report_pin']['path'],j['actual_new_build70_report_pin'])
assert bp['sha256']=='74197904b3225f511408d609cb087db59ef963fe1162ec8b78c7751e2bdc307f'
newq,newqbytes=read(j['actual_new_BOOTQ_object_pin']['path'],j['actual_new_BOOTQ_object_pin'])
assert newq['sha256'].startswith('1118') and newq in base['output_pins']
assert j['schema']=='ACTUAL_BQ64_PRIVATE_GANLIB_MODEL_GUARDED_CONTROL_REPORT_V1'
assert j['status']=='ACTUAL_PRIVATE_GANLIB_MODEL_CONTROLS_CLOSED0_ONLY'
assert j['failure']is None and j['after_check_error']is None and j['secondary_failures']==[]
assert j['actual_model_controls_passed']is True and j['final_report_resource_check_passed']is True
assert j['compiler_executed']is True and j['synthetic_protocol_fixture_only']is True
assert j['private_model_does_not_independently_qualify_public_reader']is True
for k in ['old17_PASS_inherited','actual_seven_genuine_public_READ_controls_passed','physics_qualified','new_reader_qualified','three_plane_qualified','GLOBAL_qualified','rank_qualified','online_BOOT_qualified','AAA_qualified','ABA_admitted','goal_complete']:
 assert j[k]is False,k
fixed=j['fixed_current_pins'];assert len(fixed)==2610 and len({x['path']for x in fixed})==2610
for q in fixed:current(q)
table={q['path']:norm(q)for q in fixed}
for q in hf['dependencies']+[hf['host_source'],hf['control_host_plan_pin'],j['actual_Source_freeze_pin'],j['actual_new_build70_report_pin'],j['actual_new_BOOTQ_object_pin']]+base['fixed_current_pins']+base['output_pins']:
 assert table.get(q['path'])==norm(q),q['path']
records=j['records'];assert len(records)==3
expected_labels=['build/compile_control','build/link_control','model/run_model']
assert [x['label']for x in records]==expected_labels and all(x['status']=='PASS' for x in records)
assert [x['command']for x in records[:2]]==[j['actual_compile_command'],j['actual_link_command']]
assert records[2]['command']==[str(O/'runtime/control_unqualified')]
stages,stagesp=load(O/'compact-model-controls/stages.json');assert stages['stages']==records
binding,bindingp=load(O/'Root_planned_control_binding.json')
assert binding['fixed_current_pins']==fixed
for k in ['actual_compile_command','actual_link_command','actual_new_build70_report_pin','actual_new_BOOTQ_object_pin','actual_Source_freeze_pin','original_caps','original_aux_cap_bytes','original_pending_metadata_bytes']:
 assert binding[k]==j[k],k
assert binding['control_Source_pin']==j['actual_control_Source_pin']
assert j['logical_control_count']==1 and j['actual_run_phase_count']==1 and len(j['actual_control_results'])==1 and j['actual_stale_host_evidence']==[]
outpins=[]
for q in j['output_pins']:
 p,b=read(q['path'],q);outpins.append(p)
assert len(outpins)==14 and len({x['path']for x in outpins})==14
assert {str(p)for p in O.rglob('*')if p.is_file()}=={q['path']for q in outpins}|{sp['path']}
for p in O.rglob('*'):assert not p.is_symlink()
for q in j['owned_runtime_pins']:
 assert q in j['output_pins'];current(q)
watch_evidence=[]
assert len(j['actual_watchdog_checks'])==3
for rec,reported in zip(records,j['actual_watchdog_checks']):
 wp=O/(rec['label']+'.watchdog.json');w,p=load(wp)
 assert p['sha256']==reported['sha256'] and p['path']==reported['path']
 assert type(w['returncode'])is int and w['returncode']==0 and w['limit_failure']is None
 assert w['command']==rec['command'] and w['rss_cap_mib']==512 and 0<w['wall_cap_seconds']<=600
 assert w['own_child_only']is True and w['liveness_group_cleanup']is True
 assert w['sampled_peak_rss_mib']==reported['peak_rss_mib'] and w['elapsed_seconds']==reported['elapsed_seconds']
 assert 0<=w['sampled_peak_rss_mib']<=512
 lp,lb=read(O/(rec['label']+'.log'));assert lp['sha256']==rec['log_sha256']
 watch_evidence.append(dict(label=rec['label'],watchdog_pin=p,log_pin=lp,genuine_returncode=w['returncode'],limit_failure=w['limit_failure'],sampled_peak_rss_mib=w['sampled_peak_rss_mib'],elapsed_seconds=w['elapsed_seconds']))
result=j['actual_control_results'][0]
assert type(result['actual_model_assertions'])is int and result['actual_model_assertions']==36
logp,logb=read(result['actual_log_pin']['path'],result['actual_log_pin'])
logs=[json.loads(line)for line in logb.decode('utf-8').splitlines()if line.startswith('{')]
assert logs==[result['actual_terminal']]
assert logs[0]['status']=='ACTUAL_COMPACT_GANLIB_MODEL_CONTROLS_ONLY' and type(logs[0]['assertions'])is int and logs[0]['assertions']==36
assert all(logs[0][k]is False for k in ['physics_qualified','reader_qualified','AAA_qualified'])
assert b"if (.not.condition) call XABORT('BQ64 COMPACT CONTROL ASSERTION FAILED.')"in sourcebytes and b'assertions=assertions+1'in sourcebytes
models=[]
for q in result['actual_retained_model_file_pins']:
 p,b=read(q['path'],q);assert p['identity'][3]==1;models.append(p)
assert [x['size_bytes']for x in models]==[948232,954412]
assert models[0]['sha256']=='4a016b672e1c130af270f2218b0ef944ae1c91e342928b094184afc836e269f0'
assert models[1]['sha256']=='fbb861bbc9d75763c2b228edbcc6fde6031481f81804234579efabc83b97b735'
assert models[0]['identity'][:2]!=models[1]['identity'][:2] and all(x['size_bytes']<32*2**20 for x in models)
caps={'original_stage_wall_cap_seconds':600,'whole_wall_cap_seconds':1800,'SELF_and_each_own_child_RSS_cap_bytes':536870912,'threads':1,'children_at_once':1,'retries':0,'fresh_output_cap_bytes':2147483648,'history_cap_bytes':103079215104,'filesystem_floor_bytes':8589934592,'original_cold_reserve_bytes':20971764748}
assert j['original_caps']==caps==hf['original_caps']==plan['original_caps']==base['original_caps']
assert j['original_aux_cap_bytes']==134217728 and j['original_pending_metadata_bytes']==8388608
assert j['original_guard_class']=='OwnRSSSerialExecutor' and j['original_guard_MRO_unchanged']is True
assert j['SELF_peak_bytes']==144637952 and j['SELF_peak_bytes']<536870912 and 0<j['wall_seconds']<1800
observed_resources={}
for name in ['resources_before','resources_after','resources_after_including_summary_bytes']:
 x=j[name];assert x['artifact_budget_bytes']==103079215104 and x['min_free_bytes']==8589934592
 assert x['artifact_bytes']<=103079215104 and x['disk_free_bytes']>=8589934592
 assert x['fresh_output']['artifact_budget_bytes']==2147483648 and x['fresh_output']['artifact_bytes']<=2147483648
 assert x['fresh_output']['resource_roots']==[str(O)]
 if 'control_direct_auxiliary'in x:
  a=x['control_direct_auxiliary'];assert a['cap_bytes']==134217728 and a['pending_bytes']==8388608 and a['auxiliary_bytes']+a['pending_bytes']<=a['cap_bytes']
 observed_resources[name]={k:x.get(k)for k in ['artifact_bytes','regular_files','disk_free_bytes','fresh_output','control_direct_auxiliary']}
total=sum(x['size_bytes']for x in outpins)+sp['size_bytes']
assert total+8388608<=134217728 and total<=2147483648
for q in fixed:current(q)
for q in outpins+[sp,hfp,hostp,planp,sfp,sourcep,bp,newq,tp,clip]:current(q)
report=dict(schema='INDEPENDENT_ACTUAL_COMPACT_BQ_PRIVATE_MODEL_V5_POSTVERIFICATION_V1',status='PASS_ACTUAL_V5_PRIVATE_GANLIB_MODEL_POSTVERIFIED_ONLY',failure=None,
 actual_summary_pin=sp,actual_root_true_tool_return_pin=tp,actual_Root_terminal_return=terminal,actual_Root_initial_return=initial,actual_root_CLI_pin=clip,
 actual_host_freeze_pin=hfp,actual_host_source_pin=hostp,actual_plan_pin=planp,actual_control_source_pin=sourcep,actual_fortran_source_freeze_pin=sfp,
 actual_new_build70_report_pin=bp,actual_new_BOOTQ_object_pin=newq,guarded_stage_count=3,all_actual_stage_statuses=['PASS']*3,stages_pin=stagesp,planned_binding_pin=bindingp,
 watchdog_checks=watch_evidence,actual_model_assertions=36,actual_terminal=logs[0],actual_log_pin=logp,actual_retained_physical_model_file_pins=models,
 physical_file_inventory_full_EOF_verified=True,actual_output_pins=outpins,current_output_file_count=15,current_output_total_bytes=total,
 actual_fixed_current_count=len(fixed),all_current_fixed_all7_reobserved_before_and_after=True,fixed_current_table_canonical_sha256=hashlib.sha256(json.dumps(fixed,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
 fixed_full_EOF_scope='Root genuine guarded before/after check_full_current evidence retained; independent current seven-field comparison of all2610 plus selected metadata/Source/newQ fullEOF; no repeated scientific EOF scan.',
 host_dependencies_count=len(hf['dependencies']),all_host_dependencies_and_actual_new_build_fixed_outputs_exactly_retained=True,
 source_math_guard_oracles_original_unchanged=True,original_caps=caps,original_aux_cap_bytes=134217728,original_pending_metadata_bytes=8388608,
 SELF_peak_bytes=j['SELF_peak_bytes'],wall_seconds=j['wall_seconds'],final_resource_check_passed=True,reported_resource_observations=observed_resources,
 current_final_published_output_bytes_differ_from_earlier_including_summary_check_by=total-j['resources_after_including_summary_bytes']['fresh_output']['artifact_bytes'],
 resource_observation_limitation='Published summary grew after the resource observation; current15-file fullEOF total independently fits fresh2GiB and aux128MiB including pending8MiB. Shared family current totals are not reread during Root public controls.',
 actual_model_controls_passed=True,actual_seven_genuine_public_READ_controls_passed=False,private_model_does_not_independently_qualify_public_reader=True,
 model_is_synthetic_protocol_fixture=True,production_reader_qualified=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,
 independent_postverification_business_executed=False,independent_compiler_executed=False,independent_numerical_executed=False,deletion_executed=False,all_file_descriptors_closed=True,
 caveat='This is the genuine executed private GANLIB model outcome; it is not independent production reader or full pipeline/physics qualification.')
D.mkdir(exist_ok=True)
rp=D/'REVIEW.json'
fd=os.open(rp,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o644)
try:
 payload=(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode();os.write(fd,payload);os.fsync(fd)
finally:os.close(fd)
reviewp,_=read(rp)
print(json.dumps(dict(status=report['status'],review_pin=reviewp,actual_Root_integer_exit_code=terminal['exit_code'],actual_guarded_stage_count=3,actual_model_assertions=36,current_fixed_all7_count=len(fixed),current_output_fullEOF_count=15,private_only=True,all_file_descriptors_closed=True),ensure_ascii=False))
