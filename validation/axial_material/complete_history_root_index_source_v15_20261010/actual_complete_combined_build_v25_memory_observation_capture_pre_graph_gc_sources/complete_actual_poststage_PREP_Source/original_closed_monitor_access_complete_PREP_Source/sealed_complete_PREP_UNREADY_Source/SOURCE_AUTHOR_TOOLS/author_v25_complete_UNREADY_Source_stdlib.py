"""SOURCE author only: no reviewed module imports or candidate execution."""
import ast
import hashlib
import json
import os
from pathlib import Path
import stat

P=Path('/private/tmp/axmat_v25_complete_canonical_TRUE_snapshot_jointQ_UNREADY_SOURCE_bwo0x_85')
R=Path('/Users/wen/spot'); B=R/'validation/axial_material/complete_history_root_index_source_v15_20261010'
C=R/'validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v22.py'
OLD_HELPER='combined_runtime_complete_input_graph_private_owner_namespace_last_use_20261010.py'
NEW_HELPER='combined_runtime_complete_input_graph_private_inactive_audit_snapshot_consume_20261010.py'
OLD_HSHA='cf0c2b6b6fd6b1adceec85b261008871f12769832b4dbd4fdb4204f650b4e72c'
NEW_HSHA='3b181f6366d5084fd6ccc87c1a6e7b757b706b7ba38cdf9156e1381cdb010092'
OLD_Q='Root_actual_complete_graph_private_owner_namespace_helper_admission_v22.json'
NEW_Q='Root_actual_complete_graph_private_inactive_audit_helper_admission_v25.json'
OLD_QSHA='89d2f03c0af74844731ddf5225307c38ae40521d99ca29c88c5d8db39796b816'
OLD_CSHA='09e53974005082a14d9675f69258549609a991f86ec231ab6b15edfe20dd265e'
BUSINESS=('FUTURE_ACTUAL_COMBINED_DECLARATION_SHA','FUTURE_ACTUAL_COMBINED_PREP_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_SEAL_SHA','FUTURE_ACTUAL_COMBINED_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_RUNTIME_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA')
parents={
 'canonical':C,
 'prepare_host':B/'actual_complete_combined_prepare_v22_sources/combined_prepare_host.py',
 'prepare_writer':B/'actual_complete_combined_prepare_v22_sources/write_actual_prepare_terminal.py',
 'build_host':B/'actual_complete_combined_build_v22_sources/combined_build_host.py',
 'build_writer':B/'actual_complete_combined_build_v22_sources/write_actual_build_postclose_META.py',
 'PREP_binder':B/'actual_complete_combined_prepare_v22_sources/sealed_complete_PREP_UNREADY_Source/bind_actual_Q_to_complete_PREP_SOURCE.py',
 'BUILD_binder':B/'actual_complete_combined_build_v22_sources/actual_bound_full_build_SOURCE/ROOT_ACTUAL_FULL_BUILD_SOURCE_binding_writer.py',
 'old_graph_helper':R/('validation/axial_material/'+OLD_HELPER),
 'installed_new_graph_helper':R/('validation/axial_material/'+NEW_HELPER),
}

def identity(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 i=identity(p);assert stat.S_ISREG(i[2]) and not p.is_symlink()
 raw=p.read_bytes();assert identity(p)==i
 return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=i)
def dump(p,v):
 with p.open('x') as f:json.dump(v,f,indent=2,allow_nan=False);f.write('\n')
def defs(text):
 return {n.name:ast.get_source_segment(text,n) for n in ast.parse(text).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}
def edit(text,rows,label,old,new,count=None):
 n=text.count(old);assert n>0 and old!=new,(label,n)
 if count is not None:assert n==count,(label,n,count)
 rows.append(dict(label=label,old=old,new=new,count=n));return text.replace(old,new)
def inverse(text,rows):
 for row in reversed(rows):
  assert text.count(row['new'])==row['count'],row['label']
  text=text.replace(row['new'],row['old'])
 return text
def version(text,rows):
 for old,new in (
  ('prepare_sender_window_root_index_graph_trace_table_combined_runtime_v22.py','prepare_sender_window_root_index_graph_trace_table_combined_runtime_v25.py'),
  ('axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v22-20261010','axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v25-20261010'),
  ('axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v22-20261010','axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v25-20261010'),
  ('axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v22-20261010','axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v25-20261010'),
  ('axial-material-complete-combined-prepare-host-v22-20261010','axial-material-complete-combined-prepare-host-v25-20261010'),
  ('axial-material-complete-combined-build-host-v22-20261010','axial-material-complete-combined-build-host-v25-20261010'),
  ('actual_complete_combined_prepare_v22_sources','actual_complete_combined_prepare_v25_sources'),
  ('actual_complete_combined_prepare_v22_receipts','actual_complete_combined_prepare_v25_receipts'),
  ('actual_complete_combined_build_v22_sources','actual_complete_combined_build_v25_sources'),
  ('actual_complete_combined_build_v22_receipts','actual_complete_combined_build_v25_receipts'),
  ('SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_LINK_V22','SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_LINK_V25'),
  ('AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V22','AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V25'),
  ('AXMAT_V22_GENUINE_COMPLETE_COMBINED','AXMAT_V25_GENUINE_COMPLETE_COMBINED'),
  ('ROOT_V22_ACTUAL_COMPLETE','ROOT_V25_ACTUAL_COMPLETE'),
 ):
  if old in text:text=edit(text,rows,'namespace_'+old,old,new)
 return text

