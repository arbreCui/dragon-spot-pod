"""UNREADY extract-only Source/control contract; no worker or decoder on import."""
import hashlib,importlib.util,json,os,stat,sys
from pathlib import Path
R=Path('/Users/wen/spot');BASE=Path(__file__).absolute().parent
IO=BASE.parent/'current_extra_reaction_source_v2/B_only_observer_IO_source_v1'
OUT=R/'validation/artifacts/axial-material-current-B-complete-fullfield-extract-20261015-v1'
OUTPUT_BOUND=512*2**20;SOURCE_BOUND=16*2**20
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
FALSE=dict(historical_native_RAM_bits_verified=False,original_XSM_memory_bits_verified=False,historical_unsaved_context_recovered=False,reaction_multiplicity_qualified=False,TRANC_semantics_qualified=False,physical_neutron_balance_qualified=False,coupled_370group_reference_qualified=False,scientific_accuracy_qualified=False,AAA_accuracy_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,B_OVERV_control_completed=False,B_six_phase_construction_completed=False,physics_qualified=False)
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
def admit_optional_ASCII_lifecycle(packet,state):
 proof=packet['completed_capture_ASCII_lifecycle_binding'];products=state['actual_material_product_pins']
 need(len(products)==4,'all four original actual capture product PF roles retained')
 if proof is None:
  for p in products:current(p)
  return
 need(proof['actual_role_projection_audited']is True,'future exact retirement metadata must be audited, never assumed')
 k=proof['actual_role_projection'];r=metadata(proof['receipt_pin']);rt=metadata(proof['Root_tools_pin']);p=metadata(proof['post_pin']);pt=metadata(proof['post_tools_pin'])
 genuine(rt,k['Root_return_field'],proof['receipt_pin'],k['Root_output_receipt_field']);genuine(pt,k['post_return_field'],proof['post_pin'],k['post_output_review_field'])
 targets=[p for p in products if Path(p['path']).name in('u.asc','a.asc','t.asc')]
 need(len(targets)==3 and r['schema']==k['receipt_schema']and r['status']==k['receipt_status']and r['failure']is None and r[k['released_pins_field']]==targets and r[k['released_bytes_field']]==sum(p['size_bytes']for p in targets),'exact three complete already-recorded B ASCII PFs retired; no native tree/product omission')
 need(p['schema']==k['post_schema']and p['status']==k['post_status']and p['failure']is None and p[k['post_receipt_field']]==proof['receipt_pin']and p[k['post_Root_tools_field']]==proof['Root_tools_pin'],'genuine independent exact lifecycle post0')
 need(all(not os.path.lexists(p['path'])for p in targets),'only exact proved historical completed ASCII roles absent')
 for p in products:
  if p not in targets:current(p)
