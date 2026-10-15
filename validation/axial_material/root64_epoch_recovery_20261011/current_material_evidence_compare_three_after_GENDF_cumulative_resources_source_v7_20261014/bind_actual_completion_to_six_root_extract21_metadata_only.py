"""Metadata-only first-A to extract-request command binding. Never call request main.
Requires seven real authorities; no missing future pin, inferred success or tree read.
"""
import argparse,hashlib,json,os,shlex,stat
from pathlib import Path
REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
M=REC/'current_material_evidence_six_root_validation_scope_source_v1_20261014'
FIRST_CLI=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_formal_short_FIL_A10_closed_capture_continuation_source_v3_20261014/ROOT_REVIEWABLE_EXACT_CLOSED_A10_CONTINUATION_ARGV_20261014.json')
FIRST_HF_PIN={'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_formal_short_FIL_A10_closed_capture_continuation_source_v3_20261014/COMPLETE_SHORT_FIL_A10_CLOSED_CAPTURE_CONTINUATION_HOST_SOURCE_FREEZE.json', 'sha256': '562794d0e41aae8d87efcc7234fde6ab8f2ed9fa5edcf15139f590e4a38a564e', 'size_bytes': 2482295, 'identity': [16777229, 50153616, 33188, 1, 2482295, 1791959291670025650, 1791959291670025650]}
FIRST_CLI_SHA='06b86fddac439e014df6f647665d9e23b0305b1ca52b9c40de70018138f95c81'
DYNAMIC=M/'ROOT_REVIEWABLE_MATERIAL_EVIDENCE_DYNAMIC_INTERFACE_SOURCE_ONLY.json'
DYNAMIC_SHA='REQUIRED_ACTUAL_PUBLISHED_DYNAMIC_FULLPIN'
EXPECTED_NEW_EVIDENCE_HOST_SOURCE_PIN={'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_material_evidence_six_root_validation_scope_source_v1_20261014/run_current_material_lineage_evidence.py', 'sha256': '37320ae4a60bf5a82c40373452e91c8927ad3d0faa1c66112b9c9203de11d338', 'size_bytes': 10095, 'identity': [16777229, 50163316, 33188, 1, 10095, 1791966656399246805, 1791966656399246805]}
REQUEST_BUILDER=M/'prepare_current_material_evidence_requests.py'
REQUEST_BUILDER_SHA='29f946eba64fa0fe24e2a87bb9e730d92bf48bef8d37f612dd3bb83b61875ce0'
OUT_CLI=M/'ROOT_REVIEWABLE_EXACT_EXTRACT_REQUEST_PREPARATION_AFTER_CLOSED_SHORT_FIL_A10_SIX_ROOT_EVIDENCE_ARGV_20261014.json'
POST_SCHEMA='INDEPENDENT_SHORT_FIL_A10_CLOSED_CAPTURE_CONTINUATION_V3_ACTUAL_COMPLETION_POSTVERIFICATION_V1'
POST_STATUS='PASS_ACTUAL_SHORT_FIL_A10_CLOSED_CAPTURE_CONTINUATION_V3_COMPLETION_POSTVERIFICATION'
FUTURE_ACTUAL=dict(A_report=None,A_manifest=None,A_release=None,Root_tools=None,Root_argv=None,post_review=None,post_tools=None,actual_request_pin=None,actual_extract_report_pin=None,actual_aggregate_report_pin=None,actual_GENDF_report_pin=None)
PHYSICS_FALSE=('reaction_multiplicity_qualified','physical_neutron_balance_qualified','coupled_370group_reference_qualified','scientific_accuracy_qualified')
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(path):
 p=Path(path)
 if not p.is_absolute()or '..'in p.parts:raise RuntimeError('absolute canonical metadata path')
 for a in reversed(p.parents):
  if not stat.S_ISDIR(a.lstat().st_mode):raise RuntimeError('ordinary metadata ancestor')
 s=p.lstat()
 if not stat.S_ISREG(s.st_mode)or s.st_size>64*2**20:raise RuntimeError('bounded Source metadata fullEOF only')
 with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb')as f:
  if identity(os.fstat(f.fileno()))!=identity(s):raise RuntimeError('opened7')
  raw=f.read()
  if identity(os.fstat(f.fileno()))!=identity(s):raise RuntimeError('EOF7')
 if identity(p.lstat())!=identity(s):raise RuntimeError('after7')
 return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=identity(s))
def exact(p):
 if pin(p['path'])!=p:raise RuntimeError('metadata complete fullPF')
 return json.loads(Path(p['path']).read_bytes())
