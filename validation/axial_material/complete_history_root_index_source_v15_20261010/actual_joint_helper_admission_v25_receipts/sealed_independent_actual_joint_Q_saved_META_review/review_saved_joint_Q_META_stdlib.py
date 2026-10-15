"""Finite independent review of already saved V25 helper-only Q metadata.

Does not import/execute the Q writer, helper, controller, guard, or any API.
No graph/trace/gzip/SQLite/material arrays or Source archive member replay.
Only explicit small JSON, the fixed writer Source, and saved pin lstat metadata.
"""
import ast
import hashlib
import json
import math
import os
from pathlib import Path
import stat
import struct

P=Path(__file__).parent
B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
Q=B/'Root_actual_complete_graph_private_inactive_audit_helper_admission_v25.json'
E=B/'actual_joint_helper_admission_v25_receipts'
SOURCE_PEER=B/'actual_joint_helper_admission_v25_sources/sealed_independent_actual_joint_Q_writer_Source_review'
Q_SHA='c6efd7accfdc897642853a286bd0c0fa7caac91879a02aaf34dae2d3e2162d9b'
Q_ID=[16777229,49455079,33188,1,689741,1791625657710648236,1791625657710648236]
rows=[];inputs={};meta={}

def require(label,value,evidence=None):
    if type(value)is not bool or value is not True:raise ValueError(label)
    if any(x['check']==label for x in rows):raise ValueError('duplicate aggregate check')
    d=dict(check=label,passed=True)
    if evidence is not None:d['evidence']=evidence
    rows.append(d)

def identity(p):
    s=p.lstat();return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def small_pin(p):
    p=Path(p);before=identity(p)
    if not stat.S_ISREG(before[2])or before[4]>4*2**20 or p.suffix in {'.gz','.sqlite','.db','.bin'}:raise ValueError('Source/small metadata only')
    b=p.read_bytes()
    if identity(p)!=before:raise ValueError('changed finite input')
    return dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=before),b

def pairs(items):
    d={}
    for k,v in items:
        if k in d:raise ValueError('duplicate JSON key')
        d[k]=v
    return d

def read(p,expected=None):
    p=Path(p);v,b=small_pin(p)
    if expected is not None and v['sha256']!=expected:raise ValueError('fixed small metadata SHA')
    d=json.loads(b,object_pairs_hook=pairs,parse_constant=lambda s:(_ for _ in()).throw(ValueError(s)))
    if small_pin(p)[0]!=v:raise ValueError('JSON input changed')
    inputs[str(p)]=v;meta[str(p)]=d
    return d

def shape(v,optional_size=False):
    if type(v)is not dict or type(v.get('path'))is not str or type(v.get('sha256'))is not str or len(v['sha256'])!=64 or any(c not in '0123456789abcdef'for c in v['sha256']):return False
    ids=v.get('identity',v.get('identity7'))
    if type(ids)is not list or len(ids)!=7 or any(type(x)is not int for x in ids):return False
    return ('size_bytes'not in v and optional_size)or(type(v.get('size_bytes'))is int and v['size_bytes']==ids[4]and v['size_bytes']>=0)

def normalize(v):
    ids=v.get('identity',v.get('identity7'))
    return dict(path=v['path'],sha256=v['sha256'],size_bytes=ids[4],identity=ids)

def exact(a,b,ordered=True):
    if type(a)is not type(b):return False
    if type(a)is dict:return(list(a)==list(b)if ordered else set(a)==set(b))and all(exact(a[k],b[k],ordered)for k in a)
    if type(a)is list:return len(a)==len(b)and all(exact(x,y,ordered)for x,y in zip(a,b))
    if type(a)is float:return math.isfinite(a)and math.isfinite(b)and struct.pack('>d',a)==struct.pack('>d',b)
    return a==b

def bound_small(pin):
    if not shape(pin):raise ValueError('exact 4-field actual metadata pin')
    d=read(pin['path'],pin['sha256'])
    if not exact(inputs[pin['path']],pin):raise ValueError('metadata 7ID/fullpin differs')
    return d

