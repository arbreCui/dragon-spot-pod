"""Append complete Root SOURCE binding designs; never execute them."""
import ast
import hashlib
import json
from pathlib import Path

P=Path('/private/tmp/axmat_v25_complete_canonical_TRUE_snapshot_jointQ_UNREADY_SOURCE_bwo0x_85')
R=Path('/Users/wen/spot');B=R/'validation/axial_material/complete_history_root_index_source_v15_20261010'

def dump(p,v):
 with p.open('x')as f:json.dump(v,f,indent=2,allow_nan=False);f.write('\n')
def defs(t):return {n.name:ast.get_source_segment(t,n)for n in ast.parse(t).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}

ADAPTER=r'''"""UNREADY complete V25 Root SOURCE binder design. Standard library only.
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

'''

PREP_MAIN=r'''
def main():
    global FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA
    if sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE')or sys.getprofile()is not None:raise ValueError('original nonoptimized unprofiled Source binder required')
    parser=argparse.ArgumentParser();parser.add_argument('actual_Q_path');parser.add_argument('actual_Q_sha256');parser.add_argument('fresh_TMP_output');args=parser.parse_args()
    if Path(args.actual_Q_path)!=ACTUAL_HELPER_Q_PATH:raise ValueError('fixed actual V25 Q path')
    FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA=nonzero_sha(args.actual_Q_sha256)
    output=normal(args.fresh_TMP_output,missing=True)
    if not output.is_relative_to(Path('/private/tmp'))or os.path.lexists(output):raise ValueError('fresh exclusive Source destination')
    source_package();deps=helper_Q_admission();qpin=source_pin(ACTUAL_HELPER_Q_PATH)
    proof=read(HERE/'COMPLETE_SOURCE_INVERSES.json');templates={
        'canonical':(HERE/'canonical.V25.UNREADY.full.py').read_text(),
        'prepare_host':(HERE/'host_and_postclose_templates/prepare_host.V25.UNREADY.full.py').read_text(),
        'prepare_writer':(HERE/'host_and_postclose_templates/prepare_writer.V25.UNREADY.full.py').read_text()}
    edits={k:[]for k in templates};text=templates['canonical']
    doc=ast.get_source_segment(text,ast.parse(text).body[0])
    text=source_replace(text,edits['canonical'],doc,repr('READY Source binding only for V25 complete sender/root-index flow. The new actual V25 full pure/fresh helper metadata Q and both Root terminal/saved peer/install proofs are read before project load. All original complete PREP, five-stage build, whole INPUT, physical and resource gates remain required. No new PREP/build/INPUT/native/science success is supplied by this binding; all six business pins remain None.'),'actual_Q_READY_truthful_doc')
    text=source_replace(text,edits['canonical'],"DRAFT_STATUS = 'UNREADY_V25_COMPLETE_INACTIVE_AUDIT_ACTUAL_Q_UNBOUND'","DRAFT_STATUS = 'READY_REVIEWED_V25_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY'",'actual_Q_READY_status')
    text=source_replace(text,edits['canonical'],'FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA = None','FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA = '+repr(args.actual_Q_sha256),'actual_Q_SHA')
    bound={'canonical':text};canonical_sha=hashlib.sha256(text.encode()).hexdigest()
    for role in ('prepare_host','prepare_writer'):
        text=source_future_bind(templates[role],{'FUTURE_V25_ACTUAL_Q_SHA':args.actual_Q_sha256,'FUTURE_V25_CANONICAL_SHA':canonical_sha},edits[role])
        old="SOURCE_BINDING_STATUS='UNREADY_V25_ACTUAL_Q_AND_TARGET_SOURCE_UNBOUND'"if role=='prepare_host'else"SOURCE_BINDING_STATUS='UNREADY_V25_ACTUAL_Q_AND_CANONICAL_SOURCE_UNBOUND'"
        new="SOURCE_BINDING_STATUS='READY_V25_ACTUAL_Q_AND_TARGET_SOURCE_BOUND'"if role=='prepare_host'else"SOURCE_BINDING_STATUS='READY_V25_ACTUAL_Q_AND_CANONICAL_SOURCE_BOUND'"
        text=source_replace(text,edits[role],old,new,'actual_Q_and_canonical_bound');bound[role]=text
    inverses={}
    for role,text in bound.items():
        if source_definitions(text)!=source_definitions(templates[role]):raise ValueError('Source binding changes no function body')
        inverses[role]=source_verify_original_inverse(role,text,edits[role],proof)
    assignments={node.targets[0].id:node.value for node in ast.parse(bound['canonical']).body if isinstance(node,ast.Assign)and len(node.targets)==1 and isinstance(node.targets[0],ast.Name)}
    for key in BUSINESS:
        if not isinstance(assignments[key],ast.Constant)or assignments[key].value is not None:raise ValueError('all six business pins remain unknown')
    for path,wanted in tuple(READ_PINS.items()):
        if source_pin(path)!=wanted:raise ValueError('Source binding inputs changed')
    output.mkdir();filenames={'canonical':'prepare_sender_window_root_index_graph_trace_table_combined_runtime_v25.py','prepare_host':'combined_prepare_host.py','prepare_writer':'write_actual_prepare_terminal.py'}
    for role,text in bound.items():(output/filenames[role]).write_text(text)
    (output/'ACTUAL_V25_HELPER_ONLY_JOINT_Q.byte_exact.json').write_bytes(ACTUAL_HELPER_Q_PATH.read_bytes())
    source_dump(output/'Root_actual_Q_bound_complete_PREP_Source_inverse.json',dict(schema='V25_ROOT_ACTUAL_Q_BOUND_COMPLETE_PREP_SOURCE_INVERSE_V1',source_only=True,actual_Q=qpin,complete_original_source_inverses=inverses,all_Q_and_proof_explicit_typed_owner_expected_files=deps,all_read_Source_META_fullpins=list(READ_PINS.values()),all_six_future_business_pins={k:None for k in BUSINESS},candidate_guard_API_compiler_or_numeric_executed=False,installed=False))
    print(json.dumps(dict(source_only=True,actual_Q=qpin,canonical=source_pin(output/filenames['canonical']),host=source_pin(output/filenames['prepare_host']),writer=source_pin(output/filenames['prepare_writer']),manifest=source_manifest(output,'V25_ROOT_ACTUAL_Q_BOUND_COMPLETE_PREP_SOURCE_PACKAGE_V1'),business_or_science_executed=False)))

if __name__=='__main__':main()
'''

