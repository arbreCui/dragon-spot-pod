"""UNREADY complete V25 Root SOURCE binder design. Standard library only.
Root may invoke main only with actual full pins after independent SOURCE review.
No candidate/helper/guard API import, compiler, installation or business run.
All Q/proof reads are metadata; large graph/trace/gzip endpoints are never
decoded here and are enforced by the canonical's original full fresh phases.
"""
import argparse
import ast
import hashlib
import json
import math
import os
from pathlib import Path
import re
import stat
import sys

HERE=Path(__file__).resolve().parent
ROOT=Path('/Users/wen/spot')
BASE=ROOT/'validation/axial_material/complete_history_root_index_source_v15_20261010'
ART=ROOT/'validation/artifacts'
SOURCE_DESIGN_STATUS='UNREADY_V25_ACTUAL_Q_AND_FUTURE_PREP_BUILD_PINS_UNKNOWN'
ACTUAL_HELPER_Q_PATH=BASE/'Root_actual_complete_graph_private_inactive_audit_helper_admission_v25.json'
ACTUAL_HELPER_Q_SCHEMA='AXMAT_ROOT_COMPLETE_GRAPH_PRIVATE_INACTIVE_AUDIT_HELPER_ACTUAL_JOINT_ADMISSION_V25'
ACTUAL_HELPER_Q_STATUS='QUALIFIED_ORIGINAL_FULL_PROTOCOL_AND_COMPLETE_CURRENT_GRAPH_METADATA_VERIFIER_ONLY_V25'
FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA=None
FUTURE_ACTUAL_NEW_Q_WRITER_TERMINAL_PIN = None
FUTURE_ACTUAL_NEW_Q_SAVED_PEER_PIN = None
FUTURE_ACTUAL_NEW_Q_SAVED_PEER_RETENTION_PIN = None
INPUT_HELPERS={'graph':(ROOT/'validation/axial_material/combined_runtime_complete_input_graph_private_inactive_audit_snapshot_consume_20261010.py','3b181f6366d5084fd6ccc87c1a6e7b757b706b7ba38cdf9156e1381cdb010092')}
BUSINESS=('FUTURE_ACTUAL_COMBINED_DECLARATION_SHA','FUTURE_ACTUAL_COMBINED_PREP_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_SEAL_SHA','FUTURE_ACTUAL_COMBINED_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_RUNTIME_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA')
READ_PINS={}

def identity(p):
    s=Path(p).lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def normal(p,missing=False):
    p=Path(p)
    if not p.is_absolute()or'..'in p.parts:raise ValueError('absolute ordinary Source/META path required')
    for q in [*reversed(p.parents),p]:
        try:s=q.lstat()
        except FileNotFoundError:
            if missing:continue
            raise
        if stat.S_ISLNK(s.st_mode)or(q!=p and not stat.S_ISDIR(s.st_mode)):raise ValueError('Source/META ancestor alias')
    return p

def source_pin(p):
    p=normal(p);before=identity(p)
    if not stat.S_ISREG(before[2]):raise ValueError('regular Source/META required')
    with p.open('rb')as f:h=hashlib.file_digest(f,'sha256').hexdigest()
    if identity(p)!=before:raise ValueError('complete EOF input changed')
    row=dict(path=str(p),sha256=h,size_bytes=before[4],identity=before)
    if str(p)in READ_PINS and READ_PINS[str(p)]!=row:raise ValueError('repeated Source/META differs')
    READ_PINS[str(p)]=row;return row

def nonzero_sha(value):
    if type(value)is not str or re.fullmatch('[0-9a-f]{64}',value)is None or value=='0'*64:raise ValueError('actual nonplaceholder SHA required')
    return value

def digest(p):return source_pin(p)['sha256']

def require(p,sha=None):
    p=normal(p)
    if not p.is_file()or(sha is not None and digest(p)!=nonzero_sha(sha)):raise ValueError('actual Source/META pin differs')
    return p

