import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import stat

R=Path('/Users/wen/spot')
B=R/'validation/axial_material/complete_history_root_index_source_v15_20261010'
ART=R/'validation/artifacts'
E=B/'actual_complete_combined_prepare_v22_receipts'
OLD=B/'actual_complete_combined_build_v21_sources/combined_build_host.py'
OLD_SHA='ebe99a7aaf7abd4e073d0e206bea205344e186d5a3be144a012443f1cd51a196'
TARGET=R/'validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v22.py'
TARGET_SHA='09e53974005082a14d9675f69258549609a991f86ec231ab6b15edfe20dd265e'

def read(p):
    assert p.is_absolute() and p.resolve()==p and not p.is_relative_to(ART)
    s=p.lstat();i=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
    assert stat.S_ISREG(s.st_mode) and s.st_nlink==1
    b=p.read_bytes();t=p.lstat()
    assert i==[t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns]
    return b,dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=i)
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

a=argparse.ArgumentParser()
a.add_argument('--saved-prep-peer-report',required=True)
a.add_argument('--saved-prep-peer-report-sha256',required=True)
a.add_argument('--destination',required=True)
args=a.parse_args()
P=Path(args.saved_prep_peer_report);dest=Path(args.destination)
assert str(dest).startswith('/private/tmp/') and dest.is_absolute() and not dest.exists()
pb,pp=read(P);assert pp['sha256']==args.saved_prep_peer_report_sha256
peer=json.loads(pb)
assert peer['status']=='PASS_ACTUAL_COMPLETE_PREP_ONLY'
assert peer['all_checks_typed_true'] is True
assert type(peer['blockers']) is list and not peer['blockers']
assert peer['actual_PREP_closed_EXIT0_verified'] is True
assert peer['actual_metadata_writer_closed_EXIT0_verified'] is True
assert peer['all_complete_scope_verified'] is True
assert peer['schema']=='INDEPENDENT_V22_ACTUAL_COMPLETE_PREP_SAVED_META_REVIEW_V1'
assert peer['actual_PREP_metadata_only'] is True
for field in ('whole_combined_build_qualified','whole_combined_INPUT_admitted','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted','physical_balance_qualified'):
    assert peer[field] is False
sb,sp=read(E/'Root_actual_complete_combined_prepare_summary.json');s=json.loads(sb)
assert peer['actual_Root_PREP_summary_pin']==sp
assert peer['actual_Root_PREP_terminal_pin']==pin(E/'Root_actual_prepare_tool_terminal_return.json')
assert peer['actual_complete_namespace_manifest_pin']==pin(E/'Root_actual_complete_prepare_namespace_manifest.json')
assert s['schema']=='ROOT_V22_ACTUAL_COMPLETE_COMBINED_PREPARE_SUMMARY_V1'
assert s['status']=='ACTUAL_COMPLETE_PREPARE_EXIT0_CLOSED_ONLY_NOT_COMPLETE_BUILD'
caps=('whole_wall_cap_seconds','stage_wall_cap_seconds','rss_mib','joint_archive_cap_bytes','history_cap_bytes','free_floor_bytes','threads','children','retries')
wanted=(1800,600,512,2*2**30,96*2**30,8*2**30,1,1,0)
assert all(type(s[k]) is int and s[k]==v for k,v in zip(caps,wanted))
assert s['original_caps_preserved'] is True and 0<=s['sampled_peak_rss_mib']<512
assert 0<s['child_seconds']<=600 and s['child_seconds']<=s['whole_seconds']<1800
assert 0<s['joint_archive_bytes']<2*2**30
for k in ('new_five_stage_build_executed','original_five_build_stages_executed','whole_combined_INPUT_admitted','new_native_transport_executed','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted','cleanup_performed','goal_complete'):assert s[k] is False
tp=ref3(s['actual_root_terminal'],E/'Root_actual_prepare_tool_terminal_return.json')
assert s['Root_actual_terminal']==s['actual_root_terminal']
terminal=json.loads(read(Path(tp['path']))[0]);tr=terminal['terminal_tool_return']
assert terminal['closed'] is True and type(tr['exit_code']) is int and tr['exit_code']==0 and not tr.get('session_id')
assert terminal.get('session_repolled_after_close',False) is False
np=ref3(s['namespace_manifest'],E/'Root_actual_complete_prepare_namespace_manifest.json')
namespace=json.loads(read(Path(np['path']))[0])
assert namespace['schema']=='ROOT_V22_ACTUAL_COMPLETE_PREPARE_ALL_NAMESPACES_V1' and namespace['no_build_or_native_credit'] is True
ns={d['root']:d for d in namespace['namespaces']}
H=ART/'axial-material-complete-combined-prepare-host-v22-20261010'
S=ART/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v22-20261010'
O=ART/'axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v22-20261010'
T=ART/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v22-20261010'
D=B/'actual_complete_combined_prepare_v22_sources'
assert len(ns)==5 and set(ns)=={str(p) for p in (H,S,O,T,D)}
outrefs={
 'declaration':outputref(s['actual_declaration'],O/'declaration.json'),
 'prep':outputref(s['formal_PREP_terminal'],T/'declaration_terminal_return.json'),
 'graph':outputref(s['actual_complete_input_graph'],O/'input_graph.json'),
 'trace':outputref(s['actual_complete_creation_trace'],O/'input_creation_python_open_trace.json'),
 'source_admission':outputref(ns[str(S)]['files']['source_admission.json'],S/'source_admission.json'),
}
for name,ref in outrefs.items():
    root=T if name=='prep' else S if name=='source_admission' else O
    assert ns[str(root)]['files'][str(Path(ref['path']).relative_to(root))]==ref
