"""UNREADY aggregate-only Source/control contract; no worker or decoder on import."""
import hashlib,importlib.util,json,os,stat,sys
from pathlib import Path
R=Path('/Users/wen/spot');BASE=Path(__file__).absolute().parent
IO=BASE.parent/'current_extra_reaction_source_v2/B_only_observer_IO_source_v1'
OUT=R/'validation/artifacts/axial-material-current-B-complete-sixphase-aggregate-after-B55-and-exactB4-retirement-20261015-v1'
OUTPUT_BOUND=320*2**20;SOURCE_BOUND=16*2**20
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
FALSE=dict(historical_native_RAM_bits_verified=False,original_XSM_memory_bits_verified=False,historical_unsaved_context_recovered=False,reaction_multiplicity_qualified=False,TRANC_semantics_qualified=False,physical_neutron_balance_qualified=False,coupled_370group_reference_qualified=False,scientific_accuracy_qualified=False,AAA_accuracy_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,physics_qualified=False)
def need(v,m):
 if v is not True:raise RuntimeError(m)
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p):
 q=Path(p['path']);s=q.lstat();need(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and s.st_nlink==1 and identity(s)==p['identity']and s.st_size==p['size_bytes'],'exact ordinary Source/control/input current7');return q
def pin(q):
 q=Path(q);s=q.lstat();h=hashlib.sha256()
 with q.open('rb')as f:
  need(identity(os.fstat(f.fileno()))==identity(s),'opened Source/control current7')
  while True:
   b=f.read(2**20)
   if not b:break
   h.update(b)
  need(identity(os.fstat(f.fileno()))==identity(s),'EOF Source/control current7')
 p=dict(path=str(q),sha256=h.hexdigest(),size_bytes=s.st_size,identity=identity(s));current(p);return p
def metadata(p):
 q=current(p);need(p['size_bytes']<8*2**20,'bounded metadata8MiB');raw=q.read_bytes();need(hashlib.sha256(raw).hexdigest()==p['sha256'],'metadata complete SHA');v=json.loads(raw);current(p);return v
def source(p,name):
 need(pin(p['path'])==p,'whole frozen Source fullPF');spec=importlib.util.spec_from_file_location(name,p['path']);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);current(p);return m
def unique(rows):
 t={}
 for p in rows:
  if p['path']in t:need(t[p['path']]==p,'same path one fullPF')
  t[p['path']]=p
 return list(t.values())
def write(q,v):
 raw=(json.dumps(v,indent=2,allow_nan=False)+'\n').encode();need(len(raw)<6*2**20,'metadata report6MiB')
 if Path(q).is_relative_to(BASE):need(sum(x.stat().st_size for x in BASE.rglob('*')if x.is_file())+len(raw)<SOURCE_BOUND,'whole Source/metadata16MiB including new output')
 with Path(q).open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
def genuine(v,key,p,outkey):
 t=v[key];need(v['observed_closed']is True and type(v['original_integer_exit_code'])is int and v['original_integer_exit_code']==0 and type(t['exit_code'])is int and t['exit_code']==0 and t.get('session_id')is None,'genuine closed typed0')
 need(json.loads(t['output'].strip().splitlines()[-1])[outkey]==p,'genuine return exact artifact PF')
def read_with_budget(p,budget):
 budget();v=metadata(p);budget();return v

def coverage(packet,state,post):
 return dict(schema='ROOT_ACTUAL_COMPLETE_OBSERVED_SNAPSHOT_COVERAGE_FOR_CONTEXT_V1',all_original_snapshot_pairs_saved=True,actual_extraction_report_pin=packet['actual_B_extraction_report_pin'],actual_observation_manifest_pin=packet['actual_observation_manifest_pin'],current_B_case_input_binding_pin=packet['current_B_case_input_binding_pin'],actual_closed_extraction_receipt_independently_reviewed=True,independent_actual_review_pin=packet['actual_B_extraction_post_pin'],states={'B':dict(all_snapshot_pairs=post['all_snapshot_pairs'],complete_context_pins=state['complete_context_pins'])},new_qualification_sha256=None)