def strict_json_bytes(raw):
    def pairs(rows):
        d={}
        for k,v in rows:
            if k in d:raise ValueError('duplicate Source/META key')
            d[k]=v
        return d
    def reject(v):raise ValueError('nonfinite Source/META constant '+v)
    value=json.loads(raw.decode('utf-8'),object_pairs_hook=pairs,parse_constant=reject)
    def finite(v):
        if type(v)is float and not math.isfinite(v):raise ValueError('nonfinite Source/META number')
        if type(v)is dict:
            for x in v.values():finite(x)
        elif type(v)is list:
            for x in v:finite(x)
    finite(value);return value

def read(p):
    p=normal(p)
    # Only the three explicit small ART proof basenames are decoded. Payload
    # graph/trace/gzip pins remain full ownership declarations, never arrays.
    if p.is_relative_to(ART)and p.name not in ('result.json','ACTUAL_REPORT.json','ACTUAL_PRIVATE_INACTIVE_AUDIT_SNAPSHOT_CONTROLS.json'):raise ValueError('no ART graph/trace/payload decoding in Source binding')
    before=source_pin(p);value=strict_json_bytes(p.read_bytes())
    if source_pin(p)!=before:raise ValueError('Source/META JSON changed')
    return value

def source_dump(p,v):
    with p.open('x')as f:json.dump(v,f,indent=2,allow_nan=False);f.write('\n')

def source_replace(text,rows,old,new,label):
    count=text.count(old)
    if count<=0 or old==new:raise ValueError('missing Source binding anchor '+label)
    rows.append(dict(label=label,old=old,new=new,count=count));return text.replace(old,new)

def source_inverse(text,rows):
    for row in reversed(rows):
        if text.count(row['new'])!=row['count']:raise ValueError('inverse anchor '+row['label'])
        text=text.replace(row['new'],row['old'])
    return text

def source_definitions(text):
    return {n.name:ast.get_source_segment(text,n)for n in ast.parse(text).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}

def source_package():
    m=read(HERE/'MANIFEST.json')
    files={str(p.relative_to(HERE))for p in HERE.rglob('*')if p.is_file()}
    if files!=set(m['members'])|{'MANIFEST.json'}:raise ValueError('complete SOURCE package file names')
    dirs={'.'}|{str(p.relative_to(HERE))for p in HERE.rglob('*')if p.is_dir()}
    if dirs!=set(m['directories']):raise ValueError('complete SOURCE package directory names')
    for rel,wanted in m['directories'].items():
        if identity(HERE if rel=='.'else HERE/rel)!=wanted:raise ValueError('SOURCE directory identity')
    for rel,wanted in m['members'].items():
        if source_pin(HERE/rel)!=wanted:raise ValueError('complete SOURCE member full pin')
    return m

def source_unknown_globals(text):
    result={}
    for node in ast.parse(text).body:
        if isinstance(node,ast.Assign)and len(node.targets)==1 and isinstance(node.targets[0],ast.Name)and node.targets[0].id.startswith('FUTURE_V25_'):
            if not isinstance(node.value,ast.Constant)or node.value.value is not None:raise ValueError('future Source binding unexpectedly known')
            result[node.targets[0].id]=None
    return result

def source_future_bind(text,values,rows):
    for name in source_unknown_globals(text):
        if name not in values:raise ValueError('missing actual future Source value '+name)
        text=source_replace(text,rows,name+'=None',name+'='+repr(nonzero_sha(values[name])),'actual_'+name)
    return text

def source_verify_original_inverse(role,text,ready_rows,proof):
    original=source_inverse(source_inverse(text,ready_rows),proof['exact_finite_transforms'][role])
    parent=(HERE/'ORIGINAL_PARENT_SOURCE'/(role+'.full.py')).read_text()
    if original!=parent or ast.dump(ast.parse(original),include_attributes=False)!=ast.dump(ast.parse(parent),include_attributes=False):raise ValueError('whole original Source byte/AST inverse '+role)
    return dict(READY_to_UNREADY=ready_rows,UNREADY_to_original=proof['exact_finite_transforms'][role],complete_byte_inverse=True,complete_AST_inverse=True)

