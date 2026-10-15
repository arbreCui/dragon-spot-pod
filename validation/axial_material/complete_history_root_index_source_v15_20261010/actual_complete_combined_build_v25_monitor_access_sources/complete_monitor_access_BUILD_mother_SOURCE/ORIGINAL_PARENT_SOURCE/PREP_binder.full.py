"""Root-only standard-library SOURCE binder. No imports of project code and no ART reads.

This binding branch is not executed by the Source author. Root may run it only
after the new actual Q and independent saved-Q META review have both passed.
It produces reviewable files in a fresh /private/tmp directory; no installation.
"""
import argparse
import ast
import hashlib
import json
import math
import os
from pathlib import Path
import stat
import struct
import sys

HERE=Path(__file__).resolve().parent
BASE=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
ART=Path('/Users/wen/spot/validation/artifacts')
EXPECTED_Q=BASE/'Root_actual_complete_graph_private_owner_namespace_helper_admission_v22.json'
Q_SCHEMA='AXMAT_ROOT_COMPLETE_GRAPH_PRIVATE_OWNER_NAMESPACE_HELPER_ACTUAL_JOINT_ADMISSION_V22'
Q_STATUS='QUALIFIED_ORIGINAL_FULL_PROTOCOL_AND_COMPLETE_CURRENT_GRAPH_METADATA_VERIFIER_ONLY_V22'
EXPECTED_HELPER=Path('/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_private_owner_namespace_last_use_20261010.py')
HELPER_SHA='cf0c2b6b6fd6b1adceec85b261008871f12769832b4dbd4fdb4204f650b4e72c'
HELPER_ID=[16777229,49393808,33188,1,148965,1791600075411912623,1791600075411921373]
PURE_E=BASE/'actual_complete_graph_helper_controls_v22_receipts'
FRESH_E=BASE/'actual_complete_graph_fresh_verifier_v22_receipts'
PURE_PEER=PURE_E/'sealed_independent_actual_original_pure_protocol_review'
FRESH_PEER=FRESH_E/'sealed_independent_actual_complete_fresh_verifier_review'
EXPECTED_META={
 'pure_terminal':(PURE_E/'Root_actual_pure_protocol_tool_terminal_return.json','12d8bbdef3cd59c2f9889d507cf8e5e646f37f4d7e0df1649381373c82100e78'),
 'fresh_terminal':(FRESH_E/'Root_actual_fresh_verifier_tool_terminal_return.json','de3750d802a442329089c5301d36939bda610ddc88bc7770dbe0c0f7f65a76f4'),
 'pure_summary':(PURE_E/'Root_actual_pure_protocol_summary.json','f03a8f32091134c24dbf77da9ec82c0582f3b16c6eaa1841df5934b37064c1a4'),
 'fresh_summary':(FRESH_E/'Root_actual_fresh_verifier_summary.json','fb4ff68bbe2abc319b2e217279e4676327aa0b66ead1cb28fb8bbcb0882b7b6e'),
 'pure_peer':(PURE_PEER/'INDEPENDENT_ACTUAL_PURE_PROTOCOL_META_REVIEW.json','7afd373869bb7b130247dac45378918260a9110c25e548c4ee8ed4c1ce5a5bac'),
 'fresh_peer':(FRESH_PEER/'INDEPENDENT_ACTUAL_COMPLETE_FRESH_VERIFIER_META_REVIEW.json','a143da6f31aa8802d25799e8853591dcdc19ae5b4b285def64a8109c97df389f'),
 'pure_audit':(PURE_PEER/'ACTUAL_PURE_PROTOCOL_META_PEER_AUDIT_TOOL_RETURN.json','38285bb20003c83028460af861a02e2c86690f7bf1e842a0732dc05cb9cbac33'),
 'fresh_audit':(FRESH_PEER/'ACTUAL_COMPLETE_FRESH_VERIFIER_META_PEER_AUDIT_TOOL_RETURN.json','701afc8dfdcf58e54c841956954b4a1c7bc3e6de68a4476dbc3c9f61823d171f'),
 'pure_seal':(PURE_PEER/'INDEPENDENT_ACTUAL_PURE_PROTOCOL_META_PEER_SEAL.json','292237bebb6cea27559544c8dd357c7dc532ff8db741cc736bfd21e67b85f53a'),
 'fresh_seal':(FRESH_PEER/'INDEPENDENT_ACTUAL_COMPLETE_FRESH_VERIFIER_META_PEER_SEAL.json','ba5ff1e7600d8526393fbbce2087ece9cb46d142672de5d91b6881f597e8ea34'),
 'pure_seal_tool':(PURE_PEER/'ACTUAL_PURE_META_PEER_SEAL_TOOL_TERMINAL_RETURN.json','f889c4aabcc1487dd8b2253dba2568c5dccd193bf96ca77a41292437471526a7'),
 'fresh_seal_tool':(FRESH_PEER/'ACTUAL_COMPLETE_FRESH_META_PEER_SEAL_TOOL_TERMINAL_RETURN.json','bf1c914537e6c11f78cbfb8e2edb00fead93667868e662dced65f88940879331'),
 'source_binding':(BASE/'actual_complete_graph_helper_controls_v22_sources/sealed_full_qualification_ROOT_BOUND_SOURCE/ALL_FOUR_ACTUAL_SOURCE_BINDING_INVERSES.json','5cdfb1fead9d8df8a6158cf203028578f6b453ab614863a81540f5172812abe3'),
}
SEEN={}
ART_REFS=[]
BUSINESS=('FUTURE_ACTUAL_COMBINED_DECLARATION_SHA','FUTURE_ACTUAL_COMBINED_PREP_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_SEAL_SHA','FUTURE_ACTUAL_COMBINED_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_RUNTIME_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA')
PUBLIC27=['schema','classification','consumer_scope','consumer_selected_literal_and_canonical_paths','consumer_complete_namespace_root_sequence','scope','phase','graph_content_sha256','fresh_reader_contract','canonical_files_read','actual_bytes_read','byte_count_scope','logical_owner_requirements','exhaustive_namespaces_checked','explicit_aliases_checked','coverage','trace_coverage','live_io_scope','live_subprocesses_reexecuted','declared_absence_inputs_checked_before_and_after_bytes','absence_inputs_are_not_regular_bytes_or_science','caller_must_recheck_current_OS_identity_and_live_probe_results','typed_snapshot','science_qualification_created','live_resources_verified','external_declaration_exit0_verified','caller_must_verify_live_environment_modules_PID_time_and_resources']