def same7(p):
 s=Path(p['path']).lstat()
 if not stat.S_ISREG(s.st_mode)or identity(s)!=p['identity']:raise RuntimeError('explicit live current7 '+p['path'])
def term0(t):
 if type(t.get('exit_code'))is not int or t['exit_code']!=0 or t.get('session_id')is not None or not isinstance(t.get('output'),str):raise RuntimeError('actual original typed terminal0/no session')
def jsonpin(p):return json.dumps(p,separators=(',',':'))
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 roles=('A-report','A-manifest','A-release','Root-tools','Root-argv','post-review','post-tools')
 for role in roles:
  for suffix in('summary','sha256','seven-id'):ap.add_argument('--'+role+'-'+suffix,required=True)
 ap.add_argument('--request-output-dir',required=True);ap.add_argument('--future-host-output-dir',required=True)
 for suffix in('summary','sha256','seven-id'):ap.add_argument('--evidence-dynamic-'+suffix,required=True)
 a=ap.parse_args();pins={}
 for role in roles:
  attr=role.replace('-','_');p=pin(getattr(a,attr+'_summary'))
  if p['sha256']!=getattr(a,attr+'_sha256')or p['identity']!=json.loads(getattr(a,attr+'_seven_id')):raise RuntimeError('required genuine actual authority '+role)
  pins[role]=p
 firstpin=pin(FIRST_CLI);dynamicpin=pin(DYNAMIC);builderpin=pin(REQUEST_BUILDER)
 if firstpin['sha256']!=FIRST_CLI_SHA or dynamicpin['path']!=a.evidence_dynamic_summary or dynamicpin['sha256']!=a.evidence_dynamic_sha256 or dynamicpin['identity']!=json.loads(a.evidence_dynamic_seven_id)or builderpin['sha256']!=REQUEST_BUILDER_SHA:raise RuntimeError('exact immutable published firstA/evidence interfaces and original request Source')
 first=exact(firstpin);dynamic=exact(dynamicpin)
 if first['Host_freeze_pin']!=FIRST_HF_PIN:raise RuntimeError('exact current short FIL v10 ownHF')
 phase=exact(pins['A-report']);manifest=exact(pins['A-manifest']);release=exact(pins['A-release']);root=exact(pins['Root-tools']);ra=exact(pins['Root-argv']);post=exact(pins['post-review']);pt=exact(pins['post-tools'])
 # The actual material producer does not print a report-PF stdout receipt.
 # Its Root terminal remains the original integer object; post and metadata
 # below bind the real report, manifest and release without inventing stdout.
 term0(root['actual_terminal_return'])
 if root['observed_closed']is not True or type(root['original_integer_exit_code'])is not int or root['original_integer_exit_code']!=0 or shlex.split(root['exact_executed_command'])!=ra['exact_argv']or len(ra['exact_argv'])!=62 or ra['exact_argv']!=first['exact_argv']or first['Host_freeze_pin']!=FIRST_HF_PIN or ra['exact_argv'][-2:]!=['--output-dir',first['output_root']]:raise RuntimeError('genuine independent continuation Root0/exact62/publicCLI/HF/output; original A10 remains Root1')
 if post['schema']!=POST_SCHEMA or post['status']!=POST_STATUS or post['failure']is not None or any(post[k]is not False for k in('business_executed','compiler_executed','numerical_executed','files_deleted')):raise RuntimeError('exact independent A post protocol')
 canonical={'actual_report_pin':pins['A-report'],'actual_Host_freeze_pin':first['Host_freeze_pin'],'actual_CLI_pin':firstpin,'actual_Root_true_tool_return_pin':pins['Root-tools'],'actual_Root_argv_pin':pins['Root-argv'],'actual_observation_manifest_pin':pins['A-manifest'],'actual_closed_owned_library_copy_release_pin':pins['A-release']}
 if any(post[k]!=p for k,p in canonical.items()):raise RuntimeError('post canonical five plus genuine manifest and release')
 for key in('actual_review_return','actual_postverification_return'):
  term0(pt[key])
  if json.loads(pt[key]['output'].strip().splitlines()[-1])['review_pin']!=pins['post-review']:raise RuntimeError('genuine independent post stdout exact REVIEW')
 if pt['observed_closed']is not True or type(pt['original_integer_exit_code'])is not int or pt['original_integer_exit_code']!=0:raise RuntimeError('independent observedclosed0')
 out=Path(first['output_root'])
 prior=first['actual_original_authority_pins'];owner=Path(prior['original-phase']['path']).parent
 priorphase=exact(prior['original-phase']);priortools=exact(prior['original-Root-tools']);priorargv=exact(prior['original-Root-argv']);priorcli=exact(prior['original-CLI']);priorpost=exact(prior['failed-post']);priorpt=exact(prior['failed-post-tools'])
 priorcanonical={'actual_report_pin':prior['original-phase'],'actual_Host_freeze_pin':prior['original-host-freeze'],'actual_CLI_pin':prior['original-CLI'],'actual_Root_true_tool_return_pin':prior['original-Root-tools'],'actual_Root_argv_pin':prior['original-Root-argv']}
 q=priortools['actual_terminal_return']
 if priortools['observed_closed']is not True or type(priortools['original_integer_exit_code'])is not int or priortools['original_integer_exit_code']!=1 or type(q['exit_code'])is not int or q['exit_code']!=1 or q.get('session_id')is not None or shlex.split(priortools['exact_executed_command'])!=priorargv['exact_argv']or priorargv['exact_argv']!=priorcli['exact_argv']or len(priorargv['exact_argv'])!=32:raise RuntimeError('original A10 genuine Root1/exact32 retained')
 if priorpost['schema']!='INDEPENDENT_MATERIAL_FIRST_A_SHORT_FIL_V10_ACTUAL_OBSERVATION_POSTVERIFICATION_V1'or priorpost['status']!='PASS_ACTUAL_MATERIAL_FIRST_A_SHORT_FIL_V10_STAGE0_CAPTURE_RELEASE_BLOCKED_FACTUAL_POSTVERIFICATION'or priorpost['failure']is not None or priorpost['actual_material_stage_closed0']is not True or priorpost['actual_stage_statuses']!=['PASS']or priorpost['actual_context_collection_source_function_verified']is not True or any(priorpost[k]!=v for k,v in priorcanonical.items())or any(priorpost[k]is not False for k in('business_executed','compiler_executed','numerical_executed','files_deleted')):raise RuntimeError('exact prior child0 cached collection factual post0; no A10 Root0 claim')
 for k in('actual_review_return','actual_postverification_return'):
  term0(priorpt[k])
  if json.loads(priorpt[k]['output'].strip().splitlines()[-1])['review_pin']!=prior['failed-post']:raise RuntimeError('original factual post0 stdout fullPF')
 if priorpt['observed_closed']is not True or type(priorpt['original_integer_exit_code'])is not int or priorpt['original_integer_exit_code']!=0 or priorphase['status']!='FAILED_CURRENT_OBSERVATION_NO_RETRY'or priorphase['failure']!='RuntimeError: both real process metadata tools fully pinned'or priorphase['actual_closed_owned_library_copy_release_pin']is not None or priorpost['actual_observation_manifest_pin']is not None or priorpost['actual_closed_owned_library_copy_release_pin']is not None:raise RuntimeError('original failed phase and absent manifest/release retained')
 if phase['original_failed_phase_pin']!=prior['original-phase']or phase['original_Root_true_tool_pin']!=prior['original-Root-tools']or phase['original_Root_exit_code_retained']!=1 or phase['original_Root_failure_retained']!=priorphase['failure']or phase['cached_actual_collection_post_pin']!=prior['failed-post']or phase['original_capture_collector_not_reexecuted']is not True or phase['completion_only_existing_closed_stage']is not True or phase['Dragon_or_compiler_or_material_child_launched_by_continuation']is not False or phase['new_scientific_outputs_created']is not False or phase['actual_prior_material_stage_record_reused_wholebytes']is not True or phase['records']!=priorphase['records']or phase['actual_prior_A_cwd']!=str(owner/'A')or phase['original_release_owner_output_root']!=str(owner):raise RuntimeError('new completion has only exact original stage/owner/Source provenance')
 if type(post['actual_Root_integer_exit_code'])is not int or post['actual_Root_integer_exit_code']!=0 or type(post['actual_original_Root_integer_exit_code'])is not int or post['actual_original_Root_integer_exit_code']!=1 or post['actual_material_stage_closed0']is not True or type(post['actual_new_material_child_launch_count'])is not int or post['actual_new_material_child_launch_count']!=0 or post['actual_original_fullfresh2_reserve_admitted']is not True or type(post['actual_fullfresh2_margin_bytes'])is not int or post['actual_fullfresh2_margin_bytes']<=0 or any(post['actual_original_failed_A10_authority_pins'][k]!=v for k,v in priorcanonical.items()):raise RuntimeError('strict separate continuation Root0/post0, original Root1, no new child')
 family=phase['resources_after_full_family'];margin=96*2**30-family['artifact_bytes']-20971764748-64*2**20-2*2**30
 if type(family['artifact_bytes'])is not int or family['artifact_budget_bytes']!=96*2**30 or family['min_free_bytes']!=8*2**30 or family['resource_scope_policy']!='AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1'or margin<=0 or margin!=post['actual_fullfresh2_margin_bytes']or family['disk_free_bytes']-20971764748-2*2**30<8*2**30:raise RuntimeError('actual direct original full-family cold/meta/fresh2/free8 snapshot; no next budget grant')
 if pins['A-report']['path']!=str(out/'Root_actual_material_observation_execution_summary.json')or pins['A-manifest']['path']!=str(out/'ACTUAL_CURRENT_FORMAL_COMPLETE_OBSERVATION_MANIFEST.json')or pins['A-release']['path']!=str(owner/'ACTUAL_CLOSED_OWNED_LIBRARY_COPY_RELEASE.json'):raise RuntimeError('original exact actual A published products')
 if phase['schema']!='ACTUAL_CURRENT_FORMAL_A_MATERIAL_OBSERVATION_EXECUTION_V1'or phase['status']!='ACTUAL_ONE_A_MATERIAL_STAGE_CLOSED0_EVIDENCE_ONLY'or phase['failure']is not None or phase['after_check_error']is not None or phase['actual_full_A_observation_executed']is not True or phase['actual_B_observation_executed']is not False or phase['three_recaptured_plane_histories_claimed']is not False or len(phase['records'])!=1:raise RuntimeError('one actual same-physical A capture, no three histories')
 record=phase['records'][0]
 if record['status']!='PASS'or phase['original_guard_class']!='OwnRSSSerialExecutor'or phase['original_guard_MRO_unchanged']is not True or type(phase['SELF_peak_bytes'])is not int or not 0<=phase['SELF_peak_bytes']<512*2**20 or not 0<phase['wall_seconds']<1800:raise RuntimeError('actual A original own supervisor closure')
 if manifest['schema']!='ACTUAL_CURRENT_FORMAL_COMPLETE_OBSERVATION_MANIFEST_V1'or manifest['state_order']!=['A']or set(manifest['states'])!={'A'}or manifest['observation_scope']!='ONE_SAME_PHYSICAL_A_MATERIAL_CONSTRUCTION_NOT_THREE_HISTORIES'or manifest['current_case_spec_pin']!=phase['current_case_spec_pin']or manifest['actual_observer_build_report_pin']!=phase['actual_observer_build_report_pin']or phase['actual_observer_build_report_pin']!=priorcli['actual_observer75_report_pin']:raise RuntimeError('actual same-case manifest and original build75')
 state=manifest['states']['A']
 if state['actual_owning_report_pin']!=pins['A-report']or state['actual_stage_label']!=record['label']or state['actual_command']!=record['command']or state['actual_genuine_material_stage']!=record or state['actual_cwd']!=str(owner/'A')or state['actual_material_child_closed_before_manifest']is not True or state['all_producer_file_handles_closed_before_next_state']is not True or state['all_actual_events_and_snapshots_saved']is not True:raise RuntimeError('manifest actual one stage origin')
 if manifest['actual_lsof_owner_handle_closure_qualified']is not False:raise RuntimeError('original manifest does not upgrade its lsof qualification flag')
 if any(phase[k]is not False or manifest[k]is not False for k in PHYSICS_FALSE):raise RuntimeError('one A capture cannot mint physics')
 watches=phase['actual_watchdog_checks'];wanted=str(out/(record['label']+'.watchdog.json'))
 if len(watches)!=1 or watches[0]['path']!=wanted:raise RuntimeError('unique actual A watch')
 outputs={p['path']:p for p in phase['output_pins']}
 if wanted not in outputs or outputs[wanted]['sha256']!=watches[0]['sha256']:raise RuntimeError('full watch Source authority')
 watch=exact(outputs[wanted])
 if type(watch['returncode'])is not int or watch['returncode']!=0 or watch['limit_failure']is not None or watch['command']!=record['command']or watch['own_child_only']is not True or watch['liveness_group_cleanup']is not True or type(watch['rss_cap_mib'])is not int or watch['rss_cap_mib']!=512 or not 0<watch['elapsed_seconds']<watch['wall_cap_seconds']<=600 or not 0<=watch['sampled_peak_rss_mib']<512:raise RuntimeError('real A watch0/original caps')
 if phase['actual_closed_owned_library_copy_release_pin']!=pins['A-release']or manifest['actual_closed_owned_library_copy_release_pin']!=pins['A-release']or manifest['shared_copy_pins_are_historical_closed_consumption_not_current_live_inputs']is not True:raise RuntimeError('actual reported release remains explicit historical consumption')
 if release['schema']!='ACTUAL_CLOSED_PRIVATE_MATERIAL_INPUT_COPY_RELEASE_V1'or release['all_owned_copy_paths_absent_after_release']is not True or type(release['total_owned_bytes_released'])is not int or release['total_owned_bytes_released']!=979740136 or release['all_results_contexts_native_observations_retained']is not True or release['actual_closed_stage_records']!=phase['records']:raise RuntimeError('actual original979740136 closed copy lifecycle')
 if release['owned_copy_pins_before_release']!=priorpost['actual_owned_library_copy_pins_current']or manifest['original_failed_phase_pin']!=prior['original-phase']or manifest['original_Root_true_tool_pin']!=prior['original-Root-tools']or manifest['completion_only_original_Root1_preserved']is not True:raise RuntimeError('only exact original private2 retired; original Root1 remains explicit')
 for k,v in priorpost['actual_collected_A_observation_state'].items():
  if k not in('actual_owning_report_pin','actual_stage_label','actual_command')and state[k]!=v:raise RuntimeError('complete cached original collection metadata unchanged '+k)
 originals=release['original_live_input_pins'];released=release['owned_copy_pins_before_release'];shared=manifest['actual_shared_input_library_evidence']
 if list(originals)!=['DLIB_ACTUAL','DLIB8R1_370']or len(released)!=2 or sum(p['size_bytes']for p in released)!=979740136 or shared['original_input_pins']!=originals or list(shared['shared_copy_pins'].values())!=released:raise RuntimeError('only two original shared complete library roles')
 for name,p in zip(originals,released):
  origin=originals[name]
  if p['path']!=str(owner/'s'/dict(DLIB_ACTUAL='A',DLIB8R1_370='B')[name])or p['sha256']!=origin['sha256']or p['size_bytes']!=origin['size_bytes']or p['identity']==origin['identity']or os.path.lexists(p['path']):raise RuntimeError('exact actually released distinct owned copy only')
  same7(origin)
 if any(p['path']in {x['path']for x in released}for p in phase['fixed_current_pins']+phase['owned_input_copy_pins']+phase['output_pins']):raise RuntimeError('no retired copy promoted back to current')
 if type(release['actual_PS_returncode'])is not int or release['actual_PS_returncode']!=0 or type(release['actual_lsof_returncode'])is not int or release['actual_lsof_returncode']!=0 or release['actual_PS_argv']!=['/bin/ps','-axo','pid=,ppid=,pgid=,stat=']:raise RuntimeError('real PS/lsof metadata observations')
 la=release['actual_lsof_argv']
 if len(la)!=7 or la[:6]!=['/usr/sbin/lsof','-nP','-F','pfnsiDt','-a','-p']or not la[6].isdigit():raise RuntimeError('exact original sole owner lsof vector')
 lsof_host_pid=int(la[6]);pids=[int(line[1:])for line in release['actual_lsof_stdout'].splitlines()if line.startswith('p')and line[1:].isdigit()]
 if pids!=[lsof_host_pid]or any(line.startswith('n'+str(owner/'s')+'/')for line in release['actual_lsof_stdout'].splitlines()):raise RuntimeError('full actual sole owner lsof closure')
 psrows=[]
 for line in release['actual_PS_stdout'].splitlines():
  words=line.split()
  if len(words)!=4 or not all(w.isdigit()for w in words[:3]):raise RuntimeError('original complete process census')
  psrows.append([int(w)for w in words[:3]]+[words[3]])
 if any(row[0]==watch['pid']or row[2]==watch['pid']for row in psrows):raise RuntimeError('closed A PID/group not reused')
 live=phase['fixed_current_pins']+phase['output_pins']+state['physical_input_pins']+state['complete_observed_file_pins']+state['actual_material_product_pins']+list(originals.values())
 for p in live:same7(p)
 if dynamic['schema']!='MATERIAL_EVIDENCE_SOURCE_INTERFACE_FUTURE_ACTUAL_REQUEST_REQUIRED_V1'or dynamic['required_actual_prefix']!='request'or dynamic['actual_request_pin']is not None or dynamic['is_complete_executable_argv']is not False or len(dynamic['known_argv_prefix'])!=24:raise RuntimeError('original exact evidence dynamic interface')
 sf=exact(dynamic['selected_source_freeze_pin']);hf=exact(dynamic['selected_host_freeze_pin'])
 if sf['schema']!='COMPLETE_CURRENT_MATERIAL_EVIDENCE_SOURCE_ONLY_FREEZE_V1'or sf['candidate_executed']is not False or hf['host_source']!=dynamic['host_source_pin']or dynamic['selected_source_freeze_pin']['path']!=str(M/'COMPLETE_CURRENT_MATERIAL_EVIDENCE_SOURCE_FREEZE.json')or dynamic['selected_host_freeze_pin']['path']!=str(M/'COMPLETE_CURRENT_MATERIAL_EVIDENCE_HOST_SOURCE_FREEZE.json')or dynamic['host_source_pin']!=EXPECTED_NEW_EVIDENCE_HOST_SOURCE_PIN:raise RuntimeError('immutable original full evidence Source package')
 req=Path(a.request_output_dir);future=Path(a.future_host_output_dir);child=future.with_name(future.name+'-evidence')
 if not req.is_absolute()or req.parent!=REC or req==M or not future.is_absolute()or future.parent!=out.parent or any(os.path.lexists(q)for q in [req,future,child]):raise RuntimeError('three fresh literal future namespaces')
 roots=[str(future),str(child),str(owner),str(Path(dynamic['selected_source_freeze_pin']['path']).parent),str(req),str(out)]
 if len(set(roots))!=6 or any(Path(x).is_relative_to(Path(y))for x in roots for y in roots if x!=y):raise RuntimeError('original five disjoint roles plus retained completion metadata sixth root')
 argv=dynamic['known_argv_prefix'][:11]+[str(REQUEST_BUILDER),'extract','--source-freeze-pin',jsonpin(dynamic['selected_source_freeze_pin']),'--observation-manifest-pin',jsonpin(pins['A-manifest']),'--request-output-dir',str(req),'--future-host-output-dir',str(future)]
 if len(argv)!=21:raise RuntimeError('original request prepare21 argv')
 for p in live:same7(p)
 value=dict(schema='ROOT_REVIEWABLE_EXACT_EXTRACT_REQUEST_PREPARATION_AFTER_CLOSED_SHORT_FIL_A10_SIX_ROOT_EVIDENCE_ARGV_V1',exact_argv=argv,exact_command=shlex.join(argv),request_builder_source_pin=builderpin,published_evidence_dynamic_interface_pin=dynamicpin,actual_A_authority_pins=pins,actual_A_post_canonical_authorities=canonical,request_output_root=str(req),future_evidence_host_output_root=str(future),future_evidence_child_output_root=str(child),original_joint_five_roots=roots[:5],complete_joint_six_roots=roots,exact_retained_completion_metadata_root=str(out),exact_retained_original_observed_root=str(owner),actual_request_pin=None,required_future_actual_request_prefix='request',future_evidence_known_argv_prefix=dynamic['known_argv_prefix'],is_evidence_run_command_complete=False,is_request_preparation_command_complete=True,request_preparer_not_executed=True,extractor_not_executed=True,aggregator_not_executed=True,GENDF_not_executed=True,no_scientific_body_EOF_or_payload_tree_read_by_binder=True,original62fields370_scope_and_five_root2GiB_free8GiB_caps_unchanged=True,original_evidence_child_intentional_exit2_and_FAILED_record_unchanged=True,current_runtime_budget_admission_not_issued_by_this_binder=True,actual_extract_report_pin=None,actual_aggregate_report_pin=None,actual_GENDF_report_pin=None,binder_source_pin=pin(Path(__file__).absolute()),business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False,physics_qualified=False)
 raw=(json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
 with OUT_CLI.open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
 fd=os.open(M,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
 try:os.fsync(fd)
 finally:os.close(fd)
 print(json.dumps({'status':'EXTRACT_REQUEST_PREPARATION21_COMMAND_BOUND_TO_ACTUAL_A_ROOT0_POST0_METADATA_ONLY_NO_REQUEST_OR_EXTRACTION','CLI_pin':pin(OUT_CLI),'actual_argv_count':len(argv),'request_preparer_executed':False,'business_executed':False,'compiler_executed':False,'numerical_executed':False,'files_deleted':False}),flush=True)
if __name__=='__main__':main()

