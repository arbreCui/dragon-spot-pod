"""UNREADY B55 metadata/argv interface. No helper imports, IO, compiler or native main."""
import json
from pathlib import Path
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,
 history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,
 free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
OUTPUT_BOUND=16*2**20;SOURCE_BOUND=16*2**20
FALSE=dict(A_control_reused=False,physics_qualified=False,historical_machine_bit_replay=False,
 historical_native_RAM_bits_verified=False,original_XSM_memory_bits_verified=False,
 complete_reaction_authority_qualified=False,AAA_qualified=False,ABA_admitted=False,
 goal_complete=False,source_context_issue_resolved=False)
def need(ok,message):
 if type(ok)is not bool or not ok:raise RuntimeError(message)
def genuine(v,key,p,role,code=0):
 t=v[key];need(v['observed_closed']is True and type(v['original_integer_exit_code'])is int and v['original_integer_exit_code']==code and type(t['exit_code'])is int and t['exit_code']==code and t.get('session_id')is None,'genuine original closed typed return')
 need(json.loads(t['output'].strip().splitlines()[-1])[role]==p,'actual stdout exact fullPF')
def admit_actual_B55_metadata(request,read,current7,B55_interface):
 """Caller supplies exact frozen metadata reader; no scientific body read here."""
 need(request['schema']=='CURRENT_B55_OVERV_CONTROL_PENDING_ACTUAL_BINDINGS_V1'and request['actual_B_extraction_and_post_roles_audited']is True,'UNREADY NULL extraction/post cannot execute')
 host=read(request['actual_B_extraction_Host_report_pin']);raw=read(request['actual_B_extraction_Root_tools_pin']);post=read(request['actual_B_extraction_post_pin']);pt=read(request['actual_B_extraction_post_tools_pin'])
 genuine(raw,'actual_terminal_return',request['actual_B_extraction_Host_report_pin'],'report_pin');genuine(pt,'actual_review_return',request['actual_B_extraction_post_pin'],'review_pin')
 need(raw['actual_execution_permission_mode']=='require_escalated'and raw['actual_retried']is False,'original PS guard permission and zero retry')
 need(host['schema']=='ACTUAL_CURRENT_B_COMPLETE_EXTRACT_GUARDED_ROOT_REPORT_V1'and host['status']=='ACTUAL_CURRENT_B_COMPLETE_EXTRACT_EVIDENCE_CHILD2_CLOSED_ONLY'and host['failure']is None and host['secondary_failures']==[]and host['final_report_resource_check_passed']is True and host['original_caps']==CAPS and host['actual_child_integer_exit_code']==2 and type(host['actual_child_integer_exit_code'])is int and host['actual_intentional_exit2_normal_closure']is True,'actual B full extraction Root0 and intentional child2, never child0')
 need(len(host['records'])==1 and host['records'][0]['status']=='FAILED'and host['records'][0]['error']==host['original_runner_error']=='own-child stage failed; no retry','original FAILED/error remains immutable evidence')
 need(post['schema']=='ROOT_ACTUAL_CURRENT_MATERIAL_EXTRACTION_REVIEW_V1'and post['status']=='PASS_ACTUAL_CURRENT_B_FULL55_CONTEXT8_SNAPSHOT_EXTRACTION_EVIDENCE_CHILD2_METADATA_ONLY'and post['failure']is None and post['metadata_only']is True and post['actual_extraction_host_pin']==request['actual_B_extraction_Host_report_pin']and post['actual_Root_true_tool_return_pin']==request['actual_B_extraction_Root_tools_pin']and type(post['actual_Root_integer_exit_code'])is int and post['actual_Root_integer_exit_code']==0 and type(post['actual_child_integer_exit_code'])is int and post['actual_child_integer_exit_code']==2,'exact independent actual B extraction metadata post0, without numerical replay claim')
 reportpin=request['actual_B_extraction_child_report_pin'];report=read(reportpin)
 need(host['actual_child_report_pin']==reportpin and post['actual_extraction_report_pin']==reportpin and len(report['states']['B'])==8 and len(report['context_states']['B'])==55,'actual full B eight saved pairs and55contexts')
 selected=B55_interface.select_actual_B55_control_pair(report,reportpin,request['actual_B_manifest_pin'],request['actual_B_input_binding_pin'],post,request['actual_B_extraction_post_pin'])
 descriptor=report['states']['B'][-1]
 need(descriptor==request['selected_actual_B55_snapshot_descriptor']and descriptor['state']=='B'and descriptor['event']==55 and descriptor['role']=='final-complete-micro'and descriptor['root_prefix']==[]and selected['final_pair']==request['selected_actual_B55_SQL_pool_pair'],'exact new B55 pair, no A descriptor substitution')
 current7(descriptor['paired_SQLite_pin']);current7(descriptor['paired_original_pool_pin'])
 return descriptor,selected