def aggregation_binding(packet,state,post,coverage_pin=None):
 pairs=post['all_snapshot_pairs'];final=pairs[-1]
 return dict(state_order=['B'],current_B_case_input_binding_pin=packet['current_B_case_input_binding_pin'],Source_route=dict(ITSTMP=0,historical_call_proved=False),states={'B':dict(sqlite_pin=final['sqlite_pin'],native_pool_pin=final['native_pool_pin'])},actual_context_states={'B':dict(complete_context_pins=state['complete_context_pins'],all_snapshot_pairs=pairs,actual_extraction_report_pin=packet['actual_B_extraction_report_pin'],actual_observation_manifest_pin=packet['actual_observation_manifest_pin'],selected_last_libmix_number=state['selected_last_libmix_number'],actual_extraction_coverage_contract_pin=coverage_pin)})
def proof_metadata_pins(packet):
 control=list(packet['current_B55_OVERV_control_binding']['metadata_pins'].values());life=packet['exact_B4_product_lifecycle_binding'];roles=[life['actual_B_capture_manifest_pin']]
 for phase in('archive','retirement'):
  roles += [life[phase][key]for key in('receipt_pin','Root_tools_pin','post_pin','post_tools_pin')]
 return unique(control+roles+[packet[k]for k in('actual_B_extraction_report_pin','actual_B_extraction_Host_report_pin','actual_B_extraction_Root_tools_pin','actual_B_extraction_post_pin','actual_B_extraction_post_tools_pin','actual_capture_Host_report_pin','actual_observation_manifest_pin','current_B_case_input_binding_pin','latest_complete_plan_pin')])
def live_worker_inputs(packet,state,post,Source_pins):
 protected=state['physical_input_pins']+state['complete_observed_file_pins']+[p for row in post['all_snapshot_pairs']for p in(row['sqlite_pin'],row['native_pool_pin'])]
 retired={p['path']for p in packet['exact_B4_product_lifecycle_binding']['ordered_exact4_historical_product_pins']}
 need(not retired&{p['path']for p in protected},'all original mathematical inputs remain live; exact4 products are historical export roles only')
 return unique(Source_pins+protected+proof_metadata_pins(packet))
def lifecycle_scaffold(packet,state,post,complete_inputs):
 return dict(exact_B4_product_lifecycle_binding=packet['exact_B4_product_lifecycle_binding'],actual_observation_manifest_pin=packet['actual_observation_manifest_pin'],aggregation_binding=aggregation_binding(packet,state,post),complete_input_pins=complete_inputs,explicit_cumulative_metadata_file_pins=packet['child_ordinary_explicit_metadata_pins'])