# These functions are authored SOURCE, never evaluated by this author. They
# use the canonical's original strict read/ordinary/hash functions. No helper
# API is called; input payload pins are enforced in the original whole graph.
CONTRACT=r'''

def helper_Q_check(value,message):
    if type(value)is not bool or not value:raise ValueError('actual helper Q: '+message)


def helper_Q_fullpin(value):
    helper_Q_check(type(value)is dict and type(value.get('path'))is str,'full pin path')
    ids=value.get('identity',value.get('identity7'))
    helper_Q_check(type(ids)is list and len(ids)==7 and all(type(x)is int for x in ids),'exact seven integer identity')
    if 'identity'in value and 'identity7'in value:helper_Q_check(value['identity']==value['identity7'],'identity aliases')
    helper_Q_check(stat.S_ISREG(ids[2]) and ids[4]>=0,'regular saved full pin')
    nonzero_sha(value['sha256']);normal(value['path'])
    if 'size_bytes'in value:helper_Q_check(type(value['size_bytes'])is int and value['size_bytes']==ids[4],'pin size')
    return dict(path=value['path'],sha256=value['sha256'],size_bytes=ids[4],identity=ids)


def helper_Q_verify_META(value):
    wanted=helper_Q_fullpin(value);p=require(wanted['path'],wanted['sha256']);s=p.lstat()
    actual=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
    helper_Q_check(actual==wanted['identity'],'core META identity differs')
    result=read(p)
    helper_Q_check(digest(p)==wanted['sha256'] and [x for x in (p.lstat().st_dev,p.lstat().st_ino,p.lstat().st_mode,p.lstat().st_nlink,p.lstat().st_size,p.lstat().st_mtime_ns,p.lstat().st_ctime_ns)]==wanted['identity'],'core META changed')
    return result


def helper_Q_exact(a,b,ordered=True):
    if type(a)is not type(b):return False
    if type(a)is dict:return (list(a)==list(b)if ordered else set(a)==set(b))and all(helper_Q_exact(a[k],b[k],ordered)for k in a)
    if type(a)is list:return len(a)==len(b)and all(helper_Q_exact(x,y,ordered)for x,y in zip(a,b))
    if type(a)is float:return math.isfinite(a)and math.isfinite(b)and a.hex()==b.hex()
    return a==b


def helper_Q_closed0(value,chunk):
    helper_Q_check(type(value)is dict and value.get('chunk_id')==chunk and type(value.get('exit_code'))is int and value['exit_code']==0 and 'session_id'not in value,'actual closed integer-zero terminal')


def helper_Q_collect_refs(value,refs):
    if type(value)is dict:
        if 'path'in value and 'sha256'in value and ('identity'in value or 'identity7'in value):
            row=helper_Q_fullpin(value);old=refs.get(row['path'])
            helper_Q_check(old is None or old==row,'conflicting full endpoint pins');refs[row['path']]=row
        for item in value.values():helper_Q_collect_refs(item,refs)
    elif type(value)is list:
        for item in value:helper_Q_collect_refs(item,refs)


def helper_Q_admission():
    """Read new actual Q and complete core proofs; no project/helper API.

    Every declared full EOF input and recursively stated core proof pin is an
    explicit typed owner. This does not filter a trace or grant scientific
    credit. Large graph/trace/gzip payloads are not decoded by this reader;
    their expected hashes are enforced by the original complete fresh phases.
    """
    path=require(ACTUAL_HELPER_Q_PATH,nonzero_sha(FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA))
    first=path.lstat();q=read(path)
    helper_Q_check(q['schema']==ACTUAL_HELPER_Q_SCHEMA and q['status']==ACTUAL_HELPER_Q_STATUS,'new helper-only schema/status')
    refs={};helper_Q_collect_refs(q,refs)
    hp=helper_Q_fullpin(q['helper'])
    helper_Q_check(hp['path']==str(INPUT_HELPERS['graph'][0]) and hp['sha256']==INPUT_HELPERS['graph'][1] and hp['size_bytes']==150986,'same installed 3b helper')
    helper_Q_check(hp['identity']==[16777229,49430225,33188,1,150986,1791616446797499263,1791616446797506096],'actual installed Source identity')
    require(hp['path'],hp['sha256'])
    for k in ('supervisor_class_or_MRO_modified','profile_used','fresh_production_graph_created','fresh_runtime_INPUT_qualified','new_combined_prepared','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted','whole_build_qualified','whole_INPUT_admitted','physical_balance_qualified','canonical_wired'):helper_Q_check(q[k]is False,k+' remains false')
    for k in ('Root_finite_joint_META_only_no_project_API_or_numeric','original_protocol_preserved_and_new_owner_controls_independently_saved_reviewed','original_protocol_and_new_snapshot_controls_and_full_current_graph_independently_saved_reviewed'):helper_Q_check(q[k]is True,k)
    helper_Q_check(q['scope']=='HELPER_METADATA_ORIGINAL_COMPLETE_PROTOCOL_AND_SAME_CURRENT_GRAPH_VERIFIER_ONLY_NO_WHOLE_INPUT_BUILD_NATIVE_OR_SCIENCE','qualification scope')
    declared=q['Root_finite_joint_META_full_EOF_SHA7ID_verified_unique_inputs']
    helper_Q_check(type(declared)is list and len(declared)>0,'complete declared Root EOF inputs')
    complete={}
    for row in declared:
        row=helper_Q_fullpin(row);helper_Q_check(row['path']not in complete,'unique full Root input');complete[row['path']]=row
    helper_Q_check(all(p in complete and complete[p]==r for p,r in refs.items()),'no core endpoint outside complete Root input set')
    proto=q['full_protocol']
    helper_Q_check(list(proto)==['original_and_fresh_small_producer_values_types_order_floatbits_exact','all_caller_mutable_identity_and_subtype_attributes_unchanged','accepted_str_subtype_groups','small_codec_rejections','complete_original_graph_counts','complete_old_graph_two_normal_strict_entrances_exact','complete_old_legacy_semantic_sha256','complete_old_wire_content_sha256','complete_new_creation_trace_records','complete_new_creation_trace_actual_attempts','new_creation_trace_not_substituted_into_old_graph','full_json_types_order_floatbits_and_values_retained','default_source_nonmutation'],'all original thirteen protocol fields/order')
    for k in ('original_and_fresh_small_producer_values_types_order_floatbits_exact','all_caller_mutable_identity_and_subtype_attributes_unchanged','complete_old_graph_two_normal_strict_entrances_exact','new_creation_trace_not_substituted_into_old_graph','full_json_types_order_floatbits_and_values_retained','default_source_nonmutation'):helper_Q_check(proto[k]is True,k)
    for k,n in (('accepted_str_subtype_groups',2),('small_codec_rejections',61),('complete_new_creation_trace_records',63379),('complete_new_creation_trace_actual_attempts',175886)):helper_Q_check(type(proto[k])is int and proto[k]==n,k)
    for k,n in (('canonical_files',36776),('requirements',237767),('read_trace_records',62332)):helper_Q_check(type(proto['complete_original_graph_counts'][k])is int and proto['complete_original_graph_counts'][k]==n,'old complete '+k)
    nonzero_sha(proto['complete_old_legacy_semantic_sha256']);nonzero_sha(proto['complete_old_wire_content_sha256'])
    owner=q['private_owner_consume_controls']
    helper_Q_check(owner['schema']=='AXMAT_V22_PRIVATE_OWNER_CONSUME_ACTUAL_CONTROL_V1' and [len(owner[k])for k in ('positive_controls','private_guard_rejections','accepted_str_subclass_equivalence_controls','partial_invalid_second_owner_rejections')]==[4,3,2,2],'original owner controls complete')
    for row in owner['positive_controls']:
        helper_Q_check(row['full_normalized_descriptor_types_order_values_attrs_floatbits_equal_default']is True and helper_Q_exact(row['expected_complete_descriptor_signature'],row['actual_complete_descriptor_signature']),'whole owner signatures')
        field='owned_list_completely_cleared_after_success'if row['case']=='owned_builtin_list_True'else'caller_full_identity_type_order_value_attrs_floatbits_unchanged';helper_Q_check(row[field]is True,field)
    for row in owner['private_guard_rejections']:helper_Q_check(row['class']=='InputGraphError' and row['message']=='private owner consume needs a bool and an exclusively owned builtin list' and row['caller_full_identity_type_order_value_attrs_floatbits_unchanged']is True,'original private owner reject')
    for row in owner['accepted_str_subclass_equivalence_controls']:helper_Q_check(row['default_caller_full_identity_type_order_value_attrs_floatbits_unchanged']is True and row['owned_list_completely_cleared_after_success']is True and row['complete_normalized_descriptor_types_order_value_strattrs_floatbits_equal_default']is True and helper_Q_exact(row['expected_complete_descriptor_signature'],row['actual_complete_descriptor_signature']),'whole owner subtype signature')
    for row in owner['partial_invalid_second_owner_rejections']:helper_Q_check(row['class']=='InputGraphError' and row['message']=='missing file owner','original partial rejection')
    for k in ('first_valid_slot_None_after_original_validate_and_append','invalid_second_slot_original_identity_and_value_unchanged','default_partial_caller_unchanged','original_owner_rejection_class_order_message_preserved','original_protocol_controls_fixtures_and_caps_unchanged','no_new_fixture_file_or_IO_created'):helper_Q_check(owner[k]is True,k)
    helper_Q_check(owner['new_helper_qualification_created']is False and owner['business_or_science_qualification_created']is False,'owner control scope')
    snapshot=q['private_inactive_audit_snapshot_controls'];artifact=helper_Q_verify_META(q['private_inactive_audit_snapshot_controls_order_preserved_artifact'])
    helper_Q_check(helper_Q_exact(snapshot,artifact,False),'complete ordered snapshot artifact equals sorted aggregate semantically')
    helper_Q_check(snapshot['schema']=='PRIVATE_INACTIVE_READ_OPEN_AUDIT_COMPLETE_SNAPSHOT_CONTROLS_V1' and snapshot['status']=='ACTUAL_PRIVATE_SNAPSHOT_CONTROLS_RETURNED_METADATA_ONLY' and [len(snapshot[k])for k in ('positive_controls','private_guard_rejections','last_use_failure_controls')]==[5,13,3],'all new snapshot cases')
    nine=['schema','coverage','records','subprocess_records','unique_records','actual_read_open_attempts','record_storage','success_of_open_attempt_is_not_observed','native_libc_HDF5_loader_and_directory_stat_are_not_traced']
    for i,row in enumerate(artifact['positive_controls']):
        helper_Q_check(row['default_and_explicitFalse_complete_state_unchanged']is True and row['all_nine_fields_nested_types_order_values_attrs_floatbits_equal_default']is True,'default and nine fields')
        if i<3:helper_Q_check(row['owned_same_builtin_records_map_completely_cleared']is True and row['all_other_audit_state_and_actual_Popen_references_unchanged']is True and list(row['actual_full_expected_snapshot'])==nine and helper_Q_exact(row['actual_full_expected_snapshot'],row['actual_full_consumed_snapshot']),'same actual owned snapshot/reference order')
        else:helper_Q_check(row['private_True_not_permitted_for_subclass']is True,'default subclass compatibility')
    for row in artifact['private_guard_rejections']:helper_Q_check(row['rejected']is True and row['class_name']=='InputGraphError' and row['complete_audit_state_identity_type_order_value_bits_unchanged']is True,'all private snapshot guard rejections')
    helper_Q_check([r['case']for r in artifact['last_use_failure_controls']]==['invalid_second_row_before_clear','missing_attempt_count_before_clear','nonfinite_clone_after_clear'],'last use failure order')
    for i,row in enumerate(artifact['last_use_failure_controls']):helper_Q_check(row['original_error_class_and_message_retained']is True and row['no_transactional_private_mode_promise']is True and row['both_callers_unchanged_before_clear_or_default']is(i<2) and row['private_clone_failure_after_clear_consumption_observed']is(i==2),'honest clone-after-clear nontransactional boundary')
    for k in ('actual_same_observation_full_record_role_comparison','no_cross_process_PID_FD_inode_normalization','default_original_complete_protocol_preserved'):helper_Q_check(artifact[k]is True,k)
    helper_Q_check(type(artifact['actual_child_returncode'])is int and artifact['actual_child_returncode']==0,'same actual Popen return')
    for k in ('native_or_numeric_component_executed','helper_qualification_created','business_or_science_qualification_created'):helper_Q_check(artifact[k]is False,k)
    helper_Q_check(helper_Q_exact(q['original_caps'],q['actual_measurement']['original_caps']),'top original pure caps equal actual measurement caps')
    f=q['complete_current_graph_fresh_verifier']
    public27=['schema','classification','consumer_scope','consumer_selected_literal_and_canonical_paths','consumer_complete_namespace_root_sequence','scope','phase','graph_content_sha256','fresh_reader_contract','canonical_files_read','actual_bytes_read','byte_count_scope','logical_owner_requirements','exhaustive_namespaces_checked','explicit_aliases_checked','coverage','trace_coverage','live_io_scope','live_subprocesses_reexecuted','declared_absence_inputs_checked_before_and_after_bytes','absence_inputs_are_not_regular_bytes_or_science','caller_must_recheck_current_OS_identity_and_live_probe_results','typed_snapshot','science_qualification_created','live_resources_verified','external_declaration_exit0_verified','caller_must_verify_live_environment_modules_PID_time_and_resources']
    helper_Q_check(f['all27_return_fields']==public27 and f['complete_actual_read_counts']==dict(records=37112,attempts=37112,canonical_files=37111,external_graph_reads=1,no_subprocess_reexecuted=True),'full 27 and unfiltered reads')
    pc=f['private_trace_controls'];helper_Q_check(len(pc['positive_controls'])==4 and len(pc['rejections'])==3,'whole trace control scope')
    for row in pc['positive_controls']:helper_Q_check(row['full_normalized_return_type_order_value_floatbits_and_bytes_equal_old_bcd']is True,'full trace normalized return')
    for row in pc['rejections']:helper_Q_check(row['rejected']is True and row['class_name']=='InputGraphError' and row['caller_type_identity_nested_value_order_floatbits_unchanged']is True,'private trace rejects')
    fc=f['private_full_inactive_audit_snapshot_controls']
    for k in ('default_snapshot_full_original_records_unchanged','owned_same_builtin_records_map_completely_cleared','all_other_audit_state_unchanged','all_nine_fields_full_type_order_value_floatbits_and_counts_equal','no_second_graph_or_input_phase_substituted','all37112_actual_reads_from_same_genuine_phase','no_cross_phase_hash_or_stat_cache'):helper_Q_check(fc[k]is True,k)
    helper_Q_check(helper_Q_exact(fc['default_complete_descriptor_type_order_floatbit_pin'],fc['consumed_complete_descriptor_type_order_floatbit_pin']) and fc['default_complete_descriptor_type_order_floatbit_pin']['complete_node_count']==779371,'complete same-phase descriptor')
    wire=fc['complete_consumed_vs_default_wire'];helper_Q_check(wire['complete_nine_snapshot_fields']==nine and type(wire['uncompressed_JSON_bytes'])is int and wire['uncompressed_JSON_bytes']==21411449 and wire['every_default_and_consumed_wire_byte_compared']is True and wire['full_gzip_EOF_verified']is True,'full same-phase snapshot wire')
    gz=f['complete_gzip_pins'];helper_Q_check(list(gz)==['expected_complete_return_contract','actual_complete_verifier_return','actual_complete_ReadOpenAudit_trace'],'all three original complete gzip endpoints')
    for item in gz.values():helper_Q_fullpin(item);helper_Q_check(item['complete_JSON_wire_gzip_decompression_EOF_SHA_verified']is True and item['no_fields_or_records_filtered']is True,'full gzip declaration')
    helper_Q_check(gz['expected_complete_return_contract']['sha256']==gz['actual_complete_verifier_return']['sha256'] and gz['expected_complete_return_contract']['uncompressed_JSON_sha256']==gz['actual_complete_verifier_return']['uncompressed_JSON_sha256'],'whole expected/current return bytes')
    core=['actual_root_terminal','actual_controls_summary','actual_host_result','actual_control_report','complete_namespace_manifest','independent_actual_review','independent_actual_review_tool_return','source_manifest','independent_review_retention_record','independent_review_actual_seal']
    for family,kind,chunk,count in ((q,'pure','ca2666',55),(f,'fresh','d1d77b',42)):
        data={k:helper_Q_verify_META(family[k])for k in core}
        term=data['actual_root_terminal'];helper_Q_check(term['schema']=='ROOT_V25_ACTUAL_COMPLETE_HELPER_QUALIFICATION_TOOL_TERMINAL_RETURN_V1' and term['closed']is True and term['actual_tool_terminal_return_observed']is True and term['new_actual_helper_qualification']is None,'actual '+kind+' Root terminal scope');helper_Q_closed0(term['terminal_tool_return'],chunk)
        summary=data['actual_controls_summary'];helper_Q_check(summary['schema']=='ROOT_V25_ACTUAL_COMPLETE_HELPER_QUALIFICATION_POSTCLOSE_SUMMARY_V1' and summary['kind']==kind and summary['actual_closed']is True and type(summary['actual_exit_code'])is int and summary['actual_exit_code']==0 and summary['actual_complete_control_success']is True and summary['actual_failure']is None and summary['actual_terminal_chunk_id']==chunk,'actual full '+kind+' success')
        helper_Q_check(summary['whole_frozen_D_E_files_and_directories_unchanged_before_writer']is True and summary['original_normal_archive_under_cap']is True and summary['new_actual_helper_qualification']is None,'complete original '+kind+' freeze/archive')
        for key,ref in (('actual_terminal_receipt',family['actual_root_terminal']),('namespace_manifest',family['complete_namespace_manifest'])):helper_Q_check(helper_Q_fullpin(summary[key])==helper_Q_fullpin(ref),'summary full endpoint coupling')
        host=data['actual_host_result'];watch=host['watchdog'];helper_Q_check(type(watch['returncode'])is int and watch['returncode']==0 and watch['limit_failure']is None and watch['own_child_only']is True and watch['liveness_group_cleanup']is True,'genuine '+kind+' own child')
        helper_Q_check(helper_Q_fullpin(host['actual_control_report'])==helper_Q_fullpin(family['actual_control_report']),'host/report binding')
        whole,stage=(60,60)if kind=='pure'else(1800,600)
        cap=dict(whole_seconds=whole,stage_seconds=stage,rss_mib=512,archive_bytes=64*2**20,history_bytes=96*2**30,free_bytes=8*2**30,threads=1,children=1,retries=0)
        helper_Q_check(helper_Q_exact(family['actual_measurement']['original_caps'],cap),'original '+kind+' caps')
        for k,n in (('whole_wall_cap_seconds',whole),('stage_wall_cap_seconds',stage),('rss_cap_mib',512),('archive_cap_bytes',64*2**20),('threads',1),('children_at_once',1),('retries',0)):helper_Q_check(type(host[k])is int and host[k]==n,'host '+k)
        helper_Q_check(host['profile_used']is False and host['supervisor_class_or_MRO_modified']is False,'original class/MRO/profile')
        m=family['actual_measurement'];helper_Q_check(0<=m['whole_seconds']==summary['whole_host_seconds']==host['whole_seconds']<whole and 0<=m['child_seconds']==summary['actual_child_seconds']==watch['elapsed_seconds']<watch['wall_cap_seconds']<=stage and 0<=m['sampled_peak_rss_mib']==summary['actual_own_child_sampled_peak_RSS_MiB']==watch['sampled_peak_rss_mib']<512,'actual measurements bound')
        helper_Q_check(type(m['actual_original_archive_bytes'])is int and m['actual_original_archive_bytes']<64*2**20 and m['actual_original_archive_bytes']==summary['normal_HOD_bytes'if kind=='pure'else'complete_HODE_bytes'],'actual original archive measure')
        peer=data['independent_actual_review'];helper_Q_check(peer['schema']=='INDEPENDENT_V25_ACTUAL_SUCCESS_PRIVATE_INACTIVE_AUDIT_'+kind.upper()+'_SAVED_SOURCE_META_REVIEW_V1' and peer['status']==('PASS_SAVED_ACTUAL_PURE_CONTROLS_SOURCE_META_ONLY'if kind=='pure'else'PASS_SAVED_ACTUAL_COMPLETE_FRESH_VERIFIER_SOURCE_META_ONLY') and peer['source_only']is True and peer['all_checks_typed_true']is True and peer['blockers']==[] and type(peer['check_count'])is int and peer['check_count']==len(peer['checks'])==count and all(type(row['passed'])is bool and row['passed']is True for row in peer['checks']) and peer['new_actual_helper_qualification']is None,'full saved '+kind+' independent review')
        mapping={'actual_Root_pure_summary_pin':'actual_controls_summary','actual_Root_terminal_receipt_pin':'actual_root_terminal','actual_complete_HODE_namespace_manifest_pin':'complete_namespace_manifest'}if kind=='pure'else{'actual_Root_fresh_summary_pin':'actual_controls_summary','actual_Root_fresh_terminal_pin':'actual_root_terminal','actual_complete_namespace_manifest_pin':'complete_namespace_manifest'}
        for pk,fk in mapping.items():helper_Q_check(helper_Q_fullpin(peer[pk])==helper_Q_fullpin(family[fk]),'saved peer three complete endpoint pins')
        tool=data['independent_actual_review_tool_return']
        if kind=='pure':
            observed=[row['actual_tool_return']for row in tool['records']if row['key']=='v25_actual_complete_pure_saved_Source_META_review_attempt1'];helper_Q_check(len(observed)==1 and tool['own_review_terminal_closed_strict_EXIT0']is True,'actual pure peer closed');helper_Q_closed0(observed[0],'6fa312')
        else:helper_Q_check(tool['closed']is True and tool['actual_tool_terminal_return_observed']is True,'actual fresh peer closed');helper_Q_closed0(tool['terminal_tool_return'],'514729')
        seal=data['independent_review_actual_seal'];helper_Q_check(seal['closed']is True,'actual independent seal closed');tr=seal.get('terminal_tool_return',seal.get('exec_command_result',seal.get('actual_tool_return')));helper_Q_check(type(tr)is dict and type(tr.get('exit_code'))is int and tr['exit_code']==0 and 'session_id'not in tr,'actual independent seal integer zero')
        retention=data['independent_review_retention_record'];helper_Q_check(retention['source_only']is True and retention['new_qualification_created']is False and retention['helper_guard_business_executed']is False and helper_Q_fullpin(retention['saved_actual_peer_seal_receipt'])==helper_Q_fullpin(family['independent_review_actual_seal']),'complete saved review retention')
        report=data['actual_control_report'];helper_Q_check(helper_Q_exact(report['private_owner_consume_controls'],owner),'original complete owner/report equality')if kind=='pure'else helper_Q_check(report['complete_return_fields_retained']==public27 and report['actual_complete_trace_counts']==f['complete_actual_read_counts'] and helper_Q_exact(report['private_trace_controls'],pc) and helper_Q_exact(report['private_full_inactive_audit_snapshot_controls'],fc),'complete fresh report equality')
        if kind=='pure':helper_Q_check(helper_Q_exact(report['private_inactive_audit_snapshot_controls'],snapshot,False),'complete pure report/private artifact')
    install=helper_Q_verify_META(q['actual_SOURCE_install_record']);it=helper_Q_verify_META(q['actual_SOURCE_install_tool_return'])
    helper_Q_check(q['actual_SOURCE_install_record']['sha256']=='079d4dfec16d0df86459abc2fc9238f7aabade38fca8c7adc0659a50f37dc5cf' and q['actual_SOURCE_install_tool_return']['sha256']=='a305a84b712276aecadd5ebc7fced99d0d58b68a061e228747f0ccfbeed63c12','actual Source install pins')
    helper_Q_check(it['source_only']is True and it['closed']is True and install['source_only']is True and it['new_Q']is None,'Source installation is not runtime qualification');helper_Q_closed0(it['terminal_tool_return'],'10a0e4')
    helper_Q_check(helper_Q_fullpin(install['installed_helper'])==hp==helper_Q_fullpin(it['installed_helper']),'same actual installed helper')
    helper_Q_check(q['independent_saved_review_counts']==dict(pure=55,fresh=42,auxiliary_pure_small_controls=136) and q['lossless_complete_original_Source_files_per_family']==[184,199] and q['pure_source_member_count']==9 and q['fresh_source_member_count']==10,'honest actual original Source scopes')
    final=path.lstat();qid=[final.st_dev,final.st_ino,final.st_mode,final.st_nlink,final.st_size,final.st_mtime_ns,final.st_ctime_ns]
    helper_Q_check(qid==[first.st_dev,first.st_ino,first.st_mode,first.st_nlink,first.st_size,first.st_mtime_ns,first.st_ctime_ns] and digest(path)==FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA,'actual Q unchanged')
    complete[str(path)]=dict(path=str(path),sha256=FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA,size_bytes=final.st_size,identity=qid)
    return {p:row['sha256']for p,row in complete.items()}

'''