def identity(p):
    s=Path(p).lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def pin(p):
    p=Path(p);before=identity(p)
    assert stat.S_ISREG(before[2]) and not p.is_symlink()
    with p.open('rb') as f:digest=hashlib.file_digest(f,'sha256').hexdigest()
    assert identity(p)==before
    return dict(path=str(p),sha256=digest,size_bytes=before[4],identity=before)

def sha(value):
    assert type(value) is str and len(value)==64 and all(x in '0123456789abcdef' for x in value) and value!='0'*64
    return value

def pairs(items):
    result={}
    for k,v in items:
        assert k not in result, 'duplicate JSON key';result[k]=v
    return result

def reject_constant(value):raise ValueError('nonfinite JSON constant '+value)

def finite(value):
    if type(value) is float:assert math.isfinite(value)
    elif type(value) is dict:
        for x in value.values():finite(x)
    elif type(value) is list:
        for x in value:finite(x)

def read_META(p,expected_sha=None):
    p=Path(p)
    assert p.is_absolute() and '..' not in p.parts
    assert not p.is_relative_to(ART), 'SOURCE binding must not read ART payload or graph'
    assert p.is_relative_to(BASE) or p.is_relative_to(HERE)
    before=pin(p)
    if expected_sha is not None:assert before['sha256']==sha(expected_sha)
    value=json.loads(p.read_bytes(),object_pairs_hook=pairs,parse_constant=reject_constant);finite(value)
    assert pin(p)==before
    if str(p) in SEEN:assert SEEN[str(p)]==before
    SEEN[str(p)]=before
    return value