def admit(packet):
 need(packet['schema']in('ROOT_CURRENT_B_COMPLETE_AGGREGATE_ADMISSION_PACKET_V1','CURRENT_B_COMPLETE_AGGREGATE_SOURCE_ONLY_PLAN_V1')and packet['actual_business_preconditions_closed']is True and packet['source_role_pin_audit_complete']is True and packet['B4_actual_role_projection_audited']is True and packet['original_caps']==CAPS,'UNREADY NULL archive/retirement/post/latest/real-budget bindings cannot admit or GEN')
 need(packet['only_current_stage']=='aggregate'and packet['bounded_new_aggregate_output_reservation_bytes']==OUTPUT_BOUND and packet['bounded_new_Source_metadata_reservation_bytes']==SOURCE_BOUND and packet['future_stage_budget_added_to_this_stage']is False,'complete aggregate-only320MiB+Source16MiB, no scope reduction')
 h=metadata(packet['actual_capture_Host_report_pin']);state=h['actual_B_state'];manifest=metadata(packet['actual_observation_manifest_pin']);binding=metadata(packet['current_B_case_input_binding_pin']);post=metadata(packet['actual_B_extraction_post_pin']);extract=metadata(packet['actual_B_extraction_report_pin']);eh=metadata(packet['actual_B_extraction_Host_report_pin'])
 er=metadata(packet['actual_B_extraction_Root_tools_pin']);et=metadata(packet['actual_B_extraction_post_tools_pin']);genuine(er,'actual_terminal_return',packet['actual_B_extraction_Host_report_pin'],'report_pin');genuine(et,'actual_review_return',packet['actual_B_extraction_post_pin'],'review_pin')
 need(eh['schema']=='ACTUAL_CURRENT_B_COMPLETE_EXTRACT_GUARDED_ROOT_REPORT_V1'and eh['status']=='ACTUAL_CURRENT_B_COMPLETE_EXTRACT_EVIDENCE_CHILD2_CLOSED_ONLY'and eh['failure']is None and eh['actual_child_integer_exit_code']==2 and eh['actual_intentional_exit2_normal_closure']is True and eh['records'][0]['status']=='FAILED'and eh['original_runner_error']=='own-child stage failed; no retry'and eh['actual_child_report_pin']==packet['actual_B_extraction_report_pin'],'actual complete extraction Root0 and original evidence worker2/FAILED/error retained')
 need(post['schema']=='ROOT_ACTUAL_CURRENT_MATERIAL_EXTRACTION_REVIEW_V1'and post['status']=='PASS_ACTUAL_CURRENT_B_FULL55_CONTEXT8_SNAPSHOT_EXTRACTION_EVIDENCE_CHILD2_METADATA_ONLY'and post['failure']is None and post['actual_Root_integer_exit_code']==0 and post['actual_child_integer_exit_code']==2 and post['actual_extraction_report_pin']==packet['actual_B_extraction_report_pin']and post['actual_extraction_host_pin']==packet['actual_B_extraction_Host_report_pin']and post['actual_observation_manifest_pin']==packet['actual_observation_manifest_pin']and post['current_B_case_input_binding_pin']==packet['current_B_case_input_binding_pin']and post['all_original_snapshot_and_context_pins_verified']is True,'genuine complete eight-pair independent actual B extraction post0')
 need(len(post['all_snapshot_pairs'])==len(extract['states']['B'])==8 and len(post['complete_context_pins'])==len(state['complete_context_pins'])==len(extract['context_states']['B'])==55 and post['complete_context_pins']==state['complete_context_pins']and manifest['states']['B']==dict(state,actual_owning_report_pin=packet['actual_capture_Host_report_pin']),'complete genuine current B55 contexts/eight pairs and same immutable manifest')
 helper=source(packet['copied_capture_metadata_admission_Source_pin'],'B_aggregate_current_capture_metadata')
 req=dict(actual_capture_control_binding=packet['actual_capture_control_binding'],actual_observation_manifest_pin=packet['actual_observation_manifest_pin'],current_B_case_input_binding_pin=packet['current_B_case_input_binding_pin'])
 helper.admit_actual_capture(packet['actual_capture_Host_report_pin'],state['actual_stage_label'],state['actual_command'],req,read_with_budget,lambda:None)
 route=source(packet['copied_B_input_binding_Source_pin'],'B_aggregate_original_B_binding');seed=metadata(binding['original_v10_seed_plan_pin']);route.validate_B_binding(binding,seed,binding['original_v10_seed_plan_pin']);route.validate_manifest_B(manifest,binding,packet['current_B_case_input_binding_pin'])
 need(packet['prior_B_aggregate_executed']is False and packet['prior_B_issue_count']is None and packet['issue_count_adjustment_performed']is False,'no invented prior B aggregate or issue subtraction')
 latest=metadata(packet['latest_complete_plan_pin']);roots=packet['complete_joint_roots'];cprefix=binding['complete_latest_prefix_roots']+[binding['actual_output_root']]
 need(latest['complete_joint_roots']==roots[:-1]and roots[:-1][:len(cprefix)]==cprefix and roots[-1]==str(OUT)and len(roots)==len(set(roots))and not any(Path(a).is_relative_to(Path(b))for a in roots for b in roots if a!=b)and any(BASE.is_relative_to(Path(x))for x in roots[:-1]),'entire dynamic latest prefix retains capture/extract/B55/all failures and counted Source plus one aggregate root')
 need(packet['planned_actual_output_root']==str(OUT)and not os.path.lexists(OUT),'fresh distinct aggregate owning root once')
 b55=source(packet['B55_metadata_admission_Source_pin'],'B_aggregate_real_B55_metadata_admission');admitted=b55.admit(packet['current_B55_OVERV_control_binding'],aggregation_binding(packet,state,post),metadata)
 need(admitted['same_original_final_pair']==post['all_snapshot_pairs'][-1]and admitted['prior_B_aggregate_executed']is False,'same true B55 input/control, first B aggregate only')
 life=source(packet['B4_lifecycle_admission_Source_pin'],'B_aggregate_exact4_lifecycle_admission');rows=packet['prospective_worker_live_input_pins'];life_result=life.admit(lifecycle_scaffold(packet,state,post,rows),metadata,current)
 need(life_result['retired_paths_exactly_absent']is True,'actual exact4 archive/retirement/post0 completes before any live-input admission')
 retired={p['path']for p in life_result['exact_four_historical_fullPFs_preserved']}
 need(not retired&{p['path']for p in packet['explicit_cumulative_metadata_file_pins']+packet['inherited_metadata_current7_pins']+packet['child_ordinary_explicit_metadata_pins']+rows},'only exact4 proven historical retired roles removed from live tables; all other paths remain mandatory')
 build=metadata(packet['original_guard_build_plan_pin']);bm=source(packet['original_guard_build_contract_Source_pin'],'B_aggregate_original_build_contract');bm.admit_lifecycle(build)
 need(packet['original_Common_Source_pin']==build['original_Common_Source_pin']and packet['original_support_Source_pin']==build['original_support_Source_pin']and packet['original_bounded_Source_pin']==build['original_bounded_Source_pin'],'same exact unmodified original guard Source dependencies')
 for p in packet['explicit_cumulative_metadata_file_pins']+packet['inherited_metadata_current7_pins']:bm.current_metadata_role(p,build)
 for p in packet['child_ordinary_explicit_metadata_pins']:
  q=current(p);need(q.lstat().st_uid==os.getuid(),'ordinary owned child metadata only; exact system roles stay in parent role table')
 for p in packet['existing_actual_A_prior_issue_reports_current7_only_pins']:current(p)
 return build,bm,manifest,binding,state,extract,post

