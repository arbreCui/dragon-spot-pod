"""Frozen independent A2 post; execute only after Root authorizes genuine closure."""
import argparse,hashlib,json,os,resource,shlex,stat,sys,time
from pathlib import Path
BASE=Path(__file__).absolute().parent.parent
OUT=Path(__file__).absolute().parent
START=time.monotonic();WHOLE=[];JSONL_FACTS={}
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2147483648,history_bytes=103079215104,cold_reserve_bytes=20971764748,metadata_reserve_bytes=67108864,free_floor_bytes=8589934592,threads=1,children_at_once=1,retries=0)
ORIGINAL_ISSUE=dict(category='SOURCE_CONTEXT_NOT_SAVED',field='OVERV',reason='DOUBLE sqrt/libm rounded constants require independent model/runtime controls',original_all370x8_words_compared=True,historical_machine_bit_replay=False)
FALSE_KEYS=['original_evaluation_neutron_yield_branch_captured','MF6_GENDF_label_proves_original_processing_branch','MT5_partition_qualified','fission_producer_replayed','reaction_exclusive_partition_qualified','finite18_replayed','temperature_interpolation_replayed','scientific_accuracy_qualified','unreduced_reference_qualified','historical_whole_ASCII_file_reconstruction_qualified','whole_original_NJOY_build_reproduced','current_SPH_MASK_context_applied','physical_neutron_balance_qualified','physics_qualified','historical_machine_bit_replay','historical_native_RAM_bits_verified','original_XSM_memory_bits_verified','complete_reaction_authority_qualified','full_reference_qualified','formal_H150_NZ48_full_controls_qualified','AAA_qualified','ABA_admitted','goal_complete']
def need(v,m):
 if v is not True:raise RuntimeError(m)
def budget():
 peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024)
 need(peak<512*2**20 and time.monotonic()-START<600,'own original SELF512/stage600 post bound')
def ident(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p):
 need(type(p)is dict and type(p['size_bytes'])is int and type(p['identity'])is list and len(p['identity'])==7 and all(type(v)is int for v in p['identity']),'Python integer PF')
 q=Path(p['path']);s=q.lstat();compiler=(str(q)=='/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15'and p['sha256']=='0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492'and s.st_nlink==2)
 need(q.is_absolute()and stat.S_ISREG(s.st_mode)and ident(s)==p['identity']and(s.st_nlink==1 or compiler)and not any(a.is_symlink()for a in(q,*q.parents)),'current7 exact original file/tool role')
 return q

def ownpin(p):
 b=p.read_bytes();s=p.stat();return dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=ident(s))
def blind(p,parse=False,new_output=False):
 q=current(p);need(not parse or p['size_bytes']<8*2**20,'bounded metadata8MiB only')
 if new_output:need(p['size_bytes']<320*2**20,'new output within unchanged320MiB component bound')
 h=hashlib.sha256();n=0;parts=[];lines=0;resolved=0;tail=b'';last=b'';token=b'"category":"SOURCE_CONTEXT_CURRENT_CONTROL_RESOLVED"'
 fd=os.open(q,os.O_RDONLY|os.O_NOFOLLOW)
 try:
  need(ident(os.fstat(fd))==p['identity'],'opened7')
  while True:
   b=os.read(fd,2**20)
   if not b:break
   h.update(b);n+=len(b)
   if parse:parts.append(b)
   if q.suffix=='.jsonl':
    lines+=b.count(b'\n');buf=tail+b;resolved+=buf.count(token);tail=buf[-(len(token)-1):];last=b[-1:]
   budget()
  need(ident(os.fstat(fd))==p['identity'],'EOF7')
 finally:os.close(fd)
 need(n==p['size_bytes']and h.hexdigest()==p['sha256'],'whole Source/meta/new-output byte SHA');current(p);WHOLE.append(p)
 if q.suffix=='.jsonl':
  need(n==0 or last==b'\n','complete JSONL terminal LF');JSONL_FACTS[str(q)]=dict(size_bytes=n,newline_records=lines,resolved_control_metadata_category_occurrences=resolved,JSON_values_decoded=False,numerical_values_recomputed=False)
 return json.loads(b''.join(parts))if parse else None

