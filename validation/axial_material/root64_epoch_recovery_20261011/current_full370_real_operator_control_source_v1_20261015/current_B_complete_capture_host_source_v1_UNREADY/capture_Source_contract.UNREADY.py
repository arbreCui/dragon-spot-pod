"""UNREADY Source/control contract. Importing does no native or Source preparation."""
import hashlib,importlib.util,json,os,stat,sys
from pathlib import Path
R=Path('/Users/wen/spot');BASE=Path(__file__).absolute().parent
IO=BASE.parent/'current_extra_reaction_source_v2/B_only_observer_IO_source_v1'
OUT=R/'validation/artifacts/axial-material-inputs-20261003/A/b63'
CAPTURE_BOUND=640*2**20;SOURCE_BOUND=16*2**20
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
FALSE=dict(three_plane_qualified=False,GLOBAL_qualified=False,rank_qualified=False,online_BOOT_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,historical_unsaved_context_recovered=False,reaction_multiplicity_qualified=False,physical_neutron_balance_qualified=False,coupled_370group_reference_qualified=False,scientific_accuracy_qualified=False,B_full_extraction_completed=False,B_six_phase_construction_completed=False,B_OVERV_control_completed=False,physics_qualified=False,compiled_IO_semantics_qualified=False)
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
def admit_build(packet):
 need(packet['actual_B_build_role_keys_audited']is True,'actual build roles must be audited after real closure')
 h=metadata(packet['actual_B_IO_build_Host_report_pin']);t=metadata(packet['actual_B_IO_build_Root_tools_pin']);p=metadata(packet['actual_B_IO_build_post_pin']);pt=metadata(packet['actual_B_IO_build_post_tools_pin'])
 genuine(t,'actual_terminal_return',packet['actual_B_IO_build_Host_report_pin'],'report_pin');genuine(pt,'actual_review_return',packet['actual_B_IO_build_post_pin'],'review_pin')
 need(t['actual_execution_permission_mode']=='require_escalated'and t['actual_retried']is False,'original guard permission and once build')
 need(h['schema']=='ACTUAL_B_IO_FOUR_COMPILE_ONE_LINK_QUALIFICATION_REPORT_V1'and h['status']=='ACTUAL_B_IO_BUILD_FIVE_STAGE0_CLOSED_ONLY'and h['failure']is None and h['control_plan_pin']==packet['actual_B_IO_build_plan_pin']and h['build_stage_count']==5 and h['final_report_resource_check_passed']is True and h['original_caps']==CAPS,'actual fresh five-stage guarded build closure')
 need(len(h['records'])==len(h['actual_watchdog_checks'])==5 and all(r['status']=='PASS'for r in h['records']),'all genuine five original records')
 for r,w in zip(h['records'],h['actual_watchdog_checks']):
  x=w['actual_watchdog'];need(w['actual_stage_record_label']==r['label']and type(x['returncode'])is int and x['returncode']==0 and x['command']==r['command']and x['limit_failure']is None and x['own_child_only']is True and x['liveness_group_cleanup']is True and x['rss_cap_mib']==512 and 0<=x['sampled_peak_rss_mib']<512 and 0<x['elapsed_seconds']<x['wall_cap_seconds']<=600,'all original child0/watchguard closures')
 need(p['schema']=='RECORDED_B_IO_FIVE_STAGE_BUILD_METADATA_POSTVERIFY_V1'and p['status']=='PASS_ACTUAL_B_IO_FOUR_COMPILE_ONE_LINK_STAGE0_METADATA_ONLY_NO_NATIVE_QUALIFICATION'and p['failure']is None and p['actual_Root_tools_pin']==packet['actual_B_IO_build_Root_tools_pin']and p['actual_Host_report_pin']==packet['actual_B_IO_build_Host_report_pin']and type(p['actual_Root_integer_exit_code'])is int and p['actual_Root_integer_exit_code']==0 and p['actual_child_integer_exit_codes']==[0]*5 and all(type(v)is int for v in p['actual_child_integer_exit_codes'])and p['new_runtime_full_pin']==packet['new_IO_runtime_pin'],'independent actual five-stage metadata post0 and exact new runtime')
 build=metadata(packet['actual_B_IO_build_plan_pin']);runtime=packet['new_IO_runtime_pin'];need(runtime['path']==str(Path(build['planned_actual_output_root'])/'sources/runtime/Dragon')and runtime in h['whole_new_output_pins'],'actual new emitted runtime, never old qualified binary')
 current(runtime)
 bm=source(packet['frozen_B_IO_build_contract_Source_pin'],'capture_original_B_build_contract');bm.admit_lifecycle(build)
 return build
def admit(packet):
 need(packet['schema']in('ROOT_CURRENT_B_COMPLETE_CAPTURE_ADMISSION_PACKET_V1','CURRENT_B_COMPLETE_CAPTURE_SOURCE_ONLY_PLAN_V1')and packet['actual_business_preconditions_closed']is True and packet['original_caps']==CAPS,'future NULL draft never business admission')
 build=admit_build(packet);latest=metadata(packet['latest_complete_plan_pin']);roots=packet['complete_joint_roots']
 need(latest['complete_joint_roots']==roots[:-1]and roots[-1]==str(OUT)and len(roots)==len(set(roots))and not any(Path(x).is_relative_to(Path(y))for x in roots for y in roots if x!=y),'entire latest prefix plus one literal owning capture root, no ordinal/count substitution')
 need(build['complete_joint_roots']==roots[:-1][:len(build['complete_joint_roots'])],'genuine build prefix retained inside the entire later current prefix')
 need(not os.path.lexists(OUT)and packet['planned_actual_output_root']==str(OUT)and any(BASE.is_relative_to(Path(x))for x in roots[:-1]),'fresh b63 once; Source remains counted in prior FTOP')
 need(packet['bounded_new_capture_output_reservation_bytes']==CAPTURE_BOUND and packet['bounded_new_Source_metadata_reservation_bytes']==SOURCE_BOUND and packet['full_extraction_scope_deferred_not_reduced']is True and packet['historical_capture_reference_bytes']==569395111 and packet['historical_full_extraction_reference_bytes']==438863526 and packet['new_B_upper_size_forecast_claimed']is False,'640MiB enforced capture stage bound, historical sizes are references, complete future extraction retained')
 need(packet['original_Common_Source_pin']==build['original_Common_Source_pin']and packet['original_support_Source_pin']==build['original_support_Source_pin']and packet['original_bounded_Source_pin']==build['original_bounded_Source_pin'],'unchanged original guard dependencies')
 for p in packet['explicit_cumulative_metadata_file_pins']:bm.current_metadata_role(p,build)
 for p in packet['inherited_metadata_current7_pins']:bm.current_metadata_role(p,build)
 return build,bm