BUILD_MAIN=r'''
def main():
    global FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA
    if sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE')or sys.getprofile()is not None:raise ValueError('original nonoptimized Source binder')
    a=argparse.ArgumentParser();a.add_argument('--saved-prep-peer-report',required=True);a.add_argument('--saved-prep-peer-report-sha256',required=True);a.add_argument('--actual-Q-sha256',required=True);a.add_argument('--actual-canonical-sha256',required=True);a.add_argument('--destination',required=True);args=a.parse_args()
    output=normal(args.destination,missing=True)
    if not output.is_relative_to(Path('/private/tmp'))or os.path.lexists(output):raise ValueError('fresh complete build Source namespace')
    source_package();FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA=nonzero_sha(args.actual_Q_sha256);deps=helper_Q_admission()
    E=BASE/'actual_complete_combined_prepare_v25_receipts';TARGET=ROOT/'validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v25.py'
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
    H=ART/'axial-material-complete-combined-prepare-host-v25-20261010';S=ART/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v25-20261010';O=ART/'axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v25-20261010';T=ART/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v25-20261010';D=BASE/'actual_complete_combined_prepare_v25_sources'
    ns={row['root']:row for row in namespace['namespaces']};helper_Q_check(len(ns)==5 and set(ns)=={str(x)for x in (H,S,O,T,D)},'all original complete PREP namespaces')
    outrefs={'declaration':helper_Q_fullpin(s['actual_declaration']),'prep':helper_Q_fullpin(s['formal_PREP_terminal']),'graph':helper_Q_fullpin(s['actual_complete_input_graph']),'trace':helper_Q_fullpin(s['actual_complete_creation_trace']),'source_admission':helper_Q_fullpin(ns[str(S)]['files']['source_admission.json'])}
    for name,row in outrefs.items():
        root=T if name=='prep'else S if name=='source_admission'else O
        helper_Q_check(row['path']==str(root/({'declaration':'declaration.json','prep':'declaration_terminal_return.json','graph':'input_graph.json','trace':'input_creation_python_open_trace.json','source_admission':'source_admission.json'}[name])) and helper_Q_fullpin(ns[str(root)]['files'][str(Path(row['path']).relative_to(root))])==row,'whole PREP actual output full namespace binding')
    cp=source_pin(require(TARGET,args.actual_canonical_sha256));helper_Q_check(helper_Q_fullpin(namespace['canonical_factory'])==cp,'actual installed canonical full Source')
    source_text=TARGET.read_text();assignments={n.targets[0].id:n.value for n in ast.parse(source_text).body if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
    helper_Q_check(ast.literal_eval(assignments['DRAFT_STATUS'])=='READY_REVIEWED_V25_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY' and ast.literal_eval(assignments['FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA'])==args.actual_Q_sha256,'same actual Q wired canonical')
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
'''