q=read(Q,Q_SHA);qp=inputs[str(Q)]
require('01_saved_Q_complete_EOF_SHA_exact_root_size_7integer_identity',qp['size_bytes']==689741 and qp['identity']==Q_ID)
require('02_new_V25_joint_helper_schema_status_exact_metadata_scope',q['schema']=='AXMAT_ROOT_COMPLETE_GRAPH_PRIVATE_INACTIVE_AUDIT_HELPER_ACTUAL_JOINT_ADMISSION_V25'and q['status']=='QUALIFIED_ORIGINAL_FULL_PROTOCOL_AND_COMPLETE_CURRENT_GRAPH_METADATA_VERIFIER_ONLY_V25'and q['scope']=='HELPER_METADATA_ORIGINAL_COMPLETE_PROTOCOL_AND_SAME_CURRENT_GRAPH_VERIFIER_ONLY_NO_WHOLE_INPUT_BUILD_NATIVE_OR_SCIENCE')
tool=read(E/'Root_actual_joint_helper_META_admission_writer_tool_terminal_return.json','537d9cc6fb49a7b378a7263ae617624e8b0ec841c2306b67e8c2c46baadd17e2')
tr=tool['terminal_tool_return'];out=json.loads(tr['output'],object_pairs_hook=pairs)
require('03_real_Root_writer_94520a_strict_integer0closed_observed_noSession_no_repoll',tool['schema']=='ROOT_V25_ACTUAL_JOINT_HELPER_META_ADMISSION_WRITER_TOOL_TERMINAL_RETURN_V1'and tool['closed']is True and tool['actual_tool_terminal_return_observed']is True and type(tr['exit_code'])is int and tr['exit_code']==0 and tr['chunk_id']=='94520a'and 'session_id'not in tr and tool['no_closed_session_repoll']is True)
require('04_raw_actual_stdout_full_Q_and_writer_pin_exact_no_float_integer_normalization',exact(out['actual_metadata_Q'],qp)and exact(out['actual_Source_writer'],q['Root_actual_Source_writer'])and exact(tool['observations'],[tr]))
require('05_real_actual_output_full13_full27_37112_55_42_and_false_science',out['full_protocol_fields']==13 and out['complete_return_fields']==27 and out['actual_complete_read_count']==37112 and out['pure_saved_review_checks']==55 and out['fresh_saved_review_checks']==42 and all(out[k]is False for k in ['whole_build_qualified','whole_INPUT_admitted','AAA_accuracy_qualified','ABA_admitted','candidate_or_API_or_numeric_executed']))
sourcepin,sourcebytes=small_pin(Path(q['Root_actual_Source_writer']['path']));ast.parse(sourcebytes)
require('06_exact_executed_writer_Source82a13aca_and_actual_SHA_CLI_coupling',sourcepin==q['Root_actual_Source_writer']and sourcepin['sha256']=='82a13aca3646491213a787c08ac9d611944f982943f34e4cbc18ec2695c84b71'and '--source-sha256 '+sourcepin['sha256']in tool['actual_command']['cmd']and tool['candidate_helper_guard_API_or_numeric_executed']is False)
inputs[sourcepin['path']]=sourcepin
rt=read(E/'Root_actual_joint_Q_writer_Source_peer_retention_record.json','72511e564b8196b18ec41a731148ba18b986416b77725727febacabd81f5d8cd')
rtool=read(E/'Root_actual_joint_Q_writer_Source_peer_retention_tool_returns.json','57df8e7b84ed3846551acaf1019268f03f9c640a55d41f780fe3133ce5adc1e7')
require('07_genuine_Root14a142_complete_source_peer_retention_no_new_Q',rtool['closed']is True and type(rtool['actual_complete_retention_tool_return']['exit_code'])is int and rtool['actual_complete_retention_tool_return']['exit_code']==0 and rtool['actual_complete_retention_tool_return']['chunk_id']=='14a142'and 'session_id'not in rtool['actual_complete_retention_tool_return']and rtool['new_helper_Q_created']is False and rt['source_only']is True and rt['new_qualification_created']is False and rt['helper_guard_business_executed']is False)
require('08_original_retainer_shape_failure_preserved_not_candidate_failure',type(rtool['initial_member_key_shape_failure_preserved']['exit_code'])is int and rtool['initial_member_key_shape_failure_preserved']['exit_code']==1 and rtool['initial_member_key_shape_failure_preserved']['chunk_id']=='b9202b')
require('09_full_source_peer8members_plus_actual_seal_nine_saved_files',rt['complete_original_member_count']==len(rt['complete_original_members'])==8 and all(shape(x['original'])and shape(x['saved'])and x['original']['sha256']==x['saved']['sha256']and x['original']['size_bytes']==x['saved']['size_bytes']for x in rt['complete_original_members'].values())and json.loads(rtool['actual_complete_retention_tool_return']['output'])['complete_saved_files_including_seal_receipt']==9)
peer65=bound_small(rt['complete_original_members']['REVIEW.json']['saved'])
require('10_source65_actual_fixed_fullpin_qualified_writer_scope',peer65['schema']=='INDEPENDENT_ROOT_V25_JOINT_INACTIVE_AUDIT_HELPER_Q_WRITER_SOURCE_REVIEW_V1'and peer65['status']=='SOURCE_ONLY_PASS_NO_WRITER_EXECUTION_OR_QUALIFICATION'and peer65['source_only']is True and peer65['all_checks_typed_true']is True and peer65['blockers']==[]and type(peer65['check_count'])is int and peer65['check_count']==len(peer65['checks'])==65 and all(type(x['passed'])is bool and x['passed']is True for x in peer65['checks'])and exact(peer65['qualified_Root_writer_Source_pin'],sourcepin))
p65tools=bound_small(rt['complete_original_members']['ACTUAL_SOURCE_REVIEW_TOOL_RETURNS.json']['saved']);p65seal=bound_small(rt['saved_actual_peer_seal_receipt'])
require('11_source65_genuine03e988_and92c9d0_strict0closed_receipts',type(p65tools['actual_success_tool_return']['exit_code'])is int and p65tools['actual_success_tool_return']['exit_code']==0 and p65tools['actual_success_tool_return']['chunk_id']=='03e988'and p65seal['closed']is True and type(p65seal['terminal_tool_return']['exit_code'])is int and p65seal['terminal_tool_return']['exit_code']==0 and p65seal['terminal_tool_return']['chunk_id']=='92c9d0')
require('12_source65_tool_output_original_report_SHA_coupled_to_retained_copy',json.loads(p65tools['actual_success_tool_return']['output'])['review_pin']==rt['complete_original_members']['REVIEW.json']['original']and peer65['candidate_helper_guard_controller_reader_API_or_numeric_executed']is False)
install=bound_small(q['actual_SOURCE_install_record']);it=bound_small(q['actual_SOURCE_install_tool_return'])
require('13_actual_V23_Source_install_same3b_helper_no_qualification',install['schema']=='ROOT_V23_COMPLETE_HELPER_SOURCE_INSTALL_RECORD_V1'and it['schema']=='ROOT_V23_ACTUAL_COMPLETE_HELPER_SOURCE_INSTALL_TOOL_RETURN_V1'and install['source_only']is True and it['source_only']is True and it['closed']is True and type(it['terminal_tool_return']['exit_code'])is int and it['terminal_tool_return']['exit_code']==0 and it['terminal_tool_return']['chunk_id']=='10a0e4'and it['new_Q']is None and exact(normalize(install['installed_helper']),q['helper'])and q['helper']['sha256']=='3b181f6366d5084fd6ccc87c1a6e7b757b706b7ba38cdf9156e1381cdb010092'and q['helper']['size_bytes']==150986)
require('14_helper_Source_actual_lstat_still_exact_installed_7ID',shape(q['helper'])and identity(Path(q['helper']['path']))==q['helper']['identity'])
families={}
for kind,data,chunk,count in [('pure',q,'ca2666',55),('fresh',q['complete_current_graph_fresh_verifier'],'d1d77b',42)]:
    summary=bound_small(data['actual_controls_summary']);terminal=bound_small(data['actual_root_terminal']);host=bound_small(data['actual_host_result']);report=bound_small(data['actual_control_report']);peer=bound_small(data['independent_actual_review']);ns=bound_small(data['complete_namespace_manifest']);freeze=bound_small(data['source_manifest']);retention=bound_small(data['independent_review_retention_record']);seal=bound_small(data['independent_review_actual_seal']);ptools=bound_small(data['independent_actual_review_tool_return'])
    prefix=kind+'_'
    require(prefix+'15_complete_real_summary_terminal_closed0_current_V25_family',summary['kind']==kind and summary['schema']=='ROOT_V25_ACTUAL_COMPLETE_HELPER_QUALIFICATION_POSTCLOSE_SUMMARY_V1'and summary['actual_closed']is True and type(summary['actual_exit_code'])is int and summary['actual_exit_code']==0 and summary['actual_terminal_chunk_id']==chunk and summary['actual_complete_control_success']is True and summary['actual_failure']is None and terminal['closed']is True and terminal['actual_tool_terminal_return_observed']is True and type(terminal['terminal_tool_return']['exit_code'])is int and terminal['terminal_tool_return']['exit_code']==0 and terminal['terminal_tool_return']['chunk_id']==chunk and 'session_id'not in terminal['terminal_tool_return'])
    require(prefix+'16_complete_original_saved_peer55_or42_typed_scope_and_tool',peer['source_only']is True and peer['all_checks_typed_true']is True and peer['blockers']==[]and type(peer['check_count'])is int and peer['check_count']==len(peer['checks'])==count and all(type(x['passed'])is bool and x['passed']is True for x in peer['checks'])and peer['new_actual_helper_qualification']is None)
    ptr=next(x['actual_tool_return']for x in ptools['records']if x['key']=='v25_actual_complete_pure_saved_Source_META_review_attempt1')if kind=='pure'else ptools['terminal_tool_return']
    require(prefix+'17_genuine_peer_review_and_seal_terminal_strict0closed',type(ptr['exit_code'])is int and ptr['exit_code']==0 and ptr['chunk_id']==('6fa312'if kind=='pure'else'514729')and 'session_id'not in ptr and seal['closed']is True and type(seal.get('terminal_tool_return',seal.get('actual_tool_return'))['exit_code'])is int and seal.get('terminal_tool_return',seal.get('actual_tool_return'))['exit_code']==0)
    pmapping={'actual_Root_pure_summary_pin':'actual_controls_summary','actual_Root_terminal_receipt_pin':'actual_root_terminal','actual_complete_HODE_namespace_manifest_pin':'complete_namespace_manifest'}if kind=='pure'else{'actual_Root_fresh_summary_pin':'actual_controls_summary','actual_Root_fresh_terminal_pin':'actual_root_terminal','actual_complete_namespace_manifest_pin':'complete_namespace_manifest'}
    require(prefix+'18_peer_current_original_metadata_pin_coupling',all(exact(peer[k],data[v])for k,v in pmapping.items()))
    require(prefix+'19_full_retention_exact_original_saved_no_Q_and_seal',retention['source_only']is True and retention['new_qualification_created']is False and retention['helper_guard_business_executed']is False and exact(retention['saved_actual_peer_seal_receipt'],data['independent_review_actual_seal'])and all(x['original']['sha256']==x['saved']['sha256']and x['original']['size_bytes']==x['saved']['size_bytes']for x in retention['complete_original_members'].values()))
    whole,stage=(60,60)if kind=='pure'else(1800,600);w=host['watchdog'];m=data['actual_measurement'];caps=dict(whole_seconds=whole,stage_seconds=stage,rss_mib=512,archive_bytes=64*2**20,history_bytes=96*2**30,free_bytes=8*2**30,threads=1,children=1,retries=0)
    require(prefix+'20_original_all_caps_and_genuine_measured_values_current',exact(m['original_caps'],caps)and m['whole_seconds']==summary['whole_host_seconds']==host['whole_seconds']<whole and m['child_seconds']==summary['actual_child_seconds']==w['elapsed_seconds']<stage and m['sampled_peak_rss_mib']==summary['actual_own_child_sampled_peak_RSS_MiB']==w['sampled_peak_rss_mib']<512 and w['own_child_only']is True and w['liveness_group_cleanup']is True and w['limit_failure']is None and type(w['returncode'])is int and w['returncode']==0 and host['profile_used']is False and host['supervisor_class_or_MRO_modified']is False)
    require(prefix+'21_original_archive_scope_and_current_saved_measurement_honest',m['actual_original_archive_bytes']==(summary['normal_HOD_bytes']if kind=='pure'else summary['complete_HODE_bytes'])and m['original_archive_scope']==summary['normal_host_archive_scope']and summary['original_normal_archive_under_cap']is True and m['actual_original_archive_bytes']<64*2**20)
    archives=freeze['lossless_complete_Source_archives'];views=ns['views'];links=views['O'].get('original_fixture_symlinks',[])
    require(prefix+'22_original_full_Source184199_D9or10_HODE_pin_shapes',len(views['D']['files'])==(9 if kind=='pure'else 10)and set(views)=={'H','O','D','E'}and all(type(v['files'])is list and all(shape(x)for x in v['files'])and type(v['directories'])is dict for v in views.values())and[len(x['full_decompressed_members'])for x in archives.values()]==[184,199]and all(x['all_member_bytes_and_SHA_verified_after_decompression']is True and x['no_original_member_omission']is True and x['runtime_Source_entrypoints_are_separate_original_bytes']is True for x in archives.values()))
    require(prefix+'23_two_pure_literal_symlinks_and_no_fresh_alias_omission',len(links)==(2 if kind=='pure'else 0)and all(type(x['symlink_target_text'])is str and shape(x['actual_resolved_target_full_EOF_pin'])and identity(Path(x['path']))==x['identity']and os.readlink(x['path'])==x['symlink_target_text']for x in links))
    families[kind]=dict(report=report,summary=summary,peer=peer)