def source_manifest(output,schema):
    target=output/'MANIFEST.json';target.touch(exist_ok=False)
    members={str(p.relative_to(output)):source_pin(p)for p in sorted(output.rglob('*'))if p.is_file()and p!=target}
    directories={'.':identity(output),**{str(p.relative_to(output)):identity(p)for p in sorted(output.rglob('*'))if p.is_dir()}}
    with target.open('w')as f:json.dump(dict(schema=schema,source_only=True,members=members,directories=directories,member_count=len(members),executed_project=False),f,indent=2,allow_nan=False);f.write('\n')
    return source_pin(target)



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
        freeze=data['source_manifest'];helper_Q_check(freeze['schema']=='ROOT_V25_COMPLETE_PRIVATE_INACTIVE_AUDIT_QUALIFICATION_SOURCE_FREEZE_V1' and freeze['kind']==kind and freeze['source_only']is True and freeze['new_actual_helper_qualification']is None and helper_Q_fullpin(freeze['actual_installed_helper'])==hp,'same helper and actual complete Source freeze')
        archives=freeze['lossless_complete_Source_archives'];helper_Q_check([entry['complete_file_count_including_manifest']for entry in archives.values()]==[184,199] and all(entry['all_member_bytes_and_SHA_verified_after_decompression']is True and entry['no_original_member_omission']is True and entry['runtime_Source_entrypoints_are_separate_original_bytes']is True for entry in archives.values()),'complete lossless bound and peer Source scopes')
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
    # The Q cannot contain its own later writer terminal or saved-review
    # evidence. Root binds these three external full pins independently.
    qpin=complete[str(path)]
    for value,basename in ((FUTURE_ACTUAL_NEW_Q_WRITER_TERMINAL_PIN,'Root_actual_joint_helper_META_admission_writer_tool_terminal_return.json'),(FUTURE_ACTUAL_NEW_Q_SAVED_PEER_PIN,'sealed_independent_actual_joint_Q_saved_META_review/REVIEW.json'),(FUTURE_ACTUAL_NEW_Q_SAVED_PEER_RETENTION_PIN,'Root_actual_joint_Q_saved_META_peer_retention_record.json')):
        helper_Q_check(helper_Q_fullpin(value)['path']==str(ACTUAL_HELPER_Q_PATH.parent/'actual_joint_helper_admission_v25_receipts'/basename),'fixed external actual new-Q evidence path')
    qt=helper_Q_verify_META(FUTURE_ACTUAL_NEW_Q_WRITER_TERMINAL_PIN)
    peer=helper_Q_verify_META(FUTURE_ACTUAL_NEW_Q_SAVED_PEER_PIN)
    retention=helper_Q_verify_META(FUTURE_ACTUAL_NEW_Q_SAVED_PEER_RETENTION_PIN)
    helper_Q_check(qt['schema']=='ROOT_V25_ACTUAL_JOINT_HELPER_META_ADMISSION_WRITER_TOOL_TERMINAL_RETURN_V1' and qt['closed']is True and qt['actual_tool_terminal_return_observed']is True and qt['no_closed_session_repoll']is True,'actual new-Q writer observed closed')
    helper_Q_closed0(qt['terminal_tool_return'],'94520a')
    for key in ('candidate_helper_guard_API_or_numeric_executed','whole_build_qualified','whole_INPUT_admitted','AAA_accuracy_qualified','ABA_admitted','goal_complete'):helper_Q_check(qt[key]is False,'actual Q writer '+key)
    observed=strict_json_bytes(qt['terminal_tool_return']['output'].encode('utf-8'))
    helper_Q_check(helper_Q_fullpin(observed['actual_metadata_Q'])==qpin and helper_Q_fullpin(observed['actual_Source_writer'])==helper_Q_fullpin(q['Root_actual_Source_writer']),'actual raw stdout exact full Q/writer pins')
    helper_Q_check([observed[k]for k in ('full_protocol_fields','complete_return_fields','actual_complete_read_count','pure_saved_review_checks','fresh_saved_review_checks')]==[13,27,37112,55,42] and all(type(observed[k])is int for k in ('full_protocol_fields','complete_return_fields','actual_complete_read_count','pure_saved_review_checks','fresh_saved_review_checks')),'actual writer complete scope')
    for key in ('whole_build_qualified','whole_INPUT_admitted','AAA_accuracy_qualified','ABA_admitted','candidate_or_API_or_numeric_executed'):helper_Q_check(observed[key]is False,'raw actual Q writer scope '+key)
    helper_Q_check(peer['schema']=='INDEPENDENT_V25_ACTUAL_JOINT_HELPER_Q_SAVED_META_REVIEW_V1' and peer['status']=='PASS_ACTUAL_JOINT_HELPER_Q_METADATA_ONLY' and peer['source_only']is True and peer['all_checks_typed_true']is True and peer['blockers']==[] and type(peer['check_count'])is int and peer['check_count']==len(peer['checks'])==48 and all(type(row['passed'])is bool and row['passed']is True for row in peer['checks']),'complete actual new-Q independent saved48')
    helper_Q_check(peer['actual_saved_helper_metadata_qualification_verified']is True and peer['qualification_scope']==q['scope'] and peer['Root_actual_writer_terminal_chunk']=='94520a','saved new-Q metadata-only scope')
    for key in ('whole_build_qualified','whole_INPUT_admitted','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted','physical_balance_qualified','candidate_helper_writer_guard_API_or_numeric_executed','large_graph_trace_gzip_SQLite_material_or_Source_archive_member_payload_read'):helper_Q_check(peer[key]is False,'saved Q peer '+key)
    helper_Q_check(helper_Q_fullpin(peer['Root_actual_Q_pin'])==qpin and helper_Q_fullpin(peer['Root_actual_Q_writer_terminal_pin'])==helper_Q_fullpin(FUTURE_ACTUAL_NEW_Q_WRITER_TERMINAL_PIN) and helper_Q_fullpin(peer['Root_actual_Q_writer_Source_pin'])==helper_Q_fullpin(q['Root_actual_Source_writer']),'saved48 exact Q/writer terminal/Source coupling')
    helper_Q_check(retention['schema']=='ROOT_COMPLETE_FINITE_SOURCE_REVIEW_PACKAGE_RETENTION_V1' and retention['source_only']is True and retention['new_qualification_created']is False and retention['helper_guard_business_executed']is False and retention['cleanup_performed']is False and type(retention['complete_original_member_count'])is int and retention['complete_original_member_count']==len(retention['complete_original_members'])==10,'complete actual saved48 retention')
    members=retention['complete_original_members'];savedroot=Path(FUTURE_ACTUAL_NEW_Q_SAVED_PEER_PIN['path']).parent
    for name,row in members.items():
        original=helper_Q_fullpin(row['original']);saved=helper_Q_fullpin(row['saved'])
        helper_Q_check(saved['path']==str(savedroot/name) and saved['sha256']==original['sha256'] and saved['size_bytes']==original['size_bytes'],'full original saved48 member retention')
    helper_Q_check(helper_Q_fullpin(members['REVIEW.json']['saved'])==helper_Q_fullpin(FUTURE_ACTUAL_NEW_Q_SAVED_PEER_PIN),'saved48 full report retention pin')
    reviewtool=helper_Q_verify_META(members['ACTUAL_SAVED_Q_META_REVIEW_TOOL_RETURNS.json']['saved'])
    helper_Q_check(reviewtool['schema']=='INDEPENDENT_V25_SAVED_JOINT_Q_ACTUAL_FINITE_META_TOOL_RETURNS_V1' and reviewtool['source_only']is True and reviewtool['candidate_helper_writer_guard_API_or_numeric_executed']is False and reviewtool['raw_tool_stdout_preserved_as_strings']is True,'genuine saved48 review tool scope')
    helper_Q_closed0(reviewtool['actual_success_tool_return'],'17e611')
    reviewed=strict_json_bytes(reviewtool['actual_success_tool_return']['output'].encode('utf-8'))
    helper_Q_check(reviewed['status']==peer['status'] and reviewed['source_only']is True and reviewed['all_checks_typed_true']is True and type(reviewed['check_count'])is int and reviewed['check_count']==48 and helper_Q_fullpin(reviewed['review_pin'])==helper_Q_fullpin(members['REVIEW.json']['original']) and helper_Q_fullpin(reviewed['Root_actual_Q_pin'])==qpin and helper_Q_fullpin(reviewed['Root_actual_Q_writer_terminal_pin'])==helper_Q_fullpin(FUTURE_ACTUAL_NEW_Q_WRITER_TERMINAL_PIN),'actual saved48 tool full pins')
    seal=helper_Q_verify_META(retention['saved_actual_peer_seal_receipt'])
    helper_Q_check(seal['schema']=='INDEPENDENT_V25_SAVED_JOINT_Q_ACTUAL_META_SEAL_TOOL_RETURN_V1' and seal['source_only']is True and seal['closed']is True and seal['actual_tool_terminal_return_observed']is True and seal['candidate_helper_writer_guard_API_or_numeric_executed']is False,'actual saved48 seal scope')
    helper_Q_closed0(seal['terminal_tool_return'],'821784')
    sealed=strict_json_bytes(seal['terminal_tool_return']['output'].encode('utf-8'))
    helper_Q_check(helper_Q_fullpin(sealed['review_pin'])==helper_Q_fullpin(members['REVIEW.json']['original']) and helper_Q_fullpin(sealed['Root_actual_Q_pin'])==qpin and sealed['source_only']is True and type(sealed['check_count'])is int and sealed['check_count']==48,'actual saved48 seal full pin coupling')
    external={}
    for value in (FUTURE_ACTUAL_NEW_Q_WRITER_TERMINAL_PIN,FUTURE_ACTUAL_NEW_Q_SAVED_PEER_PIN,FUTURE_ACTUAL_NEW_Q_SAVED_PEER_RETENTION_PIN,peer,retention,observed):helper_Q_collect_refs(value,external)
    for p,row in external.items():
        helper_Q_check(p not in complete or complete[p]==row,'external new-Q proof pin conflicts with original full scope');complete[p]=row
    return {p:row['sha256']for p,row in complete.items()}



