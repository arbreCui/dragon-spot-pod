"""UNREADY independent metadata post for actual current B55 OVERV controls.

No candidate/helper import, no scientific decoder, no SQL/native tree or numeric
JSONL parsing. Native/oracle/copied scientific words are blindly hashed, never decoded or recomputed.
The exact pre-GEN author freeze is bound below; actual execution remains NULL.
"""
import argparse,hashlib,json,os,resource,shlex,shutil,stat,sys,time
from pathlib import Path
BASE=Path(__file__).absolute().parent;PACKAGE=BASE.parent
ROOT=Path('/Users/wen/spot')
AUTHOR='/root/b_capture_actual_post_source';EXECUTOR='/root/b2_build_source_peer'
EXPECTED_CORE_AUTHOR_FREEZE={'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_full370_real_operator_control_source_v1_20261015/current_B55_OVERV_control_source_v1_UNREADY/AUTHOR_PRE_ROOT_GENERATION_SOURCE_FREEZE.json', 'sha256': '31a6233921a7df703dd715d27296fd432e02f1edf57a71a15186e75203a8e430', 'size_bytes': 11859, 'identity': [16777229, 50871909, 33188, 1, 11859, 1792058881697088763, 1792058881697088763]}
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
FALSE=dict(physics_qualified=False,historical_machine_bit_replay=False,historical_native_RAM_bits_verified=False,original_XSM_memory_bits_verified=False,complete_reaction_authority_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,A_control_reused=False,B_six_phase_construction_completed=False,source_context_issue_resolved=False)
START=time.monotonic()
def need(v,m):
 if type(v)is not bool or not v:raise RuntimeError(m)
def budget():
 need(time.monotonic()-START<600 and resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024)<512*2**20,'metadata post stage600/SELF512')
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p):
 budget();q=Path(p['path']);s=q.lstat()
 need(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and s.st_uid==os.getuid()and s.st_nlink==1 and ids(s)==p['identity']and s.st_size==p['size_bytes']and len(p['identity'])==7 and all(type(x)is int for x in p['identity']),'exact ordinary owned current7')
 return q
def full(p):
 q=current(p);h=hashlib.sha256();n=0
 with q.open('rb')as f:
  need(ids(os.fstat(f.fileno()))==p['identity'],'opened7')
  while b:=f.read(2**20):h.update(b);n+=len(b);budget()
  need(ids(os.fstat(f.fileno()))==p['identity'],'EOF7')
 need(n==p['size_bytes']and h.hexdigest()==p['sha256'],'blind whole-file SHA/length');current(p);return q
def pin(q):
 q=Path(q);s=q.lstat();h=hashlib.sha256()
 with q.open('rb')as f:
  need(ids(os.fstat(f.fileno()))==ids(s),'opened new file7')
  while b:=f.read(2**20):h.update(b);budget()
  need(ids(os.fstat(f.fileno()))==ids(s),'new file EOF7')
 p=dict(path=str(q),sha256=h.hexdigest(),size_bytes=s.st_size,identity=ids(s));current(p);return p
def meta(p):
 need(p['size_bytes']<8*2**20,'only bounded control metadata8MiB is decoded')
 q=full(p);v=json.loads(q.read_bytes());full(p);return v
def genuine(v,key,p,field):
 t=v[key];need(v['observed_closed']is True and type(v['original_integer_exit_code'])is int and v['original_integer_exit_code']==0 and type(t['exit_code'])is int and t['exit_code']==0 and t.get('session_id')is None and json.loads(t['output'].strip().splitlines()[-1])[field]==p,'genuine closed typed0 and exact output artifact PF')