def ref_shape(value):
    assert type(value) is dict and type(value['path']) is str and Path(value['path']).is_absolute()
    assert '..' not in Path(value['path']).parts
    sha(value['sha256'])
    ids=value.get('identity',value.get('identity7'))
    assert type(ids) is list and len(ids)==7 and all(type(x) is int for x in ids)
    assert ids[4]>=0 and stat.S_ISREG(ids[2])
    if 'size_bytes' in value:assert type(value['size_bytes']) is int and value['size_bytes']==ids[4]

def verify_ref(value):
    ref_shape(value);p=Path(value['path'])
    if p.is_relative_to(ART):
        ART_REFS.append(value);return value
    assert p.is_relative_to(BASE) or p==EXPECTED_HELPER, 'finite known META/Source references only'
    actual=pin(p)
    assert actual['sha256']==value['sha256'] and actual['identity']==value.get('identity',value.get('identity7'))
    if 'size_bytes' in value:assert actual['size_bytes']==value['size_bytes']
    if str(p) in SEEN:assert SEEN[str(p)]==actual
    SEEN[str(p)]=actual
    return value

def collect_full_references(value):
    if type(value) is dict:
        if 'path' in value and 'sha256' in value and ('identity' in value or 'identity7' in value):verify_ref(value)
        for x in value.values():collect_full_references(x)
    elif type(value) is list:
        for x in value:collect_full_references(x)

def exact(value,other):
    if type(value) is not type(other):return False
    if type(value) is float:return struct.pack('!d',value)==struct.pack('!d',other)
    if type(value) is dict:return list(value)==list(other) and all(exact(value[k],other[k]) for k in value)
    if type(value) is list:return len(value)==len(other) and all(exact(a,b) for a,b in zip(value,other))
    return value==other

def actual_terminal(value,schema,chunk):
    assert value['schema']==schema and value['closed'] is True and value['actual_tool_terminal_return_observed'] is True
    assert value['session_repolled_after_close'] is False
    tr=value['terminal_tool_return'];assert tr['chunk_id']==chunk and type(tr['exit_code']) is int and tr['exit_code']==0 and 'session_id' not in tr
    assert value['actual_new_helper_qualification_sha256'] is None

def typed_caps(value,expected):
    assert set(value)==set(expected)
    for k,v in expected.items():assert type(value[k]) is int and value[k]==v