def main():
 assert P.is_dir() and not list(P.iterdir())
 orig=P/'ORIGINAL_PARENT_SOURCE';orig.mkdir()
 allparents={};raws={}
 for name,path in parents.items():
  before=pin(path);raw=path.read_bytes();assert pin(path)==before
  (orig/(name+'.full.py')).write_bytes(raw);allparents[name]=before;raws[name]=raw.decode()
 assert allparents['canonical']['sha256']==OLD_CSHA
 assert allparents['old_graph_helper']['sha256']==OLD_HSHA
 assert allparents['installed_new_graph_helper']['sha256']==NEW_HSHA
 qold=B/OLD_Q;oldpin=pin(qold);(orig/'old_actual_Q89.full.json').write_bytes(qold.read_bytes());assert pin(qold)==oldpin
 proofs={}; outputs={}
 t=raws['canonical'];ed=[];t=version(t,ed)
 olddoc=ast.get_source_segment(t,ast.parse(t).body[0])
 doc=repr('UNREADY SOURCE ONLY V25 complete sender/root-index flow. Three private inactive audit snapshots use consume only at their actual final callsite. The installed3b helper needs a new actual V25 full pure/fresh joint metadata Q, both real closed-zero Root terminals and saved independent peers. Actual Q SHA and all six business pins remain None; no candidate was imported/executed. Original complete scopes, five stages, physics and budgets remain required. This Source does not predict RSS, build, INPUT, native or science success.')
 t=edit(t,ed,'honest_UNREADY_doc',olddoc,doc,1)
 t=edit(t,ed,'UNREADY_status_assignment',"DRAFT_STATUS = 'READY_REVIEWED_V22_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY'","DRAFT_STATUS = 'UNREADY_V25_COMPLETE_INACTIVE_AUDIT_ACTUAL_Q_UNBOUND'",1)
 t=edit(t,ed,'READY_status_predicate',"DRAFT_STATUS != 'READY_REVIEWED_V22_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY'","DRAFT_STATUS != 'READY_REVIEWED_V25_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY'",1)
 t=edit(t,ed,'installed_3b_helper_path',OLD_HELPER,NEW_HELPER,1)
 t=edit(t,ed,'installed_3b_helper_SHA',OLD_HSHA,NEW_HSHA,1)
 t=edit(t,ed,'actual_Q_UNREADY_SHA',"FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA = '"+OLD_QSHA+"'","FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA = None",1)
 anchor="FUTURE_ACTUAL_NATIVE_TERMINAL_SHA = None\n"
 constants="ACTUAL_HELPER_Q_PATH = ROOT/'validation/axial_material/complete_history_root_index_source_v15_20261010/"+NEW_Q+"'\nACTUAL_HELPER_Q_SCHEMA = 'AXMAT_ROOT_COMPLETE_GRAPH_PRIVATE_INACTIVE_AUDIT_HELPER_ACTUAL_JOINT_ADMISSION_V25'\nACTUAL_HELPER_Q_STATUS = 'QUALIFIED_ORIGINAL_FULL_PROTOCOL_AND_COMPLETE_CURRENT_GRAPH_METADATA_VERIFIER_ONLY_V25'\n"
 t=edit(t,ed,'actual_new_Q_contract_globals',anchor,anchor+constants,1)
 anchor='\n\ndef normal(path,missing=False):'
 t=edit(t,ed,'complete_actual_joint_Q_stdlib_reader',anchor,CONTRACT+anchor,1)
 old="    nonzero_sha(FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA)  # Root must bind the actual complete controls admission before READY."
 t=edit(t,ed,'actual_Q_read_before_project_load',old,old+'\n    helper_Q_admission()  # Actual new Q/core proofs are read; no project API.',1)
 t=edit(t,ed,'three_actual_final_owned_snapshot_calls','trace=audit.snapshot()','trace=audit.snapshot(_consume=True)',3)
 old="**{str(path):sha for path,sha in INPUT_HELPERS.values()},**{str(SOURCE/name):sha for name,sha in source_inventory['files'].items()}}"
 t=edit(t,ed,'all_Q_and_proof_typed_owners',old,"**{str(path):sha for path,sha in INPUT_HELPERS.values()},**{str(SOURCE/name):sha for name,sha in source_inventory['files'].items()},**helper_Q_admission()}",1)
 old="str(SENDER_DRIVER),str(SENDER_AUDITOR),str(SENDER_CONTRACT)]"
 t=edit(t,ed,'all_Q_and_proof_ordinary_endpoints',old,"str(SENDER_DRIVER),str(SENDER_AUDITOR),str(SENDER_CONTRACT),*helper_Q_admission()]",1)
 assert inverse(t,ed)==raws['canonical'];ast.parse(t)
 outputs['canonical']=t;proofs['canonical']=ed
 sub=P/'host_and_postclose_templates';sub.mkdir()
 for role in ('prepare_host','prepare_writer','build_host','build_writer'):
  text=raws[role];rows=[];text=version(text,rows)
  if OLD_HELPER in text:text=edit(text,rows,'new_helper_path',OLD_HELPER,NEW_HELPER)
  if OLD_HSHA in text:text=edit(text,rows,'same_installed_3b_SHA',OLD_HSHA,NEW_HSHA)
  if OLD_Q in text:text=edit(text,rows,'actual_new_Q_path',OLD_Q,NEW_Q)
  future_constants={}
  for value,name in ((OLD_QSHA,'FUTURE_V25_ACTUAL_Q_SHA'),(OLD_CSHA,'FUTURE_V25_CANONICAL_SHA')):
   if repr(value)in text:
    text=edit(text,rows,'future_binding_'+name,repr(value),name);future_constants[name]=None
  if role=='prepare_host':
   text=edit(text,rows,'UNREADY_prepare_host',"SOURCE_BINDING_STATUS='READY_V22_ACTUAL_Q_AND_TARGET_SOURCE_BOUND'","SOURCE_BINDING_STATUS='UNREADY_V25_ACTUAL_Q_AND_TARGET_SOURCE_UNBOUND'",1)
   text=edit(text,rows,'READY_prepare_host_predicate',"SOURCE_BINDING_STATUS!='READY_V22_ACTUAL_Q_AND_TARGET_SOURCE_BOUND'","SOURCE_BINDING_STATUS!='READY_V25_ACTUAL_Q_AND_TARGET_SOURCE_BOUND'",1)
  elif role=='prepare_writer':
   text=edit(text,rows,'UNREADY_prepare_writer',"SOURCE_BINDING_STATUS='READY_V22_ACTUAL_Q_AND_CANONICAL_SOURCE_BOUND'","SOURCE_BINDING_STATUS='UNREADY_V25_ACTUAL_Q_AND_CANONICAL_SOURCE_UNBOUND'",1)
   text=edit(text,rows,'READY_prepare_writer_predicate',"SOURCE_BINDING_STATUS!='READY_V22_ACTUAL_Q_AND_CANONICAL_SOURCE_BOUND'","SOURCE_BINDING_STATUS!='READY_V25_ACTUAL_Q_AND_CANONICAL_SOURCE_BOUND'",1)
  else:
   guard="SOURCE_BINDING_STATUS='UNREADY_V25_ACTUAL_COMPLETE_PREP_AND_SOURCE_UNBOUND'\n"
   text=edit(text,rows,'UNREADY_build_binding_global','\ndef main():','\n'+guard+'\ndef main():',1)
   prefix="    if SOURCE_BINDING_STATUS!='READY_V25_ACTUAL_COMPLETE_PREP_AND_SOURCE_BOUND':\n        raise ValueError('UNREADY: actual new Q, complete PREP saved peer and bound Source required before any I/O')\n"
   text=edit(text,rows,'UNREADY_build_pre_IO_guard','def main():\n','def main():\n'+prefix,1)
   for sha in ('8ad01e54e6ed89911c56d1fe04284e5f39f81ebe0ae9aa060253b9378df346b1','96ff567a30a451af02767c153ce8f0213c9f5b6e7330eb48b1ca9c69a992b61c','0dd662ee6ede3122fe8d4af4e8c84b7e8e20ce2b75caed8ce0d3700e875985b0','b8c1734611f449ec11dd3263a91570ed10d1817927d0a0a9bfd992753f4ec4aa','0b4ef19900921de593d5979283fd65c779a8df857ee1c6204d4e7b7951f4a306','cea518358a6bac164d6131eaa1a21cbf6d8155877dd14eb77fd5385e0f62a269'):
    if repr(sha)in text:
     name='FUTURE_V25_'+{'8ad01e54e6ed89911c56d1fe04284e5f39f81ebe0ae9aa060253b9378df346b1':'DECLARATION_SHA','96ff567a30a451af02767c153ce8f0213c9f5b6e7330eb48b1ca9c69a992b61c':'PREP_SHA','0dd662ee6ede3122fe8d4af4e8c84b7e8e20ce2b75caed8ce0d3700e875985b0':'GRAPH_SHA','b8c1734611f449ec11dd3263a91570ed10d1817927d0a0a9bfd992753f4ec4aa':'TRACE_SHA','0b4ef19900921de593d5979283fd65c779a8df857ee1c6204d4e7b7951f4a306':'PREP_SUMMARY_SHA','cea518358a6bac164d6131eaa1a21cbf6d8155877dd14eb77fd5385e0f62a269':'BUILD_HOST_SHA'}[sha]
     text=edit(text,rows,'future_only_'+name,repr(sha),name);future_constants[name]=None
  if future_constants:
   position=text.index('\nBASE') if '\nBASE'in text else text.index('\nART')
   old=text[:position]
   additions='\n'+''.join(name+'=None\n'for name in future_constants)
   text=edit(text,rows,'all_unbound_future_globals_before_first_use',old,old+additions,1)
  assert inverse(text,rows)==raws[role];ast.parse(text)
  outputs[role]=text;proofs[role]=rows
  (sub/(role+'.V25.UNREADY.full.py')).write_text(text)
 (P/'canonical.V25.UNREADY.full.py').write_text(t)
 (P/'helper_joint_Q_contract.inline_SOURCE.txt').write_text(CONTRACT)
 dump(P/'COMPLETE_SOURCE_INVERSES.json',dict(schema='V25_COMPLETE_INACTIVE_AUDIT_TRUE_SNAPSHOT_SOURCE_INVERSES_V1',source_only=True,exact_finite_transforms=proofs,original_sources=allparents,old_actual_Q=oldpin,all_original_Source_byte_AST_restored=True,six_future_business_pins={k:None for k in BUSINESS},actual_new_Q=None,project_API_or_numeric_executed=False))
 dump(P/'ROOT_BINDING_SOURCE_CONSTANTS.json',dict(schema='V25_COMPLETE_INACTIVE_AUDIT_SOURCE_BINDING_CONSTANTS_V1',source_only=True,original_sources=allparents,canonical_future_basename='prepare_sender_window_root_index_graph_trace_table_combined_runtime_v25.py',actual_new_Q_path=str(B/NEW_Q),actual_new_Q_sha256=None,Q_schema='AXMAT_ROOT_COMPLETE_GRAPH_PRIVATE_INACTIVE_AUDIT_HELPER_ACTUAL_JOINT_ADMISSION_V25',Q_status='QUALIFIED_ORIGINAL_FULL_PROTOCOL_AND_COMPLETE_CURRENT_GRAPH_METADATA_VERIFIER_ONLY_V25',helper_path=str(parents['installed_new_graph_helper']),helper_sha256=NEW_HSHA,caps=dict(whole=1800,stage=600,rss=512,archive=2*2**30,history=96*2**30,free=8*2**30,threads=1,children=1,retries=0),PREP_runtime_SHA=None,actual_PREP_peer=None,actual_BUILD_Source_SHA=None,new_Q_or_business_or_science_created=False))
 print(json.dumps(dict(source_only=True,output=str(P),complete_original_parent_count=len(parents),canonical=pin(P/'canonical.V25.UNREADY.full.py'),templates={k:pin(sub/(k+'.V25.UNREADY.full.py'))for k in ('prepare_host','prepare_writer','build_host','build_writer')},all_complete_inverses=True,executed_candidate=False)))

if __name__=='__main__':main()