def admit(packet):
 need(packet['schema']in('ROOT_CURRENT_B_COMPLETE_EXTRACT_ADMISSION_PACKET_V1','CURRENT_B_COMPLETE_EXTRACT_SOURCE_ONLY_PLAN_V1')and packet['actual_business_preconditions_closed']is True and packet['capture_actual_role_keys_audited']is True and packet['original_caps']==CAPS,'future NULL capture or post credentials remain UNREADY')
 helper=source(packet['copied_capture_metadata_admission_Source_pin'],'B_extract_capture_metadata_admission')
 h=metadata(packet['actual_capture_Host_report_pin']);state=h['actual_B_state'];manifest=metadata(packet['actual_observation_manifest_pin']);binding=metadata(packet['current_B_case_input_binding_pin'])
 request=dict(actual_capture_control_binding=packet['actual_capture_control_binding'],actual_observation_manifest_pin=packet['actual_observation_manifest_pin'],current_B_case_input_binding_pin=packet['current_B_case_input_binding_pin'])
 helper.admit_actual_capture(packet['actual_capture_Host_report_pin'],state['actual_stage_label'],state['actual_command'],request,read_with_budget,lambda:None)
 need(manifest['states']['B']['actual_owning_report_pin']==packet['actual_capture_Host_report_pin']and manifest['current_B_case_input_binding_pin']==packet['current_B_case_input_binding_pin']and manifest['state_order']==['B']and manifest['states']['B']['complete_context_pins']==state['complete_context_pins']and manifest['states']['B']['complete_state_snapshot_inputs']==state['complete_state_snapshot_inputs'],'exact immutable actual B manifest and capture Host scope')
 route=source(packet['copied_B_input_binding_Source_pin'],'B_extract_original_B_binding');seed=metadata(binding['original_v10_seed_plan_pin']);route.validate_B_binding(binding,seed,binding['original_v10_seed_plan_pin']);route.validate_manifest_B(manifest,binding,packet['current_B_case_input_binding_pin'])
 need(len(state['complete_context_pins'])==55 and len(state['complete_state_snapshot_inputs'])==8 and all(r['input_pin']['path']in{p['path']for p in state['complete_observed_file_pins']}for r in state['complete_state_snapshot_inputs']),'all actual B55contexts/eight whole trees kept')
 latest=metadata(packet['latest_complete_plan_pin']);roots=packet['complete_joint_roots'];prefix=binding['complete_latest_prefix_roots']+[binding['actual_output_root']]
 need(latest['complete_joint_roots']==roots[:-1]and roots[:-1][:len(prefix)]==prefix and roots[-1]==str(OUT)and len(roots)==len(set(roots))and not any(Path(a).is_relative_to(Path(b))for a in roots for b in roots if a!=b),'whole dynamic latest prefix retains capture and all failures plus one extraction root')
 need(packet['planned_actual_output_root']==str(OUT)and not os.path.lexists(OUT)and any(BASE.is_relative_to(Path(p))for p in roots[:-1]),'fresh extraction root once, Source counted under FTOP')
 need(packet['bounded_new_extract_output_reservation_bytes']==OUTPUT_BOUND and packet['bounded_new_Source_metadata_reservation_bytes']==SOURCE_BOUND and packet['only_current_stage']=='extract'and packet['future_aggregate_and_B_OVERV_budget_added_to_this_stage']is False,'extract-only512MiB+Source16MiB; future complete phases remain separate')
 build=metadata(packet['original_guard_build_plan_pin']);bm=source(packet['original_guard_build_contract_Source_pin'],'B_extract_original_build_contract');bm.admit_lifecycle(build)
 need(packet['original_Common_Source_pin']==build['original_Common_Source_pin']and packet['original_support_Source_pin']==build['original_support_Source_pin']and packet['original_bounded_Source_pin']==build['original_bounded_Source_pin'],'exact unchanged original guard Source dependencies')
 for p in packet['explicit_cumulative_metadata_file_pins']:bm.current_metadata_role(p,build)
 for p in packet['inherited_metadata_current7_pins']:bm.current_metadata_role(p,build)
 # Child Budget admits ordinary live metadata only. System SDK/compiler/PS roles
 # remain in the unchanged outer metadata resource path, never relabelled.
 for p in packet['child_ordinary_explicit_metadata_pins']:
  q=current(p);s=q.lstat();need(s.st_uid==os.getuid()and s.st_nlink==1,'ordinary child explicit metadata only')
 admit_optional_ASCII_lifecycle(packet,state)
 return build,bm,manifest,binding,state
def admit_extract_only_stage(packet,binding,before):
 latest=metadata(packet['latest_complete_plan_pin']);roots=packet['complete_joint_roots'];prefix=binding['complete_latest_prefix_roots']+[binding['actual_output_root']]
 need(latest['complete_joint_roots']==roots[:-1]and roots[:-1][:len(prefix)]==prefix and roots[-1]==str(OUT),'same entire current ledger at actual stage start')
 j=before['complete_joint'];h=before['original_history'];existing=j['artifact_bytes']+before['explicit_external_metadata_bytes']+before['host_open_unlinked_bytes']
 need(before['host_SELF_peak_bytes']<512*2**20 and before['whole_elapsed_seconds']<1800 and existing+OUTPUT_BOUND+SOURCE_BOUND<2*2**30,'actual original resource snapshot plus extract512/Source16 fits unchanged cumulative2GiB')
 need(h['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30 and j['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'unchanged history/cold/meta/free reserve')
 return dict(complete_joint_roots=roots,original_caps=CAPS,stage_output_reservations=dict(extract=OUTPUT_BOUND),new_Source_metadata_reservation_bytes=SOURCE_BOUND,existing_measured_total_bytes=existing,original_cumulative_fresh_bound_bytes=2*2**30,only_current_stage='extract',future_full_aggregate_and_B_OVERV_deferred_not_reduced=True)
