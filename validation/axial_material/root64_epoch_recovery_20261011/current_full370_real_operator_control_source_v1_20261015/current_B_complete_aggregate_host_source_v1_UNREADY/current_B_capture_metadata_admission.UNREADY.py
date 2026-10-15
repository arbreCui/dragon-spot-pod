"""UNREADY exact capture metadata admission. No compiler/native/helper imports.

This module is not an actual admission receipt. All future real proof fields
remain NULL in the separate draft. A reviewed owning Root host must supply the
exact actual capture, independent post and full latest ledger before execution.
"""
import json
from pathlib import Path
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,
 history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,
 free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
B_SCOPE='ONE_CURRENT_ORIGINAL_B_MATERIAL_CONSTRUCTION_FULL_CONTEXT_NOT_A_RELABELLING'
LEGACY_ENGINE_CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,
 joint_archive_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,
 threads=1,children_at_once=1,retries=0)
STAGE_OUTPUT_RESERVATIONS=dict(extract=512*2**20,aggregate=320*2**20,B_OVERV_control=16*2**20)
SOURCE_RESERVATION=16*2**20
FALSE=dict(physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
def need(v,m):
 if type(v)is not bool or not v:raise ValueError(m)
def genuine(raw,key,p,role):
 r=raw[key]
 need(raw['observed_closed']is True and type(raw['original_integer_exit_code'])is int and raw['original_integer_exit_code']==0 and type(r['exit_code'])is int and r['exit_code']==0 and r.get('session_id')is None,'genuine actual original closed typed0')
 need(json.loads(r['output'].strip().splitlines()[-1])[role]==p,'actual stdout fullPF binding')
def resources(v):
 j=v['complete_joint'];h=v['original_history']
 need(v['host_SELF_peak_bytes']<512*2**20 and v['whole_elapsed_seconds']<1800,
  'actual original host SELF512/whole1800')
 need(j['artifact_bytes']+v['explicit_external_metadata_bytes']+v['host_open_unlinked_bytes']<2*2**30,
  'actual cumulative fresh2GiB includes external metadata and open unlinked')
 need(h['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30 and j['disk_free_bytes']-20971764748-2*2**30>=8*2**30,
  'original cold/meta/history96/free8 unchanged')
def project_legacy_engine_caps(caps):
 need(caps==CAPS,'all original full caps retained upstream, not stripped or relaxed')
 projected={k:caps['fresh_bytes']if k=='joint_archive_bytes'else caps[k]for k in LEGACY_ENGINE_CAPS}
 need(projected==LEGACY_ENGINE_CAPS,'legacy metadata keys project exact identical values only')
 return projected

def admit_actual_capture(report_pin,label,command,request,read,budget):
 proof=request['actual_capture_control_binding']
 need(type(proof)is dict and proof['schema']=='CURRENT_B_ACTUAL_CAPTURE_POST_BINDING_V1',
  'UNREADY NULL actual capture/post bindings cannot execute')
 host=read(report_pin,budget);raw=read(proof['actual_Root_tools_pin'],budget)
 need(proof['actual_Host_report_pin']==report_pin and host['schema']=='ACTUAL_CURRENT_B_COMPLETE_NATIVE_CAPTURE_ROOT_REPORT_V1' and host['status']=='ACTUAL_CURRENT_B_FULL55_CONTEXT_8TREE_4PRODUCT_CAPTURE_CLOSED0_ONLY'and host['failure']is None and host['secondary_failures']==[] and host['final_report_resource_check_passed']is True,'exact new capture Host schema and real terminal closure; no invented old Host fields')
 genuine(raw,'actual_terminal_return',report_pin,'report_pin')
 need(raw['actual_execution_permission_mode']=='require_escalated'and raw['actual_retried']is False,
  'original PS guard permission and zero retry; actual raw key audit required')
 stdout=json.loads(raw['actual_terminal_return']['output'].strip().splitlines()[-1])
 need(stdout['manifest_pin']==request['actual_observation_manifest_pin']and stdout['actual_B_native_capture_closed0']is True,'same actual capture manifest stdout fullPF')
 need(host['actual_B_input_binding_pin']==request['current_B_case_input_binding_pin'] and host['original_caps']==CAPS and host['original_guard_class']=='OwnRSSSerialExecutor'and host['original_guard_MRO_unchanged']is True,'same original B input and unmodified guard class/caps')
 need(host['all_old_cwd_entries_current7_before']==host['all_old_cwd_entries_current7_after'],
  'all original library-cwd entry identities preserved')
 records=host['records'];watches=host['actual_watchdog_checks']
 need(len(records)==len(watches)==1 and records[0]['label']==label and records[0]['command']==command and records[0]['status']=='PASS','sole actual original B native stage, no reduced capture')
 row=watches[0];record=records[0];root=Path(report_pin['path']).parent
 need(row['actual_stage_record_label']==label and row['actual_watchdog_pin']['path']==str(root/(label+'.watchdog.json')) and row['actual_log_pin']['path']==str(root/(label+'.log'))and row['actual_log_pin']['sha256']==record['log_sha256'],'exact nested original record.label watchdog/log roles')
 w=read(row['actual_watchdog_pin'],budget)
 need(w==row['actual_watchdog']and type(w['returncode'])is int and w['returncode']==0 and w['command']==command and w['limit_failure']is None and w['own_child_only']is True and w['liveness_group_cleanup']is True and w['rss_cap_mib']==512 and 0<=w['sampled_peak_rss_mib']<512 and 0<w['elapsed_seconds']<w['wall_cap_seconds']<=600,'genuine original monitor child0/wall/RSS/group closure')
 resources(host['resources_before']);resources(host['resources_after'])
 state=host['actual_B_state']
 need(state['state']=='B'and len(state['complete_context_pins'])==55 and len(state['complete_state_snapshot_inputs'])==8 and len(state['actual_material_product_pins'])==4,'actual complete B55context/8tree/fourproducts')
 post=read(proof['actual_capture_post_pin'],budget);pt=read(proof['actual_capture_post_tools_pin'],budget)
 genuine(pt,'actual_review_return',proof['actual_capture_post_pin'],'review_pin')
 roles=proof['capture_post_role_projection']
 need(type(roles)is dict and type(roles['schema'])is str and type(roles['status'])is str,
  'exact real capture-post schema/status/keys must be audited and frozen after actual, never guessed')
 need(post['schema']==roles['schema']and post['status']==roles['status']and post['failure']is None and post['metadata_only']is True and post[roles['actual_Host_report_pin_field']]==report_pin and post[roles['actual_Root_tools_pin_field']]==proof['actual_Root_tools_pin'],'same real independent post0 binding')
 need(type(post[roles['actual_Root_integer_exit_code_field']])is int and post[roles['actual_Root_integer_exit_code_field']]==0,'actual post retains genuine Root0')
 return host

def admit_operation_ledger(binding,operation_root,latest_roots,complete_roots,latest_plan,resource_before):
 root=Path(operation_root);capture_prefix=binding['complete_latest_prefix_roots']+[binding['actual_output_root']]
 need(binding['original_caps']==CAPS and root.is_absolute()and str(root)==operation_root and operation_root!=binding['actual_output_root'],'distinct explicit operation owning root; never rebind immutable capture input')
 need(latest_plan['complete_joint_roots']==latest_roots and latest_roots[:len(capture_prefix)]==capture_prefix and complete_roots==latest_roots+[operation_root]and len(complete_roots)==len(set(complete_roots))and not any(Path(a).is_relative_to(Path(b))for a in complete_roots for b in complete_roots if a!=b),'entire exact latest prefix retains all actual/failure namespaces plus one operation root')
 resources(resource_before)
 existing=resource_before['complete_joint']['artifact_bytes']+resource_before['explicit_external_metadata_bytes']+resource_before['host_open_unlinked_bytes']
 reservation=sum(STAGE_OUTPUT_RESERVATIONS.values())+SOURCE_RESERVATION
 need(existing+reservation<2*2**30,'actual original resource snapshot plus full extract512/aggregate320/Bcontrol16/Source16 reserves within original cumulative2GiB; no forecast or omitted history')
 return dict(complete_joint_roots=complete_roots,original_caps=CAPS,stage_output_reservations=STAGE_OUTPUT_RESERVATIONS,new_Source_metadata_reservation_bytes=SOURCE_RESERVATION,existing_measured_total_bytes=existing,original_cumulative_fresh_bound_bytes=2*2**30)