def validate_Q(q):
    assert q['schema']==Q_SCHEMA and q['status']==Q_STATUS
    hp=q['helper'];ref_shape(hp)
    assert hp['path']==str(EXPECTED_HELPER) and hp['sha256']==HELPER_SHA and hp['identity']==HELPER_ID and hp['size_bytes']==148965
    verify_ref(hp)
    for k in ('supervisor_class_or_MRO_modified','profile_used','fresh_production_graph_created','fresh_runtime_INPUT_qualified','new_combined_prepared','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted','whole_build_qualified','whole_INPUT_admitted','physical_balance_qualified'):assert q[k] is False
    assert q['Root_finite_joint_META_only_no_project_API_or_numeric'] is True
    assert type(q['Root_finite_joint_META_fresh_explicit_full_EOF_SHA7ID_verified_unique_input_count']) is int and q['Root_finite_joint_META_fresh_explicit_full_EOF_SHA7ID_verified_unique_input_count']>0
    typed_caps(q['original_caps'],dict(whole_seconds=60,stage_seconds=60,rss_mib=512,archive_bytes=64*2**20,history_bytes=96*2**30,free_bytes=8*2**30,threads=1,children=1,retries=0))
    f=q['complete_current_graph_fresh_verifier']
    typed_caps(f['original_caps'],dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_HOST_OUT_SOURCE_E_archive_bytes=64*2**20,history_bytes=96*2**30,free_bytes=8*2**30,threads=1,children=1,retries=0))
    assert f['full_public_return_field_order']==PUBLIC27
    assert f['all_27_fields_nested_type_order_value_floatbits_and_wire_bytes_equal'] is True
    assert f['complete_actual_unfiltered_read_trace_counts']==dict(records=37112,attempts=37112,canonical_files=37111,external_graph_reads=1,no_subprocess_reexecuted=True)
    assert type(f['private_positive_controls']) is int and f['private_positive_controls']==4
    assert type(f['private_reject_controls']) is int and f['private_reject_controls']==3
    assert f['actual_external_Root_exit0_closed_and_saved_peer_pass'] is True
    assert f['legacy_SOURCE33_key_is_compatibility_alias_not_V22_source_count'] is True
    assert type(q['pure_source_member_count']) is int and q['pure_source_member_count']>0
    assert type(f['complete_source_member_count']) is int and f['complete_source_member_count']>0
    proto=q['full_protocol']
    for k in ('original_and_fresh_small_producer_values_types_order_floatbits_exact','all_caller_mutable_identity_and_subtype_attributes_unchanged','complete_old_graph_two_normal_strict_entrances_exact','new_creation_trace_not_substituted_into_old_graph','full_json_types_order_floatbits_and_values_retained','default_source_nonmutation'):assert proto[k] is True
    assert type(proto['accepted_str_subtype_groups']) is int and proto['accepted_str_subtype_groups']==2
    assert type(proto['small_codec_rejections']) is int and proto['small_codec_rejections']==61
    assert proto['complete_original_graph_counts']['canonical_files']==36776 and proto['complete_original_graph_counts']['requirements']==237767 and proto['complete_original_graph_counts']['read_trace_records']==62332
    assert proto['complete_new_creation_trace_records']==63379 and proto['complete_new_creation_trace_actual_attempts']==175886
    assert q['original_protocol_preserved_and_new_owner_controls_independently_saved_reviewed'] is True
    validate_private_owner_controls(q['private_owner_consume_controls'])
    links={'pure_terminal':q['actual_root_terminal'],'fresh_terminal':f['actual_root_terminal'],'pure_summary':q['actual_controls_summary'],'fresh_summary':f['actual_controls_summary'],'pure_peer':q['independent_actual_review'],'fresh_peer':f['independent_actual_review'],'pure_audit':q['independent_actual_review_tool_return'],'fresh_audit':f['independent_actual_review_tool_return'],'pure_seal':q['sealed_independent_pure_actual_review_manifest'],'fresh_seal':f['sealed_independent_actual_review_manifest'],'pure_seal_tool':q['independent_pure_actual_review_seal_tool_return'],'fresh_seal_tool':f['independent_actual_review_seal_tool_return'],'source_binding':f['source_binding_record']}
    data={}
    for name,ref in links.items():
        path,digest=EXPECTED_META[name]
        assert ref['path']==str(path) and ref['sha256']==digest
        verify_ref(ref);data[name]=read_META(path,digest)
    actual_terminal(data['pure_terminal'],'ROOT_V22_ACTUAL_PURE_PROTOCOL_TOOL_TERMINAL_RETURN_V1','6f6847')
    actual_terminal(data['fresh_terminal'],'ROOT_V22_ACTUAL_COMPLETE_CURRENT_GRAPH_FRESH_VERIFIER_TOOL_TERMINAL_RETURN_V1','57a6f5')
    for name,schema,count in (('pure_peer','INDEPENDENT_V22_ACTUAL_PURE_PROTOCOL_SAVED_META_PEER_REVIEW_V1',1084),('fresh_peer','INDEPENDENT_V22_ACTUAL_COMPLETE_CURRENT_GRAPH_FRESH_VERIFIER_SAVED_META_PEER_REVIEW_V1',686)):
        v=data[name];assert v['schema']==schema and v['PASS'] is True and v['hard_blockers']==[]
        assert type(v['check_count']) is int and v['check_count']==len(v['checks'])==count
        assert all(type(row['PASS']) is bool and row['PASS'] is True for row in v['checks'])
        assert v['new_Q'] is None
    assert data['pure_peer']['pure_protocol_saved_evidence_independently_reviewed'] is True
    assert data['fresh_peer']['full_current_graph_saved_evidence_independently_reviewed'] is True
    assert data['fresh_peer']['all27_return_fields']==PUBLIC27
    assert data['fresh_peer']['unfiltered37112trace_complete_order_path_sequence_sha256']=='54e9a6fe108093c2f92d31c8c2c5e38e0cad153ee170eafc8e59c44fa6d99a30'
    assert exact(data['pure_summary']['private_owner_consume_controls'],q['private_owner_consume_controls'])
    for name,kind in (('pure_summary','PURE'),('fresh_summary','FRESH')):
        v=data[name];assert v['schema']=='ROOT_V22_ACTUAL_COMPLETE_QUALIFICATION_SUMMARY_V1' and v['status']=='ACTUAL_EXIT0_CLOSED_COMPLETE_'+kind+'_CONTROLS_SAVED_REVIEW_REQUIRED'
        assert v['independent_saved_actual_review_pass'] is False and v['actual_new_helper_qualification_sha256'] is None
        assert v['closed'] is True and type(v['actual_Root_exit_code']) is int and v['actual_Root_exit_code']==0
        for k in ('whole_build_qualified','whole_INPUT_admitted','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted','physical_balance_qualified'):assert v[k] is False
    pa=data['pure_audit'];assert pa['chunk_id']=='bfea93' and type(pa['exit_code']) is int and pa['exit_code']==0 and 'session_id' not in pa
    fa=data['fresh_audit'];assert fa['schema']=='INDEPENDENT_ACTUAL_COMPLETE_FRESH_VERIFIER_META_PEER_AUDIT_TOOL_RETURN_V1' and fa['closed'] is True
    tr=fa['terminal_tool_return'];assert tr['chunk_id']=='722af0' and type(tr['exit_code']) is int and tr['exit_code']==0 and 'session_id' not in tr
    for name,key,chunk in (('pure_seal','all1084savedactualchecksPASS','bfea93'),('fresh_seal','all686_saved_actual_checksPASS','722af0')):
        v=data[name];assert v[key] is True and v['actual_peer_closed'] is True and type(v['actual_peer_exit_code']) is int and v['actual_peer_exit_code']==0
        a=v['actual_peer_audit_tool_return'];assert a['chunk_id']==chunk and type(a['exit_code']) is int and a['exit_code']==0 and 'session_id' not in a
        assert v['new_Q'] is None
    for name,chunk in (('pure_seal_tool','28f447'),('fresh_seal_tool','407e5a')):
        v=data[name];assert v['closed'] is True;tr=v['terminal_tool_return'];assert tr['chunk_id']==chunk and type(tr['exit_code']) is int and tr['exit_code']==0 and 'session_id' not in tr
    gz=f['complete_gzips'];saved_gz=data['fresh_peer']['all_three_complete_gzip_pins']
    assert list(gz)==list(saved_gz)==['expected_complete_return_contract','actual_complete_verifier_return','actual_complete_ReadOpenAudit_trace']
    for key,item in gz.items():
        ref_shape(item);complete=saved_gz[key];ref_shape(complete)
        for field in ('path','sha256','identity','size_bytes'):assert exact(item[field],complete[field])
        assert complete['complete_JSON_wire_gzip_decompression_EOF_SHA_verified'] is True and complete['no_fields_or_records_filtered'] is True
    assert gz['expected_complete_return_contract']['sha256']==gz['actual_complete_verifier_return']['sha256']
    assert saved_gz['expected_complete_return_contract']['uncompressed_JSON_sha256']==saved_gz['actual_complete_verifier_return']['uncompressed_JSON_sha256']
    assert data['source_binding']['schema']=='AXMAT_V22_ROOT_ACTUAL_SOURCE_ONLY_QUALIFICATION_BINDING_INVERSES_V1'
    assert data['source_binding']['new_Q'] is None
    collect_full_references(q)