def current_role(p,build):
 budget();q=Path(p['path']);s=q.lstat()
 need(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and ids(s)==p['identity']and s.st_size==p['size_bytes']and len(p['identity'])==7 and all(type(x)is int for x in p['identity']),'same exact inherited current7 without old payload read')
 if p in build['readonly_system_SDK_header_pins']:
  root=Path(build['readonly_system_SDK_root']);rs=root.lstat()
  need(str(root)=='/Library/Developer/CommandLineTools/SDKs/MacOSX27.0.sdk'and stat.S_ISDIR(rs.st_mode)and rs.st_uid==0 and ids(rs)==build['readonly_system_SDK_root_identity']and not any(x.is_symlink()for x in(root,*root.parents))and str(q)in{str(root/'usr/include'/n)for n in('stdio.h','stdlib.h','stdint.h')}and s.st_uid==0 and s.st_nlink==1,'only frozen selected readonly SDK headers current7')
 elif p in build['readonly_system_tool_metadata_pins']:
  need(str(q)in('/bin/ps','/usr/sbin/lsof')and s.st_uid==0 and s.st_nlink==1 and bool(s.st_mode&0o111),'only explicitly frozen readonly PS/lsof roles')
 elif p==build['C_compiler_pin']:
  need(str(q)=='/Library/Developer/CommandLineTools/usr/bin/clang'and s.st_uid==0 and s.st_nlink==1 and bool(s.st_mode&0o111),'only explicit frozen current readonly clang role')
 elif str(q)=='/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15':
  need(p['sha256']=='0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492'and s.st_uid==os.getuid()and s.st_nlink==p['identity'][3]==2,'only original frozen gfortran link exception')
 else:need(s.st_uid==os.getuid()and s.st_nlink==1,'same owned ordinary inherited role')
def all_output_pins(out):
 rows=[]
 if not os.path.lexists(out):return rows
 need(out.is_dir()and not any(x.is_symlink()for x in(out,*out.parents)),'literal fresh current B55 control output')
 for q in sorted(out.rglob('*')):
  s=q.lstat();need(not stat.S_ISLNK(s.st_mode),'no new output alias')
  if stat.S_ISREG(s.st_mode):p=pin(q);full(p);rows.append(p)
  else:need(stat.S_ISDIR(s.st_mode),'ordinary new output files/directories only')
 return rows
def counted_bytes(roots):
 total=0
 for value in roots:
  root=Path(value);need(root.is_absolute()and not any(x.is_symlink()for x in(root,*root.parents)),'literal counted root')
  if not os.path.lexists(root):continue
  need(root.is_dir(),'counted root directory')
  for q in root.rglob('*'):
   budget();s=q.lstat();need(not stat.S_ISLNK(s.st_mode),'no alias in full counted scope')
   if stat.S_ISREG(s.st_mode):total+=s.st_size
 return total
def unlinked_bytes():
 rows={}
 for name in os.listdir('/dev/fd'):
  try:s=os.fstat(int(name))
  except(ValueError,OSError):continue
  if stat.S_ISREG(s.st_mode)and s.st_nlink==0:rows[s.st_dev,s.st_ino]=s.st_size
 return sum(rows.values())