def admit_control_only_stage(request,capture_binding,latest_plan,resource_before):
 roots=request['complete_joint_roots'];out=Path(request['planned_actual_output_root']);prefix=capture_binding['complete_latest_prefix_roots']+[capture_binding['actual_output_root']]
 need(request['original_caps']==CAPS and latest_plan['complete_joint_roots']==roots[:-1]and roots[:-1][:len(prefix)]==prefix and roots[-1]==str(out)and out.is_absolute()and len(roots)==len(set(roots))and not any(Path(a).is_relative_to(Path(b))for a in roots for b in roots if a!=b),'entire dynamic latest prefix includes capture/extraction/failures plus one whole control root')
 need(request['bounded_new_control_output_reservation_bytes']==OUTPUT_BOUND and request['bounded_new_Source_metadata_reservation_bytes']==SOURCE_BOUND and request['future_aggregate_budget_added_to_this_stage']is False,'only current complete B55 control16MiB and Source16MiB; no future aggregate320 budget')
 j=resource_before['complete_joint'];h=resource_before['original_history'];existing=j['artifact_bytes']+resource_before['explicit_external_metadata_bytes']+resource_before['host_open_unlinked_bytes']
 need(resource_before['host_SELF_peak_bytes']<512*2**20 and resource_before['whole_elapsed_seconds']<1800 and existing+OUTPUT_BOUND+SOURCE_BOUND<2*2**30,'unchanged actual host512/whole1800 and full current2GiB control-stage reserve')
 need(h['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30 and j['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'unchanged cold/meta/history/free reserves')
 return dict(complete_joint_roots=roots,stage_output_reservations=dict(B55_OVERV_control=OUTPUT_BOUND),Source_metadata_reservation_bytes=SOURCE_BOUND,only_current_stage='B55_OVERV_control',existing_measured_total_bytes=existing,original_caps=CAPS)
def three_original_native_stage_commands(request,control_Fortran_Source_pin):
 """Pure argv constructor. Original Fortran and integer oracle remain whole files."""
 out=Path(request['planned_actual_output_root']);compiler=request['original_compiler_pin']['path'];obj=str(out/'build/OVERV_control.o');exe=str(out/'runtime/OVERV_control_unqualified')
 need(request['original_compile_flags']==['-O2','-march=native','-ffp-contract=off','-fcheck=all','-fbacktrace','-g','-fPIC','-frecord-marker=4','-ffixed-line-length-none']and len(request['original_four_archive_pins'])==4,'exact original nine Fortran flags/four archive order')
 return [dict(stage='compile_control',cwd=str(out/'build'),command=[compiler,*request['original_compile_flags'],*request['original_compile_include_arguments'],'-J'+str(out/'build'),'-c',control_Fortran_Source_pin['path'],'-o',obj]),dict(stage='link_control',cwd=str(out/'build'),command=[compiler,'-O2','-ffp-contract=off',obj,*[p['path']for p in request['original_four_archive_pins']],'-o',exe]),dict(stage='run_current_control',cwd=str(out/'control'),command=[exe,str(out/'input/ENERGY371_original_words.bin')])]