def closed(wrapper,key,code):
 ret=wrapper[key];need(wrapper['observed_closed']is True and type(wrapper['original_integer_exit_code'])is int and wrapper['original_integer_exit_code']==code and type(ret['exit_code'])is int and ret['exit_code']==code and'session_id'not in ret,'genuine exact closed integer return');return ret

def canonical(rows):return hashlib.sha256(json.dumps(rows,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
def resource_facts(snapshot):
 need(snapshot['host_SELF_peak_bytes']<512*2**20 and 0<=snapshot['whole_elapsed_seconds']<1800,'original host512/1800 observed')
 joint=snapshot['complete_joint'];history=snapshot['original_history'];extra=snapshot['explicit_external_metadata_bytes'];unlinked=snapshot['host_open_unlinked_bytes']
 need(joint['artifact_bytes']+extra+unlinked<2*2**30,'actual full64/external/unlinked cumulative2GiB')
 need(history['artifact_bytes']+20971764748+64*2**20<96*2**30 and joint['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'original history/cold/meta/fresh/free cap arithmetic')

def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 ap.add_argument('--actual-root-tools-pin',required=True);ap.add_argument('--actual-host-report-pin')
 args=ap.parse_args();tools_pin=json.loads(args.actual_root_tools_pin);rootpath=Path(tools_pin['path']);need(rootpath.parent==BASE,'actual Root-tools literal entry scope')
 tools=blind(tools_pin,True);need('actual_terminal_return'in tools and 'actual_execution_permission_mode'in tools,'actual canonical Root keys required, no future output invented')
 ret=tools['actual_terminal_return'];need(type(ret['exit_code'])is int and tools['observed_closed']is True and type(tools['original_integer_exit_code'])is int and tools['original_integer_exit_code']==ret['exit_code']and'session_id'not in ret,'real closed exact Root integer')
 need(tools['actual_execution_permission_mode']=='require_escalated','original actual execution permission role')
 if ret['exit_code']!=0:
  planpin=ownpin(BASE/'PLAN.json');plan=blind(planpin,True);need(len(plan['complete_joint_roots'])==64 and len(set(plan['complete_joint_roots']))==64 and plan['original_caps']==CAPS,'failed A2 exact64/caps unchanged')
  hp=None;host=None;child_code=None;files=[]
  if args.actual_host_report_pin:
   hp=json.loads(args.actual_host_report_pin);host=blind(hp,True);need(host['status']=='FAILED_CURRENT_A_AGGREGATE_AFTER_OVERV_NO_RETRY'and host['current_source_gap_resolved']is False,'only actual failure facts; no success remap')
   child_code=host['actual_child_evidence_only_integer_exit_code'];need(child_code is None or type(child_code)is int,'actual child integer or unknown')
   for p in host['complete_output_pins']:blind(p,new_output=True)
   for row in host['actual_watchdog_checks']:blind(row['actual_watchdog_pin'],True)
   for p in host['fixed_current_pins']+plan['inherited_metadata_current7_pins']:current(p)
   files=host['complete_output_pins']+[hp]
  else:need(not os.path.lexists(Path(plan['planned_actual_output_root'])/'Root_actual_current_A_aggregate_after_OVERV_control_summary.json'),'no omitted existing failed Host report')
  prior=blind(plan['prior_failed_v1_failurefacts_post_pin'],True);prior_tools=blind(plan['prior_failed_v1_failurefacts_post_tools_pin'],True);closed(prior_tools,'actual_review_return',0)
  need(prior['status']=='PASS_FAILURE_FACTS_ONLY'and prior['actual_Root_integer_exit_code']==1 and prior['actual_child_integer_exit_code']==1,'prior v1 failure1 preserved')
  unique={p['path']:p for p in WHOLE}
  for p in unique.values():blind(p,new_output=Path(p['path']).is_relative_to(Path(plan['planned_actual_output_root'])))
  report=dict(schema='INDEPENDENT_CURRENT_A_AGGREGATE_V2_ACTUAL_FAILURE_METADATA_ASSESSMENT_V1',status='PASS_FAILURE_FACTS_ONLY',failure=None,metadata_only=True,actual_Root_tools_pin=tools_pin,actual_Root_return=ret,actual_Root_integer_exit_code=ret['exit_code'],actual_Host_report_pin=hp,actual_child_integer_exit_code=child_code,actual_original_runner_records=None if host is None else host['records'],actual_source_gap_resolved=False,actual_child_report_status_unknown_if_not_present=True,actual_new_output_pins=files,Source_metadata_new_output_blindEOF_pins=list(unique.values()),original_v1_Root1_child1_not_reclassified=True,prior_v1_failurefacts_pin=plan['prior_failed_v1_failurefacts_post_pin'],complete_joint_roots=plan['complete_joint_roots'],original_caps=CAPS,old_science_body_opened=False,old_science_SHA_recomputed=False,numerical_values_recomputed=False,worker_or_helpers_imported=False,business_executed=False,numerical_executed=False,compiler_executed=False,PS_executed=False,files_deleted=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,reviewer_source_pin=ownpin(Path(__file__).absolute()))
  target=OUT/'REVIEW.json';need(not target.exists(),'failurepost once');b=(json.dumps(report,indent=2,allow_nan=False)+'\n').encode();need(len(b)<8*2**20,'post8MiB')
  with target.open('xb')as f:f.write(b)
  print(json.dumps(dict(status=report['status'],review_pin=ownpin(target))),flush=True);return
 ret=closed(tools,'actual_terminal_return',0)
 stdout=json.loads(ret['output'].strip().splitlines()[-1]);hp=stdout['report_pin']
 if args.actual_host_report_pin:need(json.loads(args.actual_host_report_pin)==hp,'actual provided Host PF equals genuine stdout')
 host=blind(hp,True)
 need(host['schema']=='ACTUAL_CURRENT_A_FULL_AGGREGATE_AFTER_OVERV_CONTROL_GUARDED_REPORT_V1'and host['status']==stdout['status']=='ACTUAL_CURRENT_A_FULL_MATH_CONTROL_EVIDENCE_EXIT2_CLOSED_ONLY'and host['failure']is None and host['secondary_failures']==[]and host['current_source_gap_resolved']is True and host['final_report_resource_check_passed']is True,'actual complete current evidence closure only')
 sf=blind(host['source_freeze_pin'],True);hf=blind(host['host_freeze_pin'],True);plan=blind(sf['control_plan_pin'],True)
 need(sf['schema']=='COMPLETE_CURRENT_MATERIAL_EVIDENCE_SOURCE_ONLY_FREEZE_V1'and hf['schema']=='CURRENT_A_AGGREGATE_AFTER_ACTUAL_OVERV_HOST_SOURCE_ONLY_FREEZE_V1'and hf['selected_source_freeze_pin']==host['source_freeze_pin']and hf['original_caps']==plan['original_caps']==host['original_caps']==CAPS,'exact actual SF/HF/PLAN/original caps')
 out=Path(plan['planned_actual_output_root']);need(Path(hp['path'])==out/'Root_actual_current_A_aggregate_after_OVERV_control_summary.json'and len(plan['complete_joint_roots'])==len(set(plan['complete_joint_roots']))==64 and plan['complete_joint_roots'][-1]==str(out),'one new complete64 output namespace')
 inherited_plan=blind(plan['inherited_complete63_plan_pin'],True);need(plan['complete_joint_roots'][:-1]==inherited_plan['complete_joint_roots']and len(inherited_plan['complete_joint_roots'])==63,'whole failed63 prefix preserved plus fresh owningOUT64')
 publication=blind(ownpin(BASE/'FINAL_PUBLICATION_RECEIPT.json'),True);cli=blind(publication['final_CLI_pin'],True)
 need(publication['final_source_freeze_pin']==host['source_freeze_pin']and publication['final_host_freeze_pin']==host['host_freeze_pin']and cli['source_freeze_pin']==host['source_freeze_pin']and cli['host_freeze_pin']==host['host_freeze_pin']and cli['exec_command_sandbox_permissions']=='require_escalated'and cli['planned_actual_output_root']==str(out),'SF/HF/CLI exact same actual publication')
 need(shlex.split(tools['exact_executed_command'])==cli['argv'],'genuine actual exact24 command equals frozen CLI')
 prior_return=blind(plan['prior_failed_v1_Root_true_tools_pin'],True);closed(prior_return,'actual_terminal_return',1)
 prior_fail=blind(plan['prior_failed_v1_failurefacts_post_pin'],True);prior_fail_tools=blind(plan['prior_failed_v1_failurefacts_post_tools_pin'],True);pfr=closed(prior_fail_tools,'actual_review_return',0)
 need(prior_fail['status']=='PASS_FAILURE_FACTS_ONLY'and prior_fail['actual_Root_integer_exit_code']==1 and prior_fail['actual_child_integer_exit_code']==1 and plan['original_failed_v1_not_reclassified_as_success']is True and json.loads(pfr['output'])['review_pin']==plan['prior_failed_v1_failurefacts_post_pin'],'original actual v1 failure spectrum1 retained')
 need(plan['bounded_new_output_reservation_bytes']==320*2**20 and plan['bounded_new_Source_metadata_reservation_bytes']==16*2**20 and plan['host_summary_hard_bound_bytes']==6*2**20 and plan['execution_request_hard_bound_bytes']==4*2**20,'original Source/output hard bounds')
 need(hp['size_bytes']<6*2**20 and host['original_runner_FAILED_record_not_reclassified']is True and host['actual_child_evidence_only_integer_exit_code']==2 and host['old_report_issue1_retained']is True and host['native_engines_started']==0,'Root0 distinct from original engineering child2 and no physics/native execution')
 need(len(host['records'])==1 and len(host['actual_watchdog_checks'])==1,'one original own child; no retry')
 record=host['records'][0];need(record['status']=='FAILED'and record['error']=='own-child stage failed; no retry','original FAILED/error2 never rewritten as PASS')
 wrow=host['actual_watchdog_checks'][0];watch=blind(wrow['actual_watchdog_pin'],True);need(watch==wrow['actual_watchdog']and type(watch['returncode'])is int and watch['returncode']==2 and watch['limit_failure']is None and watch['liveness_group_cleanup']is True and watch['own_child_only']is True and watch['rss_cap_mib']==512 and 0<watch['elapsed_seconds']<watch['wall_cap_seconds']<=600 and 0<=watch['sampled_peak_rss_mib']<512,'original actual watchdog2/resources/liveness')
 need(watch['command']==record['command']and '-B'in watch['command']and'aggregate'in watch['command'],'same original guarded unoptimized child command')
 logpath=out/(record['label']+'.log');lp=next(p for p in host['complete_output_pins']if p['path']==str(logpath));receipt=blind(lp,True)
 need(receipt==host['actual_child_receipt']and receipt['status']=='ACTUAL_COMPLETE_CURRENT_EVIDENCE_ONLY_EXIT2','complete original log receipt2')
 cp=receipt['report'];child=blind(cp,True);need(child==host['actual_evidence']and Path(cp['path']).parent==out/'evidence'and child['schema']=='ACTUAL_COMPLETE_FINAL_MICRO_MACRO_CONSTRUCTION_EVIDENCE_ONLY_V1'and child['status']=='ACTUAL_CURRENT_COMPLETE_ORIGINAL_MATH_CONSTRUCTION_EVIDENCE_ONLY_EXIT2'and child['state_order']==['A']and child['all_complete_state_scope_retained']is True and child['error']is None and len(child['states'])==1,'same full actual A evidence report')
 facts=child['states'][0];need(facts['complete_source_field_comparisons']==19249 and facts['original_context_event_count']==55 and facts['all_original_snapshot_count']==8 and facts['all_mismatching_elements']==0 and facts['all_context_or_operand_issues']==0 and facts['unknown_macro_producers']==0,'actual original full counts and current gap0 only')
 need([p['phase']for p in facts['phase_results']]==['scattering','scalar','fission','extras','overv_fallback','metadata']and all(p['computation_finished']is True for p in facts['phase_results']),'all six phases complete')
 adm=child['current_OVERV_control_admission'];need(facts['current_OVERV_control_admission']==adm and adm['schema']=='CURRENT_A_OVERV_PRIOR_ACTUAL_CONTROL_ADMISSION_V1'and adm['status']=='PRIOR_ACTUAL_CURRENT_OVERV_CONTROL_PREADMITTED_METADATA_ONLY'and adm['original_issue_fact']==ORIGINAL_ISSUE and adm['original_prior_issue_count']==1 and adm['issue_count_adjustment_performed']is False and adm['physics_qualified']is False and adm['historical_machine_bit_replay']is False,'exact current proof admission preserves oldissue1/no counter decrement')
 old_request=blind(plan['original_A_aggregate_request_pin'],True);need(len(old_request['complete_input_pins'])==5937,'all original5937 historical fullPF metadata roles retained')
 old=old_request['aggregation_binding']['actual_context_states']['A'];need(len(old['all_snapshot_pairs'])==8 and len(old['complete_context_pins'])==55 and adm['same_original_final_pair']==old['all_snapshot_pairs'][-1]and len(adm['original_energy_and_overv_record_metadata'])==371,'same8tree/55event/final55/371descriptor scope; no payload decode')
 controlpins=plan['current_OVERV_control_binding']['metadata_pins'];need(adm['control_metadata_pins']==controlpins,'exact original actual control metadata pins')
 control=blind(controlpins['control_report'],True);ct=blind(controlpins['control_returns'],True);post=blind(controlpins['control_post'],True);pt=blind(controlpins['control_post_returns'],True)
 cr=closed(ct,'actual_terminal_return',0);cpr=closed(pt,'actual_review_return',0)
 need(cr['chunk_id']=='fa62fd'and cpr['chunk_id']=='93f79f'and json.loads(cr['output'])['report_pin']==controlpins['control_report']and json.loads(cpr['output'])['review_pin']==controlpins['control_post'],'genuine prior actual control/post0 exact bindings')
 need(control['actual_control_results']['all_three_stages_PASS']is True and control['actual_control_results']['all_constant64_and_overv370x8_current_words_match']is True and post['actual_current_overv_groups']==370 and post['actual_current_overv_mixtures']==8 and post['actual_current_overv_words_compared']==2960 and post['original_SOURCE_CONTEXT_NOT_SAVED_issue_removed']is False,'prior exact OVERV2960 control; old issue1 still preserved')
 original_post=blind(controlpins['prior_aggregate_post'],True);original_report=blind(controlpins['prior_aggregate_report'],True);need(original_post['actual_context_or_operand_issues']==1 and original_report['states'][0]['all_context_or_operand_issues']==1,'original issue1 files remain original facts')
 retirement=blind(plan['actual_literal3_ASCII_retirement_receipt_pin'],True);need(host['actual_literal3_ASCII_retirement_receipt_pin']==plan['actual_literal3_ASCII_retirement_receipt_pin']and retirement['actual_released_bytes']==346861973 and all(not os.path.lexists(p['path'])for p in retirement['actual_released_pins']),'only prior exact3 export retirement remains admitted')
 targetpaths={p['path']for p in retirement['actual_released_pins']};retired_roles=plan['exact_retired_guard_only_input_pins'];need(len(retired_roles)==3 and {p['path']for p in retired_roles}==targetpaths,'only admitted exact3 old guard roles are historical')
 live_rows=[p for p in old_request['complete_input_pins']if p['path']not in targetpaths];need(len(live_rows)==plan['current_live_historical_A_input_count']==5934,'original5937 equals5934 live+3 genuine retired guards')
 for p in live_rows:current(p)
 requestpath=out/'ACTUAL_A_AGGREGATE_EXECUTION_REQUEST.json';requestpin=next(p for p in host['complete_output_pins']if p['path']==str(requestpath));request=blind(requestpin,True)
 need(requestpin['size_bytes']<4*2**20 and request['inherited_prior_request_pin']==plan['original_A_aggregate_request_pin']and request['complete_source_freeze_pin']==host['source_freeze_pin']and request['joint_archive_roots']==plan['complete_joint_roots'],'actual complete execution request route')
 packet=request['historical_complete_input_pins'];need(set(packet)=={'original_request_full_pin','original_member','ordered_fullPF_count','ordered_fullPF_canonical_sha256'}and packet['original_request_full_pin']==plan['original_A_aggregate_request_pin']and packet['original_member']=='complete_input_pins'and packet['ordered_fullPF_count']==5937 and packet['ordered_fullPF_canonical_sha256']==canonical(old_request['complete_input_pins']),'thin5937 exact ordered historical reference metadata')
 requestmap={p['path']:p for p in request['complete_input_pins']};need(len(requestmap)==len(request['complete_input_pins'])==5949 and request['current_live_historical_input_count']==5934 and request['exact_retired_input_pins']==retired_roles and all(requestmap[p['path']]==p for p in live_rows),'5934live plus proofs union5949; no science reopening')
 outputmap={p['path']:p for p in host['complete_output_pins']};need(len(outputmap)==len(host['complete_output_pins']),'no duplicated new output pin')
 scene={str(p)for p in out.rglob('*')if p.is_file()};need(scene==set(outputmap)|{hp['path']},'all new output roles protected plus own Host summary')
 need(sum(Path(p).stat().st_size for p in scene)<320*2**20,'entire actual output below320MiB')
 for p in outputmap.values():need(Path(p['path']).is_relative_to(out),'new output within exact owning scope');blind(p,new_output=True)
 fields=str(out/'evidence/A/complete_field_comparisons.jsonl');mismatch=str(out/'evidence/A/all_numeric_mismatches.jsonl');events=str(out/'evidence/A/all_presence_branch_and_missing.jsonl')
 need(JSONL_FACTS[fields]['newline_records']==19249 and JSONL_FACTS[mismatch]['newline_records']==0 and JSONL_FACTS[events]['resolved_control_metadata_category_occurrences']==1,'new JSONL layout/count and one resolved metadata event; no JSON values decoded')
 for k in FALSE_KEYS:need(host[k]is False,'host remains unqualified '+k)
 for k in ['reaction_multiplicity_qualified','physical_neutron_balance_qualified','coupled_370group_reference_qualified','scientific_accuracy_qualified','AAA_accuracy_qualified','ABA_admitted','goal_complete']:need(child[k]is False,'child remains unqualified '+k)
 need(child['complete_final_construction_qualified']is False and child['new_aggregation_qualification_sha256']is None and child['actual_scientific_qualification_sha256']is None,'no broader construction/scientific qualification minted')
 for snap in [host['resources_before'],host['resources_after'],host['resources_after_including_summary_bytes']]:resource_facts(snap)
 fixed=host['fixed_current_pins'];inherited=plan['inherited_metadata_current7_pins'];need(len({p['path']for p in fixed})==len(fixed),'distinct actual fixed input roles')
 for p in fixed+inherited:current(p)
 unique={p['path']:p for p in WHOLE}
 for p in unique.values():blind(p,new_output=Path(p['path']).is_relative_to(out))
 for p in fixed+inherited:current(p)
 need(all(not os.path.lexists(p['path'])for p in retirement['actual_released_pins']),'retired3 absence verified again')
 report=dict(schema='INDEPENDENT_ACTUAL_CURRENT_A_FULL_AGGREGATE_AFTER_OVERV_METADATA_POSTVERIFY_V1',status='PASS_RECORDED_CURRENT_A_FULL_AGGREGATE_SOURCE_GAP0_METADATA_ONLY_CHILD2_PRESERVED',failure=None,metadata_only=True,actual_Host_report_pin=hp,actual_Root_tools_pin=tools_pin,actual_Root_return=ret,actual_Root_integer_exit_code=0,actual_child_integer_exit_code=2,actual_original_runner_record=record,actual_original_watchdog=watch,original_FAILED_error2_record_retained=True,actual_child_report_pin=cp,complete_phases=facts['phase_results'],actual_compared_source_fields=19249,actual_snapshot_count=8,actual_context_event_count=55,actual_all_mismatch_elements=0,actual_unknown_macro_producers=0,actual_context_or_operand_issues=0,current_source_gap_resolved=True,original_prior_issue1_fact=ORIGINAL_ISSUE,original_prior_issue1_report_pin=controlpins['prior_aggregate_report'],old_issue1_report_not_rewritten=True,original_OVERV_control_Root_return=cr,original_OVERV_control_post_return=cpr,prior_OVERV_compared_words=2960,current_OVERV_control_admission_metadata=adm,historical5937_fullPF_metadata_packet=packet,current_live5934_input_roles_current7_verified_twice=True,actual_execution_request_union_count=5949,old_scientific_payload_current7_only=True,old_scientific_payload_body_opened=False,old_scientific_payload_SHA_recomputed=False,new_output_blind_fullEOF_SHA_verified_twice=True,new_JSONL_values_decoded=False,new_numerical_values_recomputed=False,new_JSONL_layout_facts=JSONL_FACTS,Source_report_and_new_output_fullEOF_pins=list(unique.values()),Source_report_and_new_output_fullEOF_count=len(unique),fixed_current7_role_count=len(fixed),fixed_current7_descriptor_sha256=canonical(fixed),fixed_role_reference='Exact fullPF list remains bound once in immutable Host report.fixed_current_pins',inherited_metadata_current7_role_count=len(inherited),inherited_metadata_descriptor_sha256=canonical(inherited),Source_freeze_pin=host['source_freeze_pin'],Host_freeze_pin=host['host_freeze_pin'],final_CLI_pin=publication['final_CLI_pin'],prior_actual_v1_Root1_child1_preserved=True,prior_v1_failurefacts_post_pin=plan['prior_failed_v1_failurefacts_post_pin'],actual_execution_request_pin=requestpin,actual_literal3_ASCII_retirement_receipt_pin=plan['actual_literal3_ASCII_retirement_receipt_pin'],complete_joint_roots=plan['complete_joint_roots'],original_caps=CAPS,resources_after_including_summary_bytes=host['resources_after_including_summary_bytes'],reviewer_source_pin=ownpin(Path(__file__).absolute()),worker_or_helpers_imported=False,business_executed=False,numerical_executed=False,compiler_executed=False,PS_executed=False,lsof_executed=False,files_deleted=False,physics_qualified=False,complete_reaction_authority_qualified=False,full_reference_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024),wall_seconds=time.monotonic()-START)
 target=OUT/'REVIEW.json';need(not target.exists(),'actual independent post once; no retry');b=(json.dumps(report,indent=2,allow_nan=False)+'\n').encode();need(len(b)<8*2**20,'post report8MiB')
 with target.open('xb')as f:f.write(b)
 print(json.dumps(dict(status=report['status'],review_pin=ownpin(target))),flush=True)
if __name__=='__main__':main()