def saved_resources(v,roots,limit):
 h=v['original_history'];j=v['complete_joint']
 need(v['host_SELF_peak_bytes']<512*2**20 and 0<=v['whole_elapsed_seconds']<1800 and v['entire_control_output_bytes']<limit and j['resource_roots']==roots,'actual original SELF/wall/own-stage bound and whole current root scope')
 need(h['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30 and j['artifact_bytes']+v['explicit_external_metadata_bytes']+v['host_open_unlinked_bytes']<2*2**30 and j['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'actual original history/cumulative/cold/metadata/free caps')
def save(report,source_limit,joint_existing=None):
 report.update(metadata_only=True,Source_author_task=AUTHOR,actual_executor_task=EXECUTOR,actual_post_not_executed_by_Source_author=True,reviewer_Source_pin=pin(Path(__file__).absolute()),helper_or_candidate_module_imported=False,Source_GEN_or_publication_executed=False,native_or_compiler_or_worker_executed=False,scientific_values_or_SQLite_or_native_XSM_or_context_body_decoded=False,original_collect_or_snapshot_pair_readback_repeated=False,historical_issue_records_modified=False,wall_seconds=time.monotonic()-START,**FALSE)
 raw=(json.dumps(report,indent=2,allow_nan=False)+'\n').encode();need(len(raw)<6*2**20,'post control report6MiB')
 need(counted_bytes([str(PACKAGE)])+len(raw)<source_limit,'entire Source/metadata bound including new post')
 if joint_existing is not None:need(joint_existing+len(raw)<2*2**30,'entire current cumulative2GiB including post')
 q=BASE/'REVIEW.json'
 with q.open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
 budget();print(json.dumps(dict(status=report['status'],review_pin=pin(q))),flush=True)
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for n in('Root-tools-pin','Host-pin','executor-task-name'):ap.add_argument('--'+n,required=True)
 a=ap.parse_args();need(a.executor_task_name==EXECUTOR and a.executor_task_name!=AUTHOR and not os.path.lexists(BASE/'REVIEW.json'),'exact separate independent executor and once-only immutable post')
 pRoot=json.loads(a.Root_tools_pin);pHost=json.loads(a.Host_pin);raw=meta(pRoot);host=None if pHost is None else meta(pHost);terminal=raw['actual_terminal_return']
 need(raw['observed_closed']is True and type(raw['original_integer_exit_code'])is int and type(terminal['exit_code'])is int and terminal['exit_code']==raw['original_integer_exit_code']and terminal.get('session_id')is None and raw['actual_execution_permission_mode']=='require_escalated'and raw['actual_retried']is False,'genuine closed actual Root integer/PS guard permission/no retry')
 plan_pin=pin(PACKAGE/'PLAN.json')if host is None else host['control_plan_pin'];plan=meta(plan_pin);out=Path(plan['planned_actual_output_root']);roots=plan['complete_joint_roots'];limit=plan['bounded_new_control_output_reservation_bytes'];source_limit=plan['bounded_new_Source_metadata_reservation_bytes']
 need(plan['original_caps']==CAPS and limit==16*2**20 and source_limit==16*2**20 and roots[-1]==str(out)and out.is_absolute(),'original full caps/current complete control16MiB/Source16MiB/owning root')
 if pHost is not None:need(pHost['path']==str(out/'Root_actual_current_B55_OVERV_control_summary.json')and host['schema']=='ACTUAL_CURRENT_B55_OVERV_ORIGINAL_NATIVE_INTEGER_CONTROL_GUARDED_REPORT_V1','actual owning current B55 Host schema/role')
 newpins=all_output_pins(out);table={p['path']:p for p in newpins};ownbytes=sum(p['size_bytes']for p in newpins);code=raw['original_integer_exit_code']
 if code!=0:
  childcodes=[]
  for check in ([]if host is None else host['actual_watchdog_checks']):
   w=meta(check['actual_watchdog_pin']);need(w==check['actual_watchdog']and type(w['returncode'])is int,'only real saved failed-stage typed return retained');childcodes.append(w['returncode'])
   if check['actual_log_pin']is not None:full(check['actual_log_pin'])
  result=dict(schema='CURRENT_B55_OVERV_CONTROL_ACTUAL_FAILURE_FACTS_METADATA_POST_V1',status='PASS_FAILURE_FACTS_ONLY',failure=None,actual_Root_tools_pin=pRoot,actual_Host_report_pin=pHost,actual_Root_integer_exit_code=code,actual_Host_status=None if host is None else host['status'],actual_Host_failure=None if host is None else host['failure'],actual_stage_records=None if host is None else host['records'],actual_recorded_child_integer_exit_codes=childcodes,child_code_inferred_from_Root_return=False,absent_child_code_invented=False,new_partial_output_blind_fullEOF_twice_pins=newpins,control_success_or_word_match_inferred=False,control_plan_pin=plan_pin)
  save(result,source_limit);return
 need(host is not None,'actual Root0 requires exact Host report PF');genuine(raw,'actual_terminal_return',pHost,'report_pin')
 need(host['status']=='ACTUAL_CURRENT_B55_OVERV_NATIVE_INTEGER_CONTROL_CLOSED0_ONLY'and host['failure']is None and host['secondary_failures']==[]and host['final_report_resource_check_passed']is True and host['original_caps']==CAPS and host['original_guard_MRO_unchanged']is True and host['original_guard_class']=='OwnRSSSerialExecutor','actual original guarded current B55 Root0 closure only')
 sf=meta(host['source_freeze_pin']);hf=meta(host['host_freeze_pin']);ready_pin=pin(PACKAGE/'SOURCE_REVIEW_READY.json');ready=meta(ready_pin);core=meta(EXPECTED_CORE_AUTHOR_FREEZE)
 need(core['Source_only_frozen_before_Root_generation']is True and core['whole_Source_file_pins']==sf['complete_source_file_pins'],'same exact author-frozen complete Source table')
 need(sf['schema']=='CURRENT_B55_OVERV_CONTROL_SOURCE_ONLY_FREEZE_V1'and sf['source_only']is True and sf['compiler_executed']is False and sf['native_executed']is False and hf['schema']=='CURRENT_B55_OVERV_CONTROL_HOST_FREEZE_V1'and hf['source_only']is True and hf['compiler_executed']is False and hf['selected_source_freeze_pin']==host['source_freeze_pin']and sf['control_plan_pin']==ready['control_plan_pin']==plan_pin and sf['complete_source_file_pins']==ready['complete_source_file_pins']and hf['host_source_pin']==ready['host_source_pin']and hf['contract_Source_pin']==ready['contract_Source_pin']and sf['original_caps']==hf['original_caps']==CAPS,'same exact current B55 Source/host/contract/plan publication')
 peer=meta(sf['independent_Source_review_pin']);pt=meta(sf['independent_Source_review_tools_pin']);gt=meta(sf['Root_Source_generation_true_tools_pin']);genuine(pt,'actual_review_return',sf['independent_Source_review_pin'],'review_pin');genuine(gt,'actual_Source_preparation_return',ready_pin,'ready_pin')
 need(peer['source_only']is True and peer['status']=='PASS_SOURCE_ONLY_CURRENT_B55_OVERV_CONTROL'and peer['failure']is None and peer['control_plan_pin']==plan_pin and peer['complete_source_file_pins']==sf['complete_source_file_pins'],'genuine current-round complete independent Source review0')
 for p in sf['complete_source_file_pins']:full(p);full(p)
 cli_pin=pin(PACKAGE/'FINAL_ROOT_REVIEWABLE_CLI.json');cli=meta(cli_pin)
 need(shlex.split(raw['exact_executed_command'])==cli['argv']==shlex.split(cli['command'])and len(cli['argv'])==24 and cli['source_freeze_pin']==host['source_freeze_pin']and cli['host_freeze_pin']==host['host_freeze_pin']and cli['Root_actual_exec_command_sandbox_permissions_required']==hf['Root_actual_exec_command_sandbox_permissions_required']=='require_escalated','actual exact published24 Root argv and freeze PFs')
 latest=meta(plan['latest_complete_plan_pin']);binding=meta(plan['actual_B_input_binding_pin']);manifest=meta(plan['actual_B_manifest_pin']);extract=meta(plan['actual_B_extraction_child_report_pin']);eh=meta(plan['actual_B_extraction_Host_report_pin']);ep=meta(plan['actual_B_extraction_post_pin']);er=meta(plan['actual_B_extraction_Root_tools_pin']);et=meta(plan['actual_B_extraction_post_tools_pin']);build=meta(plan['original_guard_build_plan_pin'])
 genuine(er,'actual_terminal_return',plan['actual_B_extraction_Host_report_pin'],'report_pin');genuine(et,'actual_review_return',plan['actual_B_extraction_post_pin'],'review_pin')
 need(eh['status']=='ACTUAL_CURRENT_B_COMPLETE_EXTRACT_EVIDENCE_CHILD2_CLOSED_ONLY'and eh['failure']is None and type(eh['actual_child_integer_exit_code'])is int and eh['actual_child_integer_exit_code']==2 and ep['schema']=='ROOT_ACTUAL_CURRENT_MATERIAL_EXTRACTION_REVIEW_V1'and ep['status']=='PASS_ACTUAL_CURRENT_B_FULL55_CONTEXT8_SNAPSHOT_EXTRACTION_EVIDENCE_CHILD2_METADATA_ONLY'and ep['failure']is None and ep['actual_extraction_report_pin']==plan['actual_B_extraction_child_report_pin']and ep['actual_extraction_host_pin']==plan['actual_B_extraction_Host_report_pin'],'genuine complete B extraction Root0/worker2 and independent actual post0 remain unchanged')
 need(host['complete_joint_roots']==roots==latest['complete_joint_roots']+[str(out)]and roots[:-1][:len(binding['complete_latest_prefix_roots'])+1]==binding['complete_latest_prefix_roots']+[binding['actual_output_root']]and len(roots)==len(set(roots))and all(not Path(x).is_relative_to(Path(y))for x in roots for y in roots if x!=y)and any(PACKAGE.is_relative_to(Path(x))for x in roots[:-1]),'entire dynamic latest extraction/capture/failure prefix plus one distinct control root, Source counted')
 descriptor=host['selected_actual_B55_snapshot_descriptor'];pair=host['selected_actual_B55_SQL_pool_pair']
 need(manifest['state_order']==['B']and set(manifest['states'])=={'B'}and extract['state_order']==['B']and len(extract['states']['B'])==8 and len(extract['context_states']['B'])==55 and descriptor==extract['states']['B'][-1]==plan['selected_actual_B55_snapshot_descriptor']and descriptor['state']=='B'and type(descriptor['event'])is int and descriptor['event']==55 and descriptor['role']=='final-complete-micro'and descriptor['root_prefix']==[]and pair==plan['selected_actual_B55_SQL_pool_pair']==dict(sqlite_pin=descriptor['paired_SQLite_pin'],native_pool_pin=descriptor['paired_original_pool_pin'])and ep['all_snapshot_pairs'][-1]==dict(event=descriptor['event'],role=descriptor['role'],root_prefix=descriptor['root_prefix'],input_pin=descriptor['input_pin'],**pair)and host['actual_B_extraction_report_pin']==plan['actual_B_extraction_child_report_pin']and host['actual_B_extraction_post_pin']==plan['actual_B_extraction_post_pin']and host['actual_B_manifest_pin']==plan['actual_B_manifest_pin']and host['actual_B_input_binding_pin']==plan['actual_B_input_binding_pin'],'only fresh actual B55 pair/manifest/input binding; no inherited A control')
 current(descriptor['paired_SQLite_pin']);current(descriptor['paired_original_pool_pin'])
 records=host['records'];checks=host['actual_watchdog_checks'];need(len(records)==len(checks)==3,'exact three actual original native stages')
 compiler=plan['original_compiler_pin']['path'];obj=str(out/'build/OVERV_control.o');exe=str(out/'runtime/OVERV_control_unqualified');energy=str(out/'input/ENERGY371_original_words.bin');saved=str(out/'input/OVERV370x8_original_words.bin')
 commands=[[compiler,*plan['original_compile_flags'],*plan['original_compile_include_arguments'],'-J'+str(out/'build'),'-c',sf['control_Fortran_Source_pin']['path'],'-o',obj],[compiler,'-O2','-ffp-contract=off',obj,*[p['path']for p in plan['original_four_archive_pins']],'-o',exe],[exe,energy]]
 need(host['actual_compile_command']==commands[0]and host['actual_link_command']==commands[1]and len(plan['original_four_archive_pins'])==4,'actual original compiler/Fortran Source/nine flags/include roles/four archives')
 for record,check,command,label in zip(records,checks,commands,('build/compile_control','build/link_control','control/run_current_control')):
  w=check['actual_watchdog'];need(record['label']==check['actual_stage_record_label']==label and record['status']=='PASS'and record['command']==w['command']==command and type(w['returncode'])is int and w['returncode']==0 and w['limit_failure']is None and w['own_child_only']is True and w['liveness_group_cleanup']is True and w['rss_cap_mib']==512 and 0<=w['sampled_peak_rss_mib']<512 and 0<w['elapsed_seconds']<w['wall_cap_seconds']<=600,'each actual original child0/owned PS/RSS/wall/group closure')
  need(check['actual_watchdog_pin']['path']==str(out/(record['label']+'.watchdog.json'))and check['actual_log_pin']['path']==str(out/(record['label']+'.log'))and check['actual_log_pin']['sha256']==record['log_sha256']and meta(check['actual_watchdog_pin'])==w,'exact original record.label watchdog/log bytes')
  need(table[check['actual_watchdog_pin']['path']]==check['actual_watchdog_pin']and table[check['actual_log_pin']['path']]==check['actual_log_pin'],'all new monitor/log PFs blind SHA twice match')
 actual=host['actual_control_results'];counts=dict(actual_current_energy_words_observed=371,actual_current_overv_words_compared=2960,actual_current_overv_groups=370,actual_current_overv_mixtures=8,actual_native_vs_integer_model_and_saved_word_mismatches=0,actual_constant64_words_compared=3,actual_constant64_word_mismatches=0)
 need(actual['all_three_stages_PASS']is True and actual['all_constant64_and_overv370x8_current_words_match']is True and actual['original_whole_LIBDEN_procedure_executed']is False and all(type(actual[k])is int and actual[k]==v for k,v in counts.items()),'Host saved actual complete371 ENERGY/2960 OVERV/3 constants count and zero word differences, no post array replay')
 need(actual['actual_native_log_pin']==checks[-1]['actual_log_pin']and table[actual['actual_integer_oracle_output_pin']['path']]==actual['actual_integer_oracle_output_pin'],'actual current native/oracle output PFs blind SHA only, rows unparsed')
 small=host['actual_bounded_input_evidence'];rows=small['actual_original_record_metadata'];need(len(rows)==371 and small['actual_payload_bytes_read']==13324 and type(small['actual_payload_bytes_read'])is int and small['complete_SQLite_or_pool_body_EOF_repeated']is False and small['original_XSM_opened']is False and small['energy_path']==energy and small['expected_path']==saved,'actual bounded saved reader copied only13324B, no whole old SQL/pool/XSM read')
 for i,row in enumerate(rows):
  need(row['path']==(['ENERGY']if i==0 else['MACROLIB','GROUP',i,'OVERV'])and row['kind']==2 and row['declared_count']==row['original_word_count']==(371 if i==0 else 8),'all371 original saved record metadata paths/type/count preserved')
 need(table[energy]['size_bytes']==1484 and table[saved]['size_bytes']==11840 and actual['actual_native_log_pin']['path']==str(out/'control/run_current_control.log'),'whole exact newly copied operand sizes; no numeric bytes decoded')
 old_outputs=host['output_pins'];need(len(old_outputs)==len({p['path']for p in old_outputs})and {p['path']for p in newpins}=={p['path']for p in old_outputs}|{pHost['path']},'all whole actual new outputs plus final Host summary retained, no dropped artifact')
 for p in old_outputs+[pHost]:need(table[p['path']]==p,'actual saved output PF equals independent blinded SHA/length7 twice')
 for _ in range(2):
  for p in host['fixed_current_pins']+hf['explicit_cumulative_metadata_file_pins']+plan['inherited_metadata_current7_pins']:current_role(p,build)
  current(descriptor['paired_SQLite_pin']);current(descriptor['paired_original_pool_pin'])
 need(ownbytes<limit,'entire compiler/object/runtime/operands/native/oracle/log/watch/summary control16MiB')
 for key in('resources_before','resources_after','resources_after_including_summary_bytes'):saved_resources(host[key],roots,limit)
 before=host['resources_before'];existing=before['complete_joint']['artifact_bytes']+before['explicit_external_metadata_bytes']+before['host_open_unlinked_bytes'];reservation=host['actual_control_only_stage_reservation']
 need(existing+limit+source_limit<2*2**30 and reservation['complete_joint_roots']==roots and reservation['stage_output_reservations']==dict(B55_OVERV_control=limit)and reservation['Source_metadata_reservation_bytes']==source_limit and reservation['existing_measured_total_bytes']==existing and reservation['only_current_stage']=='B55_OVERV_control'and reservation['original_caps']==CAPS,'actual original full current ledger plus control16/Source16 reservation, no future aggregate budget')
 joint=counted_bytes(roots);extra=sum(p['size_bytes']for p in hf['explicit_cumulative_metadata_file_pins']if not any(Path(p['path']).is_relative_to(Path(r))for r in roots));unlinked=unlinked_bytes();need(joint+extra+unlinked<2*2**30 and shutil.disk_usage(ROOT).free-20971764748-2*2**30>=8*2**30,'current original cumulative/cold/metadata/free caps with own open-unlinked')
 for item in(host,actual):
  for k in FALSE:
   if k in item:need(item[k]is False,'current formula control cannot mint A reuse/historical replay/physics/AAA/ABA/six-phase qualification')
 need(host['original_SOURCE_CONTEXT_NOT_SAVED_issue_not_deleted']is True,'original aggregate SOURCE_CONTEXT_NOT_SAVED history remains immutable')
 result=dict(schema='RECORDED_CURRENT_B55_OVERV_NATIVE_INTEGER_CONTROL_METADATA_POSTVERIFY_V1',status='PASS_ACTUAL_CURRENT_B55_OVERV_THREE_STAGE0_2960_WORDS_MATCH_METADATA_ONLY_NO_PHYSICS_QUALIFICATION',failure=None,actual_Root_tools_pin=pRoot,actual_Host_report_pin=pHost,actual_Root_integer_exit_code=0,actual_child_integer_exit_codes=[w['actual_watchdog']['returncode']for w in checks],actual3_stage_records=records,actual3_watchdog_checks=checks,actual_control_results_metadata=actual,actual_bounded_input_evidence_metadata=small,actual_native_control_log_pin=actual['actual_native_log_pin'],actual_integer_oracle_output_pin=actual['actual_integer_oracle_output_pin'],actual_ENERGY371_owned_copy_pin=table[energy],actual_OVERV370x8_owned_copy_pin=table[saved],actual_control_native_object_pin=table[obj],actual_control_native_executable_pin=table[exe],actual_current_control_word_comparison_counts=counts,all_current_native_vs_integer_model_vs_saved_word_equality_recorded_by_actual_Root=True,native_or_oracle_or_saved_array_equality_recomputed_by_post=False,new_numeric_operand_or_oracle_or_native_log_rows_decoded_by_post=False,actual_guarded_saved_payload_bytes_read=13324,original_large_SQL_pool_or_XSM_opened_by_post=False,actual_B_extraction_report_pin=plan['actual_B_extraction_child_report_pin'],actual_B_extraction_post_pin=plan['actual_B_extraction_post_pin'],actual_B_manifest_pin=plan['actual_B_manifest_pin'],actual_B_input_binding_pin=plan['actual_B_input_binding_pin'],selected_actual_B55_snapshot_descriptor=descriptor,selected_actual_B55_SQL_pool_pair=pair,actual_new_output_blind_fullEOF_SHA_current7_twice_pins=newpins,actual_entire_control_output_bytes=ownbytes,original_SOURCE_CONTEXT_NOT_SAVED_issue_not_deleted=True,original_whole_LIBDEN_procedure_executed=False,current_complete_joint_roots=roots,current_joint_bytes=joint,current_external_metadata_bytes=extra,current_post_open_unlinked_bytes=unlinked,original_caps=CAPS,original_host_resources_before=host['resources_before'],original_host_resources_after=host['resources_after'],original_host_resources_after_including_summary_bytes=host['resources_after_including_summary_bytes'],control_plan_pin=plan_pin,Source_freeze_pin=host['source_freeze_pin'],Host_freeze_pin=host['host_freeze_pin'],actual_CLI_pin=cli_pin,actual_Source_peer_pin=sf['independent_Source_review_pin'],actual_Source_peer_tools_pin=sf['independent_Source_review_tools_pin'],actual_Root_Source_generation_tools_pin=sf['Root_Source_generation_true_tools_pin'],core_Source_author_freeze_pin=EXPECTED_CORE_AUTHOR_FREEZE)
 save(result,source_limit,joint+extra+unlinked)
if __name__=='__main__':main()