pure=families['pure']['report'];fresh=families['fresh']['report'];protocol=q['full_protocol'];old=pure['full_old_saved_graph'];mt=old['complete_original_metadata'];trace=pure['full_new_creation_trace']
expected_protocol=dict(original_and_fresh_small_producer_values_types_order_floatbits_exact=True,all_caller_mutable_identity_and_subtype_attributes_unchanged=True,accepted_str_subtype_groups=len(pure['small_fixture']['accepted_str_subclass_equivalence_controls']),small_codec_rejections=pure['small_codecs']['rejections'],complete_original_graph_counts=mt['complete_counts'],complete_old_graph_two_normal_strict_entrances_exact=True,complete_old_legacy_semantic_sha256=mt['legacy_semantic_sha256'],complete_old_wire_content_sha256=mt['wire_content_sha256'],complete_new_creation_trace_records=trace['full_record_count'],complete_new_creation_trace_actual_attempts=trace['actual_attempt_count'],new_creation_trace_not_substituted_into_old_graph=True,full_json_types_order_floatbits_and_values_retained=True,default_source_nonmutation=True)
require('24_all_original13_protocol_fields_exact_types_order_values_from_actual_pure',len(protocol)==13 and exact(protocol,expected_protocol)and protocol['small_codec_rejections']==61 and protocol['accepted_str_subtype_groups']==2 and protocol['complete_new_creation_trace_records']==63379 and protocol['complete_new_creation_trace_actual_attempts']==175886)
require('25_complete_old_graph62332_not_substituted_and_all5_saved_stages',protocol['complete_original_graph_counts']['read_trace_records']==62332 and len(pure['stages'])==5 and old['old_read_trace_not_replaced_by_new_trace']is True and old['full_default_roundtrip_exact']is True)
oc=q['private_owner_consume_controls'];require('26_full_owner4positive3reject2subtypes2invalid_second_value_type_order_exact',exact(oc,pure['private_owner_consume_controls'])and[len(oc[k])for k in ['positive_controls','private_guard_rejections','accepted_str_subclass_equivalence_controls','partial_invalid_second_owner_rejections']]==[4,3,2,2])
snap=bound_small(q['private_inactive_audit_snapshot_controls_order_preserved_artifact']);sf=['schema','coverage','records','subprocess_records','unique_records','actual_read_open_attempts','record_storage','success_of_open_attempt_is_not_observed','native_libc_HDF5_loader_and_directory_stat_are_not_traced']
require('27_Q_full_ordered_artifact_exact_and_sorted_aggregate_distinction',exact(q['private_inactive_audit_snapshot_controls'],snap)and exact(snap,pure['private_inactive_audit_snapshot_controls'],False)and not exact(snap,pure['private_inactive_audit_snapshot_controls'],True))
require('28_all5positive13reject3failure_complete_snapshot_scope', [len(snap[k])for k in ['positive_controls','private_guard_rejections','last_use_failure_controls']]==[5,13,3]and all(list(x['actual_full_expected_snapshot'])==sf and exact(x['actual_full_expected_snapshot'],x['actual_full_consumed_snapshot']if i<3 else x['actual_full_default_snapshot'])for i,x in enumerate(snap['positive_controls'])))
require('29_lastuse_nontransactional_clone_failure_honestly_preserved',all(x['no_transactional_private_mode_promise']is True and x['original_error_class_and_message_retained']is True and x['both_callers_unchanged_before_clear_or_default']is(i<2)and x['private_clone_failure_after_clear_consumption_observed']is(i==2)for i,x in enumerate(snap['last_use_failure_controls'])))
require('30_same_real_Popen_observation_no_PID_FD_inode_normalization',snap['actual_same_observation_full_record_role_comparison']is True and snap['no_cross_process_PID_FD_inode_normalization']is True and list(snap['actual_single_Popen_observation'])==sf)
fd=q['complete_current_graph_fresh_verifier'];fc=fd['private_full_inactive_audit_snapshot_controls']
require('31_fresh27_return_fields_37112_all_current_reads_not_production_INPUT',exact(fd['all27_return_fields'],fresh['complete_return_fields_retained'])and len(fd['all27_return_fields'])==27 and exact(fd['complete_actual_read_counts'],fresh['actual_complete_trace_counts'])and fd['complete_actual_read_counts']['records']==37112 and fd['complete_actual_read_counts']['attempts']==37112 and fd['complete_actual_read_counts']['canonical_files']==37111)
require('32_fresh_all4positive3reject_and_full_saved_metadata_exact',exact(fd['private_trace_controls'],fresh['private_trace_controls'])and len(fd['private_trace_controls']['positive_controls'])==4 and len(fd['private_trace_controls']['rejections'])==3 and exact(fd['full_saved_graph_metadata'],fresh['independent_full_saved_graph_metadata']))
require('33_full_same_phase9_snapshot_779371nodes21411449wire_all_values_preserved',exact(fc,fresh['private_full_inactive_audit_snapshot_controls'])and fc['default_complete_descriptor_type_order_floatbit_pin']['complete_node_count']==779371 and exact(fc['default_complete_descriptor_type_order_floatbit_pin'],fc['consumed_complete_descriptor_type_order_floatbit_pin'])and fc['complete_consumed_vs_default_wire']['complete_nine_snapshot_fields']==sf and fc['complete_consumed_vs_default_wire']['uncompressed_JSON_bytes']==21411449 and fc['complete_consumed_vs_default_wire']['every_default_and_consumed_wire_byte_compared']is True and fc['all37112_actual_reads_from_same_genuine_phase']is True and fc['no_second_graph_or_input_phase_substituted']is True)
gkeys=['expected_complete_return_contract','actual_complete_verifier_return','actual_complete_ReadOpenAudit_trace']
require('34_all_three_full_original_gzip_evidence_pins_exact_no_payload_replay',list(fd['complete_gzip_pins'])==gkeys and all(exact(fd['complete_gzip_pins'][k],fresh[k])and shape(fresh[k])and fresh[k]['complete_JSON_wire_gzip_decompression_EOF_SHA_verified']is True and fresh[k]['no_fields_or_records_filtered']is True for k in gkeys)and fresh[gkeys[0]]['sha256']==fresh[gkeys[1]]['sha256'])
require('35_Q_counts_Source_members_caps_complete_current_not_old_qualification',exact(q['independent_saved_review_counts'],dict(pure=55,fresh=42,auxiliary_pure_small_controls=136))and q['lossless_complete_original_Source_files_per_family']==[184,199]and q['pure_source_member_count']==9 and q['fresh_source_member_count']==10 and exact(q['original_caps'],q['actual_measurement']['original_caps']))
falsekeys=['fresh_production_graph_created','fresh_runtime_INPUT_qualified','new_combined_prepared','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted','whole_build_qualified','whole_INPUT_admitted','physical_balance_qualified','canonical_wired']
require('36_all_whole_build_INPUT_native_and_science_flags_exact_false',all(q[k]is False for k in falsekeys)and q['supervisor_class_or_MRO_modified']is False and q['profile_used']is False and q['Root_finite_joint_META_only_no_project_API_or_numeric']is True)
records=q['Root_finite_joint_META_full_EOF_SHA7ID_verified_unique_inputs']
require('37_all310_Root_input_pin_descriptors_unique_typed_and_current_lstat_only',len(records)==310 and len({x['path']for x in records})==310 and all(shape(x)and identity(Path(x['path']))==x['identity']for x in records))
require('38_all_reviewed_small_Q_Source_proof_before_after_unchanged',all(small_pin(Path(k))[0]==v for k,v in inputs.items()))
for name,data in [('ACTUAL_SAVED_V25_HELPER_ONLY_Q.json',Q.read_bytes()),('ACTUAL_ROOT_JOINT_Q_WRITER_TOOL_RECEIPT.json',Path(E/'Root_actual_joint_helper_META_admission_writer_tool_terminal_return.json').read_bytes()),('REVIEWED_EXECUTED_ROOT_Q_WRITER_SOURCE.py',sourcebytes)]:
    with(P/name).open('xb')as f:f.write(data)