def replacements(text,edits):
    for e in edits:
        assert text.count(e['old'])==1,e['label'];text=text.replace(e['old'],e['new'],1)
    return text

def inverse(text,edits):
    for e in reversed(edits):
        assert text.count(e['new'])==1,e['label'];text=text.replace(e['new'],e['old'],1)
    return text

def definition_segments(text):
    return {n.name:ast.get_source_segment(text,n) for n in ast.parse(text).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}

def dump(p,value):
    with Path(p).open('x') as f:json.dump(value,f,indent=2,allow_nan=False);f.write('\n')

def main():
    assert not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE') and sys.getprofile() is None
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('actual_Q_path');ap.add_argument('actual_Q_sha256');ap.add_argument('fresh_TMP_output')
    args=ap.parse_args();qp=Path(args.actual_Q_path)
    assert qp==EXPECTED_Q and qp.is_absolute()
    sha(args.actual_Q_sha256)
    output=Path(args.fresh_TMP_output)
    assert output.is_absolute() and output.is_relative_to(Path('/private/tmp')) and not os.path.lexists(output)
    package=read_META(HERE/'MANIFEST.json')
    inventory=sorted(str(p.relative_to(HERE)) for p in HERE.rglob('*') if p.is_file())
    assert inventory==sorted(list(package['members'])+['MANIFEST.json'])
    for rel,expected in package['members'].items():
        actual=pin(HERE/rel);assert actual==expected;SEEN[str(HERE/rel)]=actual
    constants=read_META(HERE/'ROOT_BINDING_SOURCE_CONSTANTS.json')
    q=read_META(qp,args.actual_Q_sha256);validate_Q(q)
    qpin=SEEN[str(qp)]
    for name,expected in constants['original_sources'].items():
        actual=pin(expected['path']);assert actual==expected;SEEN[actual['path']]=actual
    proof=read_META(HERE/'COMPLETE_SOURCE_INVERSES.json')
    templates={name:(HERE/(name+'.V22.UNREADY.full.py')).read_text() for name in ('canonical','host','writer')}
    ce=[dict(label='actual_Q_READY_doc',old=repr(constants['UNREADY_DOC']),new=repr(constants['READY_DOC'])),dict(label='actual_Q_READY_status',old="DRAFT_STATUS = 'UNREADY_V22_COMPLETE_NEW_HELPER_ACTUAL_Q_UNBOUND'",new="DRAFT_STATUS = 'READY_REVIEWED_V22_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY'"),dict(label='qualified_cf0_helper_SHA',old="(ROOT/'validation/axial_material/combined_runtime_complete_input_graph_private_owner_namespace_last_use_20261010.py',None)",new="(ROOT/'validation/axial_material/combined_runtime_complete_input_graph_private_owner_namespace_last_use_20261010.py',"+repr(HELPER_SHA)+")"),dict(label='actual_new_Q_SHA',old='FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA = None',new='FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA = '+repr(args.actual_Q_sha256))]
    canonical=replacements(templates['canonical'],ce);canonical_sha=hashlib.sha256(canonical.encode()).hexdigest()
    he=[dict(label='host_Source_binding_status',old="SOURCE_BINDING_STATUS='UNREADY_V22_ACTUAL_Q_AND_TARGET_SOURCE_UNBOUND'",new="SOURCE_BINDING_STATUS='READY_V22_ACTUAL_Q_AND_TARGET_SOURCE_BOUND'"),dict(label='host_actual_canonical_SHA',old='TARGET_SHA=None',new='TARGET_SHA='+repr(canonical_sha)),dict(label='host_actual_new_Q_path',old='ACTUAL_HELPER_Q_PATH=None',new='ACTUAL_HELPER_Q_PATH=Path('+repr(str(qp))+')'),dict(label='host_actual_new_Q_SHA',old='ACTUAL_HELPER_Q_SHA=None',new='ACTUAL_HELPER_Q_SHA='+repr(args.actual_Q_sha256))]
    we=[dict(label='writer_Source_binding_status',old="SOURCE_BINDING_STATUS='UNREADY_V22_ACTUAL_Q_AND_CANONICAL_SOURCE_UNBOUND'",new="SOURCE_BINDING_STATUS='READY_V22_ACTUAL_Q_AND_CANONICAL_SOURCE_BOUND'"),dict(label='writer_actual_canonical_SHA',old='FACTORY_SHA=None',new='FACTORY_SHA='+repr(canonical_sha)),dict(label='writer_truthful_doc',old='"""UNREADY V22 Root PREP metadata writer Source template; only Root after actual Q binding and genuine CLOSED EXIT0 PREP may execute the bound writer."""',new='"""Root metadata only, after a genuine, closed, successful V22 PREP tool return. Actual new helper Q and complete READY canonical Source bound; no PREP success is fabricated by Source binding."""')]
    bound={'canonical':canonical,'host':replacements(templates['host'],he),'writer':replacements(templates['writer'],we)}
    edits={'canonical':ce,'host':he,'writer':we};full_inverse={}
    for name,text in bound.items():
        back=inverse(text,edits[name]);assert back==templates[name]
        parent=inverse(back,proof['exact_finite_transforms'][name])
        actual_parent=(HERE/(name+'.V21.parent.full.py')).read_text();assert parent==actual_parent
        assert ast.dump(ast.parse(parent),include_attributes=False)==ast.dump(ast.parse(actual_parent),include_attributes=False)
        assert definition_segments(text)==definition_segments(templates[name]),'READY binding must change no function body'
        full_inverse[name]=dict(READY_to_UNREADY_edits=edits[name],UNREADY_to_original_parent_edits=proof['exact_finite_transforms'][name],complete_byte_inverse=True,complete_AST_inverse=True,READY_all_functions_byte_exact=True,original_parent=constants['original_sources'][name])
    nodes=ast.parse(canonical).body
    assignments={t.id:n.value for n in nodes if isinstance(n,ast.Assign) for t in n.targets if isinstance(t,ast.Name)}
    assert len(definition_segments(canonical))==70
    for k in BUSINESS:assert isinstance(assignments[k],ast.Constant) and assignments[k].value is None
    for p,expected in SEEN.items():assert pin(p)==expected
    output.mkdir()
    filenames={'canonical':'complete_combined_runtime.V22.READY_SOURCE.py','host':'combined_prepare_host.py','writer':'write_actual_prepare_terminal.py'}
    for name,text in bound.items():
        with (output/filenames[name]).open('x') as f:f.write(text)
    with (output/'ACTUAL_NEW_JOINT_HELPER_Q.byte_exact.json').open('xb') as f:f.write(qp.read_bytes())
    assert pin(output/'ACTUAL_NEW_JOINT_HELPER_Q.byte_exact.json')['sha256']==qpin['sha256']
    dump(output/'actual_READY_binding_complete_SOURCE_inverse.json',dict(schema='V22_ACTUAL_Q_BOUND_COMPLETE_CANONICAL_GENUINE_PREP_SOURCE_INVERSES_V1',source_only=True,new_actual_Q=qpin,all_complete_byte_AST_inverses=True,full_inverse=full_inverse,all70runtime_definitions_retained=True,six_future_business_pins={k:None for k in BUSINESS},original_complete_PREP_caps=constants['caps'],full_original_Source_inputs_preserved=True,complete_dynamic_Source_inventory_preserved=True,ART_references_preserved_not_read=ART_REFS,all_read_Source_and_saved_META_before_after_pins=list(SEEN.values()),installed_or_executed=False))
    dump(output/'SOURCE_binding_result.json',dict(schema='V22_ROOT_COMPLETE_CANONICAL_GENUINE_PREP_ACTUAL_Q_SOURCE_BINDING_ONLY_V1',source_only=True,actual_Q=qpin,READY_source=pin(output/filenames['canonical']),genuine_PREP_host_Source=pin(output/filenames['host']),complete_PREP_metadata_writer_Source=pin(output/filenames['writer']),new_helper_qualification_created_by_this_Source_binder=False,helper_guard_API_PREP_build_INPUT_native_or_numeric_executed=False,canonical_or_ART_or_Root_D_E_written=False,all_future_business_pins={k:None for k in BUSINESS},requires_Root_external_saved_Q_review_and_bound_Source_review_before_installation=True))
    members={str(p.relative_to(output)):pin(p) for p in sorted(output.rglob('*')) if p.is_file()}
    dump(output/'MANIFEST.json',dict(schema='V22_ROOT_BOUND_COMPLETE_PREP_SOURCE_PACKAGE_MANIFEST_V1',source_only=True,members=members,member_count=len(members),new_business_executed=False))
    print(json.dumps(dict(source_only=True,actual_Q=qpin,complete_READY_source_sha256=canonical_sha,output=str(output),manifest=pin(output/'MANIFEST.json'),executed_project=False)))