def main():
 contract=(P/'helper_joint_Q_contract.inline_SOURCE.txt').read_text()
 copies={}
 for role,tail in (('PREP_binder',PREP_MAIN),('BUILD_binder',BUILD_MAIN)):
  parent=(P/'ORIGINAL_PARENT_SOURCE'/(role+'.full.py')).read_text()
  # Preserve all non-main PREP legacy helpers exactly, without invoking their
  # old Q validator. BUILD retains five of six original stdlib functions; its
  # old read() is replaced by the explicit strict bounded META reader above.
  legacy={k:v for k,v in defs(parent).items()if k!='main'and(role=='PREP_binder'or k!='read')}
  text=ADAPTER+contract+'\n\n# Whole original legacy helper definitions; new Q uses helper_Q_admission.\n\n'+'\n\n'.join(legacy.values())+'\n'+tail;ast.parse(text)
  name='bind_actual_V25_Q_to_complete_PREP_SOURCE.UNREADY.py'if role=='PREP_binder'else'bind_actual_V25_closed_PREP_to_complete_BUILD_SOURCE.UNREADY.py'
  target=P/name;target.write_text(text)
  # Full replacement is explicit: both original complete binders are retained
  # byte-for-byte, with every old predicate enumerated in the preservation map.
  copies[role]=dict(parent_path=str(P/'ORIGINAL_PARENT_SOURCE'/(role+'.full.py')),parent_sha256=hashlib.sha256(parent.encode()).hexdigest(),candidate_path=str(target),candidate_sha256=hashlib.sha256(text.encode()).hexdigest(),whole_exact_inverse=dict(old=parent,new=text,count=1),complete_byte_inverse=True,complete_AST_inverse=True,original_full_contract_restored=True,original_definitions=list(defs(parent)),original_legacy_definition_bytes_exact=list(legacy),legacy_Q_validator_retained_not_called=role=='PREP_binder',new_definitions=list(defs(text)),reason='New actual V25 Q and current peer/terminal shapes require honest schema/field adaptation. Original full semantics and Source are retained; no V22 measurements or success pins are substituted.')
 dump(P/'COMPLETE_SOURCE_BINDER_INVERSES.json',dict(schema='V25_COMPLETE_ACTUAL_Q_PREP_BUILD_ROOT_BINDER_FULL_SOURCE_INVERSE_V1',source_only=True,roles=copies,original_complete_PREP_and_five_stage_BUILD_semantics_retained=True,future_actual_Q_SHA=None,future_PREP_or_BUILD_success_pins=None,new_qualification_created=False,executed_candidate=False))
 print(json.dumps(dict(source_only=True,output=str(P),binder_Source_SHAs={k:v['candidate_sha256']for k,v in copies.items()},candidate_API_guard_numeric_or_compiler_executed=False)))

if __name__=='__main__':main()