require('39_complete_Q_copy_and_root_proof_original_bytes_no_normalization',small_pin(P/'ACTUAL_SAVED_V25_HELPER_ONLY_Q.json')[0]['sha256']==Q_SHA and small_pin(P/'ACTUAL_ROOT_JOINT_Q_WRITER_TOOL_RECEIPT.json')[1]==Path(E/'Root_actual_joint_helper_META_admission_writer_tool_terminal_return.json').read_bytes())
report=dict(schema='INDEPENDENT_V25_ACTUAL_JOINT_HELPER_Q_SAVED_META_REVIEW_V1',status='PASS_ACTUAL_JOINT_HELPER_Q_METADATA_ONLY',source_only=True,all_checks_typed_true=True,blockers=[],check_count=len(rows),checks=rows,Root_actual_Q_pin=qp,Root_actual_Q_writer_terminal_pin=inputs[str(E/'Root_actual_joint_helper_META_admission_writer_tool_terminal_return.json')],Root_actual_Q_writer_Source_pin=sourcepin,Root_actual_writer_terminal_chunk='94520a',actual_source_peer_retention_record_pin=inputs[str(E/'Root_actual_joint_Q_writer_Source_peer_retention_record.json')],explicit_complete_small_Source_META_input_pins=list(inputs.values()),actual_saved_helper_metadata_qualification_verified=True,qualification_scope=q['scope'],whole_build_qualified=False,whole_INPUT_admitted=False,native_RSS_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,physical_balance_qualified=False,candidate_helper_writer_guard_API_or_numeric_executed=False,large_graph_trace_gzip_SQLite_material_or_Source_archive_member_payload_read=False,Root310_input_metadata_pins_current_lstat_verified=True,Root310_input_payloads_not_rehashed_by_this_reviewer=True,E_root_identity_after_append_not_claimed_unchanged=True,live_object_identity_floatbits_and_full_gzip_replay_not_repeated_by_this_review=True)
with(P/'REVIEW.json').open('x')as f:json.dump(report,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n')
with(P/'REPORT.txt').open('x')as f:f.write('PASS_ACTUAL_JOINT_HELPER_Q_METADATA_ONLY\n'+str(len(rows))+' finite unique exact-bool aggregate checks. Genuine Root writer94520a typed0 CLOSED and actual Q c6efd7...2d9b are fully coupled.\nOriginal13 protocol + owner4/3/2/2 + new5/13/3 honest nontransactional clone-failure + fresh27/37112/4+3/full9 same-phase wire metadata retained.\nSource65, actual retention14a142, V23 actual Source-only install3b, V25 saved peers55/42, original184/199 Sources/D9/10/allcaps retained.\nAll310 declared Root input pins have exact integer metadata/current lstat; no large payload rehash or gzip/control replay by this reviewer.\nOnly helper metadata qualification. No new whole INPUT/build/native/RAM/science credit; AAA7/8 and ABA unstarted remain outside this scope.\nOriginal Q and Root proof full before/after unchanged.\n')
print(json.dumps(dict(status=report['status'],source_only=True,check_count=len(rows),review_pin=small_pin(P/'REVIEW.json')[0],Root_actual_Q_pin=qp,Root_actual_Q_writer_terminal_pin=report['Root_actual_Q_writer_terminal_pin'],all_checks_typed_true=True,whole_build_qualified=False,whole_INPUT_admitted=False,AAA_accuracy_qualified=False,ABA_admitted=False,candidate_helper_API_or_numeric_executed=False)))