old,oldp=read(OLD);assert oldp['sha256']==OLD_SHA
canonical,cp=read(TARGET);assert cp['sha256']==TARGET_SHA
assert namespace['canonical_factory']=={k:cp[k] for k in ('path','sha256','identity')}
globals={}
for node in ast.parse(canonical).body:
    if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name):
        try:globals[node.targets[0].id]=ast.literal_eval(node.value)
        except (ValueError,TypeError):pass
assert globals['DRAFT_STATUS']=='READY_REVIEWED_V22_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY'
for k in ('FUTURE_ACTUAL_COMBINED_DECLARATION_SHA','FUTURE_ACTUAL_COMBINED_PREP_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_SEAL_SHA','FUTURE_ACTUAL_COMBINED_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_RUNTIME_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA'):assert globals[k] is None
qpath=B/'Root_actual_complete_graph_private_owner_namespace_helper_admission_v22.json'
qb,qp=read(qpath);assert qp['sha256']=='89d2f03c0af74844731ddf5225307c38ae40521d99ca29c88c5d8db39796b816'
q=json.loads(qb);assert q['status']=='QUALIFIED_ORIGINAL_FULL_PROTOCOL_AND_COMPLETE_CURRENT_GRAPH_METADATA_VERIFIER_ONLY_V22'
hp=pin(R/'validation/axial_material/combined_runtime_complete_input_graph_private_owner_namespace_last_use_20261010.py')
assert hp['sha256']=='cf0c2b6b6fd6b1adceec85b261008871f12769832b4dbd4fdb4204f650b4e72c' and q['helper']==hp
records=[];text=old.decode()
changes=[
 ('axial-material-complete-combined-build-host-v21-20261010','axial-material-complete-combined-build-host-v22-20261010'),
 ('prepare_sender_window_root_index_graph_trace_table_combined_runtime_v21.py','prepare_sender_window_root_index_graph_trace_table_combined_runtime_v22.py'),
 ('023abc88dd60e89cb49ebacb881f555850b7732149b14caf14503bd135a391e5',TARGET_SHA),
 ('axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v21-20261010',S.name),
 ('axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v21-20261010',O.name),
 ('axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v21-20261010',T.name),
 ('actual_complete_combined_build_v21_sources','actual_complete_combined_build_v22_sources'),
 ('SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_LINK_V21','SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_LINK_V22'),
 ('AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V21_DECLARATION_V1','AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V22_DECLARATION_V1'),
 ('AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V21_BUILD_SEAL_V1','AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V22_BUILD_SEAL_V1'),
 ('AXMAT_V21_GENUINE_COMPLETE_COMBINED_BUILD_HOST_V1','AXMAT_V22_GENUINE_COMPLETE_COMBINED_BUILD_HOST_V1'),
 ('combined_runtime_complete_input_graph_private_verifier_trace_consume_20261010.py','combined_runtime_complete_input_graph_private_owner_namespace_last_use_20261010.py'),
 ('dc01d8cf4478f9dc918ecb828acf7d79a50fb93422bfcffe165df38978ede6a7',hp['sha256']),
 ('Root_actual_complete_graph_private_verifier_helper_admission_v21.json',qpath.name),
 ('29ac1abd0df3ff9d1d71a3239842e1c97cb2619cc4627292b0d25f6e16218bb2',qp['sha256']),
 ('80d67cd194eed1d229e46cd5512df9ba4b00954e7f6e7b36dd8ea6902851d6af',outrefs['declaration']['sha256']),
 ('7e340a31596aa58518ebde4231bd3542554acb0a4ea1888f1df7ea14bec50dcf',outrefs['prep']['sha256']),
 ('d5622ad2b2661a336134cb97a2bbf113bfb76327a467149644e539a0009c2779',outrefs['graph']['sha256']),
 ('06fb0e5b3abe6efd38a0656e0b1e3572581ceab018825cd07be3f52683876244',outrefs['trace']['sha256']),
 ('actual_complete_combined_prepare_v21_receipts','actual_complete_combined_prepare_v22_receipts'),
 ('21ee531ce1a2032cb2d6fb86fe86603ae1a9bec3300ff982d033248ac9700344',sp['sha256']),
]
for before,after in changes:
    count=text.count(before);assert count>0 and before!=after
    text=text.replace(before,after);records.append(dict(before=before,after=after,count=count))