def validate_private_owner_controls(value):
    assert value['schema'] == 'AXMAT_V22_PRIVATE_OWNER_CONSUME_ACTUAL_CONTROL_V1'
    assert value['status'] == 'ACTUAL_PRIVATE_OWNER_CONTROLS_RETURNED_METADATA_ONLY'
    positives = value['positive_controls']; rejects = value['private_guard_rejections']
    subtypes = value['accepted_str_subclass_equivalence_controls']; partial = value['partial_invalid_second_owner_rejections']
    assert len(positives) == 4 and [r['case'] for r in positives] == ['default_list', 'default_tuple', 'explicit_False_list', 'owned_builtin_list_True']
    for row in positives:
        assert row['full_normalized_descriptor_types_order_values_attrs_floatbits_equal_default'] is True
        assert row['expected_complete_descriptor_signature'] == row['actual_complete_descriptor_signature']
        if row['case'] == 'owned_builtin_list_True': assert row['owned_list_completely_cleared_after_success'] is True
        else: assert row['caller_full_identity_type_order_value_attrs_floatbits_unchanged'] is True
    assert len(rejects) == 3 and [r['case'] for r in rejects] == ['nonbool_consume', 'tuple_True', 'list_subclass_True']
    for row in rejects:
        assert row['class'] == 'InputGraphError'
        assert row['message'] == 'private owner consume needs a bool and an exclusively owned builtin list'
        assert row['caller_full_identity_type_order_value_attrs_floatbits_unchanged'] is True
    assert len(subtypes) == 2 and [r['case'] for r in subtypes] == ['plain_accepted_str', 'accepted_str_with_str_override']
    for row in subtypes:
        assert row['default_caller_full_identity_type_order_value_attrs_floatbits_unchanged'] is True
        assert row['owned_list_completely_cleared_after_success'] is True
        assert row['complete_normalized_descriptor_types_order_value_strattrs_floatbits_equal_default'] is True
        assert row['expected_complete_descriptor_signature'] == row['actual_complete_descriptor_signature']
    assert len(partial) == 2 and [r['case'] for r in partial] == ['invalid_second_owner_default', 'invalid_second_owner_owned_True']
    assert all(r['class'] == 'InputGraphError' and r['message'] == 'missing file owner' for r in partial)
    for key in ('first_valid_slot_None_after_original_validate_and_append', 'invalid_second_slot_original_identity_and_value_unchanged', 'default_partial_caller_unchanged', 'original_owner_rejection_class_order_message_preserved', 'original_protocol_controls_fixtures_and_caps_unchanged', 'no_new_fixture_file_or_IO_created'):
        assert value[key] is True
    assert value['new_helper_qualification_created'] is False and value['business_or_science_qualification_created'] is False

if __name__=='__main__':main()