# Whole original legacy helper definitions; new Q uses helper_Q_admission.

def pin(p):return read(p)[1]

def ref3(ref,p):
    assert set(ref)=={'path','sha256','identity'} and ref['path']==str(p)
    actual=pin(p);assert ref=={k:actual[k] for k in ref}
    return actual

def outputref(ref,p):
    assert set(ref)=={'path','sha256','identity'} and ref['path']==str(p)
    i=ref['identity'];assert len(i)==7 and all(type(v) is int for v in i)
    assert stat.S_ISREG(i[2]) and i[3]==1 and i[4]>0
    assert len(ref['sha256'])==64 and all(c in '0123456789abcdef' for c in ref['sha256'])
    return ref

def write(p,b):
    with p.open('xb') as f:f.write(b)

def jsonbytes(d):return (json.dumps(d,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()

def main():
    global FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA,FUTURE_ACTUAL_NEW_Q_WRITER_TERMINAL_PIN,FUTURE_ACTUAL_NEW_Q_SAVED_PEER_PIN,FUTURE_ACTUAL_NEW_Q_SAVED_PEER_RETENTION_PIN
    if sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE')or sys.getprofile()is not None:raise ValueError('original nonoptimized Source binder')
    a=argparse.ArgumentParser();a.add_argument('--saved-prep-peer-report',required=True);a.add_argument('--saved-prep-peer-report-sha256',required=True);a.add_argument('--actual-Q-sha256',required=True);a.add_argument('--actual-canonical-sha256',required=True);a.add_argument('--destination',required=True);a.add_argument('--actual-new-Q-writer-terminal',required=True);a.add_argument('--actual-new-Q-writer-terminal-sha256',required=True);a.add_argument('--actual-Q-saved-peer',required=True);a.add_argument('--actual-Q-saved-peer-sha256',required=True);a.add_argument('--actual-Q-saved-peer-retention',required=True);a.add_argument('--actual-Q-saved-peer-retention-sha256',required=True);args=a.parse_args()
    output=normal(args.destination,missing=True)
    if not output.is_relative_to(Path('/private/tmp'))or os.path.lexists(output):raise ValueError('fresh complete build Source namespace')
    source_package();FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA=nonzero_sha(args.actual_Q_sha256)
    FUTURE_ACTUAL_NEW_Q_WRITER_TERMINAL_PIN=source_pin(require(args.actual_new_Q_writer_terminal,args.actual_new_Q_writer_terminal_sha256))
    FUTURE_ACTUAL_NEW_Q_SAVED_PEER_PIN=source_pin(require(args.actual_Q_saved_peer,args.actual_Q_saved_peer_sha256))
    FUTURE_ACTUAL_NEW_Q_SAVED_PEER_RETENTION_PIN=source_pin(require(args.actual_Q_saved_peer_retention,args.actual_Q_saved_peer_retention_sha256))
    deps=helper_Q_admission()
    E=BASE/'actual_complete_combined_prepare_v25_poststage_temporaries_receipts';TARGET=ROOT/'validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v25_poststage_temporaries.py'
    peerpath=require(args.saved_prep_peer_report,args.saved_prep_peer_report_sha256);peer=read(peerpath)
    helper_Q_check(peer['schema']=='INDEPENDENT_V25_ACTUAL_COMPLETE_PREP_SAVED_META_REVIEW_V1' and peer['status']=='PASS_ACTUAL_COMPLETE_PREP_ONLY' and peer['all_checks_typed_true']is True and peer['blockers']==[] and peer['actual_PREP_closed_EXIT0_verified']is True and peer['actual_metadata_writer_closed_EXIT0_verified']is True and peer['all_complete_scope_verified']is True and peer['actual_PREP_metadata_only']is True,'actual whole PREP independent saved peer')
    for k in ('whole_combined_build_qualified','whole_combined_INPUT_admitted','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted','physical_balance_qualified'):helper_Q_check(peer[k]is False,k)
    sp=source_pin(E/'Root_actual_complete_combined_prepare_summary.json');tp=source_pin(E/'Root_actual_prepare_tool_terminal_return.json');np=source_pin(E/'Root_actual_complete_prepare_namespace_manifest.json')
    for pk,wanted in (('actual_Root_PREP_summary_pin',sp),('actual_Root_PREP_terminal_pin',tp),('actual_complete_namespace_manifest_pin',np)):helper_Q_check(helper_Q_fullpin(peer[pk])==wanted,'saved PREP peer three complete pins')
    s=read(sp['path']);terminal=read(tp['path']);namespace=read(np['path'])
    helper_Q_check(s['schema']=='ROOT_V25_ACTUAL_COMPLETE_COMBINED_PREPARE_SUMMARY_V1' and s['status']=='ACTUAL_COMPLETE_PREPARE_EXIT0_CLOSED_ONLY_NOT_COMPLETE_BUILD','actual PREP only summary')
    caps=('whole_wall_cap_seconds','stage_wall_cap_seconds','rss_mib','joint_archive_cap_bytes','history_cap_bytes','free_floor_bytes','threads','children','retries');expected_caps=(1800,600,512,2*2**30,96*2**30,8*2**30,1,1,0)
    helper_Q_check(all(type(s[k])is int and s[k]==v for k,v in zip(caps,expected_caps)),'all original PREP caps')
    helper_Q_check(s['original_caps_preserved']is True and 0<=s['sampled_peak_rss_mib']<512 and 0<s['child_seconds']<=600 and s['child_seconds']<=s['whole_seconds']<1800 and 0<s['joint_archive_bytes']<2*2**30,'genuine actual complete PREP measurements')
    for k in ('new_five_stage_build_executed','original_five_build_stages_executed','whole_combined_INPUT_admitted','new_native_transport_executed','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted','cleanup_performed','goal_complete'):helper_Q_check(s[k]is False,k)
    helper_Q_check(helper_Q_fullpin(s['actual_root_terminal'])==tp and s['Root_actual_terminal']==s['actual_root_terminal'] and helper_Q_fullpin(s['namespace_manifest'])==np,'actual PREP summary terminal/namespace coupling')
    tr=terminal['terminal_tool_return'];helper_Q_check(terminal['closed']is True and type(tr['exit_code'])is int and tr['exit_code']==0 and 'session_id'not in tr and terminal.get('session_repolled_after_close',False)is False,'actual Root closed PREP zero')
    helper_Q_check(namespace['schema']=='ROOT_V25_ACTUAL_COMPLETE_PREPARE_ALL_NAMESPACES_V1' and namespace['no_build_or_native_credit']is True,'whole PREP namespace no business credit')
    H=ART/'axial-material-complete-combined-prepare-host-v25-poststage-temporaries-20261010';S=ART/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v25-poststage-temporaries-20261010';O=ART/'axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v25-poststage-temporaries-20261010';T=ART/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v25-poststage-temporaries-20261010';D=BASE/'actual_complete_combined_prepare_v25_poststage_temporaries_sources'
    ns={row['root']:row for row in namespace['namespaces']};helper_Q_check(len(ns)==5 and set(ns)=={str(x)for x in (H,S,O,T,D)},'all original complete PREP namespaces')
    outrefs={'declaration':helper_Q_fullpin(s['actual_declaration']),'prep':helper_Q_fullpin(s['formal_PREP_terminal']),'graph':helper_Q_fullpin(s['actual_complete_input_graph']),'trace':helper_Q_fullpin(s['actual_complete_creation_trace']),'source_admission':helper_Q_fullpin(ns[str(S)]['files']['source_admission.json'])}
    for name,row in outrefs.items():
        root=T if name=='prep'else S if name=='source_admission'else O
        helper_Q_check(row['path']==str(root/({'declaration':'declaration.json','prep':'declaration_terminal_return.json','graph':'input_graph.json','trace':'input_creation_python_open_trace.json','source_admission':'source_admission.json'}[name])) and helper_Q_fullpin(ns[str(root)]['files'][str(Path(row['path']).relative_to(root))])==row,'whole PREP actual output full namespace binding')
    cp=source_pin(require(TARGET,args.actual_canonical_sha256));helper_Q_check(helper_Q_fullpin(namespace['canonical_factory'])==cp,'actual installed canonical full Source')
    source_text=TARGET.read_text();assignments={n.targets[0].id:n.value for n in ast.parse(source_text).body if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
    helper_Q_check(ast.literal_eval(assignments['DRAFT_STATUS'])=='READY_REVIEWED_V25_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY' and ast.literal_eval(assignments['FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA'])==args.actual_Q_sha256,'same actual Q wired canonical')
    for key,value in (('FUTURE_ACTUAL_NEW_Q_WRITER_TERMINAL_PIN',FUTURE_ACTUAL_NEW_Q_WRITER_TERMINAL_PIN),('FUTURE_ACTUAL_NEW_Q_SAVED_PEER_PIN',FUTURE_ACTUAL_NEW_Q_SAVED_PEER_PIN),('FUTURE_ACTUAL_NEW_Q_SAVED_PEER_RETENTION_PIN',FUTURE_ACTUAL_NEW_Q_SAVED_PEER_RETENTION_PIN)):
        helper_Q_check(helper_Q_fullpin(ast.literal_eval(assignments[key]))==helper_Q_fullpin(value),'same actual new-Q external proof Source bindings')
    for k in BUSINESS:helper_Q_check(isinstance(assignments[k],ast.Constant)and assignments[k].value is None,'all six future business pins unknown')
    proof=read(HERE/'COMPLETE_SOURCE_INVERSES.json');roles=('build_host','build_writer');templates={role:(HERE/'host_and_postclose_templates'/(role+'.V25.UNREADY.full.py')).read_text()for role in roles};bound={};edits={role:[]for role in roles}
    values={'FUTURE_V25_ACTUAL_Q_SHA':args.actual_Q_sha256,'FUTURE_V25_CANONICAL_SHA':cp['sha256'],'FUTURE_V25_DECLARATION_SHA':outrefs['declaration']['sha256'],'FUTURE_V25_PREP_SHA':outrefs['prep']['sha256'],'FUTURE_V25_GRAPH_SHA':outrefs['graph']['sha256'],'FUTURE_V25_TRACE_SHA':outrefs['trace']['sha256'],'FUTURE_V25_PREP_SUMMARY_SHA':sp['sha256']}
    text=source_future_bind(templates['build_host'],values,edits['build_host']);text=source_replace(text,edits['build_host'],"SOURCE_BINDING_STATUS='UNREADY_V25_ACTUAL_COMPLETE_PREP_AND_SOURCE_UNBOUND'","SOURCE_BINDING_STATUS='READY_V25_ACTUAL_COMPLETE_PREP_AND_SOURCE_BOUND'",'actual_complete_PREP_and_Source_bound');bound['build_host']=text
    values['FUTURE_V25_BUILD_HOST_SHA']=hashlib.sha256(text.encode()).hexdigest()
    text=source_future_bind(templates['build_writer'],values,edits['build_writer']);text=source_replace(text,edits['build_writer'],"SOURCE_BINDING_STATUS='UNREADY_V25_ACTUAL_COMPLETE_PREP_AND_SOURCE_UNBOUND'","SOURCE_BINDING_STATUS='READY_V25_ACTUAL_COMPLETE_PREP_AND_SOURCE_BOUND'",'actual_complete_PREP_and_Source_bound');bound['build_writer']=text
    inverses={}
    for role,text in bound.items():
        helper_Q_check(source_definitions(text)==source_definitions(templates[role]),'actual Source binding no function change');inverses[role]=source_verify_original_inverse(role,text,edits[role],proof)
    for path,wanted in tuple(READ_PINS.items()):helper_Q_check(source_pin(path)==wanted,'actual Source/meta input unchanged')
    output.mkdir();names={'build_host':'combined_build_host.py','build_writer':'write_actual_build_postclose_META.py'}
    for role,text in bound.items():(output/names[role]).write_text(text)
    (output/'ACTUAL_SAVED_V25_PREP_PEER.byte_exact.json').write_bytes(peerpath.read_bytes())
    source_dump(output/'Root_actual_full_V25_build_Source_binding_inverse.json',dict(schema='ROOT_V25_ACTUAL_FULL_FIVE_STAGE_BUILD_SOURCE_BINDING_INVERSE_V1',source_only=True,actual_saved_PREP_peer=source_pin(peerpath),actual_closed_PREP_summary=sp,actual_Root_closed_terminal=tp,actual_complete_NAMESPACE=np,actual_output_fullpins=outrefs,complete_original_source_inverses=inverses,all_Q_and_proof_explicit_typed_owner_expected_files=deps,all_original_full_five_stages_retained=True,original_caps=list(expected_caps),all_Source_META_actual_fullpins=list(READ_PINS.values()),candidate_guard_API_compiler_numeric_executed=False,whole_build_INPUT_native_science_qualified=False))
    print(json.dumps(dict(source_only=True,host=source_pin(output/names['build_host']),writer=source_pin(output/names['build_writer']),manifest=source_manifest(output,'ROOT_V25_ACTUAL_FULL_BUILD_SOURCE_BOUND_PACKAGE_MANIFEST_V1'),full_original_build_retained=True,project_executed=False)))

if __name__=='__main__':main()