restored=text
for record in reversed(records):
    assert restored.count(record['after'])==record['count']
    restored=restored.replace(record['after'],record['before'])
assert restored.encode()==old
compile(text,str(dest/'combined_build_host.py'),'exec')
values={}
for n in ast.parse(text).body:
    if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
        try:values[n.targets[0].id]=ast.literal_eval(n.value)
        except (ValueError,TypeError):pass
assert values['EXPECTED_LABELS']==['build/link','metadata/objects','metadata/executable','metadata/dependencies','audit/audit']
assert len(values['EXPECTED_COMMANDS'])==5
assert values['EXPECTED_COMMANDS'][-1]==['/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12',str(TARGET),'audit-build','--sha256',outrefs['declaration']['sha256'],'--prep-sha256',outrefs['prep']['sha256']]
assert text.count('WHOLE_CAP,STAGE_CAP,RSS_CAP,ARCHIVE_CAP=1800,600,512,2*2**30')==1
source_inputs=[oldp,cp,sp,tp,np,pp,qp,hp,pin(Path(__file__))]
for ref in source_inputs:assert pin(Path(ref['path']))==ref
dest.mkdir()
write(dest/'combined_build_host.py',text.encode())
write(dest/'original_full_V21_build_host.byte_exact.py',old)
write(dest/'ROOT_ACTUAL_FULL_BUILD_SOURCE_binding_writer.py',Path(__file__).read_bytes())
write(dest/'Root_actual_full_build_Source_binding_inverse.json',jsonbytes(dict(schema='ROOT_V22_ACTUAL_FULL_FIVE_STAGE_BUILD_SOURCE_BINDING_INVERSE_V1',source_only=True,complete_original_host=oldp,actual_new_host=pin(dest/'combined_build_host.py'),complete_byte_inverse_to_original=True,finite_changes=records,all_original_full_five_stages_retained=True,original_caps=[1800,600,512,2*2**30,96*2**30,8*2**30,1,1,0],actual_closed_PREP_summary=sp,actual_Root_closed_terminal=tp,actual_complete_NAMESPACE=np,actual_saved_PREP_peer=pp,all_actual_output_references=outrefs,all_source_inputs=source_inputs,ART_payload_opened=False,project_helper_guard_API_business_numeric_executed=False,whole_build_INPUT_native_science_qualified=False)))
write(dest/'ACTUAL_SAVED_PREP_PEER.byte_exact.json',pb)
members={p.name:pin(p) for p in sorted(dest.iterdir())}
write(dest/'MANIFEST.json',jsonbytes(dict(schema='ROOT_V22_ACTUAL_FULL_BUILD_SOURCE_BOUND_PACKAGE_MANIFEST_V1',source_only=True,members=members,member_count=len(members),new_business_executed=False)))
print(json.dumps({'manifest':pin(dest/'MANIFEST.json'),'host':pin(dest/'combined_build_host.py'),'finite_hunks':len(records),'whole_original_build_retained':True,'project_executed':False}))