def admit_aggregate_only_stage(packet,binding,before):
 latest=metadata(packet['latest_complete_plan_pin']);roots=packet['complete_joint_roots'];prefix=binding['complete_latest_prefix_roots']+[binding['actual_output_root']]
 need(latest['complete_joint_roots']==roots[:-1]and roots[:-1][:len(prefix)]==prefix and roots[-1]==str(OUT),'same complete latest ledger at actual stage start')
 j=before['complete_joint'];h=before['original_history'];existing=j['artifact_bytes']+before['explicit_external_metadata_bytes']+before['host_open_unlinked_bytes']
 need(before['host_SELF_peak_bytes']<512*2**20 and before['whole_elapsed_seconds']<1800 and existing+OUTPUT_BOUND+SOURCE_BOUND<2*2**30,'actual current original full ledger+aggregate320+Source16 fits original2GiB')
 need(h['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30 and j['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'original cold/meta/history96/free8 retained')
 return dict(complete_joint_roots=roots,original_caps=CAPS,stage_output_reservations=dict(aggregate=OUTPUT_BOUND),new_Source_metadata_reservation_bytes=SOURCE_BOUND,existing_measured_total_bytes=existing,original_cumulative_fresh_bound_bytes=2*2**30,only_current_stage='aggregate',other_stages_not_reserved_or_reduced=True)
